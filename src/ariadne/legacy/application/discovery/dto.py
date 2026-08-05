"""Application-layer DTOs for causal discovery."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

import pandas as pd

from ariadne.causal.discovery.config import AnalysisConfig
from ariadne.preprocessing.discovery.config import FeatureConfig


@dataclass(frozen=True)
class DiscoveryInputSpecification:
    """Identifies the input provider and its options.

    Attributes:
        provider_type: Registered provider key (e.g. ``completejourney``).
        options: Provider-specific configuration mapping.
    """

    provider_type: str
    options: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PreparedDiscoveryInput:
    """Normalized input contract returned by any DiscoveryInputProvider.

    Attributes:
        analysis_frame: Standardized frame passed to discovery algorithms.
        raw_frame: Raw feature frame before configured transforms; None if unavailable.
        transformed_frame: Transformed frame before standardization; None if unavailable.
        variable_metadata: DataFrame with variable roles, types, and transform info.
        background_knowledge: causal-learn BackgroundKnowledge object, or None.
            Opaque to the Application Service — created and consumed at the
            infrastructure boundary.
        metadata: Provider-specific key/value pairs for reporting
            (e.g. ``campaign_id``, ``pre_weeks``).
    """

    analysis_frame: pd.DataFrame
    raw_frame: pd.DataFrame | None
    transformed_frame: pd.DataFrame | None
    variable_metadata: pd.DataFrame
    background_knowledge: object | None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DiscoveryRequest:
    """Immutable request consumed by DiscoveryApplicationService.

    Attributes:
        project_root: Resolved repository root.
        analysis_config_path: Resolved path used to load analysis_config (for snapshot).
        feature_config_path: Resolved path for feature config snapshot; None for
            providers that do not use a FeatureConfig file.
        input_specification: Provider selection and options.
        analysis_config: Merged analysis configuration (YAML + CLI overrides applied).
        feature_config: Feature configuration; None for single-table and generic providers.
        output_dir: Resolved root output directory.
    """

    project_root: Path
    analysis_config_path: Path
    feature_config_path: Path | None
    input_specification: DiscoveryInputSpecification
    analysis_config: AnalysisConfig
    feature_config: FeatureConfig | None
    output_dir: Path


@dataclass(frozen=True)
class DiscoveryArtifactResult:
    """Artifact paths written during one discovery execution.

    Attributes:
        artifacts: Mapping from artifact name to absolute path.
    """

    artifacts: dict[str, Path]


@dataclass(frozen=True)
class DiscoveryExecutionResult:
    """Result returned by DiscoveryApplicationService.execute().

    Attributes:
        status: ``ok`` or ``failed``.
        algorithm_results: Per-algorithm DiscoveryResult objects keyed by name.
        artifacts: Written artifact paths keyed by artifact name.
        sample_count: Number of analysis units (rows) in the analysis frame.
        variable_count: Number of variables (columns) in the analysis frame.
        output_dir: Root output directory.
        analysis_config: Final merged analysis configuration.
        metadata: Extra key/value pairs (e.g. provider type, pc_indep_test).
    """

    status: str
    algorithm_results: dict[str, Any]
    artifacts: dict[str, Path]
    sample_count: int
    variable_count: int
    output_dir: Path
    analysis_config: AnalysisConfig
    metadata: dict[str, Any] = field(default_factory=dict)


__all__ = [
    "DiscoveryArtifactResult",
    "DiscoveryExecutionResult",
    "DiscoveryInputSpecification",
    "DiscoveryRequest",
    "PreparedDiscoveryInput",
]
