from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from causal_atelier.etl.completejourney.extract import (
    CompleteJourneyExtractor,
    RDataLoadError,
    RdaLoadStrategy,
    RdsLoadStrategy,
    build_rdata_loader,
)
from causal_atelier.etl.completejourney.transform import normalize_tables


def test_build_rdata_loader_selects_strategy() -> None:
    assert isinstance(build_rdata_loader("rda")._strategy, RdaLoadStrategy)
    assert isinstance(build_rdata_loader("rds")._strategy, RdsLoadStrategy)
    with pytest.raises(RDataLoadError):
        build_rdata_loader("csv")


def test_extractor_uses_repository_data_tree(tmp_path: Path) -> None:
    extractor = CompleteJourneyExtractor(tmp_path)

    assert extractor.build_file_path("transactions", "rds") == (
        tmp_path / "data/00_raw/completejourney/rdata/transactions.rds"
    )


def test_normalize_tables_copies_frames_and_column_names() -> None:
    original = pd.DataFrame({1: [10]})
    normalized = normalize_tables({"transactions": original})

    assert normalized["transactions"].columns.tolist() == ["1"]
    assert normalized["transactions"] is not original
