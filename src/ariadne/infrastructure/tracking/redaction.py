"""Secret redaction for tracking payloads.

Any string that contains a credential pattern is replaced with a redaction
placeholder.  This is applied to:

- ``mlflow_tracking_error`` before persistence
- Exception messages before re-raising
- Application log messages
- MLflow tag and param values

The redaction is conservative: it prefers false positives (over-redaction) to
false negatives (credential leakage).
"""

from __future__ import annotations

import re

_REDACTED = "[REDACTED]"

# Patterns that indicate a value contains a secret.
_SECRET_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"(?i)password\s*[:=]\s*\S+"),
    re.compile(r"(?i)passwd\s*[:=]\s*\S+"),
    re.compile(r"(?i)\btoken\s*[:=]\s*\S+"),
    re.compile(r"(?i)\bsecret\s*[:=]\s*\S+"),
    re.compile(r"(?i)api[_-]?key\s*[:=]\s*\S+"),
    re.compile(r"(?i)credential\s*[:=]\s*\S+"),
    re.compile(r"(?i)authorization\s*:\s*.+"),
    re.compile(r"(?i)Bearer\s+\S+"),
    re.compile(r"(?i)AccountKey\s*=\s*[A-Za-z0-9+/=]+"),
    re.compile(r"(?i)sig\s*=\s*[A-Za-z0-9%+/=]+"),
    # Connection-string patterns
    re.compile(r"(?i)(postgresql|mysql|sqlite|redis|mongodb)://[^\s]+"),
    re.compile(r"(?i)(https?://)[^@\s]*@"),
    re.compile(r"(?i)DefaultEndpointsProtocol=[^\s]+"),
    re.compile(r"(?i)SharedAccessSignature[^\s]+"),
]

# Replacement function that keeps the key name but hides the value
_REDACT_SUB = re.compile(
    r"(?i)(password|passwd|token|secret|api[_-]?key|credential|authorization"
    r"|accountkey|sig|bearer)\s*[:=]\s*\S+",
)


def redact_secret(text: str) -> str:
    """Return *text* with detected secret values replaced by ``[REDACTED]``.

    If ``text`` is empty or contains no suspected secrets, it is returned
    unchanged.  The function never raises; on any error it returns a safe
    placeholder.
    """
    if not text:
        return text
    try:
        result = text
        for pattern in _SECRET_PATTERNS:
            result = pattern.sub(_REDACTED, result)
        return result
    except Exception:
        return _REDACTED


def redact_dict(mapping: dict[str, str]) -> dict[str, str]:
    """Return a copy of *mapping* with secret values redacted."""
    return {k: redact_secret(str(v)) for k, v in mapping.items()}


__all__ = ["redact_secret", "redact_dict"]
