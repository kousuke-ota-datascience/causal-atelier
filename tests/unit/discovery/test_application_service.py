"""Tests for DiscoveryApplicationService orchestration."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from ariadne.application.discovery.dto import (
    DiscoveryArtifactResult,
    DiscoveryInputSpecification,
    DiscoveryRequest,
    PreparedDiscoveryInput,
)
from ariadne.application.discovery.providers.registry import DiscoveryInputProviderRegistry
from ariadne.application.discovery.service import DiscoveryApplicationService
from ariadne.causal.discovery.config import AnalysisConfig
from ariadne.causal.discovery.results import DiscoveryResult


def _make_request(tmp_path: Path, provider_type: str = "mock") -> DiscoveryRequest:
    return DiscoveryRequest(
        project_root=tmp_path,
        analysis_config_path=tmp_path / "analysis.yaml",
        feature_config_path=None,
        input_specification=DiscoveryInputSpecification(
            provider_type=provider_type,
            options={},
        ),
        analysis_config=AnalysisConfig(),
        feature_config=None,
        output_dir=tmp_path / "output",
    )


def _mock_prepared_input() -> PreparedDiscoveryInput:
    return PreparedDiscoveryInput(
        analysis_frame=pd.DataFrame({"a": [1.0, 2.0], "b": [3.0, 4.0]}),
        raw_frame=None,
        transformed_frame=None,
        variable_metadata=pd.DataFrame(),
        background_knowledge=None,
        metadata={"campaign_id": "18", "pre_weeks": 8},
    )


def _mock_algorithm_results() -> dict:
    return {
        "pc": DiscoveryResult(
            algorithm="pc",
            causal_graph=None,
            edges=pd.DataFrame(columns=["source", "target"]),
            status="ok",
            message="",
        )
    }


class TestDiscoveryApplicationServiceOrchestration:
    def _build_service(self, provider_type: str = "mock"):
        registry = DiscoveryInputProviderRegistry()
        mock_provider = MagicMock()
        mock_provider.prepare.return_value = _mock_prepared_input()
        registry.register(provider_type, lambda req: mock_provider)

        mock_backend = MagicMock()
        mock_backend.discover.return_value = _mock_algorithm_results()

        mock_writer = MagicMock()
        mock_writer.write.return_value = DiscoveryArtifactResult(artifacts={})

        service = DiscoveryApplicationService(
            provider_registry=registry,
            backend=mock_backend,
            artifact_writer=mock_writer,
        )
        return service, mock_provider, mock_backend, mock_writer

    def test_execute_calls_provider_backend_writer_in_order(self, tmp_path) -> None:
        service, provider, backend, writer = self._build_service()
        request = _make_request(tmp_path)
        result = service.execute(request)

        provider.prepare.assert_called_once_with(request)
        backend.discover.assert_called_once()
        writer.write.assert_called_once()

    def test_execute_returns_correct_counts(self, tmp_path) -> None:
        service, _, _, _ = self._build_service()
        request = _make_request(tmp_path)
        result = service.execute(request)

        assert result.sample_count == 2
        assert result.variable_count == 2

    def test_execute_status_ok(self, tmp_path) -> None:
        service, _, _, _ = self._build_service()
        request = _make_request(tmp_path)
        result = service.execute(request)

        assert result.status == "ok"

    def test_execute_unknown_provider_raises(self, tmp_path) -> None:
        registry = DiscoveryInputProviderRegistry()
        # Only "completejourney" registered
        registry.register("completejourney", lambda req: MagicMock())

        service = DiscoveryApplicationService(
            provider_registry=registry,
            backend=MagicMock(),
            artifact_writer=MagicMock(),
        )
        request = _make_request(tmp_path, provider_type="unknown_provider")

        with pytest.raises(ValueError, match="Unknown input provider"):
            service.execute(request)

    def test_execute_propagates_backend_errors(self, tmp_path) -> None:
        registry = DiscoveryInputProviderRegistry()
        mock_provider = MagicMock()
        mock_provider.prepare.return_value = _mock_prepared_input()
        registry.register("mock", lambda req: mock_provider)

        mock_backend = MagicMock()
        mock_backend.discover.side_effect = RuntimeError("algorithm failed")

        service = DiscoveryApplicationService(
            provider_registry=registry,
            backend=mock_backend,
            artifact_writer=MagicMock(),
        )
        request = _make_request(tmp_path)

        with pytest.raises(RuntimeError, match="algorithm failed"):
            service.execute(request)

    def test_result_includes_provider_type_in_metadata(self, tmp_path) -> None:
        service, _, _, _ = self._build_service()
        request = _make_request(tmp_path)
        result = service.execute(request)

        assert result.metadata.get("provider_type") == "mock"
