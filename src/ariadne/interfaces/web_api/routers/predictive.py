"""G3 Predictive specification and split-validation API."""

from __future__ import annotations

from typing import Any, Literal

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

from ariadne.interfaces.web_api.dependencies import PredictiveSplitServiceDep

router = APIRouter(tags=["predictive"])


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class PredictiveSplitRequest(StrictModel):
    dataset_version_id: str
    analysis_view_id: str | None = None
    family_spec: dict[str, Any]


class PartitionArtifactResponse(StrictModel):
    artifact_id: str
    schema_version: Literal["partition-artifact/1"]
    content_hash: str
    size_bytes: int
    selection_contract: dict[str, Any]


class PredictiveSplitResponse(StrictModel):
    schema_version: Literal["predictive-split-validation/1"]
    status: Literal["VALID"]
    execution_id: str
    task_type: str
    strategy: str
    partition_counts: dict[str, int]
    partition_artifact: PartitionArtifactResponse
    source_snapshot: dict[str, Any]


@router.get("/projects/{project_id}/predictive/capabilities")
async def predictive_capabilities(project_id: str) -> dict[str, Any]:
    return {
        "schema_version": "predictive-capabilities/1",
        "gate": "G3_SPLIT_ONLY",
        "task_types": ["BINARY_CLASSIFICATION", "REGRESSION"],
        "split_strategies": ["RANDOM", "STRATIFIED", "GROUP", "TIME_BASED"],
        "metrics": {
            "BINARY_CLASSIFICATION": [
                "ROC_AUC", "PR_AUC", "LOG_LOSS", "BRIER", "ACCURACY", "F1",
            ],
            "REGRESSION": ["MAE", "RMSE", "R2"],
        },
        "training_available": False,
    }


@router.post(
    "/projects/{project_id}/predictive/split-validations",
    response_model=PredictiveSplitResponse,
    status_code=201,
)
async def validate_predictive_split(
    project_id: str,
    body: PredictiveSplitRequest,
    svc: PredictiveSplitServiceDep,
) -> PredictiveSplitResponse:
    return PredictiveSplitResponse.model_validate(svc.validate_and_save(
        project_id,
        dataset_version_id=body.dataset_version_id,
        analysis_view_id=body.analysis_view_id,
        family_spec=body.family_spec,
    ))


@router.get("/projects/{project_id}/predictive/partition-artifacts/{artifact_id}")
async def get_partition_artifact(
    project_id: str,
    artifact_id: str,
    svc: PredictiveSplitServiceDep,
) -> dict[str, Any]:
    artifact = svc.get_partition_artifact(project_id, artifact_id)
    return {
        "artifact_id": artifact.artifact_id,
        "execution_id": artifact.execution_id,
        "artifact_type": artifact.artifact_type,
        "schema_version": artifact.schema_version,
        "content_hash": artifact.content_hash,
        "size_bytes": artifact.size_bytes,
        "metadata": artifact.metadata_json,
    }
