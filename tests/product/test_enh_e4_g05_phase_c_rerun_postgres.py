"""E4-G05 Phase C C3a – Predictive rerun uses canonical execution authority."""

from __future__ import annotations

import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
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
    AnalysisSpecificationOrm,
    ArtifactOrm,
    DatasetVersionOrm,
    ExecutionOrm,
    FamilyArtifactOrm,
    FamilyExecutionOrm,
    FamilyResultOrm,
    FamilyStageExecutionOrm,
    ProjectOrm,
    ResearchContextVersionOrm,
    ResultOrm,
    StageExecutionOrm,
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


def _seed_workspace(engine, family_spec: dict) -> dict[str, str]:  # type: ignore[no-untyped-def]
    ids = {name: _id() for name in (
        "project", "other_project", "source", "dataset", "context", "specification",
        "causal_execution", "queued_execution",
    )}
    now = datetime.now(timezone.utc)
    with Session(bind=engine) as session:
        session.add_all((
            ProjectOrm(project_id=ids["project"], name="G05 C3a", status="ACTIVE", created_at=now, updated_at=now),
            ProjectOrm(project_id=ids["other_project"], name="other", status="ACTIVE", created_at=now, updated_at=now),
        ))
        session.flush()
        session.add(ArtifactOrm(
            artifact_id=ids["source"], project_id=ids["project"], artifact_type="DATASET_FILE",
            object_key=f"g05/c3a/{ids['source']}", content_hash="dataset-hash", media_type="text/csv",
            size_bytes=1, metadata_json={}, created_at=now,
        ))
        session.flush()
        session.add(DatasetVersionOrm(
            dataset_version_id=ids["dataset"], project_id=ids["project"], source_artifact_id=ids["source"],
            dataset_key="g05-c3a", name="G05 C3a", version_label="v1", content_hash="dataset-hash",
            schema_json={"columns": ["score", "converted", "customer_id"]}, profile_summary_json={},
            row_count=1, column_count=3, created_at=now,
        ))
        session.flush()
        session.add(ResearchContextVersionOrm(
            research_context_version_id=ids["context"], project_id=ids["project"], context_key="g05-c3a",
            version_number=1, status="FIXED", schema_version="research-context/1", problem_statement="predict",
            research_questions_json=["Who converts?"], significance=None, hypotheses_json=[], decision_context_json={},
            relations_json=[], canonical_hash="context-hash", created_by="g05", created_at=now, fixed_at=now,
        ))
        session.flush()
        session.add(AnalysisSpecificationOrm(
            analysis_specification_id=ids["specification"], project_id=ids["project"], specification_key="g05-c3a",
            version_number=1, status="FIXED", schema_version="analysis-specification/1", analysis_family="PREDICTIVE",
            research_context_version_id=ids["context"], dataset_version_id=ids["dataset"], analysis_view_id=None,
            analysis_mode="EXPLORATORY", family_spec_schema_version="predictive-analysis-spec/1",
            family_spec_json=family_spec, revision_context_json=None, warnings_json=[], canonical_hash="spec-hash",
            created_by="g05", created_at=now, fixed_at=now,
        ))
        session.flush()
        shared = dict(
            project_id=ids["project"], dataset_version_id=ids["dataset"], batch_key=_id(), operation="DISCOVERY",
            analysis_spec_json={
                "family_spec": family_spec, "analysis_specification_id": ids["specification"],
                "execution_plan_id": "not-used-by-negative",
            }, algorithm_or_estimator="predictive-workflow", parameter_json={}, random_seed=17,
            code_version="g05", runtime_version_json={"family_snapshot": {}}, snapshot_hash="negative-hash",
            retry_count=0, requested_by="g05", requested_at=now,
        )
        session.add_all((
            ExecutionOrm(execution_id=ids["causal_execution"], analysis_family="CAUSAL", status="SUCCEEDED", **shared),
            ExecutionOrm(execution_id=ids["queued_execution"], analysis_family="PREDICTIVE", status="QUEUED", **shared),
        ))
        session.commit()
    return ids


def _stage_semantics(rows: list[StageExecutionOrm]) -> list[tuple[object, ...]]:
    return [
        (row.stage_key, row.stage_type_json, row.dependencies_json, row.ordinal)
        for row in sorted(rows, key=lambda item: (item.ordinal, item.stage_key))
    ]


@pytest.mark.postgres
def test_g05_phase_c_predictive_rerun_creates_new_canonical_execution(postgres_engine, tmp_path: Path, predictive_spec_factory) -> None:  # type: ignore[no-untyped-def]
    family_spec = predictive_spec_factory()
    ids = _seed_workspace(postgres_engine, family_spec)
    service = _service(postgres_engine, tmp_path)
    plan = service.create_plan(ids["project"], ids["specification"])
    base = service.submit_execution(
        ids["project"], specification_id=ids["specification"], plan_id=plan["execution_plan_id"],
        seed=17, requested_by="g05-base",
    )
    base_id = base["execution_id"]

    with Session(bind=postgres_engine) as session:
        base_row = session.get(ExecutionOrm, base_id)
        base_stages = list(session.scalars(select(StageExecutionOrm).where(StageExecutionOrm.execution_id == base_id)))
        assert base_row is not None and base_stages
        base_row.status = "SUCCEEDED"
        for stage in base_stages:
            stage.status = "SUCCEEDED"
        session.add(ResultOrm(
            execution_id=base_id, result_level="STAGE_RESULT", stage_execution_id=base_stages[0].stage_execution_id,
            result_type="EVALUATION_RESULT", scientific_status="EVALUATED", summary_json={"auc": 0.7},
            payload_json={"schema_version": "predictive-evaluation/1"}, diagnostics_json={}, warning_json=[], created_at=datetime.now(timezone.utc),
        ))
        session.flush()
        base_result = session.scalar(select(ResultOrm).where(ResultOrm.execution_id == base_id))
        assert base_result is not None
        session.add(ArtifactOrm(
            project_id=ids["project"], execution_id=base_id, stage_execution_id=base_stages[0].stage_execution_id,
            result_id=base_result.result_id, artifact_scope="EXECUTION_OUTPUT", artifact_type="FITTED_MODEL",
            object_key=f"g05/c3a/base/{_id()}", content_hash="base-model", media_type="application/json", size_bytes=1,
            metadata_json={"schema_version": "predictive-model/1"}, created_at=datetime.now(timezone.utc),
        ))
        session.commit()
        base_snapshot = {
            "status": base_row.status, "retry_count": base_row.retry_count,
            "stage_ids": {row.stage_execution_id for row in base_stages},
            "result_ids": set(session.scalars(select(ResultOrm.result_id).where(ResultOrm.execution_id == base_id))),
            "artifact_ids": set(session.scalars(select(ArtifactOrm.artifact_id).where(ArtifactOrm.execution_id == base_id))),
            "analysis_spec": base_row.analysis_spec_json, "runtime": base_row.runtime_version_json,
            "parameters": base_row.parameter_json, "estimator": base_row.algorithm_or_estimator,
            "seed": base_row.random_seed, "dataset": base_row.dataset_version_id,
            "stage_semantics": _stage_semantics(base_stages),
        }
        family_counts_before = _family_counts(session)

    rerun = service.rerun(ids["project"], base_id, requested_by="g05-rerun")
    assert rerun["execution_id"] != base_id
    assert rerun["analysis_family"] == "PREDICTIVE"
    assert rerun["base_execution_id"] == base_id
    assert rerun["revision_kind"] == "RERUN"

    with Session(bind=postgres_engine) as session:
        base_row = session.get(ExecutionOrm, base_id)
        rerun_row = session.get(ExecutionOrm, rerun["execution_id"])
        new_stages = list(session.scalars(select(StageExecutionOrm).where(
            StageExecutionOrm.execution_id == rerun["execution_id"]
        )))
        assert base_row is not None and rerun_row is not None and new_stages
        assert rerun_row.change_reason is None and rerun_row.revision_kind == "RERUN"
        assert rerun_row.dataset_version_id == base_snapshot["dataset"]
        assert {
            key: value for key, value in rerun_row.analysis_spec_json.items()
            if key != "revision_context"
        } == base_snapshot["analysis_spec"]
        assert rerun_row.analysis_spec_json["revision_context"] == {
            "base_execution_id": base_id,
            "base_snapshot_hash": base_row.snapshot_hash,
            "revision_kind": "RERUN",
            "change_reason": None,
            "changed_dimensions": [],
        }
        assert rerun_row.runtime_version_json == base_snapshot["runtime"]
        assert rerun_row.parameter_json == base_snapshot["parameters"]
        assert rerun_row.algorithm_or_estimator == base_snapshot["estimator"]
        assert rerun_row.random_seed == base_snapshot["seed"]
        assert {row.stage_execution_id for row in new_stages}.isdisjoint(base_snapshot["stage_ids"])
        assert _stage_semantics(new_stages) == base_snapshot["stage_semantics"]
        assert base_row.status == base_snapshot["status"] and base_row.retry_count == base_snapshot["retry_count"]
        assert {row.stage_execution_id for row in session.scalars(select(StageExecutionOrm).where(
            StageExecutionOrm.execution_id == base_id
        ))} == base_snapshot["stage_ids"]
        assert set(session.scalars(select(ResultOrm.result_id).where(ResultOrm.execution_id == base_id))) == base_snapshot["result_ids"]
        assert set(session.scalars(select(ArtifactOrm.artifact_id).where(ArtifactOrm.execution_id == base_id))) == base_snapshot["artifact_ids"]
        assert _family_counts(session) == family_counts_before

    with pytest.raises(EntityNotFound):
        service.rerun(ids["other_project"], base_id, requested_by="g05")
    with pytest.raises(EntityNotFound):
        service.rerun(ids["project"], ids["causal_execution"], requested_by="g05")
    with pytest.raises(EntityNotFound):
        service.rerun(ids["project"], _id(), requested_by="g05")
    with pytest.raises(InvalidStateTransition):
        service.rerun(ids["project"], ids["queued_execution"], requested_by="g05")

    with Session(bind=postgres_engine) as session:
        assert _family_counts(session) == family_counts_before
