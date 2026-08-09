from __future__ import annotations

import json
import uuid
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

import pytest

from ariadne.interfaces.web_api import dependencies
from ariadne.product.persistence.orm_models import (
    AnalysisSpecificationOrm,
    ExecutionPlanOrm,
    FamilyArtifactOrm,
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


def _result(
    project_id: str, dataset_id: str, *, family: str = "PREDICTIVE", value: float = .8,
    context_id: str | None = None, view_id: str | None = None,
    specification_id: str | None = None, artifact_source: Path | None = None,
) -> dict[str, str | None]:
    now = datetime.now(timezone.utc)
    plan_id, execution_id, stage_id, result_id, artifact_id = [
        str(uuid.uuid4()) for _ in range(5)
    ]
    stored = None
    if artifact_source is not None:
        stored = dependencies._get_artifact_store().store(
            artifact_source,
            f"projects/{project_id}/g6-test/{artifact_id}.json",
            "application/json",
        )
    factory = dependencies._get_session_factory()
    with factory() as session:
        session.add(ExecutionPlanOrm(
            execution_plan_id=plan_id, project_id=project_id,
            analysis_specification_id=specification_id or f"fixture-{result_id}",
            analysis_family=family,
            plan_schema_version="execution-plan/1", planner_id="g6.fixture",
            planner_version="1", stages_json=[], dependencies_json=[],
            plan_hash=uuid.uuid4().hex, created_at=now,
        )); session.flush()
        session.add(FamilyExecutionOrm(
            execution_id=execution_id, project_id=project_id,
            dataset_version_id=dataset_id, execution_plan_id=plan_id,
            research_context_version_id=context_id, analysis_view_id=view_id,
            analysis_specification_id=specification_id,
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
            summary_json={
                "metric": value, "population": "held-out TEST",
                "api_token": "must-not-leak",
            },
            payload_json={
                "prediction_rows": [{"row_id": "sensitive-row", "score": value}],
                "local_explanation": [{"row_id": "sensitive-row", "prediction": value}],
            },
            diagnostics_json={"credential": "must-not-leak-diagnostic"},
            warning_json=["shared limitation", f"metric-specific warning {value}"],
            created_at=now,
        )); session.flush()
        if stored is not None:
            session.add(FamilyArtifactOrm(
                artifact_id=artifact_id, project_id=project_id,
                execution_id=execution_id, stage_execution_id=stage_id,
                result_id=result_id, family=family,
                artifact_type="G6_SOURCE_ARTIFACT", schema_version="g6-artifact/1",
                media_type=stored.media_type, object_key=stored.object_key,
                content_hash=stored.content_hash, size_bytes=stored.size_bytes,
                metadata_json={"purpose": "result-payload-separation"}, created_at=now,
            ))
        session.commit()
    return {
        "result_id": result_id, "execution_id": execution_id,
        "artifact_id": artifact_id if stored is not None else None,
    }


def _stored_result_snapshot(result_id: str) -> dict[str, object]:
    with dependencies._get_session_factory()() as session:
        row = session.get(FamilyResultOrm, result_id)
        assert row is not None
        return deepcopy({
            "summary": row.summary_json, "payload": row.payload_json,
            "diagnostics": row.diagnostics_json, "warnings": row.warning_json,
        })


async def _closure_resources(
    client, tmp_path: Path,
) -> dict[str, str]:  # type: ignore[no-untyped-def]
    project_id, dataset_id = await _workspace(client)
    context = await client.post(
        f"/api/v1/projects/{project_id}/research-contexts",
        json={
            "context_key": "g6-export", "problem_statement": "Audit closure artifacts.",
            "research_questions": ["Can the analysis be reproduced?"],
            "significance": "Preserve auditability.", "hypotheses": [],
            "decision_context": {"action": "audit"}, "relations": [],
        },
    )
    context_id = context.json()["research_context_version_id"]
    assert (await client.post(
        f"/api/v1/projects/{project_id}/research-contexts/{context_id}/fix"
    )).status_code == 200
    view = await client.post(
        f"/api/v1/projects/{project_id}/analysis-views",
        json={
            "view_key": "g6-export", "name": "G6 export view",
            "spec": {
                "schema_version": "analysis-view/1",
                "source_dataset_version_id": dataset_id,
                "row_filter": [], "selected_columns": ["score", "target"],
                "derived_columns": [],
                "missing_value_policy": {"default": "KEEP", "columns": {}},
                "time_cutoff": None, "sampling": None,
            },
        },
    )
    view_id = view.json()["analysis_view_id"]
    assert (await client.post(
        f"/api/v1/projects/{project_id}/analysis-views/{view_id}/validate"
    )).status_code == 200
    assert (await client.post(
        f"/api/v1/projects/{project_id}/analysis-views/{view_id}/fix"
    )).status_code == 200
    specification_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    with dependencies._get_session_factory()() as session:
        session.add(AnalysisSpecificationOrm(
            analysis_specification_id=specification_id, project_id=project_id,
            specification_key="g6-export", version_number=1, status="FIXED",
            schema_version="analysis-specification/1", analysis_family="PREDICTIVE",
            research_context_version_id=context_id, dataset_version_id=dataset_id,
            analysis_view_id=view_id, analysis_mode="CONFIRMATORY",
            family_spec_schema_version="g6-export-spec/1",
            family_spec_json={"model": "fixture", "api_token": "must-not-leak-spec"},
            revision_context_json=None, warnings_json=[], canonical_hash="1" * 64,
            created_by="g6-test", created_at=now, fixed_at=now,
        ))
        session.commit()
    graph = await client.post(
        f"/api/v1/projects/{project_id}/graph-versions",
        json={
            "source_result_id": None, "parent_graph_version_id": None,
            "graph_origin": "USER_DEFINED", "name": "G6 annotation graph",
            "graph_type": "DAG",
            "graph": {"graph_type": "DAG", "nodes": ["score", "target"], "edges": []},
            "designated_outcome_node": "target",
            "provenance": {"source_note": "G6 annotation target"},
            "edit_rationale": None, "fix_immediately": True,
        },
        headers={"Idempotency-Key": "g6-annotation-graph"},
    )
    assert graph.status_code == 201
    artifact_source = tmp_path / "g6-source-artifact.json"
    artifact_source.write_text(
        json.dumps({"schema_version": "g6-source/1", "safe_summary": "download separately"}),
        encoding="utf-8",
    )
    result = _result(
        project_id, dataset_id, context_id=context_id, view_id=view_id,
        specification_id=specification_id, artifact_source=artifact_source,
    )
    return {
        "project_id": project_id, "dataset_id": dataset_id,
        "context_id": context_id, "view_id": view_id,
        "specification_id": specification_id,
        "execution_id": str(result["execution_id"]),
        "result_id": str(result["result_id"]),
        "artifact_id": str(result["artifact_id"]),
        "graph_id": graph.json()["graph_version_id"],
    }


@pytest.mark.anyio
@pytest.mark.requirement("G6-RESULTS-COMPARISON-SUMMARY")
async def test_unified_results_summary_and_compatible_comparison_do_not_rank_metrics(client) -> None:  # type: ignore[no-untyped-def]
    project_id, dataset_id = await _workspace(client)
    first = str(_result(project_id, dataset_id, value=.75)["result_id"])
    second = str(_result(project_id, dataset_id, value=.82)["result_id"])
    exploratory = str(_result(
        project_id, dataset_id, family="EXPLORATORY", value=1
    )["result_id"])

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

    stored_before = {
        first: _stored_result_snapshot(first), second: _stored_result_snapshot(second),
    }
    comparison = await client.post(
        f"/api/v1/projects/{project_id}/comparisons",
        json={"result_ids": [first, second]},
    )
    assert comparison.status_code == 201
    compared = comparison.json()
    assert compared["compatible"] is True
    assert compared["ranking"] is None
    assert compared["common_summary"]["population"] == "held-out TEST"
    assert compared["common_summary"]["api_token"] == "[REDACTED]"
    assert compared["differences"] == [
        {"field": "metric", "values": [.75, .82]}
    ]
    assert compared["common_warnings"] == ["shared limitation"]
    assert compared["warning_differences"] == [
        {"result_id": first, "warnings": ["metric-specific warning 0.75"]},
        {"result_id": second, "warnings": ["metric-specific warning 0.82"]},
    ]
    assert _stored_result_snapshot(first) == stored_before[first]
    assert _stored_result_snapshot(second) == stored_before[second]
    detail = (await client.get(
        f"/api/v1/projects/{project_id}/results/{first}"
    )).json()
    assert detail["sensitive_output_suppressed"] is True
    assert detail["payload"]["prediction_rows"] == "[SENSITIVE_OUTPUT_SUPPRESSED]"
    assert detail["payload"]["local_explanation"] == "[SENSITIVE_OUTPUT_SUPPRESSED]"
    assert detail["summary"]["api_token"] == "[REDACTED]"
    assert detail["diagnostics"]["credential"] == "[REDACTED]"
    incompatible = await client.post(
        f"/api/v1/projects/{project_id}/comparisons",
        json={"result_ids": [first, exploratory]},
    )
    assert incompatible.status_code == 422
    assert incompatible.json()["error"]["code"] == "INVALID_SCHEMA"


@pytest.mark.anyio
@pytest.mark.requirement("G6-ANNOTATION-EXPORT-SECURITY")
async def test_annotation_target_matrix_history_and_export_manifest_contracts(
    client, tmp_path: Path,
) -> None:  # type: ignore[no-untyped-def]
    resources = await _closure_resources(client, tmp_path)
    project_id = resources["project_id"]
    result_id = resources["result_id"]

    targets = {
        "Project": project_id,
        "ResearchContextVersion": resources["context_id"],
        "AnalysisView": resources["view_id"],
        "AnalysisSpecification": resources["specification_id"],
        "Execution": resources["execution_id"],
        "Result": result_id,
        "GraphVersion": resources["graph_id"],
    }
    annotation_ids: dict[str, str] = {}
    for target_type, target_id in targets.items():
        created = await client.post(
            f"/api/v1/projects/{project_id}/workspace-annotations",
            json={
                "target_type": target_type, "target_id": target_id,
                "statement": f"Audit {target_type}.",
                "rationale": "Validated on held-out TEST data.",
                "assumptions": ["Population remains comparable"],
                "limitations": ["No causal interpretation"],
                "decision": "SELECTED", "next_actions": ["Monitor drift"],
            },
        )
        assert created.status_code == 201
        body = created.json()
        assert body["rationale"] == "Validated on held-out TEST data."
        assert body["assumptions"] == ["Population remains comparable"]
        assert body["limitations"] == ["No causal interpretation"]
        assert body["decision"] == "SELECTED"
        assert body["next_actions"] == ["Monitor drift"]
        annotation_ids[target_type] = body["annotation_id"]
    updated = await client.patch(
        f"/api/v1/projects/{project_id}/workspace-annotations/{annotation_ids['Result']}",
        json={"statement": "Use with monthly monitoring.", "decision": "DEFERRED"},
    )
    assert updated.status_code == 200
    assert len(updated.json()["revision_history"]) == 1
    assert updated.json()["revision_history"][0]["decision"] == "SELECTED"
    listed = (await client.get(
        f"/api/v1/projects/{project_id}/workspace-annotations"
    )).json()["items"]
    assert {item["target_type"] for item in listed} == set(targets)

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
    assert [item["analysis_specification_id"] for item in manifest["specifications"]] == [
        resources["specification_id"]
    ]
    assert manifest["specifications"][0]["family_spec"]["api_token"] == "[REDACTED]"
    assert [item["artifact_id"] for item in manifest["artifact_references"]] == [
        resources["artifact_id"]
    ]
    lineage_refs = {
        (item["source_type"], item["source_id"], item["relation_type"],
         item["target_type"], item["target_id"])
        for item in manifest["lineage_references"]
    }
    assert (
        "Execution", resources["execution_id"], "GENERATED", "Result", result_id
    ) in lineage_refs
    assert (
        "DatasetVersion", resources["dataset_id"], "USED_INPUT",
        "Execution", resources["execution_id"],
    ) in lineage_refs
    assert all(item["source_class"] in {"TYPED_STRUCTURAL", "GENERIC_ONLY"} for item in manifest["lineage_references"])
    assert not any(
        item["source_type"] == "AnalysisSpecification"
        and item["relation_type"] == "USED_INPUT"
        and item["target_type"] == "Execution"
        for item in manifest["lineage_references"]
    )

    detail = (await client.get(
        f"/api/v1/projects/{project_id}/results/{result_id}"
    )).json()
    assert detail["artifact_ids"] == [resources["artifact_id"]]
    assert "safe_summary" not in json.dumps(detail["payload"])
    source_download = await client.get(
        f"/api/v1/projects/{project_id}/artifacts/{resources['artifact_id']}/download"
    )
    assert source_download.status_code == 200
    assert source_download.headers["cache-control"] == "private, no-store"
    assert source_download.json() == {
        "schema_version": "g6-source/1", "safe_summary": "download separately",
    }


@pytest.mark.anyio
@pytest.mark.requirement("G6-AUTHORIZATION-SENSITIVE-OUTPUT")
async def test_project_access_controlled_download_hash_and_sensitive_output_policy(
    client, tmp_path: Path, caplog,
) -> None:  # type: ignore[no-untyped-def]
    resources = await _closure_resources(client, tmp_path)
    project_id = resources["project_id"]
    result_id = resources["result_id"]
    artifact_id = resources["artifact_id"]
    exported = await client.post(
        f"/api/v1/projects/{project_id}/exports", json={"result_ids": [result_id]}
    )
    assert exported.status_code == 201
    export_id = exported.json()["export_id"]

    membership = await client.put(
        f"/api/v1/projects/{project_id}/members/reviewer",
        json={"role": "VIEWER"},
    )
    assert membership.status_code == 200
    viewer_headers = {"X-User-Id": "reviewer"}
    outsider_headers = {"X-User-Id": "non-member"}

    default_detail = await client.get(
        f"/api/v1/projects/{project_id}/results/{result_id}"
    )
    assert default_detail.status_code == 200
    assert default_detail.json()["payload"]["prediction_rows"] == (
        "[SENSITIVE_OUTPUT_SUPPRESSED]"
    )
    assert default_detail.json()["payload"]["local_explanation"] == (
        "[SENSITIVE_OUTPUT_SUPPRESSED]"
    )
    assert default_detail.json()["summary"]["api_token"] == "[REDACTED]"
    assert default_detail.json()["diagnostics"]["credential"] == "[REDACTED]"

    viewer_detail = await client.get(
        f"/api/v1/projects/{project_id}/results/{result_id}", headers=viewer_headers,
    )
    assert viewer_detail.status_code == 200
    assert viewer_detail.json()["payload"]["local_explanation"] == (
        "[SENSITIVE_OUTPUT_SUPPRESSED]"
    )
    forbidden_sensitive = await client.get(
        f"/api/v1/projects/{project_id}/results/{result_id}?include_sensitive=true",
        headers=viewer_headers,
    )
    assert forbidden_sensitive.status_code == 403
    assert forbidden_sensitive.json()["error"]["code"] == "PROJECT_ACCESS_DENIED"
    owner_sensitive = await client.get(
        f"/api/v1/projects/{project_id}/results/{result_id}?include_sensitive=true"
    )
    assert owner_sensitive.status_code == 200
    assert owner_sensitive.json()["payload"]["local_explanation"] == [
        {"row_id": "sensitive-row", "prediction": .8}
    ]
    assert owner_sensitive.json()["summary"]["api_token"] == "[REDACTED]"

    assert (await client.get(
        f"/api/v1/projects/{project_id}/artifacts/{artifact_id}",
        headers=viewer_headers,
    )).status_code == 200
    viewer_download = await client.get(
        f"/api/v1/projects/{project_id}/artifacts/{artifact_id}/download",
        headers=viewer_headers,
    )
    assert viewer_download.status_code == 200
    assert viewer_download.headers["x-content-type-options"] == "nosniff"
    assert viewer_download.headers["cache-control"] == "private, no-store"
    viewer_export = await client.get(
        f"/api/v1/projects/{project_id}/exports/{export_id}/download",
        headers=viewer_headers,
    )
    assert viewer_export.status_code == 200
    assert "must-not-leak" not in viewer_export.text

    forbidden_write = await client.put(
        f"/api/v1/projects/{project_id}/workspace-state",
        json={"dataset_version_id": resources["dataset_id"]}, headers=viewer_headers,
    )
    assert forbidden_write.status_code == 403
    assert forbidden_write.json()["error"]["code"] == "PROJECT_ACCESS_DENIED"
    assert (await client.post(
        f"/api/v1/projects/{project_id}/workspace-annotations",
        json={
            "target_type": "Result", "target_id": result_id,
            "statement": "Viewer must not write.",
        },
        headers=viewer_headers,
    )).status_code == 403
    assert (await client.put(
        f"/api/v1/projects/{project_id}/members/another-user",
        json={"role": "VIEWER"}, headers=viewer_headers,
    )).status_code == 403

    for path in (
        f"/api/v1/projects/{project_id}/results/{result_id}",
        f"/api/v1/projects/{project_id}/artifacts/{artifact_id}/download",
        f"/api/v1/projects/{project_id}/exports/{export_id}/download",
    ):
        response = await client.get(path, headers=outsider_headers)
        assert response.status_code == 403
        assert response.json()["error"]["code"] == "PROJECT_ACCESS_DENIED"

    foreign_project = (await client.post(
        "/api/v1/projects", json={"name": "G6 foreign project"}
    )).json()["project_id"]
    assert (await client.get(
        f"/api/v1/projects/{foreign_project}/results/{result_id}"
    )).status_code == 404
    foreign_artifact = await client.get(
        f"/api/v1/projects/{foreign_project}/artifacts/{artifact_id}/download"
    )
    assert foreign_artifact.status_code == 422
    assert foreign_artifact.json()["error"]["code"] == "PROJECT_BOUNDARY_VIOLATION"
    foreign_export = await client.get(
        f"/api/v1/projects/{foreign_project}/exports/{export_id}/download"
    )
    assert foreign_export.status_code == 422
    assert foreign_export.json()["error"]["code"] == "PROJECT_BOUNDARY_VIOLATION"

    with dependencies._get_session_factory()() as session:
        artifact = session.get(FamilyArtifactOrm, artifact_id)
        assert artifact is not None
        object_key = artifact.object_key
    artifact_store = dependencies._get_artifact_store()
    (artifact_store._root / object_key).write_bytes(b"tampered")
    mismatch = await client.get(
        f"/api/v1/projects/{project_id}/artifacts/{artifact_id}/download"
    )
    assert mismatch.status_code == 500
    assert mismatch.json()["error"]["code"] == "ARTIFACT_HASH_MISMATCH"
    assert "must-not-leak" not in caplog.text
    assert "sensitive-row" not in caplog.text


@pytest.mark.anyio
@pytest.mark.requirement("G6-STRICT-CONTRACT")
async def test_g6_request_contracts_reject_unknown_fields(client) -> None:  # type: ignore[no-untyped-def]
    project_id, dataset_id = await _workspace(client)
    result_id = str(_result(project_id, dataset_id)["result_id"])
    response = await client.post(
        f"/api/v1/projects/{project_id}/exports",
        json={"result_ids": [result_id], "unexpected": True},
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "INVALID_REQUEST"
    errors = response.json()["error"]["details"]["errors"]
    assert any(
        error["loc"] == ["body", "unexpected"]
        and error["type"] == "extra_forbidden"
        for error in errors
    )
