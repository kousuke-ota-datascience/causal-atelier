"""Real-PostgreSQL projection-authority evidence for E4-G06 P05."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session, sessionmaker

from ariadne.adapters.local_artifact_store import LocalArtifactStore
from ariadne.product.application.product_closure_service import ProductClosureService
from ariadne.product.persistence.orm_models import (
    AnalysisViewOrm, ArtifactOrm, DatasetVersionOrm, ExecutionOrm, LineageEdgeOrm,
    ProjectMembershipOrm, ProjectOrm, ResultOrm,
)


def _id() -> str:
    return str(uuid.uuid4())


@pytest.mark.postgres
def test_p05_authority_source_classes_survive_closure_and_export(
    postgres_engine, tmp_path: Path,
) -> None:  # type: ignore[no-untyped-def]
    ids = {name: _id() for name in (
        "project", "membership", "source", "dataset", "view", "execution", "result", "artifact", "generic",
    )}
    now = datetime.now(timezone.utc)
    with Session(bind=postgres_engine) as session:
        session.add(ProjectOrm(project_id=ids["project"], name="G06 P05", status="ACTIVE", created_at=now, updated_at=now)); session.flush()
        session.add(ProjectMembershipOrm(membership_id=ids["membership"], project_id=ids["project"], user_id="g06-p05", role="OWNER", created_at=now))
        session.add(ArtifactOrm(artifact_id=ids["source"], project_id=ids["project"], artifact_type="DATASET_FILE", object_key=f"g06/p05/{ids['source']}", content_hash="source", media_type="text/csv", size_bytes=1, metadata_json={}, created_at=now)); session.flush()
        session.add(DatasetVersionOrm(dataset_version_id=ids["dataset"], project_id=ids["project"], source_artifact_id=ids["source"], dataset_key="g06-p05", name="G06 P05", version_label="v1", content_hash="source", schema_json={}, profile_summary_json={}, row_count=1, column_count=1, created_at=now)); session.flush()
        session.add(AnalysisViewOrm(analysis_view_id=ids["view"], project_id=ids["project"], source_dataset_version_id=ids["dataset"], view_key="g06-p05", version_number=1, name="G06 P05", status="FIXED", schema_version="analysis-view/1", spec_json={}, content_hash="view", manifest_json={}, created_by="g06-p05", created_at=now, fixed_at=now)); session.flush()
        session.add(ExecutionOrm(execution_id=ids["execution"], project_id=ids["project"], analysis_family="PREDICTIVE", dataset_version_id=ids["dataset"], input_graph_version_id=None, input_result_id=None, batch_key=_id(), operation="DISCOVERY", objective_snapshot=None, rationale_snapshot=None, analysis_spec_json={"analysis_view_id": ids["view"], "analysis_specification_id": "snapshot-only-spec", "execution_plan_id": "snapshot-only-plan", "family_spec": {"schema_version": "predictive-analysis-spec/1"}}, algorithm_or_estimator="predictive", parameter_json={}, random_seed=1, code_version="g06-p05", runtime_version_json={"family_snapshot": {"research_context": {"id": "snapshot-only-context"}}}, snapshot_hash="p05", snapshot_schema_version="causal-analysis-spec/2", status="QUEUED", retry_count=0, last_error_summary=None, requested_by="g06-p05", requested_at=now, started_at=None, finished_at=None, base_execution_id=None, revision_kind=None, change_reason=None)); session.flush()
        session.add(ResultOrm(result_id=ids["result"], execution_id=ids["execution"], result_level="EXECUTION_RESULT", stage_execution_id=None, result_type="DATA_PROFILE_RESULT", scientific_status="GENERATED", summary_json={}, payload_json={"schema_version": "profile/1"}, diagnostics_json={}, warning_json=[], created_at=now)); session.flush()
        session.add(ArtifactOrm(artifact_id=ids["artifact"], project_id=ids["project"], execution_id=ids["execution"], stage_execution_id=None, result_id=ids["result"], artifact_scope="EXECUTION_OUTPUT", artifact_type="SCIENTIFIC_RESULT_JSON", object_key=f"g06/p05/{ids['artifact']}", content_hash="result", media_type="application/json", size_bytes=1, metadata_json={}, created_at=now))
        session.add(LineageEdgeOrm(lineage_edge_id=ids["generic"], project_id=ids["project"], source_type="Result", source_id=ids["result"], relation_type="MOTIVATED", target_type="Execution", target_id=ids["execution"], evidence_json={"why": "review"}, created_by="g06-p05", created_at=now))
        session.commit()

    store = LocalArtifactStore(tmp_path / "objects")
    service = ProductClosureService(sessionmaker(bind=postgres_engine), store)
    graph = service.project_lineage(ids["project"], user_id="g06-p05")
    by_key = {(edge["source_type"], edge["relation_type"], edge["target_type"]): edge for edge in graph["edges"]}
    assert by_key[("DatasetVersion", "USED_INPUT", "Execution")]["source_class"] == "TYPED_STRUCTURAL"
    assert by_key[("Result", "MOTIVATED", "Execution")]["source_class"] == "GENERIC_ONLY"

    closure = service.result_lineage(ids["project"], ids["result"], user_id="g06-p05")
    assert {edge["source_class"] for edge in closure["edges"]} == {"TYPED_STRUCTURAL", "GENERIC_ONLY"}
    with Session(bind=postgres_engine) as session:
        before = session.scalar(select(func.count()).select_from(LineageEdgeOrm))
    exported = service.create_export(ids["project"], [ids["result"]], user_id="g06-p05")
    with Session(bind=postgres_engine) as session:
        after = session.scalar(select(func.count()).select_from(LineageEdgeOrm))
    assert before == after

    manifest = json.loads((tmp_path / "objects" / f"projects/{ids['project']}/exports/{exported['export_id']}/manifest.json").read_text())
    assert {edge["source_class"] for edge in manifest["lineage_references"]} == {"TYPED_STRUCTURAL", "GENERIC_ONLY"}
    assert not any(
        edge["relation_type"] == "USED_INPUT"
        and edge["source_type"] in {"ResearchContextVersion", "AnalysisSpecification", "ExecutionPlan"}
        for edge in manifest["lineage_references"]
    )
