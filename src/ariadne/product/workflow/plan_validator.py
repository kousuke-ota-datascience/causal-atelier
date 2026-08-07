from __future__ import annotations

from collections import defaultdict

from ariadne.product.domain.errors import InvalidExecutionPlan
from ariadne.product.domain.execution_plan import ExecutionPlan, PLAN_SCHEMA_VERSION
from ariadne.product.workflow.runner_registry import StageRunnerRegistry


class PlanValidator:
    def __init__(self, runners: StageRunnerRegistry, *, max_timeout_seconds: int = 86_400) -> None:
        self.runners = runners
        self.max_timeout_seconds = max_timeout_seconds

    def validate(self, plan: ExecutionPlan) -> tuple[str, ...]:
        if plan.plan_schema_version != PLAN_SCHEMA_VERSION:
            self._error("UNSUPPORTED_PLAN_SCHEMA", "Unsupported Execution Plan schema")
        if not plan.project_id or not plan.analysis_specification_id:
            self._error("MISSING_PLAN_REFERENCE", "Plan must reference Project and Specification")
        stages = {stage.stage_key: stage for stage in plan.stages}
        if len(stages) != len(plan.stages):
            self._error("DUPLICATE_STAGE_KEY", "Stage keys must be unique")
        if not stages:
            self._error("EMPTY_PLAN", "Execution Plan must contain at least one Stage")
        for stage in plan.stages:
            if stage.enabled and not self.runners.contains(stage.stage_type):
                self._error("RUNNER_NOT_REGISTERED", f"Runner is not registered: {stage.stage_type.key}")
            timeout = stage.resource_policy.get("timeout_seconds")
            if timeout is not None and (
                isinstance(timeout, bool) or not isinstance(timeout, int)
                or timeout < 1 or timeout > self.max_timeout_seconds
            ):
                self._error("RESOURCE_POLICY_EXCEEDED", f"Invalid timeout for {stage.stage_key}")

        indegree = {key: 0 for key in stages}
        outgoing: dict[str, list[str]] = defaultdict(list)
        bound_inputs: set[tuple[str, str]] = set()
        for edge in plan.dependencies:
            source = stages.get(edge.source_stage_key)
            target = stages.get(edge.target_stage_key)
            if source is None or target is None:
                self._error("MISSING_DEPENDENCY_NODE", "Dependency references an unknown Stage")
            assert source is not None and target is not None
            if not source.enabled and target.enabled:
                self._error("DISABLED_DEPENDENCY", "An enabled Stage depends on a disabled Stage")
            if edge.source_output not in source.output_contract:
                self._error("MISSING_OUTPUT", f"Unknown output {edge.source_output}")
            if edge.target_input not in target.input_contract:
                self._error("MISSING_INPUT", f"Unknown input {edge.target_input}")
            if source.output_contract[edge.source_output] != target.input_contract[edge.target_input]:
                self._error("SCHEMA_MISMATCH", "Dependency input/output schemas differ")
            binding_key = (edge.target_stage_key, edge.target_input)
            if binding_key in bound_inputs:
                self._error("DUPLICATE_BINDING", "A Stage input has multiple upstream bindings")
            bound_inputs.add(binding_key)
            outgoing[edge.source_stage_key].append(edge.target_stage_key)
            indegree[edge.target_stage_key] += 1

        ready = sorted(key for key, degree in indegree.items() if degree == 0)
        order: list[str] = []
        while ready:
            node = ready.pop(0)
            order.append(node)
            for target in sorted(outgoing[node]):
                indegree[target] -= 1
                if indegree[target] == 0:
                    ready.append(target)
                    ready.sort()
        if len(order) != len(stages):
            cycle_nodes = sorted(key for key, degree in indegree.items() if degree)
            self._error("PLAN_CYCLE", f"Execution Plan contains a cycle: {cycle_nodes}")
        return tuple(order)

    @staticmethod
    def _error(code: str, message: str) -> None:
        raise InvalidExecutionPlan(code, message)
