"""Secure byte verification under a trusted root."""
import hashlib

from ariadne.capabilities.causal.ports.content_ref import VerifiedContent
from ariadne.shared.content_ref import ContentRef, ContractViolation
from ariadne.shared.local_fs import TrustedLocalRoot, read_relative


class LocalContentReferenceAdapter:
    def verify(self, ref: ContentRef, *, root: TrustedLocalRoot) -> VerifiedContent:
        try:
            data = read_relative(root, ref.relative_key)
        except OSError as error:
            raise ContractViolation("INPUT_SECURITY", "input", "Cannot open private content reference") from error
        if hashlib.sha256(data).hexdigest() != ref.sha256:
            raise ContractViolation("HASH_INVALID", "input", "Content byte digest mismatch")
        return VerifiedContent(ref, data, len(data))
