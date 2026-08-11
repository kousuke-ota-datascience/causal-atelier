"""Real-PostgreSQL service evidence for E4-G06 P01 generic admission."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session, sessionmaker

from ariadne.adapters.local_artifact_store import LocalArtifactStore
from ariadne.product.application.product_closure_service import ProductClosureService
from ariadne.product.domain.errors import InvalidSchema
from ariadne.product.persistence.orm_models import (
    ArtifactOrm,
    DatasetVersionOrm,
    ExecutionOrm,
    LineageEdgeOrm,
    ProjectMembershipOrm,
    ProjectOrm,
    ResultOrm,
    StageExecutionOrm,
)


def _id() -> str:
    return str(uuid.uuid4())


def _service(engine, tmp_path: Path) -> ProductClosureService:  # type: ignore[no-untyped-def]
    return ProductClosureService(sessionmaker(bind=engine), LocalArtifactStore(tmp_path / "objects"))


def _seed_resources(engine) -> dict[str, str]:  # type: ignore[no-untyped-def]
    ids = {name: _id() for name in (
        "project", "member", "source_artifact", "target_artifact", "dataset",
        "execution", "stage", "result",
    )}
    now = datetime.now(timezone.utc)
    with Session(bind=engine) as session:
        session.add(ProjectOrm(
            project_id=ids["project"], name="G06 P01", status="ACTIVE",
            created_at=now, updated_at=now,
        ))
        session.flush()
        session.add(ProjectMembershipOrm(
            membership_id=ids["member"], project_id=ids["project"], user_id="g06-p01",
            role="OWNER", created_at=now,
        ))
        session.flush()
        session.add_all((
            ArtifactOrm(
                artifact_id=ids["source_artifact"], project_id=ids["project"],
                artifact_type="DATASET_FILE", object_key=f"g06/p01/{ids['source_artifact']}",
                content_hash="source", media_type="application/json", size_bytes=1,
                metadata_json={}, created_at=now,
            ),
            ArtifactOrm(
                artifact_id=ids["target_artifact"], project_id=ids["project"],
                artifact_type="MODEL_CARD", object_key=f"g06/p01/{ids['target_artifact']}",
                content_hash="target", media_type="application/json", size_bytes=1,
                metadata_json={}, created_at=now,
            ),
        ))
        session.flush()
        session.add(DatasetVersionOrm(
            dataset_version_id=ids["dataset"], project_id=ids["project"],
            source_artifact_id=ids["source_artifact"], dataset_key="g06-p01", name="G06 P01",
            version_label="v1", content_hash="source", schema_json={}, profile_summary_json={},
            row_count=1, column_count=1, created_at=now,
        ))
        session.add(ExecutionOrm(
            execution_id=ids["execution"], project_id=ids["project"],
            dataset_version_id=ids["dataset"], input_graph_version_id=None, input_result_id=None,
            analysis_family="CAUSAL", batch_key=_id(), operation="DISCOVERY",
            objective_snapshot="G06 P01", rationale_snapshot="policy verification",
            analysis_spec_json={}, algorithm_or_estimator="pc", parameter_json={}, random_seed=17,
            code_version="g06-p01", runtime_version_json={}, snapshot_hash="g06-p01",
            snapshot_schema_version="causal-analysis-spec/2", status="QUEUED", retry_count=0,
            last_error_summary=None, requested_by="g06-p01", requested_at=now,
            started_at=None, finished_at=None,
        ))
        session.flush()
        session.add(StageExecutionOrm(
            stage_execution_id=ids["stage"], execution_id=ids["execution"], stage_key="policy",
            stage_type_json={"namespace": "g06", "name": "policy", "version": "1"}, ordinal=0,
            dependencies_json=[], status="PENDING", input_binding_json={}, output_binding_json={},
            created_at=now,
        ))
        session.flush()
        session.add(ResultOrm(
            result_id=ids["result"], execution_id=ids["execution"], result_level="STAGE_RESULT",
            stage_execution_id=ids["stage"], result_type="SPLIT_RESULT", scientific_status="PASS",
            summary_json={"rows": 1}, payload_json={"schema_version": "partition/1"},
            diagnostics_json={}, warning_json=[], created_at=now,
        ))
        session.commit()
    return ids


def _edge_count(session: Session, **values: str) -> int:
    statement = select(func.count()).select_from(LineageEdgeOrm)
    for field, value in values.items():
        statement = statement.where(getattr(LineageEdgeOrm, field) == value)
    return int(session.scalar(statement) or 0)


@pytest.mark.postgres
def test_p01_generic_admission_guard_on_real_postgres(postgres_engine, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    ids = _seed_resources(postgres_engine)
    service = _service(postgres_engine, tmp_path)

    structural = {
        "source_type": "Execution", "source_id": ids["execution"],
        "relation_type": "GENERATED", "target_type": "Result", "target_id": ids["result"],
        "evidence": {"must_not_persist": True},
    }
    with pytest.raises(InvalidSchema, match="typed structural"):
        service.create_lineage_link(ids["project"], structural, user_id="g06-p01")
    with Session(bind=postgres_engine) as session:
        assert _edge_count(session, source_id=ids["execution"], relation_type="GENERATED", target_id=ids["result"]) == 0
        assert session.get(ResultOrm, ids["result"]).execution_id == ids["execution"]  # type: ignore[union-attr]

    positive = {
        "source_type": "Artifact", "source_id": ids["source_artifact"],
        "relation_type": "DERIVED_FROM", "target_type": "Artifact", "target_id": ids["target_artifact"],
        "evidence": {"stage": "model-card"},
    }
    created = service.create_lineage_link(ids["project"], positive, user_id="g06-p01")
    assert created["evidence"] == {"stage": "model-card"}
    with Session(bind=postgres_engine) as session:
        assert _edge_count(session, source_id=ids["source_artifact"], relation_type="DERIVED_FROM", target_id=ids["target_artifact"]) == 1

    unknown = {
        "source_type": "Artifact", "source_id": ids["source_artifact"],
        "relation_type": "DERIVED_FROM", "target_type": "Result", "target_id": ids["result"],
        "evidence": {},
    }
    with pytest.raises(InvalidSchema, match="Unsupported generic lineage semantic relation"):
        service.create_lineage_link(ids["project"], unknown, user_id="g06-p01")
    with Session(bind=postgres_engine) as session:
        assert _edge_count(session, source_id=ids["source_artifact"], relation_type="DERIVED_FROM", target_id=ids["result"]) == 0
