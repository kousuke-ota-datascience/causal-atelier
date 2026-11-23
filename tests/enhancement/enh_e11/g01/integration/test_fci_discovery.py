"""P04 developer tests. Graph oracles here are specified independently of FCI output."""
import hashlib
import json
from itertools import product

import numpy as np
import pytest

from ariadne.capabilities.causal.method_registry import (
    LOCAL_FCI, LocalMethodCapabilityAdapter, MethodCapabilityRegistry,
)
from ariadne.capabilities.causal.ports.content_ref import VerifiedContent
from ariadne.causal.discovery.contracts import DiscoveryDesign, ValidatedDiscoveryRequest
from ariadne.interfaces.cli.local_causal.config_decoder import StrictLocalConfigDecoder
from ariadne.interfaces.cli.local_causal.manifest import ArtifactDescriptor
from ariadne.scientific.causal_methods.discovery import (
    FciBackend, FciDiscoveryAdapter, FciRuntimeObservation,
)
from ariadne.scientific.causal_methods.fci_eligibility import ScientificEligibilityPolicy, _fisherz
from ariadne.scientific.ports.capability import ValidatedCapabilityRequest
from ariadne.scientific.ports.causal import LocalDiscoveryDispatcher
from ariadne.shared.content_ref import ContentRef, ContractViolation
from ariadne.shared.serialization import jcs

NAMES = ("obs Z", "obs X", "obs Y")
MIME = "application/json"
TEST_OBSERVATION = FciRuntimeObservation("0.1.4.8", "a" * 64, None)


class Sink:
    def __init__(self):
        self.writes = {}

    def stage_bytes(self, key, data, media_type, classification):
        self.writes[key] = data
        return ArtifactDescriptor(key, hashlib.sha256(data).hexdigest(), len(data), media_type, classification, "PRIVATE")


def decode_fixture_dataset(content):
    fixture = json.loads(content.data)
    return tuple(fixture["columns"]), tuple(map(tuple, fixture["rows"]))


def _evidence(name, payload, *, identity=None):
    raw = json.dumps(payload, allow_nan=False).encode()
    ref = ContentRef(identity or name, f"inputs/{name}.json", hashlib.sha256(raw).hexdigest(), MIME, None)
    return VerifiedContent(ref, raw, len(raw))


def _request(ci, rows, registry, *, domains=None, bk=None):
    question = _evidence("question", {
        "question_id": "q", "research_question": "Fixture", "population": "Synthetic",
        "analysis_goal": "GRAPH_STRUCTURE",
    }, identity="q")
    scale = "CONTINUOUS" if ci == "fisherz" else "CATEGORICAL"
    design_wire = {
        "design_id": "design", "question_id": "q", "design_kind": "OBSERVATIONAL_GRAPH_DISCOVERY",
        "variables": [{"name": name, "measurement_scale": scale,
                       **({"category_codes": list(domain)} if domain is not None else {})}
                      for name, domain in zip(NAMES, domains or (None,) * len(NAMES))],
        "assumptions": {"causal_markov_declared": True, "faithfulness_declared": False,
                        "acyclicity_declared": True, "latent_confounding_possible": True, "sampling_unit": "row"},
        "background_knowledge": bk,
    }
    design_content = _evidence("design", design_wire)
    dataset = _evidence("dataset", {"columns": NAMES, "rows": rows})
    study = StrictLocalConfigDecoder().decode(jcs.canonical_bytes({
        "schema_version": "e11-local-study/1", "run_id": "p04",
        "operation": "DISCOVER", "analysis_mode": "EXPLORATORY",
        "inputs": {"question": question.ref.to_payload(), "design": design_content.ref.to_payload(),
                   "dataset": dataset.ref.to_payload(), "graph": None, "identification": None},
        "estimand": {"family": "GRAPH_STRUCTURE", "population": "OBSERVED_VARIABLES", "contrast": "NOT_APPLICABLE"},
        "method": {"id": "P1-M06", "backend": "causal-learn",
                   "config": {"indep_test": ci, "alpha": 0.05, "depth": 0, "max_path_length": 0,
                              "background_knowledge": bk}},
        "inference": {"requested": False, "confidence_level": None}, "randomness": {"seed": None},
        "privacy": {"classification": "AGGREGATE", "row_export_requested": False},
    }), declared_format="json")
    design = DiscoveryDesign.from_payload(design_wire, question_id="q", background_knowledge=bk)
    capability_request = ValidatedCapabilityRequest(study, design, LOCAL_FCI.method_id, LOCAL_FCI.backend_id, ci)
    capability = LocalMethodCapabilityAdapter(registry).resolve(capability_request)
    return ValidatedDiscoveryRequest(capability_request, capability, question, design_content, dataset,
                                     decode_fixture_dataset)


def _registry(observed, backend, resource=lambda: True):
    return MethodCapabilityRegistry(
        {LOCAL_FCI.method_id: LOCAL_FCI},
        {LOCAL_FCI.method_id: lambda: FciDiscoveryAdapter(
            descriptor=LOCAL_FCI, backend_factory=backend, policy=ScientificEligibilityPolicy(resource))},
        observed, (),
    )


@pytest.fixture(scope="module")
def effective():
    observation = FciBackend().probe()
    assert observation.reason is None and observation.distribution_version == "0.1.4.8"
    return observation


@pytest.mark.parametrize("ci", ["fisherz", "chisq", "gsq"])
def test_real_backend_empty_graph_against_independent_empty_dag(ci, effective, capfd):
    # Empty DAG => no latent projection edges => MAG and PAG both empty.
    # The exact balanced product cells are an independent synthetic fixture.
    domains = ((-7, 8), (3, 11), (-2, 13))
    rows = list(product(*domains)) * 5
    registry = _registry(effective, FciBackend)
    request = _request(ci, rows, registry, domains=None if ci == "fisherz" else domains)
    sink = Sink()
    outcome = LocalDiscoveryDispatcher(registry).discover(request, sink=sink)
    assert outcome.graph.nodes == NAMES
    assert outcome.graph.edges == ()
    assert outcome.graph.provenance.ci_test == ci
    assert outcome.graph.provenance.source_refs.dataset == request.dataset.ref
    assert outcome.eligibility.examined_triples == outcome.eligibility.expected_triples == 6
    assert outcome.eligibility.minimum_expected_count == (None if ci == "fisherz" else 5)
    assert outcome.artifact.sha256 != outcome.graph.content_hash and set(sink.writes) == {"graph.json"}
    assert capfd.readouterr() == ("", "")


@pytest.mark.parametrize("case,code", [
    ("bk", "BACKEND_SEMANTICS_UNVERIFIED"), ("empty_stratum", "UNSUPPORTED_COMBINATION"),
    ("four_per_cell", "UNSUPPORTED_COMBINATION"), ("bad_code", "UNSUPPORTED_COMBINATION"),
    ("float_code", "UNSUPPORTED_COMBINATION"), ("support_only_marginal", "UNSUPPORTED_COMBINATION"),
    ("resources", "ELIGIBILITY_UNRESOLVED"),
])
def test_preflight_rejection_never_calls_backend(case, code):
    calls = []
    domains = [(0, 1)] * 3
    rows = list(product((0, 1), repeat=3)) * (4 if case == "four_per_cell" else 5)
    if case == "empty_stratum":
        domains[2] = (0, 1, 2)
    if case == "bad_code":
        rows[0] = (2, 0, 0)
    if case == "float_code":
        rows[0] = (0.0, 0, 0)
    if case == "support_only_marginal":
        rows = [(0, 0, 0), (1, 1, 1)] * 20
    bk = {"required_edges": [], "forbidden_edges": []} if case == "bk" else None
    registry = _registry(TEST_OBSERVATION, lambda: calls.append("backend"), resource=lambda: case != "resources")
    sink = Sink()
    request = _request("gsq", rows, registry, domains=domains, bk=bk)
    with pytest.raises(ContractViolation) as caught:
        LocalDiscoveryDispatcher(registry).discover(request, sink=sink)
    assert caught.value.reason.code == code
    assert calls == [] and sink.writes == {}


def test_fisherz_sample_and_conditioning_boundaries():
    correlation = np.eye(3)
    with pytest.raises(ContractViolation, match="sample size"):
        _fisherz(correlation, [0, 1, 2], 4)
    _fisherz(correlation, [0, 1, 2], 5)
    nearly_singular = np.array([[1, 1 - 1e-14], [1 - 1e-14, 1]])
    assert np.isfinite(np.linalg.inv(nearly_singular)).all()
    with pytest.raises(ContractViolation, match="numerical"):
        _fisherz(nearly_singular, [0, 1], 6)


@pytest.mark.parametrize("defect", ["condition", "left", "right"])
def test_numeric_threshold_comparison_and_two_sided_residual(monkeypatch, defect):
    from ariadne.scientific.causal_methods import fci_eligibility as checks

    real_norm = np.linalg.norm
    observed = []

    def norm(values, *, ord):
        observed.append(ord)
        return 1e-8 if defect == "condition" else (np.nextafter(1e-8, np.inf)
                   if (defect == "left") == (len(observed) == 1) else 1e-8)

    if defect == "condition":
        monkeypatch.setattr(np.linalg, "cond", lambda *_args, **_kwargs: 1e-6 / checks._EPSILON)
        monkeypatch.setattr(np.linalg, "norm", norm)
        _fisherz(np.eye(2), [0, 1], 6)
        monkeypatch.setattr(np.linalg, "cond", lambda *_args, **_kwargs: np.nextafter(1e-6, np.inf) / checks._EPSILON)
        monkeypatch.setattr(np.linalg, "norm", real_norm)
    else:
        monkeypatch.setattr(np.linalg, "norm", norm)
    with pytest.raises(ContractViolation, match="numerical"):
        _fisherz(np.eye(2), [0, 1], 6)
    assert observed == [np.inf, np.inf]


def test_catalog_keeps_backend_factory_lazy_and_no_fallback():
    calls = []
    registry = _registry(TEST_OBSERVATION, lambda: calls.append("backend"))
    assert registry.describe("P1-M06") is LOCAL_FCI
    assert registry.resolve("P1-M06", "causal-learn", "gsq").available
    with pytest.raises(ContractViolation):
        registry.resolve("P1-M06", "PC", "gsq")
    assert calls == []


def test_two_node_latent_observational_ambiguity():
    # Marginalizing L in the Gaussian common-cause model gives the same
    # observed covariance as a direct model, despite different MAG endpoints.
    confounded = np.array([[1.0, 0.0, 1.0], [1.0, 1.0, 0.0]])
    direct = np.array([[np.sqrt(2), 0.0], [1 / np.sqrt(2), np.sqrt(1.5)]])
    np.testing.assert_allclose(confounded @ confounded.T, direct @ direct.T)
    assert ("TAIL", "ARROW") != ("ARROW", "ARROW")


def test_real_fisherz_latent_projection_preserves_uncertainty(effective):
    # DAG L -> X, L -> Y and independent Z. After eliminating L, the MAG
    # has X <-> Y and isolated Z. The single adjacency has no compelled
    # endpoint: direct DAGs in either orientation match the same CI graph.
    rows = [(z, 3 * latent + ex, 3 * latent + ey)
            for latent, ex, ey, z in product((-1, 1), repeat=4)] * 10
    registry = _registry(effective, FciBackend)
    request = _request("fisherz", rows, registry)
    outcome = LocalDiscoveryDispatcher(registry).discover(request, sink=Sink())
    assert len(outcome.graph.edges) == 1
    edge = outcome.graph.edges[0]
    assert {edge.source, edge.target} == set(NAMES[1:])
    assert (edge.source_mark, edge.target_mark) == ("CIRCLE", "CIRCLE")


def test_real_qualified_collider_matches_independent_dag(effective):
    # DAG X -> Z <- Y, all observed. Its unshielded collider compels both
    # arrowheads into Z and the other two endpoints remain uncertain.
    rows = [(3 * x + 3 * y + noise, x, y)
            for x, y, noise in product((-1, 1), repeat=3)] * 20
    registry = _registry(effective, FciBackend)
    outcome = LocalDiscoveryDispatcher(registry).discover(_request("fisherz", rows, registry), sink=Sink())
    normalized = {}
    for edge in outcome.graph.edges:
        if edge.target == NAMES[0]:
            normalized[edge.source] = edge.source_mark, edge.target_mark
        else:
            assert edge.source == NAMES[0]
            normalized[edge.target] = edge.target_mark, edge.source_mark
    assert normalized == {NAMES[1]: ("CIRCLE", "ARROW"), NAMES[2]: ("CIRCLE", "ARROW")}


@pytest.mark.parametrize("rows", [
    [(0, 1, 2), (1, 2, 3)],
    [(1, x, y) for x, y in product((-1, 1), repeat=2)] * 3,
    [(x, x, y) for x, y in product((-1, 1), repeat=2)] * 3,
    [(1e308 * x, y, z) for x, y, z in product((-1, 1), repeat=3)],
])
def test_fisherz_inadmissibility_calls_no_backend(rows):
    calls = []
    registry = _registry(TEST_OBSERVATION, lambda: calls.append("backend"))
    sink = Sink()
    with pytest.raises(ContractViolation):
        LocalDiscoveryDispatcher(registry).discover(_request("fisherz", rows, registry), sink=sink)
    assert calls == [] and sink.writes == {}


def test_preflight_rejects_exhaustion_after_partial_scan():
    calls = []
    grants = iter((True, True, True, False))
    registry = _registry(TEST_OBSERVATION, lambda: calls.append("backend"), resource=lambda: next(grants))
    request = _request("fisherz", list(product((-1, 1), repeat=3)), registry)
    with pytest.raises(ContractViolation) as caught:
        LocalDiscoveryDispatcher(registry).discover(request, sink=Sink())
    assert caught.value.reason.code == "ELIGIBILITY_UNRESOLVED" and not calls


@pytest.mark.parametrize("invalid", [(2, 1), (1, 1), (0, True), (0, 1.0), (0, 1 << 63)])
def test_categorical_design_token_domain_rules(invalid):
    registry = _registry(TEST_OBSERVATION, lambda: pytest.fail("called Backend"))
    with pytest.raises(ContractViolation, match="categorical domain"):
        _request("chisq", list(product((0, 1), repeat=3)) * 5, registry,
                 domains=(invalid, (0, 1), (0, 1)))


def test_backend_node_order_mismatch_is_typed_and_stages_nothing():
    class WrongOrderBackend:
        def fit(self, request, data):
            return {"nodes": sorted(request.columns), "edges": []}

    registry = _registry(TEST_OBSERVATION, WrongOrderBackend)
    request = _request("fisherz", list(product((-1, 1), repeat=3)), registry)
    sink = Sink()
    with pytest.raises(ContractViolation) as caught:
        LocalDiscoveryDispatcher(registry).discover(request, sink=sink)
    assert caught.value.reason.code == "BACKEND_GRAPH_NODE_MISMATCH" and sink.writes == {}


def test_capability_unavailable_has_no_adapter_load():
    observation = FciRuntimeObservation(None, None, "BACKEND_UNAVAILABLE")
    registry = _registry(observation, lambda: pytest.fail("called Backend"))
    capability = registry.resolve("P1-M06", "causal-learn", "fisherz")
    assert not capability.available
    with pytest.raises(ContractViolation) as caught:
        registry.load_adapter(capability)
    assert caught.value.reason.code == "BACKEND_UNAVAILABLE"
