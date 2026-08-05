"""Stage-local runner for causal discovery."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ariadne.application.discovery.factory import (
    build_discovery_application_service,
    build_discovery_request_from_argv,
)
from ariadne.application.pipeline.configuration import dump_yaml, load_yaml_mapping
from ariadne.preprocessing.common import FeatureSemanticsCatalog
from ariadne.shared.validation import ValidationIssue, ValidationSeverity


def _extract_project_root(resolved_args: list[str]) -> Path | None:
    """Extract --project-root value from a resolved_args list.

    Returns None if the flag is absent; the factory will raise in that case.
    """
    try:
        idx = resolved_args.index("--project-root")
        return Path(resolved_args[idx + 1]).resolve()
    except (ValueError, IndexError):
        return None


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
        """Run causal discovery via the Application Service."""

        # Extract project_root from the resolved_args list that the planner
        # always includes as --project-root <path>.
        project_root = _extract_project_root(stage_plan.resolved_args)

        request = build_discovery_request_from_argv(
            stage_plan.resolved_args,
            project_root=project_root,
        )
        service = build_discovery_application_service(request.project_root)
        result = service.execute(request)

        output_dir = result.output_dir
        feature_config_path = stage_plan.config_paths.get("feature_config")
        if feature_config_path is not None:
            semantics_path = output_dir / "resolved_feature_semantics.yaml"
            self._write_resolved_feature_semantics(
                Path(feature_config_path), semantics_path
            )
        else:
            semantics_path = None

        planned_artifacts = {
            "edges_pc": output_dir / "pc" / "edges.csv",
            "edges_ges": output_dir / "ges" / "edges.csv",
            "edges_lingam": output_dir / "lingam" / "edges.csv",
            "edges_notears": output_dir / "notears" / "edges.csv",
            "bootstrap_summary": output_dir / "pc" / "edge_stability.csv",
            "resolved_config": output_dir / "resolved_analysis_config.yaml",
            "resolved_feature_config": output_dir / "resolved_features_config.yaml",
        }
        if semantics_path is not None:
            planned_artifacts["resolved_feature_semantics"] = semantics_path

        artifacts = {
            name: path
            for name, path in planned_artifacts.items()
            if path.exists()
        }
        return {
            "status": result.status,
            "artifacts": artifacts,
            "metadata": {"runner": self.name, "output_dir": str(output_dir)},
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

