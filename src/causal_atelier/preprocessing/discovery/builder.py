from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd

from causal_atelier.preprocessing.common import drop_collinear_columns

from causal_atelier.causal.discovery.results import PreprocessingResult
from .aggregations import build_transaction_features
from .config import FeatureConfig
from .encoders import (
    apply_configured_transforms,
)
from .metadata import build_variable_metadata
from .source_features import (
    build_baseline_features,
    build_treatment_frame,
)
from .tables import (
    build_campaign_window,
    build_household_index,
    table_frame,
)


class AbstractPreprocessor(ABC):
    """因果探索に投入できるモデルデータを生成する preprocessor のインターフェース。"""

    @abstractmethod
    def preprocess(self) -> PreprocessingResult:
        """前処理を実行し、中間生成物を含む結果を返す。

        Returns:
            モデルフレーム、探索入力、標準化済み入力、変数メタデータを含む結果。
        """
        raise NotImplementedError


class CompleteJourneyPreprocessor(AbstractPreprocessor):
    """Complete Journey の因果探索用特徴量を構築・標準化する。

    このクラスは探索パイプラインにおける feature builder の中心である。
    raw table を世帯単位の特徴量に集約し、設定された対数変換を適用し、
    定数列と高相関列を落としてから z-score 標準化する。推論側の
    ``FeatureBuilder`` と同じ責務階層に置くため、探索側でも
    ``features.builder`` 配下に配置している。

    Args:
        tables: logical table name を key とする入力テーブル。
        campaign_id: 分析対象キャンペーン ID。
        pre_weeks: treatment 前として使う週数。
        collinearity_threshold: 冗長列を落とす絶対相関閾値。
        feature_config: 探索用特徴量生成設定。
    """

    def __init__(
        self,
        *,
        tables: dict[str, pd.DataFrame],
        campaign_id: str,
        pre_weeks: int,
        collinearity_threshold: float,
        feature_config: FeatureConfig,
    ) -> None:
        """preprocessor を初期化する。"""
        self.tables = tables
        self.campaign_id = campaign_id
        self.pre_weeks = pre_weeks
        self.collinearity_threshold = collinearity_threshold
        self.feature_config = feature_config

    def preprocess(self) -> PreprocessingResult:
        """特徴量生成、設定変換、標準化を一括で実行する。

        Returns:
            各段階のデータフレームと変数メタデータ。
        """
        model_frame = self.build_model_frame(self.tables)
        feature_names = [spec.name for spec in self.feature_config.used_feature_specs()]
        raw_discovery_frame = model_frame.loc[:, feature_names]
        discovery_frame, transform_by_column = apply_configured_transforms(
            raw_discovery_frame,
            self.feature_config,
        )
        standardized = self.standardize(discovery_frame)
        variable_metadata = build_variable_metadata(
            self.feature_config,
            columns=list(discovery_frame.columns),
            retained_columns=list(standardized.columns),
            transform_by_column=transform_by_column,
        )
        return PreprocessingResult(
            model_frame=model_frame.reset_index(),
            raw_discovery_frame=raw_discovery_frame.reset_index(drop=True),
            discovery_frame=discovery_frame.reset_index(drop=True),
            standardized=standardized.reset_index(drop=True),
            variable_metadata=variable_metadata,
        )

    def build_model_frame(self, tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
        """標準化前の世帯単位 feature frame を作る。

        Args:
            tables: logical table name を key とする入力テーブル。

        Returns:
            世帯 ID を index に持つ feature frame。
        """
        transactions = table_frame(tables, self.feature_config, "transactions")
        households = build_household_index(transactions, self.feature_config)
        window = build_campaign_window(
            campaign_descriptions=table_frame(
                tables,
                self.feature_config,
                "campaign_descriptions",
            ),
            transactions=transactions,
            campaign_id=self.campaign_id,
            feature_config=self.feature_config,
            pre_weeks=self.pre_weeks,
        )

        frames = [
            build_baseline_features(
                table_frame(tables, self.feature_config, "demographics"),
                households,
                self.feature_config,
            ),
            build_transaction_features(
                transactions,
                households,
                window,
                self.feature_config,
            ),
            build_treatment_frame(
                table_frame(tables, self.feature_config, "campaigns"),
                households,
                self.campaign_id,
                self.feature_config,
            ),
        ]
        return pd.concat(frames, axis=1)

    def drop_collinear_columns(self, frame: pd.DataFrame) -> pd.DataFrame:
        """絶対相関が閾値以上の列を落とす。

        Args:
            frame: 数値特徴量フレーム。

        Returns:
            冗長列を除去したフレーム。
        """
        retained, _ = drop_collinear_columns(
            frame,
            collinearity_threshold=self.collinearity_threshold,
        )
        return retained

    def standardize(self, frame: pd.DataFrame) -> pd.DataFrame:
        """定数列・高相関列を落として z-score 標準化する。

        Args:
            frame: 数値の探索特徴量フレーム。

        Returns:
            探索アルゴリズムへ渡す標準化済みフレーム。
        """
        standardized = frame.copy()
        std = standardized.std(axis=0)
        non_constant = std[std > 0].index
        standardized = standardized.loc[:, non_constant]
        standardized = self.drop_collinear_columns(standardized)
        return (standardized - standardized.mean(axis=0)) / standardized.std(axis=0)
