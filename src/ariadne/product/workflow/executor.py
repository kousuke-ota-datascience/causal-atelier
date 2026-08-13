"""Family-neutral synchronous runner infrastructure used by workers and tests."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable

from ariadne.product.domain.execution_plan import ExecutionPlan
from ariadne.product.domain.stage_execution import StageExecution
from ariadne.product.workflow.bindings import BindingResolver
from ariadne.product.workflow.contracts import StageContext, StageRunResult
from ariadne.product.workflow.plan_validator import PlanValidator
from ariadne.product.workflow.runner_registry import StageRunnerRegistry


@dataclass(frozen=True)
class ExecutionOutcome:
    status: str
    stages: tuple[StageExecution, ...]
    results: tuple[Any, ...]
    artifacts: tuple[Any, ...]
    stage_results: tuple[tuple[str, StageRunResult], ...] = ()


class GenericExecutor:
    def __init__(
        self,
        runners: StageRunnerRegistry,
        *,
        clock: Callable[[], datetime] | None = None,
        compensate: Callable[[StageExecution, Exception], None] | None = None,
    ) -> None:
        self.runners = runners
        self.validator = PlanValidator(runners)
        self.bindings = BindingResolver()
        self.clock = clock or (lambda: datetime.now(timezone.utc))
        self.compensate = compensate or (lambda stage, error: None)

    def execute(
        self,
        execution_id: str,
        plan: ExecutionPlan,
        *,
        external_inputs: dict[str, dict[str, Any]] | None = None,
        snapshots: dict[str, Any] | None = None,
        worker_id: str = "local-worker",
        cancelled: Callable[[], bool] | None = None,
        stage_executions: tuple[StageExecution, ...] | None = None,
        effective_random_seed: int | None = None,
    ) -> ExecutionOutcome:
        order = self.validator.validate(plan)
        definitions = {item.stage_key: item for item in plan.stages}
        supplied = {stage.stage_key: stage for stage in (stage_executions or ())}
        executions = {
            key: StageExecution(
                execution_id=execution_id,
                stage_key=key,
                stage_type=definitions[key].stage_type,
                ordinal=index,
            )
            for index, key in enumerate(order)
        }
        for key, stage in supplied.items():
            if key not in executions:
                raise ValueError(f"Supplied StageExecution is not in the plan: {key}")
            executions[key] = stage
        outputs: dict[str, dict[str, Any]] = {}
        all_results: list[Any] = []
        all_artifacts: list[Any] = []
        stage_results: list[tuple[str, StageRunResult]] = []
        for key in order:
            stage = executions[key]
            definition = definitions[key]
            if not definition.enabled:
                stage.skip(self.clock())
                continue
            if cancelled is not None and cancelled():
                return ExecutionOutcome("CANCELLED", tuple(executions[k] for k in order), tuple(all_results), tuple(all_artifacts), tuple(stage_results))
            upstream = [edge.source_stage_key for edge in plan.dependencies if edge.target_stage_key == key]
            if any(executions[parent].status.value != "SUCCEEDED" for parent in upstream):
                stage.skip(self.clock())
                continue
            stage.mark_ready()
            stochastic = (
                definition.stage_type.namespace == "predictive"
                and definition.stage_type.name in {"split", "train"}
            )
            stage.start_attempt(
                worker_id, self.clock(),
                effective_random_seed=effective_random_seed if stochastic else None,
            )
            try:
                inputs = self.bindings.resolve(
                    plan, definition, outputs, (external_inputs or {}).get(key)
                )
                stage.input_binding = inputs
                context = StageContext(execution_id, definition, inputs, snapshots or {})
                runner = self.runners.resolve(definition.stage_type)
                runner.validate(context)
                result = runner.run(context)
                missing = sorted(set(definition.output_contract) - set(result.output_bindings))
                if missing:
                    raise ValueError(f"Runner omitted declared outputs: {missing}")
                outputs[key] = result.output_bindings
                all_results.extend(result.results)
                all_artifacts.extend(result.artifacts)
                stage_results.append((key, result))
                stage.succeed(result.output_bindings, self.clock())
            except Exception as exc:
                self.compensate(stage, exc)
                error = {"type": type(exc).__name__, "message": str(exc)}
                for attribute in ("code", "path"):
                    value = getattr(exc, attribute, None)
                    if value is not None:
                        error[attribute] = value
                stage.fail(error, self.clock())
                for remaining_key in order[order.index(key) + 1:]:
                    remaining = executions[remaining_key]
                    if remaining.status.value == "PENDING":
                        remaining.skip(self.clock())
                return ExecutionOutcome("FAILED", tuple(executions[k] for k in order), tuple(all_results), tuple(all_artifacts), tuple(stage_results))
        return ExecutionOutcome("SUCCEEDED", tuple(executions[k] for k in order), tuple(all_results), tuple(all_artifacts), tuple(stage_results))
