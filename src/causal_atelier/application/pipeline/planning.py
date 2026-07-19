"""Execution plan construction shared by all interfaces."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from causal_atelier.application.pipeline.artifacts import ArtifactRegistry, ArtifactSpec
from causal_atelier.application.pipeline.configuration import (
    load_yaml_mapping,
    resolve_project_path,
)


@dataclass(frozen=True)
class StagePlan:
    """Resolved plan for one stage."""

    name: Literal["discovery", "inference"]
    enabled: bool
    input_paths: dict[str, Path]
    output_paths: dict[str, Path]
    config_paths: dict[str, Path]
    resolved_args: list[str]
    metadata: dict[str, Any]


@dataclass(frozen=True)
class ExecutionPlan:
    """Resolved integrated pipeline plan."""

    run_id: str
    strategy: str
    stages: list[StagePlan]
    resolved_configs: dict[str, Path]
    artifact_registry: ArtifactRegistry
    validation_checks: list[str]
    metadata: dict[str, Any]

    def enabled_stages(self) -> list[StagePlan]:
        """Return enabled stages in execution order."""

        return [stage for stage in self.stages if stage.enabled]

    def to_dict(self) -> dict[str, Any]:
        """Serialize the execution plan for dry-run output."""

        return {
            "run_id": self.run_id,
            "selected_pipeline_strategy": self.strategy,
            "stages": [
                {
                    "name": stage.name,
                    "enabled": stage.enabled,
                    "input_paths": {key: str(path) for key, path in stage.input_paths.items()},
                    "output_paths": {key: str(path) for key, path in stage.output_paths.items()},
                    "config_paths": {key: str(path) for key, path in stage.config_paths.items()},
                    "child_stage_args": stage.resolved_args,
                    "metadata": stage.metadata,
                }
                for stage in self.stages
            ],
            "resolved_config_paths": {key: str(path) for key, path in self.resolved_configs.items()},
            "validation_checks": self.validation_checks,
            "artifact_plan": self.artifact_registry.to_dict(),
            "metadata": self.metadata,
        }


class PipelinePlanner:
    """Build an execution plan from integrated CLI arguments."""

    def __init__(self, project_root: Path) -> None:
        """Initialize the planner."""

        self.project_root = project_root

    def build_plan(self, args: Any, *, strategy_name: str) -> ExecutionPlan:
        """Build a resolved execution plan."""

        pipeline_config_path = resolve_project_path(
            args.pipeline_config
            or Path("configs/causal/inference/pipeline.yaml"),
            self.project_root,
        )
        pipeline_config = (
            load_yaml_mapping(pipeline_config_path) if pipeline_config_path.exists() else {}
        )
        pipeline = dict(pipeline_config.get("pipeline", {}))
        stages_config = dict(pipeline_config.get("stages", {}))
        run_id = args.run_id or pipeline.get("run_id") or uuid.uuid4().hex[:12]
        random_seed = int(args.random_seed or pipeline.get("random_seed", 42))

        discovery_stage = self._build_discovery_stage(
            args=args,
            stage_config=dict(stages_config.get("discovery", {})),
            run_id=run_id,
            random_seed=random_seed,
        )
        inference_stage = self._build_inference_stage(
            args=args,
            stage_config=dict(stages_config.get("inference", {})),
            discovery_manifest=discovery_stage.output_paths["manifest"],
            run_id=run_id,
            random_seed=random_seed,
        )
        registry = ArtifactRegistry(
            tuple(
                ArtifactSpec(f"{stage.name}.{name}", path, required=name == "manifest")
                for stage in (discovery_stage, inference_stage)
                for name, path in stage.output_paths.items()
            )
        )
        resolved_configs = {
            "pipeline": pipeline_config_path,
            **{f"discovery.{key}": value for key, value in discovery_stage.config_paths.items()},
            **{f"inference.{key}": value for key, value in inference_stage.config_paths.items()},
        }
        return ExecutionPlan(
            run_id=str(run_id),
            strategy=strategy_name,
            stages=[discovery_stage, inference_stage],
            resolved_configs=resolved_configs,
            artifact_registry=registry,
            validation_checks=[
                "config_file_exists",
                "output_dir_resolves",
                "discovery_manifest_schema",
                "feature_semantics_consistency",
                "causal_design_presence",
                "adjustment_set_validity",
            ],
            metadata={
                "project_root": str(self.project_root),
                "random_seed": random_seed,
                "pipeline_config": str(pipeline_config_path),
            },
        )

    def _build_discovery_stage(
        self,
        *,
        args: Any,
        stage_config: dict[str, Any],
        run_id: str,
        random_seed: int,
    ) -> StagePlan:
        enabled = bool(stage_config.get("enabled", True))
        analysis_config = resolve_project_path(
            args.discovery_analysis_config
            or stage_config.get(
                "analysis_config",
                Path("configs/causal/discovery.yaml"),
            ),
            self.project_root,
        )
        feature_config = resolve_project_path(
            args.discovery_feature_config
            or stage_config.get(
                "feature_config",
                Path("configs/preprocessing/discovery_features.yaml"),
            ),
            self.project_root,
        )
        output_dir = resolve_project_path(
            args.discovery_output_dir
            or stage_config.get(
                "output_dir",
                Path("artifacts/pipelines/causal_discovery"),
            ),
            self.project_root,
        )
        child_args = [
            "--project-root",
            str(self.project_root),
            "--analysis-config",
            str(analysis_config),
            "--feature-config",
            str(feature_config),
            "--output-dir",
            str(output_dir),
        ]
        _append_value(child_args, "--dataset-yaml", args.dataset_yaml)
        _append_value(child_args, "--campaign-id", args.campaign_id)
        _append_value(child_args, "--pre-weeks", args.pre_weeks)
        _append_value(child_args, "--collinearity-threshold", args.collinearity_threshold)
        _append_many(child_args, "--algorithms", args.discovery_algorithms)
        _append_value(child_args, "--alpha", args.discovery_alpha)
        _append_many(child_args, "--alpha-grid", args.discovery_alpha_grid)
        _append_value(child_args, "--pc-indep-test", args.discovery_pc_indep_test)
        _append_value(child_args, "--bootstrap-samples", args.discovery_bootstrap_samples)
        _append_value(child_args, "--bootstrap-sample-fraction", args.discovery_bootstrap_sample_fraction)
        _append_value(child_args, "--random-seed", args.discovery_random_seed or random_seed)
        _append_flag(child_args, "--no-background-knowledge", args.discovery_no_background_knowledge)
        _append_value(child_args, "--notears-threshold", args.discovery_notears_threshold)
        return StagePlan(
            name="discovery",
            enabled=enabled,
            input_paths={},
            output_paths={
                "output_dir": output_dir,
                "manifest": output_dir / "manifest.yaml",
                "resolved_feature_semantics": output_dir / "resolved_feature_semantics.yaml",
            },
            config_paths={
                "analysis_config": analysis_config,
                "feature_config": feature_config,
            },
            resolved_args=child_args,
            metadata={"run_id": run_id, "random_seed": random_seed},
        )

    def _build_inference_stage(
        self,
        *,
        args: Any,
        stage_config: dict[str, Any],
        discovery_manifest: Path,
        run_id: str,
        random_seed: int,
    ) -> StagePlan:
        enabled = bool(stage_config.get("enabled", True))
        config_path = resolve_project_path(
            args.inference_config
            or stage_config.get(
                "config",
                Path("configs/causal/inference/defaults.yaml"),
            ),
            self.project_root,
        )
        output_dir = resolve_project_path(
            args.inference_output_dir
            or stage_config.get(
                "output_dir",
                Path("artifacts/pipelines/causal_inference"),
            ),
            self.project_root,
        )
        feature_config = resolve_project_path(
            args.inference_feature_config
            or stage_config.get(
                "feature_config",
                Path("configs/preprocessing/inference_features.yaml"),
            ),
            self.project_root,
        )
        causal_design = resolve_project_path(
            stage_config.get(
                "causal_design",
                Path("configs/causal/inference/designs/completejourney_household.yaml"),
            ),
            self.project_root,
        )
        feature_semantics = resolve_project_path(
            stage_config.get(
                "feature_semantics",
                Path("configs/preprocessing/feature_semantics.yaml"),
            ),
            self.project_root,
        )
        child_args = [
            "--project-root",
            str(self.project_root),
            "--config",
            str(config_path),
            "--feature-config",
            str(feature_config),
            "--discovery-manifest",
            str(discovery_manifest),
            "--output-dir",
            str(output_dir),
        ]
        _append_value(child_args, "--dataset-yaml", args.dataset_yaml)
        _append_value(child_args, "--campaign-id", args.campaign_id)
        _append_value(child_args, "--pre-weeks", args.pre_weeks)
        _append_value(child_args, "--collinearity-threshold", args.collinearity_threshold)
        _append_value(child_args, "--mode", args.inference_mode)
        _append_value(child_args, "--treatment", args.inference_treatment)
        _append_value(child_args, "--outcome", args.inference_outcome)
        _append_value(child_args, "--estimand", args.inference_estimand)
        _append_many(child_args, "--effect-methods", args.inference_effect_methods)
        _append_value(child_args, "--adjustment-strategy", args.inference_adjustment_strategy)
        _append_many(child_args, "--covariates", args.inference_covariates)
        _append_value(child_args, "--robust-se", args.inference_robust_se)
        _append_value(child_args, "--min-samples", args.inference_min_samples)
        _append_value(child_args, "--edge-robust-se", args.inference_edge_robust_se)
        return StagePlan(
            name="inference",
            enabled=enabled,
            input_paths={
                "discovery_manifest": discovery_manifest,
                "feature_semantics": feature_semantics,
                "causal_design": causal_design,
            },
            output_paths={"output_dir": output_dir, "manifest": output_dir / "manifest.yaml"},
            config_paths={
                "config": config_path,
                "feature_config": feature_config,
                "causal_design": causal_design,
                "feature_semantics": feature_semantics,
            },
            resolved_args=child_args,
            metadata={"run_id": run_id, "random_seed": random_seed},
        )


def _append_value(output: list[str], flag: str, value: Any | None) -> None:
    if value is not None:
        output.extend([flag, str(value)])


def _append_many(output: list[str], flag: str, values: list[Any] | tuple[Any, ...] | None) -> None:
    if values:
        output.append(flag)
        output.extend(str(value) for value in values)


def _append_flag(output: list[str], flag: str, value: bool | None) -> None:
    if value:
        output.append(flag)


__all__ = ["ExecutionPlan", "PipelinePlanner", "StagePlan"]
