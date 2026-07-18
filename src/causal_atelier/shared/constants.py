"""Shared constants that are independent of pipeline execution."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(".")
DEFAULT_DATASET_YAML = Path("configs/etl/completejourney/load.yaml")
DEFAULT_CAUSAL_DISCOVERY_DIR = Path("artifacts/pipelines/causal_discovery")
DEFAULT_CAUSAL_INFERENCE_DIR = Path("artifacts/pipelines/causal_inference")

SUPPORTED_DISCOVERY_ALGORITHMS = ("pc", "ges", "lingam", "notears")

__all__ = [
    "DEFAULT_CAUSAL_DISCOVERY_DIR",
    "DEFAULT_CAUSAL_INFERENCE_DIR",
    "DEFAULT_DATASET_YAML",
    "PROJECT_ROOT",
    "SUPPORTED_DISCOVERY_ALGORITHMS",
]
