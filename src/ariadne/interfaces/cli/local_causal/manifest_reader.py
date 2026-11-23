"""Independent read-only verification of a committed local bundle."""
from __future__ import annotations

import hashlib
import os

from ariadne.capabilities.causal.ports.local_io import RunId, VerifiedLocalRun
from ariadne.causal.discovery.graph_evidence import GraphEvidence
from ariadne.interfaces.cli.local_causal.config_decoder import StrictLocalConfigDecoder
from ariadne.interfaces.cli.local_causal.content_io import LocalContentReferenceAdapter
from ariadne.interfaces.cli.local_causal.manifest import (
    AXES, GRAPH_VERSION, NEGATIVE_REASON, STATUS_VERSION, ArtifactDescriptor, LocalRunManifest,
)
from ariadne.interfaces.cli.local_causal.study import fields, safe_run_id
from ariadne.shared.content_ref import ContentRef, ContractViolation, nonempty_text, valid_sha256
from ariadne.shared.local_fs import (
    TrustedLocalRoot, VerifiedRootIdentity, _check_fd, private_directory, read_private_file,
)
from ariadne.shared.serialization import jcs

MARKER = "_COMMITTED.json"
MANIFEST = "manifest.json"
DIAGNOSTICS = "diagnostics.json"
ARTIFACT_KEYS = frozenset({"study.json", "status.json", "graph.json", DIAGNOSTICS})


def publication_error(code: str, message: str) -> ContractViolation:
    return ContractViolation(code, "publication", message)


def _check(condition: bool, message: str, code: str = "SCHEMA_INVALID") -> None:
    if not condition:
        raise publication_error(code, message)


def _hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _json(raw: bytes):
    try:
        return jcs.parse_json(raw)
    except (ValueError, RecursionError) as error:
        raise publication_error("SCHEMA_INVALID", "Invalid strict JSON artifact") from error


def validate_diagnostics(raw: bytes, run_id: str) -> None:
    _check(
        _json(raw) == {"run_id": run_id, "operation": "DISCOVER", "method_id": "P1-M06",
                       "reason_codes": [NEGATIVE_REASON]},
        "Invalid G01 Graph-negative diagnostics payload",
    )



def validate_status(raw: bytes, run_id: str, *, negative: bool | None = None) -> None:
    status = _json(raw)
    expected = {
        "schema_version": STATUS_VERSION, "run_id": run_id, "technical_status": "COMPLETED",
        **AXES, "manifest_relative_path": f"runs/{run_id}/manifest.json",
    }
    permitted = ([], [NEGATIVE_REASON]) if negative is None else ([NEGATIVE_REASON] if negative else [],)
    _check(any(status == {**expected, "reason_codes": codes} for codes in permitted),
           "Status and Manifest disagree")

def _validate_graph(raw: bytes) -> None:
    graph = fields(
        _json(raw), "schema_version kind version_id parent_version_id nodes edges temporal provenance content_hash",
        "publication",
    )
    _check(graph["schema_version"] == GRAPH_VERSION and graph["kind"] == "PAG"
           and graph["version_id"] is None and graph["parent_version_id"] is None
           and graph["temporal"] is None, "Invalid standalone G01 PAG envelope")
    nodes, edges = graph["nodes"], graph["edges"]
    _check(type(nodes) is list and bool(nodes) and all(nonempty_text(node) for node in nodes)
           and len(set(nodes)) == len(nodes) and type(edges) is list and type(graph["provenance"]) is dict,
           "Invalid Graph structure")
    pairs = set()
    for item in edges:
        edge = fields(item, "source target source_mark target_mark lag", "publication")
        source, target = edge["source"], edge["target"]
        _check(source in nodes and target in nodes and source != target and edge["lag"] is None
               and all(edge[name] in ("TAIL", "ARROW", "CIRCLE") for name in ("source_mark", "target_mark")),
               "Invalid Graph edge")
        pair = frozenset((source, target))
        _check(pair not in pairs, "Duplicate Graph edge")
        pairs.add(pair)
    projection = {key: value for key, value in graph.items() if key != "content_hash"}
    _check(jcs.digest(projection) == graph["content_hash"], "Graph content digest mismatch",
           "ARTIFACT_HASH_MISMATCH")


def _verify_artifacts(
    directory: int, identity: VerifiedRootIdentity, manifest: LocalRunManifest, *, metadata: set[str],
    verify_graph_provenance: bool = False,
):
    payload = _json(manifest.to_canonical_bytes())
    inventory = tuple(ArtifactDescriptor(**item) for item in payload["artifacts"])
    expected_keys = {item.key for item in inventory} | metadata
    _check(set(os.listdir(directory)) == expected_keys, "Unexpected or missing bundle files",
           "PRIVATE_ARTIFACT_DENIED")
    files = {}
    for descriptor in inventory:
        raw = read_private_file(directory, descriptor.key, identity)
        _check(len(raw) == descriptor.size_bytes and _hash(raw) == descriptor.sha256,
               "Artifact byte size or digest mismatch", "ARTIFACT_HASH_MISMATCH")
        files[descriptor.key] = raw

    study = StrictLocalConfigDecoder().decode(files["study.json"], declared_format="json")
    study_payload = study.to_payload()
    run_id = payload["run_id"]
    _check(study_payload["run_id"] == run_id and payload["request_hash"] == jcs.digest(study_payload)
           and study_payload["operation"] == payload["operation"]
           and study_payload["analysis_mode"] == payload["execution"]["analysis_mode"]
           and study_payload["inference"] == payload["execution"]["inference_config"]
           and study_payload["method"]["id"] == payload["execution"]["method"]
           and study_payload["method"]["backend"] == payload["execution"]["backend"]
           and study_payload["estimand"] == payload["estimand"], "Study and Manifest disagree")
    for key in ("question", "design", "dataset"):
        _check(study_payload["inputs"][key] == payload["lineage"][key], "Input lineage mismatch")
    negative = payload["lineage"]["graph"] is None
    validate_status(files["status.json"], run_id, negative=negative)
    if negative:
        validate_diagnostics(files[DIAGNOSTICS], run_id)
    elif verify_graph_provenance:
        evidence = GraphEvidence.from_canonical_json(files["graph.json"])
        evidence.provenance.validate_lineage(study, lineage=payload["lineage"], execution=payload["execution"])
    else:
        _validate_graph(files["graph.json"])
    return payload, inventory, study


def _named_directory(parent: int, key: str, fd: int, identity: VerifiedRootIdentity) -> None:
    named = os.stat(key, dir_fd=parent, follow_symlinks=False)
    opened = _check_fd(fd, identity, directory=True)
    _check((named.st_dev, named.st_ino, named.st_uid, named.st_mode)
           == (opened.st_dev, opened.st_ino, opened.st_uid, opened.st_mode), "Bundle directory was replaced")


class LocalManifestReader:
    def verify(self, *, root: TrustedLocalRoot, run_id: RunId) -> VerifiedLocalRun:
        return self.read_run(root, run_id)

    def read_run(self, trusted_root: TrustedLocalRoot, run_id: RunId) -> VerifiedLocalRun:
        try:
            return self._read(trusted_root, run_id)
        except FileNotFoundError as error:
            raise publication_error("NOT_COMMITTED", "Required run file is missing") from error
        except ContractViolation as error:
            if error.reason.phase == "publication":
                raise
            raise publication_error(error.reason.code, "Committed run failed validation") from error
        except OSError as error:
            raise publication_error("NOT_COMMITTED", "Committed run could not be safely read") from error

    def _read(self, root: TrustedLocalRoot, run_id: RunId) -> VerifiedLocalRun:
        _check(safe_run_id(run_id), "Invalid run ID")
        identity = root.verify()
        root_fd = root.fileno()
        with private_directory(root_fd, "runs", identity) as runs:
            with private_directory(runs, run_id, identity) as directory:
                marker = fields(_json(read_private_file(directory, MARKER, identity)),
                                "marker_version run_id manifest_sha256 request_hash", "publication")
                _check(marker["marker_version"] == "e11-commit/1", "Unsupported marker version",
                       "VERSION_UNSUPPORTED")
                _check(marker["run_id"] == run_id and valid_sha256(marker["request_hash"]),
                       "Marker identity mismatch")
                raw_manifest = read_private_file(directory, MANIFEST, identity)
                _check(_hash(raw_manifest) == marker["manifest_sha256"], "Manifest digest mismatch",
                       "MANIFEST_HASH_MISMATCH")
                manifest = LocalRunManifest.from_payload(_json(raw_manifest))
                _check(manifest.to_canonical_bytes() == raw_manifest, "Manifest is not canonical")
                payload, inventory, _study = _verify_artifacts(
                    directory, identity, manifest, metadata={MANIFEST, MARKER}, verify_graph_provenance=True,
                )
                _check((payload["run_id"], payload["request_hash"]) == (run_id, marker["request_hash"]),
                       "Marker and Manifest disagree")
                for name in ("question", "design", "dataset"):
                    ref = ContentRef.from_payload(payload["lineage"][name])
                    LocalContentReferenceAdapter().verify(ref, root=root)
                _named_directory(runs, run_id, directory, identity)
                _named_directory(root_fd, "runs", runs, identity)
                root.verify()
        return VerifiedLocalRun(run_id, marker["request_hash"], manifest, inventory)
