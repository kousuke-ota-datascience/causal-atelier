"""Deterministic ENH-E1 identification for randomized and back-door designs."""

from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import Any

import pandas as pd

from ariadne.product.domain.analysis_spec import causal_question_hash
from ariadne.product.domain.enums import GraphType, ResultType, ScientificStatus
from ariadne.product.domain.errors import InvalidAnalysisSpec, ScientificCoreExecutionError
from ariadne.product.domain.graph_semantics import validate_graph_document
from ariadne.product.ports.scientific_core import IdentificationInput, ScientificResultDescriptor


class IdentificationAdapter:
    def run(self, input_: IdentificationInput, output_dir: Path) -> list[ScientificResultDescriptor]:
        frame = _load_dataset(input_.dataset_path)
        graph = _load_graph(input_.graph_path)
        try:
            graph_type = GraphType(graph["graph_type"])
        except (KeyError, TypeError, ValueError) as exc:
            raise InvalidAnalysisSpec("graph_type must be DAG, CPDAG, or PAG") from exc
        validate_graph_document(graph_type, graph)
        question = input_.analysis_spec["causal_question"]
        design = input_.analysis_spec["causal_design"]
        strategy = design["identification_strategy"]
        treatment, outcome = question["treatment"], question["outcome"]
        adjustment = list(design.get("adjustment_set", []))
        reasons: list[dict[str, Any]] = []

        if treatment not in graph["nodes"]:
            reasons.append(_reason("MISSING_TREATMENT_NODE", "Treatment is absent from graph."))
        if outcome not in graph["nodes"]:
            reasons.append(_reason("MISSING_OUTCOME_NODE", "Outcome is absent from graph."))
        missing_columns = [column for column in [treatment, outcome, *adjustment] if column not in frame]
        if missing_columns:
            reasons.append(_reason("MISSING_DATA_COLUMN", "Analysis columns are absent.", {"columns": missing_columns}))

        if graph_type != GraphType.DAG:
            reasons.append(_reason(
                "UNRESOLVED_GRAPH_ORIENTATION",
                "CPDAG/PAG is preserved and cannot be implicitly converted to a DAG.",
                {"graph_type": graph_type.value},
            ))
        elif _has_cycle(_dag_maps(graph)[1]):
            reasons.append(_reason("GRAPH_NOT_ACYCLIC", "Graph declared as DAG contains a directed cycle."))
        elif not reasons and strategy == "RANDOMIZED":
            reasons.extend(_validate_randomized(graph, treatment, outcome, adjustment))
        elif not reasons:
            reasons.extend(_validate_backdoor(graph, treatment, outcome, adjustment))
        ident_status = _identification_status(graph_type, reasons)

        payload = {
            "status": ident_status.value,
            "strategy": strategy,
            "estimand": question["estimand"],
            "adjustment_set_candidates": [adjustment] if adjustment else [[]],
            "selected_adjustment_set": adjustment,
            "assumptions": list(design.get("assumptions", [])),
            "explanation": (
                "The declared strategy passed deterministic ENH-E1 checks."
                if ident_status == ScientificStatus.IDENTIFIED
                else "Identification was not established automatically."
            ),
            "non_identification_reasons": reasons,
            "causal_question_hash": causal_question_hash(input_.analysis_spec),
            "graph_type": graph_type.value,
        }
        eligibility = _eligibility(frame, graph, question, adjustment)
        return [
            ScientificResultDescriptor(
                result_type=ResultType.IDENTIFICATION_RESULT,
                scientific_status=ident_status,
                summary={
                    "strategy": strategy,
                    "estimand": question["estimand"],
                    "reason_count": len(reasons),
                },
                payload=payload,
                warnings=reasons,
            ),
            eligibility,
        ]


def _validate_backdoor(
    graph: dict[str, Any], treatment: str, outcome: str, adjustment: list[str]
) -> list[dict[str, Any]]:
    reasons: list[dict[str, Any]] = []
    if treatment in adjustment or outcome in adjustment:
        reasons.append(_reason("INVALID_ADJUSTMENT_MEMBER", "Treatment/outcome cannot be adjusted for."))
        return reasons
    parents, children = _dag_maps(graph)
    descendants = _reachable(children, treatment)
    post_treatment = sorted(set(adjustment) & descendants)
    if post_treatment:
        reasons.append(_reason("POST_TREATMENT_ADJUSTMENT", "Treatment descendants cannot be adjusted for.", {"columns": post_treatment}))
    active_paths, collider_paths = _active_backdoor_paths(
        parents, children, treatment, outcome, set(adjustment)
    )
    if collider_paths:
        reasons.append(_reason(
            "COLLIDER_ADJUSTMENT",
            "Adjustment activates a collider or descendant of a collider on a back-door path.",
            {
                "columns": sorted({
                    column
                    for item in collider_paths
                    for column in item["activating_adjustment_columns"]
                }),
                "activated_paths": collider_paths,
            },
        ))
    elif not reasons and active_paths:
        reasons.append(_reason(
            "OPEN_BACKDOOR_PATH",
            "Adjustment set does not block every back-door path.",
            {"active_paths": active_paths},
        ))
    return reasons


def _validate_randomized(
    graph: dict[str, Any], treatment: str, outcome: str, adjustment: list[str]
) -> list[dict[str, Any]]:
    if treatment in adjustment or outcome in adjustment:
        return [_reason(
            "INVALID_ADJUSTMENT_MEMBER",
            "Treatment/outcome cannot be adjusted for.",
        )]
    _, children = _dag_maps(graph)
    post_treatment = sorted(set(adjustment) & _reachable(children, treatment))
    if post_treatment:
        return [_reason(
            "POST_TREATMENT_ADJUSTMENT",
            "Randomized designs may adjust only for pre-treatment covariates.",
            {"columns": post_treatment},
        )]
    return []


def _identification_status(
    graph_type: GraphType, reasons: list[dict[str, Any]]
) -> ScientificStatus:
    """Apply deterministic-invalid > orientation-review > identified priority."""
    deterministic = [
        reason for reason in reasons
        if reason["code"] != "UNRESOLVED_GRAPH_ORIENTATION"
    ]
    if deterministic:
        return ScientificStatus.NOT_IDENTIFIED
    if graph_type != GraphType.DAG:
        return ScientificStatus.REQUIRES_REVIEW
    return ScientificStatus.IDENTIFIED


def _active_backdoor_paths(
    parents: dict[str, set[str]], children: dict[str, set[str]], treatment: str,
    outcome: str, conditioned: set[str],
) -> tuple[list[list[str]], list[dict[str, Any]]]:
    """Return active paths and paths activated by collider conditioning.

    Arrows out of treatment are removed first, so causal paths cannot be mistaken
    for back-door paths.  A path is active when every non-collider is unconditioned
    and every collider has itself or a descendant in the conditioning set.
    """
    reduced_children = {node: set(values) for node, values in children.items()}
    reduced_parents = {node: set(values) for node, values in parents.items()}
    for child in children[treatment]:
        reduced_children[treatment].discard(child)
        reduced_parents[child].discard(treatment)
    undirected = {
        node: reduced_parents[node] | reduced_children[node]
        for node in reduced_parents
    }
    paths: list[list[str]] = []

    def visit(node: str, path: list[str]) -> None:
        if len(paths) >= 10_000:
            raise InvalidAnalysisSpec("Graph has too many treatment-outcome paths")
        if node == outcome:
            paths.append(path)
            return
        for neighbor in sorted(undirected[node]):
            if neighbor not in path:
                visit(neighbor, [*path, neighbor])

    visit(treatment, [treatment])
    active: list[list[str]] = []
    collider_activated: list[dict[str, Any]] = []
    descendant_cache = {
        node: _reachable(children, node) for node in children
    }
    for path in paths:
        path_colliders: list[str] = []
        activators: set[str] = set()
        is_active = True
        for index in range(1, len(path) - 1):
            previous, node, following = path[index - 1:index + 2]
            collider = previous in reduced_parents[node] and following in reduced_parents[node]
            if collider:
                activated_by = conditioned & ({node} | descendant_cache[node])
                if not activated_by:
                    is_active = False
                    break
                path_colliders.append(node)
                activators.update(activated_by)
            elif node in conditioned:
                is_active = False
                break
        if is_active:
            active.append(path)
            if path_colliders and activators:
                collider_activated.append({
                    "path": path,
                    "colliders": path_colliders,
                    "activating_adjustment_columns": sorted(activators),
                })
    return active, collider_activated


def _eligibility(
    frame: pd.DataFrame, graph: dict[str, Any], question: dict[str, Any], adjustment: list[str]
) -> ScientificResultDescriptor:
    checks: list[dict[str, Any]] = []
    treatment, outcome = question["treatment"], question["outcome"]
    required = [treatment, outcome, *adjustment]
    missing = [column for column in required if column not in frame]
    _check(checks, "REQUIRED_COLUMNS", "FAIL" if missing else "PASS", "Required analysis columns.", {"missing": missing})
    inferred_types = {
        "treatment": _infer_treatment_type(frame, treatment),
        "outcome": _infer_outcome_type(frame, outcome),
    }
    numeric_ready = False
    binary_treatment = False
    if missing:
        _skipped(checks, "TYPE_COMPATIBILITY", "REQUIRED_COLUMNS")
        _skipped(checks, "BINARY_TREATMENT", "REQUIRED_COLUMNS")
        _skipped(checks, "CONSTANT_COLUMNS", "REQUIRED_COLUMNS")
        _skipped(checks, "MISSINGNESS", "REQUIRED_COLUMNS")
        _skipped(checks, "SAMPLE_SIZE", "REQUIRED_COLUMNS")
        _skipped(checks, "TREATMENT_PREVALENCE", "REQUIRED_COLUMNS")
    else:
        non_numeric = [
            column for column in required
            if not (
                pd.api.types.is_numeric_dtype(frame[column])
                or pd.api.types.is_bool_dtype(frame[column])
            )
        ]
        numeric_ready = not non_numeric
        _check(checks, "TYPE_COMPATIBILITY", "FAIL" if non_numeric else "PASS", "Analysis columns require numeric E1 types.", {"columns": non_numeric})
        treatment_values = set(frame[treatment].dropna().unique().tolist())
        binary_treatment = treatment_values == {0, 1} or treatment_values == {False, True}
        if inferred_types["treatment"]["type"] == "UNSUPPORTED":
            _skipped(checks, "BINARY_TREATMENT", "TYPE_COMPATIBILITY")
        else:
            _check(checks, "BINARY_TREATMENT", "PASS" if binary_treatment else "FAIL", "Treatment must contain both binary arms.", {"values": sorted(map(str, treatment_values))})
        constants = [column for column in required if frame[column].nunique(dropna=True) <= 1]
        _check(checks, "CONSTANT_COLUMNS", "FAIL" if constants else "PASS", "Analysis columns must vary.", {"columns": constants})
        missingness = {column: float(frame[column].isna().mean()) for column in required}
        _check(checks, "MISSINGNESS", "WARN" if any(missingness.values()) else "PASS", "Missingness summary.", missingness)
        n_complete = int(frame[required].dropna().shape[0])
        _check(checks, "SAMPLE_SIZE", "FAIL" if n_complete < 20 else "WARN" if n_complete < 100 else "PASS", "Complete-case sample size.", {"n": n_complete})
        if numeric_ready and binary_treatment:
            prevalence = float(frame[treatment].dropna().astype(float).mean())
            _check(checks, "TREATMENT_PREVALENCE", "WARN" if prevalence < .1 or prevalence > .9 else "PASS", "Treatment prevalence.", {"prevalence": prevalence})
        else:
            _skipped(checks, "TREATMENT_PREVALENCE", "TYPE_COMPATIBILITY_OR_BINARY_TREATMENT")
    if adjustment:
        if missing or not numeric_ready or not binary_treatment:
            prerequisite = "REQUIRED_COLUMNS" if missing else "TYPE_COMPATIBILITY_OR_BINARY_TREATMENT"
            _skipped(checks, "LIMITED_OVERLAP", prerequisite)
            _skipped(checks, "EXTREME_WEIGHT_RISK", prerequisite)
        else:
            complete = frame[[treatment, *adjustment]].dropna()
            try:
                import statsmodels.api as sm
                with warnings.catch_warnings(record=True) as model_warnings:
                    warnings.simplefilter("always")
                    model = sm.Logit(
                        complete[treatment].astype(float),
                        sm.add_constant(complete[adjustment].astype(float), has_constant="add"),
                    ).fit(disp=False)
                propensity = model.predict()
                extreme_fraction = float(((propensity < .05) | (propensity > .95)).mean())
                overlap_status = "FAIL" if extreme_fraction > .5 else "WARN" if extreme_fraction > .2 else "PASS"
                _check(checks, "LIMITED_OVERLAP", overlap_status, "Preliminary propensity overlap.", {
                    "minimum": float(propensity.min()), "maximum": float(propensity.max()),
                    "extreme_fraction": extreme_fraction,
                })
                minimum_probability = float(min(propensity.min(), (1 - propensity).min()))
                _check(checks, "EXTREME_WEIGHT_RISK", overlap_status, "Inverse-weight instability risk.", {
                    "maximum_inverse_weight": (
                        1.0 / minimum_probability if minimum_probability > 0 else None
                    )
                })
                if model_warnings:
                    _check(
                        checks,
                        "PROPENSITY_ESTIMATION",
                        "WARN",
                        "Preliminary propensity model emitted numerical warnings.",
                        {"warning_types": sorted({type(item.message).__name__ for item in model_warnings})},
                    )
            except Exception as exc:
                _check(checks, "PROPENSITY_ESTIMATION", "WARN", "Preliminary propensity model was not estimable.", {"exception_type": type(exc).__name__})
    else:
        _not_applicable(checks, "LIMITED_OVERLAP", "No adjustment covariates were declared.")
        _not_applicable(checks, "EXTREME_WEIGHT_RISK", "No adjustment covariates were declared.")
    graph_missing = [column for column in required if column not in graph["nodes"]]
    _check(checks, "GRAPH_NODE_ALIGNMENT", "FAIL" if graph_missing else "PASS", "Graph/data alignment.", {"missing": graph_missing})
    if graph.get("graph_type") == "DAG" and treatment in graph["nodes"]:
        _, children = _dag_maps(graph)
        post_treatment = sorted(set(adjustment) & _reachable(children, treatment))
        _check(checks, "POST_TREATMENT_VARIABLE", "FAIL" if post_treatment else "PASS", "Adjustment must precede treatment.", {"columns": post_treatment})
    unit = question["analysis_unit"]
    if unit in frame:
        duplicates = int(frame[unit].duplicated().sum())
        _check(checks, "DUPLICATE_ANALYSIS_UNIT", "FAIL" if duplicates else "PASS", "Analysis-unit uniqueness.", {"duplicates": duplicates})
    else:
        _check(checks, "DUPLICATE_ANALYSIS_UNIT", "WARN", "Analysis unit is semantic and not a dataset column.", {"analysis_unit": unit})
    rank = {"PASS": 0, "WARN": 1, "FAIL": 2}
    ranked = [item["status"] for item in checks if item["status"] in rank]
    overall = max(ranked, key=rank.__getitem__)
    status = ScientificStatus(overall)
    return ScientificResultDescriptor(
        result_type=ResultType.DATA_ELIGIBILITY_RESULT,
        scientific_status=status,
        summary={"status": overall, "check_count": len(checks)},
        payload={"status": overall, "checks": checks, "inferred_types": inferred_types},
        diagnostics={"checks": checks},
        warnings=[item for item in checks if item["status"] != "PASS"],
    )


def _check(items: list[dict[str, Any]], code: str, status: str, message: str, evidence: Any) -> None:
    items.append({"check_code": code, "status": status, "message": message, "evidence": evidence})


def _skipped(items: list[dict[str, Any]], code: str, prerequisite: str) -> None:
    _check(
        items,
        code,
        "SKIPPED_DUE_TO_PREREQUISITE",
        "Check was not executed because a prerequisite failed.",
        {"prerequisite": prerequisite},
    )


def _not_applicable(items: list[dict[str, Any]], code: str, rationale: str) -> None:
    _check(items, code, "NOT_APPLICABLE", "Check does not apply.", {"rationale": rationale})


def _type_evidence(frame: pd.DataFrame, column: str) -> dict[str, Any]:
    if column not in frame:
        return {"column_present": False, "non_null_count": 0, "distinct_count": 0}
    values = frame[column].dropna()
    return {
        "column_present": True,
        "non_null_count": int(values.shape[0]),
        "distinct_count": int(values.nunique()),
    }


def _infer_treatment_type(frame: pd.DataFrame, column: str) -> dict[str, Any]:
    evidence = _type_evidence(frame, column)
    if column not in frame:
        return {"type": "UNSUPPORTED", "evidence": evidence}
    values = set(frame[column].dropna().unique().tolist())
    numeric = pd.api.types.is_numeric_dtype(frame[column]) or pd.api.types.is_bool_dtype(frame[column])
    supported = numeric and (values == {0, 1} or values == {False, True})
    return {"type": "BINARY" if supported else "UNSUPPORTED", "evidence": evidence}


def _infer_outcome_type(frame: pd.DataFrame, column: str) -> dict[str, Any]:
    evidence = _type_evidence(frame, column)
    if column not in frame:
        return {"type": "UNSUPPORTED", "evidence": evidence}
    values = set(frame[column].dropna().unique().tolist())
    numeric = pd.api.types.is_numeric_dtype(frame[column]) or pd.api.types.is_bool_dtype(frame[column])
    if not numeric or not values:
        normalized = "UNSUPPORTED"
    elif values == {0, 1} or values == {False, True}:
        normalized = "BINARY"
    else:
        normalized = "CONTINUOUS"
    return {"type": normalized, "evidence": evidence}


def _reason(code: str, message: str, evidence: Any | None = None) -> dict[str, Any]:
    return {"code": code, "message": message, "evidence": evidence or {}}


def _dag_maps(graph: dict[str, Any]) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    parents = {node: set() for node in graph["nodes"]}
    children = {node: set() for node in graph["nodes"]}
    for edge in graph["edges"]:
        if edge["endpoint_source"] == "TAIL" and edge["endpoint_target"] == "ARROW":
            children[edge["source"]].add(edge["target"]); parents[edge["target"]].add(edge["source"])
        else:
            raise InvalidAnalysisSpec("DAG contains a non-directed endpoint")
    return parents, children


def _reachable(adjacency: dict[str, set[str]], start: str) -> set[str]:
    seen: set[str] = set(); pending = list(adjacency[start])
    while pending:
        node = pending.pop()
        if node not in seen:
            seen.add(node); pending.extend(adjacency[node])
    return seen


def _has_cycle(adjacency: dict[str, set[str]]) -> bool:
    temporary: set[str] = set(); permanent: set[str] = set()
    def visit(node: str) -> bool:
        if node in temporary:
            return True
        if node in permanent:
            return False
        temporary.add(node)
        if any(visit(child) for child in adjacency[node]):
            return True
        temporary.remove(node); permanent.add(node)
        return False
    return any(visit(node) for node in adjacency)


def _load_dataset(path: Path) -> pd.DataFrame:
    try:
        return pd.read_parquet(path) if path.suffix.lower() == ".parquet" else pd.read_csv(path)
    except Exception as exc:
        raise ScientificCoreExecutionError(f"Unable to read dataset: {exc}") from exc


def _load_graph(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ScientificCoreExecutionError(f"Unable to read graph: {exc}") from exc
    if not isinstance(value, dict):
        raise InvalidAnalysisSpec("graph must be an object")
    return value
