"""Real-PostgreSQL typed read reconstruction evidence for E4-G06 P04."""

from __future__ import annotations

import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from ariadne.adapters.local_artifact_store import LocalArtifactStore
from ariadne.product.application.execution_service import ExecutionService
from ariadne.product.application.predictive_workflow_service import PredictiveWorkflowService
from ariadne.product.application.product_closure_service import ProductClosureService
from ariadne.product.persistence.orm_models import (
    AnalysisViewOrm, ArtifactOrm, DatasetVersionOrm, ExecutionOrm, LineageEdgeOrm,
    ProjectMembershipOrm, ProjectOrm, ResultOrm,
)
from ariadne.product.persistence.unit_of_work import SqlUnitOfWork


def _id() -> str:
    return str(uuid.uuid4())


def _predictive_service(engine, tmp_path: Path) -> PredictiveWorkflowService:  # type: ignore[no-untyped-def]
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
def test_p04_reconstructs_canonical_predictive_lineage_without_structural_generic_rows(
    postgres_engine, tmp_path: Path,
) -> None:  # type: ignore[no-untyped-def]
    ids = {key: _id() for key in (
        "project", "membership", "source", "dataset", "view", "execution", "result", "artifact", "generic",
    )}
    now = datetime.now(timezone.utc)
    with Session(bind=postgres_engine) as session:
        session.add(ProjectOrm(project_id=ids["project"], name="G06 P04", status="ACTIVE", created_at=now, updated_at=now))
        session.flush()
        session.add(ProjectMembershipOrm(membership_id=ids["membership"], project_id=ids["project"], user_id="g06-p04", role="OWNER", created_at=now))
        session.add(ArtifactOrm(artifact_id=ids["source"], project_id=ids["project"], artifact_type="DATASET_FILE", object_key=f"g06/p04/{ids['source']}", content_hash="source", media_type="text/csv", size_bytes=1, metadata_json={}, created_at=now))
        session.flush()
        session.add(DatasetVersionOrm(dataset_version_id=ids["dataset"], project_id=ids["project"], source_artifact_id=ids["source"], dataset_key="g06-p04", name="G06 P04", version_label="v1", content_hash="source", schema_json={}, profile_summary_json={}, row_count=1, column_count=1, created_at=now))
        session.flush()
        session.add(AnalysisViewOrm(analysis_view_id=ids["view"], project_id=ids["project"], source_dataset_version_id=ids["dataset"], view_key="g06-p04", version_number=1, name="G06 P04", status="FIXED", schema_version="analysis-view/1", spec_json={}, content_hash="view", manifest_json={}, created_by="g06-p04", created_at=now, fixed_at=now))
        session.flush()
        session.add(ExecutionOrm(
            execution_id=ids["execution"], project_id=ids["project"], analysis_family="PREDICTIVE", dataset_version_id=ids["dataset"], input_graph_version_id=None, input_result_id=None, batch_key=_id(), operation="DISCOVERY", objective_snapshot=None, rationale_snapshot=None,
            analysis_spec_json={"analysis_view_id": ids["view"], "family_spec": {"schema_version": "predictive-analysis-spec/1"}}, algorithm_or_estimator="predictive", parameter_json={}, random_seed=1, code_version="g06-p04", runtime_version_json={}, snapshot_hash="p04", snapshot_schema_version="causal-analysis-spec/2", status="QUEUED", retry_count=0, last_error_summary=None, requested_by="g06-p04", requested_at=now, started_at=None, finished_at=None, base_execution_id=None, revision_kind=None, change_reason=None,
        ))
        session.flush()
        session.add(ResultOrm(result_id=ids["result"], execution_id=ids["execution"], result_level="EXECUTION_RESULT", stage_execution_id=None, result_type="DATA_PROFILE_RESULT", scientific_status="GENERATED", summary_json={}, payload_json={"schema_version": "profile/1"}, diagnostics_json={}, warning_json=[], created_at=now))
        session.flush()
        session.add(ArtifactOrm(artifact_id=ids["artifact"], project_id=ids["project"], execution_id=ids["execution"], stage_execution_id=None, result_id=ids["result"], artifact_scope="EXECUTION_OUTPUT", artifact_type="SCIENTIFIC_RESULT_JSON", object_key=f"g06/p04/{ids['artifact']}", content_hash="result", media_type="application/json", size_bytes=1, metadata_json={}, created_at=now))
        session.add(LineageEdgeOrm(lineage_edge_id=ids["generic"], project_id=ids["project"], source_type="Result", source_id=ids["result"], relation_type="MOTIVATED", target_type="Execution", target_id=ids["execution"], evidence_json={"why": "review"}, created_by="g06-p04", created_at=now))
        session.commit()

    with Session(bind=postgres_engine) as session:
        structural = list(session.scalars(select(LineageEdgeOrm).where(
            LineageEdgeOrm.target_id == ids["execution"],
            LineageEdgeOrm.relation_type == "USED_INPUT",
        )))
    assert structural == []

    closure = ProductClosureService(sessionmaker(bind=postgres_engine), LocalArtifactStore(tmp_path / "closure-objects"))
    graph = closure.project_lineage(ids["project"], user_id="g06-p04")
    keys = {(edge["source_type"], edge["source_id"], edge["relation_type"], edge["target_type"], edge["target_id"]) for edge in graph["edges"]}
    assert ("DatasetVersion", ids["dataset"], "USED_INPUT", "Execution", ids["execution"]) in keys
    assert ("AnalysisView", ids["view"], "USED_INPUT", "Execution", ids["execution"]) in keys
    assert ("Execution", ids["execution"], "GENERATED", "Result", ids["result"]) in keys
    assert ("Result", ids["result"], "GENERATED", "Artifact", ids["artifact"]) in keys
    assert ("Result", ids["result"], "MOTIVATED", "Execution", ids["execution"]) in keys

    predictive = _predictive_service(postgres_engine, tmp_path)
    lineage = predictive.list_lineage(ids["project"], ids["execution"])
    predictive_keys = {(edge["source_type"], edge["source_id"], edge["relation_type"], edge["target_type"], edge["target_id"]) for edge in lineage}
    assert keys & predictive_keys >= {
        ("DatasetVersion", ids["dataset"], "USED_INPUT", "Execution", ids["execution"]),
        ("AnalysisView", ids["view"], "USED_INPUT", "Execution", ids["execution"]),
        ("Execution", ids["execution"], "GENERATED", "Result", ids["result"]),
        ("Result", ids["result"], "GENERATED", "Artifact", ids["artifact"]),
        ("Result", ids["result"], "MOTIVATED", "Execution", ids["execution"]),
    }
