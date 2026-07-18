"""Stable hashing helpers for reproducibility metadata."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any


def _json_default(value: Any) -> str:
    return str(value)


def hash_file(path: Path | str) -> str:
    """Return a SHA-256 hash of a file."""

    digest = hashlib.sha256()
    with Path(path).open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hash_mapping(value: Mapping[str, Any]) -> str:
    """Return a stable SHA-256 hash for a mapping."""

    payload = json.dumps(
        dict(value),
        default=_json_default,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def hash_resolved_config(path: Path | str | None, mapping: Mapping[str, Any] | None = None) -> str:
    """Hash a resolved config mapping when available, otherwise hash a file."""

    if mapping is not None:
        return hash_mapping(mapping)
    if path is None:
        return ""
    return hash_file(path)


__all__ = ["hash_file", "hash_mapping", "hash_resolved_config"]
