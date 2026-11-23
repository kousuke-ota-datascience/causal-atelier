"""Pure E11 content reference values."""
from __future__ import annotations

import re
import unicodedata
from collections.abc import Mapping
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Reason:
    code: str
    phase: str
    message: str


class ContractViolation(ValueError):
    def __init__(self, code: str, phase: str, message: str):
        self.reason = Reason(code, phase, message)
        super().__init__(message)


def safe_relative_key(key: object) -> bool:
    return (
        type(key) is str
        and not re.match(r"^[A-Za-z]:", key)
        and "\\" not in key
        and all(part not in {"", ".", ".."} for part in key.split("/"))
        and all(unicodedata.category(char) not in {"Cc", "Cf", "Cs"} for char in key)
    )


def valid_sha256(value: object) -> bool:
    return type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def nonempty_text(value: object) -> bool:
    return type(value) is str and bool(value) and not any(
        unicodedata.category(char) == "Cs" for char in value
    )


@dataclass(frozen=True)
class ContentRef:
    identity: str
    relative_key: str
    sha256: str
    media_type: str
    schema_version: str | None

    def __post_init__(self) -> None:
        if not safe_relative_key(self.relative_key):
            raise ContractViolation("SCHEMA_INVALID", "content_ref", "Invalid relative key")
        if not valid_sha256(self.sha256):
            raise ContractViolation("HASH_INVALID", "content_ref", "Invalid SHA-256")
        if not nonempty_text(self.identity) or not nonempty_text(self.media_type):
            raise ContractViolation("SCHEMA_INVALID", "content_ref", "Invalid identity or media type")
        if self.schema_version is not None and not nonempty_text(self.schema_version):
            raise ContractViolation("SCHEMA_INVALID", "content_ref", "Invalid schema version")

    @classmethod
    def from_payload(cls, payload: Mapping[str, object]) -> ContentRef:
        if not isinstance(payload, Mapping) or set(payload) != set(cls.__annotations__):
            raise ContractViolation("SCHEMA_INVALID", "content_ref", "Expected exactly five reference fields")
        return cls(**payload)

    def to_payload(self) -> dict[str, object]:
        return asdict(self)
