"""G01 aggregate-only publication policy."""
from ariadne.capabilities.causal.ports.local_io import PrivacyDecision
from ariadne.shared.content_ref import ContractViolation
from ariadne.shared.serialization import jcs


class LocalPrivacyPolicy:
    def authorize(self, *, study, root, principal, output_shape) -> PrivacyDecision:
        payload = study.to_payload()
        identity = root.verify()
        if (
            principal.uid != identity.owner_uid or output_shape != "DISCOVER_AGGREGATE_ONLY"
            or payload["privacy"] != {"classification": "AGGREGATE", "row_export_requested": False}
        ):
            raise ContractViolation("PRIVACY_DENIED", "privacy", "Local run requires aggregate-only privacy")
        return PrivacyDecision(True, payload["run_id"], jcs.digest(payload), identity, principal.uid,
                               "AGGREGATE", False, output_shape)

    def filter_export_columns(self, frame_schema, *, decision):
        raise ContractViolation("PRIVACY_DENIED", "privacy", "Local G01 does not release rows")
