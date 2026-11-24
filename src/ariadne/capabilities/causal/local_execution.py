"""P05 application orchestration for the DISCOVER-only Local lane."""
from __future__ import annotations

import hashlib
import logging
import re
from dataclasses import dataclass
from io import BytesIO
from typing import Protocol

import pyarrow as pa
import pyarrow.parquet as parquet

from ariadne.capabilities.causal.ports.content_ref import ContentReferencePort, VerifiedContent
from ariadne.capabilities.causal.ports.local_io import (
    LocalManifestReaderPort, LocalPublicationPort, PrivacyDecision, PublicationSessionToken, VerifiedLocalRun,
)
from ariadne.capabilities.causal.ports.local_privacy import LocalPrivacyPolicyPort
from ariadne.capabilities.causal.ports.manifest_factory import (
    LocalManifestFactoryPort, ManifestBuildEvidence, ManifestRuntimeFacts,
)
from ariadne.causal.design.study import ValidatedStudy
from ariadne.causal.discovery.contracts import (
    DiscoveryDesign, DiscoveryGraphOutcome, ValidatedDiscoveryRequest, read_evidence,
)
from ariadne.causal.discovery.graph_evidence import GraphEvidence
from ariadne.scientific.capabilities import BackendCapabilityRecord, unsupported
from ariadne.scientific.causal_methods.fci_eligibility import EligibilityEvidence, ScientificEligibilityPolicy
from ariadne.scientific.ports.capability import MethodCapabilityPort, ValidatedCapabilityRequest
from ariadne.scientific.ports.causal import DiscoveryPort
from ariadne.shared.content_ref import ContentRef, ContractViolation
from ariadne.shared.local_fs import LocalPrincipal, TrustedLocalRoot
from ariadne.shared.serialization import jcs

_OUTPUT_SHAPE = "DISCOVER_AGGREGATE_ONLY"
_STATUS_AXES = {
    "identification_status": "NOT_APPLICABLE", "point_availability": "NOT_REQUESTED",
    "inference_availability": "NOT_REQUESTED", "science_acceptance": "NOT_EVALUATED",
}
_LOG = logging.getLogger(__name__)


class RuntimeEnvironmentPort(Protocol):
    def resources_available(self) -> bool: ...
    def snapshot(self, capability: BackendCapabilityRecord) -> ManifestRuntimeFacts: ...


class ClockPort(Protocol):
    def monotonic(self) -> float: ...


@dataclass(frozen=True)
class LocalRunContext:
    root: TrustedLocalRoot
    principal: LocalPrincipal

    def verify(self) -> None:
        if (type(self.root) is not TrustedLocalRoot or type(self.principal) is not LocalPrincipal
            or self.principal != LocalPrincipal.current() or self.root.verify().owner_uid != self.principal.uid):
            raise ContractViolation("PRIVACY_DENIED", "privacy", "Invalid Local execution principal")


@dataclass(frozen=True)
class PreflightReport:
    request: ValidatedDiscoveryRequest
    eligibility: EligibilityEvidence
    privacy: PrivacyDecision
    elapsed_seconds: float
    science_acceptance: str = "NOT_EVALUATED"


@dataclass(frozen=True)
class LocalRunOutcome:
    verified: VerifiedLocalRun
    reused: bool
    technical_status: str = "COMPLETED"
    identification_status: str = "NOT_APPLICABLE"
    point_availability: str = "NOT_REQUESTED"
    inference_availability: str = "NOT_REQUESTED"
    science_acceptance: str = "NOT_EVALUATED"


def _decode_dataset(content: VerifiedContent) -> tuple[tuple[str, ...], tuple[tuple[int | float, ...], ...]]:
    if content.ref.media_type != "application/vnd.apache.parquet":
        raise unsupported("Local Discovery Dataset requires Parquet media type")
    try:
        table = parquet.read_table(BytesIO(content.data), use_threads=False)
        if any(not (pa.types.is_integer(column.type) or pa.types.is_floating(column.type))
               for column in table.columns):
            raise unsupported("Dataset columns must be numeric")
        values = tuple(column.to_pylist() for column in table.columns)
        return tuple(table.column_names), tuple(zip(*values))
    except (pa.ArrowException, OSError, ValueError) as error:
        raise ContractViolation("SCHEMA_INVALID", "configuration", "Invalid Parquet Dataset") from error


@dataclass(frozen=True, kw_only=True)
class LocalCausalUseCase:
    refs: ContentReferencePort
    capabilities: MethodCapabilityPort
    discovery: DiscoveryPort
    identifier: object
    estimators: object
    diagnostics: object
    publisher: LocalPublicationPort
    reader: LocalManifestReaderPort
    privacy: LocalPrivacyPolicyPort
    runtime: RuntimeEnvironmentPort
    clock: ClockPort
    manifest_factory: LocalManifestFactoryPort

    def __post_init__(self) -> None:
        if any(getattr(self, name) is None for name in self.__dataclass_fields__):
            raise TypeError("All twelve Local UseCase dependencies are required")

    def preflight(self, spec: ValidatedStudy, context: LocalRunContext) -> PreflightReport:
        started = self.clock.monotonic()
        if type(spec) is not ValidatedStudy:
            raise unsupported("Expected validated Local Study")
        payload = spec.to_payload()
        method = payload["method"]
        if (
            (payload["schema_version"], payload["operation"], payload["analysis_mode"], method["id"], method["backend"])
            != ("e11-local-study/1", "DISCOVER", "EXPLORATORY", "P1-M06", "causal-learn")
            or type(payload.get("run_id")) is not str
            or re.fullmatch(r"[A-Za-z0-9_-]{1,128}", payload["run_id"]) is None
            or not spec.estimand.is_graph_structure()
        ):
            raise unsupported("Unsupported Local operation, Method or estimand")
        context.verify()
        if any(ref.relative_key.split("/")[0] in {".staging", "runs"}
               for ref in (spec.question, spec.design, spec.dataset)):
            raise ContractViolation("INPUT_SECURITY", "input", "Input references must be outside the publication area")
        question, design, dataset = (
            self.refs.verify(ref, root=context.root) for ref in (spec.question, spec.design, spec.dataset)
        )
        checked_design = DiscoveryDesign.from_payload(
            read_evidence(design), question_id=spec.question.identity,
            background_knowledge=method["config"]["background_knowledge"],
        )
        cap_request = ValidatedCapabilityRequest(spec, checked_design, method["id"], method["backend"],
                                                 method["config"]["indep_test"])
        cap = self.capabilities.resolve(cap_request)
        request = ValidatedDiscoveryRequest(cap_request, cap, question, design, dataset, _decode_dataset)
        _, eligibility = ScientificEligibilityPolicy(self.runtime.resources_available).check(request)
        decision = self.privacy.authorize(study=spec, root=context.root, principal=context.principal,
                                          output_shape=_OUTPUT_SHAPE)
        expected = PrivacyDecision(True, payload["run_id"], jcs.digest(payload), context.root.verify(),
                                   context.principal.uid, "AGGREGATE", False, _OUTPUT_SHAPE)
        if type(decision) is not PrivacyDecision or decision.allowed is not True or decision != expected:
            raise ContractViolation("PRIVACY_DENIED", "privacy", "Privacy decision disagrees with Local request")
        return PreflightReport(request, eligibility, decision, self.clock.monotonic() - started)

    def run(self, spec: ValidatedStudy, context: LocalRunContext) -> LocalRunOutcome:
        ready = self.preflight(spec, context)
        payload = spec.to_payload()
        run_id, request_hash, root = payload["run_id"], jcs.digest(payload), context.root
        try:
            previous = self.reader.verify(root=root, run_id=run_id)
        except ContractViolation as error:
            if error.reason.code != "RUN_NOT_FOUND":
                raise
        else:
            if previous.request_hash != request_hash:
                raise ContractViolation("RUN_ID_CONFLICT", "publication", "Existing run belongs to another request")
            return LocalRunOutcome(previous, reused=True)
        session = PublicationSessionToken()
        sink = self.publisher.begin(run_id=run_id, request_hash=request_hash, root=root, session=session)
        try:
            outcome = self.discovery.discover(ready.request, sink=sink)
            if type(outcome) is not DiscoveryGraphOutcome:
                raise ContractViolation("BACKEND_GRAPH_INVALID", "engine", "Discovery returned no approved Graph")
            graph = outcome.graph
            if type(graph) is not GraphEvidence:
                raise ContractViolation("BACKEND_GRAPH_INVALID", "engine", "Discovery returned invalid Graph evidence")
            graph_bytes = jcs.canonical_bytes(graph.canonical_payload())
            artifact = outcome.artifact
            if (
                artifact.key != "graph.json" or artifact.sha256 != hashlib.sha256(graph_bytes).hexdigest()
                or artifact.size_bytes != len(graph_bytes) or artifact.media_type != "application/json"
                or artifact.privacy_class != "AGGREGATE" or artifact.visibility != "PRIVATE"
            ):
                raise ContractViolation("BACKEND_GRAPH_INVALID", "engine", "Discovery Graph descriptor disagrees")
            method = payload["method"]
            graph.provenance.validate_lineage(spec, lineage=payload["inputs"],
                                              execution={"method": method["id"], "backend": method["backend"]})
            status = {
                "schema_version": "e11-local-status/1", "run_id": run_id, "technical_status": "COMPLETED",
                **_STATUS_AXES, "reason_codes": [], "manifest_relative_path": f"runs/{run_id}/manifest.json",
            }
            stage = sink.stage_bytes
            descriptors = (stage("study.json", jcs.canonical_bytes(payload), "application/json", "AGGREGATE"),
                           stage("status.json", jcs.canonical_bytes(status), "application/json", "AGGREGATE"),
                           artifact)
            evidence = ManifestBuildEvidence(
                spec, payload, status, self.runtime.snapshot(ready.request.capability),
                {"seed": ready.request.seed}, descriptors,
                ContentRef(graph.content_hash, f"runs/{run_id}/graph.json", artifact.sha256, artifact.media_type,
                           "e11-local-graph/1"), (), None,
            )
            manifest = self.manifest_factory.build(evidence=evidence)
            sealed = self.publisher.seal(sink=sink, manifest=manifest, privacy=ready.privacy)
        except Exception:
            try:
                self.publisher.abort(sink=sink, session=session, run_id=run_id, request_hash=request_hash,
                                     root=root, reason="PREPUBLICATION_FAILED")
            except Exception:
                _LOG.warning("PUBLICATION_ABORT_FAILED phase=publication")
            raise
        committed = self.publisher.publish(bundle=sealed, root=root)
        try:
            verified = self.reader.verify(root=root, run_id=run_id)
        except ContractViolation as error:
            raise ContractViolation("PUBLICATION_INDETERMINATE", "publication",
                                    "Published run did not pass independent readback") from error
        if verified.run_id != run_id or verified.request_hash != request_hash:
            raise ContractViolation("PUBLICATION_INDETERMINATE", "publication", "Verified run identity changed")
        return LocalRunOutcome(verified, reused=committed.reused)
