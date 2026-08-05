"""Protocol definitions (Ports) for discovery use case boundaries."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from ariadne.application.discovery.dto import (
    DiscoveryArtifactResult,
    DiscoveryRequest,
    PreparedDiscoveryInput,
)
from ariadne.causal.discovery.config import AnalysisConfig


@runtime_checkable
class DiscoveryInputProvider(Protocol):
    """Loads and normalises input data from a specific source."""

    def prepare(self, request: DiscoveryRequest) -> PreparedDiscoveryInput:
        """Prepare discovery input from the request context.

        Args:
            request: Discovery request with project_root, analysis_config,
                feature_config, and provider-specific options.

        Returns:
            Normalised discovery input ready for the backend.
        """
        ...


@runtime_checkable
class DiscoveryBackend(Protocol):
    """Runs causal discovery algorithms on prepared input."""

    def discover(
        self,
        prepared_input: PreparedDiscoveryInput,
        analysis_config: AnalysisConfig,
    ) -> dict[str, Any]:
        """Run discovery algorithms and return per-algorithm results.

        Args:
            prepared_input: Normalised input from the provider.
            analysis_config: Algorithm and diagnostic configuration.

        Returns:
            Mapping from algorithm name to DiscoveryResult.
        """
        ...


@runtime_checkable
class DiscoveryArtifactWriter(Protocol):
    """Persists discovery outputs to an artifact store."""

    def write(
        self,
        request: DiscoveryRequest,
        prepared_input: PreparedDiscoveryInput,
        algorithm_results: dict[str, Any],
    ) -> DiscoveryArtifactResult:
        """Write discovery outputs and return artifact references.

        Args:
            request: Original discovery request.
            prepared_input: Normalised input (frames, metadata) for reporting.
            algorithm_results: Per-algorithm DiscoveryResult mapping.

        Returns:
            Written artifact paths.
        """
        ...


__all__ = [
    "DiscoveryArtifactWriter",
    "DiscoveryBackend",
    "DiscoveryInputProvider",
]
