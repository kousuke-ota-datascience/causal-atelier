"""Pure G01 manifest parsing and projection from staged run evidence."""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass

from ariadne.causal.design.study import ValidatedStudy, freeze_json, thaw_json
from ariadne.interfaces.cli.local_causal.study import (
    INFERENCE, STUDY_VERSION, LocalStudySpec, fields, require, safe_run_id,
)
from ariadne.shared.content_ref import ContentRef, ContractViolation, Reason, nonempty_text, valid_sha256
from ariadne.shared.serialization import jcs

MANIFEST_VERSION = "e11-local-manifest/1"
STATUS_VERSION = "e11-local-status/1"
GRAPH_VERSION = "e11-local-graph/1"
NEGATIVE_REASON = "SCI_NO_ADMISSIBLE_PAG"
PHASE = "manifest"
AXES = {
    "identification_status": "NOT_APPLICABLE",
    "point_availability": "NOT_REQUESTED",
    "inference_availability": "NOT_REQUESTED",
    "science_acceptance": "NOT_EVALUATED",
}


def _snapshot(value: object) -> Mapping[str, object]:
    require(isinstance(value, Mapping), PHASE, "Expected JSON object")
    try:
        jcs.canonical_bytes(thaw_json(value))
    except ValueError as error:
        raise ContractViolation("SCHEMA_INVALID", PHASE, "Invalid JSON object") from error
    return freeze_json(value)


@dataclass(frozen=True)
class ArtifactDescriptor:
    key: str
    sha256: str
    size_bytes: int
    media_type: str
    privacy_class: str
    visibility: str


@dataclass(frozen=True)
class RuntimeEvidence:
    repo_commit: str
    dirty: bool
    python_version: str
    platform: str
    uv_lock_sha256: str
    distributions: Mapping[str, object]
    api_probes: Mapping[str, object]

    def __post_init__(self) -> None:
        for key in ("distributions", "api_probes"):
            object.__setattr__(self, key, _snapshot(getattr(self, key)))

    def to_payload(self) -> dict[str, object]:
        return {key: thaw_json(getattr(self, key)) for key in self.__annotations__}


@dataclass(frozen=True)
class ValidatedRunEvidence:
    study: ValidatedStudy
    study_payload: Mapping[str, object]
    status_payload: Mapping[str, object]
    runtime: RuntimeEvidence
    stochastic: Mapping[str, object]
    artifact_descriptors: tuple[ArtifactDescriptor, ...]
    output_graph_ref: ContentRef | None
    graph_negative_reason_codes: tuple[str, ...]
    review_science_evidence_ref: ContentRef | None

    def __post_init__(self) -> None:
        for key in ("study_payload", "status_payload", "stochastic"):
            object.__setattr__(self, key, _snapshot(getattr(self, key)))
        require(type(self.artifact_descriptors) is tuple and all(
            type(item) is ArtifactDescriptor for item in self.artifact_descriptors
        ), PHASE, "Expected immutable artifact descriptors")
        require(type(self.graph_negative_reason_codes) is tuple and all(
            type(code) is str for code in self.graph_negative_reason_codes
        ), PHASE, "Expected immutable scientific reason codes")


def _check_runtime(runtime: object) -> None:
    value = fields(runtime, "repo_commit dirty python_version platform uv_lock_sha256 distributions api_probes", PHASE)
    for key in ("repo_commit", "python_version", "platform"):
        require(nonempty_text(value[key]), PHASE, f"Missing runtime {key}")
    require(type(value["dirty"]) is bool, PHASE, "Invalid dirty flag")
    require(valid_sha256(value["uv_lock_sha256"]), PHASE, "Invalid lock digest", "HASH_INVALID")
    for key in ("distributions", "api_probes"):
        require(isinstance(value[key], Mapping), PHASE, f"Invalid runtime {key}")


def _check_estimand(payload: object) -> None:
    value = fields(payload, "family population contrast", PHASE, "time target_ref")
    require((value["family"], value["population"], value["contrast"]) == (
        "GRAPH_STRUCTURE", "OBSERVED_VARIABLES", "NOT_APPLICABLE",
    ), PHASE, "Invalid G01 estimand")
    require(value.get("time") is None or type(value["time"]) is str, PHASE, "Invalid estimand time")
    if value.get("target_ref") is not None:
        ContentRef.from_payload(value["target_ref"])


def _check_artifacts(artifacts: object, graph: ContentRef | None, run_id: str) -> None:
    require(type(artifacts) is list, PHASE, "Invalid artifact array")
    inventory = {}
    allowed = {"study.json", "status.json", "graph.json" if graph is not None else "diagnostics.json"}
    for artifact in artifacts:
        value = fields(artifact, "key sha256 size_bytes media_type privacy_class visibility", PHASE)
        key = value["key"]
        require(type(key) is str and key in allowed and key not in inventory, PHASE, "Invalid or duplicate artifact key")
        require(valid_sha256(value["sha256"]), PHASE, "Invalid artifact digest", "HASH_INVALID")
        require(type(value["size_bytes"]) is int and value["size_bytes"] > 0, PHASE, "Invalid artifact byte count")
        require(value["media_type"] == "application/json", PHASE, "Invalid artifact MIME")
        require(value["privacy_class"] == "AGGREGATE" and value["visibility"] == "PRIVATE",
                PHASE, "Invalid artifact privacy", "PRIVACY_POLICY_CONFLICT")
        inventory[key] = value
    require(set(inventory) == allowed, PHASE, "Incomplete artifact inventory")
    if graph is not None:
        require(graph.relative_key == f"runs/{run_id}/graph.json" and graph.schema_version == GRAPH_VERSION,
                PHASE, "Invalid Graph reference path or version")
        require(graph.media_type == inventory["graph.json"]["media_type"], PHASE, "Graph MIME mismatch")
        require(graph.sha256 == inventory["graph.json"]["sha256"], PHASE, "Graph byte digest mismatch", "HASH_INVALID")


def _check_manifest(payload: object) -> None:
    value = fields(payload, "manifest_version run_id operation request_hash schema_dispatch lineage estimand "
                   "execution runtime stochastic artifacts review canonical_codec_version", PHASE)
    require(value["manifest_version"] == MANIFEST_VERSION and value["canonical_codec_version"] == jcs.VERSION,
            PHASE, "Unsupported Manifest or codec version", "VERSION_UNSUPPORTED")
    require(safe_run_id(value["run_id"]) and value["operation"] == "DISCOVER", PHASE, "Invalid G01 run")
    require(valid_sha256(value["request_hash"]), PHASE, "Invalid request digest", "HASH_INVALID")
    lineage = fields(value["lineage"], "question design dataset graph identification", PHASE)
    for name in ("question", "design", "dataset"):
        ContentRef.from_payload(lineage[name])
    require(lineage["identification"] is None, PHASE, "Unexpected Identification reference")
    graph = None if lineage["graph"] is None else ContentRef.from_payload(lineage["graph"])
    require(value["schema_dispatch"] == {"study": STUDY_VERSION, "status": STATUS_VERSION,
                                        "result": None, "graph": GRAPH_VERSION if graph else None},
            PHASE, "Invalid schema dispatch")
    _check_estimand(value["estimand"])
    execution = fields(value["execution"], "technical_status analysis_mode method backend inference_config scientific_axes", PHASE)
    require(execution == {"technical_status": "COMPLETED", "analysis_mode": "EXPLORATORY",
                          "method": "P1-M06", "backend": "causal-learn",
                          "inference_config": INFERENCE, "scientific_axes": AXES}
            and type(execution["inference_config"]["requested"]) is bool, PHASE, "Invalid execution evidence")
    _check_runtime(value["runtime"])
    require(isinstance(value["stochastic"], Mapping), PHASE, "Invalid stochastic evidence")
    require(value["review"] == {"science_evidence_ref": None}, PHASE, "Unexpected science review evidence")
    _check_artifacts(value["artifacts"], graph, value["run_id"])


@dataclass(frozen=True)
class LocalRunManifest:
    _payload: Mapping[str, object]

    def __post_init__(self) -> None:
        frozen = _snapshot(self._payload)
        value = thaw_json(frozen)
        _check_manifest(value)
        value["artifacts"].sort(key=lambda item: item["key"])
        object.__setattr__(self, "_payload", freeze_json(value))

    @classmethod
    def from_payload(cls, payload: Mapping[str, object]) -> LocalRunManifest:
        return cls(payload)

    @classmethod
    def from_run_evidence(cls, evidence: ValidatedRunEvidence) -> LocalRunManifest:
        require(type(evidence) is ValidatedRunEvidence and type(evidence.study) is ValidatedStudy
                and type(evidence.runtime) is RuntimeEvidence, PHASE, "Invalid run evidence type")
        study = thaw_json(evidence.study_payload)
        expected = LocalStudySpec.from_payload(study).to_validated_study()
        require(jcs.canonical_bytes(study) == jcs.canonical_bytes(evidence.study.to_payload())
                and (expected.estimand, expected.question, expected.design, expected.dataset)
                == (evidence.study.estimand, evidence.study.question, evidence.study.design, evidence.study.dataset),
                PHASE, "Study projection mismatch")
        run_id = study["run_id"]
        graph = evidence.output_graph_ref
        require(graph is None or type(graph) is ContentRef, PHASE, "Invalid output Graph reference")
        reason_codes = [] if graph is not None else [NEGATIVE_REASON]
        require(evidence.graph_negative_reason_codes == tuple(reason_codes), PHASE, "Invalid scientific reason codes")
        status = thaw_json(evidence.status_payload)
        require(status == {"schema_version": STATUS_VERSION, "run_id": run_id, "technical_status": "COMPLETED",
                           **AXES, "reason_codes": reason_codes, "manifest_relative_path": f"runs/{run_id}/manifest.json"},
                PHASE, "Invalid candidate status or reason codes")
        require(evidence.review_science_evidence_ref is None, PHASE, "Unexpected science review evidence")
        return cls.from_payload({
            "manifest_version": MANIFEST_VERSION, "run_id": run_id, "operation": study["operation"],
            "request_hash": jcs.digest(study),
            "schema_dispatch": {"study": STUDY_VERSION, "status": STATUS_VERSION, "result": None,
                                "graph": GRAPH_VERSION if graph else None},
            "lineage": {**study["inputs"], "graph": graph.to_payload() if graph else None, "identification": None},
            "estimand": study["estimand"],
            "execution": {"technical_status": status["technical_status"], "analysis_mode": study["analysis_mode"],
                          "method": study["method"]["id"], "backend": study["method"]["backend"],
                          "inference_config": study["inference"], "scientific_axes": AXES},
            "runtime": evidence.runtime.to_payload(), "stochastic": thaw_json(evidence.stochastic),
            "artifacts": [asdict(item) for item in evidence.artifact_descriptors],
            "review": {"science_evidence_ref": None}, "canonical_codec_version": jcs.VERSION,
        })

    def validate_invariants(self) -> tuple[Reason, ...]:
        try:
            _check_manifest(thaw_json(self._payload))
        except ContractViolation as error:
            return (error.reason,)
        return ()

    def to_canonical_bytes(self) -> bytes:
        return jcs.canonical_bytes(thaw_json(self._payload))
