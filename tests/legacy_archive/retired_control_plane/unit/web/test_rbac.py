"""RBAC and project-boundary tests.

Covers:
  FR-PRJ-001  Project logical-delete (Admin only)
  FR-PRJ-002  Resources belong to Projects
  FR-PRJ-003  Viewer / Analyst / Maintainer / Project Admin roles
  FR-PRJ-004  API enforces tenant boundary and project permissions
"""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from ariadne.domain import metadata as m
from ariadne.infrastructure.settings import WebSettings
from ariadne.interfaces.api.app import create_app
from ariadne.workers.executor import Worker


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_app(tmp_path: Path):
    settings = WebSettings(
        database_url=f"sqlite:///{tmp_path / 'metadata.db'}",
        artifact_root=tmp_path / "objects",
        workspace_root=tmp_path / "workspaces",
        auto_create_schema=True,
    )
    app = create_app(settings)
    return app, settings


def _headers(subject: str) -> dict:
    return {"X-User-Subject": subject}


def _create_project(client: TestClient, slug: str, subject: str = "owner") -> dict:
    r = client.post(
        "/api/v1/projects",
        json={"slug": slug, "name": slug},
        headers=_headers(subject),
    )
    assert r.status_code == 201, r.text
    return r.json()


def _register_user(app, subject: str) -> str:
    """Ensure a user row exists and return its ID."""
    with app.state.database.session() as session:
        user = session.scalar(
            select(m.User).where(
                m.User.identity_provider == "development",
                m.User.external_subject == subject,
            )
        )
        if user is None:
            user = m.User(
                identity_provider="development",
                external_subject=subject,
                display_name=subject,
            )
            session.add(user)
            session.flush()
        return user.id


def _add_member(client: TestClient, project_id: str, user_id: str, role: str, admin_subject: str = "owner") -> None:
    r = client.post(
        f"/api/v1/projects/{project_id}/members",
        json={"user_id": user_id, "role": role},
        headers=_headers(admin_subject),
    )
    assert r.status_code == 201, r.text


# ---------------------------------------------------------------------------
# FR-PRJ-003 / FR-PRJ-004: RBAC role permissions
# ---------------------------------------------------------------------------

@pytest.mark.requirement("FR-PRJ-003")
@pytest.mark.requirement("FR-PRJ-004")
@pytest.mark.api
def test_project_creator_gets_project_admin_role(tmp_path: Path) -> None:
    """Project作成者がProject Adminになる."""
    app, _ = _make_app(tmp_path)
    with TestClient(app) as client:
        _create_project(client, "my-proj", subject="creator")
        projects = client.get("/api/v1/projects", headers=_headers("creator")).json()
        assert projects["items"][0]["slug"] == "my-proj"


@pytest.mark.requirement("FR-PRJ-003")
@pytest.mark.requirement("FR-PRJ-004")
@pytest.mark.api
def test_viewer_can_read_but_not_create_dataset(tmp_path: Path) -> None:
    """Viewerは読み取りのみ可能で、Datasetを登録できない."""
    app, _ = _make_app(tmp_path)
    with TestClient(app) as client:
        project = _create_project(client, "test-proj")
        viewer_id = _register_user(app, "viewer-user")
        _add_member(client, project["id"], viewer_id, "VIEWER")

        r = client.get(f"/api/v1/projects/{project['id']}", headers=_headers("viewer-user"))
        assert r.status_code == 200

        r = client.post(
            f"/api/v1/projects/{project['id']}/objects",
            files={"file": ("test.csv", b"a,b\n1,2\n", "text/csv")},
            headers=_headers("viewer-user"),
        )
        assert r.status_code == 404


@pytest.mark.requirement("FR-PRJ-003")
@pytest.mark.requirement("FR-PRJ-004")
@pytest.mark.api
def test_analyst_can_upload_but_not_delete_project(tmp_path: Path) -> None:
    """Analystはuploadできるがproject削除はできない."""
    app, _ = _make_app(tmp_path)
    with TestClient(app) as client:
        project = _create_project(client, "a-proj")
        analyst_id = _register_user(app, "analyst-user")
        _add_member(client, project["id"], analyst_id, "ANALYST")

        r = client.post(
            f"/api/v1/projects/{project['id']}/objects",
            files={"file": ("data.csv", b"x\n1\n", "text/csv")},
            headers=_headers("analyst-user"),
        )
        assert r.status_code == 201

        r = client.delete(f"/api/v1/projects/{project['id']}", headers=_headers("analyst-user"))
        assert r.status_code == 404


@pytest.mark.requirement("FR-PRJ-003")
@pytest.mark.requirement("FR-PRJ-004")
@pytest.mark.api
def test_only_project_admin_can_add_member(tmp_path: Path) -> None:
    """Project Adminのみメンバーを追加できる."""
    app, _ = _make_app(tmp_path)
    with TestClient(app) as client:
        project = _create_project(client, "mem-proj")
        maintainer_id = _register_user(app, "maintainer-user")
        _add_member(client, project["id"], maintainer_id, "MAINTAINER")

        new_user_id = _register_user(app, "brand-new-user")
        r = client.post(
            f"/api/v1/projects/{project['id']}/members",
            json={"user_id": new_user_id, "role": "VIEWER"},
            headers=_headers("maintainer-user"),
        )
        assert r.status_code == 404


@pytest.mark.requirement("FR-PRJ-003")
@pytest.mark.requirement("FR-PRJ-004")
@pytest.mark.api
def test_project_admin_can_update_project(tmp_path: Path) -> None:
    """Project Adminはprojectを更新できる."""
    app, _ = _make_app(tmp_path)
    with TestClient(app) as client:
        project = _create_project(client, "upd-proj")
        r = client.patch(
            f"/api/v1/projects/{project['id']}",
            json={"name": "Updated Name"},
            headers=_headers("owner"),
        )
        assert r.status_code == 200
        assert r.json()["name"] == "Updated Name"


@pytest.mark.requirement("FR-PRJ-003")
@pytest.mark.requirement("FR-PRJ-004")
@pytest.mark.api
def test_project_admin_can_logically_delete_project(tmp_path: Path) -> None:
    """Project Adminはprojectを論理削除できる."""
    app, _ = _make_app(tmp_path)
    with TestClient(app) as client:
        project = _create_project(client, "del-proj")

        r = client.delete(f"/api/v1/projects/{project['id']}", headers=_headers("owner"))
        assert r.status_code == 204

        r = client.get(f"/api/v1/projects/{project['id']}", headers=_headers("owner"))
        assert r.status_code == 404

        with app.state.database.session() as session:
            proj = session.get(m.Project, project["id"])
            assert proj.status == "DELETED"
            assert proj.deleted_at is not None


# ---------------------------------------------------------------------------
# FR-PRJ-002 / FR-PRJ-004: Cross-project resource boundary
# ---------------------------------------------------------------------------

@pytest.mark.requirement("FR-PRJ-002")
@pytest.mark.requirement("FR-PRJ-004")
@pytest.mark.api
def test_user_without_membership_cannot_access_project(tmp_path: Path) -> None:
    """プロジェクトメンバーでないユーザーはproject resourceにアクセスできない."""
    app, _ = _make_app(tmp_path)
    with TestClient(app) as client:
        project = _create_project(client, "private-proj", subject="owner")

        r = client.get(f"/api/v1/projects/{project['id']}", headers=_headers("outsider"))
        assert r.status_code == 404
        assert r.json()["error"]["code"] == "NOT_FOUND"


@pytest.mark.requirement("FR-PRJ-002")
@pytest.mark.requirement("FR-PRJ-004")
@pytest.mark.api
def test_user_cannot_list_datasets_of_foreign_project(tmp_path: Path) -> None:
    """別Projectのdatasetを一覧できない."""
    app, _ = _make_app(tmp_path)
    with TestClient(app) as client:
        project_a = _create_project(client, "proj-a", subject="alice")
        _create_project(client, "proj-b", subject="bob")

        r = client.get(
            f"/api/v1/datasets?project_id={project_a['id']}",
            headers=_headers("bob"),
        )
        assert r.status_code == 404


@pytest.mark.requirement("FR-PRJ-004")
@pytest.mark.api
def test_execution_create_requires_analyst_or_above(tmp_path: Path) -> None:
    """Executionの作成はANALYST以上が必要."""
    app, _ = _make_app(tmp_path)
    with TestClient(app) as client:
        project = _create_project(client, "exe-proj")
        viewer_id = _register_user(app, "viewer-only")
        _add_member(client, project["id"], viewer_id, "VIEWER")

        r = client.post(
            "/api/v1/executions",
            json={
                "project_id": project["id"],
                "execution_kind": "PIPELINE",
                "execution_mode": "DRY_RUN",
                "stages": [],
            },
            headers=_headers("viewer-only"),
        )
        assert r.status_code == 404


@pytest.mark.requirement("FR-PRJ-004")
@pytest.mark.api
def test_cancel_execution_requires_analyst_or_above(tmp_path: Path) -> None:
    """Cancel操作はANALYST以上が必要."""
    app, _ = _make_app(tmp_path)
    with TestClient(app) as client:
        project = _create_project(client, "cancel-proj")
        viewer_id = _register_user(app, "viewer-cancel")
        _add_member(client, project["id"], viewer_id, "VIEWER")

        exe = client.post(
            "/api/v1/executions",
            json={
                "project_id": project["id"],
                "execution_kind": "ETL",
                "execution_mode": "RUN",
                "stages": [{"stage_key": "etl", "stage_type": "ETL"}],
            },
            headers=_headers("owner"),
        )
        assert exe.status_code == 202
        exe_id = exe.json()["id"]

        r = client.post(
            f"/api/v1/executions/{exe_id}/cancel",
            headers=_headers("viewer-cancel"),
        )
        assert r.status_code == 404
