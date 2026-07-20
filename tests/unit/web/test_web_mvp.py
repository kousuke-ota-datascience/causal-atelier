from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from causal_atelier.infrastructure.settings import WebSettings
from causal_atelier.interfaces.api.app import create_app
from causal_atelier.workers.executor import Worker


@pytest.fixture()
def web(tmp_path: Path):
    settings = WebSettings(
        database_url=f"sqlite:///{tmp_path / 'metadata.db'}",
        artifact_root=tmp_path / "objects",
        workspace_root=tmp_path / "workspaces",
        auto_create_schema=True,
        query_async_threshold_bytes=1_000_000,
    )
    app = create_app(settings)
    with TestClient(app) as client:
        yield client, app, settings


def _project(client: TestClient) -> dict:
    response = client.post(
        "/api/v1/projects",
        json={"slug": "analysis-project", "name": "Analysis project"},
    )
    assert response.status_code == 201
    return response.json()


def test_project_resources_are_hidden_across_users(web) -> None:
    client, _, _ = web
    project = _project(client)
    response = client.get(
        f"/api/v1/projects/{project['id']}",
        headers={"X-User-Subject": "different-user"},
    )
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"


def test_project_can_be_logically_deleted(web) -> None:
    client, app, _ = web
    project = _project(client)

    response = client.delete(f"/api/v1/projects/{project['id']}")

    assert response.status_code == 204
    assert client.get(f"/api/v1/projects/{project['id']}").status_code == 404
    listed_ids = {item["id"] for item in client.get("/api/v1/projects").json()["items"]}
    assert project["id"] not in listed_ids
    with app.state.database.session() as session:
        from causal_atelier.infrastructure.persistence import models as m

        deleted = session.get(m.Project, project["id"])
        assert deleted.status == "DELETED"
        assert deleted.deleted_at is not None


def test_configuration_yaml_is_validated_versioned_and_published(web) -> None:
    client, _, _ = web
    project = _project(client)
    configuration = client.post(
        "/api/v1/configurations",
        json={
            "project_id": project["id"],
            "configuration_type": "CAUSAL_DESIGN",
            "slug": "coupon-ate",
            "name": "Coupon ATE",
        },
    ).json()
    version_response = client.post(
        f"/api/v1/configurations/{configuration['id']}/versions",
        json={
            "yaml_text": """
causal_design:
  estimand: ATE
  treatment: {name: treated, levels: [0, 1]}
  outcome: {name: sales, window: {start: campaign_start, end: campaign_end}}
  unit: household
  assumptions: [consistency, positivity]
""",
        },
    )
    assert version_response.status_code == 201
    version = version_response.json()
    assert version["validation_status"] == "VALID"
    published = client.post(f"/api/v1/configuration-versions/{version['id']}/publish")
    assert published.status_code == 200
    assert published.json()["status"] == "PUBLISHED"
    duplicate = client.post(
        f"/api/v1/configurations/{configuration['id']}/versions",
        json={"canonical_json": version["canonical_json"]},
    )
    assert duplicate.status_code == 409


def test_dataset_profile_preview_and_aggregation(web) -> None:
    client, app, settings = web
    project = _project(client)
    object_response = client.post(
        f"/api/v1/projects/{project['id']}/objects",
        files={
            "file": ("transactions.csv", b"segment,value\na,1\na,2\nb,8\n", "text/csv")
        },
    )
    dataset = client.post(
        "/api/v1/datasets",
        json={
            "project_id": project["id"],
            "slug": "transactions",
            "name": "Transactions",
            "dataset_kind": "RAW",
        },
    ).json()
    version_response = client.post(
        f"/api/v1/datasets/{dataset['id']}/versions",
        json={
            "source_type": "UPLOAD",
            "tables": [
                {"logical_name": "transactions", "object": object_response.json()}
            ],
        },
    )
    assert version_response.status_code == 201
    table_id = version_response.json()["tables"][0]["id"]
    assert Worker(app.state.database, settings).run_once()
    profile = client.get(f"/api/v1/dataset-table-versions/{table_id}/profile").json()
    assert profile["status"] == "SUCCEEDED"
    assert profile["summary_json"]["row_count"] == 3
    preview = client.get(
        f"/api/v1/dataset-table-versions/{table_id}/preview?limit=2"
    ).json()
    assert len(preview["rows"]) == 2
    query = client.post(
        f"/api/v1/dataset-table-versions/{table_id}/visualization-queries",
        json={
            "specification": {
                "chart_type": "bar",
                "group_by": ["segment"],
                "aggregation_target": "value",
                "aggregation": "sum",
            }
        },
    )
    assert query.status_code == 200
    assert query.json()["status"] == "SUCCEEDED"
    assert query.json()["result_json"]["rows"] == [
        {"segment": "a", "sum_value": 3.0},
        {"segment": "b", "sum_value": 8.0},
    ]


def test_dry_run_is_idempotent_and_contains_an_immutable_plan(web) -> None:
    client, _, _ = web
    project = _project(client)
    request = {
        "project_id": project["id"],
        "run_kind": "PIPELINE",
        "execution_mode": "DRY_RUN",
        "stages": [
            {
                "stage_key": "etl",
                "stage_type": "ETL",
                "parameters": {"etl_type": "COMPLETE_JOURNEY"},
            }
        ],
    }
    first = client.post(
        "/api/v1/runs", json=request, headers={"Idempotency-Key": "same-request"}
    )
    second = client.post(
        "/api/v1/runs", json=request, headers={"Idempotency-Key": "same-request"}
    )
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["id"] == second.json()["id"]
    assert second.headers["Idempotency-Replayed"] == "true"
    assert first.json()["execution_plan"]["execution_mode"] == "DRY_RUN"
    assert first.json()["status"] == "SUCCEEDED"


def test_column_policy_blocks_preview_and_analysis(web) -> None:
    client, app, settings = web
    project = _project(client)
    uploaded = client.post(
        f"/api/v1/projects/{project['id']}/objects",
        files={"file": ("people.csv", b"name,amount\nAlice,1\nBob,2\n", "text/csv")},
    ).json()
    dataset = client.post(
        "/api/v1/datasets",
        json={
            "project_id": project["id"],
            "slug": "people",
            "name": "People",
            "dataset_kind": "RAW",
        },
    ).json()
    version = client.post(
        f"/api/v1/datasets/{dataset['id']}/versions",
        json={
            "source_type": "UPLOAD",
            "tables": [{"logical_name": "people", "object": uploaded}],
        },
    ).json()
    table = version["tables"][0]
    with app.state.database.session() as session:
        from sqlalchemy import select
        from causal_atelier.infrastructure.persistence import models as m

        column = session.scalar(
            select(m.DatasetColumn).where(
                m.DatasetColumn.dataset_table_version_id == table["id"],
                m.DatasetColumn.name == "name",
            )
        )
        column_id = column.id
    policy = client.patch(
        f"/api/v1/dataset-columns/{column_id}/policy",
        json={
            "classification": "PII",
            "preview_allowed": False,
            "analysis_allowed": False,
            "download_allowed": False,
        },
    )
    assert policy.status_code == 200
    preview = client.get(f"/api/v1/dataset-table-versions/{table['id']}/preview").json()
    assert "name" not in preview["rows"][0]
    denied = client.post(
        f"/api/v1/dataset-table-versions/{table['id']}/visualization-queries",
        json={"specification": {"group_by": ["name"], "aggregation": "count"}},
    )
    assert denied.status_code == 403


def test_retry_adds_an_attempt_without_overwriting_failure_history(web) -> None:
    client, app, settings = web
    project = _project(client)
    created = client.post(
        "/api/v1/runs",
        json={
            "project_id": project["id"],
            "run_kind": "ETL",
            "execution_mode": "RUN",
            "stages": [{"stage_key": "etl", "stage_type": "ETL"}],
        },
    )
    assert created.status_code == 202
    run_id = created.json()["id"]
    worker = Worker(app.state.database, settings)
    assert worker.run_once()
    failed = client.get(f"/api/v1/runs/{run_id}").json()
    assert failed["status"] == "FAILED"

    retried = client.post(f"/api/v1/runs/{run_id}/retry")
    assert retried.status_code == 202
    assert retried.json()["id"] == run_id
    assert worker.run_once()

    with app.state.database.session() as session:
        from sqlalchemy import select
        from causal_atelier.infrastructure.persistence import models as m

        stage = session.scalar(select(m.StageRun).where(m.StageRun.run_id == run_id))
        attempts = session.scalars(
            select(m.StageAttempt)
            .where(m.StageAttempt.stage_run_id == stage.id)
            .order_by(m.StageAttempt.attempt_number)
        ).all()
        assert [attempt.attempt_number for attempt in attempts] == [1, 2]
        assert [attempt.status for attempt in attempts] == ["FAILED", "FAILED"]
        assert all(attempt.error_message for attempt in attempts)


def test_analysis_ready_discovery_graph_and_result_navigation(web) -> None:
    client, app, settings = web
    project = _project(client)
    rows = ["treatment,outcome,covariate"]
    rows.extend(
        f"{index % 2},{2 * (index % 2) + index / 10},{index}"
        for index in range(60)
    )
    uploaded = client.post(
        f"/api/v1/projects/{project['id']}/objects",
        files={"file": ("analysis.csv", ("\n".join(rows) + "\n").encode(), "text/csv")},
    ).json()
    dataset = client.post(
        "/api/v1/datasets",
        json={
            "project_id": project["id"],
            "slug": "analysis-ready",
            "name": "Analysis ready",
            "dataset_kind": "PROCESSED",
        },
    ).json()
    version = client.post(
        f"/api/v1/datasets/{dataset['id']}/versions",
        json={
            "source_type": "UPLOAD",
            "source_metadata": {"analysis_unit_description": "one observation"},
            "tables": [{"logical_name": "analysis", "object": uploaded}],
        },
    ).json()
    assert version["analysis_binding"]["readiness_status"] == "READY"
    listed = client.get(f"/api/v1/datasets/{dataset['id']}/versions").json()
    assert listed["items"][0]["tables"][0]["columns"][0]["name"] == "treatment"

    semantics = _published_configuration(
        client,
        project["id"],
        "FEATURE_SEMANTICS",
        "analysis-semantics",
        {
            "dataset_version_id": version["id"],
            "default_unit_id": "row",
            "features": [
                {
                    "name": name,
                    "source_table": "analysis",
                    "source_column": name,
                    "role": role,
                    "allowed_for_discovery": True,
                    "allowed_for_adjustment": role == "covariate",
                }
                for name, role in (
                    ("treatment", "treatment"),
                    ("outcome", "outcome"),
                    ("covariate", "covariate"),
                )
            ],
        },
    )
    analysis = _published_configuration(
        client,
        project["id"],
        "DISCOVERY_ANALYSIS",
        "generic-discovery",
        {"input_mode": "ANALYSIS_READY", "algorithms": ["pc"]},
    )
    created = client.post(
        "/api/v1/runs",
        json={
            "project_id": project["id"],
            "run_kind": "DISCOVERY",
            "execution_mode": "RUN",
            "stages": [
                {
                    "stage_key": "discovery",
                    "stage_type": "DISCOVERY",
                    "input_mode": "ANALYSIS_READY",
                    "dataset_inputs": {"analysis_data": version["id"]},
                    "configuration_inputs": {
                        "analysis_config": analysis["id"],
                        "feature_semantics": semantics["id"],
                    },
                    "parameters": {
                        "algorithms": ["pc"],
                        "conditioning": {
                            "missing_values": "complete_case",
                            "categorical_encoding": "ordinal",
                            "standardize": True,
                        },
                    },
                }
            ],
        },
    )
    assert created.status_code == 202
    run_id = created.json()["id"]
    assert created.json()["stages"][0]["input_mode"] == "ANALYSIS_READY"
    resolved = created.json()["execution_plan"]["stages"][0]["resolved_inputs"]
    assert resolved["datasets"]["analysis_data"]["content_hash"]
    assert resolved["configurations"]["feature_semantics"]["content_hash"]

    worker = Worker(app.state.database, settings)
    for _ in range(5):
        worker.run_once()
        if client.get(f"/api/v1/runs/{run_id}").json()["status"] in {
            "SUCCEEDED",
            "FAILED",
        }:
            break
    completed = client.get(f"/api/v1/runs/{run_id}").json()
    assert completed["status"] == "SUCCEEDED", completed.get("error_summary")
    run_results = client.get(f"/api/v1/runs/{run_id}/results").json()
    assert run_results["total"] == 1
    assert run_results["items"][0]["result_type"] == "DISCOVERY"
    result = client.get(run_results["items"][0]["url"]).json()
    assert result["input_mode"] == "ANALYSIS_READY"
    assert result["feature_semantics_version_id"] == semantics["id"]
    assert result["algorithms"][0]["algorithm"] == "pc"

    graph = client.post(
        "/api/v1/causal-graphs",
        json={
            "project_id": project["id"],
            "slug": "selected-pc",
            "name": "Selected PC graph",
        },
    ).json()
    graph_version_response = client.post(
        f"/api/v1/causal-graphs/{graph['id']}/versions",
        json={
            "source_discovery_algorithm_result_id": result["algorithms"][0]["id"],
            "feature_semantics_version_id": semantics["id"],
            "selection_note": "selected in test",
        },
    )
    assert graph_version_response.status_code == 201
    graph_version = graph_version_response.json()
    published = client.post(
        f"/api/v1/causal-graph-versions/{graph_version['id']}/publish"
    )
    assert published.status_code == 200
    assert published.json()["status"] == "PUBLISHED"
    assert published.json()["content_hash"] == graph_version["content_hash"]

    inference_analysis = _published_configuration(
        client,
        project["id"],
        "INFERENCE_ANALYSIS",
        "generic-inference",
        {"input_mode": "ANALYSIS_READY", "analysis_mode": "EDGE_WEIGHT"},
    )
    inference_run = client.post(
        "/api/v1/runs",
        json={
            "project_id": project["id"],
            "run_kind": "INFERENCE",
            "execution_mode": "RUN",
            "stages": [
                {
                    "stage_key": "inference",
                    "stage_type": "INFERENCE",
                    "analysis_mode": "EDGE_WEIGHT",
                    "input_mode": "ANALYSIS_READY",
                    "dataset_inputs": {"analysis_data": version["id"]},
                    "configuration_inputs": {
                        "analysis_config": inference_analysis["id"],
                        "feature_semantics": semantics["id"],
                    },
                    "graph_inputs": {"causal_graph": graph_version["id"]},
                    "parameters": {
                        "conditioning": {
                            "missing_values": "complete_case",
                            "categorical_encoding": "ordinal",
                            "standardize": True,
                        }
                    },
                }
            ],
        },
    )
    assert inference_run.status_code == 202, inference_run.text
    inference_run_id = inference_run.json()["id"]
    for _ in range(3):
        worker.run_once()
        inference_status = client.get(
            f"/api/v1/runs/{inference_run_id}"
        ).json()["status"]
        if inference_status in {"SUCCEEDED", "FAILED"}:
            break
    assert inference_status == "SUCCEEDED"
    inference_results = client.get(
        f"/api/v1/runs/{inference_run_id}/results"
    ).json()
    assert inference_results["items"][0]["result_type"] == "EDGE_WEIGHT"
    edge_result = client.get(inference_results["items"][0]["url"]).json()
    assert edge_result["input_mode"] == "ANALYSIS_READY"
    assert edge_result["causal_graph_version_id"] == graph_version["id"]

    design = _published_configuration(
        client,
        project["id"],
        "CAUSAL_DESIGN",
        "analysis-design",
        {
            "causal_design": {
                "dataset_version_id": version["id"],
                "feature_semantics_version_id": semantics["id"],
                "causal_graph_version_id": graph_version["id"],
                "estimand": "ATE",
                "treatment": {"name": "treatment", "levels": [0, 1]},
                "outcome": {"name": "outcome"},
                "unit": "row",
                "target_population": "registered observations",
                "adjustment_strategy": "MANUAL",
                "adjustment_set": ["covariate"],
                "assumptions": [
                    {
                        "code": "exchangeability",
                        "statement": "No unmeasured confounding after adjustment",
                    }
                ],
            }
        },
    )
    treatment_analysis = _published_configuration(
        client,
        project["id"],
        "INFERENCE_ANALYSIS",
        "treatment-inference",
        {"input_mode": "ANALYSIS_READY", "analysis_mode": "TREATMENT_EFFECT"},
    )
    treatment_run = client.post(
        "/api/v1/runs",
        json={
            "project_id": project["id"],
            "run_kind": "INFERENCE",
            "execution_mode": "RUN",
            "stages": [
                {
                    "stage_key": "treatment_effect",
                    "stage_type": "INFERENCE",
                    "analysis_mode": "TREATMENT_EFFECT",
                    "input_mode": "ANALYSIS_READY",
                    "dataset_inputs": {"analysis_data": version["id"]},
                    "configuration_inputs": {
                        "analysis_config": treatment_analysis["id"],
                        "feature_semantics": semantics["id"],
                        "causal_design": design["id"],
                    },
                    "graph_inputs": {"causal_graph": graph_version["id"]},
                    "parameters": {
                        "estimand": "ATE",
                        "covariates": ["covariate"],
                        "effect_methods": ["diff_in_means", "g_computation_ate"],
                        "conditioning": {
                            "missing_values": "complete_case",
                            "categorical_encoding": "ordinal",
                            "standardize": True,
                        },
                    },
                }
            ],
        },
    )
    assert treatment_run.status_code == 202, treatment_run.text
    treatment_run_id = treatment_run.json()["id"]
    for _ in range(3):
        worker.run_once()
        treatment_status = client.get(
            f"/api/v1/runs/{treatment_run_id}"
        ).json()["status"]
        if treatment_status in {"SUCCEEDED", "FAILED"}:
            break
    assert treatment_status == "SUCCEEDED"
    treatment_results = client.get(
        f"/api/v1/runs/{treatment_run_id}/results"
    ).json()
    treatment_result = client.get(treatment_results["items"][0]["url"]).json()
    assert treatment_result["estimand"] == "ATE"
    assert treatment_result["causal_graph_version_id"] == graph_version["id"]
    assert treatment_result["selected_adjustment_variables"][0]["feature_name"] == "covariate"

    with app.state.database.session() as session:
        from causal_atelier.infrastructure.persistence import models as m

        stage_id = completed["stages"][0]["id"]
        requested = session.get(m.StageRunInputPreparation, stage_id)
        actual = session.get(
            m.StageAttemptInputPreparation,
            completed["stages"][0]["selected_attempt_id"],
        )
        assert requested.input_mode == "ANALYSIS_READY"
        assert actual.status == "SUCCEEDED"
        assert actual.resolved_preparation_artifact_id


def _published_configuration(
    client: TestClient,
    project_id: str,
    configuration_type: str,
    slug: str,
    document: dict,
) -> dict:
    configuration_response = client.post(
        "/api/v1/configurations",
        json={
            "project_id": project_id,
            "configuration_type": configuration_type,
            "slug": slug,
            "name": slug.replace("-", " ").title(),
        },
    )
    assert configuration_response.status_code == 201
    configuration = configuration_response.json()
    version_response = client.post(
        f"/api/v1/configurations/{configuration['id']}/versions",
        json={"canonical_json": document},
    )
    assert version_response.status_code == 201, version_response.text
    version = version_response.json()
    assert version["validation_status"] == "VALID", version["validation_summary"]
    published = client.post(f"/api/v1/configuration-versions/{version['id']}/publish")
    assert published.status_code == 200, published.text
    return published.json()
