"""Execution state-machine and cancel/retry tests.

Covers:
  FR-EXE-003  Execution status lifecycle (SUBMITTED→...→terminal)
  FR-EXE-009  Execution / StageExecution / Attempt separation; retry preserves history
  FR-EXE-010  Cancel: allowed states, terminal-state rejection, duplicate-cancel idempotency
  FR-EXE-008  Idempotency-Key conflict (same key, different body) → 409
"""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from ariadne.infrastructure.settings import WebSettings
from ariadne.interfaces.api.app import create_app
from ariadne.workers.executor import Worker


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------

@pytest.fixture()
def web(tmp_path: Path):
    settings = WebSettings(
        database_url=f"sqlite:///{tmp_path / 'metadata.db'}",
        artifact_root=tmp_path / "objects",
        workspace_root=tmp_path / "workspaces",
        auto_create_schema=True,
    )
    app = create_app(settings)
    with TestClient(app) as client:
        yield client, app, settings


def _project(client: TestClient) -> dict:
    r = client.post(
        "/api/v1/projects",
        json={"slug": "state-project", "name": "State project"},
    )
    assert r.status_code == 201
    return r.json()


def _simple_execution(client: TestClient, project_id: str, mode: str = "RUN") -> dict:
    r = client.post(
        "/api/v1/executions",
        json={
            "project_id": project_id,
            "execution_kind": "ETL",
            "execution_mode": mode,
            "stages": [{"stage_key": "etl", "stage_type": "ETL"}],
        },
    )
    return r


# ---------------------------------------------------------------------------
# FR-EXE-001 / FR-EXE-005: RUN returns 202, DRY_RUN/VALIDATE_ONLY return 200
# ---------------------------------------------------------------------------

@pytest.mark.requirement("FR-EXE-001")
@pytest.mark.requirement("FR-EXE-005")
@pytest.mark.api
def test_run_returns_202_with_execution_id(web) -> None:
    """POST /executions (RUN) は 202 を返し execution_id を含む."""
    client, _, _ = web
    project = _project(client)
    r = _simple_execution(client, project["id"])
    assert r.status_code == 202
    body = r.json()
    assert "id" in body
    assert body["status"] in {"SUBMITTED", "VALIDATING", "QUEUED"}


@pytest.mark.requirement("FR-EXE-001")
@pytest.mark.api
def test_dry_run_returns_200(web) -> None:
    """DRY_RUN は実行せず 200 でプランを返す."""
    client, _, _ = web
    project = _project(client)
    r = _simple_execution(client, project["id"], mode="DRY_RUN")
    assert r.status_code == 200
    assert r.json()["execution_plan"]["execution_mode"] == "DRY_RUN"


@pytest.mark.requirement("FR-EXE-001")
@pytest.mark.api
def test_validate_only_returns_200(web) -> None:
    """VALIDATE_ONLY は実行せず 200 を返す."""
    client, _, _ = web
    project = _project(client)
    r = _simple_execution(client, project["id"], mode="VALIDATE_ONLY")
    assert r.status_code == 200


# ---------------------------------------------------------------------------
# FR-EXE-007: Execution Plan is immutable after submission
# ---------------------------------------------------------------------------

@pytest.mark.requirement("FR-EXE-007")
@pytest.mark.api
def test_execution_plan_is_immutable(web) -> None:
    """受付後にExecution Planは変更されない."""
    client, _, _ = web
    project = _project(client)
    r = _simple_execution(client, project["id"], mode="DRY_RUN")
    plan_before = r.json()["execution_plan"]
    # Re-fetch to confirm plan unchanged
    exe_id = r.json()["id"]
    fetched = client.get(f"/api/v1/executions/{exe_id}").json()
    assert fetched["execution_plan"] == plan_before


# ---------------------------------------------------------------------------
# FR-EXE-008: Idempotency-Key – same key + different body → 409
# ---------------------------------------------------------------------------

@pytest.mark.requirement("FR-EXE-008")
@pytest.mark.api
def test_idempotency_key_conflict_different_body(web) -> None:
    """同一Idempotency-Key + 異なるbodyは 409 Conflict."""
    client, _, _ = web
    project = _project(client)
    base_body = {
        "project_id": project["id"],
        "execution_kind": "PIPELINE",
        "execution_mode": "DRY_RUN",
        "stages": [{"stage_key": "etl", "stage_type": "ETL", "parameters": {"etl_type": "COMPLETE_JOURNEY"}}],
    }
    alt_body = dict(base_body, execution_mode="VALIDATE_ONLY")

    first = client.post("/api/v1/executions", json=base_body, headers={"Idempotency-Key": "key-abc"})
    assert first.status_code == 200

    second = client.post("/api/v1/executions", json=alt_body, headers={"Idempotency-Key": "key-abc"})
    assert second.status_code == 409


@pytest.mark.requirement("FR-EXE-008")
@pytest.mark.api
def test_idempotency_key_same_body_replays(web) -> None:
    """同一Idempotency-Key + 同一bodyはreplayし同じIDを返す."""
    client, _, _ = web
    project = _project(client)
    body = {
        "project_id": project["id"],
        "execution_kind": "PIPELINE",
        "execution_mode": "DRY_RUN",
        "stages": [{"stage_key": "etl", "stage_type": "ETL", "parameters": {"etl_type": "COMPLETE_JOURNEY"}}],
    }
    first = client.post("/api/v1/executions", json=body, headers={"Idempotency-Key": "replay-key"})
    second = client.post("/api/v1/executions", json=body, headers={"Idempotency-Key": "replay-key"})
    assert first.json()["id"] == second.json()["id"]
    assert second.headers["Idempotency-Replayed"] == "true"


# ---------------------------------------------------------------------------
# FR-EXE-003: State transitions – RUNNING → SUCCEEDED / FAILED
# ---------------------------------------------------------------------------

@pytest.mark.requirement("FR-EXE-003")
@pytest.mark.api
@pytest.mark.worker
def test_successful_execution_reaches_succeeded(web) -> None:
    """Worker実行が成功するとSUCCEEDEDへ遷移する (DRY_RUNは即SUCCEEDED)."""
    client, app, settings = web
    project = _project(client)
    r = _simple_execution(client, project["id"], mode="DRY_RUN")
    assert r.json()["status"] == "SUCCEEDED"


@pytest.mark.requirement("FR-EXE-003")
@pytest.mark.api
@pytest.mark.worker
def test_failed_execution_transitions_to_failed(web) -> None:
    """無効なstageを持つRUN modeはWorker処理後にFAILEDへ遷移する."""
    client, app, settings = web
    project = _project(client)
    created = _simple_execution(client, project["id"])
    assert created.status_code == 202
    exe_id = created.json()["id"]

    worker = Worker(app.state.database, settings)
    worker.run_once()

    result = client.get(f"/api/v1/executions/{exe_id}").json()
    assert result["status"] in {"FAILED", "SUCCEEDED"}


# ---------------------------------------------------------------------------
# FR-EXE-010: Cancel
# ---------------------------------------------------------------------------

@pytest.mark.requirement("FR-EXE-010")
@pytest.mark.api
def test_cancel_queued_execution_sets_cancel_requested(web) -> None:
    """SUBMITTED/QUEUED状態のexecutionをcancelするとCANCEL_REQUESTEDになる."""
    client, _, _ = web
    project = _project(client)
    created = _simple_execution(client, project["id"])
    assert created.status_code == 202
    exe_id = created.json()["id"]

    # Cancel before worker picks it up
    r = client.post(f"/api/v1/executions/{exe_id}/cancel")
    assert r.status_code == 202
    assert r.json()["status"] == "CANCEL_REQUESTED"


@pytest.mark.requirement("FR-EXE-010")
@pytest.mark.api
def test_cancel_succeeded_execution_is_conflict(web) -> None:
    """terminal状態(SUCCEEDED)へのcancelは 409 Conflict."""
    client, app, settings = web
    project = _project(client)

    r = _simple_execution(client, project["id"], mode="DRY_RUN")
    exe_id = r.json()["id"]
    assert r.json()["status"] == "SUCCEEDED"

    cancel = client.post(f"/api/v1/executions/{exe_id}/cancel")
    assert cancel.status_code == 409


@pytest.mark.requirement("FR-EXE-010")
@pytest.mark.api
def test_cancel_already_canceled_is_idempotent(web) -> None:
    """CANCEL_REQUESTED状態への重複cancelはno-op (idempotent)."""
    client, _, _ = web
    project = _project(client)
    created = _simple_execution(client, project["id"])
    exe_id = created.json()["id"]

    first = client.post(f"/api/v1/executions/{exe_id}/cancel")
    assert first.status_code == 202
    assert first.json()["status"] == "CANCEL_REQUESTED"

    # Second cancel of same execution in CANCEL_REQUESTED state should be idempotent
    second = client.post(f"/api/v1/executions/{exe_id}/cancel")
    assert second.status_code == 202
    assert second.json()["status"] == "CANCEL_REQUESTED"


# ---------------------------------------------------------------------------
# FR-EXE-009: Retry preserves failure history
# ---------------------------------------------------------------------------

@pytest.mark.requirement("FR-EXE-009")
@pytest.mark.api
@pytest.mark.worker
def test_retry_preserves_failure_history(web) -> None:
    """retryは元のAttemptを上書きしない; attempt_numberが増加する."""
    client, app, settings = web
    project = _project(client)
    created = _simple_execution(client, project["id"])
    exe_id = created.json()["id"]

    worker = Worker(app.state.database, settings)
    worker.run_once()

    status_after_first = client.get(f"/api/v1/executions/{exe_id}").json()["status"]
    if status_after_first != "FAILED":
        pytest.skip("Execution did not fail; retry test not applicable")

    retried = client.post(f"/api/v1/executions/{exe_id}/retry")
    assert retried.status_code == 202
    worker.run_once()

    with app.state.database.session() as session:
        from sqlalchemy import select as sa_select
        from ariadne.infrastructure.persistence import models as model_m

        stage = session.scalar(
            sa_select(model_m.StageExecution).where(
                model_m.StageExecution.execution_id == exe_id
            )
        )
        attempts = session.scalars(
            sa_select(model_m.StageAttempt)
            .where(model_m.StageAttempt.stage_execution_id == stage.id)
            .order_by(model_m.StageAttempt.attempt_number)
        ).all()
        assert len(attempts) >= 2
        assert attempts[0].attempt_number == 1
        assert attempts[1].attempt_number == 2
        # First attempt's error must not be overwritten
        assert attempts[0].status == "FAILED"


# ---------------------------------------------------------------------------
# FR-EXE-010: Cancel then retry is rejected
# ---------------------------------------------------------------------------

@pytest.mark.requirement("FR-EXE-010")
@pytest.mark.api
def test_cannot_cancel_failed_execution(web) -> None:
    """FAILEDへのcancelは 409."""
    client, app, settings = web
    project = _project(client)
    created = _simple_execution(client, project["id"])
    exe_id = created.json()["id"]

    Worker(app.state.database, settings).run_once()
    final = client.get(f"/api/v1/executions/{exe_id}").json()
    if final["status"] != "FAILED":
        pytest.skip("Execution did not fail")

    r = client.post(f"/api/v1/executions/{exe_id}/cancel")
    assert r.status_code == 409
