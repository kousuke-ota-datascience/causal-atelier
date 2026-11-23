"""Application-facing content verification."""
from dataclasses import dataclass
from typing import Protocol

from ariadne.shared.content_ref import ContentRef
from ariadne.shared.local_fs import TrustedLocalRoot


@dataclass(frozen=True)
class VerifiedContent:
    ref: ContentRef
    data: bytes
    size_bytes: int


class ContentReferencePort(Protocol):
    def verify(self, ref: ContentRef, *, root: TrustedLocalRoot) -> VerifiedContent: ...
