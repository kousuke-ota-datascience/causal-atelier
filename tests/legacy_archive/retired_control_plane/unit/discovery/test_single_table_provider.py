"""Tests for SingleTableDiscoveryInputProvider."""

from __future__ import annotations

import warnings
from pathlib import Path
from unittest.mock import MagicMock

import pandas as pd
import pytest

from ariadne.application.discovery.dto import DiscoveryInputSpecification, DiscoveryRequest
from ariadne.application.discovery.providers.single_table import (
    SingleTableDiscoveryInputProvider,
)


def _make_request(tmp_path: Path, options: dict) -> DiscoveryRequest:
    from ariadne.causal.discovery.config import AnalysisConfig

    return DiscoveryRequest(
        project_root=tmp_path,
        analysis_config_path=tmp_path / "analysis.yaml",
        feature_config_path=None,
        input_specification=DiscoveryInputSpecification(
            provider_type="single_table",
            options=options,
        ),
        analysis_config=AnalysisConfig(),
        feature_config=None,
        output_dir=tmp_path / "output",
    )


class TestSingleTableDiscoveryInputProvider:
    def test_prepare_csv(self, tmp_path: Path) -> None:
        df = pd.DataFrame({"a": [1.0, 2.0, 3.0], "b": [4.0, 5.0, 6.0]})
        table_path = tmp_path / "data.csv"
        df.to_csv(table_path, index=False)

        request = _make_request(tmp_path, {"table_path": "data.csv"})
        provider = SingleTableDiscoveryInputProvider(request)
        result = provider.prepare(request)

        assert list(result.analysis_frame.columns) == ["a", "b"]
        assert len(result.analysis_frame) == 3
        assert result.background_knowledge is None

    def test_prepare_parquet(self, tmp_path: Path) -> None:
        df = pd.DataFrame({"x": [1.0, 2.0], "y": [3.0, 4.0]})
        table_path = tmp_path / "data.parquet"
        df.to_parquet(table_path, index=False)

        request = _make_request(tmp_path, {"table_path": "data.parquet"})
        provider = SingleTableDiscoveryInputProvider(request)
        result = provider.prepare(request)

        assert list(result.analysis_frame.columns) == ["x", "y"]

    def test_column_selection(self, tmp_path: Path) -> None:
        df = pd.DataFrame({"a": [1.0, 2.0], "b": [3.0, 4.0], "c": [5.0, 6.0]})
        table_path = tmp_path / "data.csv"
        df.to_csv(table_path, index=False)

        request = _make_request(tmp_path, {"table_path": "data.csv", "columns": ["a", "c"]})
        provider = SingleTableDiscoveryInputProvider(request)
        result = provider.prepare(request)

        assert list(result.analysis_frame.columns) == ["a", "c"]

    def test_unit_id_dropped(self, tmp_path: Path) -> None:
        df = pd.DataFrame({"id": [1, 2, 3], "a": [1.0, 2.0, 3.0]})
        table_path = tmp_path / "data.csv"
        df.to_csv(table_path, index=False)

        request = _make_request(tmp_path, {"table_path": "data.csv", "unit_id": "id"})
        provider = SingleTableDiscoveryInputProvider(request)
        result = provider.prepare(request)

        assert "id" not in result.analysis_frame.columns

    def test_missing_values_fail_raises(self, tmp_path: Path) -> None:
        import numpy as np
        df = pd.DataFrame({"a": [1.0, None, 3.0], "b": [4.0, 5.0, 6.0]})
        table_path = tmp_path / "data.csv"
        df.to_csv(table_path, index=False)

        request = _make_request(tmp_path, {"table_path": "data.csv", "missing_values": "fail"})
        provider = SingleTableDiscoveryInputProvider(request)
        with pytest.raises(ValueError, match="Missing values"):
            provider.prepare(request)

    def test_missing_values_drop(self, tmp_path: Path) -> None:
        df = pd.DataFrame({"a": [1.0, None, 3.0], "b": [4.0, 5.0, 6.0]})
        table_path = tmp_path / "data.csv"
        df.to_csv(table_path, index=False)

        request = _make_request(tmp_path, {"table_path": "data.csv", "missing_values": "drop"})
        provider = SingleTableDiscoveryInputProvider(request)
        result = provider.prepare(request)

        assert len(result.analysis_frame) == 2

    def test_zscore_standardization(self, tmp_path: Path) -> None:
        df = pd.DataFrame({"a": [1.0, 2.0, 3.0], "b": [10.0, 20.0, 30.0]})
        table_path = tmp_path / "data.csv"
        df.to_csv(table_path, index=False)

        request = _make_request(
            tmp_path, {"table_path": "data.csv", "standardization": "zscore"}
        )
        provider = SingleTableDiscoveryInputProvider(request)
        result = provider.prepare(request)

        import numpy as np
        assert abs(result.analysis_frame["a"].mean()) < 1e-10
        assert abs(result.analysis_frame["a"].std(ddof=1) - 1.0) < 1e-10

    def test_constant_column_warned_and_dropped(self, tmp_path: Path) -> None:
        df = pd.DataFrame({"a": [1.0, 1.0, 1.0], "b": [1.0, 2.0, 3.0]})
        table_path = tmp_path / "data.csv"
        df.to_csv(table_path, index=False)

        request = _make_request(tmp_path, {"table_path": "data.csv"})
        provider = SingleTableDiscoveryInputProvider(request)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = provider.prepare(request)

        assert "a" not in result.analysis_frame.columns
        assert any("Constant columns" in str(warning.message) for warning in w)

    def test_missing_table_path_raises(self, tmp_path: Path) -> None:
        request = _make_request(tmp_path, {})
        provider = SingleTableDiscoveryInputProvider(request)
        with pytest.raises(ValueError, match="table_path"):
            provider.prepare(request)

    def test_nonexistent_file_raises(self, tmp_path: Path) -> None:
        request = _make_request(tmp_path, {"table_path": "nonexistent.csv"})
        provider = SingleTableDiscoveryInputProvider(request)
        with pytest.raises(ValueError, match="does not exist"):
            provider.prepare(request)

    def test_missing_columns_raises(self, tmp_path: Path) -> None:
        df = pd.DataFrame({"a": [1.0, 2.0]})
        table_path = tmp_path / "data.csv"
        df.to_csv(table_path, index=False)

        request = _make_request(
            tmp_path, {"table_path": "data.csv", "columns": ["a", "missing_col"]}
        )
        provider = SingleTableDiscoveryInputProvider(request)
        with pytest.raises(ValueError, match="missing_col"):
            provider.prepare(request)

    def test_does_not_require_campaign_id(self, tmp_path: Path) -> None:
        """Single table provider must not need campaign_id or pre_weeks."""
        df = pd.DataFrame({"x": [1.0, 2.0, 3.0]})
        table_path = tmp_path / "data.csv"
        df.to_csv(table_path, index=False)

        request = _make_request(tmp_path, {"table_path": "data.csv"})
        provider = SingleTableDiscoveryInputProvider(request)
        result = provider.prepare(request)

        assert "campaign_id" not in result.metadata
        assert "pre_weeks" not in result.metadata
