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
from ariadne.interfaces.web_api.routers.exploration import _result
from ariadne.product.application.execution_service import ExecutionService
from ariadne.product.application.exploratory_service import ExploratoryWorkspaceService
from ariadne.product.domain.errors import EntityNotFound, InvalidSchema
from ariadne.product.persistence.orm_models import (
    ArtifactOrm,
    DatasetVersionOrm,
    ExecutionOrm,
    FamilyExecutionOrm,
    FamilyResultOrm,
    LineageEdgeOrm,
    ProjectOrm,
    ResultOrm,
    StageExecutionOrm,
)
from ariadne.product.persistence.unit_of_work import SqlUnitOfWork


def _id() -> str:
    return str(uuid.uuid4())


def _seed(engine) -> dict[str, str]:  # type: ignore[no-untyped-def]
    ids = {name: _id() for name in (
        "project", "other_project", "source", "dataset", "execution", "stage", "result",
        "causal_execution", "causal_stage", "causal_result",
    )}
    now = datetime.now(timezone.utc)
    with Session(bind=engine) as session:
        for project_id, name in ((ids["project"], "g05 exploratory"), (ids["other_project"], "other")):
            session.add(ProjectOrm(project_id=project_id, name=name, status="ACTIVE", created_at=now, updated_at=now))
        session.flush()
        session.add(ArtifactOrm(
            artifact_id=ids["source"], project_id=ids["project"], artifact_type="DATASET_FILE",
            object_key=f"g05/phase-b/{ids['source']}", content_hash="source-hash",
            media_type="text/csv", size_bytes=1, metadata_json={}, created_at=now,
        ))
        session.flush()
        session.add(DatasetVersionOrm(
            dataset_version_id=ids["dataset"], project_id=ids["project"], source_artifact_id=ids["source"],
            dataset_key="g05", name="G05", version_label="v1", content_hash="source-hash",
            schema_json={}, profile_summary_json={}, row_count=1, column_count=1, created_at=now,
        ))
        session.flush()
        session.add_all((
            ExecutionOrm(
                execution_id=ids["execution"], project_id=ids["project"], dataset_version_id=ids["dataset"],
                batch_key=_id(), operation="DISCOVERY", analysis_family="EXPLORATORY",
                analysis_spec_json={"analysis_view_id": "view-g05", "family_spec": {"operation": "PROFILE"}},
                algorithm_or_estimator="exploratory-workflow", parameter_json={}, code_version="g05",
                runtime_version_json={}, snapshot_hash="exploratory-hash", status="SUCCEEDED", retry_count=0,
                requested_by="g05", requested_at=now,
            ),
            ExecutionOrm(
                execution_id=ids["causal_execution"], project_id=ids["project"], dataset_version_id=ids["dataset"],
                batch_key=_id(), operation="DISCOVERY", analysis_family="CAUSAL", analysis_spec_json={},
                algorithm_or_estimator="causal", parameter_json={}, code_version="g05", runtime_version_json={},
                snapshot_hash="causal-hash", status="SUCCEEDED", retry_count=0, requested_by="g05", requested_at=now,
            ),
        ))
        session.flush()
        session.add_all((
            StageExecutionOrm(
                stage_execution_id=ids["stage"], execution_id=ids["execution"], stage_key="profile",
                stage_type_json={"capability": "exploratory", "name": "profile", "version": "1"}, ordinal=0,
                dependencies_json=[], status="SUCCEEDED", input_binding_json={}, output_binding_json={}, created_at=now,
            ),
            StageExecutionOrm(
                stage_execution_id=ids["causal_stage"], execution_id=ids["causal_execution"], stage_key="causal",
                stage_type_json={"capability": "causal", "name": "discovery", "version": "1"}, ordinal=0,
                dependencies_json=[], status="SUCCEEDED", input_binding_json={}, output_binding_json={}, created_at=now,
            ),
        ))
        session.flush()
        session.add_all((
            ResultOrm(
                result_id=ids["result"], execution_id=ids["execution"], result_level="STAGE_RESULT",
                stage_execution_id=ids["stage"], result_type="DATA_PROFILE_RESULT", scientific_status="GENERATED_WITH_WARNINGS",
                summary_json={"rows": 1},
                payload_json={"schema_version": "exploratory-profile/1", "profile": {"column": "value"}},
                diagnostics_json={"null_count": 0}, warning_json=[{"code": "SMALL_SAMPLE"}], created_at=now,
            ),
            ResultOrm(
                result_id=ids["causal_result"], execution_id=ids["causal_execution"], result_level="STAGE_RESULT",
                stage_execution_id=ids["causal_stage"], result_type="DIAGNOSTICS_RESULT", scientific_status="PASS",
                summary_json={}, payload_json={"schema_version": "causal/1"}, diagnostics_json={}, warning_json=[], created_at=now,
            ),
        ))
        session.commit()
    return ids


def _service(engine, tmp_path: Path) -> ExploratoryWorkspaceService:  # type: ignore[no-untyped-def]
    factory = sessionmaker(bind=engine)

    @contextmanager
    def uow_factory() -> Iterator[SqlUnitOfWork]:
        session = factory()
        try:
            yield SqlUnitOfWork(session)
        finally:
            session.close()

    return ExploratoryWorkspaceService(
        factory, LocalArtifactStore(tmp_path / "objects"),
        execution_service=ExecutionService(uow_factory=uow_factory),
    )


@pytest.mark.postgres
def test_g05_phase_b_exploratory_canonical_result_projection_and_draft(postgres_engine, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    ids = _seed(postgres_engine)
    service = _service(postgres_engine, tmp_path)
    with Session(bind=postgres_engine) as session:
        before = (
            session.scalar(select(func.count()).select_from(FamilyExecutionOrm)),
            session.scalar(select(func.count()).select_from(FamilyResultOrm)),
        )

    execution = service.get_execution(ids["project"], ids["execution"])
    assert execution.execution_id == ids["execution"]
    assert execution.analysis_family.value == "EXPLORATORY"
    assert [item.execution_id for item in service.list_executions(ids["project"])] == [ids["execution"]]

    listed = service.list_results(ids["project"])
    assert len(listed) == 1
    projected = listed[0]
    assert projected.result_id == ids["result"]
    assert projected.project_id == ids["project"]
    assert projected.execution_id == ids["execution"]
    assert projected.stage_execution_id == ids["stage"]
    assert projected.analysis_family == "EXPLORATORY"
    assert projected.result_type == "DATA_PROFILE_RESULT"
    assert projected.analytical_status == "GENERATED_WITH_WARNINGS"
    assert projected.schema_version == "exploratory-profile/1"
    assert projected.summary_json == {"rows": 1}
    assert projected.payload_json == {"schema_version": "exploratory-profile/1", "profile": {"column": "value"}}
    assert projected.diagnostics_json == {"null_count": 0}
    assert projected.warning_json == [{"code": "SMALL_SAMPLE"}]
    assert projected.created_at is not None

    # A fresh service/session must reconstruct the same canonical projection.
    fetched = _service(postgres_engine, tmp_path).get_result(ids["project"], ids["result"])
    assert fetched == projected
    response = _result(fetched)
    assert response.model_dump() == {
        "result_id": ids["result"], "project_id": ids["project"], "execution_id": ids["execution"],
        "stage_execution_id": ids["stage"], "analysis_family": "EXPLORATORY",
        "result_type": "DATA_PROFILE_RESULT", "schema_version": "exploratory-profile/1",
        "analytical_status": "GENERATED_WITH_WARNINGS", "summary": {"rows": 1},
        "payload": {"schema_version": "exploratory-profile/1", "profile": {"column": "value"}},
        "diagnostics": {"null_count": 0}, "warnings": [{"code": "SMALL_SAMPLE"}],
        "created_at": projected.created_at,
    }

    causal_draft = service.create_analysis_draft(ids["project"], ids["result"], "CAUSAL")
    predictive_draft = service.create_analysis_draft(ids["project"], ids["result"], "PREDICTIVE")
    for draft, target in ((causal_draft, "CAUSAL"), (predictive_draft, "PREDICTIVE")):
        assert draft["analysis_family"] == target
        assert draft["dataset_version_id"] == ids["dataset"]
        assert draft["analysis_view_id"] == "view-g05"
        assert draft["source_relation"]["source_result_id"] == ids["result"]
    with Session(bind=postgres_engine) as session:
        edges = list(session.scalars(select(LineageEdgeOrm).where(
            LineageEdgeOrm.source_id == ids["result"], LineageEdgeOrm.relation_type == "MOTIVATED",
        )))
        after = (
            session.scalar(select(func.count()).select_from(FamilyExecutionOrm)),
            session.scalar(select(func.count()).select_from(FamilyResultOrm)),
        )
    assert len(edges) == 2
    assert {edge.evidence_json["source_result_id"] for edge in edges} == {ids["result"]}
    assert after == before


@pytest.mark.postgres
def test_g05_phase_b_exploratory_projection_rejects_cross_project_non_exploratory_and_invalid_target(postgres_engine, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    ids = _seed(postgres_engine)
    service = _service(postgres_engine, tmp_path)
    with pytest.raises(EntityNotFound):
        service.get_result(ids["other_project"], ids["result"])
    with pytest.raises(EntityNotFound):
        service.get_result(ids["project"], ids["causal_result"])
    with pytest.raises(InvalidSchema):
        service.create_analysis_draft(ids["project"], ids["result"], "EXPLORATORY")
