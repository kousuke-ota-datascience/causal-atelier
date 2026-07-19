"""Dataset, object registration, preview, profile, and ETL comparison endpoints."""

from __future__ import annotations

import hashlib
import re
import uuid
from pathlib import Path

import yaml
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Query,
    Request,
    UploadFile,
    status,
)
from fastapi.responses import Response
from sqlalchemy import func, select
from causal_atelier.application.control_plane import ControlPlaneService as Session

from causal_atelier.application.data_catalog import DataCatalogService
from causal_atelier.application.run_execution.services import add_audit
from causal_atelier.infrastructure.artifact_store import artifact_location
from causal_atelier.domain import metadata as m
from causal_atelier.interfaces.api.dependencies import (
    RequestUser,
    get_current_user,
    get_session,
    require_project_role,
)
from causal_atelier.interfaces.api.schemas import (
    DatasetCreate,
    DatasetRegistryImport,
    DatasetVersionCreate,
)

from .common import (
    get_or_404,
    model_dict,
    project_for_dataset_version,
    project_for_table,
)


router = APIRouter(tags=["datasets"])


@router.post("/projects/{project_id}/objects", status_code=status.HTTP_201_CREATED)
def upload_object(
    project_id: str,
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
    request: Request = None,
) -> dict:
    require_project_role(session, user, project_id, "ANALYST")
    suffix = Path(file.filename or "data").suffix.lower()
    if suffix not in {".csv", ".parquet", ".rda", ".rds"}:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Only CSV, Parquet, RDA, and RDS objects are supported",
        )
    safe_name = re.sub(
        r"[^A-Za-z0-9_.-]", "_", Path(file.filename or f"data{suffix}").name
    )
    key = f"uploads/{project_id}/{uuid.uuid4()}/{safe_name}"
    stored = request.app.state.artifact_store.put_stream(file.file, key=key)
    return {
        "backend": stored.location.backend,
        "namespace": stored.location.namespace,
        "key": stored.location.key,
        "version": stored.location.version,
        "media_type": file.content_type,
        "format": {
            ".parquet": "PARQUET",
            ".csv": "CSV",
            ".rda": "RDA",
            ".rds": "RDS",
        }[suffix],
        "size_bytes": stored.size_bytes,
        "checksum": stored.checksum,
    }


@router.post("/datasets", status_code=status.HTTP_201_CREATED)
def create_dataset(
    body: DatasetCreate,
    request: Request,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    require_project_role(session, user, body.project_id, "ANALYST")
    exists = session.scalar(
        select(m.Dataset).where(
            m.Dataset.project_id == body.project_id,
            func.lower(m.Dataset.slug) == body.slug.lower(),
        )
    )
    if exists:
        raise HTTPException(status.HTTP_409_CONFLICT, "Dataset slug already exists")
    dataset = m.Dataset(**body.model_dump(), created_by=user.id)
    session.add(dataset)
    session.flush()
    add_audit(
        session,
        project_id=body.project_id,
        actor_user_id=user.id,
        action="DATASET_CREATE",
        resource_type="DATASET",
        resource_id=dataset.id,
        request_id=request.state.request_id,
        after=body.model_dump(),
    )
    return model_dict(dataset)


@router.get("/datasets")
def list_datasets(
    project_id: str,
    page: int = 1,
    limit: int = 50,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    require_project_role(session, user, project_id)
    page, limit = max(1, page), min(200, max(1, limit))
    query = select(m.Dataset).where(
        m.Dataset.project_id == project_id, m.Dataset.deleted_at.is_(None)
    )
    total = session.scalar(select(func.count()).select_from(query.subquery())) or 0
    items = session.scalars(
        query.order_by(m.Dataset.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    ).all()
    return {
        "items": [model_dict(item) for item in items],
        "total": total,
        "page": page,
        "limit": limit,
    }


@router.post("/datasets/import-registry", status_code=status.HTTP_201_CREATED)
def import_dataset_registry(
    body: DatasetRegistryImport,
    request: Request,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    require_project_role(session, user, body.project_id, "ANALYST")
    try:
        registry = yaml.safe_load(body.registry_yaml) or {}
    except yaml.YAMLError as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid registry YAML"
        ) from exc
    if not isinstance(registry, dict):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Registry must be a mapping"
        )
    logical_names = [str(name) for name in registry if name != "default"]
    missing = sorted(set(logical_names) - set(body.objects))
    extra = sorted(set(body.objects) - set(logical_names))
    if missing or extra:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            {"missing_object_references": missing, "unknown_object_references": extra},
        )
    dataset = m.Dataset(
        project_id=body.project_id,
        slug=body.slug,
        name=body.name,
        description=body.description,
        dataset_kind=body.dataset_kind,
        created_by=user.id,
    )
    session.add(dataset)
    session.flush()
    tables = [
        {
            "logical_name": name,
            "object": body.objects[name].model_dump(),
            "source_entry_name": name,
        }
        for name in logical_names
    ]
    version = DataCatalogService(
        session,
        request.app.state.artifact_store,
        request.app.state.query_engine,
    ).create_version(
        dataset=dataset,
        actor_user_id=user.id,
        source_type="IMPORT",
        source_metadata={
            "registry_format": "LEGACY_YAML",
            "registry_hash": hashlib.sha256(body.registry_yaml.encode()).hexdigest(),
        },
        tables=tables,
        profile=body.profile,
    )
    return _version_response(session, version)


@router.post("/datasets/{dataset_id}/versions", status_code=status.HTTP_201_CREATED)
def create_dataset_version(
    dataset_id: str,
    body: DatasetVersionCreate,
    request: Request,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    dataset = get_or_404(session, m.Dataset, dataset_id)
    require_project_role(session, user, dataset.project_id, "ANALYST")
    service = DataCatalogService(
        session, request.app.state.artifact_store, request.app.state.query_engine
    )
    version = service.create_version(
        dataset=dataset,
        actor_user_id=user.id,
        source_type=body.source_type,
        source_metadata=body.source_metadata,
        tables=[table.model_dump() for table in body.tables],
        profile=body.profile,
    )
    return _version_response(session, version)


@router.get("/dataset-versions/{version_id}")
def get_dataset_version(
    version_id: str,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    version = get_or_404(session, m.DatasetVersion, version_id)
    require_project_role(session, user, project_for_dataset_version(session, version))
    return _version_response(session, version)


@router.get("/dataset-versions/{version_id}/registry")
def export_registry(
    version_id: str,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> Response:
    version = get_or_404(session, m.DatasetVersion, version_id)
    require_project_role(session, user, project_for_dataset_version(session, version))
    service = DataCatalogService(session, None, None)
    document = service.registry_snapshot(version)
    return Response(
        yaml.safe_dump(document, sort_keys=False), media_type="application/yaml"
    )


@router.get("/dataset-table-versions/{table_version_id}/preview")
def preview_table(
    table_version_id: str,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=100, ge=1, le=1000),
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
    request: Request = None,
) -> dict:
    table = get_or_404(session, m.DatasetTableVersion, table_version_id)
    require_project_role(session, user, project_for_table(session, table))
    stored = get_or_404(session, m.StoredObject, table.stored_object_id)
    allowed, masked = _column_access(session, table.id, "preview_allowed")
    result = request.app.state.query_engine.preview(
        request.app.state.artifact_store.resolve_local_path(artifact_location(stored)),
        table.file_format,
        page=page,
        limit=limit,
        columns=allowed,
    ).to_dict()
    for row in result["rows"]:
        for name, rule in masked.items():
            if name in row:
                row[name] = _mask(row[name], rule)
    result["dataset_table_version_id"] = table.id
    all_columns = {field["name"] for field in table.schema_json.get("fields", [])}
    result["omitted_columns"] = sorted(all_columns - set(allowed))
    return result


@router.get("/dataset-table-versions/{table_version_id}/profile")
def get_profile(
    table_version_id: str,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    table = get_or_404(session, m.DatasetTableVersion, table_version_id)
    require_project_role(session, user, project_for_table(session, table))
    profile = session.scalar(
        select(m.DataProfile)
        .where(m.DataProfile.dataset_table_version_id == table.id)
        .order_by(m.DataProfile.created_at.desc())
    )
    if not profile:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Profile not found")
    response = model_dict(profile)
    if profile.status == "SUCCEEDED":
        allowed, _ = _column_access(session, table.id, "analysis_allowed")
        response["summary_json"] = {
            **profile.summary_json,
            "columns": [
                column
                for column in profile.summary_json.get("columns", [])
                if column["name"] in allowed
            ],
        }
    return response


@router.patch("/dataset-columns/{column_id}/policy")
def update_column_policy(
    column_id: str,
    body: dict,
    request: Request,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    column = get_or_404(session, m.DatasetColumn, column_id)
    table = get_or_404(session, m.DatasetTableVersion, column.dataset_table_version_id)
    project_id = project_for_table(session, table)
    require_project_role(session, user, project_id, "PROJECT_ADMIN")
    policy = get_or_404(session, m.DatasetColumnPolicy, column.id)
    permitted = {
        "classification",
        "preview_allowed",
        "analysis_allowed",
        "download_allowed",
        "mask_rule",
        "minimum_group_count",
    }
    unknown = set(body) - permitted
    if unknown:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            f"Unknown policy fields: {sorted(unknown)}",
        )
    for name, value in body.items():
        setattr(policy, name, value)
    policy.updated_by = user.id
    policy.updated_at = m.utcnow()
    add_audit(
        session,
        project_id=project_id,
        actor_user_id=user.id,
        action="DATASET_COLUMN_POLICY_UPDATE",
        resource_type="DATASET_COLUMN_POLICY",
        resource_id=column.id,
        request_id=request.state.request_id,
        after=body,
    )
    return model_dict(policy)


@router.get("/etl-runs/{run_id}/dataset-comparison")
def compare_etl_datasets(
    run_id: str,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    run = get_or_404(session, m.Run, run_id)
    require_project_role(session, user, run.project_id)
    stage_ids = session.scalars(
        select(m.StageRun.id).where(
            m.StageRun.run_id == run.id, m.StageRun.stage_type == "ETL"
        )
    ).all()
    input_ids = session.scalars(
        select(m.StageRunDatasetInput.dataset_version_id).where(
            m.StageRunDatasetInput.stage_run_id.in_(stage_ids)
        )
    ).all()
    output_versions = session.scalars(
        select(m.DatasetVersion).where(
            m.DatasetVersion.origin_stage_run_id.in_(stage_ids)
        )
    ).all()
    if not input_ids or not output_versions:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "ETL input/output dataset mapping not found"
        )
    input_tables = session.scalars(
        select(m.DatasetTableVersion).where(
            m.DatasetTableVersion.dataset_version_id == input_ids[0]
        )
    ).all()
    output_tables = session.scalars(
        select(m.DatasetTableVersion).where(
            m.DatasetTableVersion.dataset_version_id == output_versions[0].id
        )
    ).all()
    before = {table.logical_name: table for table in input_tables}
    after = {table.logical_name: table for table in output_tables}
    comparisons = []
    for name in sorted(set(before) | set(after)):
        left, right = before.get(name), after.get(name)
        comparisons.append(_compare_table(session, name, left, right))
    return {
        "run_id": run.id,
        "input_dataset_version_id": input_ids[0],
        "output_dataset_version_id": output_versions[0].id,
        "column_mapping_method": "EXACT_NAME_ONLY",
        "unmapped_columns_are_not_inferred": True,
        "tables": comparisons,
    }


def _version_response(session: Session, version: m.DatasetVersion) -> dict:
    tables = session.scalars(
        select(m.DatasetTableVersion)
        .where(m.DatasetTableVersion.dataset_version_id == version.id)
        .order_by(m.DatasetTableVersion.ordinal)
    ).all()
    response = model_dict(version)
    response["tables"] = [
        model_dict(table, exclude={"stored_object_id"}) for table in tables
    ]
    return response


def _column_access(
    session: Session, table_id: str, permission: str
) -> tuple[list[str], dict[str, str]]:
    rows = session.execute(
        select(m.DatasetColumn, m.DatasetColumnPolicy)
        .join(
            m.DatasetColumnPolicy,
            m.DatasetColumnPolicy.dataset_column_id == m.DatasetColumn.id,
        )
        .where(m.DatasetColumn.dataset_table_version_id == table_id)
        .order_by(m.DatasetColumn.ordinal)
    ).all()
    allowed = [column.name for column, policy in rows if getattr(policy, permission)]
    masked = {
        column.name: policy.mask_rule
        for column, policy in rows
        if getattr(policy, permission) and policy.mask_rule
    }
    return allowed, masked


def _mask(value: object, rule: str) -> object:
    if value is None:
        return None
    text = str(value)
    if rule == "LAST4":
        return "*" * max(0, len(text) - 4) + text[-4:]
    if rule == "HASH":
        import hashlib

        return hashlib.sha256(text.encode()).hexdigest()[:12]
    return "***"


def _profile_for(session: Session, table: m.DatasetTableVersion | None) -> dict:
    if not table:
        return {}
    profile = session.scalar(
        select(m.DataProfile)
        .where(
            m.DataProfile.dataset_table_version_id == table.id,
            m.DataProfile.status == "SUCCEEDED",
        )
        .order_by(m.DataProfile.created_at.desc())
    )
    return profile.summary_json if profile else {}


def _compare_table(
    session: Session,
    name: str,
    before: m.DatasetTableVersion | None,
    after: m.DatasetTableVersion | None,
) -> dict:
    before_profile, after_profile = (
        _profile_for(session, before),
        _profile_for(session, after),
    )
    before_columns = {
        field["name"]: field
        for field in (before.schema_json.get("fields", []) if before else [])
    }
    after_columns = {
        field["name"]: field
        for field in (after.schema_json.get("fields", []) if after else [])
    }
    left_profiles = {item["name"]: item for item in before_profile.get("columns", [])}
    right_profiles = {item["name"]: item for item in after_profile.get("columns", [])}
    common = sorted(set(before_columns) & set(after_columns))
    return {
        "logical_name": name,
        "status": "MATCHED" if before and after else ("ADDED" if after else "REMOVED"),
        "row_count": {
            "before": before_profile.get(
                "row_count", before.row_count if before else None
            ),
            "after": after_profile.get("row_count", after.row_count if after else None),
        },
        "columns_added": sorted(set(after_columns) - set(before_columns)),
        "columns_removed": sorted(set(before_columns) - set(after_columns)),
        "type_changes": [
            {
                "column": column,
                "before": before_columns[column]["physical_type"],
                "after": after_columns[column]["physical_type"],
            }
            for column in common
            if before_columns[column]["physical_type"]
            != after_columns[column]["physical_type"]
        ],
        "profile_differences": [
            {
                "column": column,
                "null_ratio_before": left_profiles.get(column, {}).get("null_ratio"),
                "null_ratio_after": right_profiles.get(column, {}).get("null_ratio"),
                "distinct_before": left_profiles.get(column, {}).get("distinct_count"),
                "distinct_after": right_profiles.get(column, {}).get("distinct_count"),
            }
            for column in common
        ],
        "renames": [],
    }


__all__ = ["router"]
