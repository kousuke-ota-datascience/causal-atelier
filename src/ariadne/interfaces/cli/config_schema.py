"""Strict local CLI configuration contracts."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class DiscoveryCliConfig(_Strict):
    config_version: Literal["1.0"]
    dataset: Path
    dataset_hash: str | None = None
    algorithm: Literal["pc", "ges", "lingam", "notears"]
    parameters: dict[str, Any] = Field(default_factory=dict)
    analysis_spec: dict[str, Any]
    random_seed: int | None = None
    output_dir: Path


class EstimationCliConfig(_Strict):
    config_version: Literal["1.0"]
    dataset: Path
    dataset_hash: str | None = None
    graph: Path
    graph_hash: str | None = None
    estimator: Literal["difference_in_means", "diff_in_means", "ols", "outcome_regression", "ipw", "aipw"]
    parameters: dict[str, Any] = Field(default_factory=dict)
    analysis_spec: dict[str, Any]
    random_seed: int | None = None
    output_dir: Path
