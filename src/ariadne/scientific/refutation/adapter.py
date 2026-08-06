"""Minimum ENH-E1 placebo-treatment and data-subset refuters."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from ariadne.product.domain.enums import ResultType, ScientificStatus
from ariadne.product.domain.errors import InvalidAnalysisSpec
from ariadne.product.ports.scientific_core import (
    RefutationInput, ScientificResultDescriptor,
)
from ariadne.scientific.inference.adapter import EstimationAdapter


class RefutationAdapter:
    def run(self, input_: RefutationInput, output_dir: Path) -> list[ScientificResultDescriptor]:
        method = input_.method.upper()
        spec = input_.analysis_spec["operation_spec"]
        frame = _load(input_.dataset_path)
        seed = input_.random_seed if input_.random_seed is not None else 0
        rng = np.random.default_rng(seed)
        base = input_.base_result
        base_payload = base.get("payload", base)
        base_estimate = base_payload.get("estimate")
        if not isinstance(base_estimate, (int, float)):
            raise InvalidAnalysisSpec("upstream Treatment Effect Result has no numeric estimate")
        question = input_.analysis_spec.get("causal_question") or base.get("causal_question")
        design = input_.analysis_spec.get("causal_design") or base.get("causal_design")
        if not isinstance(question, dict) or not isinstance(design, dict):
            raise InvalidAnalysisSpec("base causal question/design are required")
        estimation_spec = {
            **input_.analysis_spec,
            "causal_question": question,
            "causal_design": design,
            "operation_spec": {
                "estimator": base_payload.get("estimator"),
                "inference_options": {},
            },
        }
        estimator = str(base_payload.get("estimator", ""))
        if not estimator:
            raise InvalidAnalysisSpec("base estimator is required")

        if method == "PLACEBO_TREATMENT":
            repetitions = int(spec.get("repetitions", 0))
            if repetitions < 2:
                raise InvalidAnalysisSpec("PLACEBO_TREATMENT requires repetitions >= 2")
            estimates = []
            treatment = question["treatment"]
            for index in range(repetitions):
                perturbed = frame.copy()
                perturbed[treatment] = rng.permutation(perturbed[treatment].to_numpy())
                estimates.append(self._estimate(perturbed, input_, estimation_spec, estimator, output_dir / str(index)))
            estimate = float(np.mean(estimates))
            std = float(np.std(estimates, ddof=1))
            failure = abs(estimate) > 1.96 * std if std > 0 else estimate != 0
            perturbation = {"repetitions": repetitions, "null": 0.0}
            metric = {"mean_placebo_effect": estimate, "standard_deviation": std}
        elif method == "DATA_SUBSET":
            fraction = float(spec.get("subset_fraction", 0))
            if not 0 < fraction < 1:
                raise InvalidAnalysisSpec("DATA_SUBSET requires 0 < subset_fraction < 1")
            indexes = rng.choice(
                len(frame), size=min(len(frame), max(20, int(len(frame) * fraction))), replace=False
            )
            estimate = self._estimate(frame.iloc[indexes], input_, estimation_spec, estimator, output_dir)
            base_se = base_payload.get("standard_error")
            tolerance = 1.96 * float(base_se) if isinstance(base_se, (int, float)) else 0.0
            failure = abs(estimate - float(base_estimate)) > tolerance if tolerance else False
            perturbation = {"subset_fraction": fraction, "n": len(indexes)}
            metric = {"absolute_difference": abs(estimate - float(base_estimate)), "tolerance": tolerance}
        else:
            raise InvalidAnalysisSpec(f"Unsupported refutation method: {method}")

        status = ScientificStatus.FAILURE_DETECTED if failure else ScientificStatus.NO_FAILURE_DETECTED
        payload = {
            "method": method, "random_seed": seed, "perturbation": perturbation,
            "base_estimate": float(base_estimate), "refutation_estimate": estimate,
            "metric": metric, "severity": "FAIL" if failure else "PASS",
            "interpretation": (
                "A specified failure was detected."
                if failure else
                "No specified failure was detected. This does not prove the identification assumptions."
            ),
        }
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "refutation_result.json").write_text(json.dumps(payload, sort_keys=True, indent=2), encoding="utf-8")
        return [ScientificResultDescriptor(
            result_type=ResultType.REFUTATION_RESULT,
            scientific_status=status,
            summary={"method": method, "severity": payload["severity"]},
            payload=payload,
        )]

    @staticmethod
    def _estimate(frame: pd.DataFrame, input_: RefutationInput, spec: dict, estimator: str, output_dir: Path) -> float:  # type: ignore[type-arg]
        path = output_dir / "input.csv"
        output_dir.mkdir(parents=True, exist_ok=True)
        frame.to_csv(path, index=False)
        from ariadne.product.ports.scientific_core import EstimationInput
        descriptors = EstimationAdapter().run(EstimationInput(
            dataset_path=path, graph_path=input_.graph_path, estimator=estimator,
            upstream_result=input_.base_result, parameters=input_.parameters,
            random_seed=input_.random_seed, analysis_spec=spec,
        ), output_dir)
        estimate = descriptors[0].payload.get("estimate")
        if not isinstance(estimate, (int, float)):
            raise InvalidAnalysisSpec("Refutation estimator did not return an estimate")
        return float(estimate)


def _load(path: Path) -> pd.DataFrame:
    return pd.read_parquet(path) if path.suffix.lower() == ".parquet" else pd.read_csv(path)
