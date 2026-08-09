"""D1: retained family claim/process facades cannot be Product authorities."""

from __future__ import annotations

import inspect
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session, sessionmaker

from ariadne.adapters.local_artifact_store import LocalArtifactStore
from ariadne.interfaces.worker.execution_processor import ExecutionProcessor
from ariadne.interfaces.worker.runner import run_worker
from ariadne.product.application.exploratory_service import ExploratoryWorkspaceService
from ariadne.product.application.predictive_workflow_service import PredictiveWorkflowService
from ariadne.product.domain.errors import LegacyProductAuthorityDisabled
from ariadne.product.persistence.orm_models import (
    ArtifactOrm,
    DatasetVersionOrm,
    ExecutionOrm,
    ExecutionPlanOrm,
    FamilyArtifactOrm,
    FamilyExecutionOrm,
    FamilyResultOrm,
    FamilyStageExecutionOrm,
    ProjectOrm,
)
from ariadne.product.persistence.unit_of_work import SqlUnitOfWork


def _id() -> str:
    return str(uuid.uuid4())


def _family_snapshot(session: Session) -> tuple[tuple[int, int, int, int], tuple[tuple[str, str], ...]]:
    counts = tuple(session.scalar(select(func.count()).select_from(model)) for model in (
        FamilyExecutionOrm, FamilyStageExecutionOrm, FamilyResultOrm, FamilyArtifactOrm,
    ))
    states = tuple(session.execute(select(
        FamilyExecutionOrm.execution_id, FamilyExecutionOrm.status,
    ).order_by(FamilyExecutionOrm.execution_id)).all())
    return counts, states  # type: ignore[return-value]


def _seed(engine) -> dict[str, str]:  # type: ignore[no-untyped-def]
    ids = {name: _id() for name in (
        "project", "source", "dataset", "canonical", "explore_plan", "predict_plan",
        "explore_execution", "predict_execution", "explore_stage", "predict_stage",
        "explore_result", "predict_result", "explore_artifact", "predict_artifact",
    )}
    now = datetime.now(timezone.utc)
    with Session(bind=engine) as session:
        session.add(ProjectOrm(
            project_id=ids["project"], name="D1", status="ACTIVE",
            created_at=now, updated_at=now,
        ))
        session.flush()
        session.add(ArtifactOrm(
            artifact_id=ids["source"], project_id=ids["project"],
            artifact_type="DATASET_FILE", object_key=f"d1/{ids['source']}.csv",
            content_hash="source", media_type="text/csv", size_bytes=1,
            metadata_json={}, created_at=now,
        ))
        session.flush()
        session.add(DatasetVersionOrm(
            dataset_version_id=ids["dataset"], project_id=ids["project"],
            source_artifact_id=ids["source"], dataset_key="d1", name="D1",
            version_label="v1", content_hash="source", schema_json={},
            profile_summary_json={}, row_count=1, column_count=1, created_at=now,
        ))
        session.flush()
        for plan_id, family in ((ids["explore_plan"], "EXPLORATORY"), (ids["predict_plan"], "PREDICTIVE")):
            session.add(ExecutionPlanOrm(
                execution_plan_id=plan_id, project_id=ids["project"],
                analysis_specification_id=f"d1-{family}", analysis_family=family,
                plan_schema_version="execution-plan/1", planner_id="d1", planner_version="1",
                stages_json=[], dependencies_json=[], plan_hash=f"d1-{plan_id}", created_at=now,
            ))
        session.flush()
        for family, execution_key, plan_key, stage_key, result_key, artifact_key in (
            ("EXPLORATORY", "explore_execution", "explore_plan", "explore_stage", "explore_result", "explore_artifact"),
            ("PREDICTIVE", "predict_execution", "predict_plan", "predict_stage", "predict_result", "predict_artifact"),
        ):
            session.add(FamilyExecutionOrm(
                execution_id=ids[execution_key], project_id=ids["project"],
                dataset_version_id=ids["dataset"], execution_plan_id=ids[plan_key],
                analysis_family=family, specification_schema_version="legacy/1",
                specification_snapshot_json={}, snapshot_json={}, snapshot_hash=f"legacy-{family}",
                status="QUEUED", retry_count=0, requested_by="d1", requested_at=now,
            ))
            session.flush()
            session.add(FamilyStageExecutionOrm(
                stage_execution_id=ids[stage_key], execution_id=ids[execution_key],
                stage_key="legacy", stage_type_json={}, ordinal=0, status="PENDING",
                attempt_history_json=[], input_binding_json={}, output_binding_json={},
            ))
            session.flush()
            session.add(FamilyResultOrm(
                result_id=ids[result_key], project_id=ids["project"],
                execution_id=ids[execution_key], stage_execution_id=ids[stage_key],
                analysis_family=family, result_type="LEGACY", schema_version="legacy/1",
                analytical_status="PASS", summary_json={}, payload_json={}, diagnostics_json={},
                warning_json=[], created_at=now,
            ))
            session.flush()
            session.add(FamilyArtifactOrm(
                artifact_id=ids[artifact_key], project_id=ids["project"],
                execution_id=ids[execution_key], stage_execution_id=ids[stage_key],
                result_id=ids[result_key], family=family, artifact_type="LEGACY",
                schema_version="legacy/1", media_type="application/json",
                object_key=f"d1/{ids[artifact_key]}", content_hash="legacy", size_bytes=1,
                metadata_json={}, created_at=now,
            ))
            session.flush()
        session.add(ExecutionOrm(
            execution_id=ids["canonical"], project_id=ids["project"],
            dataset_version_id=ids["dataset"], batch_key=_id(), operation="DISCOVERY",
            analysis_family="CAUSAL", analysis_spec_json={}, algorithm_or_estimator="d1",
            parameter_json={}, random_seed=1, code_version="d1", runtime_version_json={},
            snapshot_hash="canonical-d1", status="QUEUED", retry_count=0,
            requested_by="d1", requested_at=now,
        ))
        session.commit()
    return ids


def _uow_factory(engine):  # type: ignore[no-untyped-def]
    factory = sessionmaker(bind=engine)

    @contextmanager
    def factory_context() -> Iterator[SqlUnitOfWork]:
        session = factory()
        try:
            yield SqlUnitOfWork(session)
        finally:
            session.close()

    return factory, factory_context


def test_g05_d1_worker_runner_has_only_canonical_claim_authority() -> None:
    source = inspect.getsource(run_worker)
    assert "uow.executions.claim_next" in source
    assert source.count(".claim_next(") == 1
    assert "ExploratoryWorkspaceService" not in source
    assert "PredictiveWorkflowService" not in source
    assert "ExecutionProcessor" in source


@pytest.mark.postgres
def test_g05_d1_legacy_claim_process_facades_reject_and_canonical_failure_does_not_fallback(
    postgres_engine, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:  # type: ignore[no-untyped-def]
    ids = _seed(postgres_engine)
    factory, uow_context = _uow_factory(postgres_engine)
    store = LocalArtifactStore(tmp_path / "objects")
    exploratory = ExploratoryWorkspaceService(factory, store)
    predictive = PredictiveWorkflowService(factory, store)
    with Session(bind=postgres_engine) as session:
        before = _family_snapshot(session)

    for operation in (
        lambda: exploratory.claim_next("d1-token", worker_id="d1-worker"),
        lambda: exploratory.process_execution(ids["explore_execution"], worker_token="d1-token"),
        lambda: predictive.claim_next("d1-token", worker_id="d1-worker"),
        lambda: predictive.process_execution(ids["predict_execution"], worker_token="d1-token"),
    ):
        with pytest.raises(LegacyProductAuthorityDisabled):
            operation()

    with uow_context() as uow:
        claimed = uow.executions.claim_next("d1-canonical-token", worker_id="d1-canonical-worker")
        uow.commit()
    assert claimed is not None and claimed.execution_id == ids["canonical"]
    processor = ExecutionProcessor(
        uow_context, object(), store, owner_token="d1-canonical-worker",
    )

    def controlled_failure(_execution) -> None:  # type: ignore[no-untyped-def]
        raise RuntimeError("D1 controlled canonical processing failure")

    monkeypatch.setattr(processor, "_execute", controlled_failure)
    processor.process(claimed)

    with Session(bind=postgres_engine) as session:
        assert session.get(ExecutionOrm, ids["canonical"]).status == "FAILED"
        assert _family_snapshot(session) == before
