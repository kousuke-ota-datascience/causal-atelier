from __future__ import annotations

import pytest
from sqlalchemy import select

from ariadne.interfaces.web_api import dependencies
from ariadne.interfaces.worker.execution_processor import ExecutionProcessor
from ariadne.product.persistence.orm_models import (
    AnalysisSpecificationOrm,
    AnalysisViewOrm,
    ArtifactOrm,
    LineageEdgeOrm,
)
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
    context = await client.post(
        f"/api/v1/projects/{project_id}/research-contexts",
        json={"context_key": "explore-handoff"},
    )
    context_id = context.json()["research_context_version_id"]
    dataset = await client.post(
        f"/api/v1/projects/{project_id}/dataset-versions",
        files={"file": ("data.csv", b"group,sales,units\nA,10,1\nA,12,2\nB,20,3\n", "text/csv")},
        data={"dataset_key": "explore", "version_label": "v1", "name": "explore"},
        headers={"Idempotency-Key": "e3-explore"},
    )
    dataset_id = dataset.json()["dataset_version_id"]
    selection = {
        "schema_version": "analysis-view/1",
        "source_dataset_version_id": dataset_id,
        "row_filter": [{"column": "group", "operator": "EQ", "value": "A"}],
        "selected_columns": ["group", "sales", "units"],
        "derived_columns": [],
        "missing_value_policy": {},
        "time_cutoff": None,
        "sampling": None,
    }
    view = await client.post(f"/api/v1/projects/{project_id}/analysis-views", json={
        "view_key": "handoff", "name": "Handoff selection", "spec": selection,
    })
    source_view_id = view.json()["analysis_view_id"]
    assert view.status_code == 201
    assert (await client.post(
        f"/api/v1/projects/{project_id}/analysis-views/{source_view_id}/fix"
    )).status_code == 200
    request = {
        "dataset_version_id": dataset_id,
        "analysis_view_id": source_view_id,
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
    factory = dependencies._get_session_factory()
    with factory() as session:
        session.add(LineageEdgeOrm(
            project_id=project_id,
            source_type="Result",
            source_id=result_id,
            relation_type="DOCUMENTS",
            target_type="ResearchContextVersion",
            target_id=context_id,
            evidence_json={},
            created_by="test",
        ))
        session.commit()
    draft = await client.post(
        f"/api/v1/projects/{project_id}/exploration/results/{result_id}/create-analysis-draft",
        json={
            "target_family": "PREDICTIVE",
            "analysis_mode": "EXPLORATORY",
        },
    )
    assert draft.status_code == 201
    assert draft.json()["source_relation"]["analysis_mode"] == "EXPLORATORY"
    assert draft.json()["status"] == "DRAFT"

    with factory() as session:
        artifact = session.scalar(select(ArtifactOrm).where(
            ArtifactOrm.execution_id == execution_id
        ))
        assert artifact is not None
        assert artifact.metadata_json["view_manifest"]["source_dataset_content_hash"]
        edges = list(session.scalars(select(LineageEdgeOrm).where(
            LineageEdgeOrm.project_id == project_id
        )))
        handoff_spec = session.get(
            AnalysisSpecificationOrm, draft.json()["analysis_specification_id"]
        )
        handoff_view = session.get(AnalysisViewOrm, draft.json()["analysis_view_id"])
    assert any(edge.source_id == result_id and edge.target_type == "AnalysisSpecification" for edge in edges)
    assert handoff_spec is not None and handoff_spec.status == "DRAFT"
    assert handoff_spec.research_context_version_id == context_id
    assert handoff_view is not None and handoff_view.status == "DRAFT"
    assert handoff_view.spec_json == selection

    second_context = await client.post(
        f"/api/v1/projects/{project_id}/research-contexts",
        json={"context_key": "ambiguous-handoff"},
    )
    second_context_id = second_context.json()["research_context_version_id"]
    with factory() as session:
        session.add(LineageEdgeOrm(
            project_id=project_id,
            source_type="Result",
            source_id=result_id,
            relation_type="DOCUMENTS",
            target_type="ResearchContextVersion",
            target_id=second_context_id,
            evidence_json={},
            created_by="test",
        ))
        session.commit()
    ambiguous = await client.post(
        f"/api/v1/projects/{project_id}/exploration/results/{result_id}/create-analysis-draft",
        json={"target_family": "CAUSAL", "analysis_mode": "CONFIRMATORY"},
    )
    assert ambiguous.status_code == 422
    confirmatory = await client.post(
        f"/api/v1/projects/{project_id}/exploration/results/{result_id}/create-analysis-draft",
        json={
            "target_family": "CAUSAL",
            "analysis_mode": "CONFIRMATORY",
            "research_context_version_id": second_context_id,
        },
    )
    assert confirmatory.status_code == 201
    assert confirmatory.json()["warnings"] == [{
        "code": "EXPLORATORY_REUSE_SAME_DATA",
        "source_result_id": result_id,
        "dataset_version_id": dataset_id,
    }]
