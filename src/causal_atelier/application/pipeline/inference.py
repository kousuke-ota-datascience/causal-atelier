"""Stage-local runner for causal inference."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from causal_atelier.application.pipeline.configuration import load_yaml_mapping
from causal_atelier.shared.validation import ValidationIssue, ValidationSeverity


class InferenceStageRunner:
    """Run and validate the inference stage only."""

    name = "inference"

    def validate_plan(self, stage_plan: Any) -> list[ValidationIssue]:
        """Validate inference-stage inputs."""

        issues: list[ValidationIssue] = []
        for name, path in stage_plan.config_paths.items():
            if name in {"causal_design", "feature_semantics"}:
                continue
            if not Path(path).exists():
                issues.append(
                    ValidationIssue(
                        ValidationSeverity.ERROR,
                        "inference_config_missing",
                        f"missing inference config: {path}",
                        f"inference.{name}",
                    )
                )
        manifest = Path(stage_plan.input_paths["discovery_manifest"])
        if not manifest.exists():
            issues.append(
                ValidationIssue(
                    ValidationSeverity.ERROR,
                    "discovery_manifest_missing",
                    f"missing discovery manifest: {manifest}",
                    "inference.discovery_manifest",
                )
            )
        return issues

    def run(self, stage_plan: Any) -> dict[str, Any]:
        """Run causal inference via the stage-local CLI."""

        from causal_atelier.interfaces.cli.inference import main as inference_main

        inference_main(stage_plan.resolved_args)
        output_dir = Path(stage_plan.output_paths["output_dir"])
        mode = _resolved_mode(stage_plan)
        planned_artifacts = {
            "resolved_config": output_dir / "resolved_config.yaml",
            "resolved_feature_config": output_dir / "resolved_feature_config.yaml",
        }
        if mode == "edge_weight":
            planned_artifacts.update(
                {
                    "edge_effects": output_dir / "edge_weight" / "edge_effects.csv",
                    "report_edge_weight": output_dir / "edge_weight" / "edge_effects.md",
                }
            )
        if mode == "treatment_effect":
            planned_artifacts.update(
                {
                    "treatment_effects": output_dir / "treatment_effect" / "treatment_effects.csv",
                    "report_treatment_effect": output_dir / "treatment_effect" / "treatment_effects.md",
                }
            )
        artifacts = {
            name: path
            for name, path in planned_artifacts.items()
            if path.exists()
        }
        return {
            "status": "ok",
            "artifacts": artifacts,
            "metadata": {"runner": self.name},
        }


__all__ = ["InferenceStageRunner"]


def _resolved_mode(stage_plan: Any) -> str:
    args = list(stage_plan.resolved_args)
    if "--mode" in args:
        return str(args[args.index("--mode") + 1])
    config_path = Path(stage_plan.config_paths["config"])
    if config_path.exists():
        return str(load_yaml_mapping(config_path).get("mode", "edge_weight"))
    return "edge_weight"
