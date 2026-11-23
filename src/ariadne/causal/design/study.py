"""Validated study values independent of CLI transport."""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from ariadne.causal.inference.contracts import EstimandRef
from ariadne.shared.content_ref import ContentRef


class _FrozenArray(tuple):
    """Immutable internal representation of a JSON array."""


def freeze_json(value: object) -> object:
    if isinstance(value, Mapping):
        return MappingProxyType({key: freeze_json(item) for key, item in value.items()})
    if type(value) is list:
        return _FrozenArray(freeze_json(item) for item in value)
    return value


def thaw_json(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: thaw_json(item) for key, item in value.items()}
    if type(value) is _FrozenArray:
        return [thaw_json(item) for item in value]
    return value


@dataclass(frozen=True)
class ValidatedStudy:
    estimand: EstimandRef
    question: ContentRef
    design: ContentRef
    dataset: ContentRef
    _payload: Mapping[str, object]

    def __post_init__(self) -> None:
        object.__setattr__(self, "_payload", freeze_json(self._payload))

    def to_payload(self) -> dict[str, object]:
        return thaw_json(self._payload)
