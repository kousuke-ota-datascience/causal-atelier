"""E4-G05 Phase C C2 – Predictive retry stays on canonical lifecycle authority."""

from __future__ import annotations

import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterator

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session, sessionmaker

from ariadne.adapters.local_artifact_store import LocalArtifactStore
from ariadne.product.application.execution_service import ExecutionService
from ariadne.product.application.predictive_workflow_service import PredictiveWorkflowService
from ariadne.product.domain.errors import EntityNotFound, InvalidStateTransition
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
    ResultOrm,
    StageAttemptOrm,
    StageExecutionOrm,
)
from ariadne.product.persistence.repositories import (
    SqlExecutionRepository,
    SqlStageExecutionRepository,
)
from ariadne.product.persistence.unit_of_work import SqlUnitOfWork


def _id() -> str:
    return str(uuid.uuid4())


def _family_counts(session: Session) -> tuple[int, int, int, int]:
    return tuple(
        session.scalar(select(func.count()).select_from(model))
        for model in (
            FamilyExecutionOrm, FamilyStageExecutionOrm, FamilyResultOrm, FamilyArtifactOrm,
        )
    )  # type: ignore[return-value]


def _seed(engine) -> dict[str, str]:  # type: ignore[no-untyped-def]
    ids = {name: _id() for name in (
        "project", "other_project", "source", "dataset", "execution", "failed_stage",
        "result", "artifact", "causal_execution", "queued_execution", "legacy_plan",
        "legacy_execution", "legacy_stage", "legacy_result", "legacy_artifact",
    )}
    now = datetime.now(timezone.utc)
    predictive_spec = {
        "family_spec": {"schema_version": "predictive-analysis-spec/1", "target": "outcome"},
        "analysis_specification_id": "predictive-spec-c2",
        "execution_plan_id": "predictive-plan-c2",
    }
    predictive_snapshot = {
        "schema_version": "predictive-execution-snapshot/1",
        "execution_plan": {"id": "predictive-plan-c2", "hash": "plan-hash"},
        "seed": 719,
    }
    with Session(bind=engine) as session:
        session.add_all((
            ProjectOrm(project_id=ids["project"], name="G05 C2", status="ACTIVE", created_at=now, updated_at=now),
            ProjectOrm(project_id=ids["other_project"], name="other", status="ACTIVE", created_at=now, updated_at=now),
        ))
        session.flush()
        session.add(ArtifactOrm(
            artifact_id=ids["source"], project_id=ids["project"], artifact_type="DATASET_FILE",
            object_key=f"g05/c2/{ids['source']}", content_hash="source-hash", media_type="text/csv",
            size_bytes=1, metadata_json={}, created_at=now,
        ))
        session.add(DatasetVersionOrm(
            dataset_version_id=ids["dataset"], project_id=ids["project"], source_artifact_id=ids["source"],
            dataset_key="g05-c2", name="G05 C2", version_label="v1", content_hash="source-hash",
            schema_json={}, profile_summary_json={}, row_count=1, column_count=1, created_at=now,
        ))
        session.flush()
        session.add_all((
            ExecutionOrm(
                execution_id=ids["execution"], project_id=ids["project"], dataset_version_id=ids["dataset"],
                batch_key=_id(), operation="DISCOVERY", analysis_family="PREDICTIVE",
                analysis_spec_json=predictive_spec, algorithm_or_estimator="logistic_regression.v1",
                parameter_json={"C": 1.0}, random_seed=719, code_version="g05-c2",
                runtime_version_json={"family_snapshot": predictive_snapshot}, snapshot_hash="predictive-hash",
                status="FAILED", retry_count=2, last_error_summary="transient training failure",
                requested_by="g05", requested_at=now, started_at=now, finished_at=now,
            ),
            ExecutionOrm(
                execution_id=ids["causal_execution"], project_id=ids["project"], dataset_version_id=ids["dataset"],
                batch_key=_id(), operation="DISCOVERY", analysis_family="CAUSAL", analysis_spec_json={},
                algorithm_or_estimator="causal", parameter_json={}, code_version="g05-c2", runtime_version_json={},
                snapshot_hash="causal-hash", status="FAILED", retry_count=0, requested_by="g05", requested_at=now,
            ),
            ExecutionOrm(
                execution_id=ids["queued_execution"], project_id=ids["project"], dataset_version_id=ids["dataset"],
                batch_key=_id(), operation="DISCOVERY", analysis_family="PREDICTIVE", analysis_spec_json=predictive_spec,
                algorithm_or_estimator="logistic_regression.v1", parameter_json={}, random_seed=719,
                code_version="g05-c2", runtime_version_json={"family_snapshot": predictive_snapshot},
                snapshot_hash="completed-hash", status="SUCCEEDED", retry_count=0, requested_by="g05", requested_at=now,
            ),
        ))
        session.flush()
        session.add(StageExecutionOrm(
            stage_execution_id=ids["failed_stage"], execution_id=ids["execution"], stage_key="training",
            stage_type_json={"namespace": "predictive", "name": "training", "version": "1"}, ordinal=0,
            dependencies_json=[], status="FAILED", input_binding_json={"split": "stable"}, output_binding_json={},
            last_error_json={"code": "TRANSIENT"}, created_at=now, started_at=now, finished_at=now,
        ))
        session.flush()
        session.add(StageAttemptOrm(
            stage_execution_id=ids["failed_stage"], attempt_number=1, worker_id="initial-worker",
            started_at=now, finished_at=now, error_json={"code": "TRANSIENT"},
        ))
        session.flush()
        session.add(ResultOrm(
            result_id=ids["result"], execution_id=ids["execution"], result_level="STAGE_RESULT",
            stage_execution_id=ids["failed_stage"], result_type="TRAINING_RESULT", scientific_status="TRAINED_WITH_WARNINGS",
            summary_json={"iterations": 5}, payload_json={"schema_version": "predictive-training/1", "metric": 0.7},
            diagnostics_json={"converged": False}, warning_json=[{"code": "EARLY_STOP"}], created_at=now,
        ))
        session.flush()
        session.add(ArtifactOrm(
            artifact_id=ids["artifact"], project_id=ids["project"], execution_id=ids["execution"],
            stage_execution_id=ids["failed_stage"], result_id=ids["result"], artifact_scope="EXECUTION_OUTPUT",
            artifact_type="FITTED_MODEL", object_key=f"g05/c2/model/{ids['artifact']}", content_hash="model-hash",
            media_type="application/json", size_bytes=3, metadata_json={"schema_version": "predictive-model/1"}, created_at=now,
        ))

        # A legacy sentinel proves that canonical retry neither creates nor deletes old-family rows.
        session.add(ExecutionPlanOrm(
            execution_plan_id=ids["legacy_plan"], project_id=ids["project"], analysis_specification_id="legacy-spec",
            analysis_family="PREDICTIVE", plan_schema_version="predictive-plan/1", planner_id="g05", planner_version="1",
            stages_json=[], dependencies_json=[], plan_hash="a" * 64, created_at=now,
        ))
        session.flush()
        session.add(FamilyExecutionOrm(
            execution_id=ids["legacy_execution"], project_id=ids["project"], dataset_version_id=ids["dataset"],
            execution_plan_id=ids["legacy_plan"], analysis_family="PREDICTIVE",
            specification_schema_version="predictive-analysis-spec/1", specification_snapshot_json={}, snapshot_json={},
            snapshot_hash="b" * 64, status="FAILED", retry_count=4, requested_by="legacy", requested_at=now,
        ))
        session.flush()
        session.add(FamilyStageExecutionOrm(
            stage_execution_id=ids["legacy_stage"], execution_id=ids["legacy_execution"], stage_key="legacy",
            stage_type_json={}, ordinal=0, status="FAILED", attempt_history_json=[{"attempt_number": 1}],
            input_binding_json={}, output_binding_json={}, last_error_json={"code": "OLD"}, started_at=now, finished_at=now,
        ))
        session.flush()
        session.add(FamilyResultOrm(
            result_id=ids["legacy_result"], project_id=ids["project"], execution_id=ids["legacy_execution"],
            stage_execution_id=ids["legacy_stage"], analysis_family="PREDICTIVE", result_type="TRAINING_RESULT",
            schema_version="predictive-training/1", analytical_status="TRAINED", summary_json={}, payload_json={},
            diagnostics_json={}, warning_json=[], created_at=now,
        ))
        session.flush()
        session.add(FamilyArtifactOrm(
            artifact_id=ids["legacy_artifact"], project_id=ids["project"], execution_id=ids["legacy_execution"],
            stage_execution_id=ids["legacy_stage"], result_id=ids["legacy_result"], family="PREDICTIVE",
            artifact_type="FITTED_MODEL", schema_version="predictive-model/1", media_type="application/json",
            object_key=f"g05/c2/legacy/{ids['legacy_artifact']}", content_hash="legacy-hash", size_bytes=1,
            metadata_json={}, created_at=now,
        ))
        session.commit()
    return ids


def _service(engine, tmp_path: Path) -> PredictiveWorkflowService:  # type: ignore[no-untyped-def]
    factory = sessionmaker(bind=engine)

    @contextmanager
    def uow_factory() -> Iterator[SqlUnitOfWork]:
        session = factory()
        try:
            yield SqlUnitOfWork(session)
        finally:
            session.close()

    return PredictiveWorkflowService(
        factory, LocalArtifactStore(tmp_path / "objects"),
        execution_service=ExecutionService(uow_factory=uow_factory),
    )


@pytest.mark.postgres
def test_g05_phase_c_predictive_retry_is_canonical_and_append_preserving(postgres_engine, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    ids = _seed(postgres_engine)
    service = _service(postgres_engine, tmp_path)
    with Session(bind=postgres_engine) as session:
        family_counts_before = _family_counts(session)

    retried = service.retry(ids["project"], ids["execution"])
    assert retried["execution_id"] == ids["execution"]
    assert retried["analysis_family"] == "PREDICTIVE"
    assert retried["status"] == "QUEUED"
    assert retried["retry_count"] == 3
    assert retried["specification_snapshot"] == {
        "schema_version": "predictive-analysis-spec/1", "target": "outcome",
    }
    assert retried["snapshot"] == {
        "schema_version": "predictive-execution-snapshot/1",
        "execution_plan": {"id": "predictive-plan-c2", "hash": "plan-hash"}, "seed": 719,
    }

    # Fresh session: no legacy reset/delete and no canonical ownership rewrite happened.
    with Session(bind=postgres_engine) as session:
        execution = session.get(ExecutionOrm, ids["execution"])
        stages = list(session.scalars(select(StageExecutionOrm).where(
            StageExecutionOrm.execution_id == ids["execution"]
        )))
        result = session.get(ResultOrm, ids["result"])
        artifact = session.get(ArtifactOrm, ids["artifact"])
        assert execution is not None and execution.execution_id == ids["execution"]
        assert execution.analysis_family == "PREDICTIVE" and execution.random_seed == 719
        assert execution.analysis_spec_json["execution_plan_id"] == "predictive-plan-c2"
        assert len(stages) == 1 and stages[0].stage_execution_id == ids["failed_stage"]
        assert stages[0].status == "PENDING"
        assert result is not None and result.execution_id == ids["execution"]
        assert artifact is not None and artifact.execution_id == ids["execution"] and artifact.result_id == ids["result"]
        assert _family_counts(session) == family_counts_before

    # G03-compatible claim and second attempt append to the same persistent StageExecution.
    now = datetime.now(timezone.utc)
    with Session(bind=postgres_engine) as session:
        # R1 diagnostic contract: global claim_next is FIFO over eligible
        # canonical rows.  This fixture must therefore expose exactly the
        # retried target before asserting the following claim.
        candidates = list(session.execute(
            select(
                ExecutionOrm.execution_id, ExecutionOrm.project_id,
                ExecutionOrm.analysis_family, ExecutionOrm.status,
                ExecutionOrm.requested_at, ExecutionOrm.retry_count,
                ExecutionOrm.lease_owner, ExecutionOrm.lease_expires_at,
                ExecutionOrm.base_execution_id, ExecutionOrm.revision_kind,
            ).where(
                (ExecutionOrm.status == "QUEUED")
                | ((ExecutionOrm.status == "RUNNING") & (ExecutionOrm.lease_expires_at <= now))
            ).order_by(ExecutionOrm.requested_at, ExecutionOrm.execution_id)
        ))
        assert [row.execution_id for row in candidates] == [ids["execution"]]
        executions = SqlExecutionRepository(session)
        stages = SqlStageExecutionRepository(session)
        claimed = executions.claim_next("c2-retry-token", worker_id="c2-retry-worker")
        assert claimed is not None and claimed.execution_id == ids["execution"]
        session.commit()
        stage = stages.get(ids["failed_stage"])
        assert stage is not None and [attempt.attempt_number for attempt in stage.attempts] == [1]
        assert stage.attempts[0].error == {"code": "TRANSIENT"}
        stage.mark_ready()
        stages.update(stage, owner="c2-retry-worker")
        stages.start_attempt(stage, owner="c2-retry-worker", worker_id="c2-retry-worker", at=now)
        stage.succeed({"model": ids["artifact"]}, now + timedelta(seconds=1))
        stages.update(stage, owner="c2-retry-worker")
        session.commit()

    with Session(bind=postgres_engine) as session:
        stage = SqlStageExecutionRepository(session).get(ids["failed_stage"])
        assert stage is not None and stage.stage_execution_id == ids["failed_stage"]
        assert [attempt.attempt_number for attempt in stage.attempts] == [1, 2]
        assert stage.attempts[0].error == {"code": "TRANSIENT"}
        assert stage.attempts[1].error is None
        assert _family_counts(session) == family_counts_before

    with pytest.raises(EntityNotFound):
        service.retry(ids["other_project"], ids["execution"])
    with pytest.raises(EntityNotFound):
        service.retry(ids["project"], ids["causal_execution"])
    with pytest.raises(InvalidStateTransition):
        service.retry(ids["project"], ids["queued_execution"])
    with pytest.raises(EntityNotFound):
        service.retry(ids["project"], _id())
