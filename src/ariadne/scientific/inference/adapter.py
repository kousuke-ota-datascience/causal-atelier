"""DB-free adapter for binary-treatment ATE/ATT estimation."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from ariadne.product.domain.enums import GraphType, ScientificStatus
from ariadne.product.domain.errors import (
    InvalidAnalysisSpec,
    ScientificCoreExecutionError,
    UnsupportedEstimator,
)
from ariadne.product.domain.graph_semantics import validate_graph_document
from ariadne.product.ports.scientific_core import EstimationInput, EstimationOutput

_METHODS = {
    "difference_in_means": "diff_in_means",
    "diff_in_means": "diff_in_means",
    "ols": "ols_coefficient",
    "outcome_regression": "ols_coefficient",
    "ipw": "ipw",
    "aipw": "aipw",
}
_SPEC_FIELDS = {
    "treatment", "outcome", "estimand", "target_population", "adjustment_set",
    "assumptions", "inference_options",
}
_PARAM_FIELDS = {
    "diff_in_means": set(),
    "ols_coefficient": {"robust_se"},
    "ipw": {"propensity_clip"},
    "aipw": {"robust_se", "propensity_clip", "cross_fitting_folds"},
}


class EstimationAdapter:
    def run(self, input_: EstimationInput, output_dir: Path) -> EstimationOutput:
        estimator = input_.estimator.lower()
        if estimator not in _METHODS:
            raise UnsupportedEstimator(input_.estimator)
        unknown_spec = set(input_.analysis_spec) - _SPEC_FIELDS
        unknown_params = set(input_.parameters) - _PARAM_FIELDS[_METHODS[estimator]]
        if unknown_spec or unknown_params:
            raise InvalidAnalysisSpec(
                f"Unknown estimation fields: {sorted(unknown_spec | unknown_params)}"
            )
        spec = input_.analysis_spec
        treatment = _required_string(spec, "treatment")
        outcome = _required_string(spec, "outcome")
        estimand = str(spec.get("estimand", "")).upper()
        if estimand not in {"ATE", "ATT"}:
            raise InvalidAnalysisSpec("analysis_spec.estimand must be ATE or ATT")
        adjustment_set = spec.get("adjustment_set")
        if not isinstance(adjustment_set, list) or not all(
            isinstance(column, str) and column for column in adjustment_set
        ):
            raise InvalidAnalysisSpec("analysis_spec.adjustment_set must be an explicit list")
        if len(adjustment_set) != len(set(adjustment_set)):
            raise InvalidAnalysisSpec("adjustment_set must be unique")
        if treatment in adjustment_set or outcome in adjustment_set:
            raise InvalidAnalysisSpec("adjustment_set cannot contain treatment or outcome")

        frame = _load_dataset(input_.dataset_path)
        required = [treatment, outcome, *adjustment_set]
        missing = [column for column in required if column not in frame.columns]
        if missing:
            raise InvalidAnalysisSpec(f"analysis columns are missing: {missing}")
        graph = _load_graph(input_.graph_path)
        try:
            graph_type = GraphType(graph["graph_type"])
        except (KeyError, ValueError, TypeError) as exc:
            raise InvalidAnalysisSpec("graph.graph_type must be DAG, CPDAG, or PAG") from exc
        validate_graph_document(graph_type, graph)
        if treatment not in graph["nodes"] or outcome not in graph["nodes"]:
            return _negative_output(
                ScientificStatus.NOT_IDENTIFIED,
                estimator,
                "Treatment and outcome must both be present in the fixed graph.",
            )
        if not _has_semantic_path(graph, treatment, outcome):
            return _negative_output(
                ScientificStatus.NOT_IDENTIFIED,
                estimator,
                "The fixed graph contains no possibly directed treatment-to-outcome path.",
            )

        complete = frame.loc[:, required].dropna()
        counts = complete[treatment].value_counts()
        n_treated = int(counts.get(1, 0))
        n_control = int(counts.get(0, 0))
        diagnostics = {
            "sample_size": {
                "n_input": int(len(frame)), "n_complete": int(len(complete)),
                "n_treated": n_treated, "n_control": n_control,
                "sample_loss": int(len(frame) - len(complete)),
            }
        }
        if len(complete) < 20 or min(n_treated, n_control) < 5:
            return _negative_output(
                ScientificStatus.INSUFFICIENT_SAMPLE,
                estimator,
                "At least 20 complete observations and 5 observations per treatment arm are required.",
                diagnostics,
            )

        params = input_.parameters
        clip_value = params.get("propensity_clip", [0.01, 0.99])
        if not isinstance(clip_value, (list, tuple)) or len(clip_value) != 2:
            raise InvalidAnalysisSpec("propensity_clip must contain lower and upper bounds")
        clip = (float(clip_value[0]), float(clip_value[1]))
        try:
            from ariadne.causal.inference.diagnostics.balance import compute_balance_table
            from ariadne.causal.inference.diagnostics.design import summarize_design
            from ariadne.causal.inference.diagnostics.overlap import summarize_propensity_overlap
            from ariadne.causal.inference.estimators.treatment_effect import TreatmentEffectEstimator

            engine = TreatmentEffectEstimator(
                frame=complete,
                treatment=treatment,
                outcome=outcome,
                covariates=list(adjustment_set),
                estimand=estimand,
                robust_se=str(params.get("robust_se", "HC3")),
                propensity_clip=clip,
                cross_fitting_folds=int(params.get("cross_fitting_folds", 0)),
            )
            method = _METHODS[estimator]
            if method == "ipw":
                record = engine.ipw(estimand)
            elif method == "aipw":
                record = engine.aipw(estimand)
            elif method == "ols_coefficient":
                record = engine.ols()
            else:
                record = engine.diff_in_means()

            diagnostics["design"] = _first_record(summarize_design(complete, treatment))
            diagnostics["balance"] = _records(compute_balance_table(complete, treatment, adjustment_set))
            if engine.last_propensity_score is not None:
                overlap = _first_record(summarize_propensity_overlap(engine.last_propensity_score, clip))
                diagnostics["overlap"] = overlap
                extreme = int(overlap["n_ps_below_0_01"]) + int(overlap["n_ps_above_0_99"])
                if extreme / len(complete) > 0.2:
                    return _negative_output(
                        ScientificStatus.INSUFFICIENT_OVERLAP,
                        estimator,
                        "More than 20% of propensity scores are outside the configured overlap bounds.",
                        diagnostics,
                    )
        except InvalidAnalysisSpec:
            raise
        except ValueError as exc:
            raise InvalidAnalysisSpec(str(exc)) from exc
        except Exception as exc:
            raise ScientificCoreExecutionError(
                f"{estimator} estimation failed: {type(exc).__name__}: {exc}"
            ) from exc

        effect = float(record.effect)
        status = ScientificStatus.VALID
        warnings: list[str] = []
        if estimator in {"difference_in_means", "diff_in_means"}:
            warnings.append("Unadjusted difference in means does not control confounding.")
        if estimator in {"ols", "outcome_regression"} and estimand == "ATT":
            warnings.append("The additive OLS coefficient is used as the ATT contrast.")
        if not math.isfinite(effect) or record.std_error is None or not math.isfinite(float(record.std_error)):
            status = ScientificStatus.ESTIMATION_UNRELIABLE
            warnings.append("The estimator did not produce finite uncertainty.")

        payload = {
            "estimator": estimator,
            "estimand": estimand,
            "treatment": treatment,
            "outcome": outcome,
            "adjustment_set": list(adjustment_set),
            "estimate": effect if math.isfinite(effect) else None,
            "standard_error": record.std_error,
            "confidence_interval": [record.ci_low, record.ci_high]
            if record.ci_low is not None and record.ci_high is not None else None,
            "p_value": record.p_value,
        }
        output_dir.mkdir(parents=True, exist_ok=True)
        result_path = output_dir / f"{estimator}_result.json"
        result_path.write_text(json.dumps(payload, sort_keys=True, indent=2), encoding="utf-8")
        diagnostics_path = output_dir / f"{estimator}_diagnostics.json"
        diagnostics_path.write_text(json.dumps(diagnostics, sort_keys=True, indent=2), encoding="utf-8")
        return EstimationOutput(
            scientific_status=status,
            payload=payload,
            summary={
                "estimator": estimator, "estimand": estimand, "estimate": payload["estimate"],
                "standard_error": record.std_error, "confidence_interval": payload["confidence_interval"],
            },
            diagnostics=diagnostics,
            warnings=warnings,
            artifacts=[result_path, diagnostics_path],
        )


def _required_string(spec: dict[str, Any], name: str) -> str:
    value = spec.get(name)
    if not isinstance(value, str) or not value:
        raise InvalidAnalysisSpec(f"analysis_spec.{name} is required")
    return value


def _load_dataset(path: Path) -> pd.DataFrame:
    try:
        if path.suffix.lower() == ".parquet":
            return pd.read_parquet(path)
        if path.suffix.lower() == ".csv":
            return pd.read_csv(path)
    except Exception as exc:
        raise ScientificCoreExecutionError(f"Unable to read dataset: {exc}") from exc
    raise InvalidAnalysisSpec(f"Unsupported dataset format: {path.suffix!r}")


def _load_graph(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ScientificCoreExecutionError(f"Unable to read graph artifact: {exc}") from exc
    if not isinstance(value, dict):
        raise InvalidAnalysisSpec("graph artifact must contain a JSON object")
    return value


def _has_semantic_path(graph: dict[str, Any], start: str, goal: str) -> bool:
    adjacency: dict[str, set[str]] = {node: set() for node in graph["nodes"]}
    for edge in graph["edges"]:
        left = edge["endpoint_source"].upper()
        right = edge["endpoint_target"].upper()
        if left != "ARROW":
            adjacency[edge["source"]].add(edge["target"])
        if right != "ARROW":
            adjacency[edge["target"]].add(edge["source"])
    pending = [start]
    seen = {start}
    while pending:
        node = pending.pop()
        for target in adjacency[node]:
            if target == goal:
                return True
            if target not in seen:
                seen.add(target)
                pending.append(target)
    return False


def _records(frame: pd.DataFrame) -> list[dict[str, Any]]:
    return json.loads(frame.to_json(orient="records"))


def _first_record(frame: pd.DataFrame) -> dict[str, Any]:
    records = _records(frame)
    return records[0] if records else {}


def _negative_output(
    status: ScientificStatus,
    estimator: str,
    warning: str,
    diagnostics: dict[str, Any] | None = None,
) -> EstimationOutput:
    return EstimationOutput(
        scientific_status=status,
        payload={"estimator": estimator, "estimate": None, "standard_error": None, "confidence_interval": None},
        summary={"estimator": estimator, "estimate": None},
        diagnostics=diagnostics or {},
        warnings=[warning],
    )


__all__ = ["EstimationAdapter"]
