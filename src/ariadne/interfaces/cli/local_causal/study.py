"""Pure local study transport and G01 validation."""
from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass

from ariadne.causal.design.study import ValidatedStudy, freeze_json, thaw_json
from ariadne.causal.inference.contracts import EstimandRef
from ariadne.shared.content_ref import ContentRef, ContractViolation, Reason
from ariadne.shared.serialization.jcs import canonical_bytes

STUDY_VERSION = "e11-local-study/1"
INFERENCE = {"requested": False, "confidence_level": None}
PRIVACY = {"classification": "AGGREGATE", "row_export_requested": False}


def require(condition: bool, phase: str, message: str, code: str = "SCHEMA_INVALID") -> None:
    if not condition:
        raise ContractViolation(code, phase, message)


def fields(value: object, required: str, phase: str, optional: str = "") -> Mapping[str, object]:
    required_keys = set(required.split())
    allowed = required_keys | set(optional.split())
    require(isinstance(value, Mapping) and required_keys <= set(value) <= allowed, phase, "Invalid object keys")
    return value


def safe_run_id(value: object) -> bool:
    return type(value) is str and re.fullmatch(r"[A-Za-z0-9_-]{1,128}", value) is not None


def validate_method_config(config: object) -> None:
    phase = "method_config"
    value = fields(config, "indep_test alpha depth max_path_length background_knowledge", phase)
    require(value["indep_test"] in ("fisherz", "chisq", "gsq"), phase, "Invalid independence test")
    alpha = value["alpha"]
    require(type(alpha) in (float, int) and 0 < alpha < 1, phase, "Invalid alpha")
    for key in ("depth", "max_path_length"):
        require(type(value[key]) is int and value[key] >= -1, phase, f"Invalid {key}")
    bk = value["background_knowledge"]
    if bk is None:
        return
    for edges in fields(bk, "required_edges forbidden_edges", phase).values():
        require(type(edges) is list, phase, "Expected a list of directed pairs")
        seen = set()
        for edge in edges:
            require(
                type(edge) is list and len(edge) == 2 and all(type(name) is str and name for name in edge),
                phase, "Invalid directed pair",
            )
            pair = tuple(edge)
            require(pair not in seen, phase, "Duplicate directed pair")
            seen.add(pair)


@dataclass(frozen=True)
class LocalStudySpec:
    schema_version: str
    run_id: str
    operation: str
    analysis_mode: str
    question: ContentRef
    design: ContentRef
    dataset: ContentRef
    graph: ContentRef | None
    identification: ContentRef | None
    estimand: EstimandRef
    method: Mapping[str, object]
    inference: Mapping[str, object]
    randomness: Mapping[str, object]
    privacy: Mapping[str, object]
    _payload: Mapping[str, object]

    def validate_local_invariants(self) -> tuple[Reason, ...]:
        phase = "study"
        try:
            require(self.schema_version == STUDY_VERSION, phase, "Unsupported Study version", "VERSION_UNSUPPORTED")
            require(safe_run_id(self.run_id), phase, "Invalid run ID")
            require(self.operation == "DISCOVER" and self.analysis_mode == "EXPLORATORY", phase, "Invalid G01 operation or mode")
            require(self.graph is None and self.identification is None, phase, "Unexpected input Graph or Identification")
            require(self.estimand.is_graph_structure(), phase, "Invalid G01 estimand")
            require(self.inference == INFERENCE, phase, "Inference must be disabled")
            require(self.privacy == PRIVACY, phase, "G01 requires aggregate-only output", "PRIVACY_POLICY_CONFLICT")
        except ContractViolation as error:
            return (error.reason,)
        return ()

    @classmethod
    def from_payload(cls, payload: object) -> LocalStudySpec:
        phase = "study"
        value = fields(payload, "schema_version run_id operation analysis_mode inputs estimand method inference randomness privacy", phase)
        require(value["schema_version"] == STUDY_VERSION, phase, "Unsupported Study version", "VERSION_UNSUPPORTED")
        canonical_bytes(value)
        refs = fields(value["inputs"], "question design dataset", phase, "graph identification")
        inputs = {name: ContentRef.from_payload(refs[name]) for name in ("question", "design", "dataset")}
        for name in ("graph", "identification"):
            ref = refs.get(name)
            inputs[name] = None if ref is None else ContentRef.from_payload(ref)
        target = fields(value["estimand"], "family population contrast", phase, "time target_ref")
        time = target.get("time")
        require(time is None or type(time) is str, phase, "Invalid estimand time")
        target_ref = target.get("target_ref")
        estimand = EstimandRef(target["family"], target["population"], target["contrast"], time,
                               None if target_ref is None else ContentRef.from_payload(target_ref))
        method = fields(value["method"], "id backend config", phase)
        inference = fields(value["inference"], "requested confidence_level", phase)
        require(type(inference["requested"]) is bool, phase, "Invalid inference request type")
        randomness = fields(value["randomness"], "seed", phase)
        require(randomness["seed"] is None or type(randomness["seed"]) is int, phase, "Invalid seed")
        privacy = fields(value["privacy"], "classification row_export_requested", phase)
        require(type(privacy["row_export_requested"]) is bool, phase, "Invalid row export request type")
        require(privacy["classification"] in ("AGGREGATE", "RESTRICTED_ROW_LEVEL"), phase, "Invalid classification")
        return cls(value["schema_version"], value["run_id"], value["operation"], value["analysis_mode"],
                   **inputs, estimand=estimand, method=freeze_json(method), inference=freeze_json(inference),
                   randomness=freeze_json(randomness), privacy=freeze_json(privacy), _payload=freeze_json(value))

    def to_validated_study(self) -> ValidatedStudy:
        reasons = self.validate_local_invariants()
        if reasons:
            reason = reasons[0]
            raise ContractViolation(reason.code, reason.phase, reason.message)
        require((self.method["id"], self.method["backend"]) == ("P1-M06", "causal-learn"),
                "method_config", "Unsupported G01 method or backend")
        validate_method_config(thaw_json(self.method["config"]))
        return ValidatedStudy(self.estimand, self.question, self.design, self.dataset, self._payload)
