"""Feature semantics and stage-independent feature utilities."""

from .semantics import (
    FeatureRole,
    FeatureSemanticSpec,
    FeatureSemanticsCatalog,
    compare_feature_semantics,
)
from .windowing import (
    CampaignWindow,
    drop_collinear_columns,
    select_campaign_window,
    window_bounds,
)

__all__ = [
    "CampaignWindow",
    "FeatureRole",
    "FeatureSemanticSpec",
    "FeatureSemanticsCatalog",
    "compare_feature_semantics",
    "drop_collinear_columns",
    "select_campaign_window",
    "window_bounds",
]
