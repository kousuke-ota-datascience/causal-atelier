from __future__ import annotations

from typing import Any

from ariadne.product.domain.errors import InvalidExecutionPlan
from ariadne.product.domain.execution_plan import ExecutionPlan, StageDefinition


class BindingResolver:
    def resolve(
        self,
        plan: ExecutionPlan,
        stage: StageDefinition,
        outputs_by_stage: dict[str, dict[str, Any]],
        external_inputs: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        inputs = dict(external_inputs or {})
        for binding in plan.dependencies:
            if binding.target_stage_key != stage.stage_key:
                continue
            try:
                value = outputs_by_stage[binding.source_stage_key][binding.source_output]
            except KeyError as exc:
                raise InvalidExecutionPlan(
                    "MISSING_RUNTIME_OUTPUT",
                    f"Output {binding.source_stage_key}.{binding.source_output} is unavailable",
                ) from exc
            inputs[binding.target_input] = value
        missing = sorted(set(stage.input_contract) - set(inputs))
        if missing:
            raise InvalidExecutionPlan(
                "MISSING_RUNTIME_INPUT", f"Required Stage inputs are unavailable: {missing}"
            )
        return inputs
