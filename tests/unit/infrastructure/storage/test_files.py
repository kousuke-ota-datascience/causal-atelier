from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd
import pytest

from ariadne.infrastructure.storage.files import (
    CsvReadOptions,
    FileConfigRegistry,
    FileIOConfigError,
    FileIOUtils,
    FileReadConfig,
    FileSpec,
    FileWriteConfig,
    ReadOptions,
    WriteOptions,
)


@pytest.fixture
def file_io() -> FileIOUtils:
    return FileIOUtils(logging.getLogger("test_file_io"))


def test_registry_merges_default_and_entry(tmp_path: Path) -> None:
    registry = FileConfigRegistry.from_mapping(
        {
            "default": {
                "file": {
                    "path": str(tmp_path),
                    "name": "default.csv",
                    "type": "csv",
                },
                "read_option": {
                    "csv": {
                        "delimiter": ",",
                        "encoding": "utf-8",
                        "dtype": "object",
                    }
                },
            },
            "pipe_file": {
                "file": {"name": "pipe.csv"},
                "read_option": {"csv": {"delimiter": "|"}},
            },
        }
    )

    config = registry.read_config("pipe_file")

    assert config.file.path == tmp_path
    assert config.file.name == "pipe.csv"
    assert config.file.type == "csv"
    assert config.options.csv.delimiter == "|"
    assert config.options.csv.encoding == "utf-8"
    assert registry.default["file"]["name"] == "default.csv"


def test_registry_rejects_missing_default() -> None:
    with pytest.raises(FileIOConfigError, match="default"):
        FileConfigRegistry.from_mapping({"data": {"file": {"type": "csv"}}})


def test_file_spec_requires_exactly_one_name_form(tmp_path: Path) -> None:
    with pytest.raises(FileIOConfigError, match="either file.name or file.names"):
        FileSpec(path=tmp_path, type="csv")

    with pytest.raises(FileIOConfigError, match="only one"):
        FileSpec(path=tmp_path, type="csv", name="a.csv", names=("b.csv",))


def test_read_and_write_yaml(file_io: FileIOUtils, tmp_path: Path) -> None:
    config = FileWriteConfig(
        file=FileSpec(path=tmp_path, name="sample.yaml", type="yaml"),
        options=WriteOptions(),
    )

    file_io.write_file({"a": 1, "b": ["x"]}, config)
    read_config = FileReadConfig(file=config.file, options=ReadOptions())

    assert file_io.read_file(read_config) == {"a": 1, "b": ["x"]}


def test_expand_wildcards_and_read_files_concat(
    file_io: FileIOUtils,
    tmp_path: Path,
) -> None:
    (tmp_path / "b.csv").write_text("id\n2\n", encoding="utf-8")
    (tmp_path / "a.csv").write_text("id\n1\n", encoding="utf-8")

    config = FileReadConfig(
        file=FileSpec(path=tmp_path, name="*.csv", type="csv"),
        options=ReadOptions(csv=CsvReadOptions(dtype={"id": "int64"})),
    )

    expanded = file_io.expand_wildcards(config)
    data = file_io.read_files(expanded)

    assert expanded.file.names == ("a.csv", "b.csv")
    assert data["id"].tolist() == [1, 2]


def test_convert_dtype_ignores_missing_columns(file_io: FileIOUtils) -> None:
    data = pd.DataFrame(
        {
            "date": ["2026-01-02"],
            "amount": ["10"],
        }
    )

    file_io.convert_dtype(
        data,
        {
            "datetime64": {"date": "%Y-%m-%d", "missing_date": "%Y-%m-%d"},
            "int64": ["amount", "missing_amount"],
            "object": [],
            "float64": None,
        },
    )

    assert pd.api.types.is_datetime64_any_dtype(data["date"])
    assert pd.api.types.is_integer_dtype(data["amount"])
