"""Dataset version router."""

from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import APIRouter, File, Form, Header, UploadFile

from ariadne.interfaces.web_api.dependencies import ProjectDataServiceDep
from ariadne.interfaces.web_api.schemas import (
    DatasetVersionListResponse,
    DatasetVersionResponse,
    DatasetPreviewResponse,
)
from ariadne.interfaces.web_api.dependencies import IdempotencyServiceDep
from ariadne.product.application.project_data_service import RegisterDatasetVersionCommand
from ariadne.product.domain.dataset_version import DatasetVersion

router = APIRouter(tags=["dataset-versions"])


def _dsv_to_response(dv: DatasetVersion) -> DatasetVersionResponse:
    return DatasetVersionResponse(
        dataset_version_id=dv.dataset_version_id,
        project_id=dv.project_id,
        source_artifact_id=dv.source_artifact_id,
        dataset_key=dv.dataset_key,
        name=dv.name,
        version_label=dv.version_label,
        content_hash=dv.content_hash,
        schema=dv.schema_json,
        profile_summary=dv.profile_summary_json,
        row_count=dv.row_count,
        column_count=dv.column_count,
        source_note=dv.source_note,
        created_at=dv.created_at,
    )


@router.post("/projects/{project_id}/dataset-versions", status_code=201, response_model=DatasetVersionResponse)
async def register_dataset_version(
    project_id: str,
    dataset_key: str = Form(...),
    name: str = Form(...),
    version_label: str = Form(...),
    source_note: str | None = Form(None),
    file: UploadFile = File(...),
    svc: ProjectDataServiceDep = ...,
    idempotency: IdempotencyServiceDep = ...,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
) -> DatasetVersionResponse:
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename or "data.parquet").suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = Path(tmp.name)

    try:
        import pandas as pd
        suffix = tmp_path.suffix.lower()
        if suffix == ".parquet":
            df = pd.read_parquet(tmp_path)
        else:
            df = pd.read_csv(tmp_path)

        schema_json = {col: _product_column_type(df[col]) for col in df.columns}
        row_count = len(df)
        column_count = len(df.columns)

        payload = {"dataset_key": dataset_key, "name": name, "version_label": version_label,
                   "source_note": source_note, "content": __import__("hashlib").sha256(tmp_path.read_bytes()).hexdigest()}
        response = idempotency.execute(
            project_id=project_id, scope="dataset-version", key=idempotency_key, payload=payload,
            command=lambda: _dsv_to_response(svc.register_dataset_version(RegisterDatasetVersionCommand(
                project_id=project_id, dataset_key=dataset_key, name=name,
                version_label=version_label, source_path=tmp_path, schema_json=schema_json,
                row_count=row_count, column_count=column_count, source_note=source_note,
            ))).model_dump(mode="json"),
        )
    finally:
        tmp_path.unlink(missing_ok=True)

    return DatasetVersionResponse.model_validate(response)


def _product_column_type(series: object) -> str:
    """Normalize dataframe storage types before crossing into Product Domain."""
    import pandas as pd

    dtype = getattr(series, "dtype", None)
    if pd.api.types.is_bool_dtype(dtype):
        return "BOOLEAN"
    if pd.api.types.is_integer_dtype(dtype):
        return "INTEGER"
    if pd.api.types.is_float_dtype(dtype):
        return "REAL"
    if pd.api.types.is_datetime64_any_dtype(dtype):
        return "DATETIME"
    if pd.api.types.is_string_dtype(dtype) or pd.api.types.is_object_dtype(dtype):
        return "TEXT"
    return "OTHER"


@router.get("/projects/{project_id}/dataset-versions", response_model=DatasetVersionListResponse)
async def list_dataset_versions(
    project_id: str,
    svc: ProjectDataServiceDep,
) -> DatasetVersionListResponse:
    items = svc.list_dataset_versions(project_id)
    return DatasetVersionListResponse(items=[_dsv_to_response(dv) for dv in items])


@router.get("/dataset-versions/{dataset_version_id}", response_model=DatasetVersionResponse)
async def get_dataset_version(dataset_version_id: str, svc: ProjectDataServiceDep) -> DatasetVersionResponse:
    return _dsv_to_response(svc.get_dataset_version(dataset_version_id))


@router.get("/dataset-versions/{dataset_version_id}/preview", response_model=DatasetPreviewResponse)
async def preview_dataset(dataset_version_id: str, svc: ProjectDataServiceDep, limit: int = 20) -> DatasetPreviewResponse:
    return DatasetPreviewResponse.model_validate(svc.get_dataset_preview(dataset_version_id, limit))
