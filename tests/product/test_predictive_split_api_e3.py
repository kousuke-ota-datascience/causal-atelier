from __future__ import annotations

import pytest
from sqlalchemy import select

from ariadne.interfaces.web_api import dependencies
from ariadne.product.persistence.orm_models import FamilyExecutionOrm


@pytest.mark.anyio
@pytest.mark.requirement("FR-058", "FR-059", "FR-064", "FR-073", "AR-019")
async def test_retired_split_validation_api_explicitly_rejects_legacy_lifecycle_write(
    client, predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    response = await client.post(
        "/api/v1/projects/not-used/predictive/split-validations",
        json={
            "dataset_version_id": "not-used",
            "analysis_view_id": None,
            "family_spec": predictive_spec_factory(),
        },
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "DOMAIN_ERROR"
    assert "PredictiveSplitService.validate_and_save" in response.json()["error"]["message"]


@pytest.mark.anyio
@pytest.mark.requirement("FR-058", "FR-059", "NFR-005")
async def test_retired_split_validation_api_does_not_persist_legacy_execution_on_invalid_input(
    client, predictive_spec_factory,
) -> None:  # type: ignore[no-untyped-def]
    project_id = (await client.post(
        "/api/v1/projects", json={"name": "Predictive error contract"}
    )).json()["project_id"]
    dataset = await client.post(
        f"/api/v1/projects/{project_id}/dataset-versions",
        files={"file": (
            "small.csv",
            b"score,converted\n0.1,0\n0.2,1\n0.3,0\n0.4,1\n",
            "text/csv",
        )},
        data={"dataset_key": "small", "version_label": "v1", "name": "small"},
        headers={"Idempotency-Key": "e3-predictive-small"},
    )
    request = {
        "dataset_version_id": dataset.json()["dataset_version_id"],
        "analysis_view_id": None,
        "family_spec": predictive_spec_factory(),
    }
    response = await client.post(
        f"/api/v1/projects/{project_id}/predictive/split-validations", json=request
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "DOMAIN_ERROR"

    factory = dependencies._get_session_factory()
    with factory() as session:
        persisted = session.scalar(select(FamilyExecutionOrm).where(
            FamilyExecutionOrm.project_id == project_id,
            FamilyExecutionOrm.analysis_family == "PREDICTIVE",
        ))
    assert persisted is None


@pytest.mark.anyio
@pytest.mark.requirement("FR-055", "FR-058", "G5-CAPABILITIES")
async def test_g5_capabilities_advertise_explanation_and_model_card(
    client,
) -> None:  # type: ignore[no-untyped-def]
    project_id = (await client.post(
        "/api/v1/projects", json={"name": "Predictive capabilities"}
    )).json()["project_id"]
    response = await client.get(f"/api/v1/projects/{project_id}/predictive/capabilities")
    assert response.status_code == 200
    assert response.json()["gate"] == "G5_EXPLAIN_UI"
    assert response.json()["training_available"] is True
    assert response.json()["evaluation_available"] is True
    assert response.json()["explanation_available"] is True
    assert response.json()["model_card_available"] is True
    assert response.json()["model_registry"]
    assert response.json()["explanation_methods"] == [{
        "method": "LINEAR_COEFFICIENT_CONTRIBUTION",
        "supported_models": [
            "logistic_regression.v1",
            "linear_regression.v1",
        ],
        "supports_global": True,
        "supports_local": True,
        "model_output_scales": ["LOG_ODDS", "PREDICTION"],
    }]
    assert "PR_AUC" in response.json()["metrics"]["BINARY_CLASSIFICATION"]
