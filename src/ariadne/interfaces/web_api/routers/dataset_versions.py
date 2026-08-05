"""Dataset version router."""

from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import APIRouter, File, Form, UploadFile

from ariadne.interfaces.web_api.dependencies import ProjectDataServiceDep
from ariadne.interfaces.web_api.schemas import (
    DatasetVersionListResponse,
    DatasetVersionResponse,
)
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
        column_schema=dv.schema_json,
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

        schema_json = {col: str(dtype) for col, dtype in df.dtypes.items()}
        row_count = len(df)
        column_count = len(df.columns)

        dv = svc.register_dataset_version(RegisterDatasetVersionCommand(
            project_id=project_id,
            dataset_key=dataset_key,
            name=name,
            version_label=version_label,
            source_path=tmp_path,
            schema_json=schema_json,
            row_count=row_count,
            column_count=column_count,
            source_note=source_note,
        ))
    finally:
        tmp_path.unlink(missing_ok=True)

    return _dsv_to_response(dv)


@router.get("/projects/{project_id}/dataset-versions", response_model=DatasetVersionListResponse)
def list_dataset_versions(
    project_id: str,
) -> DatasetVersionListResponse:
    from ariadne.interfaces.web_api.dependencies import _uow_context
    with _uow_context() as uow:
        items = uow.dataset_versions.list_by_project(project_id)
    return DatasetVersionListResponse(items=[_dsv_to_response(dv) for dv in items])


@router.get("/dataset-versions/{dataset_version_id}", response_model=DatasetVersionResponse)
def get_dataset_version(dataset_version_id: str) -> DatasetVersionResponse:
    from ariadne.interfaces.web_api.dependencies import _uow_context
    from ariadne.product.domain.errors import EntityNotFound
    with _uow_context() as uow:
        dv = uow.dataset_versions.get(dataset_version_id)
        if dv is None:
            raise EntityNotFound("DatasetVersion", dataset_version_id)
    return _dsv_to_response(dv)
