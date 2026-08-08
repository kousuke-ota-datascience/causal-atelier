from __future__ import annotations

import pytest


async def _project(client, name: str) -> str:  # type: ignore[no-untyped-def]
    response = await client.post("/api/v1/projects", json={"name": name})
    assert response.status_code == 201
    return response.json()["project_id"]


def _context_payload(key: str = "retention") -> dict[str, object]:
    return {
        "context_key": key,
        "problem_statement": "Identify customers at risk before renewal.",
        "research_questions": ["Who is likely not to renew?"],
        "significance": "Supports proactive retention decisions.",
        "hypotheses": ["Lower engagement is associated with non-renewal."],
        "decision_context": {"decision": "prioritize outreach"},
        "relations": [],
    }


@pytest.mark.anyio
@pytest.mark.requirement("G4-RESEARCH-CONTEXT-LIFECYCLE")
async def test_research_context_versions_are_fixed_immutable_and_usage_queryable(
    client,
) -> None:  # type: ignore[no-untyped-def]
    project_id = await _project(client, "G4 Context")
    created = await client.post(
        f"/api/v1/projects/{project_id}/research-contexts",
        json=_context_payload(),
        headers={"X-User-Id": "researcher"},
    )
    assert created.status_code == 201
    draft = created.json()
    assert draft["status"] == "DRAFT"
    assert draft["version_number"] == 1
    assert draft["canonical_hash"] is None
    context_id = draft["research_context_version_id"]

    patched = await client.patch(
        f"/api/v1/projects/{project_id}/research-contexts/{context_id}",
        json={"research_questions": ["Which eligible customers will not renew?"]},
    )
    assert patched.status_code == 200

    fixed = await client.post(
        f"/api/v1/projects/{project_id}/research-contexts/{context_id}/fix"
    )
    assert fixed.status_code == 200
    assert fixed.json()["status"] == "FIXED"
    assert len(fixed.json()["canonical_hash"]) == 64

    immutable = await client.patch(
        f"/api/v1/projects/{project_id}/research-contexts/{context_id}",
        json={"problem_statement": "mutated"},
    )
    assert immutable.status_code == 409
    assert immutable.json()["error"]["code"] == "RESOURCE_IMMUTABLE"

    version_two = await client.post(
        f"/api/v1/projects/{project_id}/research-contexts",
        json=_context_payload(),
    )
    assert version_two.status_code == 201
    assert version_two.json()["version_number"] == 2
    listed = await client.get(f"/api/v1/projects/{project_id}/research-contexts")
    assert [item["version_number"] for item in listed.json()["items"]] == [2, 1]

    usage = await client.get(
        f"/api/v1/projects/{project_id}/research-contexts/{context_id}/usage"
    )
    assert usage.status_code == 200
    assert usage.json()["analysis_specification_ids"] == []
    assert usage.json()["execution_ids"] == []


@pytest.mark.anyio
@pytest.mark.requirement("G4-PROJECT-BOUNDARY")
async def test_research_context_relation_cannot_cross_project(client) -> None:  # type: ignore[no-untyped-def]
    first_project = await _project(client, "First")
    second_project = await _project(client, "Second")
    foreign = await client.post(
        f"/api/v1/projects/{second_project}/research-contexts",
        json=_context_payload("foreign"),
    )
    foreign_id = foreign.json()["research_context_version_id"]
    payload = _context_payload("local")
    payload["relations"] = [{
        "relation_type": "RELATED_TO",
        "target_context_version_id": foreign_id,
    }]
    local = await client.post(
        f"/api/v1/projects/{first_project}/research-contexts", json=payload
    )
    response = await client.post(
        f"/api/v1/projects/{first_project}/research-contexts/"
        f"{local.json()['research_context_version_id']}/fix"
    )
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "ENTITY_NOT_FOUND"
