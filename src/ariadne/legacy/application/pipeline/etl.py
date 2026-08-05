"""Complete Journey ETL application service."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping
from ariadne.etl.completejourney.extract import (
    DEFAULT_TABLE_TYPES,
    CompleteJourneyExtractor,
)
from ariadne.etl.completejourney.load import CompleteJourneyParquetLoader
from ariadne.etl.completejourney.transform import normalize_tables


def execute_completejourney_etl(
    project_root: Path,
    table_types: Mapping[str, str] = DEFAULT_TABLE_TYPES,
) -> dict[str, Path]:
    """Extract, normalize, and persist all Complete Journey tables."""

    extracted = CompleteJourneyExtractor(project_root).extract_all(table_types)
    normalized = normalize_tables(extracted)
    return CompleteJourneyParquetLoader(project_root).load_all(normalized)


__all__ = ["execute_completejourney_etl"]
