from __future__ import annotations

from sqlalchemy import select
import pytest

from ariadne.interfaces.web_api import dependencies
from ariadne.product.persistence.orm_models import (
    ExecutionOrm,
    FamilyExecutionOrm,
    StageExecutionOrm,
)


@pytest.mark.anyio
async def test_g05_exploratory_product_submission_uses_only_canonical_execution(client) -> None:  # type: ignore[no-untyped-def]
    project_id = (await client.post("/api/v1/projects", json={"name": "G05 exploration"})).json()["project_id"]
    dataset = await client.post(
        f"/api/v1/projects/{project_id}/dataset-versions",
        files={"file": ("data.csv", b"group,value\na,1\nb,2\n", "text/csv")},
        data={"dataset_key": "g05", "version_label": "v1", "name": "G05"},
        headers={"Idempotency-Key": "g05-exploratory"},
    )
    response = await client.post(
        f"/api/v1/projects/{project_id}/exploration/executions",
        json={
            "dataset_version_id": dataset.json()["dataset_version_id"],
            "analysis_view_id": None,
            "family_spec": {
                "schema_version": "exploratory-analysis-spec/1",
                "operation": "PROFILE", "columns": ["value"],
            },
        },
    )
    assert response.status_code == 202
    execution_id = response.json()["execution_id"]

    with dependencies._get_session_factory()() as session:
        execution = session.get(ExecutionOrm, execution_id)
        assert execution is not None
        assert execution.analysis_family == "EXPLORATORY"
        assert list(session.scalars(select(StageExecutionOrm).where(
            StageExecutionOrm.execution_id == execution_id
        )))
        assert session.get(FamilyExecutionOrm, execution_id) is None
