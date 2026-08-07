from __future__ import annotations

import json
from pathlib import Path

import pytest
from sqlalchemy import select

from ariadne.interfaces.web_api import dependencies
from ariadne.product.persistence.orm_models import (
    FamilyArtifactOrm,
    FamilyExecutionOrm,
    FamilyStageExecutionOrm,
    LineageEdgeOrm,
)


@pytest.mark.anyio
@pytest.mark.requirement("FR-058", "FR-059", "FR-064", "FR-073", "AR-019")
async def test_split_api_persists_reproducible_partition_artifact_and_lineage(
    client, tmp_path: Path, predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    project_id = (await client.post("/api/v1/projects", json={"name": "Predictive G3"})).json()["project_id"]
    rows = ["entity_id,event_time,score,converted"]
    rows.extend(
        f"entity-{index // 2},2026-01-{index + 1:02d},{index / 10},{index % 2}"
        for index in range(12)
    )
    dataset = await client.post(
        f"/api/v1/projects/{project_id}/dataset-versions",
        files={"file": ("predictive.csv", ("\n".join(rows) + "\n").encode(), "text/csv")},
        data={"dataset_key": "predictive", "version_label": "v1", "name": "predictive"},
        headers={"Idempotency-Key": "e3-predictive-split"},
    )
    dataset_id = dataset.json()["dataset_version_id"]
    spec = predictive_spec_factory()
    spec["split_spec"].update({"strategy": "GROUP", "group_column": "entity_id"})
    request = {"dataset_version_id": dataset_id, "analysis_view_id": None, "family_spec": spec}

    first = await client.post(f"/api/v1/projects/{project_id}/predictive/split-validations", json=request)
    second = await client.post(f"/api/v1/projects/{project_id}/predictive/split-validations", json=request)
    assert first.status_code == 201 and second.status_code == 201
    first_body, second_body = first.json(), second.json()
    assert first_body["partition_counts"] == {"TRAIN": 6, "VALIDATION": 2, "TEST": 4}
    assert first_body["partition_artifact"]["content_hash"] == second_body["partition_artifact"]["content_hash"]
    assert first_body["partition_artifact"]["selection_contract"]["TEST"] == {
        "fit_allowed": False, "selection_allowed": False, "final_evaluation_only": True,
    }
    listed_executions = await client.get(f"/api/v1/projects/{project_id}/executions")
    assert listed_executions.status_code == 200
    assert first_body["execution_id"] not in {
        item["execution_id"] for item in listed_executions.json()["items"]
    }

    artifact_id = first_body["partition_artifact"]["artifact_id"]
    metadata = await client.get(
        f"/api/v1/projects/{project_id}/predictive/partition-artifacts/{artifact_id}"
    )
    assert metadata.status_code == 200
    assert metadata.json()["metadata"]["source_snapshot"]["dataset_version_id"] == dataset_id

    factory = dependencies._get_session_factory()
    with factory() as session:
        artifact = session.get(FamilyArtifactOrm, artifact_id)
        assert artifact is not None
        execution = session.get(FamilyExecutionOrm, first_body["execution_id"])
        stage = session.scalar(select(FamilyStageExecutionOrm).where(
            FamilyStageExecutionOrm.execution_id == first_body["execution_id"]
        ))
        assert execution is not None and execution.analysis_family == "PREDICTIVE"
        assert execution.specification_schema_version == "predictive-analysis-spec/1"
        assert stage is not None and stage.stage_type_json == {
            "namespace": "predictive", "name": "split", "version": "1",
        }
        stored_path = tmp_path / "partition.json"
        dependencies._get_artifact_store().retrieve(artifact.object_key, stored_path)
        manifest = json.loads(stored_path.read_text(encoding="utf-8"))
        edges = list(session.scalars(select(LineageEdgeOrm).where(
            LineageEdgeOrm.project_id == project_id,
            LineageEdgeOrm.target_id.in_([first_body["execution_id"], artifact_id]),
        )))
    assert manifest["schema_version"] == "partition-artifact/1"
    assert manifest["partitions"]
    assert manifest["group_counts"] == {"TRAIN": 3, "VALIDATION": 1, "TEST": 2}
    assert set(manifest["class_distribution"]) == {"TRAIN", "VALIDATION", "TEST"}
    assert any(edge.source_type == "DatasetVersion" and edge.source_id == dataset_id for edge in edges)
    assert any(edge.target_type == "Artifact" and edge.target_id == artifact_id for edge in edges)


@pytest.mark.anyio
@pytest.mark.requirement("FR-058", "FR-073", "AR-019")
async def test_split_from_fixed_analysis_view_records_view_lineage(
    client, tmp_path: Path, predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    project_id = (await client.post(
        "/api/v1/projects", json={"name": "Predictive View lineage"}
    )).json()["project_id"]
    rows = ["entity_id,event_time,score,converted"]
    rows.extend(
        f"entity-{index // 2},2026-01-{index + 1:02d},{index / 10},{index % 2}"
        for index in range(12)
    )
    dataset = await client.post(
        f"/api/v1/projects/{project_id}/dataset-versions",
        files={"file": (
            "predictive-view.csv",
            ("\n".join(rows) + "\n").encode(),
            "text/csv",
        )},
        data={"dataset_key": "predictive-view", "version_label": "v1", "name": "view"},
        headers={"Idempotency-Key": "e3-predictive-view"},
    )
    dataset_id = dataset.json()["dataset_version_id"]
    view_spec = {
        "schema_version": "analysis-view/1",
        "source_dataset_version_id": dataset_id,
        "row_filter": [],
        "selected_columns": ["entity_id", "event_time", "score", "converted"],
        "derived_columns": [],
        "missing_value_policy": {"default": "KEEP", "columns": {}},
        "time_cutoff": None,
        "sampling": None,
    }
    created = await client.post(
        f"/api/v1/projects/{project_id}/analysis-views",
        json={"view_key": "predictive", "name": "Predictive population", "spec": view_spec},
    )
    view_id = created.json()["analysis_view_id"]
    fixed = await client.post(
        f"/api/v1/projects/{project_id}/analysis-views/{view_id}/fix"
    )
    assert fixed.status_code == 200 and fixed.json()["status"] == "FIXED"

    spec = predictive_spec_factory()
    spec["split_spec"].update({"strategy": "GROUP", "group_column": "entity_id"})
    split = await client.post(
        f"/api/v1/projects/{project_id}/predictive/split-validations",
        json={
            "dataset_version_id": dataset_id,
            "analysis_view_id": view_id,
            "family_spec": spec,
        },
    )
    assert split.status_code == 201
    body = split.json()

    factory = dependencies._get_session_factory()
    with factory() as session:
        artifact = session.get(FamilyArtifactOrm, body["partition_artifact"]["artifact_id"])
        assert artifact is not None
        stored_path = tmp_path / "view-partition.json"
        dependencies._get_artifact_store().retrieve(artifact.object_key, stored_path)
        manifest = json.loads(stored_path.read_text(encoding="utf-8"))
        edge = session.scalar(select(LineageEdgeOrm).where(
            LineageEdgeOrm.project_id == project_id,
            LineageEdgeOrm.source_type == "AnalysisView",
            LineageEdgeOrm.source_id == view_id,
            LineageEdgeOrm.target_id == body["execution_id"],
        ))
    assert edge is not None and edge.relation_type == "USED_INPUT"
    assert manifest["row_identifier"]["kind"] == "ANALYSIS_VIEW_ROW_ORDINAL"
    assert manifest["source_snapshot"]["analysis_view_hash"] == fixed.json()["content_hash"]


@pytest.mark.anyio
@pytest.mark.requirement("FR-058", "FR-059", "NFR-005")
async def test_split_runner_validation_error_preserves_machine_code_and_field_path(
    client, predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    project_id = (await client.post(
        "/api/v1/projects", json={"name": "Predictive error contract"}
    )).json()["project_id"]
    dataset = await client.post(
        f"/api/v1/projects/{project_id}/dataset-versions",
        files={"file": (
            "small.csv",
            b"score,converted\n0.1,0\n0.2,1\n0.3,0\n0.4,1\n",
            "text/csv",
        )},
        data={"dataset_key": "small", "version_label": "v1", "name": "small"},
        headers={"Idempotency-Key": "e3-predictive-small"},
    )
    request = {
        "dataset_version_id": dataset.json()["dataset_version_id"],
        "analysis_view_id": None,
        "family_spec": predictive_spec_factory(),
    }
    response = await client.post(
        f"/api/v1/projects/{project_id}/predictive/split-validations", json=request
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "INSUFFICIENT_SPLIT_SAMPLE"
    assert response.json()["error"]["details"]["path"] == "split_spec"

    factory = dependencies._get_session_factory()
    with factory() as session:
        persisted = session.scalar(select(FamilyExecutionOrm).where(
            FamilyExecutionOrm.project_id == project_id,
            FamilyExecutionOrm.analysis_family == "PREDICTIVE",
        ))
    assert persisted is None


@pytest.mark.anyio
@pytest.mark.requirement("FR-055", "FR-058", "G5-CAPABILITIES")
async def test_g5_capabilities_advertise_explanation_and_model_card(
    client,
) -> None:  # type: ignore[no-untyped-def]
    project_id = (await client.post(
        "/api/v1/projects", json={"name": "Predictive capabilities"}
    )).json()["project_id"]
    response = await client.get(f"/api/v1/projects/{project_id}/predictive/capabilities")
    assert response.status_code == 200
    assert response.json()["gate"] == "G5_EXPLAIN_UI"
    assert response.json()["training_available"] is True
    assert response.json()["evaluation_available"] is True
    assert response.json()["explanation_available"] is True
    assert response.json()["model_card_available"] is True
    assert response.json()["model_registry"]
    assert response.json()["explanation_methods"] == [{
        "method": "LINEAR_COEFFICIENT_CONTRIBUTION",
        "supported_models": [
            "logistic_regression.v1",
            "linear_regression.v1",
        ],
        "supports_global": True,
        "supports_local": True,
        "model_output_scales": ["LOG_ODDS", "PREDICTION"],
    }]
    assert "PR_AUC" in response.json()["metrics"]["BINARY_CLASSIFICATION"]
