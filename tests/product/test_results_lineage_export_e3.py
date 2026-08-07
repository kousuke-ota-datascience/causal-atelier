from __future__ import annotations

import json
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


async def _workspace(client) -> tuple[str, str]:  # type: ignore[no-untyped-def]
    project_id = (await client.post(
        "/api/v1/projects", json={"name": "G6 Results", "topic": "closure"}
    )).json()["project_id"]
    dataset = await client.post(
        f"/api/v1/projects/{project_id}/dataset-versions",
        files={"file": ("data.csv", b"score,target\n-1,0\n1,1\n", "text/csv")},
        data={"dataset_key": "g6-results", "version_label": "v1", "name": "G6"},
        headers={"Idempotency-Key": "g6-results"},
    )
    return project_id, dataset.json()["dataset_version_id"]


def _result(project_id: str, dataset_id: str, *, family: str = "PREDICTIVE", value: float = .8) -> str:
    now = datetime.now(timezone.utc)
    plan_id, execution_id, stage_id, result_id = [str(uuid.uuid4()) for _ in range(4)]
    factory = dependencies._get_session_factory()
    with factory() as session:
        session.add(ExecutionPlanOrm(
            execution_plan_id=plan_id, project_id=project_id,
            analysis_specification_id=f"fixture-{result_id}", analysis_family=family,
            plan_schema_version="execution-plan/1", planner_id="g6.fixture",
            planner_version="1", stages_json=[], dependencies_json=[],
            plan_hash=uuid.uuid4().hex, created_at=now,
        )); session.flush()
        session.add(FamilyExecutionOrm(
            execution_id=execution_id, project_id=project_id,
            dataset_version_id=dataset_id, execution_plan_id=plan_id,
            analysis_family=family, specification_schema_version="fixture/1",
            specification_snapshot_json={}, snapshot_json={}, snapshot_hash=uuid.uuid4().hex,
            status="SUCCEEDED", retry_count=0, requested_by="g6", requested_at=now,
            started_at=now, finished_at=now,
        )); session.flush()
        session.add(FamilyStageExecutionOrm(
            stage_execution_id=stage_id, execution_id=execution_id, stage_key="evaluate",
            stage_type_json={"namespace": "g6", "name": "evaluate", "version": "1"},
            ordinal=0, status="SUCCEEDED", attempt_history_json=[{"attempt": 1}],
            input_binding_json={}, output_binding_json={}, started_at=now, finished_at=now,
        )); session.flush()
        session.add(FamilyResultOrm(
            result_id=result_id, project_id=project_id, execution_id=execution_id,
            stage_execution_id=stage_id, analysis_family=family,
            result_type="EVALUATION_RESULT" if family == "PREDICTIVE" else "PROFILE_RESULT",
            schema_version="fixture-result/1", analytical_status="EVALUATED",
            summary_json={"metric": value, "api_token": "must-not-leak"},
            payload_json={"prediction_rows": [{"score": value}]}, diagnostics_json={},
            warning_json=["fixture limitation"], created_at=now,
        )); session.commit()
    return result_id


@pytest.mark.anyio
@pytest.mark.requirement("G6-RESULTS-COMPARISON-SUMMARY")
async def test_unified_results_summary_and_compatible_comparison_do_not_rank_metrics(client) -> None:  # type: ignore[no-untyped-def]
    project_id, dataset_id = await _workspace(client)
    first = _result(project_id, dataset_id, value=.75)
    second = _result(project_id, dataset_id, value=.82)
    exploratory = _result(project_id, dataset_id, family="EXPLORATORY", value=1)

    listed = await client.get(f"/api/v1/projects/{project_id}/results")
    assert listed.status_code == 200
    assert {item["analysis_family"] for item in listed.json()["items"]} == {
        "PREDICTIVE", "EXPLORATORY"
    }
    summary = (await client.get(
        f"/api/v1/projects/{project_id}/results/summary"
    )).json()
    assert summary["result_count"] == 3
    assert summary["ranking"] is None
    assert "not normalized or ranked" in summary["warning"]

    comparison = await client.post(
        f"/api/v1/projects/{project_id}/comparisons",
        json={"result_ids": [first, second]},
    )
    assert comparison.status_code == 201
    assert comparison.json()["compatible"] is True
    assert comparison.json()["ranking"] is None
    assert comparison.json()["differences"] == [
        {"field": "metric", "values": [.75, .82]}
    ]
    detail = (await client.get(
        f"/api/v1/projects/{project_id}/results/{first}"
    )).json()
    assert detail["sensitive_output_suppressed"] is True
    assert detail["payload"]["prediction_rows"] == "[SENSITIVE_OUTPUT_SUPPRESSED]"
    incompatible = await client.post(
        f"/api/v1/projects/{project_id}/comparisons",
        json={"result_ids": [first, exploratory]},
    )
    assert incompatible.status_code == 422
    assert incompatible.json()["error"]["code"] == "INVALID_SCHEMA"


@pytest.mark.anyio
@pytest.mark.requirement("G6-ANNOTATION-EXPORT-SECURITY")
async def test_annotation_history_export_redaction_artifact_download_and_roles(client) -> None:  # type: ignore[no-untyped-def]
    project_id, dataset_id = await _workspace(client)
    result_id = _result(project_id, dataset_id)

    created = await client.post(
        f"/api/v1/projects/{project_id}/workspace-annotations",
        json={
            "target_type": "Result", "target_id": result_id,
            "statement": "Use for prioritization only.",
            "rationale": "Validated on held-out TEST data.",
            "assumptions": ["Population remains comparable"],
            "limitations": ["No causal interpretation"],
            "decision": "SELECTED", "next_actions": ["Monitor drift"],
        },
    )
    assert created.status_code == 201
    annotation_id = created.json()["annotation_id"]
    updated = await client.patch(
        f"/api/v1/projects/{project_id}/workspace-annotations/{annotation_id}",
        json={"statement": "Use with monthly monitoring.", "decision": "DEFERRED"},
    )
    assert updated.status_code == 200
    assert len(updated.json()["revision_history"]) == 1
    assert updated.json()["revision_history"][0]["decision"] == "SELECTED"

    exported = await client.post(
        f"/api/v1/projects/{project_id}/exports", json={"result_ids": [result_id]}
    )
    assert exported.status_code == 201
    export_id = exported.json()["export_id"]
    assert exported.json()["manifest_summary"]["sensitive_rows_included"] is False
    metadata = await client.get(
        f"/api/v1/projects/{project_id}/artifacts/{export_id}"
    )
    assert metadata.status_code == 200
    assert metadata.json()["source"] == "EXPORT"
    downloaded = await client.get(
        f"/api/v1/projects/{project_id}/exports/{export_id}/download"
    )
    assert downloaded.status_code == 200
    assert downloaded.headers["x-content-type-options"] == "nosniff"
    manifest = json.loads(downloaded.content)
    assert manifest["schema_version"] == "ariadne-export-manifest/1"
    assert manifest["sensitive_rows_included"] is False
    assert "must-not-leak" not in downloaded.text
    assert manifest["results"][0]["summary"]["api_token"] == "[REDACTED]"
    assert "prediction_rows" not in manifest["results"][0]

    membership = await client.put(
        f"/api/v1/projects/{project_id}/members/reviewer",
        json={"role": "VIEWER"},
    )
    assert membership.status_code == 200
    viewer_headers = {"X-User-Id": "reviewer"}
    assert (await client.get(
        f"/api/v1/projects/{project_id}/results", headers=viewer_headers
    )).status_code == 200
    forbidden = await client.put(
        f"/api/v1/projects/{project_id}/workspace-state",
        json={"dataset_version_id": dataset_id}, headers=viewer_headers,
    )
    assert forbidden.status_code == 403
    assert forbidden.json()["error"]["code"] == "PROJECT_ACCESS_DENIED"


@pytest.mark.anyio
@pytest.mark.requirement("G6-STRICT-CONTRACT")
async def test_g6_request_contracts_reject_unknown_fields(client) -> None:  # type: ignore[no-untyped-def]
    project_id, _ = await _workspace(client)
    response = await client.post(
        f"/api/v1/projects/{project_id}/exports",
        json={"result_ids": [], "unexpected": True},
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "INVALID_REQUEST"
