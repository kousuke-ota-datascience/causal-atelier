"""Stage runner protocol and pipeline executor."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from ariadne.shared.validation import ValidationIssue, ValidationSeverity

from ariadne.application.pipeline.artifacts import RunManifest
from .planning import ExecutionPlan, StagePlan


@dataclass(frozen=True)
class StageResult:
    """Result returned after one stage executes."""

    stage: str
    status: str
    artifacts: dict[str, Path]
    metadata: dict[str, Any]


class StageRunner(Protocol):
    """Protocol for stage-local runner adapters."""

    name: str

    def validate_plan(self, stage_plan: StagePlan) -> list[ValidationIssue]:
        """Validate a stage-local plan."""

    def run(self, stage_plan: StagePlan) -> StageResult | dict[str, Any]:
        """Run a stage."""


class PipelineExecutor:
    """Execute enabled stages in plan order."""

    def __init__(self, runners: dict[str, StageRunner]) -> None:
        """Initialize the executor."""

        self.runners = runners

    @classmethod
    def default(cls) -> "PipelineExecutor":
        """Build the default executor with discovery and inference runners."""

        from ariadne.application.pipeline.discovery import DiscoveryStageRunner
        from ariadne.application.pipeline.inference import InferenceStageRunner

        return cls(
            {
                "discovery": DiscoveryStageRunner(),
                "inference": InferenceStageRunner(),
            }
        )

    def execute(self, plan: ExecutionPlan) -> list[StageResult]:
        """Execute all enabled stages."""

        results: list[StageResult] = []
        for stage_plan in plan.enabled_stages():
            runner = self.runners[stage_plan.name]
            issues = runner.validate_plan(stage_plan)
            errors = [issue for issue in issues if issue.severity == ValidationSeverity.ERROR]
            if errors:
                messages = "; ".join(issue.message for issue in errors)
                raise ValueError(f"{stage_plan.name} validation failed: {messages}")
            raw_result = runner.run(stage_plan)
            result = _coerce_stage_result(stage_plan.name, raw_result)
            self._write_manifest(plan, stage_plan, result)
            results.append(result)
        return results

    def _write_manifest(
        self,
        plan: ExecutionPlan,
        stage_plan: StagePlan,
        result: StageResult,
    ) -> None:
        manifest_path = stage_plan.output_paths["manifest"]
        output_dir = stage_plan.output_paths["output_dir"]
        manifest = RunManifest.build(
            run_label=plan.run_label,
            stage=stage_plan.name,
            output_dir=output_dir,
            config_paths=stage_plan.config_paths,
            artifacts={**stage_plan.output_paths, **result.artifacts},
            random_seed=stage_plan.metadata.get("random_seed"),
            metadata={**stage_plan.metadata, **result.metadata},
        )
        manifest.write(manifest_path)


def _coerce_stage_result(stage_name: str, raw_result: StageResult | dict[str, Any]) -> StageResult:
    if isinstance(raw_result, StageResult):
        return raw_result
    artifacts = {
        name: Path(path)
        for name, path in dict(raw_result.get("artifacts", {})).items()
    }
    return StageResult(
        stage=stage_name,
        status=str(raw_result.get("status", "ok")),
        artifacts=artifacts,
        metadata=dict(raw_result.get("metadata", {})),
    )


__all__ = ["PipelineExecutor", "StageResult", "StageRunner"]
