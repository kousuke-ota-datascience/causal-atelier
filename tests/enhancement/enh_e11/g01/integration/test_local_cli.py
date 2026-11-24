"""P05 CLI, Manifest dependency inversion, and real FS session lifecycle."""
from dataclasses import replace
import hashlib
from itertools import product
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from ariadne.capabilities.causal.local_execution import LocalRunContext
from ariadne.capabilities.causal.ports.local_io import PublicationSessionToken
from ariadne.interfaces.cli.local_causal import command
from ariadne.interfaces.cli.local_causal.config_decoder import StrictLocalConfigDecoder
from ariadne.interfaces.cli.local_causal.manifest import LocalRunManifest
from ariadne.interfaces.cli.local_causal.manifest_reader import LocalManifestReader
from ariadne.interfaces.cli.local_causal.privacy import LocalPrivacyPolicy
from ariadne.interfaces.cli.local_causal.publication import LocalPublicationAdapter, PublishState
from ariadne.shared.content_ref import ContentRef, ContractViolation
from ariadne.shared.local_fs import LocalPrincipal, TrustedLocalRoot

REPO = Path(__file__).resolve().parents[5]
RUN = "test-local"
NAMES = ("data-z", "data-y", "data-x")


@pytest.fixture
def root_path():
    with TemporaryDirectory(dir=REPO, prefix=".p05-test-") as directory:
        yield Path(directory)


def _private_write(path, data):
    with os.fdopen(os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600), "wb") as stream:
        stream.write(data)


def _inputs(root, *, row_requested=False):
    inputs = root / "inputs"
    inputs.mkdir(mode=0o700)
    assumptions = {"causal_markov_declared": True, "faithfulness_declared": True, "acyclicity_declared": True,
                   "latent_confounding_possible": True, "sampling_unit": "row"}
    design = {"design_id": "d", "question_id": "q", "design_kind": "OBSERVATIONAL_GRAPH_DISCOVERY",
              "variables": [{"name": name, "measurement_scale": "CONTINUOUS"} for name in NAMES],
              "assumptions": assumptions, "background_knowledge": None}
    question = {"question_id": "q", "research_question": "Synthetic fixture", "population": "Fixture",
                "analysis_goal": "GRAPH_STRUCTURE"}
    rows = list(product((-1.0, 1.0), repeat=3)) * 5
    buffer = pa.BufferOutputStream()
    pq.write_table(pa.table(dict(zip(NAMES, zip(*rows)))), buffer)
    refs = {}
    for field, name, identity, raw, media in (
        ("question", "q.json", "q", json.dumps(question).encode(), "application/json"),
        ("design", "d.json", "d", json.dumps(design).encode(), "application/json"),
        ("dataset", "data.parquet", "data", buffer.getvalue().to_pybytes(), "application/vnd.apache.parquet"),
    ):
        _private_write(inputs / name, raw)
        refs[field] = ContentRef(identity, f"inputs/{name}", hashlib.sha256(raw).hexdigest(), media, None).to_payload()
    wire = {"schema_version": "e11-local-study/1", "run_id": RUN, "operation": "DISCOVER",
            "analysis_mode": "EXPLORATORY", "inputs": {**refs, "graph": None, "identification": None},
            "estimand": {"family": "GRAPH_STRUCTURE", "population": "OBSERVED_VARIABLES", "contrast": "NOT_APPLICABLE"},
            "method": {"id": "P1-M06", "backend": "causal-learn", "config": {
                "indep_test": "fisherz", "alpha": 0.05, "depth": 0, "max_path_length": 0, "background_knowledge": None}},
            "inference": {"requested": False, "confidence_level": None}, "randomness": {"seed": None},
            "privacy": {"classification": "AGGREGATE", "row_export_requested": row_requested}}
    config = root / "study.json"
    _private_write(config, json.dumps(wire).encode())
    return config


def test_cli_check_and_publish_retry_on_real_ext4(root_path, capsys, monkeypatch):
    config = _inputs(root_path)
    actual_compose = command._compose
    use_case = actual_compose()
    real_factory = LocalRunManifest.from_run_evidence
    factory_calls = []

    def factory(evidence):
        factory_calls.append(evidence)
        return real_factory(evidence)

    monkeypatch.setattr(LocalRunManifest, "from_run_evidence", staticmethod(factory))
    monkeypatch.setattr(command, "_compose", lambda: use_case)
    argv = ["--config", str(config), "--output-root", str(root_path), "--json"]
    assert command.main([*argv, "--check-only"]) == 0
    observed = capsys.readouterr()
    assert json.loads(observed.out)["technical_status"] == "PREFLIGHT_OK"
    assert not observed.err and not (root_path / ".staging").exists() and not factory_calls
    assert command.main(argv) == 0
    observed = capsys.readouterr()
    assert json.loads(observed.out) == {
        "run_id": RUN, "technical_status": "COMPLETED", "science_acceptance": "NOT_EVALUATED",
        "manifest_relative_path": f"runs/{RUN}/manifest.json",
    }
    assert not observed.err and len(factory_calls) == 1
    names = {path.name for path in (root_path / "runs" / RUN).iterdir()}
    assert names == {"graph.json", "study.json", "status.json", "manifest.json", "_COMMITTED.json"}
    graph = json.loads((root_path / "runs" / RUN / "graph.json").read_bytes())
    assert graph["kind"] == "PAG" and graph["nodes"] == list(NAMES)
    with TrustedLocalRoot.open(root_path, allowed_directory=REPO) as trusted:
        assert LocalManifestReader().verify(root=trusted, run_id=RUN).run_id == RUN
    assert command.main(argv) == 0
    capsys.readouterr()
    assert len(factory_calls) == 1


def test_cli_denies_row_request_before_composition(root_path, capsys, monkeypatch):
    config = _inputs(root_path, row_requested=True)
    monkeypatch.setattr(command, "_compose", lambda: pytest.fail("Composed a denied request"))
    assert command.main(["--config", str(config), "--output-root", str(root_path), "--json"]) == 3
    result = capsys.readouterr()
    assert json.loads(result.out)["phase"] == "privacy"
    assert str(root_path) not in result.out + result.err
    assert not (root_path / ".staging").exists()


@pytest.mark.parametrize("mismatch", [
    "issuer", "different_run", "same_run_new_token", "root", "hash", "policy", "fake", "invalid_token", "legacy",
])
def test_abort_refuses_mismatched_sessions_without_mutation(root_path, mismatch):
    policy = LocalPrivacyPolicy()
    adapter = LocalPublicationAdapter(policy)
    second = LocalPublicationAdapter(policy if mismatch != "policy" else LocalPrivacyPolicy())
    with TrustedLocalRoot.open(root_path, allowed_directory=REPO) as root:
        with TrustedLocalRoot.open(root_path, allowed_directory=REPO) as other_root:
            session = PublicationSessionToken()
            expected = {"session": session, "run_id": RUN, "request_hash": "a" * 64, "root": root}
            first = adapter.begin(**expected)
            other_token = PublicationSessionToken()
            other = (second if mismatch in ("issuer", "policy") else adapter).begin(
                run_id="other" if mismatch == "different_run" else RUN, request_hash="a" * 64, root=root,
                session=None if mismatch == "legacy" else other_token,
            )
            wrong = {"issuer": other, "different_run": other, "same_run_new_token": other,
                     "policy": other, "fake": object(), "legacy": other}.get(mismatch, first)
            actual = dict(expected)
            if mismatch in ("issuer", "different_run", "policy"):
                actual["session"] = other_token
            if mismatch == "root":
                actual["root"] = other_root
            if mismatch == "hash":
                actual["request_hash"] = "b" * 64
            if mismatch == "invalid_token":
                actual["session"] = object()
            try:
                first_handle, other_handle = first._publisher.staging_handle, other._publisher.staging_handle
                with pytest.raises(ContractViolation) as caught:
                    adapter.abort(sink=wrong, reason="TEST", **actual)
                assert caught.value.reason.code == "PUBLICATION_FAILED"
                assert first._publisher.state is other._publisher.state is PublishState.STAGING
                os.fstat(first_handle.directory)
                os.fstat(other_handle.directory)
                adapter.abort(sink=first, reason="TEST", **expected)
                assert first._publisher.state is PublishState.ABORTED
                with pytest.raises(OSError):
                    os.fstat(first_handle.directory)
                with pytest.raises(ContractViolation):
                    adapter.abort(sink=first, reason="TEST", **expected)
                assert other._publisher.state is PublishState.STAGING
            finally:
                if first._publisher.state is PublishState.STAGING:
                    first._publisher.abort("TEST_CLEANUP")
                other._publisher.abort("TEST_CLEANUP")
    assert not (root_path / "runs").exists()
    assert not list(root_path.glob(".staging/*/_COMMITTED.json"))


def test_begin_rejects_invalid_token_before_staging(root_path):
    with TrustedLocalRoot.open(root_path, allowed_directory=REPO) as root:
        with pytest.raises(ContractViolation):
            LocalPublicationAdapter(LocalPrivacyPolicy()).begin(
                run_id=RUN, request_hash="a" * 64, root=root, session=object(),
            )
    assert not (root_path / ".staging").exists()


@pytest.fixture(scope="module")
def runtime_use_case():
    return command._compose()


class _PublicationSpy:
    def __init__(self, concrete, *, fail_publish=False):
        self.concrete = concrete
        self.fail_publish = fail_publish
        self.begins = []
        self.aborts = []
        self.publishes = 0

    def begin(self, **kwargs):
        sink = self.concrete.begin(**kwargs)
        self.begins.append((kwargs, sink))
        return sink

    def seal(self, **kwargs):
        return self.concrete.seal(**kwargs)

    def abort(self, **kwargs):
        expected, sink = self.begins[-1]
        assert kwargs.pop("sink") is sink
        assert {key: kwargs[key] for key in expected} == expected
        self.aborts.append(sink)
        self.concrete.abort(sink=sink, **kwargs)

    def publish(self, **kwargs):
        self.publishes += 1
        if self.fail_publish:
            # Exercise the Application boundary. Concrete Publisher owns its handles after this call.
            raise ContractViolation("PUBLICATION_INDETERMINATE", "publication", "Fixture")
        return self.concrete.publish(**kwargs)


class _FailingFactory:
    def build(self, *, evidence):
        raise ContractViolation("SCHEMA_INVALID", "publication", "Fixture")


@pytest.mark.parametrize("start_publish", [False, True])
def test_use_case_aborts_only_before_publish(root_path, runtime_use_case, start_publish):
    config = _inputs(root_path)
    spec = StrictLocalConfigDecoder().decode(config.read_bytes(), declared_format="json")
    spy = _PublicationSpy(runtime_use_case.publisher, fail_publish=start_publish)
    factory = runtime_use_case.manifest_factory if start_publish else _FailingFactory()
    use_case = replace(runtime_use_case, publisher=spy, manifest_factory=factory)
    with TrustedLocalRoot.open(root_path, allowed_directory=REPO) as root:
        with pytest.raises(ContractViolation) as caught:
            use_case.run(spec, LocalRunContext(root, LocalPrincipal.current()))
        code = "PUBLICATION_INDETERMINATE" if start_publish else "SCHEMA_INVALID"
        assert caught.value.reason.code == code
        assert len(spy.aborts) == (0 if start_publish else 1)
        assert spy.publishes == int(start_publish)
        if start_publish:
            spy.begins[0][1]._publisher.abort("TEST_CLEANUP")
    assert not (root_path / "runs" / RUN).exists()


@pytest.mark.parametrize(("failure", "expected"), [("legacy", 2), ("hash", 3), ("bk", 4), ("existing", 5)])
def test_cli_failure_categories_without_publication(root_path, capsys, runtime_use_case, monkeypatch, failure, expected):
    config = _inputs(root_path)
    wire = json.loads(config.read_bytes())
    if failure == "legacy":
        wire["schema_version"] = "causal-analysis-spec/2"
    elif failure == "hash":
        wire["inputs"]["question"]["sha256"] = "b" * 64
    elif failure == "bk":
        bk = {"required_edges": [], "forbidden_edges": []}
        design_path = root_path / "inputs" / "d.json"
        design = json.loads(design_path.read_bytes())
        design["background_knowledge"] = bk
        raw = json.dumps(design).encode()
        design_path.write_bytes(raw)
        wire["inputs"]["design"]["sha256"] = hashlib.sha256(raw).hexdigest()
        wire["method"]["config"]["background_knowledge"] = bk
    else:
        (root_path / "runs").mkdir(mode=0o700)
        (root_path / "runs" / RUN).mkdir(mode=0o700)
    config.write_text(json.dumps(wire))
    monkeypatch.setattr(command, "_compose", lambda: runtime_use_case)
    assert command.main(["--config", str(config), "--output-root", str(root_path), "--json"]) == expected
    result = capsys.readouterr()
    envelope = json.loads(result.out)
    assert envelope["technical_status"] == "FAILED" and envelope["manifest_relative_path"] is None
    assert str(root_path) not in result.out + result.err
    assert not (root_path / ".staging").exists()
    assert not (root_path / "runs" / RUN / "_COMMITTED.json").exists()


def test_application_has_no_cli_implementation_import():
    import ast
    from ariadne.capabilities.causal import local_execution
    from ariadne.capabilities.causal.ports import manifest_factory

    for module in (local_execution, manifest_factory):
        tree = ast.parse(Path(module.__file__).read_text())
        for statement in ast.walk(tree):
            if isinstance(statement, ast.ImportFrom):
                assert not (statement.module or "").startswith("ariadne.interfaces.cli")
            elif isinstance(statement, ast.Import):
                assert all(not item.name.startswith("ariadne.interfaces.cli") for item in statement.names)
