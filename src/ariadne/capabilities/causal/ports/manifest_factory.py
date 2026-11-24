"""Application-visible strict evidence values and the Local Manifest factory port."""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol

from ariadne.capabilities.causal.ports.local_io import ManifestValue
from ariadne.causal.design.study import ValidatedStudy, freeze_json, thaw_json
from ariadne.scientific.ports.artifacts import ArtifactDescriptorView
from ariadne.shared.content_ref import ContentRef, ContractViolation, valid_sha256
from ariadne.shared.serialization import jcs


def _snapshot(data: Mapping[str, object]) -> Mapping[str, object]:
    try:
        if not isinstance(data, Mapping):
            raise ValueError("Expected a JSON mapping")
        plain = thaw_json(data)
        jcs.canonical_bytes(plain)
        return freeze_json(plain)
    except (ValueError, RecursionError) as error:
        raise ContractViolation("SCHEMA_INVALID", "publication", "Invalid Manifest evidence snapshot") from error


@dataclass(frozen=True)
class ManifestArtifactFacts:
    key: str
    sha256: str
    size_bytes: int
    media_type: str
    privacy_class: str
    visibility: str

    @classmethod
    def snapshot(cls, descriptor: ArtifactDescriptorView) -> ManifestArtifactFacts:
        try:
            fields = {name: getattr(descriptor, name) for name in cls.__annotations__}
            expected = {"size_bytes": int}
            if any(type(value) is not expected.get(name, str) for name, value in fields.items()):
                raise ValueError("Invalid stage descriptor fields")
            return cls(**fields)
        except (AttributeError, ValueError) as error:
            raise ContractViolation("SCHEMA_INVALID", "publication", "Invalid Stage Artifact Descriptor") from error


@dataclass(frozen=True)
class ManifestRuntimeFacts:
    repo_commit: str
    dirty: bool
    python_version: str
    platform: str
    uv_lock_sha256: str
    distributions: Mapping[str, object]
    api_probes: Mapping[str, object]

    def __post_init__(self) -> None:
        for key in ("distributions", "api_probes"):
            object.__setattr__(self, key, _snapshot(getattr(self, key)))
        if not valid_sha256(self.uv_lock_sha256):
            raise ContractViolation("HASH_INVALID", "publication", "Invalid runtime lock digest")


@dataclass(frozen=True)
class ManifestBuildEvidence:
    study: ValidatedStudy
    study_payload: Mapping[str, object]
    status_payload: Mapping[str, object]
    runtime: ManifestRuntimeFacts
    stochastic: Mapping[str, object]
    artifact_descriptors: tuple[ArtifactDescriptorView, ...]
    output_graph_ref: ContentRef | None
    graph_negative_reason_codes: tuple[str, ...]
    review_science_evidence_ref: ContentRef | None

    def __post_init__(self) -> None:
        if (
            type(self.study) is not ValidatedStudy or type(self.runtime) is not ManifestRuntimeFacts
            or type(self.artifact_descriptors) is not tuple
            or type(self.graph_negative_reason_codes) is not tuple
            or any(type(code) is not str for code in self.graph_negative_reason_codes)
            or any(ref is not None and type(ref) is not ContentRef
                   for ref in (self.output_graph_ref, self.review_science_evidence_ref))
        ):
            raise ContractViolation("SCHEMA_INVALID", "publication", "Invalid typed Manifest evidence")
        for key in ("study_payload", "status_payload", "stochastic"):
            object.__setattr__(self, key, _snapshot(getattr(self, key)))
        object.__setattr__(self, "artifact_descriptors",
                           tuple(ManifestArtifactFacts.snapshot(item) for item in self.artifact_descriptors))


class LocalManifestFactoryPort(Protocol):
    def build(self, *, evidence: ManifestBuildEvidence) -> ManifestValue: ...
