"""A single Local Method registry with lazy selected-adapter loading."""
from dataclasses import dataclass
from types import MappingProxyType

from ariadne.scientific.capabilities import (
    CI_PROFILES, LOCAL_BACKEND, LOCAL_METHOD, LOCAL_VERSION, BackendCapabilityRecord, MethodDescriptor,
    backend_error, unsupported,
)
from ariadne.scientific.causal_methods.discovery import FciRuntimeObservation
from ariadne.scientific.ports.capability import ValidatedCapabilityRequest
from ariadne.shared.content_ref import valid_sha256

LOCAL_FCI = MethodDescriptor(LOCAL_METHOD, "DISCOVER", "GRAPH_STRUCTURE", False, LOCAL_BACKEND,
                             CI_PROFILES, "1")

# Catalog namespaces and counts are pinned by the frozen Method metadata authority.
_METHOD_IDS = frozenset(f"P{phase}-M{index:02d}" for phase, limit in enumerate((20, 8, 13), 1)
                        for index in range(1, limit + 1))


@dataclass(frozen=True)
class MethodCapabilityRegistry:
    descriptors: object
    backend_factories: object
    effective_env: FciRuntimeObservation
    inference_registry: object

    def __post_init__(self) -> None:
        descriptors = dict(self.descriptors)
        factories = dict(self.backend_factories)
        if (
            any(key not in _METHOD_IDS or type(value) is not MethodDescriptor or value.method_id != key
                for key, value in descriptors.items())
            or descriptors.get(LOCAL_METHOD) != LOCAL_FCI
            or set(factories) - {LOCAL_METHOD}
            or any(not callable(factory) for factory in factories.values())
            or type(self.effective_env) is not FciRuntimeObservation
        ):
            raise unsupported("Invalid Local Method registry")
        object.__setattr__(self, "descriptors", MappingProxyType(descriptors))
        object.__setattr__(self, "backend_factories", MappingProxyType(factories))

    def describe(self, method_id: str) -> MethodDescriptor:
        if method_id not in self.descriptors:
            raise unsupported("Unknown Local Method")
        return self.descriptors[method_id]

    def resolve(self, method_id: str, backend_id: str, profile: str) -> BackendCapabilityRecord:
        descriptor = self.describe(method_id)
        if method_id != LOCAL_METHOD or backend_id != descriptor.backend_id or profile not in descriptor.profiles:
            raise unsupported("Unsupported Local Method, Backend or CI")
        observed = self.effective_env
        reason = observed.reason
        if reason is None and (observed.distribution_version != LOCAL_VERSION
                               or not valid_sha256(observed.api_signature_hash)):
            reason = "BACKEND_API_MISMATCH"
        if reason is None and method_id not in self.backend_factories:
            reason = "METHOD_PROFILE_UNAVAILABLE"
        return BackendCapabilityRecord(method_id, backend_id, observed.distribution_version,
                                       descriptor.adapter_version, observed.api_signature_hash,
                                       descriptor.extra, profile, reason is None, reason)

    def load_adapter(self, capability: BackendCapabilityRecord):
        if capability != self.resolve(capability.method_id, capability.backend_id, capability.profile):
            raise backend_error("BACKEND_API_MISMATCH", "Stale or inconsistent capability")
        if not capability.available:
            raise backend_error(capability.reason or "BACKEND_UNAVAILABLE", "Selected adapter unavailable")
        try:
            return self.backend_factories[capability.method_id]()
        except ImportError as error:
            raise backend_error("BACKEND_UNAVAILABLE", "Selected adapter import failed") from error


@dataclass(frozen=True)
class LocalMethodCapabilityAdapter:
    registry: MethodCapabilityRegistry

    def resolve(self, request: ValidatedCapabilityRequest) -> BackendCapabilityRecord:
        if type(request) is not ValidatedCapabilityRequest:
            raise unsupported("Expected validated capability request")
        request.validate()
        return self.registry.resolve(request.method_id, request.backend_id, request.profile)
