"""raw source table から探索用 feature block を構築する処理。"""

from __future__ import annotations

import pandas as pd

from .config import FeatureConfig
from .encoders import apply_feature_transform


def build_baseline_features(
    demographics: pd.DataFrame,
    households: pd.Index,
    feature_config: FeatureConfig,
) -> pd.DataFrame:
    """demographics から世帯単位の baseline features を作る。

    Args:
        demographics: Demographic source table.
        households: Modeling-unit index.
        feature_config: Feature-generation configuration.

    Returns:
        Baseline feature frame indexed by household.
    """
    demographic_table = feature_config.tables["demographics"]
    household_column = demographic_table.household_key or feature_config.metadata["entity_id"]
    aligned = demographics.set_index(household_column).reindex(households)

    frame = pd.DataFrame(index=households)
    for spec in feature_config.features_for_source_table("demographics"):
        frame[spec.name] = apply_feature_transform(
            aligned[spec.source_column],
            spec,
            feature_config,
        )
    return frame


def build_treatment_frame(
    campaigns: pd.DataFrame,
    households: pd.Index,
    campaign_id: str,
    feature_config: FeatureConfig,
) -> pd.DataFrame:
    """campaign membership から treatment indicator frame を作る。

    Args:
        campaigns: Campaign household membership table.
        households: Modeling-unit index.
        campaign_id: Campaign identifier to mark as treated.
        feature_config: Feature-generation configuration.

    Returns:
        Treatment feature frame indexed by household.
    """
    campaign_table = feature_config.tables["campaigns"]
    household_column = campaign_table.household_key or feature_config.metadata["entity_id"]
    campaign_id_column = campaign_table.campaign_id or "campaign_id"

    treated_households = campaigns.loc[
        campaigns[campaign_id_column].astype(str).eq(campaign_id),
        household_column,
    ]
    membership = pd.Series(
        households.isin(treated_households).astype(float),
        index=households,
    )

    frame = pd.DataFrame(index=households)
    for spec in feature_config.features_for_source_table("campaigns"):
        frame[spec.name] = apply_feature_transform(membership, spec, feature_config)
    return frame
