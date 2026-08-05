"""Discovery Application Service."""

from __future__ import annotations

from ariadne.application.discovery.dto import (
    DiscoveryExecutionResult,
    DiscoveryRequest,
)
from ariadne.application.discovery.ports import (
    DiscoveryArtifactWriter,
    DiscoveryBackend,
    DiscoveryInputProvider,
)
from ariadne.application.discovery.providers.registry import DiscoveryInputProviderRegistry


class DiscoveryApplicationService:
    """Orchestrates the causal discovery use case.

    CLI, PipelineStageRunner, and Worker all call this service with a
    DiscoveryRequest.  The service knows nothing about argparse, stdout,
    Complete-Journey table names, or local-filesystem paths.

    Args:
        provider_registry: Registry that resolves the correct input provider.
        backend: Algorithm runner (e.g. CausalLearnDiscoveryBackend).
        artifact_writer: Persists outputs (e.g. LocalDiscoveryArtifactWriter).
    """

    def __init__(
        self,
        *,
        provider_registry: DiscoveryInputProviderRegistry,
        backend: DiscoveryBackend,
        artifact_writer: DiscoveryArtifactWriter,
    ) -> None:
        self._registry = provider_registry
        self._backend = backend
        self._writer = artifact_writer

    def execute(self, request: DiscoveryRequest) -> DiscoveryExecutionResult:
        """Run the full discovery use case.

        Args:
            request: Immutable discovery request.

        Returns:
            Execution result with algorithm outputs, artifact paths, and counts.

        Raises:
            ValueError: If the requested provider type is not registered.
            Exception: Provider, backend, or artifact-writer failures propagate as-is.
        """
        provider = self._registry.create(
            request.input_specification.provider_type,
            request,
        )
        prepared = provider.prepare(request)

        algorithm_results = self._backend.discover(prepared, request.analysis_config)

        artifact_result = self._writer.write(request, prepared, algorithm_results)

        return DiscoveryExecutionResult(
            status="ok",
            algorithm_results=algorithm_results,
            artifacts=artifact_result.artifacts,
            sample_count=len(prepared.analysis_frame),
            variable_count=len(prepared.analysis_frame.columns),
            output_dir=request.output_dir,
            analysis_config=request.analysis_config,
            metadata={
                "provider_type": request.input_specification.provider_type,
                "pc_indep_test": request.analysis_config.discovery.pc.indep_test,
                **prepared.metadata,
            },
        )


__all__ = ["DiscoveryApplicationService"]
