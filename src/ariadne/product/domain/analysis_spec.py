"""Strict ENH-E1 analysis-spec validation and scientific identity helpers."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from ariadne.product.domain.enums import ExecutionOperation
from ariadne.product.domain.errors import InvalidAnalysisSpec

SCHEMA_VERSION = "causal-analysis-spec/2"
_COMMON = {
    "schema_version", "analysis_mode", "research_context", "causal_question",
    "causal_design", "operation_spec", "validation_override",
}
_RESEARCH_CONTEXT = {
    "problem_statement", "research_question", "significance", "hypothesis",
}
_CAUSAL_QUESTION = {
    "population", "treatment", "comparator", "outcome", "analysis_unit",
    "treatment_time", "outcome_window", "estimand", "decision_use",
}
_REQUIRED_QUESTION = _CAUSAL_QUESTION - {"decision_use"}
_CAUSAL_DESIGN = {
    "assignment_assumption", "time_zero", "eligibility_criteria",
    "identification_strategy", "adjustment_set", "assumptions",
}
_OPERATION_FIELDS = {
    ExecutionOperation.DISCOVERY: {
        "feature_columns", "constraints", "expected_graph_type", "bootstrap_samples",
    },
    ExecutionOperation.IDENTIFICATION: {"allow_partial_identification"},
    ExecutionOperation.ESTIMATION: {"estimator", "inference_options"},
    ExecutionOperation.REFUTATION: {"method", "repetitions", "subset_fraction"},
    ExecutionOperation.SENSITIVITY: {"dimension", "values", "adjustment_sets"},
}


def validate_analysis_spec(operation: ExecutionOperation, value: dict[str, Any]) -> None:
    if not isinstance(value, dict):
        raise InvalidAnalysisSpec("analysis_spec must be an object")
    _reject_unknown("analysis_spec", value, _COMMON)
    missing = _COMMON - set(value)
    if missing:
        raise InvalidAnalysisSpec(f"analysis_spec fields are required: {sorted(missing)}")
    if value["schema_version"] != SCHEMA_VERSION:
        raise InvalidAnalysisSpec(f"schema_version must be {SCHEMA_VERSION!r}")
    if value["analysis_mode"] not in {"EXPLORATORY", "CONFIRMATORY"}:
        raise InvalidAnalysisSpec("analysis_mode must be EXPLORATORY or CONFIRMATORY")
    for name in ("research_context", "causal_question", "causal_design", "operation_spec"):
        if not isinstance(value[name], dict):
            raise InvalidAnalysisSpec(f"{name} must be an object")
    _reject_unknown("research_context", value["research_context"], _RESEARCH_CONTEXT)
    _reject_unknown("causal_question", value["causal_question"], _CAUSAL_QUESTION)
    _reject_unknown("causal_design", value["causal_design"], _CAUSAL_DESIGN)
    operation_allowed = _OPERATION_FIELDS[operation]
    if operation == ExecutionOperation.REFUTATION:
        operation_allowed = (
            {"method", "repetitions"}
            if value["operation_spec"].get("method") == "PLACEBO_TREATMENT"
            else {"method", "subset_fraction"}
        )
    elif operation == ExecutionOperation.SENSITIVITY:
        operation_allowed = (
            {"dimension", "values"}
            if value["operation_spec"].get("dimension") == "PROPENSITY_CLIPPING"
            else {"dimension", "adjustment_sets"}
        )
    _reject_unknown("operation_spec", value["operation_spec"], operation_allowed)

    question = value["causal_question"]
    if operation in {ExecutionOperation.IDENTIFICATION, ExecutionOperation.ESTIMATION}:
        missing_question = _REQUIRED_QUESTION - set(question)
        if missing_question:
            raise InvalidAnalysisSpec(
                f"causal_question fields are required: {sorted(missing_question)}"
            )
        if any(not isinstance(question[name], str) or not question[name] for name in _REQUIRED_QUESTION):
            raise InvalidAnalysisSpec("causal_question fields must be non-empty strings")
        if question["estimand"] not in {"ATE", "ATT"}:
            raise InvalidAnalysisSpec("causal_question.estimand must be ATE or ATT")
        if question["treatment"] == question["outcome"]:
            raise InvalidAnalysisSpec("treatment and outcome must differ")

    design = value["causal_design"]
    adjustment = design.get("adjustment_set", [])
    assumptions = design.get("assumptions", [])
    if not _string_list(adjustment, unique=True):
        raise InvalidAnalysisSpec("causal_design.adjustment_set must be a unique string list")
    if not _string_list(assumptions):
        raise InvalidAnalysisSpec("causal_design.assumptions must be a string list")

    override = value["validation_override"]
    if override is not None:
        if not isinstance(override, dict) or set(override) != {"reason", "actor", "warning_codes"}:
            raise InvalidAnalysisSpec("validation_override requires reason, actor, warning_codes")
        if not isinstance(override["reason"], str) or not override["reason"].strip():
            raise InvalidAnalysisSpec("validation_override.reason is required")
        if not isinstance(override["actor"], str) or not override["actor"].strip():
            raise InvalidAnalysisSpec("validation_override.actor is required")
        if not _string_list(override["warning_codes"], unique=True) or not override["warning_codes"]:
            raise InvalidAnalysisSpec("validation_override.warning_codes is required")

    spec = value["operation_spec"]
    if operation == ExecutionOperation.DISCOVERY:
        columns = spec.get("feature_columns")
        if not _string_list(columns, unique=True) or not columns:
            raise InvalidAnalysisSpec("operation_spec.feature_columns is required")
        if spec.get("expected_graph_type") not in {None, "DAG", "CPDAG", "PAG"}:
            raise InvalidAnalysisSpec("expected_graph_type must be DAG, CPDAG, PAG, or null")
        if not isinstance(spec.get("constraints", {}), dict):
            raise InvalidAnalysisSpec("operation_spec.constraints must be an object")
    elif operation == ExecutionOperation.IDENTIFICATION:
        if design.get("identification_strategy") not in {"RANDOMIZED", "BACKDOOR"}:
            raise InvalidAnalysisSpec("identification_strategy must be RANDOMIZED or BACKDOOR")
        if not isinstance(spec.get("allow_partial_identification", False), bool):
            raise InvalidAnalysisSpec("allow_partial_identification must be boolean")
    elif operation == ExecutionOperation.ESTIMATION:
        estimator = spec.get("estimator")
        if not isinstance(estimator, str) or not estimator:
            raise InvalidAnalysisSpec("operation_spec.estimator is required")
        if not isinstance(spec.get("inference_options", {}), dict):
            raise InvalidAnalysisSpec("inference_options must be an object")
    elif operation == ExecutionOperation.REFUTATION:
        if spec.get("method") not in {"PLACEBO_TREATMENT", "DATA_SUBSET"}:
            raise InvalidAnalysisSpec("unsupported refutation method")
        if spec["method"] == "PLACEBO_TREATMENT" and (
            not isinstance(spec.get("repetitions"), int) or spec["repetitions"] < 2
        ):
            raise InvalidAnalysisSpec("PLACEBO_TREATMENT requires repetitions >= 2")
        if spec["method"] == "DATA_SUBSET" and (
            not isinstance(spec.get("subset_fraction"), (int, float))
            or not 0 < float(spec["subset_fraction"]) < 1
        ):
            raise InvalidAnalysisSpec("DATA_SUBSET requires 0 < subset_fraction < 1")
    elif operation == ExecutionOperation.SENSITIVITY:
        if spec.get("dimension") not in {"ADJUSTMENT_SET", "PROPENSITY_CLIPPING"}:
            raise InvalidAnalysisSpec("unsupported sensitivity dimension")
        if spec["dimension"] == "PROPENSITY_CLIPPING":
            values = spec.get("values")
            if not isinstance(values, list) or not values or any(
                not isinstance(item, (int, float)) or not 0 < float(item) < .5 for item in values
            ):
                raise InvalidAnalysisSpec("PROPENSITY_CLIPPING requires values between 0 and 0.5")
        else:
            sets = spec.get("adjustment_sets")
            if not isinstance(sets, list) or not sets or any(
                not _string_list(item, unique=True) for item in sets
            ):
                raise InvalidAnalysisSpec("ADJUSTMENT_SET requires unique string-list variants")


def causal_question_hash(value: dict[str, Any]) -> str:
    question = value.get("causal_question", {})
    raw = json.dumps(question, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _reject_unknown(name: str, value: dict[str, Any], allowed: set[str]) -> None:
    unknown = set(value) - allowed
    if unknown:
        raise InvalidAnalysisSpec(f"unknown {name} fields: {sorted(unknown)}")


def _string_list(value: Any, *, unique: bool = False) -> bool:
    return (
        isinstance(value, list)
        and all(isinstance(item, str) and item for item in value)
        and (not unique or len(value) == len(set(value)))
    )
