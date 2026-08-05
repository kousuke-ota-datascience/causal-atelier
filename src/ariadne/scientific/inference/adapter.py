"""Scientific Core adapter – wraps legacy causal inference estimators.

This adapter converts between the Product domain's ScientificCorePort interface
and the existing causal inference implementation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from ariadne.product.domain.enums import ScientificStatus
from ariadne.product.ports.scientific_core import EstimationInput, EstimationOutput


class EstimationAdapter:
    """Adapter from EstimationInput → EstimationOutput using legacy inference."""

    def run(self, input_: EstimationInput, output_dir: Path) -> EstimationOutput:
        output_dir.mkdir(parents=True, exist_ok=True)

        df = _load_dataset(input_.dataset_path)
        graph_json = _load_graph(input_.graph_path)
        estimator = input_.estimator.lower()
        params = input_.parameters
        spec = input_.analysis_spec

        treatment = spec.get("treatment")
        outcome = spec.get("outcome")
        if not treatment or not outcome:
            return EstimationOutput(
                scientific_status=ScientificStatus.SCIENTIFIC_ERROR,
                warnings=["analysis_spec must include 'treatment' and 'outcome'"],
            )

        try:
            result = _run_estimator(
                df=df,
                graph_json=graph_json,
                estimator=estimator,
                treatment=treatment,
                outcome=outcome,
                params=params,
                spec=spec,
                random_seed=input_.random_seed,
            )
        except Exception as exc:
            return EstimationOutput(
                scientific_status=ScientificStatus.SCIENTIFIC_ERROR,
                warnings=[str(exc)],
            )

        # Save artifacts
        artifact_paths: list[Path] = []
        results_path = output_dir / f"{estimator}_results.json"
        results_path.write_text(json.dumps(result, indent=2, default=str))
        artifact_paths.append(results_path)

        scientific_status = _determine_scientific_status(result)

        return EstimationOutput(
            scientific_status=scientific_status,
            payload=result,
            summary=_build_summary(result),
            artifacts=artifact_paths,
        )


def _run_estimator(
    df: pd.DataFrame,
    graph_json: dict[str, Any],
    estimator: str,
    treatment: str,
    outcome: str,
    params: dict[str, Any],
    spec: dict[str, Any],
    random_seed: int | None,
) -> dict[str, Any]:
    """Dispatch to the appropriate legacy estimator."""
    try:
        from ariadne.causal.inference.estimators import run_ate_estimation  # type: ignore[import]
    except ImportError:
        # Fall back to econml directly if the wrapper is unavailable
        return _run_econml_directly(df, estimator, treatment, outcome, params, random_seed)

    return run_ate_estimation(
        df=df,
        graph=graph_json,
        estimator=estimator,
        treatment=treatment,
        outcome=outcome,
        params=params,
        spec=spec,
        random_seed=random_seed,
    )


def _run_econml_directly(
    df: pd.DataFrame,
    estimator: str,
    treatment: str,
    outcome: str,
    params: dict[str, Any],
    random_seed: int | None,
) -> dict[str, Any]:
    """Minimal econml-based ATE estimation as fallback."""
    import numpy as np
    from econml.dr import DRLearner  # type: ignore[import]

    X_cols = [c for c in df.columns if c not in (treatment, outcome)]
    T = df[treatment].values
    Y = df[outcome].values
    X = df[X_cols].values if X_cols else np.ones((len(df), 1))

    rng = np.random.RandomState(random_seed or 42)
    est = DRLearner(random_state=rng)
    est.fit(Y, T, X=X)
    ate = float(est.ate(X))

    return {
        "estimator": estimator,
        "treatment": treatment,
        "outcome": outcome,
        "ate": ate,
        "confidence_interval": None,
    }


def _load_dataset(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".parquet":
        return pd.read_parquet(path)
    if suffix == ".csv":
        return pd.read_csv(path)
    raise ValueError(f"Unsupported dataset format: {suffix!r}")


def _load_graph(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _determine_scientific_status(result: dict[str, Any]) -> ScientificStatus:
    if result.get("identified") is False:
        return ScientificStatus.NOT_IDENTIFIED
    ci = result.get("confidence_interval")
    if ci is None:
        return ScientificStatus.ESTIMATION_UNRELIABLE
    return ScientificStatus.ESTIMATION_RELIABLE


def _build_summary(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "estimator": result.get("estimator"),
        "treatment": result.get("treatment"),
        "outcome": result.get("outcome"),
        "ate": result.get("ate"),
    }
