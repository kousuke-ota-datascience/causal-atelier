from __future__ import annotations

import pandas as pd
import pytest

from ariadne.capabilities.exploratory.view_compiler import AnalysisViewCompiler
from ariadne.product.domain.errors import InvalidSchema


def view_spec(dataset_id: str = "dataset") -> dict:  # type: ignore[type-arg]
    return {
        "schema_version": "analysis-view/1",
        "source_dataset_version_id": dataset_id,
        "row_filter": [{"column": "group", "operator": "IN", "value": ["A", "B"]}],
        "selected_columns": ["group", "date", "sales", "units", "unit_price"],
        "derived_columns": [{
            "name": "unit_price",
            "expression": {
                "operator": "DIVIDE",
                "left": {"column": "sales"},
                "right": {"column": "units"},
            },
        }],
        "missing_value_policy": {
            "default": "KEEP",
            "columns": {"sales": {"strategy": "FILL_MEAN"}},
        },
        "time_cutoff": {"column": "date", "operator": "LTE", "value": "2026-01-03"},
        "sampling": None,
    }


@pytest.mark.requirement("FR-014", "FR-015", "FR-017", "FR-022", "NFR-003")
def test_analysis_view_compilation_is_reproducible_and_manifested() -> None:
    frame = pd.DataFrame({
        "group": ["A", "B", "C", "A"],
        "date": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"],
        "sales": [10.0, None, 30.0, 40.0],
        "units": [2, 4, 5, 8],
    })
    compiler = AnalysisViewCompiler()
    schema = {"group": "TEXT", "date": "TEXT", "sales": "REAL", "units": "INTEGER"}
    first = compiler.compile(frame, schema, view_spec(), source_dataset_content_hash="source-hash")
    second = compiler.compile(frame, schema, view_spec(), source_dataset_content_hash="source-hash")
    assert first.materialized_hash == second.materialized_hash
    assert first.manifest == second.manifest
    records = first.frame.to_dict(orient="records")
    assert records[0] == {
        "group": "A", "date": "2026-01-01", "sales": 10.0, "units": 2, "unit_price": 5.0,
    }
    assert {key: records[1][key] for key in ("group", "date", "sales", "units")} == {
        "group": "B", "date": "2026-01-02", "sales": 10.0, "units": 4,
    }
    assert pd.isna(records[1]["unit_price"])
    assert first.manifest["view_spec"] == view_spec()
    assert first.manifest["source_dataset_content_hash"] == "source-hash"


@pytest.mark.requirement("FR-015", "FR-022")
def test_analysis_view_rejects_unknown_or_non_deterministic_expressions_and_empty_population() -> None:
    compiler = AnalysisViewCompiler()
    frame = pd.DataFrame({"x": [1, 2]})
    schema = {"x": "INTEGER"}
    spec = {
        "schema_version": "analysis-view/1", "source_dataset_version_id": "d",
        "row_filter": [], "selected_columns": ["x"], "derived_columns": [],
        "missing_value_policy": {}, "time_cutoff": None, "sampling": None,
    }
    with pytest.raises(InvalidSchema):
        compiler.validate(schema, {**spec, "derived_columns": [{
            "name": "bad", "expression": {"function": "CURRENT_TIME", "args": []},
        }]})
    with pytest.raises(InvalidSchema, match="ANALYSIS_VIEW_EMPTY"):
        compiler.compile(
            frame, schema,
            {**spec, "row_filter": [{"column": "x", "operator": "GT", "value": 100}]},
            source_dataset_content_hash="hash",
        )


async def _project_dataset(client):  # type: ignore[no-untyped-def]
    project = (await client.post("/api/v1/projects", json={"name": "E3 View"})).json()
    response = await client.post(
        f"/api/v1/projects/{project['project_id']}/dataset-versions",
        files={"file": ("data.csv", b"group,date,sales,units\nA,2026-01-01,10,2\nB,2026-01-02,,4\n", "text/csv")},
        data={"dataset_key": "view", "version_label": "v1", "name": "view"},
        headers={"Idempotency-Key": "e3-view"},
    )
    assert response.status_code == 201
    return project, response.json()


@pytest.mark.anyio
@pytest.mark.requirement("FR-014", "FR-016", "FR-017")
async def test_analysis_view_api_lifecycle_is_versioned_and_fixed_is_immutable(client) -> None:  # type: ignore[no-untyped-def]
    project, dataset = await _project_dataset(client)
    project_id, dataset_id = project["project_id"], dataset["dataset_version_id"]
    created = await client.post(f"/api/v1/projects/{project_id}/analysis-views", json={
        "view_key": "eligible", "name": "Eligible rows", "spec": view_spec(dataset_id),
    })
    assert created.status_code == 201
    view_id = created.json()["analysis_view_id"]
    validation = await client.post(f"/api/v1/projects/{project_id}/analysis-views/{view_id}/validate")
    assert validation.status_code == 200 and validation.json()["valid"] is True
    fixed = await client.post(f"/api/v1/projects/{project_id}/analysis-views/{view_id}/fix")
    assert fixed.status_code == 200
    assert fixed.json()["status"] == "FIXED"
    assert fixed.json()["content_hash"] and fixed.json()["manifest"]["materialized_hash"]
    immutable = await client.patch(
        f"/api/v1/projects/{project_id}/analysis-views/{view_id}", json={"name": "changed"}
    )
    assert immutable.status_code == 409
    assert immutable.json()["error"]["code"] == "RESOURCE_IMMUTABLE"
    second = await client.post(f"/api/v1/projects/{project_id}/analysis-views", json={
        "view_key": "eligible", "name": "Eligible rows v2", "spec": view_spec(dataset_id),
    })
    assert second.json()["version_number"] == 2
