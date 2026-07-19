"""Stage-local runner for causal discovery."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from causal_atelier.application.pipeline.configuration import dump_yaml, load_yaml_mapping
from causal_atelier.preprocessing.common import FeatureSemanticsCatalog
from causal_atelier.shared.validation import ValidationIssue, ValidationSeverity


class DiscoveryStageRunner:
    """Run and validate the discovery stage only."""

    name = "discovery"

    def validate_plan(self, stage_plan: Any) -> list[ValidationIssue]:
        """Validate discovery-stage inputs."""

        issues: list[ValidationIssue] = []
        for name, path in stage_plan.config_paths.items():
            if not Path(path).exists():
                issues.append(
                    ValidationIssue(
                        ValidationSeverity.ERROR,
                        "discovery_config_missing",
                        f"missing discovery config: {path}",
                        f"discovery.{name}",
                    )
                )
        return issues

    def run(self, stage_plan: Any) -> dict[str, Any]:
        """Run causal discovery via the stage-local CLI."""

        from causal_atelier.interfaces.cli.discovery import main as discovery_main

        discovery_main(stage_plan.resolved_args)
        output_dir = Path(stage_plan.output_paths["output_dir"])
        feature_config_path = Path(stage_plan.config_paths["feature_config"])
        semantics_path = output_dir / "resolved_feature_semantics.yaml"
        self._write_resolved_feature_semantics(feature_config_path, semantics_path)
        planned_artifacts = {
            "edges_pc": output_dir / "pc" / "edges.csv",
            "edges_ges": output_dir / "ges" / "edges.csv",
            "edges_lingam": output_dir / "lingam" / "edges.csv",
            "edges_notears": output_dir / "notears" / "edges.csv",
            "bootstrap_summary": output_dir / "pc" / "edge_stability.csv",
            "resolved_config": output_dir / "resolved_analysis_config.yaml",
            "resolved_feature_config": output_dir / "resolved_features_config.yaml",
            "resolved_feature_semantics": semantics_path,
        }
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

    def _write_resolved_feature_semantics(
        self,
        feature_config_path: Path,
        output_path: Path,
    ) -> None:
        """Derive and write feature semantics from the discovery feature config."""

        catalog = FeatureSemanticsCatalog.from_feature_config_mapping(
            load_yaml_mapping(feature_config_path)
        )
        dump_yaml(output_path, catalog.to_dict())


__all__ = ["DiscoveryStageRunner"]
