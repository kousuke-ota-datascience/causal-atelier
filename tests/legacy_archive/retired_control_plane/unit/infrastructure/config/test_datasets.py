from __future__ import annotations

from pathlib import Path

from ariadne.infrastructure.config.datasets import (
    find_project_root,
    load_dataset_definition,
    resolve_placeholders,
)


def test_find_project_root_detects_pyproject(project_root: Path) -> None:
    start = project_root / "articles/3771bdc6a25760/notebooks"

    assert find_project_root(start) == project_root


def test_resolve_placeholders_preserves_unknown_keys(project_root: Path) -> None:
    resolved = resolve_placeholders(
        {
            "path": "{path_sys_base}/shared/data",
            "typo_path": "{path_sysy_base}/shared/data",
            "unknown": "{not_defined}/x",
            "nested": ["{path_sys_base}/a"],
        },
        {
            "path_sys_base": str(project_root),
            "path_sysy_base": str(project_root),
        },
    )

    assert resolved["path"] == f"{project_root}/shared/data"
    assert resolved["typo_path"] == f"{project_root}/shared/data"
    assert resolved["unknown"] == "{not_defined}/x"
    assert resolved["nested"] == [f"{project_root}/a"]


def test_load_dataset_definition_resolves_project_root_placeholder(
    project_root: Path,
    tmp_path: Path,
) -> None:
    dataset_yaml = tmp_path / "dataset.yaml"
    dataset_yaml.write_text(
        """
default:
  file:
    path: "{path_sys_base}/shared/data"
    name: ""
    type: "parquet"
sample:
  file:
    name: "sample.parquet"
""",
        encoding="utf-8",
    )

    data = load_dataset_definition(dataset_yaml, project_root)

    assert data["default"]["file"]["path"] == f"{project_root}/shared/data"
