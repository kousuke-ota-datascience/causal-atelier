from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from ariadne.preprocessing.common import CampaignWindow


@dataclass(frozen=True)
class PreprocessingResult:
    """探索前処理の出力をまとめるコンテナ。

    Attributes:
        model_frame: 探索対象列の選択前に作られる世帯単位 feature frame。
        raw_discovery_frame: 設定変換前の探索特徴量。
        discovery_frame: 設定変換後、標準化前の探索特徴量。
        standardized: 探索アルゴリズムに渡す標準化済み特徴量。
        variable_metadata: 探索変数の役割・型・変換情報。
    """

    model_frame: pd.DataFrame
    raw_discovery_frame: pd.DataFrame
    discovery_frame: pd.DataFrame
    standardized: pd.DataFrame
    variable_metadata: pd.DataFrame


@dataclass(frozen=True)
class DiscoveryResult:
    """1 つの探索アルゴリズムの結果を表すコンテナ。

    Attributes:
        algorithm: アルゴリズム名。
        causal_graph: アルゴリズムが返した native graph/model object。
        edges: 共通 schema に正規化した edge table。
        status: ``ok``、``skipped``、または ``failed``。
        message: 空文字、または失敗・skip 理由。
    """

    algorithm: str
    causal_graph: object | None
    edges: pd.DataFrame
    status: str
    message: str
