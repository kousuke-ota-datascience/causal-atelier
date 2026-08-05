"""Persist normalized Complete Journey tables."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import pandas as pd


class CompleteJourneyParquetLoader:
    """Write normalized tables to the interim data stage."""

    def __init__(self, project_root: Path | None = None) -> None:
        root = (project_root or Path.cwd()).resolve()
        self.output_dir = root / "data/10_interim/completejourney"

    def load_all(self, tables: Mapping[str, pd.DataFrame]) -> dict[str, Path]:
        """Write every table and return its output path."""

        self.output_dir.mkdir(parents=True, exist_ok=True)
        outputs: dict[str, Path] = {}
        for name, table in tables.items():
            output_path = self.output_dir / f"{name}.parquet"
            table.to_parquet(output_path)
            outputs[str(name)] = output_path
        return outputs


__all__ = ["CompleteJourneyParquetLoader"]
