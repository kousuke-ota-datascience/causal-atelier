"""Framework-free boundary between Product and the scientific implementation."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from ariadne.product.domain.enums import ResultType, ScientificStatus


@dataclass(frozen=True)
class ArtifactDescriptor:
    path: Path
    content_role: str = "SCIENTIFIC_RESULT"


@dataclass(frozen=True)
class ScientificResultDescriptor:
    result_type: ResultType
    scientific_status: ScientificStatus
    summary: dict[str, Any] = field(default_factory=dict)
    payload: dict[str, Any] = field(default_factory=dict)
    diagnostics: dict[str, Any] = field(default_factory=dict)
    warnings: list[dict[str, Any] | str] = field(default_factory=list)
    artifacts: list[ArtifactDescriptor] = field(default_factory=list)


class ScientificResultBatch(list[ScientificResultDescriptor]):
    """A list with read-only legacy projections used by local integrations."""

    @property
    def scientific_status(self) -> ScientificStatus:
        return self[0].scientific_status

    @property
    def summary(self) -> dict[str, Any]:
        return self[0].summary

    @property
    def payload(self) -> dict[str, Any]:
        return self[0].payload

    @property
    def graph_json(self) -> dict[str, Any]:
        return self[0].payload

    @property
    def graph_type(self) -> str:
        return str(self[0].payload.get("graph_type", ""))

    @property
    def diagnostics(self) -> dict[str, Any]:
        return self[0].diagnostics

    @property
    def warnings(self) -> list[dict[str, Any] | str]:
        return [warning for item in self for warning in item.warnings]

    @property
    def artifacts(self) -> list[Path]:
        return [artifact.path for item in self for artifact in item.artifacts]


class DiscoveryOutput(ScientificResultBatch):
    def __init__(
        self, scientific_status: ScientificStatus, graph_type: str = "CPDAG",
        graph_json: dict[str, Any] | None = None, summary: dict[str, Any] | None = None,
        diagnostics: dict[str, Any] | None = None, warnings: list[Any] | None = None,
        artifacts: list[Path] | None = None,
    ) -> None:
        status = ScientificStatus.GENERATED if scientific_status == ScientificStatus.VALID else scientific_status
        super().__init__([ScientificResultDescriptor(
            ResultType.DISCOVERY_GRAPH_RESULT, status, summary or {}, graph_json or {},
            diagnostics or {}, warnings or [], [ArtifactDescriptor(path) for path in artifacts or []],
        )])


class EstimationOutput(ScientificResultBatch):
    def __init__(
        self, scientific_status: ScientificStatus, payload: dict[str, Any] | None = None,
        summary: dict[str, Any] | None = None, diagnostics: dict[str, Any] | None = None,
        warnings: list[Any] | None = None, artifacts: list[Path] | None = None,
    ) -> None:
        status = ScientificStatus.ESTIMATED if scientific_status == ScientificStatus.VALID else scientific_status
        super().__init__([ScientificResultDescriptor(
            ResultType.TREATMENT_EFFECT_RESULT, status, summary or {}, payload or {},
            diagnostics or {}, warnings or [], [ArtifactDescriptor(path) for path in artifacts or []],
        )])


@dataclass(frozen=True)
class DiscoveryInput:
    dataset_path: Path
    algorithm: str
    parameters: dict[str, Any] = field(default_factory=dict)
    random_seed: int | None = None
    analysis_spec: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class IdentificationInput:
    dataset_path: Path
    graph_path: Path
    method: str
    parameters: dict[str, Any] = field(default_factory=dict)
    random_seed: int | None = None
    analysis_spec: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EstimationInput:
    dataset_path: Path
    graph_path: Path
    estimator: str
    upstream_result: dict[str, Any] = field(default_factory=dict)
    parameters: dict[str, Any] = field(default_factory=dict)
    random_seed: int | None = None
    analysis_spec: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RefutationInput:
    dataset_path: Path
    graph_path: Path
    base_result: dict[str, Any]
    method: str
    parameters: dict[str, Any] = field(default_factory=dict)
    random_seed: int | None = None
    analysis_spec: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SensitivityInput:
    dataset_path: Path
    graph_path: Path
    base_result: dict[str, Any]
    dimension: str
    parameters: dict[str, Any] = field(default_factory=dict)
    random_seed: int | None = None
    analysis_spec: dict[str, Any] = field(default_factory=dict)


class ScientificCorePort(Protocol):
    def run_discovery(self, input_: DiscoveryInput, output_dir: Path) -> list[ScientificResultDescriptor]: ...
    def run_identification(self, input_: IdentificationInput, output_dir: Path) -> list[ScientificResultDescriptor]: ...
    def run_estimation(self, input_: EstimationInput, output_dir: Path) -> list[ScientificResultDescriptor]: ...
    def run_refutation(self, input_: RefutationInput, output_dir: Path) -> list[ScientificResultDescriptor]: ...
    def run_sensitivity(self, input_: SensitivityInput, output_dir: Path) -> list[ScientificResultDescriptor]: ...
