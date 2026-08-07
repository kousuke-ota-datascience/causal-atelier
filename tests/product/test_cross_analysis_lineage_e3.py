from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest

from ariadne.interfaces.web_api import dependencies
from ariadne.product.persistence.orm_models import (
    ExecutionPlanOrm,
    FamilyExecutionOrm,
    FamilyResultOrm,
    FamilyStageExecutionOrm,
)


async def _project_dataset(client, name: str, key: str) -> tuple[str, str]:  # type: ignore[no-untyped-def]
    project = await client.post("/api/v1/projects", json={"name": name})
    assert project.status_code == 201
    project_id = project.json()["project_id"]
    dataset = await client.post(
        f"/api/v1/projects/{project_id}/dataset-versions",
        files={"file": ("data.csv", b"x,y\n1,0\n2,1\n", "text/csv")},
        data={"dataset_key": key, "version_label": "v1", "name": name},
        headers={"Idempotency-Key": f"g6-{key}"},
    )
    assert dataset.status_code == 201
    return project_id, dataset.json()["dataset_version_id"]


def _family_result(
    project_id: str, dataset_id: str, family: str, result_type: str,
) -> tuple[str, str]:
    now = datetime.now(timezone.utc)
    execution_id, stage_id, result_id, plan_id = (
        str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())
    )
    factory = dependencies._get_session_factory()
    with factory() as session:
        session.add(ExecutionPlanOrm(
            execution_plan_id=plan_id, project_id=project_id,
            analysis_specification_id=f"g6-{family.lower()}-{result_id}",
            analysis_family=family, plan_schema_version="execution-plan/1",
            planner_id="g6.fixture", planner_version="1",
            stages_json=[], dependencies_json=[], plan_hash=uuid.uuid4().hex,
            created_at=now,
        ))
        session.flush()
        session.add(FamilyExecutionOrm(
            execution_id=execution_id, project_id=project_id,
            dataset_version_id=dataset_id, analysis_view_id=None,
            research_context_version_id=None, analysis_specification_id=None,
            execution_plan_id=plan_id, analysis_family=family,
            specification_schema_version="g6-fixture/1",
            specification_snapshot_json={}, snapshot_json={},
            snapshot_hash=uuid.uuid4().hex, status="SUCCEEDED", retry_count=0,
            last_error_json=None, requested_by="g6-test", requested_at=now,
            started_at=now, finished_at=now,
        ))
        session.flush()
        session.add(FamilyStageExecutionOrm(
            stage_execution_id=stage_id, execution_id=execution_id,
            stage_key="g6", stage_type_json={"namespace": "g6", "name": "fixture", "version": "1"},
            ordinal=0, status="SUCCEEDED", attempt_history_json=[{"attempt": 1}],
            input_binding_json={}, output_binding_json={}, started_at=now, finished_at=now,
        ))
        session.flush()
        session.add(FamilyResultOrm(
            result_id=result_id, project_id=project_id, execution_id=execution_id,
            stage_execution_id=stage_id, analysis_family=family,
            result_type=result_type, schema_version="g6-result/1",
            analytical_status="GENERATED", summary_json={"value": 1},
            payload_json={}, diagnostics_json={}, warning_json=[], created_at=now,
        ))
        session.commit()
    return execution_id, result_id


@pytest.mark.anyio
@pytest.mark.requirement("G6-CROSS-ANALYSIS-LINEAGE")
async def test_project_lineage_combines_families_and_explicit_relations(client) -> None:  # type: ignore[no-untyped-def]
    project_id, dataset_id = await _project_dataset(client, "G6 lineage", "g6-lineage")
    explore_execution, explore_result = _family_result(
        project_id, dataset_id, "EXPLORATORY", "CHART_RESULT"
    )
    predictive_execution, predictive_result = _family_result(
        project_id, dataset_id, "PREDICTIVE", "EVALUATION_RESULT"
    )
    linked = await client.post(
        f"/api/v1/projects/{project_id}/lineage-links",
        json={
            "source_type": "Result", "source_id": explore_result,
            "relation_type": "MOTIVATED",
            "target_type": "Result", "target_id": predictive_result,
            "evidence": {"statement": "Exploration motivated prediction."},
        },
    )
    assert linked.status_code == 201
    assert linked.json()["relation_type"] == "MOTIVATED"

    response = await client.get(f"/api/v1/projects/{project_id}/lineage")
    assert response.status_code == 200
    graph = response.json()
    assert graph["schema_version"] == "project-lineage/1"
    node_keys = {(item["node_type"], item["entity_id"]) for item in graph["nodes"]}
    assert ("Result", explore_result) in node_keys
    assert ("Result", predictive_result) in node_keys
    edges = {
        (item["source_type"], item["source_id"], item["relation_type"],
         item["target_type"], item["target_id"], item["explicit"])
        for item in graph["edges"]
    }
    assert ("DatasetVersion", dataset_id, "USED_INPUT", "Execution", explore_execution, False) in edges
    assert ("Execution", predictive_execution, "GENERATED", "Result", predictive_result, False) in edges
    assert ("Result", explore_result, "MOTIVATED", "Result", predictive_result, True) in edges

    result_graph = await client.get(
        f"/api/v1/projects/{project_id}/results/{predictive_result}/lineage"
    )
    assert result_graph.status_code == 200
    assert result_graph.json()["root_result_id"] == predictive_result
    assert explore_result in {item["entity_id"] for item in result_graph.json()["nodes"]}


@pytest.mark.anyio
@pytest.mark.requirement("G6-PROJECT-BOUNDARY")
async def test_explicit_lineage_link_rejects_cross_project_resources(client) -> None:  # type: ignore[no-untyped-def]
    first_project, first_dataset = await _project_dataset(client, "first", "g6-first")
    second_project, second_dataset = await _project_dataset(client, "second", "g6-second")
    _, first_result = _family_result(first_project, first_dataset, "EXPLORATORY", "PROFILE_RESULT")
    _, second_result = _family_result(second_project, second_dataset, "PREDICTIVE", "EVALUATION_RESULT")

    response = await client.post(
        f"/api/v1/projects/{first_project}/lineage-links",
        json={
            "source_type": "Result", "source_id": first_result,
            "relation_type": "MOTIVATED",
            "target_type": "Result", "target_id": second_result,
            "evidence": {},
        },
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "PROJECT_BOUNDARY_VIOLATION"
