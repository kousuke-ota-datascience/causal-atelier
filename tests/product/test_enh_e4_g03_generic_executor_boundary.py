from __future__ import annotations

import inspect
from pathlib import Path

import pytest

from ariadne.product.domain.enums import AnalysisFamily, StageExecutionStatus
from ariadne.product.domain.errors import InvalidExecutionPlan
from ariadne.product.domain.execution import Execution
from ariadne.product.domain.execution_plan import ExecutionPlan, StageDefinition, StageType
from ariadne.product.domain.stage_execution import StageExecution
from ariadne.product.workflow.executor import GenericExecutor
from ariadne.product.workflow.stage_materialization import StagePlanMaterializer


def _plan(family: AnalysisFamily) -> ExecutionPlan:
    return ExecutionPlan.build(
        project_id="project",
        analysis_specification_id="specification",
        analysis_family=family,
        planner_id=f"{family.value.lower()}.test",
        planner_version="1",
        stages=(StageDefinition("prepare", StageType("core", "prepare", "1")),),
    )


def test_g03_ac001_materializes_persistent_shape_for_all_canonical_families() -> None:
    for family in AnalysisFamily:
        execution = Execution(analysis_family=family)
        stages = StagePlanMaterializer.materialize(execution, _plan(family))
        assert len(stages) == 1
        assert stages[0].execution_id == execution.execution_id
        assert stages[0].status is StageExecutionStatus.PENDING


def test_g03_ac004_empty_or_mismatched_plan_is_rejected_before_persistence() -> None:
    execution = Execution(analysis_family=AnalysisFamily.CAUSAL)
    empty = ExecutionPlan.build(
        project_id="project", analysis_specification_id="specification",
        analysis_family=AnalysisFamily.CAUSAL, planner_id="test", planner_version="1",
    )
    with pytest.raises(InvalidExecutionPlan) as caught:
        StagePlanMaterializer.materialize(execution, empty)
    assert caught.value.code == "EMPTY_STAGE_PLAN"
    with pytest.raises(InvalidExecutionPlan) as caught:
        StagePlanMaterializer.materialize(execution, _plan(AnalysisFamily.PREDICTIVE))
    assert caught.value.code == "FAMILY_MISMATCH"


def test_g03_ac003_generic_executor_has_no_persistence_or_retry_authority() -> None:
    signature = inspect.signature(GenericExecutor.__init__)
    assert "commit" not in signature.parameters
    assert "retryable" not in signature.parameters
    source = Path(inspect.getsourcefile(GenericExecutor) or "").read_text(encoding="utf-8")
    assert "UnitOfWork" not in source
    assert "SqlAlchemy" not in source


def test_g03_stage_identity_and_attempt_history_are_append_preserving() -> None:
    stage = StageExecution(execution_id="execution", stage_key="prepare")
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc)
    stage.mark_ready()
    first = stage.start_attempt("worker", now)
    stage.fail({"message": "temporary"}, now)
    stage.start_attempt("worker", now)
    assert stage.stage_execution_id
    assert first.attempt_number == 1
    assert [attempt.attempt_number for attempt in stage.attempts] == [1, 2]
    assert stage.status is StageExecutionStatus.RUNNING


def test_g03_ac005_cancellation_is_explicit_and_terminal() -> None:
    from datetime import datetime, timezone

    stage = StageExecution(execution_id="execution", stage_key="prepare")
    stage.cancel(datetime.now(timezone.utc))
    assert stage.status is StageExecutionStatus.CANCELLED
