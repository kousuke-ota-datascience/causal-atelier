"""Minimum ENH-E1 adjustment-set and propensity-clipping sensitivity."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any

from ariadne.product.domain.enums import ResultType, ScientificStatus
from ariadne.product.domain.errors import InvalidAnalysisSpec
from ariadne.product.ports.scientific_core import (
    EstimationInput, ScientificResultDescriptor, SensitivityInput,
)
from ariadne.scientific.inference.adapter import EstimationAdapter


class SensitivityAdapter:
    def run(self, input_: SensitivityInput, output_dir: Path) -> list[ScientificResultDescriptor]:
        base = input_.base_result.get("payload", input_.base_result)
        base_estimate = base.get("estimate")
        estimator = str(base.get("estimator", ""))
        if not isinstance(base_estimate, (int, float)) or not estimator:
            raise InvalidAnalysisSpec("numeric base estimate and estimator are required")
        spec = input_.analysis_spec["operation_spec"]
        dimension = input_.dimension.upper()
        variants: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
        if dimension == "ADJUSTMENT_SET":
            sets = spec.get("adjustment_sets")
            if not isinstance(sets, list) or not sets:
                raise InvalidAnalysisSpec("ADJUSTMENT_SET requires adjustment_sets")
            for value in sets:
                if not isinstance(value, list):
                    raise InvalidAnalysisSpec("each adjustment set must be a list")
                variants.append((str(value), {"adjustment_set": value}, input_.parameters))
        elif dimension == "PROPENSITY_CLIPPING":
            values = spec.get("values")
            if not isinstance(values, list) or not values:
                raise InvalidAnalysisSpec("PROPENSITY_CLIPPING requires values")
            for value in values:
                threshold = float(value)
                if not 0 < threshold < .5:
                    raise InvalidAnalysisSpec("clipping threshold must be between 0 and 0.5")
                variants.append((str(threshold), {}, {**input_.parameters, "propensity_clip": [threshold, 1-threshold]}))
        else:
            raise InvalidAnalysisSpec(f"Unsupported sensitivity dimension: {dimension}")

        estimates: list[dict[str, Any]] = []
        for index, (label, design_change, parameters) in enumerate(variants):
            analysis_spec = {**input_.analysis_spec}
            analysis_spec["causal_design"] = {
                **analysis_spec.get("causal_design", {}), **design_change,
            }
            analysis_spec["operation_spec"] = {"estimator": estimator, "inference_options": {}}
            descriptors = EstimationAdapter().run(EstimationInput(
                dataset_path=input_.dataset_path, graph_path=input_.graph_path,
                estimator=estimator, upstream_result=input_.base_result,
                parameters=parameters, random_seed=input_.random_seed,
                analysis_spec=analysis_spec,
            ), output_dir / str(index))
            estimates.append({"variation": label, **descriptors[0].payload})
        values = [float(item["estimate"]) for item in estimates if isinstance(item.get("estimate"), (int, float))]
        if not values:
            status = ScientificStatus.INCONCLUSIVE
            sign_reversal = decision_reversal = False
            effect_range: list[float] | None = None
        else:
            base_sign = float(base_estimate) >= 0
            sign_reversal = any((value >= 0) != base_sign for value in values)
            base_ci = base.get("confidence_interval")
            base_decision = bool(base_ci and (base_ci[0] > 0 or base_ci[1] < 0))
            decisions = [
                bool(item.get("confidence_interval") and (
                    item["confidence_interval"][0] > 0 or item["confidence_interval"][1] < 0
                )) for item in estimates
            ]
            decision_reversal = any(value != base_decision for value in decisions)
            status = ScientificStatus.FRAGILE if sign_reversal or decision_reversal else ScientificStatus.ROBUST
            effect_range = [min(values), max(values)]
        payload = {
            "base_specification": base,
            "changed_dimension": dimension,
            "variation": estimates,
            "effect_range": effect_range,
            "sign_reversal": sign_reversal,
            "decision_reversal": decision_reversal,
            "warning": "This shows conclusion dependence over the specified range; it does not guarantee causal assumptions.",
        }
        return [ScientificResultDescriptor(
            result_type=ResultType.SENSITIVITY_RESULT,
            scientific_status=status,
            summary={"dimension": dimension, "effect_range": effect_range},
            payload=payload,
            warnings=[payload["warning"]],
        )]
