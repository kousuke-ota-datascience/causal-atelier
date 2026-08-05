"""Common exception hierarchy for the causal pipeline."""

from __future__ import annotations


class CausalPipelineError(Exception):
    """Base exception for expected causal pipeline failures."""


class ConfigValidationError(CausalPipelineError):
    """Raised when YAML or CLI configuration is invalid."""


class FeatureSemanticsError(CausalPipelineError):
    """Raised when feature semantics are missing or inconsistent."""


class ArtifactSchemaError(CausalPipelineError):
    """Raised when an artifact exists but does not satisfy its schema."""


__all__ = [
    "ArtifactSchemaError",
    "CausalPipelineError",
    "ConfigValidationError",
    "FeatureSemanticsError",
]
