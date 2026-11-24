"""Translate neutral evidence into the original P01 Manifest factory."""
from ariadne.capabilities.causal.ports.manifest_factory import ManifestBuildEvidence
from ariadne.causal.design.study import thaw_json
from ariadne.interfaces.cli.local_causal.manifest import (
    ArtifactDescriptor, LocalRunManifest, RuntimeEvidence, ValidatedRunEvidence,
)
from ariadne.shared.content_ref import ContractViolation


class LocalManifestFactoryAdapter:
    def build(self, *, evidence: ManifestBuildEvidence) -> LocalRunManifest:
        if type(evidence) is not ManifestBuildEvidence:
            raise ContractViolation("SCHEMA_INVALID", "publication", "Missing typed Manifest evidence")
        runtime = evidence.runtime
        return LocalRunManifest.from_run_evidence(ValidatedRunEvidence(
            study=evidence.study,
            study_payload=thaw_json(evidence.study_payload),
            status_payload=thaw_json(evidence.status_payload),
            runtime=RuntimeEvidence(runtime.repo_commit, runtime.dirty, runtime.python_version, runtime.platform,
                                    runtime.uv_lock_sha256, thaw_json(runtime.distributions),
                                    thaw_json(runtime.api_probes)),
            stochastic=thaw_json(evidence.stochastic),
            artifact_descriptors=tuple(
                ArtifactDescriptor(item.key, item.sha256, item.size_bytes, item.media_type,
                                   item.privacy_class, item.visibility)
                for item in evidence.artifact_descriptors
            ),
            output_graph_ref=evidence.output_graph_ref,
            graph_negative_reason_codes=evidence.graph_negative_reason_codes,
            review_science_evidence_ref=evidence.review_science_evidence_ref,
        ))
