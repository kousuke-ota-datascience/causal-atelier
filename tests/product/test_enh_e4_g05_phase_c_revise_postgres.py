"""E4-G05 Phase C C3b – Predictive revise keeps canonical revision semantics."""

from __future__ import annotations

from copy import deepcopy
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
from ariadne.product.application.workspace_lifecycle_service import WorkspaceLifecycleService
from ariadne.product.domain.errors import (
    EntityNotFound,
    InvalidExecutionPlan,
    InvalidStateTransition,
    ScientificContractViolation,
)
from ariadne.product.persistence.orm_models import (
    ArtifactOrm,
    DatasetVersionOrm,
    ExecutionOrm,
    FamilyArtifactOrm,
    FamilyExecutionOrm,
    FamilyResultOrm,
    FamilyStageExecutionOrm,
    ProjectOrm,
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


def _services(engine, tmp_path: Path) -> tuple[PredictiveWorkflowService, WorkspaceLifecycleService]:  # type: ignore[no-untyped-def]
    factory = sessionmaker(bind=engine)

    @contextmanager
    def uow_factory() -> Iterator[SqlUnitOfWork]:
        session = factory()
        try:
            yield SqlUnitOfWork(session)
        finally:
            session.close()

    return (
        PredictiveWorkflowService(
            factory, LocalArtifactStore(tmp_path / "objects"),
            execution_service=ExecutionService(uow_factory=uow_factory),
        ),
        WorkspaceLifecycleService(factory),
    )


def _seed_project_and_dataset(engine) -> dict[str, str]:  # type: ignore[no-untyped-def]
    ids = {name: _id() for name in ("project", "other_project", "source", "dataset")}
    now = datetime.now(timezone.utc)
    with Session(bind=engine) as session:
        session.add_all((
            ProjectOrm(project_id=ids["project"], name="G05 C3b", status="ACTIVE", created_at=now, updated_at=now),
            ProjectOrm(project_id=ids["other_project"], name="other", status="ACTIVE", created_at=now, updated_at=now),
        ))
        session.flush()
        session.add(ArtifactOrm(
            artifact_id=ids["source"], project_id=ids["project"], artifact_type="DATASET_FILE",
            object_key=f"g05/c3b/{ids['source']}", content_hash="dataset-hash", media_type="text/csv",
            size_bytes=1, metadata_json={}, created_at=now,
        ))
        session.flush()
        session.add(DatasetVersionOrm(
            dataset_version_id=ids["dataset"], project_id=ids["project"], source_artifact_id=ids["source"],
            dataset_key="g05-c3b", name="G05 C3b", version_label="v1", content_hash="dataset-hash",
            schema_json={"columns": ["score", "converted", "customer_id"]}, profile_summary_json={},
            row_count=1, column_count=3, created_at=now,
        ))
        session.commit()
    return ids


def _fixed_specification(
    workspace: WorkspaceLifecycleService, ids: dict[str, str], family_spec: dict,
) -> str:
    context = workspace.create_research_context(ids["project"], {
        "context_key": "g05-c3b", "problem_statement": "predict conversion",
        "research_questions": ["Who converts?"],
    }, created_by="g05")
    workspace.fix_research_context(ids["project"], context["research_context_version_id"])
    specification = workspace.create_analysis_specification(ids["project"], {
        "specification_key": "g05-c3b", "analysis_family": "PREDICTIVE",
        "research_context_version_id": context["research_context_version_id"],
        "dataset_version_id": ids["dataset"], "analysis_view_id": None, "analysis_mode": "EXPLORATORY",
        "family_spec_schema_version": "predictive-analysis-spec/1", "family_spec": family_spec,
    }, created_by="g05")
    workspace.fix_analysis_specification(ids["project"], specification["analysis_specification_id"])
    return specification["analysis_specification_id"]


def _stage_semantics(rows: list[StageExecutionOrm]) -> list[tuple[object, ...]]:
    return [
        (row.stage_key, row.stage_type_json, row.dependencies_json, row.ordinal)
        for row in sorted(rows, key=lambda item: (item.ordinal, item.stage_key))
    ]


@pytest.mark.postgres
def test_g05_phase_c_predictive_revise_is_canonical_and_truthful(postgres_engine, tmp_path: Path, predictive_spec_factory) -> None:  # type: ignore[no-untyped-def]
    ids = _seed_project_and_dataset(postgres_engine)
    service, workspace = _services(postgres_engine, tmp_path)
    base_family_spec = predictive_spec_factory()
    base_specification_id = _fixed_specification(workspace, ids, base_family_spec)
    base_plan = service.create_plan(ids["project"], base_specification_id)
    base = service.submit_execution(
        ids["project"], specification_id=base_specification_id,
        plan_id=base_plan["execution_plan_id"], seed=17, requested_by="g05-base",
    )
    base_id = base["execution_id"]
    causal_id = _id()

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
        result = session.scalar(select(ResultOrm).where(ResultOrm.execution_id == base_id))
        assert result is not None
        session.add(ArtifactOrm(
            project_id=ids["project"], execution_id=base_id, stage_execution_id=base_stages[0].stage_execution_id,
            result_id=result.result_id, artifact_scope="EXECUTION_OUTPUT", artifact_type="FITTED_MODEL",
            object_key=f"g05/c3b/base/{_id()}", content_hash="base-model", media_type="application/json", size_bytes=1,
            metadata_json={"schema_version": "predictive-model/1"}, created_at=datetime.now(timezone.utc),
        ))
        session.add(ExecutionOrm(
            execution_id=causal_id, project_id=ids["project"], dataset_version_id=ids["dataset"],
            batch_key=_id(), operation="DISCOVERY", analysis_family="CAUSAL", analysis_spec_json={},
            algorithm_or_estimator="causal", parameter_json={}, code_version="g05", runtime_version_json={},
            snapshot_hash="causal-negative", status="SUCCEEDED", retry_count=0,
            requested_by="g05", requested_at=datetime.now(timezone.utc),
        ))
        session.commit()
        base_snapshot = {
            "status": base_row.status, "retry_count": base_row.retry_count,
            "stage_ids": {row.stage_execution_id for row in base_stages},
            "stage_semantics": _stage_semantics(base_stages),
            "result_ids": set(session.scalars(select(ResultOrm.result_id).where(ResultOrm.execution_id == base_id))),
            "artifact_ids": set(session.scalars(select(ArtifactOrm.artifact_id).where(ArtifactOrm.execution_id == base_id))),
            "dataset": base_row.dataset_version_id,
        }
        family_counts_before = _family_counts(session)

    revised_family_spec = deepcopy(base_family_spec)
    revised_family_spec["model_spec"] = {
        "model_id": "logistic_regression.v1", "parameters": {"l2": 0.25},
    }
    reason = "正則化強度を変更して予測安定性を検証するため"
    revised_specification = workspace.revise_analysis_specification(
        ids["project"], base_specification_id, changes={"family_spec": revised_family_spec},
        change_reason=reason, created_by="g05",
    )
    revised_specification_id = revised_specification["analysis_specification_id"]
    workspace.fix_analysis_specification(ids["project"], revised_specification_id)
    revised_plan = service.create_plan(ids["project"], revised_specification_id)
    revised = service.revise(
        ids["project"], base_id, specification_id=revised_specification_id, seed=17,
        change_reason=reason, requested_by="g05-revise",
    )

    assert revised["execution_id"] != base_id
    assert revised["analysis_family"] == "PREDICTIVE"
    assert revised["base_execution_id"] == base_id
    assert revised["revision_kind"] == "REVISED"

    with Session(bind=postgres_engine) as session:
        base_row = session.get(ExecutionOrm, base_id)
        revised_row = session.get(ExecutionOrm, revised["execution_id"])
        new_stages = list(session.scalars(select(StageExecutionOrm).where(
            StageExecutionOrm.execution_id == revised["execution_id"]
        )))
        assert base_row is not None and revised_row is not None and new_stages
        assert revised_row.change_reason == reason and revised_row.revision_kind == "REVISED"
        assert revised_row.dataset_version_id == base_snapshot["dataset"]
        assert revised_row.analysis_spec_json["analysis_specification_id"] == revised_specification_id
        assert revised_row.analysis_spec_json["family_spec"]["model_spec"] == {
            "model_id": "logistic_regression.v1", "parameters": {"l2": 0.25},
        }
        assert revised_row.analysis_spec_json["revision_context"]["revision_kind"] == "REVISED"
        assert revised_row.analysis_spec_json["revision_context"]["change_reason"] == reason
        assert {row.stage_execution_id for row in new_stages}.isdisjoint(base_snapshot["stage_ids"])
        assert [
            (row.stage_key, row.stage_type_json, row.ordinal)
            for row in sorted(new_stages, key=lambda row: row.ordinal)
        ] == [
            (stage["stage_key"], stage["stage_type"], ordinal)
            for ordinal, stage in enumerate(revised_plan["stages"])
        ]
        assert base_row.status == base_snapshot["status"] and base_row.retry_count == base_snapshot["retry_count"]
        assert {row.stage_execution_id for row in session.scalars(select(StageExecutionOrm).where(
            StageExecutionOrm.execution_id == base_id
        ))} == base_snapshot["stage_ids"]
        assert set(session.scalars(select(ResultOrm.result_id).where(ResultOrm.execution_id == base_id))) == base_snapshot["result_ids"]
        assert set(session.scalars(select(ArtifactOrm.artifact_id).where(ArtifactOrm.execution_id == base_id))) == base_snapshot["artifact_ids"]
        assert _family_counts(session) == family_counts_before

    prefill = service.prefill(ids["project"], revised["execution_id"])
    assert prefill["analysis_specification_id"] == revised_specification_id
    assert prefill["execution_plan_id"] == revised_plan["execution_plan_id"]
    assert prefill["seed"] == 17
    assert prefill["revision_context"] == {
        "base_execution_id": base_id, "kind": "REVISED", "change_reason": reason,
    }

    # Same conditions follow canonical comparison semantics: the resulting child is a RERUN, not a forged REVISED.
    same = service.revise(
        ids["project"], base_id, specification_id=base_specification_id, seed=17,
        change_reason="同条件での再実行を要求", requested_by="g05-same",
    )
    with Session(bind=postgres_engine) as session:
        same_row = session.get(ExecutionOrm, same["execution_id"])
        assert same_row is not None
        assert same_row.analysis_spec_json["revision_context"]["changed_dimensions"] == []
    assert same["revision_kind"] == "RERUN"

    for invalid_reason in (None, "", "   "):
        with pytest.raises(ScientificContractViolation):
            service.revise(  # type: ignore[arg-type]
                ids["project"], base_id, specification_id=revised_specification_id, seed=17,
                change_reason=invalid_reason, requested_by="g05-invalid",
            )
    with pytest.raises(EntityNotFound):
        service.revise(ids["other_project"], base_id, specification_id=revised_specification_id, seed=17, change_reason=reason, requested_by="g05")
    with pytest.raises(EntityNotFound):
        service.revise(ids["project"], _id(), specification_id=revised_specification_id, seed=17, change_reason=reason, requested_by="g05")
    with pytest.raises(EntityNotFound):
        service.revise(ids["project"], causal_id, specification_id=revised_specification_id, seed=17, change_reason=reason, requested_by="g05")
    with pytest.raises(InvalidStateTransition):
        service.revise(ids["project"], same["execution_id"], specification_id=revised_specification_id, seed=17, change_reason=reason, requested_by="g05")
    with pytest.raises(InvalidExecutionPlan):
        service.submit_execution(ids["project"], specification_id=revised_specification_id, plan_id=base_plan["execution_plan_id"], seed=17, requested_by="g05")
    with pytest.raises(InvalidExecutionPlan):
        service.revise(ids["project"], base_id, specification_id=revised_specification_id, seed=999, change_reason=reason, requested_by="g05")

    with Session(bind=postgres_engine) as session:
        assert _family_counts(session) == family_counts_before
