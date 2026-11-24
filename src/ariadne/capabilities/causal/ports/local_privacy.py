"""Application-visible stateless Local privacy policy."""
from typing import Protocol

from ariadne.capabilities.causal.ports.local_io import LocalPrivacyPolicy


class LocalPrivacyPolicyPort(LocalPrivacyPolicy, Protocol):
    def filter_export_columns(self, frame_schema: object, *, decision: object) -> object: ...
