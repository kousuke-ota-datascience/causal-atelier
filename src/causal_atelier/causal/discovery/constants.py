"""因果探索パイプライン固有の定数。

共通の dataset registry path、artifacts path、探索アルゴリズム名は
``causal_atelier.shared.constants`` から受け取る。この module には、因果探索
CLI と探索 feature schema が直接使う既定値と許可リストだけを置く。
"""

from __future__ import annotations

from pathlib import Path

from causal_atelier.shared.constants import (
    DEFAULT_CAUSAL_DISCOVERY_DIR,
    DEFAULT_DATASET_YAML,
    SUPPORTED_DISCOVERY_ALGORITHMS,
)


DEFAULT_ANALYSIS_CONFIG = Path("configs/causal/discovery.yaml")
DEFAULT_FEATURE_CONFIG = Path("configs/preprocessing/discovery_features.yaml")
DEFAULT_OUTPUT_DIR = DEFAULT_CAUSAL_DISCOVERY_DIR

ALLOWED_ALGORITHMS = SUPPORTED_DISCOVERY_ALGORITHMS
ALLOWED_TRANSFORMS = (
    "identity",
    "ordered_category_midpoint",
    "numeric_category",
    "equals",
    "is_missing_or_unknown",
    "campaign_membership",
    "log1p",
    "signed_log1p",
)
ALLOWED_AGGREGATIONS = ("sum", "nunique", "mean", "count")

DEFAULT_PC_INDEP_TESTS = ("fisherz", "kci", "chisq", "gsq")
DEFAULT_DISCRETE_PC_INDEP_TESTS = ("chisq", "gsq")
DEFAULT_ALPHA_GRID = (0.001, 0.005, 0.01, 0.05)
