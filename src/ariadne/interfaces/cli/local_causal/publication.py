"""Single-run private staging and atomic Linux publication."""
from __future__ import annotations

import ctypes
import errno
import os
import secrets
from contextlib import ExitStack
from dataclasses import dataclass
from enum import Enum, auto

from ariadne.capabilities.causal.ports.local_io import (
    CommittedLocalRun, LocalPrivacyPolicy, ManifestValue, PrivacyDecision, ValidatedStagedBundle,
)
from ariadne.interfaces.cli.local_causal.config_decoder import StrictLocalConfigDecoder
from ariadne.interfaces.cli.local_causal.manifest import ArtifactDescriptor, LocalRunManifest
from ariadne.interfaces.cli.local_causal.manifest_reader import (
    ARTIFACT_KEYS, DIAGNOSTICS, MANIFEST, MARKER, LocalManifestReader,
    _check, _hash, _named_directory, _validate_graph, _verify_artifacts, publication_error,
    validate_diagnostics, validate_status,
)
from ariadne.interfaces.cli.local_causal.study import safe_run_id
from ariadne.scientific.ports.artifacts import StagingArtifactSink
from ariadne.shared.content_ref import ContractViolation, valid_sha256
from ariadne.shared.local_fs import (
    LocalPrincipal, TrustedLocalRoot, VerifiedRootIdentity, _check_fd, private_directory, read_private_file,
)
from ariadne.shared.serialization import jcs

_OUTPUT_SHAPE = "DISCOVER_AGGREGATE_ONLY"
_LIBC = ctypes.CDLL(None, use_errno=True)
_RENAME_NOREPLACE = 1


def _rename_noreplace(source_fd: int, source: str, target_fd: int, target: str) -> None:
    rename = getattr(_LIBC, "renameat2", None)
    if rename is None:
        raise OSError(errno.ENOSYS, "renameat2 unavailable")
    if rename(source_fd, os.fsencode(source), target_fd, os.fsencode(target), _RENAME_NOREPLACE):
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error))


def _privacy_error() -> ContractViolation:
    return ContractViolation("PRIVACY_POLICY_CONFLICT", "privacy", "Publication privacy bindings did not authorize the bundle")


def _write_private(fd: int, key: str, raw: bytes, identity: VerifiedRootIdentity) -> bytes:
    flags = os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC
    output = os.open(key, flags, 0o600, dir_fd=fd)
    try:
        _check_fd(output, identity, directory=False)
        with os.fdopen(output, "w+b", closefd=False) as stream:
            stream.write(raw)
            stream.flush()
            stream.seek(0)
            observed = stream.read()
        info = _check_fd(output, identity, directory=False)
        _check(info.st_size == len(raw) and observed == raw, "Staging byte readback differs")
        os.fsync(output)
        return observed
    finally:
        os.close(output)


class PublishState(Enum):
    PREPARING = auto()
    STAGING = auto()
    VALIDATING = auto()
    PUBLISHING = auto()
    COMMITTED = auto()
    ABORTED = auto()
    INDETERMINATE = auto()


@dataclass(frozen=True)
class StagingHandle:
    parent: int
    directory: int
    token: str


@dataclass(frozen=True)
class _Sink:
    _publisher: LocalArtifactPublisher

    def stage_bytes(self, key: str, data: bytes, media_type: str, classification: str) -> ArtifactDescriptor:
        return self._publisher.stage_bytes(key, data, media_type, classification)


@dataclass(frozen=True)
class ValidatedBundle:
    _publisher: LocalArtifactPublisher
    run_id: str
    request_hash: str
    root_identity: VerifiedRootIdentity
    manifest: LocalRunManifest
    artifacts: tuple[ArtifactDescriptor, ...]
    privacy: PrivacyDecision
    marker: bytes


class LocalArtifactPublisher:
    def __init__(
        self, root: TrustedLocalRoot, run_id: str, request_hash: str, permission_policy: LocalPrivacyPolicy,
    ):
        _check(safe_run_id(run_id) and valid_sha256(request_hash), "Invalid run identity")
        self._identity = root.verify()
        self._root = root
        self._run_id = run_id
        self._request_hash = request_hash
        self._permission_policy = permission_policy
        self._state = PublishState.PREPARING
        self._handles = ExitStack()
        self._staging_handle: StagingHandle | None = None
        self._artifacts: tuple[ArtifactDescriptor, ...] = ()
        self._sink = _Sink(self)
        self._validated: ValidatedBundle | None = None

    root = property(lambda self: self._root)
    run_id = property(lambda self: self._run_id)
    request_hash = property(lambda self: self._request_hash)
    permission_policy = property(lambda self: self._permission_policy)
    state = property(lambda self: self._state)
    staging_handle = property(lambda self: self._staging_handle)
    artifacts = property(lambda self: self._artifacts)

    def _require_state(self, expected: PublishState) -> None:
        _check(self.state is expected, "Invalid publication state", "PUBLICATION_FAILED")

    def _check_live(self) -> None:
        _check(self.root.verify() == self._identity, "Publication root changed")
        handle = self._staging_handle
        if handle is not None:
            _named_directory(self.root.fileno(), ".staging", handle.parent, self._identity)
            _named_directory(handle.parent, handle.token, handle.directory, self._identity)

    def _validate_staging_payload(self, key: str, data: bytes) -> None:
        if key == "study.json":
            study = StrictLocalConfigDecoder().decode(data, declared_format="json").to_payload()
            _check(study["run_id"] == self.run_id and jcs.digest(study) == self.request_hash,
                   "Staged Study belongs to a different request")
        elif key == "status.json":
            validate_status(data, self.run_id)
        elif key == DIAGNOSTICS:
            validate_diagnostics(data, self.run_id)
        else:
            _validate_graph(data)

    def _close_handles(self) -> None:
        self._handles.close()
        self._staging_handle = None

    def begin(self) -> StagingArtifactSink:
        self._require_state(PublishState.PREPARING)
        try:
            root_fd = self.root.fileno()
            parent = self._handles.enter_context(
                private_directory(root_fd, ".staging", self._identity, create=True)
            )
            token = secrets.token_hex(24)
            os.mkdir(token, 0o700, dir_fd=parent)
            directory = self._handles.enter_context(private_directory(parent, token, self._identity))
            self._staging_handle = StagingHandle(parent, directory, token)
            os.fsync(parent)
            os.fsync(root_fd)
            self._state = PublishState.STAGING
            return self._sink
        except (OSError, ContractViolation) as error:
            self.abort("begin failed")
            raise publication_error("PUBLICATION_FAILED", "Could not begin local staging") from error

    def stage_bytes(self, key: str, data: bytes, media_type: str, classification: str) -> ArtifactDescriptor:
        self._require_state(PublishState.STAGING)
        try:
            _check(type(key) is str, "Artifact key must be text")
            if classification != "AGGREGATE" or key.endswith(".parquet"):
                raise _privacy_error()
            _check(key in ARTIFACT_KEYS and all(item.key != key for item in self._artifacts),
                   "Invalid or duplicate staged artifact key")
            _check(type(data) is bytes and bool(data) and media_type == "application/json",
                   "Invalid staged artifact bytes or media type")
            self._validate_staging_payload(key, data)
            self._check_live()
            handle = self._staging_handle
            observed = _write_private(handle.directory, key, data, self._identity)
            descriptor = ArtifactDescriptor(key, _hash(observed), len(observed), media_type, classification, "PRIVATE")
            self._artifacts += (descriptor,)
            return descriptor
        except (OSError, ContractViolation) as error:
            self.abort("artifact staging failed")
            if isinstance(error, ContractViolation):
                raise
            raise publication_error("PUBLICATION_FAILED", "Artifact staging failed") from error

    def validate(self, manifest: LocalRunManifest, *, privacy: PrivacyDecision) -> ValidatedBundle:
        self._require_state(PublishState.STAGING)
        self._state = PublishState.VALIDATING
        try:
            _check(type(manifest) is LocalRunManifest, "Expected a validated LocalRunManifest")
            if type(privacy) is not PrivacyDecision or privacy.allowed is not True:
                raise _privacy_error()
            try:
                self._check_live()
            except (OSError, ContractViolation) as error:
                raise _privacy_error() from error
            handle = self._staging_handle
            payload, inventory, study = _verify_artifacts(
                handle.directory, self._identity, manifest, metadata=set(),
            )
            _check((payload["run_id"], payload["request_hash"]) == (self.run_id, self.request_hash),
                   "Manifest belongs to a different request")
            _check({item.key: item for item in inventory} == {item.key: item for item in self.artifacts},
                   "Manifest does not match staging evidence")
            principal = LocalPrincipal.current()
            expected = PrivacyDecision(True, self.run_id, self.request_hash, self._identity, principal.uid,
                                       "AGGREGATE", False, _OUTPUT_SHAPE)
            current = self.permission_policy.authorize(
                study=study, root=self.root, principal=principal, output_shape=_OUTPUT_SHAPE,
            )
            if not _same_decision(expected, privacy) or not _same_decision(expected, current):
                raise _privacy_error()
            raw = manifest.to_canonical_bytes()
            marker = jcs.canonical_bytes({"marker_version": "e11-commit/1", "run_id": self.run_id,
                                         "request_hash": self.request_hash, "manifest_sha256": _hash(raw)})
            _write_private(handle.directory, MANIFEST, raw, self._identity)
            _write_private(handle.directory, MARKER, marker, self._identity)
            os.fsync(handle.directory)
            os.fsync(handle.parent)
            self._validated = ValidatedBundle(self, self.run_id, self.request_hash, self._identity,
                                              manifest, inventory, privacy, marker)
            return self._validated
        except (OSError, ContractViolation) as error:
            self.abort("bundle validation failed")
            if isinstance(error, ContractViolation):
                raise
            raise publication_error("PUBLICATION_FAILED", "Bundle could not be sealed") from error

    def _recheck_sealed(self, validated: ValidatedBundle) -> None:
        self._check_live()
        handle = self._staging_handle
        _check(read_private_file(handle.directory, MANIFEST, self._identity) == validated.manifest.to_canonical_bytes()
               and read_private_file(handle.directory, MARKER, self._identity) == validated.marker,
               "Sealed Manifest or Marker was modified", "MANIFEST_HASH_MISMATCH")
        _verify_artifacts(handle.directory, self._identity, validated.manifest, metadata={MANIFEST, MARKER})

    def commit(self, validated: ValidatedBundle) -> CommittedLocalRun:
        self._require_state(PublishState.VALIDATING)
        _check(self._validated is not None and validated is self._validated, "Bundle does not belong to this publisher")
        renamed = False
        reused = False
        self._state = PublishState.PUBLISHING
        try:
            self._recheck_sealed(validated)
            handle = self._staging_handle
            identity = self.root.verify()
            root_fd = self.root.fileno()
            with private_directory(root_fd, "runs", identity, create=True) as runs:
                os.fsync(root_fd)
                self._check_live()
                _named_directory(root_fd, "runs", runs, identity)
                try:
                    _rename_noreplace(handle.parent, handle.token, runs, self.run_id)
                    renamed = True
                except FileExistsError:
                    reused = True
                except OSError as error:
                    # A failed Linux operation with an unclassified errno is not proof of non-publication.
                    renamed = error.errno not in {errno.ENOSYS, errno.EINVAL, errno.EOPNOTSUPP, errno.EXDEV,
                                                  errno.EPERM, errno.EACCES, errno.ENOENT, errno.ENOTDIR,
                                                  errno.ENOSPC, errno.EROFS}
                    raise
                os.fsync(handle.parent)
                os.fsync(runs)
                verified = LocalManifestReader().read_run(self.root, self.run_id)
                if renamed:
                    _named_directory(runs, self.run_id, handle.directory, identity)
                if verified.manifest.to_canonical_bytes() != validated.manifest.to_canonical_bytes():
                    raise publication_error("RUN_ID_CONFLICT", "Existing run differs from sealed candidate")
            self._state = PublishState.COMMITTED
            self._close_handles()
            return CommittedLocalRun(verified, reused)
        except (OSError, ContractViolation) as error:
            if renamed:
                self._state = PublishState.INDETERMINATE
                self._close_handles()
                raise publication_error("PUBLICATION_INDETERMINATE", "Published run could not be verified") from error
            self.abort("publication failed before rename")
            if reused:
                raise publication_error("RUN_ID_CONFLICT", "Existing run could not be reused") from error
            if isinstance(error, ContractViolation):
                raise
            raise publication_error("PUBLICATION_FAILED", "Atomic publication failed") from error

    def abort(self, reason: str) -> None:
        _check(self.state not in (PublishState.COMMITTED, PublishState.INDETERMINATE),
               "Published runs cannot be aborted", "PUBLICATION_FAILED")
        handle = self._staging_handle
        if handle is not None:
            # The unpredictable private staging name quarantines any residue.
            # Only release our handles here; never delete a potentially published run.
            self._close_handles()
        else:
            self._handles.close()
        self._state = PublishState.ABORTED


def _same_decision(first: PrivacyDecision, second: object) -> bool:
    return type(second) is PrivacyDecision and all(
        type(getattr(first, name)) is type(getattr(second, name))
        and getattr(first, name) == getattr(second, name)
        for name in PrivacyDecision.__annotations__
    )


class LocalPublicationAdapter:
    def __init__(self, permission_policy: LocalPrivacyPolicy):
        self._permission_policy = permission_policy

    def begin(self, *, run_id: str, request_hash: str, root: TrustedLocalRoot) -> StagingArtifactSink:
        return LocalArtifactPublisher(root, run_id, request_hash, self._permission_policy).begin()

    def seal(
        self, *, sink: StagingArtifactSink, manifest: ManifestValue, privacy: PrivacyDecision,
    ) -> ValidatedBundle:
        _check(type(sink) is _Sink and sink is sink._publisher._sink and type(manifest) is LocalRunManifest
               and sink._publisher.permission_policy is self._permission_policy, "Invalid staging sink or Manifest")
        return sink._publisher.validate(manifest, privacy=privacy)

    def publish(self, *, bundle: ValidatedStagedBundle, root: TrustedLocalRoot) -> CommittedLocalRun:
        _check(type(bundle) is ValidatedBundle and bundle._publisher.root is root
               and bundle._publisher.permission_policy is self._permission_policy, "Invalid publication bundle")
        return bundle._publisher.commit(bundle)
