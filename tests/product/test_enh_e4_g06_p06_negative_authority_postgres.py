"""Real-PostgreSQL mutation and persisted-authority audit for E4-G06 P06."""

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
from ariadne.product.application.product_closure_service import ProductClosureService
from ariadne.product.domain.lineage import LineageAuthority, classify_lineage_authority
from ariadne.product.persistence.orm_models import (
    ArtifactOrm, DatasetVersionOrm, ExecutionOrm, LineageEdgeOrm,
    ProjectMembershipOrm, ProjectOrm, ResultOrm,
)
from ariadne.product.persistence.unit_of_work import SqlUnitOfWork


def _id() -> str:
    return str(uuid.uuid4())


def _execution_kwargs(ids: dict[str, str], now: datetime, *, status: str, base_execution_id: str | None = None, revision_kind: str | None = None, change_reason: str | None = None) -> dict[str, object]:
    return {
        "project_id": ids["project"], "analysis_family": "CAUSAL", "dataset_version_id": ids["dataset"],
        "input_graph_version_id": None, "input_result_id": None, "batch_key": _id(), "operation": "DISCOVERY",
        "objective_snapshot": None, "rationale_snapshot": None, "analysis_spec_json": {},
        "algorithm_or_estimator": "p06", "parameter_json": {}, "random_seed": 1, "code_version": "p06",
        "runtime_version_json": {}, "snapshot_hash": _id(), "snapshot_schema_version": "causal-analysis-spec/2",
        "status": status, "retry_count": 0, "last_error_summary": None, "requested_by": "g06-p06",
        "requested_at": now, "started_at": None, "finished_at": now if status == "SUCCEEDED" else None,
        "base_execution_id": base_execution_id, "revision_kind": revision_kind, "change_reason": change_reason,
    }


@pytest.mark.postgres
def test_p06_retry_revision_and_persisted_authority_invariant(postgres_engine, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    ids = {name: _id() for name in ("project", "membership", "source", "dataset", "base", "retry", "rerun", "revised", "result", "artifact", "generic")}
    now = datetime.now(timezone.utc)
    with Session(bind=postgres_engine) as session:
        session.add(ProjectOrm(project_id=ids["project"], name="G06 P06", status="ACTIVE", created_at=now, updated_at=now)); session.flush()
        session.add(ProjectMembershipOrm(membership_id=ids["membership"], project_id=ids["project"], user_id="g06-p06", role="OWNER", created_at=now))
        session.add(ArtifactOrm(artifact_id=ids["source"], project_id=ids["project"], artifact_type="DATASET_FILE", object_key=f"g06/p06/{ids['source']}", content_hash="source", media_type="text/csv", size_bytes=1, metadata_json={}, created_at=now)); session.flush()
        session.add(DatasetVersionOrm(dataset_version_id=ids["dataset"], project_id=ids["project"], source_artifact_id=ids["source"], dataset_key="g06-p06", name="G06 P06", version_label="v1", content_hash="source", schema_json={}, profile_summary_json={}, row_count=1, column_count=1, created_at=now)); session.flush()
        session.add_all((
            ExecutionOrm(execution_id=ids["base"], **_execution_kwargs(ids, now, status="SUCCEEDED")),
            ExecutionOrm(execution_id=ids["retry"], **_execution_kwargs(ids, now, status="FAILED")),
            ExecutionOrm(execution_id=ids["rerun"], **_execution_kwargs(ids, now, status="QUEUED", base_execution_id=ids["base"], revision_kind="RERUN")),
            ExecutionOrm(execution_id=ids["revised"], **_execution_kwargs(ids, now, status="QUEUED", base_execution_id=ids["base"], revision_kind="REVISED", change_reason="changed estimator")),
        )); session.flush()
        session.add(ResultOrm(result_id=ids["result"], execution_id=ids["base"], result_level="EXECUTION_RESULT", stage_execution_id=None, result_type="DATA_PROFILE_RESULT", scientific_status="GENERATED", summary_json={}, payload_json={"schema_version": "profile/1"}, diagnostics_json={}, warning_json=[], created_at=now)); session.flush()
        session.add(ArtifactOrm(artifact_id=ids["artifact"], project_id=ids["project"], execution_id=ids["base"], stage_execution_id=None, result_id=ids["result"], artifact_scope="EXECUTION_OUTPUT", artifact_type="SCIENTIFIC_RESULT_JSON", object_key=f"g06/p06/{ids['artifact']}", content_hash="result", media_type="application/json", size_bytes=1, metadata_json={}, created_at=now))
        session.add(LineageEdgeOrm(lineage_edge_id=ids["generic"], project_id=ids["project"], source_type="Result", source_id=ids["result"], relation_type="MOTIVATED", target_type="Execution", target_id=ids["base"], evidence_json={}, created_by="g06-p06", created_at=now))
        session.commit()

    factory = sessionmaker(bind=postgres_engine)
    @contextmanager
    def uow_factory() -> Iterator[SqlUnitOfWork]:
        session = factory()
        try:
            yield SqlUnitOfWork(session)
        finally:
            session.close()
    ExecutionService(uow_factory=uow_factory).retry_execution(ids["retry"])
    with Session(bind=postgres_engine) as session:
        retried = session.get(ExecutionOrm, ids["retry"])
        assert retried is not None and retried.execution_id == ids["retry"] and retried.retry_count == 1 and retried.status == "QUEUED"
        assert session.scalar(select(func.count()).select_from(ExecutionOrm)) == 4
        rows = list(session.scalars(select(LineageEdgeOrm).where(LineageEdgeOrm.project_id == ids["project"])))
    assert rows
    classifications = [classify_lineage_authority(row.source_type, row.relation_type, row.target_type) for row in rows]
    assert classifications == [LineageAuthority.GENERIC_ONLY]

    service = ProductClosureService(factory, LocalArtifactStore(tmp_path / "objects"))
    graph = service.project_lineage(ids["project"], user_id="g06-p06")
    edges = {(edge["source_id"], edge["relation_type"], edge["target_id"], edge["source_class"]) for edge in graph["edges"]}
    assert (ids["base"], "DERIVED_FROM", ids["rerun"], "TYPED_STRUCTURAL") in edges
    assert (ids["base"], "REVISED_FROM", ids["revised"], "TYPED_STRUCTURAL") in edges
    with Session(bind=postgres_engine) as session:
        before = list(session.scalars(select(LineageEdgeOrm).where(LineageEdgeOrm.project_id == ids["project"])))
    service.result_lineage(ids["project"], ids["result"], user_id="g06-p06")
    service.create_export(ids["project"], [ids["result"]], user_id="g06-p06")
    with Session(bind=postgres_engine) as session:
        after = list(session.scalars(select(LineageEdgeOrm).where(LineageEdgeOrm.project_id == ids["project"])))
    assert [(row.lineage_edge_id, row.source_type, row.relation_type, row.target_type) for row in after] == [(row.lineage_edge_id, row.source_type, row.relation_type, row.target_type) for row in before]
