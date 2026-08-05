"""特徴量設定に基づいて世帯単位の分析フレームを構築する。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

from ariadne.preprocessing.common import (
    CampaignWindow,
    drop_collinear_columns as common_drop_collinear_columns,
    select_campaign_window as common_select_campaign_window,
    window_bounds as common_window_bounds,
)

from .aggregations import aggregate_metrics
from .config import EncodingSpec, FeatureConfig
from .encoders import (
    encode_binary_with_unknown,
    encode_kids_count,
    encode_numeric_extract,
    encode_one_hot,
    encode_ordinal_map,
)


@dataclass(frozen=True)
class FeatureBuildResult:
    """分析 mode が利用する特徴量生成結果。

    Attributes:
        model_frame: raw source column を含む世帯単位フレーム。
        inference_frame: treatment effect と original-scale edge coefficient に
            使う、未標準化の数値フレーム。
        standardized: standardized edge coefficient に使う z-score フレーム。
        dropped_columns: 標準化前に除外した列と理由。
    """

    model_frame: pd.DataFrame
    inference_frame: pd.DataFrame
    standardized: pd.DataFrame
    dropped_columns: pd.DataFrame


class FeatureBuilder:
    """raw table と特徴量設定から世帯単位の分析フレームを作る。

    この builder は Complete Journey の transaction・demographics・campaign
    membership を household-level の分析単位へ変換する。集約、カテゴリ
    encoding、調整変数候補は ``FeatureConfig`` から読み取るため、Python 実装を
    変えずに YAML 側で分析設計を調整できる。

    推論側では treatment effect 推定と edge weight 推定の両方が同じ特徴量を
    参照するため、未標準化フレームと標準化フレームの両方を返す。

    Args:
        feature_config: YAML から読み込んだ特徴量生成仕様。

    Attributes:
        feature_config: validation 済み特徴量生成仕様。
    """

    def __init__(self, feature_config: FeatureConfig) -> None:
        """builder を初期化する。"""
        self.feature_config = feature_config

    def build(
        self,
        tables: dict[str, pd.DataFrame],
        campaign_id: str,
        pre_weeks: int,
        collinearity_threshold: float,
    ) -> FeatureBuildResult:
        """世帯単位の分析フレームを構築する。

        Args:
            tables: logical table name から raw data frame への mapping。
            campaign_id: treatment と分析 window を定義する campaign ID。
            pre_weeks: campaign 開始前に pre-treatment window として使う週数。
            collinearity_threshold: 標準化前に冗長列を落とす絶対相関閾値。

        Returns:
            original scale と standardized scale のフレームを含む生成結果。

        Raises:
            ValueError: 必須テーブルまたは設定列が不足している場合。
        """
        model_frame = self.build_model_frame(tables, campaign_id, pre_weeks)
        inference_frame = self.build_inference_frame(model_frame)
        standardized, dropped_columns = self.standardize(
            inference_frame,
            collinearity_threshold=collinearity_threshold,
        )
        configured_notes = pd.DataFrame(
            list(self.feature_config.validation.dropped_column_notes),
            columns=["column", "reason"],
        )
        if not configured_notes.empty:
            dropped_columns = pd.concat([dropped_columns, configured_notes], ignore_index=True)
        return FeatureBuildResult(
            model_frame=model_frame.reset_index(),
            inference_frame=inference_frame.reset_index(drop=True),
            standardized=standardized.reset_index(drop=True),
            dropped_columns=dropped_columns,
        )

    def build_model_frame(
        self,
        tables: dict[str, pd.DataFrame],
        campaign_id: str,
        pre_weeks: int,
    ) -> pd.DataFrame:
        """数値 encoding 前の household-indexed frame を作る。

        Args:
            tables: logical table name を key とする source table。
            campaign_id: 分析対象 campaign ID。
            pre_weeks: pre-treatment として使う週数。

        Returns:
            raw demographics、設定済み集約、treatment を含む model frame。
        """
        transactions = self._table(tables, "transactions")
        campaigns = self._table(tables, "campaigns")
        demographics = self._table(tables, "demographics")
        campaign_descriptions = self._table(tables, "campaign_descriptions")
        unit_key = self.feature_config.dataset.unit_key

        households = pd.Index(transactions[unit_key].dropna().unique(), name=unit_key)
        frame = pd.DataFrame(index=households)

        window = self.select_campaign_window(
            campaign_descriptions=campaign_descriptions,
            transactions=transactions,
            campaign_id=campaign_id,
            pre_weeks=pre_weeks,
        )

        for block in self.feature_config.aggregations.values():
            source = self._table(tables, block.source_table)
            aggregated = self.aggregate_block(source, block_name=block.prefix, window=window)
            frame = frame.join(aggregated.set_index(list(block.group_by)))

        aggregated_columns = [
            column
            for column in frame.columns
            if any(column.startswith(f"{block.prefix}_") for block in self.feature_config.aggregations.values())
        ]
        frame[aggregated_columns] = frame[aggregated_columns].fillna(0.0)

        treatment_name = str(self.feature_config.treatment.get("name", "treated"))
        treatment_campaign_col = str(
            self.feature_config.treatment.get("campaign_id_column", "campaign_id")
        )
        treatment_household_col = str(
            self.feature_config.treatment.get("household_key_column", unit_key)
        )
        treated_households = campaigns.loc[
            campaigns[treatment_campaign_col].astype(str).eq(str(campaign_id)),
            treatment_household_col,
        ]
        frame[treatment_name] = frame.index.isin(treated_households).astype(int)

        demographics_key = self.feature_config.tables["demographics"].household_key or unit_key
        demographic_columns = list(
            dict.fromkeys(spec.input_column for spec in self.feature_config.encodings.values())
        )
        aligned_demographics = demographics.set_index(demographics_key).reindex(households)
        for column in demographic_columns:
            frame[column] = aligned_demographics[column].astype("string").fillna("Unknown")

        return frame

    def aggregate_block(
        self,
        frame: pd.DataFrame,
        *,
        block_name: str,
        window: CampaignWindow,
    ) -> pd.DataFrame:
        """設定された transaction 集約 block を 1 つ計算する。

        Args:
            frame: source table。
            block_name: aggregation block の prefix。
            window: campaign-relative window。

        Returns:
            group key 列を含む集約済み feature frame。

        Raises:
            ValueError: block が未対応 window を参照する場合。
        """
        block = next(
            candidate
            for candidate in self.feature_config.aggregations.values()
            if candidate.prefix == block_name
        )
        start_week, end_week = self.window_bounds(window, block.window)
        time_key = self.feature_config.dataset.time_key
        needed_columns = set(block.group_by)
        for metric in block.metrics.values():
            if metric.column is not None:
                needed_columns.add(metric.column)
        filtered = frame.loc[
            frame[time_key].between(start_week, end_week),
            list(needed_columns),
        ]
        return aggregate_metrics(
            filtered,
            group_by=list(block.group_by),
            metrics=block.metrics,
            prefix=block.prefix,
        )

    def build_inference_frame(self, model_frame: pd.DataFrame) -> pd.DataFrame:
        """raw model-frame 列を推論用の数値列へ encoding する。

        Args:
            model_frame: encoding 前の household-indexed frame。

        Returns:
            original scale の数値 inference frame。
        """
        output = pd.DataFrame(index=model_frame.index)
        for spec in self.feature_config.encodings.values():
            self._append_encoded_columns(output, model_frame[spec.input_column], spec)

        for block in self.feature_config.aggregations.values():
            for metric_name in block.metrics:
                column = f"{block.prefix}_{metric_name}"
                output[column] = model_frame[column].astype(float)

        treatment_name = str(self.feature_config.treatment.get("name", "treated"))
        output[treatment_name] = model_frame[treatment_name].astype(float)

        for block in self.feature_config.aggregations.values():
            if block.window != "outcome":
                continue
            for metric_name in block.metrics:
                column = f"{block.prefix}_{metric_name}"
                if column not in output:
                    output[column] = model_frame[column].astype(float)

        ordered = self._legacy_column_order(output.columns)
        return output.loc[:, ordered]

    def _append_encoded_columns(
        self,
        output: pd.DataFrame,
        source: pd.Series,
        spec: EncodingSpec,
    ) -> None:
        """encoding 済み列を output frame に追加する。

        Args:
            output: 追加先の mutable frame。
            source: encoding 対象 series。
            spec: encoding 仕様。

        Raises:
            ValueError: encoding type が未対応、または設定が不完全な場合。
        """
        if spec.type == "ordinal_map":
            if spec.output is None or spec.map is None:
                raise ValueError(f"ordinal_map requires output and map: {spec.input_column}")
            output[spec.output] = encode_ordinal_map(
                source,
                spec.map,
                unknown_value=spec.unknown_value,
            )
            return
        if spec.type == "unknown_indicator":
            if spec.output is None:
                raise ValueError(f"unknown_indicator requires output: {spec.input_column}")
            unknown_values = {"Unknown", *(str(item) for item in spec.unknown_values if item is not None)}
            output[spec.output] = (
                source.isna() | source.astype("string").isin(unknown_values)
            ).astype(float)
            return
        if spec.type == "numeric_extract":
            if spec.output is None:
                raise ValueError(f"numeric_extract requires output: {spec.input_column}")
            output[spec.output] = encode_numeric_extract(
                source,
                unknown_value=spec.unknown_value,
            )
            return
        if spec.type == "kids_count":
            if spec.output is None:
                raise ValueError(f"kids_count requires output: {spec.input_column}")
            output[spec.output] = encode_kids_count(
                source,
                unknown_value=spec.unknown_value,
            )
            return
        if spec.type == "binary_with_unknown":
            if spec.output_positive is None or spec.output_unknown is None:
                raise ValueError(
                    f"binary_with_unknown requires output columns: {spec.input_column}"
                )
            encoded = encode_binary_with_unknown(source, spec.positive_values)
            aliases = spec.aliases or {}
            for alias, target in aliases.items():
                if target == spec.output_positive:
                    output[alias] = encoded["positive"]
            output[spec.output_positive] = encoded["positive"]
            output[spec.output_unknown] = encoded["unknown"]
            return
        if spec.type == "one_hot":
            if spec.output is None:
                raise ValueError(f"one_hot requires output prefix: {spec.input_column}")
            encoded = encode_one_hot(source, spec.output)
            for column in encoded.columns:
                output[column] = encoded[column]
            return
        raise ValueError(f"unsupported encoding type: {spec.type}")

    def standardize(
        self,
        frame: pd.DataFrame,
        *,
        collinearity_threshold: float,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """推定不能列を落とし、残った特徴量を z-score 標準化する。

        Args:
            frame: 数値 inference frame。
            collinearity_threshold: 冗長列を落とす絶対相関閾値。

        Returns:
            標準化済み frame と dropped-column table の pair。
        """
        numeric = frame.apply(pd.to_numeric, errors="coerce")
        records: list[dict[str, Any]] = []
        for column in frame.columns:
            if numeric[column].isna().all():
                records.append({"column": column, "reason": "all_missing"})
            elif not pd.api.types.is_numeric_dtype(frame[column]):
                records.append({"column": column, "reason": "non_numeric"})

        kept = numeric.drop(columns=[record["column"] for record in records])
        std = kept.std(axis=0)
        constant_columns = std[std <= 0].index.tolist()
        records.extend(
            {"column": column, "reason": "constant"}
            for column in constant_columns
        )
        kept = kept.drop(columns=constant_columns)
        kept, collinear = common_drop_collinear_columns(
            kept,
            collinearity_threshold=collinearity_threshold,
        )
        if not collinear.empty:
            records.extend(collinear.to_dict(orient="records"))
        standardized = (kept - kept.mean(axis=0)) / kept.std(axis=0)
        return standardized, pd.DataFrame(records, columns=["column", "reason"])

    def drop_collinear_columns(
        self,
        frame: pd.DataFrame,
        *,
        collinearity_threshold: float,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """絶対相関が閾値以上の列を落とす。

        Args:
            frame: 数値 feature frame。
            collinearity_threshold: 絶対相関閾値。

        Returns:
            retained frame と dropped-column table の pair。
        """
        return common_drop_collinear_columns(
            frame,
            collinearity_threshold=collinearity_threshold,
        )

    def select_campaign_window(
        self,
        *,
        campaign_descriptions: pd.DataFrame,
        transactions: pd.DataFrame,
        campaign_id: str,
        pre_weeks: int,
    ) -> CampaignWindow:
        """campaign の pre-treatment/outcome 週を選択する。

        Args:
            campaign_descriptions: campaign 日付テーブル。
            transactions: 全体の週範囲を推定する transaction table。
            campaign_id: campaign ID。
            pre_weeks: pre-treatment 週数。

        Returns:
            campaign window。

        Raises:
            ValueError: campaign が未知、または usable な週がない場合。
        """
        campaign_table = self.feature_config.tables["campaign_descriptions"]
        transaction_table = self.feature_config.tables["transactions"]
        campaign_id_column = campaign_table.campaign_id or "campaign_id"
        start_column = campaign_table.start_day or "start_date"
        end_column = campaign_table.end_day or "end_date"
        week_column = transaction_table.week or self.feature_config.dataset.time_key
        timestamp_column = transaction_table.transaction_timestamp or "transaction_timestamp"
        divisor = int(
            _nested_get(
                self.feature_config.windows,
                ["campaign_dates", "day_to_week", "divisor"],
                default=7,
            )
        )

        return common_select_campaign_window(
            campaign_descriptions=campaign_descriptions,
            transactions=transactions,
            campaign_id=campaign_id,
            campaign_id_column=campaign_id_column,
            start_day_column=start_column,
            end_day_column=end_column,
            week_column=week_column,
            transaction_timestamp_column=timestamp_column,
            pre_weeks=pre_weeks,
            day_to_week_divisor=divisor,
        )

    def window_bounds(self, window: CampaignWindow, name: str) -> tuple[int, int]:
        """設定 window 名に対応する週範囲を返す。

        Args:
            window: campaign-relative window。
            name: ``pre`` や ``outcome`` などの window 名。

        Returns:
            両端を含む ``(start_week, end_week)``。

        Raises:
            ValueError: window 名が未対応の場合。
        """
        return common_window_bounds(window, name)

    def _table(self, tables: dict[str, pd.DataFrame], logical_name: str) -> pd.DataFrame:
        """logical name から設定済み table を返す。

        Args:
            tables: Tables keyed by logical name.
            logical_name: Requested logical name.

        Returns:
            Source data frame.

        Raises:
            ValueError: If the table is missing.
        """
        if logical_name not in tables:
            raise ValueError(f"missing required logical table: {logical_name}")
        return tables[logical_name]

    def _legacy_column_order(self, columns: pd.Index) -> list[str]:
        """存在する列について旧実装互換の列順を返す。

        Args:
            columns: Available output columns.

        Returns:
            Ordered column names.
        """
        preferred = [
            "age_midpoint",
            "age_unknown",
            "income_midpoint_k",
            "income_unknown",
            "homeowner",
            "homeowner_yes",
            "homeowner_unknown",
            "married",
            "married_yes",
            "married_unknown",
            "household_size",
            "kids_count",
            "pre_baskets",
            "pre_quantity",
            "pre_sales_value",
            "pre_retail_disc",
            "pre_coupon_disc",
            "pre_coupon_match_disc",
            "treated",
            "outcome_baskets",
            "outcome_quantity",
            "outcome_sales_value",
            "outcome_retail_disc",
            "outcome_coupon_disc",
            "outcome_coupon_match_disc",
        ]
        available = list(columns)
        ordered = [column for column in preferred if column in available]
        ordered.extend(column for column in available if column not in ordered)
        return ordered


def _nested_get(mapping: dict[str, Any], keys: list[str], default: Any) -> Any:
    """ネストした mapping から値を読み、なければ default を返す。

    Args:
        mapping: Source mapping.
        keys: Nested key path.
        default: Value returned when any key is missing.

    Returns:
        Nested value or ``default``.
    """
    current: Any = mapping
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current
