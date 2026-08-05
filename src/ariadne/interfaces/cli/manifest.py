"""Portable local CLI manifest."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class CliManifest:
    manifest_version: str
    operation: str
    dataset: dict[str, Any]
    graph: dict[str, Any] | None
    algorithm_or_estimator: str
    parameters: dict[str, Any]
    analysis_spec: dict[str, Any]
    random_seed: int | None
    code_version: str
    runtime_versions: dict[str, str]
    scientific_status: str
    result_summary: dict[str, Any]
    artifacts: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
