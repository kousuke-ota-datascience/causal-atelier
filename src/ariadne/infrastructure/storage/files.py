from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Literal, Mapping

import glob
import pickle

import dask.dataframe as dd
import pandas as pd
import yaml


FileType = Literal["csv", "yaml", "pickle", "parquet"]
SUPPORTED_FILE_TYPES: tuple[FileType, ...] = ("csv", "yaml", "pickle", "parquet")


class FileIOConfigError(ValueError):
    """Raised when file IO configuration is invalid."""


def _deep_merge(
    base: Mapping[str, Any],
    override: Mapping[str, Any],
) -> dict[str, Any]:
    merged = deepcopy(dict(base))
    for key, value in override.items():
        if isinstance(value, Mapping) and isinstance(merged.get(key), Mapping):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = deepcopy(value)
    return merged


def _require_mapping(value: Any, key: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise FileIOConfigError(f"{key} must be a mapping.")
    return value


def _require_file_type(value: Any) -> FileType:
    if value not in SUPPORTED_FILE_TYPES:
        raise FileIOConfigError(
            f"file.type must be one of {SUPPORTED_FILE_TYPES}: {value!r}"
        )
    return value


@dataclass(frozen=True, slots=True)
class FileSpec:
    path: Path
    type: FileType
    name: str | None = None
    names: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.name and not self.names:
            raise FileIOConfigError("Specify either file.name or file.names.")
        if self.name and self.names:
            raise FileIOConfigError("Specify only one of file.name or file.names.")

    @classmethod
    def from_yaml(cls, value: Mapping[str, Any]) -> "FileSpec":
        return cls(
            path=Path(str(value.get("path", ""))),
            name=value.get("name"),
            names=tuple(value.get("names", ())),
            type=_require_file_type(value.get("type")),
        )

    @property
    def single_path(self) -> Path:
        if self.name is None:
            raise FileIOConfigError("file.name is required for single-file IO.")
        return self.path / self.name

    @property
    def paths(self) -> tuple[Path, ...]:
        if not self.names:
            raise FileIOConfigError("file.names is required for multi-file IO.")
        return tuple(self.path / name for name in self.names)

    def with_names(self, names: list[str] | tuple[str, ...]) -> "FileSpec":
        return replace(self, name=None, names=tuple(names))


@dataclass(frozen=True, slots=True)
class CsvReadOptions:
    delimiter: str = ","
    header: int | None = 0
    dtype: Any = "object"
    quotechar: str = '"'
    quoting: int = 1
    encoding: str = "utf-8"

    @classmethod
    def from_yaml(cls, value: Mapping[str, Any] | None) -> "CsvReadOptions":
        data = {} if value is None else dict(value)
        return cls(
            delimiter=data.get("delimiter", ","),
            header=data.get("header", 0),
            dtype=data.get("dtype", "object"),
            quotechar=data.get("quotechar", '"'),
            quoting=data.get("quoting", 1),
            encoding=data.get("encoding", "utf-8"),
        )


@dataclass(frozen=True, slots=True)
class CsvWriteOptions:
    delimiter: str = ","
    quotechar: str = '"'
    quoting: int = 1
    encoding: str = "utf-8"
    header: bool = True
    index: bool = False

    @classmethod
    def from_yaml(cls, value: Mapping[str, Any] | None) -> "CsvWriteOptions":
        data = {} if value is None else dict(value)
        return cls(
            delimiter=data.get("delimiter", ","),
            quotechar=data.get("quotechar", '"'),
            quoting=data.get("quoting", 1),
            encoding=data.get("encoding", "utf-8"),
            header=data.get("header", True),
            index=data.get("index", False),
        )


@dataclass(frozen=True, slots=True)
class YamlOptions:
    encoding: str = "utf-8"

    @classmethod
    def from_yaml(cls, value: Mapping[str, Any] | None) -> "YamlOptions":
        data = {} if value is None else dict(value)
        return cls(encoding=data.get("encoding", "utf-8"))


@dataclass(frozen=True, slots=True)
class ReadOptions:
    csv: CsvReadOptions = field(default_factory=CsvReadOptions)
    yaml: YamlOptions = field(default_factory=YamlOptions)

    @classmethod
    def from_yaml(cls, value: Mapping[str, Any] | None) -> "ReadOptions":
        data = {} if value is None else dict(value)
        return cls(
            csv=CsvReadOptions.from_yaml(data.get("csv")),
            yaml=YamlOptions.from_yaml(data.get("yaml")),
        )


@dataclass(frozen=True, slots=True)
class WriteOptions:
    csv: CsvWriteOptions = field(default_factory=CsvWriteOptions)
    yaml: YamlOptions = field(default_factory=YamlOptions)

    @classmethod
    def from_yaml(cls, value: Mapping[str, Any] | None) -> "WriteOptions":
        data = {} if value is None else dict(value)
        return cls(
            csv=CsvWriteOptions.from_yaml(data.get("csv")),
            yaml=YamlOptions.from_yaml(data.get("yaml")),
        )


@dataclass(frozen=True, slots=True)
class FileReadConfig:
    file: FileSpec
    options: ReadOptions = field(default_factory=ReadOptions)

    @classmethod
    def from_yaml(cls, value: Mapping[str, Any]) -> "FileReadConfig":
        return cls(
            file=FileSpec.from_yaml(_require_mapping(value.get("file"), "file")),
            options=ReadOptions.from_yaml(value.get("read_option")),
        )


@dataclass(frozen=True, slots=True)
class FileWriteConfig:
    file: FileSpec
    options: WriteOptions = field(default_factory=WriteOptions)

    @classmethod
    def from_yaml(cls, value: Mapping[str, Any]) -> "FileWriteConfig":
        return cls(
            file=FileSpec.from_yaml(_require_mapping(value.get("file"), "file")),
            options=WriteOptions.from_yaml(value.get("write_option")),
        )


@dataclass(frozen=True, slots=True)
class FileConfigRegistry:
    default: Mapping[str, Any]
    entries: Mapping[str, Mapping[str, Any]]

    @classmethod
    def from_yaml_file(cls, path: str | Path) -> "FileConfigRegistry":
        with Path(path).open(encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}
        return cls.from_mapping(data)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "FileConfigRegistry":
        if "default" not in value:
            raise FileIOConfigError("Configuration must include a default section.")

        entries = {
            key: _require_mapping(entry, key)
            for key, entry in value.items()
            if key != "default"
        }
        return cls(default=_require_mapping(value["default"], "default"), entries=entries)

    def read_config(self, name: str) -> FileReadConfig:
        return FileReadConfig.from_yaml(self._merged_entry(name))

    def write_config(self, name: str) -> FileWriteConfig:
        return FileWriteConfig.from_yaml(self._merged_entry(name))

    def _merged_entry(self, name: str) -> dict[str, Any]:
        if name not in self.entries:
            raise FileIOConfigError(f"Unknown configuration entry: {name}")
        return _deep_merge(self.default, self.entries[name])


class FileIOUtils:
    def __init__(self, logger):
        self._logger = logger

    def read_file(self, config: FileReadConfig, *, use_dask: bool = False) -> Any:
        try:
            if config.file.type == "csv":
                return pd.read_table(
                    config.file.single_path,
                    delimiter=config.options.csv.delimiter,
                    header=config.options.csv.header,
                    dtype=config.options.csv.dtype,
                    quotechar=config.options.csv.quotechar,
                    quoting=config.options.csv.quoting,
                    encoding=config.options.csv.encoding,
                )

            if config.file.type == "yaml":
                with config.file.single_path.open(
                    encoding=config.options.yaml.encoding
                ) as file:
                    return yaml.safe_load(file)

            if config.file.type == "pickle":
                with config.file.single_path.open("rb") as file:
                    return pickle.load(file)

            if config.file.type == "parquet":
                if use_dask:
                    return dd.read_parquet(config.file.single_path)
                return pd.read_parquet(config.file.single_path)

            raise FileIOConfigError(f"Unsupported file type: {config.file.type}")
        except Exception:
            self._logger.error("read config: %s", config, exc_info=True)
            raise

    def read_files(
        self,
        config: FileReadConfig,
        *,
        use_dask: bool = False,
        concat: bool = True,
    ) -> Any:
        try:
            loaded = {
                name: self.read_file(
                    replace(config, file=replace(config.file, name=name, names=())),
                    use_dask=use_dask,
                )
                for name in config.file.names
            }

            if not concat or config.file.type == "yaml":
                return loaded

            return pd.concat(loaded, axis=0).reset_index(drop=True)
        except Exception:
            self._logger.error("read config: %s", config, exc_info=True)
            raise

    def write_file(self, data: Any, config: FileWriteConfig) -> None:
        try:
            config.file.single_path.parent.mkdir(parents=True, exist_ok=True)

            if config.file.type == "csv":
                data.to_csv(
                    path_or_buf=config.file.single_path,
                    sep=config.options.csv.delimiter,
                    quotechar=config.options.csv.quotechar,
                    quoting=config.options.csv.quoting,
                    encoding=config.options.csv.encoding,
                    header=config.options.csv.header,
                    index=config.options.csv.index,
                )
                return

            if config.file.type == "yaml":
                with config.file.single_path.open(
                    "w",
                    encoding=config.options.yaml.encoding,
                ) as file:
                    yaml.safe_dump(data, file, allow_unicode=True, indent=4)
                return

            if config.file.type == "pickle":
                with config.file.single_path.open("wb") as file:
                    pickle.dump(data, file)
                return

            if config.file.type == "parquet":
                data.to_parquet(config.file.single_path)
                return

            raise FileIOConfigError(f"Unsupported file type: {config.file.type}")
        except Exception:
            self._logger.error("write config: %s", config, exc_info=True)
            raise

    def expand_wildcards(self, config: FileReadConfig) -> FileReadConfig:
        if config.file.name is None:
            raise FileIOConfigError("file.name is required to expand wildcards.")

        names = [
            Path(path).relative_to(config.file.path).as_posix()
            for path in glob.glob(str(config.file.single_path))
        ]
        return replace(config, file=config.file.with_names(sorted(names)))

    def convert_dtype(self, df: pd.DataFrame, dtype_def: Mapping[str, Any]) -> None:
        for dtype, columns in self._clean_dtype_def(dtype_def).items():
            self._logger.debug("%s, columns=%s", dtype, columns)

            if dtype == "datetime64":
                for column, fmt in columns.items():
                    if column in df.columns:
                        df[column] = pd.to_datetime(df[column], format=fmt)
                continue

            for column in columns:
                if column in df.columns:
                    df[column] = df[column].astype(dtype)

    def align_index_to_output_csv(
        self,
        df: pd.DataFrame,
        *,
        destructive: bool = False,
    ) -> pd.DataFrame | None:
        if destructive:
            df.rename(index=lambda s: s + 1, inplace=True)
            df.index.names = ["No"]
            return None

        output = df.rename(index=lambda s: s + 1)
        output.index.names = ["No"]
        return output

    @staticmethod
    def _clean_dtype_def(dtype_def: Mapping[str, Any]) -> dict[str, Any]:
        return {
            dtype: columns
            for dtype, columns in dtype_def.items()
            if columns is not None and len(columns) > 0
        }
