"""Visualization query completion policy shared by API and worker adapters."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select

from ariadne.application.ports import MetadataRepository
from ariadne.domain import metadata as m


def complete_visualization_query(
    session: MetadataRepository,
    query: m.VisualizationQuery,
    table: m.DatasetTableVersion,
    result: dict[str, Any],
) -> None:
    minimum = _small_cell_threshold(session, table.id, query.query_json)
    if minimum:
        result["rows"] = [
            row
            for row in result["rows"]
            if row.get("__group_count", minimum) >= minimum
        ]
        result.setdefault("metadata", {})["small_cell_suppression"] = {
            "minimum_group_count": minimum
        }
    for row in result["rows"]:
        row.pop("__group_count", None)
    result["columns"] = [
        column for column in result.get("columns", []) if column != "__group_count"
    ]
    query.status = "SUCCEEDED"
    query.result_json = result
    query.sampled = result.get("sampled", False)
    query.sample_size = result.get("sample_size")
    query.sampling_method = result.get("sampling_method")
    query.random_seed = result.get("random_seed")
    query.scanned_bytes = result.get("scanned_bytes")
    query.result_row_count = len(result.get("rows", []))
    query.duration_ms = result.get("duration_ms")
    query.finished_at = m.utcnow()


def _small_cell_threshold(
    session: MetadataRepository,
    table_id: str,
    specification: dict[str, Any],
) -> int | None:
    group_by = specification.get("group_by", [])
    if not group_by:
        return None
    policies = session.execute(
        select(
            m.DatasetColumn.name,
            m.DatasetColumnPolicy.classification,
            m.DatasetColumnPolicy.minimum_group_count,
        )
        .join(
            m.DatasetColumnPolicy,
            m.DatasetColumnPolicy.dataset_column_id == m.DatasetColumn.id,
        )
        .where(
            m.DatasetColumn.dataset_table_version_id == table_id,
            m.DatasetColumn.name.in_(group_by),
        )
    ).all()
    thresholds = [
        threshold or 5
        for _, classification, threshold in policies
        if classification in {"PII", "RESTRICTED"}
    ]
    return max(thresholds) if thresholds else None


__all__ = ["complete_visualization_query"]
