"""Immutable Local capability metadata and effective runtime observations."""
from dataclasses import dataclass

from ariadne.shared.content_ref import ContractViolation


def unsupported(message: str) -> ContractViolation:
    return ContractViolation("UNSUPPORTED_COMBINATION", "configuration", message)


def backend_error(code: str, message: str) -> ContractViolation:
    return ContractViolation(code, "engine", message)


CI_PROFILES = ("fisherz", "chisq", "gsq")
LOCAL_METHOD = "P1-M06"
LOCAL_BACKEND = "causal-learn"
LOCAL_VERSION = "0.1.4.8"


@dataclass(frozen=True)
class MethodDescriptor:
    method_id: str
    operation: str
    estimand: str
    inference_requested: bool
    backend_id: str
    profiles: tuple[str, ...]
    adapter_version: str
    extra: str | None = None


@dataclass(frozen=True)
class BackendCapabilityRecord:
    method_id: str
    backend_id: str
    distribution_version: str | None
    adapter_version: str
    api_signature_hash: str | None
    extra: str | None
    profile: str
    available: bool
    reason: str | None

    def check(self, request) -> None:
        request.validate()
        if (self.method_id, self.backend_id, self.profile) != (
            request.method_id, request.backend_id, request.profile,
        ):
            raise unsupported("Capability does not match the validated request")
        if not self.available:
            raise backend_error(self.reason or "BACKEND_UNAVAILABLE", "Selected Backend is unavailable")
