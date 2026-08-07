from __future__ import annotations

import json
from pathlib import Path

import pytest
from sqlalchemy import select

from ariadne.interfaces.web_api import dependencies
from ariadne.product.persistence.orm_models import FamilyArtifactOrm, LineageEdgeOrm


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
        stored_path = tmp_path / "partition.json"
        dependencies._get_artifact_store().retrieve(artifact.object_key, stored_path)
        manifest = json.loads(stored_path.read_text(encoding="utf-8"))
        edges = list(session.scalars(select(LineageEdgeOrm).where(
            LineageEdgeOrm.project_id == project_id,
            LineageEdgeOrm.target_id.in_([first_body["execution_id"], artifact_id]),
        )))
    assert manifest["schema_version"] == "partition-artifact/1"
    assert manifest["partitions"]
    assert any(edge.source_type == "DatasetVersion" and edge.source_id == dataset_id for edge in edges)
    assert any(edge.target_type == "Artifact" and edge.target_id == artifact_id for edge in edges)
