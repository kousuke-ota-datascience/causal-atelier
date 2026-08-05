"""ScientificCore port protocol."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from ariadne.product.domain.enums import ScientificStatus


@dataclass(frozen=True)
class DiscoveryInput:
    dataset_path: Path
    algorithm: str
    parameters: dict[str, Any] = field(default_factory=dict)
    random_seed: int | None = None
    analysis_spec: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EstimationInput:
    dataset_path: Path
    graph_path: Path
    estimator: str
    parameters: dict[str, Any] = field(default_factory=dict)
    random_seed: int | None = None
    analysis_spec: dict[str, Any] = field(default_factory=dict)


@dataclass
class DiscoveryOutput:
    scientific_status: ScientificStatus
    graph_type: str = "CPDAG"
    graph_json: dict[str, Any] = field(default_factory=dict)
    summary: dict[str, Any] = field(default_factory=dict)
    diagnostics: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    artifacts: list[Path] = field(default_factory=list)


@dataclass
class EstimationOutput:
    scientific_status: ScientificStatus
    payload: dict[str, Any] = field(default_factory=dict)
    summary: dict[str, Any] = field(default_factory=dict)
    diagnostics: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    artifacts: list[Path] = field(default_factory=list)


class ScientificCorePort(Protocol):
    def run_discovery(
        self, input_: DiscoveryInput, output_dir: Path
    ) -> DiscoveryOutput: ...

    def run_estimation(
        self, input_: EstimationInput, output_dir: Path
    ) -> EstimationOutput: ...
