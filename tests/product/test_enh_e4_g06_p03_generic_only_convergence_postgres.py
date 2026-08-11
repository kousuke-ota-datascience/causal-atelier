"""Real-PostgreSQL active generic-only writer evidence for E4-G06 P03."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from ariadne.adapters.local_artifact_store import LocalArtifactStore
from ariadne.product.application.product_closure_service import ProductClosureService
from ariadne.product.persistence.orm_models import (
    ArtifactOrm,
    DatasetVersionOrm,
    LineageEdgeOrm,
    ProjectMembershipOrm,
    ProjectOrm,
)


def _id() -> str:
    return str(uuid.uuid4())


@pytest.mark.postgres
def test_p03_annotation_decision_is_guarded_generic_only_writer(postgres_engine, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    ids = {name: _id() for name in ("project", "membership", "artifact", "dataset")}
    now = datetime.now(timezone.utc)
    with Session(bind=postgres_engine) as session:
        session.add(ProjectOrm(project_id=ids["project"], name="G06 P03", status="ACTIVE", created_at=now, updated_at=now))
        session.flush()
        session.add(ProjectMembershipOrm(
            membership_id=ids["membership"], project_id=ids["project"], user_id="g06-p03",
            role="OWNER", created_at=now,
        ))
        session.add(ArtifactOrm(
            artifact_id=ids["artifact"], project_id=ids["project"], artifact_type="DATASET_FILE",
            object_key=f"g06/p03/{ids['artifact']}", content_hash="dataset", media_type="text/csv",
            size_bytes=1, metadata_json={}, created_at=now,
        ))
        session.flush()
        session.add(DatasetVersionOrm(
            dataset_version_id=ids["dataset"], project_id=ids["project"], source_artifact_id=ids["artifact"],
            dataset_key="g06-p03", name="G06 P03", version_label="v1", content_hash="dataset",
            schema_json={}, profile_summary_json={}, row_count=1, column_count=1, created_at=now,
        ))
        session.commit()

    service = ProductClosureService(sessionmaker(bind=postgres_engine), LocalArtifactStore(tmp_path / "objects"))
    annotation = service.create_annotation(ids["project"], {
        "target_type": "Project", "target_id": ids["project"], "statement": "Selected for review.",
        "rationale": "P03 evidence", "assumptions": [], "limitations": [], "decision": "SELECTED", "next_actions": [],
    }, user_id="g06-p03")
    with Session(bind=postgres_engine) as session:
        edge = session.scalar(select(LineageEdgeOrm).where(
            LineageEdgeOrm.source_id == ids["project"], LineageEdgeOrm.relation_type == "SELECTED",
            LineageEdgeOrm.target_type == "Annotation", LineageEdgeOrm.target_id == annotation["annotation_id"],
        ))
    assert edge is not None
    assert edge.evidence_json == {"rationale": "P03 evidence"}
