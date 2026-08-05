"""Pipeline execution strategies."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from ariadne.shared.validation import ValidationResult, ValidationSeverity

from .execution import PipelineExecutor, StageResult
from .planning import ExecutionPlan
from .validation import CrossStageValidator


@dataclass(frozen=True)
class PipelineCommandResult:
    """Result of a pipeline-level command strategy."""

    strategy: str
    status: str
    validation: ValidationResult | None = None
    stage_results: list[StageResult] | None = None
    payload: dict[str, Any] | None = None


class PipelineCommandStrategy(Protocol):
    """Protocol for integrated CLI execution strategies."""

    name: str

    def execute(self, plan: ExecutionPlan) -> PipelineCommandResult:
        """Execute a plan."""


class DryRunStrategy:
    """Render the execution plan without running validation or stages."""

    name = "dry_run"

    def execute(self, plan: ExecutionPlan) -> PipelineCommandResult:
        """Return the serialized plan."""

        return PipelineCommandResult(
            strategy=self.name,
            status="ok",
            payload=plan.to_dict(),
        )


class ValidateOnlyStrategy:
    """Validate the execution plan without running stages."""

    name = "validate_only"

    def __init__(self, validator: CrossStageValidator | None = None) -> None:
        self.validator = validator or CrossStageValidator()

    def execute(self, plan: ExecutionPlan) -> PipelineCommandResult:
        """Validate the plan."""

        validation = self.validator.validate(plan)
        return PipelineCommandResult(
            strategy=self.name,
            status="error" if validation.has_errors else "ok",
            validation=validation,
        )


class RunStrategy:
    """Run validation and then execute stages."""

    name = "run"

    def __init__(
        self,
        *,
        validator: CrossStageValidator | None = None,
        executor: PipelineExecutor | None = None,
    ) -> None:
        self.validator = validator or CrossStageValidator()
        self.executor = executor or PipelineExecutor.default()

    def execute(self, plan: ExecutionPlan) -> PipelineCommandResult:
        """Validate and execute the plan."""

        validation = self.validator.validate(plan)
        if validation.has_errors:
            return PipelineCommandResult(
                strategy=self.name,
                status="error",
                validation=validation,
            )
        stage_results = self.executor.execute(plan)
        return PipelineCommandResult(
            strategy=self.name,
            status="ok",
            validation=validation,
            stage_results=stage_results,
        )


def select_strategy(
    *,
    dry_run: bool,
    validate_only: bool,
) -> PipelineCommandStrategy:
    """Select a pipeline command strategy from CLI switches."""

    if dry_run and validate_only:
        raise ValueError("--dry-run and --validate-only are mutually exclusive")
    if dry_run:
        return DryRunStrategy()
    if validate_only:
        return ValidateOnlyStrategy()
    return RunStrategy()


def format_validation(result: ValidationResult) -> str:
    """Format validation issues for CLI output."""

    lines = [
        "validation status: error" if result.has_errors else "validation status: ok",
        "checked configs",
        "checked artifact paths",
        "checked feature semantics",
        "checked causal design",
        "checked adjustment set",
    ]
    for issue in result.issues:
        lines.append(
            f"- {issue.severity.value}: {issue.code}: {issue.message}"
            + (f" ({issue.location})" if issue.location else "")
        )
    if not any(issue.severity == ValidationSeverity.ERROR for issue in result.issues):
        lines.append("- errors: none")
    return "\n".join(lines)


__all__ = [
    "DryRunStrategy",
    "PipelineCommandResult",
    "PipelineCommandStrategy",
    "RunStrategy",
    "ValidateOnlyStrategy",
    "format_validation",
    "select_strategy",
]
