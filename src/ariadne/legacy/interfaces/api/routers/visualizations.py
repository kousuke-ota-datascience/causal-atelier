"""Saved visualization specifications and bounded server-side queries."""

from __future__ import annotations

import csv
import io
import struct
import zlib
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy import select
from ariadne.application.control_plane import ControlPlaneService as Session

from ariadne.application.run_execution.services import canonical_hash
from ariadne.application.visualization import complete_visualization_query
from ariadne.infrastructure.artifact_store import artifact_location
from ariadne.domain import metadata as m
from ariadne.interfaces.api.dependencies import (
    RequestUser,
    get_current_user,
    get_session,
    require_project_role,
)
from ariadne.interfaces.api.schemas import (
    VisualizationQueryCreate,
    VisualizationSpecificationCreate,
)

from .common import get_or_404, model_dict, project_for_table


router = APIRouter(tags=["visualizations"])


@router.post("/visualization-specifications", status_code=status.HTTP_201_CREATED)
def create_specification(
    body: VisualizationSpecificationCreate,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    require_project_role(session, user, body.project_id, "ANALYST")
    if not body.dataset_table_version_id and not body.logical_table_name:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "A table version or logical table name is required",
        )
    if body.dataset_table_version_id:
        table = get_or_404(
            session, m.DatasetTableVersion, body.dataset_table_version_id
        )
        if project_for_table(session, table) != body.project_id:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Resource not found")
        _authorize_query_columns(
            session, table, body.specification.model_dump(mode="json")
        )
    specification = body.specification.model_dump(mode="json")
    record = m.VisualizationSpecification(
        project_id=body.project_id,
        name=body.name,
        description=body.description,
        dataset_table_version_id=body.dataset_table_version_id,
        logical_table_name=body.logical_table_name,
        specification_json=specification,
        specification_hash=canonical_hash(specification),
        created_by=user.id,
    )
    session.add(record)
    session.flush()
    return model_dict(record)


@router.get("/visualization-specifications/{specification_id}")
def get_specification(
    specification_id: str,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    specification = get_or_404(session, m.VisualizationSpecification, specification_id)
    require_project_role(session, user, specification.project_id)
    return model_dict(specification)


@router.get("/visualization-specifications/{specification_id}/export")
def export_specification(
    specification_id: str,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    specification = get_or_404(session, m.VisualizationSpecification, specification_id)
    require_project_role(session, user, specification.project_id)
    return {
        "schema_version": "1",
        "id": specification.id,
        "name": specification.name,
        "description": specification.description,
        "dataset_table_version_id": specification.dataset_table_version_id,
        "logical_table_name": specification.logical_table_name,
        "specification": specification.specification_json,
        "specification_hash": specification.specification_hash,
    }


@router.post("/visualization-specifications/{specification_id}/execute")
def execute_specification(
    specification_id: str,
    request: Request,
    response: Response,
    body: dict[str, Any] | None = None,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    saved = get_or_404(session, m.VisualizationSpecification, specification_id)
    require_project_role(session, user, saved.project_id, "ANALYST")
    table_id = (body or {}).get(
        "dataset_table_version_id"
    ) or saved.dataset_table_version_id
    if not table_id:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "dataset_table_version_id is required"
        )
    table = get_or_404(session, m.DatasetTableVersion, table_id)
    if project_for_table(session, table) != saved.project_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Resource not found")
    result = _create_query(
        request,
        session,
        user,
        table,
        saved.specification_json,
        force_async=bool((body or {}).get("force_async", False)),
        specification_id=saved.id,
    )
    if result["status"] in {"SUBMITTED", "RUNNING"}:
        response.status_code = status.HTTP_202_ACCEPTED
    return result


@router.post("/dataset-table-versions/{table_version_id}/visualization-queries")
def create_query(
    table_version_id: str,
    body: VisualizationQueryCreate,
    request: Request,
    response: Response,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    table = get_or_404(session, m.DatasetTableVersion, table_version_id)
    project_id = project_for_table(session, table)
    require_project_role(session, user, project_id, "ANALYST")
    result = _create_query(
        request,
        session,
        user,
        table,
        body.specification.model_dump(mode="json"),
        force_async=body.force_async,
    )
    if result["status"] in {"SUBMITTED", "RUNNING"}:
        response.status_code = status.HTTP_202_ACCEPTED
    return result


@router.get("/visualization-queries/{query_id}")
def get_query(
    query_id: str,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    query = get_or_404(session, m.VisualizationQuery, query_id)
    require_project_role(session, user, query.project_id)
    return _query_response(query)


@router.post(
    "/visualization-queries/{query_id}/cancel", status_code=status.HTTP_202_ACCEPTED
)
def cancel_query(
    query_id: str,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    query = get_or_404(session, m.VisualizationQuery, query_id)
    require_project_role(session, user, query.project_id, "ANALYST")
    if query.status in {"SUCCEEDED", "FAILED", "CANCELLED"}:
        raise HTTPException(
            status.HTTP_409_CONFLICT, f"Query is already {query.status}"
        )
    query.status = "CANCELLED"
    query.finished_at = m.utcnow()
    return _query_response(query)


@router.get("/visualization-queries/{query_id}/export")
def export_query(
    query_id: str,
    format: str = "csv",
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> Response:
    query = get_or_404(session, m.VisualizationQuery, query_id)
    require_project_role(session, user, query.project_id)
    if query.status != "SUCCEEDED" or not query.result_json:
        raise HTTPException(status.HTTP_409_CONFLICT, "Query result is not available")
    rows = query.result_json.get("rows", [])
    if format.lower() == "csv":
        output = io.StringIO()
        columns = query.result_json.get("columns", [])
        writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
        return Response(
            output.getvalue(),
            media_type="text/csv",
            headers={
                "Content-Disposition": f'attachment; filename="visualization-{query.id}.csv"'
            },
        )
    if format.lower() == "png":
        png = _bar_chart_png(rows, query.result_json.get("columns", []))
        return Response(
            png,
            media_type="image/png",
            headers={
                "Content-Disposition": f'attachment; filename="visualization-{query.id}.png"'
            },
        )
    raise HTTPException(
        status.HTTP_422_UNPROCESSABLE_ENTITY, "format must be csv or png"
    )


def _create_query(
    request: Request,
    session: Session,
    user: RequestUser,
    table: m.DatasetTableVersion,
    specification: dict[str, Any],
    *,
    force_async: bool,
    specification_id: str | None = None,
) -> dict:
    project_id = project_for_table(session, table)
    _authorize_query_columns(session, table, specification)
    stored = get_or_404(session, m.StoredObject, table.stored_object_id)
    query_hash = canonical_hash(
        {
            "dataset_content_hash": table.content_hash,
            "specification": specification,
            "engine": request.app.state.query_engine.version,
        }
    )
    cached = session.scalar(
        select(m.VisualizationQuery)
        .where(
            m.VisualizationQuery.dataset_table_version_id == table.id,
            m.VisualizationQuery.query_hash == query_hash,
            m.VisualizationQuery.query_engine_version
            == request.app.state.query_engine.version,
            m.VisualizationQuery.status == "SUCCEEDED",
        )
        .order_by(m.VisualizationQuery.finished_at.desc())
    )
    if cached:
        query = m.VisualizationQuery(
            project_id=project_id,
            dataset_table_version_id=table.id,
            visualization_specification_id=specification_id,
            status="SUCCEEDED",
            query_json=specification,
            query_hash=query_hash,
            query_engine_version=request.app.state.query_engine.version,
            result_json=cached.result_json,
            result_artifact_id=cached.result_artifact_id,
            cache_hit=True,
            sampled=cached.sampled,
            sample_size=cached.sample_size,
            sampling_method=cached.sampling_method,
            random_seed=cached.random_seed,
            scanned_bytes=0,
            result_row_count=cached.result_row_count,
            duration_ms=0,
            created_by=user.id,
            started_at=m.utcnow(),
            finished_at=m.utcnow(),
        )
        session.add(query)
        session.flush()
        return _query_response(query)
    asynchronous = (
        force_async
        or (stored.size_bytes or 0)
        > request.app.state.settings.query_async_threshold_bytes
    )
    query = m.VisualizationQuery(
        project_id=project_id,
        dataset_table_version_id=table.id,
        visualization_specification_id=specification_id,
        status="SUBMITTED" if asynchronous else "RUNNING",
        query_json=specification,
        query_hash=query_hash,
        query_engine_version=request.app.state.query_engine.version,
        created_by=user.id,
        started_at=None if asynchronous else m.utcnow(),
    )
    session.add(query)
    session.flush()
    if asynchronous:
        session.add(
            m.OutboxEvent(
                aggregate_type="VISUALIZATION_QUERY",
                aggregate_id=query.id,
                event_type="EXECUTE_VISUALIZATION_QUERY",
                payload_json={"query_id": query.id},
            )
        )
    else:
        try:
            result = request.app.state.query_engine.execute(
                request.app.state.artifact_store.resolve_local_path(
                    artifact_location(stored)
                ),
                table.file_format,
                specification,
            )
            complete_visualization_query(session, query, table, result.to_dict())
        except Exception as exc:
            query.status = "FAILED"
            query.error_summary = str(exc)
            query.finished_at = m.utcnow()
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc
    return _query_response(query)


def _authorize_query_columns(
    session: Session, table: m.DatasetTableVersion, specification: dict[str, Any]
) -> None:
    requested = set(specification.get("selected_columns", []))
    requested.update(specification.get("group_by", []))
    requested.update(item["column"] for item in specification.get("filters", []))
    if specification.get("series_column"):
        requested.add(specification["series_column"])
    if specification.get("aggregation_target"):
        requested.add(specification["aggregation_target"])
    rows = session.execute(
        select(m.DatasetColumn.name, m.DatasetColumnPolicy.analysis_allowed)
        .join(
            m.DatasetColumnPolicy,
            m.DatasetColumnPolicy.dataset_column_id == m.DatasetColumn.id,
        )
        .where(m.DatasetColumn.dataset_table_version_id == table.id)
    ).all()
    permissions = dict(rows)
    unknown = requested - set(permissions)
    denied = {
        name for name in requested if name in permissions and not permissions[name]
    }
    if unknown:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, f"Unknown columns: {sorted(unknown)}"
        )
    if denied:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            f"Columns are not allowed for analysis: {sorted(denied)}",
        )


def _query_response(query: m.VisualizationQuery) -> dict:
    return {
        **model_dict(query),
        "poll_url": f"/api/v1/visualization-queries/{query.id}"
        if query.status in {"SUBMITTED", "RUNNING"}
        else None,
        "export_url": f"/api/v1/visualization-queries/{query.id}/export"
        if query.status == "SUCCEEDED"
        else None,
    }


def _bar_chart_png(rows: list[dict[str, Any]], columns: list[str]) -> bytes:
    """Render a deliberately small dependency-free bar chart PNG."""

    width, height = 800, 450
    pixels = bytearray([248, 250, 252] * width * height)
    numeric = next(
        (
            name
            for name in columns
            if any(isinstance(row.get(name), (int, float)) for row in rows)
        ),
        None,
    )
    values = (
        [max(0.0, float(row.get(numeric, 0) or 0)) for row in rows[:40]]
        if numeric
        else []
    )
    maximum = max(values, default=1.0) or 1.0
    chart_left, chart_bottom, chart_top = 50, height - 40, 25
    bar_width = max(2, min(30, (width - chart_left - 20) // max(1, len(values))))
    for index, value in enumerate(values):
        x0 = chart_left + index * bar_width
        bar_height = int((chart_bottom - chart_top) * value / maximum)
        for y in range(chart_bottom - bar_height, chart_bottom):
            for x in range(x0, min(width, x0 + bar_width - 2)):
                offset = (y * width + x) * 3
                pixels[offset : offset + 3] = bytes((37, 99, 235))
    raw = b"".join(
        b"\x00" + pixels[y * width * 3 : (y + 1) * width * 3] for y in range(height)
    )

    def chunk(kind: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + kind
            + data
            + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        )

    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


__all__ = ["router"]
