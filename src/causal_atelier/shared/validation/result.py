"""Validation result container."""

from __future__ import annotations

from dataclasses import dataclass

from .issues import ValidationIssue, ValidationSeverity


@dataclass(frozen=True)
class ValidationResult:
    """A collection of validation issues."""

    issues: list[ValidationIssue]

    @property
    def has_errors(self) -> bool:
        """Whether at least one issue is an error."""

        return any(issue.severity == ValidationSeverity.ERROR for issue in self.issues)

    def extend(self, issues: list[ValidationIssue]) -> "ValidationResult":
        """Return a new result with additional issues."""

        return ValidationResult([*self.issues, *issues])

    def to_dicts(self) -> list[dict[str, object]]:
        """Serialize issues."""

        return [issue.to_dict() for issue in self.issues]


__all__ = ["ValidationResult"]
