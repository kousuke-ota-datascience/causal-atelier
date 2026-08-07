from __future__ import annotations

from ariadne.product.domain.errors import DuplicateRegistration, RunnerNotRegistered
from ariadne.product.domain.execution_plan import StageType
from ariadne.product.workflow.contracts import StageRunner


class StageRunnerRegistry:
    def __init__(self) -> None:
        self._runners: dict[StageType, StageRunner] = {}

    @property
    def capability_fingerprint(self) -> tuple[str, ...]:
        return tuple(sorted(stage_type.key for stage_type in self._runners))

    def register(self, runner: StageRunner) -> None:
        if runner.stage_type in self._runners:
            raise DuplicateRegistration(f"Runner is already registered: {runner.stage_type.key}")
        self._runners[runner.stage_type] = runner

    def resolve(self, stage_type: StageType) -> StageRunner:
        try:
            return self._runners[stage_type]
        except KeyError as exc:
            raise RunnerNotRegistered(stage_type.key) from exc

    def contains(self, stage_type: StageType) -> bool:
        return stage_type in self._runners
