from __future__ import annotations

import pytest
from sqlalchemy import select

from ariadne.interfaces.web_api import dependencies
from ariadne.interfaces.worker.execution_processor import ExecutionProcessor
from ariadne.product.persistence.orm_models import ArtifactOrm, LineageEdgeOrm
from ariadne.scientific.core_adapter import ScientificCoreAdapter


def _process_canonical_exploratory(execution_id: str) -> None:
    token = "test-exploratory-worker"
    with dependencies._uow_context() as uow:
        claimed = uow.executions.claim_next(token, worker_id=token)
        uow.commit()
    assert claimed is not None and claimed.execution_id == execution_id
    ExecutionProcessor(
        dependencies._uow_context, ScientificCoreAdapter(),
        dependencies._get_artifact_store(), owner_token=token,
    ).process(claimed)


@pytest.mark.anyio
@pytest.mark.requirement("E2E-02", "E2E-03", "FR-029", "FR-030", "FR-032", "FR-034")
async def test_saved_exploration_result_artifact_manifest_and_draft_lineage(client) -> None:  # type: ignore[no-untyped-def]
    project_id = (await client.post("/api/v1/projects", json={"name": "Explore E2E"})).json()["project_id"]
    dataset = await client.post(
        f"/api/v1/projects/{project_id}/dataset-versions",
        files={"file": ("data.csv", b"group,sales,units\nA,10,1\nA,12,2\nB,20,3\n", "text/csv")},
        data={"dataset_key": "explore", "version_label": "v1", "name": "explore"},
        headers={"Idempotency-Key": "e3-explore"},
    )
    dataset_id = dataset.json()["dataset_version_id"]
    request = {
        "dataset_version_id": dataset_id,
        "analysis_view_id": None,
        "family_spec": {
            "schema_version": "exploratory-analysis-spec/1", "operation": "CHART",
            "columns": ["units", "sales"],
            "chart_encoding": {"mark": "point", "x": "units", "y": "sales"},
            "sampling": {"size": 100},
        },
    }
    preview = await client.post(f"/api/v1/projects/{project_id}/exploration/preview", json=request)
    assert preview.status_code == 200 and preview.json()["saved"] is False
    submitted = await client.post(f"/api/v1/projects/{project_id}/exploration/executions", json=request)
    assert submitted.status_code == 202
    assert submitted.json()["status"] == "QUEUED"
    execution_id = submitted.json()["execution_id"]
    _process_canonical_exploratory(execution_id)
    running = (await client.get(
        f"/api/v1/projects/{project_id}/exploration/executions/{execution_id}"
    )).json()
    assert running["status"] == "SUCCEEDED"
    execution = (await client.get(
        f"/api/v1/projects/{project_id}/exploration/executions/{execution_id}"
    )).json()
    assert execution["status"] == "SUCCEEDED"
    results = (await client.get(f"/api/v1/projects/{project_id}/exploration/results")).json()["items"]
    assert len(results) == 1 and results[0]["result_type"] == "CHART_RESULT"
    assert results[0]["analysis_family"] == "EXPLORATORY"
    result_id = results[0]["result_id"]
    draft = await client.post(
        f"/api/v1/projects/{project_id}/exploration/results/{result_id}/create-analysis-draft",
        json={"target_family": "PREDICTIVE"},
    )
    assert draft.status_code == 201
    assert draft.json()["source_relation"]["analysis_mode"] == "EXPLORATORY"
    assert "exploratory" in draft.json()["source_relation"]["warning"].lower()

    factory = dependencies._get_session_factory()
    with factory() as session:
        artifact = session.scalar(select(ArtifactOrm).where(
            ArtifactOrm.execution_id == execution_id
        ))
        assert artifact is not None
        assert artifact.metadata_json["view_manifest"]["source_dataset_content_hash"]
        edges = list(session.scalars(select(LineageEdgeOrm).where(
            LineageEdgeOrm.project_id == project_id
        )))
    assert any(edge.source_type == "DatasetVersion" and edge.target_id == execution_id for edge in edges)
    assert any(edge.source_id == result_id and edge.target_type == "Artifact" for edge in edges)
    assert any(edge.source_id == result_id and edge.target_type == "AnalysisSpecificationDraft" for edge in edges)
