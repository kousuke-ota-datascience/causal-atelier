"""G01 P02 exercising real private Linux directories and publication syscalls."""
from __future__ import annotations

import errno
import hashlib
import multiprocessing
import os
import signal
import tempfile
from dataclasses import replace
from pathlib import Path

import pytest

from ariadne.capabilities.causal.ports.local_io import PrivacyDecision
from ariadne.interfaces.cli.local_causal import publication
from ariadne.interfaces.cli.local_causal.config_decoder import StrictLocalConfigDecoder
from ariadne.interfaces.cli.local_causal.content_io import LocalContentReferenceAdapter
from ariadne.interfaces.cli.local_causal.manifest import (
    AXES, NEGATIVE_REASON, LocalRunManifest, RuntimeEvidence, ValidatedRunEvidence,
)
from ariadne.interfaces.cli.local_causal.manifest_reader import LocalManifestReader
from ariadne.interfaces.cli.local_causal.publication import LocalPublicationAdapter, PublishState
from ariadne.shared.content_ref import ContentRef, ContractViolation
from ariadne.shared.local_fs import LocalPrincipal, TrustedLocalRoot
from ariadne.shared.serialization import jcs

MIME = "application/json"
RUN = "test-run"
ROOT = Path(__file__).resolve().parents[5]
REQUEST_FILE = "study.json"


class Policy:
    def __init__(self, *, allowed=True):
        self.allowed = allowed

    def authorize(self, *, study, root, principal, output_shape):
        wire = study.to_payload()
        return PrivacyDecision(self.allowed, wire["run_id"], jcs.digest(wire), root.verify(),
                               principal.uid, "AGGREGATE", False, output_shape)


@pytest.fixture
def private_root():
    # pytest's default /tmp can be tmpfs. Exercise the checked-out ext4 volume.
    with tempfile.TemporaryDirectory(prefix=".p02-test-", dir=ROOT) as temp:
        path = Path(temp)
        with TrustedLocalRoot.open(path, allowed_directory=ROOT) as root:
            yield root, path


def _put(path, raw):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(raw)


def _study(path):
    inputs = {}
    for name in ("question", "design", "dataset"):
        raw = name.encode()
        filename = name + ".dat"
        if not (path / filename).exists():
            _put(path / filename, raw)
        inputs[name] = ContentRef(name, filename, hashlib.sha256(raw).hexdigest(), MIME, None).to_payload()
    return {
        "schema_version": "e11-local-study/1", "run_id": RUN,
        "operation": "DISCOVER", "analysis_mode": "EXPLORATORY",
        "inputs": {**inputs, "graph": None, "identification": None},
        "estimand": {"family": "GRAPH_STRUCTURE", "population": "OBSERVED_VARIABLES", "contrast": "NOT_APPLICABLE"},
        "method": {"id": "P1-M06", "backend": "causal-learn",
                   "config": {"indep_test": "fisherz", "alpha": 0.05, "depth": -1, "max_path_length": -1,
                              "background_knowledge": None}},
        "inference": {"requested": False, "confidence_level": None}, "randomness": {"seed": None},
        "privacy": {"classification": "AGGREGATE", "row_export_requested": False},
    }


def _prepare(root, path, *, negative=False, policy=None, payload=None, invalid_status=None):
    payload = _study(path) if payload is None else payload
    raw_study = jcs.canonical_bytes(payload)
    study = StrictLocalConfigDecoder().decode(raw_study, declared_format="json")
    request_hash = jcs.digest(payload)
    policy = Policy() if policy is None else policy
    decision = Policy().authorize(study=study, root=root, principal=LocalPrincipal.current(),
                                  output_shape="DISCOVER_AGGREGATE_ONLY")
    facade = LocalPublicationAdapter(policy)
    sink = facade.begin(run_id=RUN, request_hash=request_hash, root=root)
    reasons = [NEGATIVE_REASON] if negative else []
    status = {"schema_version": "e11-local-status/1", "run_id": RUN, "technical_status": "COMPLETED",
              **AXES, "reason_codes": reasons, "manifest_relative_path": f"runs/{RUN}/manifest.json"}
    staged_status = status if invalid_status is None else {**status, **invalid_status}
    artifacts = [
        sink.stage_bytes(REQUEST_FILE, raw_study, MIME, "AGGREGATE"),
        sink.stage_bytes("status.json", jcs.canonical_bytes(staged_status), MIME, "AGGREGATE"),
    ]
    if negative:
        raw = jcs.canonical_bytes({"run_id": RUN, "operation": "DISCOVER", "method_id": "P1-M06",
                                   "reason_codes": reasons})
        artifacts.append(sink.stage_bytes("diagnostics.json", raw, MIME, "AGGREGATE"))
        graph_ref = None
    else:
        graph = {"schema_version": "e11-local-graph/1", "kind": "PAG", "version_id": None,
                 "parent_version_id": None, "nodes": ["a", "b"], "edges": [], "temporal": None, "provenance": {}}
        raw = jcs.canonical_bytes({**graph, "content_hash": jcs.digest(graph)})
        output = sink.stage_bytes("graph.json", raw, MIME, "AGGREGATE")
        artifacts.append(output)
        graph_ref = ContentRef("synthetic", f"runs/{RUN}/graph.json", output.sha256, MIME, "e11-local-graph/1")
    manifest = LocalRunManifest.from_run_evidence(
        ValidatedRunEvidence(study, payload, status, RuntimeEvidence("fixture", False, "3.12", "Linux",
                             "a" * 64, {}, {}), {}, tuple(artifacts), graph_ref, tuple(reasons), None)
    )
    return facade, sink, manifest, decision


@pytest.mark.parametrize("negative", [False, True])
def test_real_publish_reader_and_equal_value_decision(private_root, negative):
    root, path = private_root
    facade, sink, manifest, decision = _prepare(root, path, negative=negative)
    clone = replace(decision)
    assert clone == decision and clone is not decision
    bundle = facade.seal(sink=sink, manifest=manifest, privacy=clone)
    assert not (path / "runs").exists()
    committed = facade.publish(bundle=bundle, root=root)
    assert committed.technical_status == "COMPLETED" and not committed.reused
    run = LocalManifestReader().verify(root=root, run_id=RUN)
    assert run.manifest.to_canonical_bytes() == manifest.to_canonical_bytes()
    assert (path / "runs" / RUN).stat().st_mode & 0o777 == 0o700
    assert all(file.stat().st_mode & 0o777 == 0o600 for file in (path / "runs" / RUN).iterdir())
    with pytest.raises(ContractViolation):
        facade.publish(bundle=bundle, root=root)


@pytest.mark.parametrize("change", ["missing", "deny", "uid", "run", "hash", "other_fd", "policy"])
def test_privacy_rejects_before_marker(private_root, change):
    root, path = private_root
    policy = Policy(allowed=change != "policy")
    facade, sink, manifest, decision = _prepare(root, path, policy=policy)
    with TrustedLocalRoot.open(path, allowed_directory=ROOT) as other:
        candidates = {"missing": None, "deny": replace(decision, allowed=False),
                      "uid": replace(decision, principal_uid=0), "run": replace(decision, run_id="other"),
                      "hash": replace(decision, request_hash="b" * 64),
                      "other_fd": replace(decision, root_identity=other.verify()), "policy": decision}
        with pytest.raises(ContractViolation) as caught:
            facade.seal(sink=sink, manifest=manifest, privacy=candidates[change])
    assert caught.value.reason.code == "PRIVACY_POLICY_CONFLICT"
    assert not list(path.glob(".staging/*/_COMMITTED.json"))
    assert not (path / "runs").exists()


@pytest.mark.parametrize("invalid", [
    b'{}',
    b'{"run_id":"other","operation":"DISCOVER","method_id":"P1-M06","reason_codes":["SCI_NO_ADMISSIBLE_PAG"]}',
    b'{"run_id":"test-run","operation":"DISCOVER","method_id":"P1-M06","reason_codes":["EXECUTION_FAILED"]}',
    b'{"run_id":"test-run","run_id":"test-run","operation":"DISCOVER","method_id":"P1-M06","reason_codes":["SCI_NO_ADMISSIBLE_PAG"]}',
    b'{"run_id":"test-run","operation":"DISCOVER","method_id":"P1-M06","reason_codes":["SCI_NO_ADMISSIBLE_PAG"],"extra":0}',
])
def test_diagnostics_detected_before_seal_even_with_correct_hash(private_root, invalid):
    root, path = private_root
    assert root.verify().owner_uid == os.geteuid()
    facade, sink, manifest, decision = _prepare(root, path, negative=True)
    stage = next(path.glob(".staging/*"))
    (stage / "diagnostics.json").write_bytes(invalid)
    # Simulate internally consistent descriptors to reach the semantic check.
    payload = jcs.parse_json(manifest.to_canonical_bytes())
    for item in payload["artifacts"]:
        if item["key"] == "diagnostics.json":
            item.update(sha256=hashlib.sha256(invalid).hexdigest(), size_bytes=len(invalid))
    changed = LocalRunManifest.from_payload(payload)
    with pytest.raises(ContractViolation, match="diagnostics payload|strict JSON"):
        facade.seal(sink=sink, manifest=changed, privacy=decision)
    assert not (stage / "_COMMITTED.json").exists()


def test_status_reason_must_join_negative(private_root):
    root, path = private_root
    facade, sink, manifest, decision = _prepare(root, path, negative=True, invalid_status={"reason_codes": []})
    with pytest.raises(ContractViolation, match="Status and Manifest"):
        facade.seal(sink=sink, manifest=manifest, privacy=decision)
    assert not list(path.glob(".staging/*/_COMMITTED.json"))


@pytest.mark.parametrize("change", ["mode", "symlink", "hardlink", "bytes", "missing"])
def test_content_reference_rejects_unsafe_file(private_root, change):
    root, path = private_root
    payload = _study(path)
    ref = ContentRef.from_payload(payload["inputs"]["question"])
    adapter = LocalContentReferenceAdapter()
    assert adapter.verify(ref, root=root).data == b"question"
    target = path / ref.relative_key
    if change == "mode":
        target.chmod(0o644)
    elif change == "symlink":
        target.unlink()
        target.symlink_to("design.dat")
    elif change == "hardlink":
        os.link(target, path / "duplicate")
    elif change == "bytes":
        target.write_bytes(b"change")
    else:
        target.unlink()
    with pytest.raises(ContractViolation):
        adapter.verify(ref, root=root)


def test_root_rejects_symlink_permissions_and_outside(private_root):
    root, path = private_root
    (path / "alias").symlink_to(path, target_is_directory=True)
    with pytest.raises(ContractViolation):
        TrustedLocalRoot.open(path / "alias", allowed_directory=path)
    with pytest.raises(ContractViolation):
        TrustedLocalRoot.open(path.parent, allowed_directory=path)
    path.chmod(0o755)
    with pytest.raises(ContractViolation):
        root.verify()


def test_sealed_mutation_and_marker_tamper(private_root):
    root, path = private_root
    facade, sink, manifest, decision = _prepare(root, path)
    sealed = facade.seal(sink=sink, manifest=manifest, privacy=decision)
    stage = next(path.glob(".staging/*"))
    (stage / "status.json").write_bytes(b"{}")
    with pytest.raises(ContractViolation, match="Artifact byte"):
        facade.publish(bundle=sealed, root=root)
    facade, sink, manifest, decision = _prepare(root, path)
    facade.publish(bundle=facade.seal(sink=sink, manifest=manifest, privacy=decision), root=root)
    (path / "runs" / RUN / "manifest.json").write_bytes(b"{}")
    with pytest.raises(ContractViolation) as caught:
        LocalManifestReader().verify(root=root, run_id=RUN)
    assert caught.value.reason.code == "MANIFEST_HASH_MISMATCH"


def _race_worker(root, path, barrier, results, changed):
    payload = _study(path)
    if changed:
        payload["randomness"]["seed"] = 1
    facade, sink, manifest, decision = _prepare(root, path, payload=payload)
    sealed = facade.seal(sink=sink, manifest=manifest, privacy=decision)
    barrier.wait(timeout=10)
    try:
        committed = facade.publish(bundle=sealed, root=root)
        results.put(("COMPLETED", committed.reused))
    except ContractViolation as error:
        results.put((error.reason.code, False))


@pytest.mark.parametrize("same", [True, False])
def test_real_two_process_noreplace(private_root, same):
    root, path = private_root
    _study(path)
    ctx = multiprocessing.get_context("fork")
    results, barrier = ctx.Queue(), ctx.Barrier(2)
    workers = [ctx.Process(target=_race_worker, args=(root, path, barrier, results, changed))
               for changed in (False, not same)]
    for worker in workers:
        worker.start()
    try:
        observed = {results.get(timeout=15) for _ in workers}
    finally:
        for worker in workers:
            worker.join(timeout=3)
            if worker.is_alive():
                worker.kill()
                worker.join()
    assert observed == {("COMPLETED", False), ("COMPLETED" if same else "RUN_ID_CONFLICT", same)}
    assert len(list((path / "runs").iterdir())) == 1
    assert LocalManifestReader().verify(root=root, run_id=RUN).run_id == RUN


@pytest.mark.parametrize("after", [False, True])
def test_real_sigkill_at_rename_boundary(private_root, monkeypatch, after):
    root, path = private_root
    facade, sink, manifest, decision = _prepare(root, path)
    bundle = facade.seal(sink=sink, manifest=manifest, privacy=decision)
    real_rename = publication._rename_noreplace

    def kill_at_boundary(*args):
        if after:
            real_rename(*args)
        os.kill(os.getpid(), signal.SIGKILL)

    with monkeypatch.context() as patch:
        patch.setattr(publication, "_rename_noreplace", kill_at_boundary)
        child = multiprocessing.get_context("fork").Process(target=facade.publish, kwargs={"bundle": bundle, "root": root})
        child.start()
        child.join(timeout=10)
        if child.is_alive():
            child.kill()
            child.join()
            pytest.fail("Fault process hung")
    assert child.exitcode == -signal.SIGKILL
    if after:
        assert LocalManifestReader().verify(root=root, run_id=RUN).run_id == RUN
    else:
        assert not (path / "runs" / RUN).exists()
    sink._publisher.abort("release parent's staging handles")


def test_post_rename_fsync_error_is_indeterminate(private_root, monkeypatch):
    root, path = private_root
    facade, sink, manifest, decision = _prepare(root, path)
    bundle = facade.seal(sink=sink, manifest=manifest, privacy=decision)
    real_fsync = os.fsync

    def fail_after_rename(fd):
        if (path / "runs" / RUN).exists():
            raise OSError(errno.EIO, "injected directory fsync fault")
        real_fsync(fd)

    with monkeypatch.context() as patch:
        patch.setattr(publication.os, "fsync", fail_after_rename)
        with pytest.raises(ContractViolation) as caught:
            facade.publish(bundle=bundle, root=root)
    assert caught.value.reason.code == "PUBLICATION_INDETERMINATE"
    assert sink._publisher.state is PublishState.INDETERMINATE
    assert (path / "runs" / RUN / "_COMMITTED.json").is_file()


def _inject_kernel_errno(syscall, code):
    import ctypes

    library = ctypes.CDLL("libseccomp.so.2")
    library.seccomp_init.argtypes = [ctypes.c_uint32]
    library.seccomp_init.restype = ctypes.c_void_p
    library.seccomp_syscall_resolve_name.argtypes = [ctypes.c_char_p]
    library.seccomp_syscall_resolve_name.restype = ctypes.c_int
    library.seccomp_rule_add_array.argtypes = [
        ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int, ctypes.c_uint, ctypes.c_void_p,
    ]
    library.seccomp_load.argtypes = [ctypes.c_void_p]
    library.seccomp_release.argtypes = [ctypes.c_void_p]
    allow = 0x7FFF0000
    return_errno = 0x00050000 | code
    context = library.seccomp_init(allow)
    assert context
    try:
        number = library.seccomp_syscall_resolve_name(syscall.encode())
        assert number >= 0
        assert library.seccomp_rule_add_array(context, return_errno, number, 0, None) == 0
        assert library.seccomp_load(context) == 0
        return number
    finally:
        library.seccomp_release(context)


def _kernel_fault_worker(facade, sink, manifest, decision, root, syscall, code, result):
    if syscall == "renameat2":
        bundle = facade.seal(sink=sink, manifest=manifest, privacy=decision)
    import ctypes

    number = _inject_kernel_errno(syscall, code)
    libc = ctypes.CDLL(None, use_errno=True)
    # The filter denies this raw syscall before its arguments are examined.
    assert libc.syscall(number, -1, 0, -1, 0, 1) == -1
    assert ctypes.get_errno() == code
    try:
        if syscall == "fsync":
            facade.seal(sink=sink, manifest=manifest, privacy=decision)
        else:
            facade.publish(bundle=bundle, root=root)
    except ContractViolation as error:
        cause = error.__cause__
        result.put((error.reason.code, cause.errno if isinstance(cause, OSError) else None))


@pytest.mark.parametrize(("syscall", "code"), [
    ("fsync", errno.ENOSPC),
    ("renameat2", errno.ENOSYS),
    ("renameat2", errno.EINVAL),
    ("renameat2", errno.EOPNOTSUPP),
    ("renameat2", errno.EXDEV),
])
def test_kernel_faults_on_real_ext4_do_not_publish(private_root, syscall, code):
    root, path = private_root
    facade, sink, manifest, decision = _prepare(root, path)
    context = multiprocessing.get_context("fork")
    result = context.Queue()
    child = context.Process(target=_kernel_fault_worker,
                            args=(facade, sink, manifest, decision, root, syscall, code, result))
    child.start()
    try:
        child.join(timeout=10)
        assert child.exitcode == 0
        error_code, observed_errno = result.get(timeout=3)
        assert error_code == "PUBLICATION_FAILED"
        # glibc can translate ENOSYS to EINVAL for renameat2 with nonzero flags.
        assert observed_errno in ({errno.ENOSYS, errno.EINVAL} if code == errno.ENOSYS else {code})
    finally:
        if child.is_alive():
            child.kill()
            child.join()
        sink._publisher.abort("release parent's staging handles")
    assert not (path / "runs" / RUN).exists()
    if syscall == "fsync":
        assert not list(path.glob(".staging/*/_COMMITTED.json"))


def test_reader_checks_diagnostics_semantics_even_with_matching_hashes(private_root):
    root, path = private_root
    facade, sink, manifest, decision = _prepare(root, path, negative=True)
    facade.publish(bundle=facade.seal(sink=sink, manifest=manifest, privacy=decision), root=root)
    destination = path / "runs" / RUN
    invalid = b"{}"
    (destination / "diagnostics.json").write_bytes(invalid)
    payload = jcs.parse_json(manifest.to_canonical_bytes())
    for descriptor in payload["artifacts"]:
        if descriptor["key"] == "diagnostics.json":
            descriptor.update(size_bytes=len(invalid), sha256=hashlib.sha256(invalid).hexdigest())
    raw_manifest = jcs.canonical_bytes(payload)
    (destination / "manifest.json").write_bytes(raw_manifest)
    marker = jcs.parse_json((destination / "_COMMITTED.json").read_bytes())
    marker["manifest_sha256"] = hashlib.sha256(raw_manifest).hexdigest()
    (destination / "_COMMITTED.json").write_bytes(jcs.canonical_bytes(marker))
    with pytest.raises(ContractViolation, match="diagnostics payload"):
        LocalManifestReader().verify(root=root, run_id=RUN)


def test_ref_detects_real_inode_replacement(private_root, monkeypatch):
    root, path = private_root
    payload = _study(path)
    ref = ContentRef.from_payload(payload["inputs"]["question"])
    target = path / ref.relative_key
    replacement = path / "replacement"
    _put(replacement, target.read_bytes())
    real_stat = os.stat

    def stat_after_replace(filename, *args, **kwargs):
        if filename == ref.relative_key and kwargs.get("dir_fd") is not None:
            replacement.replace(target)
        return real_stat(filename, *args, **kwargs)

    with monkeypatch.context() as patch:
        patch.setattr(os, "stat", stat_after_replace)
        with pytest.raises(ContractViolation, match="identity or size changed"):
            LocalContentReferenceAdapter().verify(ref, root=root)


def test_row_and_extra_inventory_are_denied(private_root):
    root, path = private_root
    facade, sink, manifest, decision = _prepare(root, path)
    with pytest.raises(ContractViolation) as caught:
        sink.stage_bytes("rows.parquet", b"secret", "application/vnd.apache.parquet", "RESTRICTED_ROW_LEVEL")
    assert caught.value.reason.code == "PRIVACY_POLICY_CONFLICT"
    assert not list(path.glob(".staging/*/rows.parquet"))
    facade, sink, manifest, decision = _prepare(root, path)
    stages = list(path.glob(".staging/*"))
    for stage in stages:
        _put(stage / "extra.json", b"{}")
    with pytest.raises(ContractViolation, match="Unexpected or missing"):
        facade.seal(sink=sink, manifest=manifest, privacy=decision)
    assert not list(path.glob(".staging/*/_COMMITTED.json"))


def test_tmpfs_root_is_rejected():
    with tempfile.TemporaryDirectory(dir="/dev/shm") as name:
        path = Path(name)
        with pytest.raises(ContractViolation, match="ext4 or XFS"):
            TrustedLocalRoot.open(path, allowed_directory=Path("/dev/shm"))


def test_cross_run_dirfd_replacement_is_refused_before_rename(private_root):
    root, path = private_root
    facade, sink, manifest, decision = _prepare(root, path)
    stage = next(path.glob(".staging/*"))
    stage.rename(path / "detached")
    stage.mkdir(mode=0o700)
    with pytest.raises(ContractViolation) as caught:
        facade.seal(sink=sink, manifest=manifest, privacy=decision)
    assert caught.value.reason.code == "PRIVACY_POLICY_CONFLICT"
    assert not (path / "runs").exists()
    assert not (path / "detached" / "_COMMITTED.json").exists()


def test_reader_rejects_legacy_manifest_even_with_matching_marker(private_root):
    root, path = private_root
    facade, sink, manifest, decision = _prepare(root, path)
    facade.publish(bundle=facade.seal(sink=sink, manifest=manifest, privacy=decision), root=root)
    committed = path / "runs" / RUN
    legacy = jcs.parse_json(manifest.to_canonical_bytes())
    legacy["manifest_version"] = "2.0"
    raw = jcs.canonical_bytes(legacy)
    (committed / "manifest.json").write_bytes(raw)
    marker = jcs.parse_json((committed / "_COMMITTED.json").read_bytes())
    marker["manifest_sha256"] = hashlib.sha256(raw).hexdigest()
    (committed / "_COMMITTED.json").write_bytes(jcs.canonical_bytes(marker))
    with pytest.raises(ContractViolation) as caught:
        LocalManifestReader().verify(root=root, run_id=RUN)
    assert caught.value.reason.code == "VERSION_UNSUPPORTED"
