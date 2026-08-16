#!/usr/bin/env python3
"""Shared workflow metadata parsing with format tolerance and semantic strictness."""
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable


class MetadataAmbiguityError(ValueError):
    """Raised when the same metadata label is declared with conflicting values."""


class DependencySyntaxError(ValueError):
    """Raised when a dependency declaration is present but semantically unparseable."""


@dataclass(frozen=True)
class DependencyReference:
    kind: str
    identifier: str
    required_state: str | None = None


def _metadata_line_value(line: str, label: str) -> str | None:
    escaped = re.escape(label)
    # Cosmetic variants intentionally supported:
    #   **Label:** value
    #   Label: value
    #   - Label: value
    patterns = (
        rf"^\s*\*\*{escaped}\s*:\*\*\s*(.*?)\s*$",
        rf"^\s*-\s*{escaped}\s*:\s*(.*?)\s*$",
        rf"^\s*{escaped}\s*:\s*(.*?)\s*$",
    )
    for pattern in patterns:
        match = re.match(pattern, line, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def metadata_values(text: str, label: str) -> tuple[str, ...]:
    """Return all declarations of *label* using supported cosmetic forms."""
    values: list[str] = []
    for line in text.splitlines():
        value = _metadata_line_value(line, label)
        if value is not None:
            values.append(value)
    return tuple(values)


def metadata_field(text: str, label: str) -> str:
    """Resolve one metadata field without semantic guessing.

    Missing or empty values return ``""``. Repeated identical declarations are
    tolerated. Conflicting declarations raise ``MetadataAmbiguityError``.
    """
    values = metadata_values(text, label)
    if not values:
        return ""
    distinct = []
    for value in values:
        if value not in distinct:
            distinct.append(value)
    if len(distinct) > 1:
        raise MetadataAmbiguityError(
            f"conflicting metadata declarations for {label!r}: {distinct!r}"
        )
    return distinct[0]


def normalize_token(value: str) -> str:
    value = value.strip().strip("`").upper()
    return re.sub(r"[\s\-]+", "_", value)


def normalize_trial(value: str) -> str | None:
    value = value.strip()
    if not re.fullmatch(r"\d{1,2}", value):
        return None
    return value.zfill(2)


def parse_dependencies(value: str) -> tuple[DependencyReference, ...]:
    """Parse canonical dependency grammar independent of repository existence.

    Accepted semantic forms:
      NONE / NO_DEPENDENCY / NO_DEPENDENCIES
      Pxx
      Gxx PASS
      comma-separated combinations of Pxx / Gxx PASS

    Repository existence/evidence is validated by the caller. Unknown prose is
    never guessed into a dependency.
    """
    raw = value.strip()
    if not raw:
        raise DependencySyntaxError("dependency declaration is empty")
    if normalize_token(raw) in {"NONE", "NO_DEPENDENCY", "NO_DEPENDENCIES"}:
        return ()

    refs: list[DependencyReference] = []
    parts = [part.strip() for part in raw.split(",")]
    if any(not part for part in parts):
        raise DependencySyntaxError(f"empty dependency expression in: {value}")

    for part in parts:
        package = re.fullmatch(r"P\d{2}", part, flags=re.IGNORECASE)
        if package:
            refs.append(DependencyReference("package", part.upper()))
            continue
        gate = re.fullmatch(r"(G\d{2})\s+PASS", part, flags=re.IGNORECASE)
        if gate:
            refs.append(DependencyReference("gate", gate.group(1).upper(), "PASS"))
            continue
        raise DependencySyntaxError(f"unrecognized dependency expression: {part}")
    return tuple(refs)


def validate_dependency_ids(
    refs: Iterable[DependencyReference],
    *,
    known_package_ids: Iterable[str] = (),
    known_gate_ids: Iterable[str] = (),
) -> list[str]:
    """Validate repository-derived identity existence without hard-coded allow-lists."""
    packages = {x.upper() for x in known_package_ids}
    gates = {x.upper() for x in known_gate_ids}
    errors: list[str] = []
    for ref in refs:
        if ref.kind == "package" and ref.identifier not in packages:
            errors.append(f"unknown package dependency: {ref.identifier}")
        elif ref.kind == "gate" and ref.identifier not in gates:
            errors.append(f"unknown gate dependency: {ref.identifier}")
    return errors


def parse_dependency_reference(
    value: str,
    *,
    known_package_ids: Iterable[str] = (),
    known_gate_ids: Iterable[str] = (),
) -> DependencyReference | None:
    """Compatibility helper for one dependency reference."""
    try:
        refs = parse_dependencies(value)
    except DependencySyntaxError:
        return None
    if len(refs) != 1:
        return None
    errors = validate_dependency_ids(
        refs,
        known_package_ids=known_package_ids,
        known_gate_ids=known_gate_ids,
    )
    return None if errors else refs[0]

class ExecutionModeSyntaxError(ValueError):
    """Raised when Gate 06 Execution mode is not canonical."""


class RequiredPackagesSyntaxError(ValueError):
    """Raised when Gate 06 Required packages is semantically invalid."""


def parse_execution_mode(value: str) -> str:
    token = normalize_token(value)
    if token not in {"SINGLE_EXECUTION", "WORK_PACKAGE"}:
        raise ExecutionModeSyntaxError(f"unrecognized execution mode: {value}")
    return token


def parse_required_packages(value: str) -> tuple[str, ...]:
    raw = value.strip()
    if not raw:
        raise RequiredPackagesSyntaxError("Required packages declaration is empty")
    if normalize_token(raw) in {"NONE", "NO_PACKAGE", "NO_PACKAGES"}:
        return ()
    parts = [part.strip().upper() for part in raw.split(",")]
    if any(not part for part in parts):
        raise RequiredPackagesSyntaxError(f"empty package expression in: {value}")
    if any(not re.fullmatch(r"P\d{2}", part) for part in parts):
        raise RequiredPackagesSyntaxError(f"unrecognized required package expression: {value}")
    if len(set(parts)) != len(parts):
        raise RequiredPackagesSyntaxError(f"duplicate required package in: {value}")
    return tuple(parts)


def parse_gate_dependencies(value: str) -> tuple[DependencyReference, ...]:
    refs = parse_dependencies(value)
    non_gate = [ref.identifier for ref in refs if ref.kind != "gate"]
    if non_gate:
        raise DependencySyntaxError(
            "Gate 06 Depends on accepts only Gxx PASS or NONE; got: " + ", ".join(non_gate)
        )
    return refs
