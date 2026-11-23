"""Typed P04 Local capability request and port."""
from dataclasses import dataclass
from typing import Protocol

from ariadne.causal.design.study import ValidatedStudy
from ariadne.scientific.capabilities import (
    CI_PROFILES, LOCAL_BACKEND, LOCAL_METHOD, BackendCapabilityRecord, unsupported,
)


@dataclass(frozen=True)
class ValidatedCapabilityRequest:
    study: ValidatedStudy
    design: object
    method_id: str
    backend_id: str
    profile: str

    def validate(self) -> None:
        from ariadne.causal.discovery.contracts import DiscoveryDesign

        if type(self.study) is not ValidatedStudy or type(self.design) is not DiscoveryDesign:
            raise unsupported("Expected validated Study and Design")
        wire = self.study.to_payload()
        method = wire.get("method")
        if type(method) is not dict or type(method.get("config")) is not dict:
            raise unsupported("Expected validated Method configuration")
        if (
            wire.get("operation") != "DISCOVER" or wire.get("analysis_mode") != "EXPLORATORY"
            or not self.study.estimand.is_graph_structure()
            or wire.get("inference") != {"requested": False, "confidence_level": None}
            or (self.method_id, self.backend_id) != (LOCAL_METHOD, LOCAL_BACKEND)
            or self.profile not in CI_PROFILES
            or (method.get("id"), method.get("backend"), method["config"].get("indep_test"))
            != (self.method_id, self.backend_id, self.profile)
            or self.design.measurement_scale != ("CONTINUOUS" if self.profile == "fisherz" else "CATEGORICAL")
        ):
            raise unsupported("Unsupported Local Discovery capability or Design")


class MethodCapabilityPort(Protocol):
    def resolve(self, request: ValidatedCapabilityRequest) -> BackendCapabilityRecord: ...
