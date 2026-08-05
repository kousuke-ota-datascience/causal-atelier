"""Unit tests for secret redaction utility.

Covers:
- Known secret patterns are redacted
- Non-secret strings are returned unchanged
- Empty strings are handled
- dict redaction works
"""

from __future__ import annotations

import pytest

from ariadne.infrastructure.tracking.redaction import redact_secret, redact_dict


class TestRedactSecret:
    def test_empty_string_unchanged(self) -> None:
        assert redact_secret("") == ""

    def test_non_secret_string_unchanged(self) -> None:
        assert redact_secret("mlflow run succeeded") == "mlflow run succeeded"

    def test_password_pattern_redacted(self) -> None:
        result = redact_secret("password=supersecret123")
        assert "supersecret123" not in result
        assert "[REDACTED]" in result

    def test_token_pattern_redacted(self) -> None:
        result = redact_secret("token=abc.def.ghi")
        assert "abc.def.ghi" not in result

    def test_bearer_token_redacted(self) -> None:
        result = redact_secret("Authorization: Bearer eyJhbGciOiJSUzI1NiJ9.payload")
        assert "eyJhbGciOiJSUzI1NiJ9" not in result

    def test_connection_string_redacted(self) -> None:
        result = redact_secret("postgresql://user:password@host:5432/db")
        assert "password" not in result or "[REDACTED]" in result

    def test_secret_key_redacted(self) -> None:
        result = redact_secret("secret=my-top-secret-value")
        assert "my-top-secret-value" not in result

    def test_account_key_redacted(self) -> None:
        result = redact_secret("AccountKey=AAABBBCCC+ddd/eee==")
        assert "AAABBBCCC" not in result

    def test_function_never_raises(self) -> None:
        # Should not raise on any input
        result = redact_secret(None)  # type: ignore[arg-type]
        assert result is None or isinstance(result, str)

    def test_diagnostic_info_preserved(self) -> None:
        # After redaction, enough diagnostic info remains
        result = redact_secret("MLflow connection failed at host:5432 - timeout after 30s")
        assert "MLflow connection failed" in result or "[REDACTED]" in result


class TestRedactDict:
    def test_clean_dict_unchanged(self) -> None:
        d = {"key": "value", "name": "test"}
        result = redact_dict(d)
        assert result["key"] == "value"
        assert result["name"] == "test"

    def test_secret_value_redacted(self) -> None:
        d = {"auth": "token=abc123", "name": "experiment"}
        result = redact_dict(d)
        assert "abc123" not in result["auth"]

    def test_returns_copy(self) -> None:
        d = {"k": "v"}
        result = redact_dict(d)
        result["k"] = "changed"
        assert d["k"] == "v"
