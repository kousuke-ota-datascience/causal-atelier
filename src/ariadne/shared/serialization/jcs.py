"""RFC 8785 canonical JSON for E11."""
from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Mapping

VERSION = "e11-json-jcs-rfc8785/1"


def _number(value: int | float) -> str:
    number = float(value)
    if not math.isfinite(number) or (type(value) is int and int(number) != value):
        raise ValueError("Number cannot be represented exactly in the JSON number domain")
    if number == 0:
        return "0"
    # repr supplies the nearest shortest round-trip digits for binary64.
    # Place the decimal point using JCS notation rules and integer offsets.
    sign = "-" if number < 0 else ""
    mantissa, _, exponent = repr(abs(number)).partition("e")
    whole, _, fraction = mantissa.partition(".")
    raw_digits = whole + fraction
    significant = raw_digits.lstrip("0")
    point = len(whole) + int(exponent or "0") - (len(raw_digits) - len(significant))
    digits = significant.rstrip("0")

    if -5 <= point <= 21:
        if point <= 0:
            return sign + "0." + "0" * -point + digits
        if point >= len(digits):
            return sign + digits.ljust(point, "0")
        return sign + digits[:point] + "." + digits[point:]

    tail = "." + digits[1:] if len(digits) > 1 else ""
    return f"{sign}{digits[0]}{tail}e{point - 1:+d}"


def _encode(value: object) -> str:
    if value is None:
        return "null"
    if type(value) is bool:
        return "true" if value else "false"
    if type(value) in (int, float):
        return _number(value)
    if type(value) is str:
        value.encode("utf-8")
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, Mapping):
        if any(type(key) is not str for key in value):
            raise ValueError("JSON object keys must be strings")
        keys = sorted(value, key=lambda key: key.encode("utf-16-be"))
        return "{" + ",".join(_encode(key) + ":" + _encode(value[key]) for key in keys) + "}"
    if type(value) is list:
        return "[" + ",".join(_encode(item) for item in value) + "]"
    raise ValueError(f"Unsupported JSON value type: {type(value).__name__}")


def canonical_bytes(value: object) -> bytes:
    """Serialize JSON values without normalizing their Unicode code points."""
    try:
        return _encode(value).encode("utf-8")
    except (RecursionError, OverflowError, UnicodeError) as error:
        raise ValueError("Invalid JSON value for canonical encoding") from error


def digest(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON object key")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ValueError(f"Invalid JSON numeric constant: {value}")


def parse_json(raw: bytes) -> object:
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object, parse_constant=_reject_constant)
    canonical_bytes(value)
    return value
