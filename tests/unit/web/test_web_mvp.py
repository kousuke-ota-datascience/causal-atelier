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
