"""Final cross-surface authority audit for E4-G05 Phase C Predictive flow."""

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
from ariadne.product.domain.errors import EntityNotFound
from ariadne.product.persistence.orm_models import (
    ArtifactOrm, DatasetVersionOrm, ExecutionOrm, FamilyArtifactOrm, FamilyExecutionOrm,
    FamilyResultOrm, FamilyStageExecutionOrm, LineageEdgeOrm, ProjectOrm, ResultOrm,
    StageExecutionOrm,
)
from ariadne.product.persistence.unit_of_work import SqlUnitOfWork


def _id() -> str:
    return str(uuid.uuid4())


def _family_counts(session: Session) -> tuple[int, int, int, int]:
    return tuple(session.scalar(select(func.count()).select_from(model)) for model in (
        FamilyExecutionOrm, FamilyStageExecutionOrm, FamilyResultOrm, FamilyArtifactOrm,
    ))  # type: ignore[return-value]


def _service(engine, tmp_path: Path) -> PredictiveWorkflowService:  # type: ignore[no-untyped-def]
    factory = sessionmaker(bind=engine)

    @contextmanager
    def uow_factory() -> Iterator[SqlUnitOfWork]:
        session = factory()
        try:
            yield SqlUnitOfWork(session)
        finally:
            session.close()

    return PredictiveWorkflowService(factory, LocalArtifactStore(tmp_path / "objects"), execution_service=ExecutionService(uow_factory=uow_factory))


@pytest.mark.postgres
def test_g05_phase_c_predictive_cross_surface_authority_audit(postgres_engine, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    ids = {name: _id() for name in ("project", "other", "source", "dataset", "execution", "stage", "result", "artifact", "causal")}
    now = datetime.now(timezone.utc)
    with Session(bind=postgres_engine) as session:
        session.add_all((
            ProjectOrm(project_id=ids["project"], name="C4", status="ACTIVE", created_at=now, updated_at=now),
            ProjectOrm(project_id=ids["other"], name="other", status="ACTIVE", created_at=now, updated_at=now),
        )); session.flush()
        session.add(ArtifactOrm(artifact_id=ids["source"], project_id=ids["project"], artifact_type="DATASET_FILE", object_key=f"g05/c4/{ids['source']}", content_hash="source", media_type="text/csv", size_bytes=1, metadata_json={}, created_at=now)); session.flush()
        session.add(DatasetVersionOrm(dataset_version_id=ids["dataset"], project_id=ids["project"], source_artifact_id=ids["source"], dataset_key="c4", name="C4", version_label="v1", content_hash="source", schema_json={}, profile_summary_json={}, row_count=1, column_count=1, created_at=now)); session.flush()
        common = dict(project_id=ids["project"], dataset_version_id=ids["dataset"], batch_key=_id(), operation="DISCOVERY", algorithm_or_estimator="predictive-workflow", parameter_json={}, random_seed=17, code_version="g05", runtime_version_json={"family_snapshot": {"schema_version": "family-execution-snapshot/1"}}, snapshot_hash="c4", retry_count=0, requested_by="g05", requested_at=now)
        session.add_all((
            ExecutionOrm(execution_id=ids["execution"], analysis_family="PREDICTIVE", analysis_spec_json={"family_spec": {"schema_version": "predictive-analysis-spec/1"}, "analysis_specification_id": "spec-c4", "execution_plan_id": "plan-c4"}, status="QUEUED", **common),
            ExecutionOrm(execution_id=ids["causal"], analysis_family="CAUSAL", analysis_spec_json={}, status="QUEUED", **common),
        )); session.flush()
        session.add(StageExecutionOrm(stage_execution_id=ids["stage"], execution_id=ids["execution"], stage_key="split", stage_type_json={"namespace": "predictive", "name": "split", "version": "1"}, ordinal=0, dependencies_json=[], status="PENDING", input_binding_json={}, output_binding_json={}, created_at=now)); session.flush()
        session.add(ResultOrm(result_id=ids["result"], execution_id=ids["execution"], result_level="STAGE_RESULT", stage_execution_id=ids["stage"], result_type="SPLIT_RESULT", scientific_status="PASS", summary_json={"rows": 1}, payload_json={"schema_version": "partition/1"}, diagnostics_json={}, warning_json=[], created_at=now)); session.flush()
        session.add(ArtifactOrm(artifact_id=ids["artifact"], project_id=ids["project"], execution_id=ids["execution"], stage_execution_id=ids["stage"], result_id=ids["result"], artifact_scope="EXECUTION_OUTPUT", artifact_type="PARTITION_INDEX", object_key=f"g05/c4/out/{ids['artifact']}", content_hash="partition", media_type="application/json", size_bytes=1, metadata_json={"schema_version": "partition-artifact/1"}, created_at=now))
        session.add(LineageEdgeOrm(project_id=ids["project"], source_type="Execution", source_id=ids["execution"], relation_type="GENERATED", target_type="Result", target_id=ids["result"], evidence_json={}, created_by="g05", created_at=now))
        session.commit()

    service = _service(postgres_engine, tmp_path)
    with Session(bind=postgres_engine) as session:
        before = _family_counts(session)
    assert [item["execution_id"] for item in service.list_executions(ids["project"])] == [ids["execution"]]
    assert service.get_execution(ids["project"], ids["execution"])["analysis_family"] == "PREDICTIVE"
    assert service.get_stages(ids["project"], ids["execution"])[0]["stage_execution_id"] == ids["stage"]
    assert service.list_results(ids["project"], ids["execution"])[0]["result_type"] == "SPLIT_RESULT"
    assert service.list_artifacts(ids["project"], ids["execution"])[0]["artifact_type"] == "PARTITION_INDEX"
    assert service.list_lineage(ids["project"], ids["execution"])[0]["target_id"] == ids["result"]
    assert service.prefill(ids["project"], ids["execution"])["analysis_specification_id"] == "spec-c4"
    assert service.cancel(ids["project"], ids["execution"])["status"] == "CANCELLED"
    assert service.get_stages(ids["project"], ids["execution"])[0]["status"] == "CANCELLED"
    for operation in (service.get_execution, service.get_stages, service.list_results, service.list_artifacts, service.list_lineage, service.prefill):
        with pytest.raises(EntityNotFound):
            operation(ids["project"], _id())
    with pytest.raises(EntityNotFound):
        service.get_execution(ids["project"], ids["causal"])
    with pytest.raises(EntityNotFound):
        service.get_execution(ids["other"], ids["execution"])
    with Session(bind=postgres_engine) as session:
        assert _family_counts(session) == before
