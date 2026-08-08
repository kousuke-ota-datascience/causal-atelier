"""Strict versioned JSON schemas and deterministic canonicalization.

The registry deliberately stays framework-free.  Capability packages register
their validators without making the product domain depend on Pydantic, an ORM,
or an analytical library.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Callable, Mapping
from dataclasses import asdict, is_dataclass
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from ariadne.product.domain.errors import InvalidSchema, UnsupportedSchemaVersion

SchemaValidator = Callable[[Mapping[str, Any]], Mapping[str, Any] | None]


def _normalize(value: Any) -> Any:
    if is_dataclass(value):
        return _normalize(asdict(value))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, (UUID, datetime)):
        return str(value)
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise InvalidSchema("NaN and Infinity are not valid canonical JSON")
        if value == 0:
            return 0
        if value.is_integer():
            return int(value)
        return value
    if isinstance(value, Mapping):
        if not all(isinstance(key, str) for key in value):
            raise InvalidSchema("JSON object keys must be strings")
        return {key: _normalize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_normalize(item) for item in value]
    raise InvalidSchema(f"Unsupported canonical JSON value: {type(value).__name__}")


def canonical_bytes(payload: Mapping[str, Any]) -> bytes:
    normalized = _normalize(payload)
    return json.dumps(
        normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


def canonical_hash(payload: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def reject_unknown(payload: Mapping[str, Any], allowed: set[str], *, name: str) -> None:
    unknown = sorted(set(payload) - allowed)
    if unknown:
        raise InvalidSchema(f"Unknown {name} fields: {unknown}")


class SchemaRegistry:
    def __init__(self) -> None:
        self._validators: dict[str, SchemaValidator] = {}

    @property
    def versions(self) -> frozenset[str]:
        return frozenset(self._validators)

    def register(self, schema_version: str, validator: SchemaValidator) -> None:
        if not schema_version or schema_version in self._validators:
            raise InvalidSchema(f"Schema is already registered: {schema_version}")
        self._validators[schema_version] = validator

    def validate(self, schema_version: str, payload: Mapping[str, Any]) -> dict[str, Any]:
        validator = self._validators.get(schema_version)
        if validator is None:
            raise UnsupportedSchemaVersion(schema_version)
        if not isinstance(payload, Mapping):
            raise InvalidSchema("Schema payload must be an object")
        normalized = validator(payload)
        return dict(normalized if normalized is not None else payload)

    def canonicalize(self, schema_version: str, payload: Mapping[str, Any]) -> bytes:
        return canonical_bytes(self.validate(schema_version, payload))

    def hash(self, schema_version: str, payload: Mapping[str, Any]) -> str:
        return hashlib.sha256(self.canonicalize(schema_version, payload)).hexdigest()
