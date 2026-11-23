"""G01 P01 lexical reference, study, JSON and manifest evidence checks."""
import json
from dataclasses import replace
from pathlib import Path

import pytest

from ariadne.interfaces.cli.local_causal.config_decoder import StrictLocalConfigDecoder
from ariadne.interfaces.cli.local_causal.manifest import (
    AXES,
    NEGATIVE_REASON,
    ArtifactDescriptor,
    LocalRunManifest,
    RuntimeEvidence,
    ValidatedRunEvidence,
)
from ariadne.shared.content_ref import ContentRef, ContractViolation
from ariadne.shared.serialization import jcs

FIXTURE = (
    Path(__file__).resolve().parents[5]
    / "docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion"
    / "00_enhance_background/Revised_requirements_definition_documents"
    / "23_api_interface_design/schema_drafts/e11_jcs_golden_vectors.json"
)
VECTORS = json.loads(FIXTURE.read_text(encoding="utf-8"))
HASH = "a" * 64


@pytest.mark.parametrize("vector", VECTORS["positive"], ids=lambda item: item["id"])
def test_jcs_golden_bytes(vector):
    assert jcs.canonical_bytes(vector["input"]) == vector["expected_canonical_utf8_json"].encode()
    assert jcs.digest(vector["input"]) == vector["expected_sha256"]


@pytest.mark.parametrize("raw", [b'{"a":NaN}', b'{"a":Infinity}', b'{"a":-Infinity}', b'{"a":1,"a":2}',
                                 b'{"a":"\\ud800"}', b'{"a":9007199254740993}'])
def test_jcs_rejects_invalid_json(raw):
    with pytest.raises(ValueError):
        jcs.parse_json(raw)


def test_jcs_rejects_non_json_and_does_not_normalize():
    with pytest.raises(ValueError):
        jcs.canonical_bytes(object())
    assert jcs.canonical_bytes("é") != jcs.canonical_bytes("e\u0301")


@pytest.mark.parametrize("key", ["/abs", "a/../b", ".", "a//b", "z:/a", "a\\b", "a\x00", "a\u202eb"])
def test_ref_lexical_rejection(key):
    with pytest.raises(ContractViolation):
        ContentRef("identity", key, HASH, "application/json", None)


@pytest.fixture
def study_payload():
    return {
        "schema_version": "e11-local-study/1", "run_id": "run-1",
        "operation": "DISCOVER", "analysis_mode": "EXPLORATORY",
        "inputs": {
            **{name: ContentRef(name, f"inputs/{name}.json", HASH, "application/json", None).to_payload()
               for name in ("question", "design", "dataset")},
            "graph": None, "identification": None,
        },
        "estimand": {"family": "GRAPH_STRUCTURE", "population": "OBSERVED_VARIABLES", "contrast": "NOT_APPLICABLE"},
        "method": {"id": "P1-M06", "backend": "causal-learn",
                   "config": {"indep_test": "fisherz", "alpha": 0.05, "depth": -1, "max_path_length": -1,
                              "background_knowledge": None}},
        "inference": {"requested": False, "confidence_level": None},
        "randomness": {"seed": None},
        "privacy": {"classification": "AGGREGATE", "row_export_requested": False},
    }


def _decode(payload):
    return StrictLocalConfigDecoder().decode(json.dumps(payload).encode(), declared_format="json")


def test_json_and_yaml_study_preserve_projection(study_payload):
    import yaml

    raw = yaml.safe_dump(study_payload).encode()
    decoder = StrictLocalConfigDecoder()
    assert decoder.decode(raw, declared_format="yaml") == _decode(study_payload)
    assert _decode(study_payload).to_payload() == study_payload


@pytest.mark.parametrize("raw", [b"a: 1\na: 2", b"a: !!python/object:object {}", b"a: &a [*a]"])
def test_yaml_hard_errors(raw):
    with pytest.raises(ContractViolation, match="configuration"):
        StrictLocalConfigDecoder().decode(raw, declared_format="yaml")


@pytest.mark.parametrize(("group", "key", "value", "code"), [
    ("top", "schema_version", "causal-analysis-spec/2", "VERSION_UNSUPPORTED"),
    ("top", "unexpected", True, "SCHEMA_INVALID"),
    ("method", "id", "P1-M05", "SCHEMA_INVALID"),
    ("estimand", "family", "ATE", "SCHEMA_INVALID"),
    ("inference", "requested", True, "SCHEMA_INVALID"),
    ("privacy", "row_export_requested", True, "PRIVACY_POLICY_CONFLICT"),
])
def test_invalid_study(study_payload, group, key, value, code):
    target = study_payload if group == "top" else study_payload[group]
    target[key] = value
    with pytest.raises(ContractViolation) as error:
        _decode(study_payload)
    assert error.value.reason.code == code


def _evidence(study_payload, *, negative=False):
    reasons = [NEGATIVE_REASON] if negative else []
    output_key = "diagnostics.json" if negative else "graph.json"
    status = {
        "schema_version": "e11-local-status/1", "run_id": "run-1", "technical_status": "COMPLETED",
        **AXES, "reason_codes": reasons, "manifest_relative_path": "runs/run-1/manifest.json",
    }
    graph = None if negative else ContentRef(
        "graph", "runs/run-1/graph.json", HASH, "application/json", "e11-local-graph/1",
    )
    descriptors = tuple(
        ArtifactDescriptor(key, HASH, 10, "application/json", "AGGREGATE", "PRIVATE")
        for key in ("study.json", output_key, "status.json")
    )
    runtime = RuntimeEvidence("test-commit", False, "3.12", "Linux", HASH, {}, {})
    return ValidatedRunEvidence(_decode(study_payload), study_payload, status, runtime, {}, descriptors,
                                graph, tuple(reasons), None)


@pytest.mark.parametrize("negative", [False, True])
def test_manifest_round_trip(study_payload, negative):
    evidence = _evidence(study_payload, negative=negative)
    manifest = LocalRunManifest.from_run_evidence(evidence)
    payload = json.loads(manifest.to_canonical_bytes())
    assert manifest.validate_invariants() == ()
    assert manifest.to_canonical_bytes() == LocalRunManifest.from_payload(payload).to_canonical_bytes()
    assert payload["request_hash"] == jcs.digest(study_payload)
    assert payload["schema_dispatch"]["result"] is None
    assert payload["lineage"]["question"] == study_payload["inputs"]["question"]
    assert [item["key"] for item in payload["artifacts"]] == [
        "diagnostics.json" if negative else "graph.json", "status.json", "study.json",
    ]
    assert "manifest_sha256" not in payload


@pytest.mark.parametrize("codes", [
    (), ("EXECUTION_FAILED",), ("SCI_OTHER",), (NEGATIVE_REASON, "EXECUTION_FAILED"),
    (NEGATIVE_REASON, NEGATIVE_REASON),
])
def test_negative_reason_must_be_closed_singleton(study_payload, codes):
    evidence = _evidence(study_payload, negative=True)
    status = {**evidence.status_payload, "reason_codes": list(codes)}
    with pytest.raises(ContractViolation):
        LocalRunManifest.from_run_evidence(replace(evidence, status_payload=status, graph_negative_reason_codes=codes))


@pytest.mark.parametrize(("field", "value"), [
    ("run_id", "wrong"), ("technical_status", "EXECUTION_FAILED"),
    ("manifest_relative_path", None), ("science_acceptance", "PASS"),
    ("reason_codes", [NEGATIVE_REASON]),
])
def test_manifest_rejects_invalid_positive_status(study_payload, field, value):
    evidence = _evidence(study_payload)
    status = {**evidence.status_payload, "reason_codes": []}
    status[field] = value
    with pytest.raises(ContractViolation):
        LocalRunManifest.from_run_evidence(replace(evidence, status_payload=status))


@pytest.mark.parametrize(("field", "value"), [
    ("relative_key", "graph.json"), ("sha256", "b" * 64), ("media_type", "text/plain"),
])
def test_graph_ref_must_join_staged_descriptor(study_payload, field, value):
    evidence = _evidence(study_payload)
    wrong_ref = replace(evidence.output_graph_ref, **{field: value})
    with pytest.raises(ContractViolation):
        LocalRunManifest.from_run_evidence(replace(evidence, output_graph_ref=wrong_ref))


def test_evidence_does_not_retain_mutable_aliases(study_payload):
    evidence = _evidence(study_payload)
    expected = LocalRunManifest.from_run_evidence(evidence).to_canonical_bytes()
    study_payload["inputs"]["dataset"]["identity"] = "changed"
    assert LocalRunManifest.from_run_evidence(evidence).to_canonical_bytes() == expected


@pytest.mark.parametrize("bad_config", [
    {"extra": 1}, {"depth": True}, {"max_path_length": -2}, {"alpha": 1},
    {"background_knowledge": {"required_edges": [["a", "b"], ["a", "b"]], "forbidden_edges": []}},
])
def test_method_config_rejection(study_payload, bad_config):
    study_payload["method"]["config"].update(bad_config)
    with pytest.raises(ContractViolation) as error:
        _decode(study_payload)
    assert error.value.reason.phase == "method_config"


@pytest.mark.parametrize("negative", [False, True])
@pytest.mark.parametrize("change", ["missing", "extra", "duplicate", "wrong_output", "row", "self"])
def test_manifest_inventory_rejection(study_payload, negative, change):
    evidence = _evidence(study_payload, negative=negative)
    first, output, last = evidence.artifact_descriptors
    if change == "missing":
        artifacts = (first, last)
    elif change == "extra":
        artifacts = (first, output, last, replace(output, key="extra.json"))
    elif change == "duplicate":
        artifacts = (first, output, last, first)
    elif change == "wrong_output":
        artifacts = (first, replace(output, key="graph.json" if negative else "diagnostics.json"), last)
    elif change == "row":
        artifacts = (first, replace(output, privacy_class="RESTRICTED_ROW_LEVEL"), last)
    else:
        artifacts = (first, output, last, replace(output, key="manifest.json"))
    with pytest.raises(ContractViolation) as error:
        LocalRunManifest.from_run_evidence(replace(evidence, artifact_descriptors=artifacts))
    assert error.value.reason.code == ("PRIVACY_POLICY_CONFLICT" if change == "row" else "SCHEMA_INVALID")


@pytest.mark.parametrize("mismatch", ["input_ref", "method", "request_hash"])
def test_manifest_rejects_invalid_study_projection(study_payload, mismatch):
    evidence = _evidence(study_payload)
    if mismatch == "input_ref":
        study_payload["inputs"]["dataset"]["identity"] = "other-data"
    elif mismatch == "method":
        study_payload["method"]["config"]["alpha"] = 0.1
    else:
        study_payload["request_hash"] = HASH
    with pytest.raises(ContractViolation) as error:
        LocalRunManifest.from_run_evidence(replace(evidence, study_payload=study_payload))
    assert error.value.reason.code == "SCHEMA_INVALID"


def test_hash_domains(study_payload):
    import hashlib

    graph_meaning = {"nodes": ["a", "b"], "edges": []}
    graph_hash = jcs.digest(graph_meaning)
    raw_graph = jcs.canonical_bytes({**graph_meaning, "content_hash": graph_hash})
    graph_bytes_hash = hashlib.sha256(raw_graph).hexdigest()
    evidence = _evidence(study_payload)
    artifacts = tuple(
        replace(item, sha256=graph_bytes_hash, size_bytes=len(raw_graph)) if item.key == "graph.json" else item
        for item in evidence.artifact_descriptors
    )
    evidence = replace(evidence, artifact_descriptors=artifacts,
                       output_graph_ref=replace(evidence.output_graph_ref, sha256=graph_bytes_hash))
    manifest_bytes = LocalRunManifest.from_run_evidence(evidence).to_canonical_bytes()
    request_hash = json.loads(manifest_bytes)["request_hash"]
    manifest_bytes_hash = hashlib.sha256(manifest_bytes).hexdigest()
    assert len({request_hash, graph_hash, graph_bytes_hash, manifest_bytes_hash}) == 4
