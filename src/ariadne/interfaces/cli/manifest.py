"""CLI manifest schema for ariadne-discover and ariadne-estimate commands."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class DiscoveryManifest:
    """Manifest written by ariadne-discover on successful completion."""

    manifest_version: str
    ariadne_version: str
    algorithm: str
    dataset_path: str
    dataset_hash: str
    parameters: dict[str, Any]
    random_seed: int | None
    scientific_status: str
    graph_json: dict[str, Any]
    summary: dict[str, Any]
    output_dir: str
    artifacts: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class EstimationManifest:
    """Manifest written by ariadne-estimate on successful completion."""

    manifest_version: str
    ariadne_version: str
    estimator: str
    dataset_path: str
    dataset_hash: str
    graph_path: str
    graph_hash: str
    parameters: dict[str, Any]
    analysis_spec: dict[str, Any]
    random_seed: int | None
    scientific_status: str
    payload: dict[str, Any]
    summary: dict[str, Any]
    output_dir: str
    artifacts: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
