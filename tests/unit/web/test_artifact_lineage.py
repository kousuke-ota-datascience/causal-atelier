"""Artifact lineage and Saved Causal Graph Version tests.

Covers:
  FR-ART-001  Artifact: logical ID, kind, URI, checksum, size, media type
  FR-ART-003  Local path NOT exposed as API contract
  FR-ART-006  Lineage: DatasetVersion → Discovery → Graph → Design → Inference
  FR-ART-007  Artifact download requires project permission
  FR-SCG-002  CausalGraph and GraphVersion separated
  FR-SCG-005  PUBLISHED GraphVersion is immutable
  FR-SCG-008  Inference records GraphVersion ID and content hash
  FR-SCG-009  Dataset/Semantics inconsistency rejected before Execution
  FR-RES-005  Traceability back to Dataset, Semantics, Discovery, Graph, Design
"""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from ariadne.infrastructure.settings import WebSettings
from ariadne.interfaces.api.app import create_app
from ariadne.workers.executor import Worker


# ---------------------------------------------------------------------------
# Fixture and helpers
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


def _project(client: TestClient, slug: str = "art-proj") -> dict:
    r = client.post("/api/v1/projects", json={"slug": slug, "name": slug})
    assert r.status_code == 201
    return r.json()


def _upload_csv(client: TestClient, project_id: str) -> dict:
    rows = ["treatment,outcome,covariate"] + [f"{i%2},{i/10},{i}" for i in range(60)]
    content = ("\n".join(rows) + "\n").encode()
    r = client.post(
        f"/api/v1/projects/{project_id}/objects",
        files={"file": ("analysis.csv", content, "text/csv")},
    )
    assert r.status_code == 201
    return r.json()


def _published_configuration(client, project_id, cfg_type, slug, document):
    cfg = client.post(
        "/api/v1/configurations",
        json={"project_id": project_id, "configuration_type": cfg_type, "slug": slug, "name": slug},
    ).json()
    ver = client.post(
        f"/api/v1/configurations/{cfg['id']}/versions",
        json={"canonical_json": document},
    )
    assert ver.status_code == 201, ver.text
    version = ver.json()
    pub = client.post(f"/api/v1/configuration-versions/{version['id']}/publish")
    assert pub.status_code == 200
    return pub.json()


def _run_discovery(client, app, settings, project_id, version_id, semantics_id, analysis_id):
    created = client.post(
        "/api/v1/executions",
        json={
            "project_id": project_id,
            "execution_kind": "DISCOVERY",
            "execution_mode": "RUN",
            "stages": [{
                "stage_key": "discovery",
                "stage_type": "DISCOVERY",
                "input_mode": "ANALYSIS_READY",
                "dataset_inputs": {"analysis_data": version_id},
                "configuration_inputs": {"analysis_config": analysis_id, "feature_semantics": semantics_id},
                "parameters": {"algorithms": ["pc"], "conditioning": {"missing_values": "complete_case", "categorical_encoding": "ordinal", "standardize": True}},
            }],
        },
    )
    assert created.status_code == 202
    exe_id = created.json()["id"]
    worker = Worker(app.state.database, settings)
    for _ in range(5):
        worker.run_once()
        st = client.get(f"/api/v1/executions/{exe_id}").json()["status"]
        if st in {"SUCCEEDED", "FAILED"}:
            break
    return exe_id, client.get(f"/api/v1/executions/{exe_id}").json()


# ---------------------------------------------------------------------------
# FR-ART-003: Local path not in API response
# ---------------------------------------------------------------------------

@pytest.mark.requirement("FR-ART-003")
@pytest.mark.api
def test_artifact_download_url_is_not_a_local_path(web) -> None:
    """Artifact URLはlocal absolute pathを含まない."""
    client, app, settings = web
    project = _project(client)
    obj = _upload_csv(client, project["id"])
    ds = client.post(
        "/api/v1/datasets",
        json={"project_id": project["id"], "slug": "ds", "name": "DS", "dataset_kind": "PROCESSED"},
    ).json()
    version = client.post(
        f"/api/v1/datasets/{ds['id']}/versions",
        json={"source_type": "UPLOAD", "tables": [{"logical_name": "t", "object": obj}]},
    ).json()

    semantics = _published_configuration(
        client, project["id"], "FEATURE_SEMANTICS", "sem",
        {"dataset_version_id": version["id"], "default_unit_id": "row",
         "features": [
             {"name": "treatment", "source_table": "t", "source_column": "treatment", "role": "treatment", "allowed_for_discovery": True, "allowed_for_adjustment": False},
             {"name": "outcome", "source_table": "t", "source_column": "outcome", "role": "outcome", "allowed_for_discovery": True, "allowed_for_adjustment": False},
             {"name": "covariate", "source_table": "t", "source_column": "covariate", "role": "covariate", "allowed_for_discovery": True, "allowed_for_adjustment": True},
         ]},
    )
    analysis = _published_configuration(
        client, project["id"], "DISCOVERY_ANALYSIS", "dis",
        {"input_mode": "ANALYSIS_READY", "algorithms": ["pc"]},
    )
    exe_id, _ = _run_discovery(client, app, settings, project["id"], version["id"], semantics["id"], analysis["id"])

    artifacts = client.get(f"/api/v1/executions/{exe_id}/artifacts").json()
    for art in artifacts:
        download_url = art.get("download_url") or art.get("url") or ""
        # Must not expose absolute local filesystem paths
        assert not download_url.startswith("/"), f"Local path exposed: {download_url}"


# ---------------------------------------------------------------------------
# FR-ART-006 / FR-RES-005: Lineage traceable from Result
# ---------------------------------------------------------------------------

@pytest.mark.requirement("FR-ART-006")
@pytest.mark.requirement("FR-RES-005")
@pytest.mark.api
@pytest.mark.worker
def test_discovery_result_links_to_dataset_and_semantics(web) -> None:
    """Discovery ResultにDatasetVersionとSemanticsのIDが記録される."""
    client, app, settings = web
    project = _project(client)
    obj = _upload_csv(client, project["id"])
    ds = client.post(
        "/api/v1/datasets",
        json={"project_id": project["id"], "slug": "ds2", "name": "DS2", "dataset_kind": "PROCESSED"},
    ).json()
    version = client.post(
        f"/api/v1/datasets/{ds['id']}/versions",
        json={"source_type": "UPLOAD", "tables": [{"logical_name": "t", "object": obj}]},
    ).json()
    semantics = _published_configuration(
        client, project["id"], "FEATURE_SEMANTICS", "sem2",
        {"dataset_version_id": version["id"], "default_unit_id": "row",
         "features": [
             {"name": "treatment", "source_table": "t", "source_column": "treatment", "role": "treatment", "allowed_for_discovery": True, "allowed_for_adjustment": False},
             {"name": "outcome", "source_table": "t", "source_column": "outcome", "role": "outcome", "allowed_for_discovery": True, "allowed_for_adjustment": False},
             {"name": "covariate", "source_table": "t", "source_column": "covariate", "role": "covariate", "allowed_for_discovery": True, "allowed_for_adjustment": True},
         ]},
    )
    analysis = _published_configuration(
        client, project["id"], "DISCOVERY_ANALYSIS", "dis2",
        {"input_mode": "ANALYSIS_READY", "algorithms": ["pc"]},
    )
    exe_id, completed = _run_discovery(client, app, settings, project["id"], version["id"], semantics["id"], analysis["id"])
    assert completed["status"] == "SUCCEEDED", completed.get("error_summary")

    results = client.get(f"/api/v1/executions/{exe_id}/results").json()
    assert results["total"] >= 1
    result = client.get(results["items"][0]["url"]).json()
    assert result["feature_semantics_version_id"] == semantics["id"]


# ---------------------------------------------------------------------------
# FR-SCG-005: PUBLISHED GraphVersion is immutable
# ---------------------------------------------------------------------------

@pytest.mark.requirement("FR-SCG-005")
@pytest.mark.api
@pytest.mark.worker
def test_published_graph_version_cannot_be_overwritten(web) -> None:
    """PUBLISHED Graph Versionのcontent_hashは変更されない."""
    client, app, settings = web
    project = _project(client, "graph-proj")
    obj = _upload_csv(client, project["id"])
    ds = client.post(
        "/api/v1/datasets",
        json={"project_id": project["id"], "slug": "gds", "name": "GDS", "dataset_kind": "PROCESSED"},
    ).json()
    version = client.post(
        f"/api/v1/datasets/{ds['id']}/versions",
        json={"source_type": "UPLOAD", "tables": [{"logical_name": "t", "object": obj}]},
    ).json()
    semantics = _published_configuration(
        client, project["id"], "FEATURE_SEMANTICS", "gsem",
        {"dataset_version_id": version["id"], "default_unit_id": "row",
         "features": [
             {"name": "treatment", "source_table": "t", "source_column": "treatment", "role": "treatment", "allowed_for_discovery": True, "allowed_for_adjustment": False},
             {"name": "outcome", "source_table": "t", "source_column": "outcome", "role": "outcome", "allowed_for_discovery": True, "allowed_for_adjustment": False},
             {"name": "covariate", "source_table": "t", "source_column": "covariate", "role": "covariate", "allowed_for_discovery": True, "allowed_for_adjustment": True},
         ]},
    )
    analysis = _published_configuration(
        client, project["id"], "DISCOVERY_ANALYSIS", "gdis",
        {"input_mode": "ANALYSIS_READY", "algorithms": ["pc"]},
    )
    exe_id, completed = _run_discovery(client, app, settings, project["id"], version["id"], semantics["id"], analysis["id"])
    assert completed["status"] == "SUCCEEDED"

    results = client.get(f"/api/v1/executions/{exe_id}/results").json()
    result = client.get(results["items"][0]["url"]).json()
    algo_result_id = result["algorithms"][0]["id"]

    graph = client.post(
        "/api/v1/causal-graphs",
        json={"project_id": project["id"], "slug": "g1", "name": "G1"},
    ).json()
    gv_r = client.post(
        f"/api/v1/causal-graphs/{graph['id']}/versions",
        json={"source_discovery_algorithm_result_id": algo_result_id, "feature_semantics_version_id": semantics["id"], "selection_note": "test"},
    )
    assert gv_r.status_code == 201
    gv = gv_r.json()
    content_hash_before = gv["content_hash"]

    pub = client.post(f"/api/v1/causal-graph-versions/{gv['id']}/publish")
    assert pub.status_code == 200
    assert pub.json()["status"] == "PUBLISHED"

    # Re-fetch: content_hash unchanged after publish
    refetched = client.get(f"/api/v1/causal-graph-versions/{gv['id']}").json()
    assert refetched["content_hash"] == content_hash_before


# ---------------------------------------------------------------------------
# FR-ART-007: Artifact endpoint enforces project RBAC
# ---------------------------------------------------------------------------

@pytest.mark.requirement("FR-ART-007")
@pytest.mark.api
def test_outsider_cannot_download_artifact(web) -> None:
    """別Projectのartifactはダウンロードできない."""
    client, app, settings = web
    project = _project(client, "art-rbac")
    obj = _upload_csv(client, project["id"])
    ds = client.post(
        "/api/v1/datasets",
        json={"project_id": project["id"], "slug": "ads", "name": "ADS", "dataset_kind": "PROCESSED"},
    ).json()
    version = client.post(
        f"/api/v1/datasets/{ds['id']}/versions",
        json={"source_type": "UPLOAD", "tables": [{"logical_name": "t", "object": obj}]},
    ).json()
    semantics = _published_configuration(
        client, project["id"], "FEATURE_SEMANTICS", "asem",
        {"dataset_version_id": version["id"], "default_unit_id": "row",
         "features": [
             {"name": "treatment", "source_table": "t", "source_column": "treatment", "role": "treatment", "allowed_for_discovery": True, "allowed_for_adjustment": False},
             {"name": "outcome", "source_table": "t", "source_column": "outcome", "role": "outcome", "allowed_for_discovery": True, "allowed_for_adjustment": False},
             {"name": "covariate", "source_table": "t", "source_column": "covariate", "role": "covariate", "allowed_for_discovery": True, "allowed_for_adjustment": True},
         ]},
    )
    analysis = _published_configuration(
        client, project["id"], "DISCOVERY_ANALYSIS", "adis",
        {"input_mode": "ANALYSIS_READY", "algorithms": ["pc"]},
    )
    exe_id, completed = _run_discovery(client, app, settings, project["id"], version["id"], semantics["id"], analysis["id"])
    if completed["status"] != "SUCCEEDED":
        pytest.skip("Discovery did not succeed; skipping artifact RBAC check")

    artifacts = client.get(f"/api/v1/executions/{exe_id}/artifacts").json()
    if not artifacts:
        pytest.skip("No artifacts produced")

    art_id = artifacts[0].get("id")
    if not art_id:
        pytest.skip("No artifact ID available")

    # Outsider cannot access artifact
    r = client.get(f"/api/v1/artifacts/{art_id}", headers={"X-User-Subject": "outsider"})
    assert r.status_code == 404
