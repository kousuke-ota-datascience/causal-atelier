from __future__ import annotations

import pytest


async def _project(client, name: str) -> str:  # type: ignore[no-untyped-def]
    response = await client.post("/api/v1/projects", json={"name": name})
    assert response.status_code == 201
    return response.json()["project_id"]


async def _dataset(client, project_id: str, key: str) -> str:  # type: ignore[no-untyped-def]
    response = await client.post(
        f"/api/v1/projects/{project_id}/dataset-versions",
        files={"file": ("data.csv", b"score,converted\n1,0\n2,1\n", "text/csv")},
        data={"dataset_key": key, "version_label": "v1", "name": key},
        headers={"Idempotency-Key": f"g4-{key}"},
    )
    assert response.status_code == 201
    return response.json()["dataset_version_id"]


async def _fixed_context(client, project_id: str) -> str:  # type: ignore[no-untyped-def]
    response = await client.post(
        f"/api/v1/projects/{project_id}/research-contexts",
        json={
            "context_key": "prediction",
            "problem_statement": "Predict conversion before outreach.",
            "research_questions": ["Who will convert?"],
        },
    )
    context_id = response.json()["research_context_version_id"]
    fixed = await client.post(
        f"/api/v1/projects/{project_id}/research-contexts/{context_id}/fix"
    )
    assert fixed.status_code == 200
    return context_id


def _specification(
    context_id: str, dataset_id: str, family_spec: dict,
) -> dict[str, object]:  # type: ignore[type-arg]
    return {
        "schema_version": "analysis-specification/1",
        "specification_key": "conversion-model",
        "analysis_family": "PREDICTIVE",
        "research_context_version_id": context_id,
        "dataset_version_id": dataset_id,
        "analysis_view_id": None,
        "analysis_mode": "CONFIRMATORY",
        "family_spec_schema_version": "predictive-analysis-spec/1",
        "family_spec": family_spec,
        "warnings": [],
    }


@pytest.mark.anyio
@pytest.mark.requirement("G4-ANALYSIS-SPECIFICATION-LIFECYCLE")
async def test_common_analysis_specification_validate_fix_and_revise(
    client, predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    project_id = await _project(client, "G4 Specification")
    dataset_id = await _dataset(client, project_id, "spec-data")
    context_id = await _fixed_context(client, project_id)
    created = await client.post(
        f"/api/v1/projects/{project_id}/analysis-specifications",
        json=_specification(context_id, dataset_id, predictive_spec_factory()),
        headers={"X-User-Id": "analyst"},
    )
    assert created.status_code == 201
    draft = created.json()
    assert draft["status"] == "DRAFT"
    assert draft["analysis_family"] == "PREDICTIVE"
    specification_id = draft["analysis_specification_id"]

    validated = await client.post(
        f"/api/v1/projects/{project_id}/analysis-specifications/"
        f"{specification_id}/validate"
    )
    assert validated.status_code == 200
    assert validated.json()["valid"] is True

    fixed = await client.post(
        f"/api/v1/projects/{project_id}/analysis-specifications/"
        f"{specification_id}/fix"
    )
    assert fixed.status_code == 200
    assert fixed.json()["status"] == "FIXED"
    assert len(fixed.json()["canonical_hash"]) == 64

    immutable = await client.patch(
        f"/api/v1/projects/{project_id}/analysis-specifications/{specification_id}",
        json={"analysis_mode": "EXPLORATORY"},
    )
    assert immutable.status_code == 409
    assert immutable.json()["error"]["code"] == "RESOURCE_IMMUTABLE"

    revised_family_spec = predictive_spec_factory()
    revised_family_spec["prediction_question"]["intended_use"] = "rank outreach"
    revised = await client.post(
        f"/api/v1/projects/{project_id}/analysis-specifications/"
        f"{specification_id}/revise",
        json={
            "change_reason": "Clarify intended use",
            "changes": {"family_spec": revised_family_spec},
        },
    )
    assert revised.status_code == 201
    assert revised.json()["status"] == "DRAFT"
    assert revised.json()["version_number"] == 2
    assert (
        revised.json()["revision_context"]["base_analysis_specification_id"]
        == specification_id
    )

    usage = await client.get(
        f"/api/v1/projects/{project_id}/research-contexts/{context_id}/usage"
    )
    assert set(usage.json()["analysis_specification_ids"]) == {
        specification_id,
        revised.json()["analysis_specification_id"],
    }


@pytest.mark.anyio
@pytest.mark.requirement("G4-ANALYSIS-SPECIFICATION-VALIDATION")
async def test_specification_rejects_foreign_dataset_and_test_selection(
    client, predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    project_id = await _project(client, "Local")
    foreign_project_id = await _project(client, "Foreign")
    context_id = await _fixed_context(client, project_id)
    foreign_dataset_id = await _dataset(client, foreign_project_id, "foreign-data")
    foreign = await client.post(
        f"/api/v1/projects/{project_id}/analysis-specifications",
        json=_specification(context_id, foreign_dataset_id, predictive_spec_factory()),
    )
    assert foreign.status_code == 404

    local_dataset_id = await _dataset(client, project_id, "local-data")
    leaking_spec = predictive_spec_factory()
    leaking_spec["tuning_spec"] = {"selection_partitions": ["TRAIN", "TEST"]}
    draft = await client.post(
        f"/api/v1/projects/{project_id}/analysis-specifications",
        json=_specification(context_id, local_dataset_id, leaking_spec),
    )
    assert draft.status_code == 201
    rejected = await client.post(
        f"/api/v1/projects/{project_id}/analysis-specifications/"
        f"{draft.json()['analysis_specification_id']}/fix"
    )
    assert rejected.status_code == 422
    assert rejected.json()["error"]["code"] == "TEST_ISOLATION_VIOLATION"
