"""Encoding registry for feature construction."""

from __future__ import annotations

from collections.abc import Callable

import pandas as pd

from .encoders import encode_binary_with_unknown, encode_one_hot, encode_ordinal_map


EncodingFunction = Callable[..., pd.DataFrame | pd.Series]


ENCODING_REGISTRY: dict[str, EncodingFunction] = {
    "one_hot": encode_one_hot,
    "ordinal": encode_ordinal_map,
    "binary": encode_binary_with_unknown,
    "binary_with_unknown": encode_binary_with_unknown,
}


def get_encoding(name: str) -> EncodingFunction:
    """Return an encoding function or fail fast."""

    try:
        return ENCODING_REGISTRY[name]
    except KeyError as exc:
        raise ValueError(f"unsupported encoding: {name}") from exc


__all__ = ["ENCODING_REGISTRY", "EncodingFunction", "get_encoding"]
