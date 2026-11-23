"""Local Discovery's scientific execution interface."""
from dataclasses import dataclass
from typing import Protocol

from ariadne.causal.discovery.contracts import DiscoveryGraphOutcome, ValidatedDiscoveryRequest
from ariadne.scientific.capabilities import backend_error, unsupported
from ariadne.scientific.ports.artifacts import StagingArtifactSink


class DiscoveryPort(Protocol):
    def discover(self, request: ValidatedDiscoveryRequest, *, sink: StagingArtifactSink) -> DiscoveryGraphOutcome: ...


@dataclass(frozen=True)
class LocalDiscoveryDispatcher:
    registry: object

    def discover(self, request: ValidatedDiscoveryRequest, *, sink: StagingArtifactSink) -> DiscoveryGraphOutcome:
        if type(request) is not ValidatedDiscoveryRequest:
            raise unsupported("Expected validated Discovery request")
        adapter = self.registry.load_adapter(request.capability)
        descriptor = adapter.method_descriptor
        if (descriptor.method_id, descriptor.backend_id) != (
            request.capability.method_id, request.capability.backend_id,
        ):
            raise backend_error("BACKEND_API_MISMATCH", "Discovery adapter binding changed")
        return adapter.execute(request, sink=sink)
