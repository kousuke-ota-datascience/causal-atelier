"""Tests for CLI args → DiscoveryRequest mapping."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from ariadne.interfaces.cli.discovery import parse_args
from ariadne.application.discovery.factory import build_discovery_request
from ariadne.causal.discovery.constants import DEFAULT_ANALYSIS_CONFIG, DEFAULT_FEATURE_CONFIG


class TestParseArgs:
    def test_defaults(self) -> None:
        args = parse_args([])
        assert args.analysis_config == DEFAULT_ANALYSIS_CONFIG
        assert args.feature_config == DEFAULT_FEATURE_CONFIG
        assert args.project_root is None
        assert args.campaign_id is None
        assert args.input_provider is None

    def test_input_provider_flag(self) -> None:
        args = parse_args(["--input-provider", "single_table"])
        assert args.input_provider == "single_table"

    def test_algorithms_flag(self) -> None:
        args = parse_args(["--algorithms", "pc", "ges"])
        assert list(args.algorithms) == ["pc", "ges"]

    def test_no_background_knowledge_flag(self) -> None:
        args = parse_args(["--no-background-knowledge"])
        assert args.no_background_knowledge is True

    def test_invalid_algorithm_raises(self) -> None:
        with pytest.raises(SystemExit):
            parse_args(["--algorithms", "invalid_algo"])


class TestBuildDiscoveryRequest:
    """DiscoveryRequest construction from parsed args."""

    def _make_args(self, **kwargs):
        defaults = {
            "project_root": None,
            "analysis_config": DEFAULT_ANALYSIS_CONFIG,
            "feature_config": DEFAULT_FEATURE_CONFIG,
            "dataset_yaml": None,
            "campaign_id": None,
            "pre_weeks": None,
            "alpha": None,
            "pc_indep_test": None,
            "alpha_grid": None,
            "bootstrap_samples": None,
            "bootstrap_sample_fraction": None,
            "random_seed": None,
            "pc_discrete_bins": None,
            "collinearity_threshold": None,
            "no_background_knowledge": None,
            "output_dir": None,
            "algorithms": None,
            "notears_threshold": None,
            "input_provider": None,
        }
        defaults.update(kwargs)
        import argparse
        ns = argparse.Namespace(**defaults)
        return ns

    def test_defaults_to_completejourney_provider(self, tmp_path) -> None:
        project_root = tmp_path
        analysis_config_path = tmp_path / "analysis.yaml"
        feature_config_path = tmp_path / "features.yaml"

        _write_minimal_analysis_config(analysis_config_path)
        _write_minimal_feature_config(feature_config_path)

        args = self._make_args(
            analysis_config=analysis_config_path,
            feature_config=feature_config_path,
        )
        request = build_discovery_request(args, project_root)

        assert request.input_specification.provider_type == "completejourney"
        assert request.project_root == project_root

    def test_explicit_provider_type_single_table(self, tmp_path) -> None:
        project_root = tmp_path
        analysis_config_path = tmp_path / "analysis.yaml"
        feature_config_path = tmp_path / "features.yaml"

        _write_minimal_analysis_config(analysis_config_path)
        _write_minimal_feature_config(feature_config_path)

        args = self._make_args(
            analysis_config=analysis_config_path,
            feature_config=feature_config_path,
            input_provider="single_table",
        )
        request = build_discovery_request(args, project_root)

        assert request.input_specification.provider_type == "single_table"
        assert request.feature_config is None

    def test_cli_override_campaign_id(self, tmp_path) -> None:
        project_root = tmp_path
        analysis_config_path = tmp_path / "analysis.yaml"
        feature_config_path = tmp_path / "features.yaml"

        _write_minimal_analysis_config(analysis_config_path)
        _write_minimal_feature_config(feature_config_path)

        args = self._make_args(
            analysis_config=analysis_config_path,
            feature_config=feature_config_path,
            campaign_id="42",
        )
        request = build_discovery_request(args, project_root)

        assert request.analysis_config.run.campaign_id == "42"

    def test_output_dir_from_analysis_config(self, tmp_path) -> None:
        project_root = tmp_path
        analysis_config_path = tmp_path / "analysis.yaml"
        feature_config_path = tmp_path / "features.yaml"
        output_dir = tmp_path / "my_output"

        _write_minimal_analysis_config(analysis_config_path, output_dir=str(output_dir))
        _write_minimal_feature_config(feature_config_path)

        args = self._make_args(
            analysis_config=analysis_config_path,
            feature_config=feature_config_path,
        )
        request = build_discovery_request(args, project_root)

        assert request.output_dir == output_dir

    def test_config_priority_cli_override_beats_yaml(self, tmp_path) -> None:
        """CLI alpha override must win over YAML default."""
        project_root = tmp_path
        analysis_config_path = tmp_path / "analysis.yaml"
        feature_config_path = tmp_path / "features.yaml"

        _write_minimal_analysis_config(analysis_config_path, alpha=0.05)
        _write_minimal_feature_config(feature_config_path)

        args = self._make_args(
            analysis_config=analysis_config_path,
            feature_config=feature_config_path,
            alpha=0.001,  # CLI override
        )
        request = build_discovery_request(args, project_root)

        assert request.analysis_config.discovery.pc.alpha == 0.001


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_minimal_analysis_config(path: Path, output_dir: str = "output", alpha: float = 0.01) -> None:
    path.write_text(
        f"""
run:
  campaign_id: "18"
  pre_weeks: 8
  output_dir: {output_dir}
discovery:
  algorithms: [pc]
  pc:
    alpha: {alpha}
""",
        encoding="utf-8",
    )


def _write_minimal_feature_config(path: Path) -> None:
    path.write_text(
        """
metadata: {}
tables: {}
campaign_window: {}
categorical_mappings: {}
features: {}
background_knowledge:
  tier_order: [baseline, treatment, outcome]
""",
        encoding="utf-8",
    )
