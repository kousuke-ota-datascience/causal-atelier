"""Development and OIDC bearer-token identity extraction."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import jwt
from jwt import PyJWKClient

from ariadne.infrastructure.settings import WebSettings


@dataclass(frozen=True)
class Identity:
    provider: str
    subject: str
    display_name: str
    email: str | None = None
    system_admin: bool = False


class TokenVerifier:
    def __init__(self, settings: WebSettings) -> None:
        self.settings = settings
        self._jwks = (
            PyJWKClient(settings.oidc_jwks_url) if settings.oidc_jwks_url else None
        )

    def verify(self, token: str) -> Identity:
        if (
            not self._jwks
            or not self.settings.oidc_issuer
            or not self.settings.oidc_audience
        ):
            raise ValueError(
                "OIDC issuer, audience, and JWKS URL must all be configured"
            )
        signing_key = self._jwks.get_signing_key_from_jwt(token)
        claims: dict[str, Any] = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256", "ES256"],
            audience=self.settings.oidc_audience,
            issuer=self.settings.oidc_issuer,
        )
        return Identity(
            provider=self.settings.oidc_issuer,
            subject=str(claims["sub"]),
            display_name=str(
                claims.get("name") or claims.get("preferred_username") or claims["sub"]
            ),
            email=claims.get("email"),
            system_admin=bool(claims.get("ariadne_system_admin", False)),
        )


__all__ = ["Identity", "TokenVerifier"]
