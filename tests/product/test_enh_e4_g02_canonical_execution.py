from __future__ import annotations

from datetime import datetime, timezone

import pytest

from ariadne.product.domain.enums import AnalysisFamily, ExecutionStatus
from ariadne.product.domain.errors import InvalidStateTransition
from ariadne.product.domain.execution import Execution


def test_g02_001_one_execution_identity_contract_supports_all_families() -> None:
    executions = [
        Execution(analysis_family=family)
        for family in AnalysisFamily
    ]

    assert {execution.analysis_family for execution in executions} == set(AnalysisFamily)
    assert len({execution.execution_id for execution in executions}) == 3
    assert all(execution.status is ExecutionStatus.QUEUED for execution in executions)


def test_g02_002_common_state_machine_rejects_invalid_terminal_transition() -> None:
    execution = Execution(analysis_family=AnalysisFamily.PREDICTIVE)
    now = datetime.now(timezone.utc)

    execution.mark_running(now)
    execution.mark_succeeded(now)

    with pytest.raises(InvalidStateTransition):
        execution.mark_running(now)


def test_g02_003_retry_keeps_identity_and_distinguishes_occurrence() -> None:
    execution = Execution(analysis_family=AnalysisFamily.EXPLORATORY)
    execution.mark_running(datetime.now(timezone.utc))
    execution.mark_failed(datetime.now(timezone.utc), "temporary failure")
    execution_id = execution.execution_id

    execution.increment_retry()

    assert execution.execution_id == execution_id
    assert execution.retry_count == 1
    assert execution.status is ExecutionStatus.QUEUED


def test_g02_004_rerun_and_revise_use_new_typed_base_identity() -> None:
    base = Execution(analysis_family=AnalysisFamily.CAUSAL)
    rerun = Execution(
        analysis_family=base.analysis_family,
        base_execution_id=base.execution_id,
        revision_kind="RERUN",
    )
    revised = Execution(
        analysis_family=base.analysis_family,
        base_execution_id=base.execution_id,
        revision_kind="REVISED",
        change_reason="updated assumptions",
    )

    assert rerun.execution_id != base.execution_id
    assert revised.execution_id != base.execution_id
    assert rerun.base_execution_id == base.execution_id
    assert revised.base_execution_id == base.execution_id
    assert rerun.revision_kind != revised.revision_kind


def test_g02_005_lease_is_explicit_and_clearable() -> None:
    execution = Execution()
    expiry = datetime.now(timezone.utc)

    execution.set_lease("worker-a", expiry)
    assert execution.lease_owner == "worker-a"
    assert execution.lease_expires_at == expiry

    execution.clear_lease()
    assert execution.lease_owner is None
    assert execution.lease_expires_at is None
