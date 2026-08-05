"""Complete Journey の dataset registry からテーブルを読み込む共通実装。

探索側も推論側も共通の ``FileConfigRegistry`` を経由して同じ raw/interim
データを読む。差分は「返却辞書を logical name で持つか」「必須列検証を行うか」
だけなので、この loader に集約している。
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from ariadne.infrastructure.config.datasets import load_dataset_definition
from ariadne.infrastructure.logging import CustomLogger
from ariadne.infrastructure.storage.files import FileConfigRegistry, FileIOUtils

from .validation import validate_required_columns


@dataclass(frozen=True)
class TableLoadSpec:
    """dataset registry の 1 entry を読むための正規化済み指定。

    Attributes:
        logical_name: パイプライン内で使う論理テーブル名。
        registry_entry: dataset registry 内の entry 名。
        required_columns: 読込後に存在を検証する列名。
    """

    logical_name: str
    registry_entry: str
    required_columns: tuple[str, ...] = ()

    @classmethod
    def from_config(cls, logical_name: str, spec: Any) -> "TableLoadSpec":
        """各パイプラインの TableSpec 風オブジェクトから読込指定を作る。

        Args:
            logical_name: 設定ファイル上の論理テーブル名。
            spec: 少なくとも ``name`` 属性を持つ設定オブジェクト。

        Returns:
            共通 loader が扱える正規化済み指定。
        """
        return cls(
            logical_name=str(logical_name),
            registry_entry=str(getattr(spec, "name")),
            required_columns=tuple(str(column) for column in getattr(spec, "required_columns", ())),
        )


class DatasetRegistryLoader:
    """dataset registry と ``FileIOUtils`` を使ってテーブルを読む loader。

    Args:
        project_root: dataset registry 内のプレースホルダ解決に使う repository root。
        dataset_yaml: dataset registry YAML。
        logger_name: 読込ログの logger 名。
        log_path: ログファイルパス。省略時は current working directory に
            ``{logger_name}.log`` を作る。
    """

    def __init__(
        self,
        *,
        project_root: Path,
        dataset_yaml: Path,
        logger_name: str,
        log_path: Path | None = None,
    ) -> None:
        """loader を初期化する。"""
        self.project_root = project_root
        self.dataset_yaml = dataset_yaml
        self.logger_name = logger_name
        self.log_path = log_path

    def load_entries(self, table_entries: Iterable[str]) -> dict[str, pd.DataFrame]:
        """registry entry 名の iterable からテーブルを読み込む。

        Args:
            table_entries: dataset registry 上の entry 名。

        Returns:
            entry 名を key、読み込んだデータフレームを value とする辞書。
        """
        specs = {
            str(entry): TableLoadSpec(
                logical_name=str(entry),
                registry_entry=str(entry),
            )
            for entry in table_entries
        }
        return self.load_specs(specs, key_by="registry_entry")

    def load_specs(
        self,
        table_specs: Mapping[str, Any],
        *,
        key_by: str = "logical_name",
    ) -> dict[str, pd.DataFrame]:
        """TableSpec mapping から必要なテーブルを読み込む。

        Args:
            table_specs: 論理テーブル名から各パイプラインの TableSpec への mapping。
            key_by: 返却辞書の key。``"logical_name"`` または
                ``"registry_entry"`` を指定する。

        Returns:
            読み込んだデータフレームの辞書。

        Raises:
            ValueError: ``key_by`` が未対応の場合、または必須列が不足する場合。
        """
        if key_by not in {"logical_name", "registry_entry"}:
            raise ValueError(f"unsupported key_by: {key_by}")

        dataset_definition = load_dataset_definition(self.dataset_yaml, self.project_root)
        registry = FileConfigRegistry.from_mapping(dataset_definition)
        file_io = FileIOUtils(self._logger())

        tables: dict[str, pd.DataFrame] = {}
        for logical_name, spec in table_specs.items():
            load_spec = TableLoadSpec.from_config(str(logical_name), spec)
            frame = file_io.read_file(
                registry.read_config(load_spec.registry_entry),
                use_dask=False,
            )
            validate_required_columns(
                frame,
                load_spec.required_columns,
                load_spec.logical_name,
            )
            output_key = (
                load_spec.logical_name
                if key_by == "logical_name"
                else load_spec.registry_entry
            )
            tables[output_key] = frame
        return tables

    def _logger(self):
        """FileIOUtils に渡す logger を作成する。"""
        log_path = self.log_path or Path.cwd() / f"{self.logger_name}.log"
        return CustomLogger(self.logger_name, log_path).get_logger()


class LogicalTableDataLoader:
    """pipeline 固有 loader の共通 base class。

    dataset registry の読込自体は ``DatasetRegistryLoader`` が担う。この class は、
    各 pipeline が持つ logical table spec を受け取り、``load_all`` と
    ``load_tables`` の public API を共通化するための薄い wrapper である。

    Args:
        project_root: dataset registry 内のパス解決に使う repository root。
        dataset_yaml: dataset registry YAML。
        table_specs: logical table name から TableSpec 風 object への mapping。
        logger_name: FileIOUtils に渡す logger 名。
        log_path: 任意のログファイルパス。
    """

    default_table_entries: tuple[str, ...] = ()

    def __init__(
        self,
        *,
        project_root: Path,
        dataset_yaml: Path,
        table_specs: Mapping[str, Any] | None,
        logger_name: str,
        log_path: Path | None = None,
    ) -> None:
        """loader を初期化する。"""
        self.project_root = project_root
        self.dataset_yaml = dataset_yaml
        self.table_specs = table_specs
        self.logger_name = logger_name
        self.log_path = log_path

    def load_all(self) -> dict[str, pd.DataFrame]:
        """設定された全テーブルを logical name で読み込む。

        Returns:
            logical table name を key、データフレームを value とする辞書。

        Raises:
            ValueError: ``table_specs`` が未指定の場合。
        """
        if self.table_specs is None:
            raise ValueError("table_specs is required for load_all")
        return self._registry_loader().load_specs(
            self.table_specs,
            key_by="logical_name",
        )

    def load_tables(
        self,
        table_entries: Iterable[str] | None = None,
    ) -> dict[str, pd.DataFrame]:
        """registry entry 名でテーブルを読み込む。

        Args:
            table_entries: dataset registry の entry 名。省略時は class の
                ``default_table_entries`` を使う。

        Returns:
            registry entry 名を key、データフレームを value とする辞書。
        """
        entries = self.default_table_entries if table_entries is None else tuple(table_entries)
        return self._registry_loader().load_entries(entries)

    def _registry_loader(self) -> DatasetRegistryLoader:
        """共通 registry loader を作成する。"""
        return DatasetRegistryLoader(
            project_root=self.project_root,
            dataset_yaml=self.dataset_yaml,
            logger_name=self.logger_name,
            log_path=self.log_path,
        )
