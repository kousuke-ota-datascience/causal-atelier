"""Complete Journey ETL application service."""

from __future__ import annotations

from pathlib import Path

from causal_atelier.etl.completejourney.extract import CompleteJourneyExtractor
from causal_atelier.etl.completejourney.load import CompleteJourneyParquetLoader
from causal_atelier.etl.completejourney.transform import normalize_tables


def execute_completejourney_etl(project_root: Path) -> dict[str, Path]:
    """Extract, normalize, and persist all Complete Journey tables."""

    extracted = CompleteJourneyExtractor(project_root).extract_all()
    normalized = normalize_tables(extracted)
    return CompleteJourneyParquetLoader(project_root).load_all(normalized)


__all__ = ["execute_completejourney_etl"]
