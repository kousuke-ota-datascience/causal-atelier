"""Real-PostgreSQL P02 evidence for canonical submit lineage cutover."""

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
from ariadne.product.application.exploratory_service import ExploratoryWorkspaceService
from ariadne.product.application.predictive_workflow_service import PredictiveWorkflowService
from ariadne.product.application.workspace_lifecycle_service import WorkspaceLifecycleService
from ariadne.product.domain.errors import LegacyProductAuthorityDisabled
from ariadne.product.domain.lineage import LineageAuthority, classify_lineage_authority
from ariadne.product.persistence.orm_models import (
    AnalysisViewOrm,
    ArtifactOrm,
    DatasetVersionOrm,
    ExecutionOrm,
    LineageEdgeOrm,
    ProjectOrm,
)
from ariadne.product.persistence.unit_of_work import SqlUnitOfWork


def _id() -> str:
    return str(uuid.uuid4())


def _services(engine, tmp_path: Path) -> tuple[ExploratoryWorkspaceService, PredictiveWorkflowService, WorkspaceLifecycleService]:  # type: ignore[no-untyped-def]
    factory = sessionmaker(bind=engine)

    @contextmanager
    def uow_factory() -> Iterator[SqlUnitOfWork]:
        session = factory()
        try:
            yield SqlUnitOfWork(session)
        finally:
            session.close()

    execution_service = ExecutionService(uow_factory=uow_factory)
    store = LocalArtifactStore(tmp_path / "objects")
    return (
        ExploratoryWorkspaceService(factory, store, execution_service=execution_service),
        PredictiveWorkflowService(factory, store, execution_service=execution_service),
        WorkspaceLifecycleService(factory),
    )


def _seed(engine) -> dict[str, str]:  # type: ignore[no-untyped-def]
    ids = {name: _id() for name in ("project", "artifact", "dataset", "view")}
    now = datetime.now(timezone.utc)
    with Session(bind=engine) as session:
        session.add(ProjectOrm(project_id=ids["project"], name="G06 P02", status="ACTIVE", created_at=now, updated_at=now))
        session.flush()
        session.add(ArtifactOrm(
            artifact_id=ids["artifact"], project_id=ids["project"], artifact_type="DATASET_FILE",
            object_key=f"g06/p02/{ids['artifact']}", content_hash="dataset-hash", media_type="text/csv",
            size_bytes=1, metadata_json={}, created_at=now,
        ))
        session.flush()
        session.add(DatasetVersionOrm(
            dataset_version_id=ids["dataset"], project_id=ids["project"], source_artifact_id=ids["artifact"],
            dataset_key="g06-p02", name="G06 P02", version_label="v1", content_hash="dataset-hash",
            schema_json={"columns": ["score", "converted", "customer_id"]}, profile_summary_json={},
            row_count=1, column_count=3, created_at=now,
        ))
        session.flush()
        session.add(AnalysisViewOrm(
            analysis_view_id=ids["view"], project_id=ids["project"], source_dataset_version_id=ids["dataset"],
            view_key="g06-p02", version_number=1, name="G06 P02", status="FIXED", schema_version="analysis-view/1",
            spec_json={}, content_hash="view-hash", manifest_json={}, created_by="g06-p02", created_at=now, fixed_at=now,
        ))
        session.commit()
    return ids


def _typed_edges(session: Session, execution_id: str) -> list[LineageEdgeOrm]:
    rows = list(session.scalars(select(LineageEdgeOrm).where(
        LineageEdgeOrm.target_type == "Execution", LineageEdgeOrm.target_id == execution_id,
    )))
    return [
        row for row in rows
        if classify_lineage_authority(row.source_type, row.relation_type, row.target_type)
        is LineageAuthority.TYPED_STRUCTURAL
    ]


@pytest.mark.postgres
def test_p02_canonical_exploratory_and_predictive_submit_do_not_write_typed_edges(
    postgres_engine, tmp_path: Path, predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    ids = _seed(postgres_engine)
    exploratory, predictive, workspace = _services(postgres_engine, tmp_path)

    exploratory_execution = exploratory.submit_execution(
        ids["project"], dataset_version_id=ids["dataset"], analysis_view_id=ids["view"],
        family_spec={"schema_version": "exploratory-analysis-spec/1", "operation": "PROFILE", "columns": ["score"]},
        requested_by="g06-p02",
    )
    with Session(bind=postgres_engine) as session:
        row = session.get(ExecutionOrm, exploratory_execution.execution_id)
        assert row is not None and row.analysis_family == "EXPLORATORY"
        assert row.dataset_version_id == ids["dataset"]
        assert row.analysis_spec_json["analysis_view_id"] == ids["view"]
        assert _typed_edges(session, row.execution_id) == []

    context = workspace.create_research_context(ids["project"], {
        "context_key": "g06-p02", "problem_statement": "predict", "research_questions": ["Who converts?"],
    }, created_by="g06-p02")
    workspace.fix_research_context(ids["project"], context["research_context_version_id"])
    specification = workspace.create_analysis_specification(ids["project"], {
        "specification_key": "g06-p02", "analysis_family": "PREDICTIVE",
        "research_context_version_id": context["research_context_version_id"], "dataset_version_id": ids["dataset"],
        "analysis_view_id": ids["view"], "analysis_mode": "EXPLORATORY",
        "family_spec_schema_version": "predictive-analysis-spec/1", "family_spec": predictive_spec_factory(),
    }, created_by="g06-p02")
    workspace.fix_analysis_specification(ids["project"], specification["analysis_specification_id"])
    plan = predictive.create_plan(ids["project"], specification["analysis_specification_id"])
    submitted = predictive.submit_execution(
        ids["project"], specification_id=specification["analysis_specification_id"],
        plan_id=plan["execution_plan_id"], seed=17, requested_by="g06-p02",
    )
    with Session(bind=postgres_engine) as session:
        row = session.get(ExecutionOrm, submitted["execution_id"])
        assert row is not None and row.analysis_family == "PREDICTIVE"
        assert row.dataset_version_id == ids["dataset"]
        assert row.analysis_spec_json["analysis_view_id"] == ids["view"]
        assert row.analysis_spec_json["analysis_specification_id"] == specification["analysis_specification_id"]
        assert row.analysis_spec_json["execution_plan_id"] == plan["execution_plan_id"]
        assert _typed_edges(session, row.execution_id) == []
        unclassified = list(session.scalars(select(LineageEdgeOrm).where(
            LineageEdgeOrm.target_type == "Execution", LineageEdgeOrm.target_id == row.execution_id,
        )))
        assert {(edge.source_type, edge.relation_type) for edge in unclassified} == {
            ("ResearchContextVersion", "USED_INPUT"),
            ("AnalysisSpecification", "USED_INPUT"),
            ("ExecutionPlan", "USED_INPUT"),
        }

    with pytest.raises(LegacyProductAuthorityDisabled):
        predictive.claim_next("token", worker_id="g06-p02")
    with pytest.raises(LegacyProductAuthorityDisabled):
        exploratory.claim_next("token", worker_id="g06-p02")
