"""D2 PostgreSQL negative: absent canonical DI cannot write Family tables."""

from __future__ import annotations

from pathlib import Path
from typing import cast

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session, sessionmaker

from ariadne.adapters.local_artifact_store import LocalArtifactStore
from ariadne.product.application.exploratory_service import ExploratoryWorkspaceService
from ariadne.product.application.predictive_workflow_service import PredictiveWorkflowService
from ariadne.product.application.predictive_split_service import PredictiveSplitService
from ariadne.product.application.execution_service import ExecutionService
from ariadne.product.domain.errors import LegacyProductAuthorityDisabled
from ariadne.product.persistence.orm_models import (
    FamilyArtifactOrm,
    FamilyExecutionOrm,
    FamilyResultOrm,
    FamilyStageExecutionOrm,
)


def _counts(session: Session) -> tuple[int, int, int, int]:
    return tuple(session.scalar(select(func.count()).select_from(model)) for model in (
        FamilyExecutionOrm, FamilyStageExecutionOrm, FamilyResultOrm, FamilyArtifactOrm,
    ))  # type: ignore[return-value]


@pytest.mark.postgres
def test_g05_d2_missing_canonical_dependency_cannot_activate_legacy_lifecycle_write(
    postgres_engine, tmp_path: Path,
) -> None:  # type: ignore[no-untyped-def]
    factory = sessionmaker(bind=postgres_engine)
    store = LocalArtifactStore(tmp_path / "objects")
    exploratory = ExploratoryWorkspaceService(factory, store)
    predictive = PredictiveWorkflowService(factory, store)
    split = PredictiveSplitService(
        factory, store, execution_service=cast(ExecutionService, object()),
    )
    with Session(bind=postgres_engine) as session:
        before = _counts(session)

    for operation in (
        lambda: exploratory.submit_execution(
            "missing-project", dataset_version_id="missing-dataset",
            analysis_view_id=None, family_spec={},
        ),
        lambda: predictive.submit_execution(
            "missing-project", specification_id="missing-spec", plan_id="missing-plan",
            seed=1, requested_by="d2",
        ),
        lambda: predictive.cancel("missing-project", "historical-execution"),
        lambda: predictive.retry("missing-project", "historical-execution"),
        lambda: predictive.rerun("missing-project", "historical-execution", requested_by="d2"),
        lambda: predictive.revise(
            "missing-project", "historical-execution", specification_id="missing-spec",
            seed=1, change_reason="d2", requested_by="d2",
        ),
        lambda: split.validate_and_save(
            "missing-project", dataset_version_id="missing-dataset",
            analysis_view_id=None, family_spec={},
        ),
    ):
        with pytest.raises(LegacyProductAuthorityDisabled):
            operation()

    with Session(bind=postgres_engine) as session:
        assert _counts(session) == before
