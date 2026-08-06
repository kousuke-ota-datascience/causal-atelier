"""Deterministic ENH-E1 identification for randomized and back-door designs."""

from __future__ import annotations

import json
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
            ident_status = ScientificStatus.REQUIRES_REVIEW
            reasons.append(_reason(
                "UNRESOLVED_GRAPH_ORIENTATION",
                "CPDAG/PAG is preserved and cannot be implicitly converted to a DAG.",
                {"graph_type": graph_type.value},
            ))
        elif _has_cycle(_dag_maps(graph)[1]):
            reasons.append(_reason("GRAPH_NOT_ACYCLIC", "Graph declared as DAG contains a directed cycle."))
            ident_status = ScientificStatus.NOT_IDENTIFIED
        elif reasons:
            ident_status = ScientificStatus.NOT_IDENTIFIED
        elif strategy == "RANDOMIZED":
            if adjustment:
                reasons.append(_reason("RANDOMIZED_ADJUSTMENT_NOT_EMPTY", "RANDOMIZED requires an empty adjustment set."))
                ident_status = ScientificStatus.NOT_IDENTIFIED
            else:
                ident_status = ScientificStatus.IDENTIFIED
        else:
            reasons.extend(_validate_backdoor(graph, treatment, outcome, adjustment))
            ident_status = ScientificStatus.NOT_IDENTIFIED if reasons else ScientificStatus.IDENTIFIED

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
    colliders = sorted(node for node in adjustment if len(parents.get(node, set())) >= 2)
    if colliders:
        reasons.append(_reason("COLLIDER_ADJUSTMENT", "Known collider cannot be adjusted for.", {"columns": colliders}))
    if not reasons and not _blocks_backdoor(parents, children, treatment, outcome, set(adjustment)):
        reasons.append(_reason("OPEN_BACKDOOR_PATH", "Adjustment set does not block every back-door path."))
    return reasons


def _blocks_backdoor(
    parents: dict[str, set[str]], children: dict[str, set[str]], treatment: str,
    outcome: str, conditioned: set[str],
) -> bool:
    # Back-door graph: remove arrows out of treatment, then use the ancestral moral graph.
    reduced_children = {node: set(values) for node, values in children.items()}
    for child in list(reduced_children[treatment]):
        reduced_children[treatment].remove(child)
    reduced_parents = {node: set(values) for node, values in parents.items()}
    for child in children[treatment]:
        reduced_parents[child].discard(treatment)
    ancestors = set(conditioned) | {treatment, outcome}
    pending = list(ancestors)
    while pending:
        node = pending.pop()
        for parent in reduced_parents[node]:
            if parent not in ancestors:
                ancestors.add(parent); pending.append(parent)
    undirected = {node: set() for node in ancestors}
    for child in ancestors:
        ps = reduced_parents[child] & ancestors
        for parent in ps:
            undirected[parent].add(child); undirected[child].add(parent)
        for left in ps:
            for right in ps - {left}:
                undirected[left].add(right)
    pending = [treatment]
    seen = set(conditioned) | {treatment}
    while pending:
        node = pending.pop()
        for neighbor in undirected[node]:
            if neighbor == outcome:
                return False
            if neighbor not in seen:
                seen.add(neighbor); pending.append(neighbor)
    return True


def _eligibility(
    frame: pd.DataFrame, graph: dict[str, Any], question: dict[str, Any], adjustment: list[str]
) -> ScientificResultDescriptor:
    checks: list[dict[str, Any]] = []
    treatment, outcome = question["treatment"], question["outcome"]
    required = [treatment, outcome, *adjustment]
    missing = [column for column in required if column not in frame]
    _check(checks, "REQUIRED_COLUMNS", "FAIL" if missing else "PASS", "Required analysis columns.", {"missing": missing})
    if not missing:
        non_numeric = [column for column in required if not pd.api.types.is_numeric_dtype(frame[column])]
        _check(checks, "TYPE_COMPATIBILITY", "FAIL" if non_numeric else "PASS", "Analysis columns require numeric E1 types.", {"columns": non_numeric})
        treatment_values = set(frame[treatment].dropna().unique().tolist())
        _check(checks, "BINARY_TREATMENT", "PASS" if treatment_values <= {0, 1} and treatment_values == {0, 1} else "FAIL", "Treatment must contain both binary arms.", {"values": sorted(map(str, treatment_values))})
        constants = [column for column in required if frame[column].nunique(dropna=True) <= 1]
        _check(checks, "CONSTANT_COLUMNS", "FAIL" if constants else "PASS", "Analysis columns must vary.", {"columns": constants})
        missingness = {column: float(frame[column].isna().mean()) for column in required}
        _check(checks, "MISSINGNESS", "WARN" if any(missingness.values()) else "PASS", "Missingness summary.", missingness)
        n_complete = int(frame[required].dropna().shape[0])
        _check(checks, "SAMPLE_SIZE", "FAIL" if n_complete < 20 else "WARN" if n_complete < 100 else "PASS", "Complete-case sample size.", {"n": n_complete})
        prevalence = float(frame[treatment].dropna().mean())
        _check(checks, "TREATMENT_PREVALENCE", "WARN" if prevalence < .1 or prevalence > .9 else "PASS", "Treatment prevalence.", {"prevalence": prevalence})
        if adjustment:
            complete = frame[[treatment, *adjustment]].dropna()
            try:
                import statsmodels.api as sm
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
                _check(checks, "EXTREME_WEIGHT_RISK", overlap_status, "Inverse-weight instability risk.", {
                    "maximum_inverse_weight": float(max((1 / propensity).max(), (1 / (1 - propensity)).max()))
                })
            except Exception as exc:
                _check(checks, "PROPENSITY_ESTIMATION", "WARN", "Preliminary propensity model was not estimable.", {"exception_type": type(exc).__name__})
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
    overall = max((item["status"] for item in checks), key=rank.__getitem__)
    status = ScientificStatus(overall)
    return ScientificResultDescriptor(
        result_type=ResultType.DATA_ELIGIBILITY_RESULT,
        scientific_status=status,
        summary={"status": overall, "check_count": len(checks)},
        payload={"status": overall, "checks": checks},
        diagnostics={"checks": checks},
        warnings=[item for item in checks if item["status"] != "PASS"],
    )


def _check(items: list[dict[str, Any]], code: str, status: str, message: str, evidence: Any) -> None:
    items.append({"check_code": code, "status": status, "message": message, "evidence": evidence})


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
