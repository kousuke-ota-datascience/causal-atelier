"""Local publication and reader contracts."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol

from ariadne.causal.design.study import ValidatedStudy
from ariadne.scientific.ports.artifacts import ArtifactDescriptorView, StagingArtifactSink
from ariadne.shared.local_fs import LocalPrincipal, TrustedLocalRoot, VerifiedRootIdentity

OutputShape = Literal["DISCOVER_AGGREGATE_ONLY"]
RunId = str


@dataclass(frozen=True)
class PrivacyDecision:
    allowed: bool
    run_id: str
    request_hash: str
    root_identity: VerifiedRootIdentity
    principal_uid: int
    classification: Literal["AGGREGATE"]
    row_export_requested: Literal[False]
    output_shape: OutputShape


class LocalPrivacyPolicy(Protocol):
    def authorize(
        self, *, study: ValidatedStudy, root: TrustedLocalRoot, principal: LocalPrincipal,
        output_shape: OutputShape,
    ) -> PrivacyDecision: ...


class ManifestValue(Protocol):
    def to_canonical_bytes(self) -> bytes: ...


class ValidatedStagedBundle(Protocol):
    @property
    def run_id(self) -> RunId: ...
    @property
    def request_hash(self) -> str: ...


@dataclass(frozen=True)
class VerifiedLocalRun:
    run_id: RunId
    request_hash: str
    manifest: ManifestValue
    artifacts: tuple[ArtifactDescriptorView, ...]


@dataclass(frozen=True)
class CommittedLocalRun:
    verified: VerifiedLocalRun
    reused: bool
    technical_status: Literal["COMPLETED"] = "COMPLETED"


class PublicationSessionToken:
    """Opaque in-process identity for a single publication attempt."""

    __slots__ = ()


class LocalPublicationPort(Protocol):
    def begin(
        self, *, run_id: str, request_hash: str, root: TrustedLocalRoot,
        session: PublicationSessionToken | None = None,
    ) -> StagingArtifactSink: ...
    def abort(
        self, *, sink: StagingArtifactSink, session: PublicationSessionToken, run_id: str,
        request_hash: str, root: TrustedLocalRoot, reason: str,
    ) -> None: ...
    def seal(
        self, *, sink: StagingArtifactSink, manifest: ManifestValue, privacy: PrivacyDecision,
    ) -> ValidatedStagedBundle: ...
    def publish(self, *, bundle: ValidatedStagedBundle, root: TrustedLocalRoot) -> CommittedLocalRun: ...


class LocalManifestReaderPort(Protocol):
    def verify(self, *, root: TrustedLocalRoot, run_id: RunId) -> VerifiedLocalRun: ...
