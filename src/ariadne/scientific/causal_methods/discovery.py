"""Selected Local FCI adapter, with isolated Backend stdout and stable PAG evidence."""
import json
import subprocess
import sys
from dataclasses import dataclass

from ariadne.causal.discovery.contracts import DiscoveryGraphOutcome, ValidatedDiscoveryRequest
from ariadne.causal.discovery.graph_evidence import GraphEvidence
from ariadne.scientific.capabilities import LOCAL_BACKEND, LOCAL_METHOD, backend_error, unsupported
from ariadne.scientific.causal_methods.fci_eligibility import ScientificEligibilityPolicy
from ariadne.scientific.ports.artifacts import StagingArtifactSink
from ariadne.shared.content_ref import ContractViolation, valid_sha256
from ariadne.shared.serialization import jcs


@dataclass(frozen=True)
class FciRuntimeObservation:
    distribution_version: str | None
    api_signature_hash: str | None
    reason: str | None


class FciBackend:
    @staticmethod
    def _call(request):
        try:
            result = subprocess.run(
                [sys.executable, "-m", "ariadne.scientific.causal_methods._fci_worker"],
                input=json.dumps(request, allow_nan=False), text=True,
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=True,
            )
            response = json.loads(result.stdout)
        except (OSError, ValueError, subprocess.SubprocessError) as error:
            raise backend_error("BACKEND_EXECUTION_FAILED", "FCI process did not complete") from error
        if type(response) is not dict:
            raise backend_error("BACKEND_API_MISMATCH", "Invalid FCI process response")
        if "error" in response:
            raise backend_error(response["error"], "FCI process rejected the request")
        return response

    def probe(self) -> FciRuntimeObservation:
        try:
            response = self._call({"action": "probe"})
            if not valid_sha256(response.get("api_signature_hash")):
                raise backend_error("BACKEND_API_MISMATCH", "Missing effective FCI signature")
            return FciRuntimeObservation(response["version"], response["api_signature_hash"], None)
        except ContractViolation as error:
            return FciRuntimeObservation(None, None, error.reason.code)

    def fit(self, request, data):
        wire = request.study.to_payload()
        return self._call({
            "action": "fit", "rows": data.tolist(), "columns": list(request.columns),
            "config": wire["method"]["config"], "seed": request.seed,
            "version": request.capability.distribution_version,
            "api_signature_hash": request.capability.api_signature_hash,
        })


class FciDiscoveryAdapter:
    def __init__(self, *, descriptor, backend_factory, policy: ScientificEligibilityPolicy):
        if (
            (descriptor.method_id, descriptor.operation, descriptor.estimand, descriptor.backend_id)
            != (LOCAL_METHOD, "DISCOVER", "GRAPH_STRUCTURE", LOCAL_BACKEND)
            or descriptor.inference_requested
        ):
            raise unsupported("Descriptor is incompatible with Local FCI Discovery")
        self.method_descriptor = descriptor
        self.backend_factory = backend_factory
        self.policy = policy

    def preflight(self, request: ValidatedDiscoveryRequest):
        return self.policy.check(request)[1]

    def execute(self, request: ValidatedDiscoveryRequest, *, sink: StagingArtifactSink) -> DiscoveryGraphOutcome:
        data, eligibility = self.policy.check(request)
        if request.capability.adapter_version != self.method_descriptor.adapter_version:
            raise backend_error("BACKEND_API_MISMATCH", "FCI request belongs to another adapter version")
        backend = self.backend_factory()
        if not callable(getattr(backend, "fit", None)):
            raise backend_error("BACKEND_API_MISMATCH", "Selected Backend lacks a fit method")
        response = backend.fit(request, data)
        if type(response) is not dict:
            raise backend_error("BACKEND_API_MISMATCH", "Selected Backend returned an invalid response")
        if response.get("nodes") != list(request.columns):
            raise backend_error("BACKEND_GRAPH_NODE_MISMATCH", "FCI node identity or ordering changed")
        refs = {name: getattr(request.study, name).to_payload() for name in ("question", "design", "dataset")}
        payload = {
            "schema_version": "e11-local-graph/1", "kind": "PAG", "nodes": list(request.columns),
            "edges": response.get("edges"), "version_id": None, "parent_version_id": None, "temporal": None,
            "provenance": {
                "method_id": LOCAL_METHOD, "backend": LOCAL_BACKEND, "ci_test": request.capability.profile,
                "assumptions": list(request.capability_request.design.assumptions), "source_refs": refs,
                "parent_graph_ref": None,
            },
        }
        try:
            raw = jcs.canonical_bytes({**payload, "content_hash": jcs.digest(payload)})
            graph = GraphEvidence.from_canonical_json(raw)
        except (ContractViolation, ValueError) as error:
            raise backend_error("BACKEND_GRAPH_INVALID", "FCI returned an invalid PAG") from error
        artifact = sink.stage_bytes("graph.json", raw, "application/json", "AGGREGATE")
        return DiscoveryGraphOutcome(graph, artifact, eligibility)
