from __future__ import annotations

from datetime import datetime, timezone

from ariadne.interfaces.worker.execution_processor import _actual_failed_stage_error
from ariadne.product.domain.stage_execution import StageExecution
from ariadne.product.domain.execution_plan import StageType


def _stage(key: str, ordinal: int) -> StageExecution:
    return StageExecution(
        execution_id="execution-1",
        stage_key=key,
        ordinal=ordinal,
        stage_type=StageType("predictive", key, "1"),
    )


def test_terminal_error_uses_actual_failed_stage_not_skipped_downstream_stage() -> None:
    failed = _stage("train", 2)
    failed.mark_ready()
    failed.start_attempt("worker-1", datetime.now(timezone.utc))
    failed.fail(
        {"type": "ValueError", "message": "actual training failure", "code": "TRAIN_INVALID"},
        datetime.now(timezone.utc),
    )
    skipped = _stage("explain", 3)
    skipped.skip(datetime.now(timezone.utc))

    assert _actual_failed_stage_error((failed, skipped)) == {
        "type": "ValueError",
        "message": "actual training failure",
        "code": "TRAIN_INVALID",
    }
