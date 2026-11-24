# G01 Trial 01 独立プローブ再実行資料

以下のコードはリポジトリ外の一時ファイルとして実行した。記録したファイル名で各コードを保存し、固定候補 checkout から [実測出力](independent_raw_evidence.md) のコマンドを実行する。これらのプローブには合成データのみを使った。pytest の固定候補テストと実 CLI は既存 `.venv` を使用した。Schema の観測だけは別領域 `/tmp/e11-g01-schema-tools` にインストールした `jsonschema==4.19.2`（attrs 26.1.0、jsonschema-specifications 2025.9.1、referencing 0.37.0、rpds-py 2026.9.1、typing-extensions 4.16.0）を `PYTHONPATH` に追加した。

## e11_g01_trial01_independent_regression_audit.py

SHA-256 `0334ac81eb122bbea6a1f6bdfaa2789289f85ea3cdb63a6bcc06fd15eee05135`。

```python
import ast
import hashlib
import importlib.metadata as md
import pathlib
import re
import subprocess
import sys
import tomllib
from collections import deque

base, candidate = (pathlib.Path(arg) for arg in sys.argv[1:])
banned = {"lightgbm", "dowhy", "econml"}
def read(path):
    return tomllib.loads(path.read_text())
before, after = (read(root / "pyproject.toml") for root in (base, candidate))
for key in ("dependencies", "optional-dependencies"):
    assert before["project"][key] == after["project"][key]
assert before.get("dependency-groups") == after.get("dependency-groups")
print("TOML declarations identical", len(after["project"]["dependencies"]), sorted(after["project"]["optional-dependencies"]), sorted(after.get("dependency-groups", {})))
delta = after["project"]["scripts"].pop("ariadne-causal-local")
assert delta == "ariadne.interfaces.cli.local_causal.command:main" and before == after
print("Only structured TOML delta: ariadne-causal-local =", delta)
lock = (candidate / "uv.lock").read_bytes()
assert lock == (base / "uv.lock").read_bytes()
print("Lock SHA256", hashlib.sha256(lock).hexdigest())
for root in (base, candidate):
    source = "\n".join(path.read_text().lower() for path in (root / "src/ariadne/capabilities/causal").glob("*.py"))
    for name in sorted(banned):
        assert f"import {name}" not in source and f"from {name}" not in source
        print(root.name, "original source assertions", name, "PASS")
def git(*args):
    return subprocess.check_output(["git", "-C", str(candidate), *args], text=True).splitlines()
changed = [p for p in git("diff", "--name-only", "ff38f224", "HEAD", "--", "src") if p.endswith(".py")]
def closure(root, starting):
    src = root / "src"
    pending = deque()
    def enqueue(module):
        parts = module.split(".")
        for end in range(1, len(parts) + 1):
            path = src.joinpath(*parts[:end])
            pending.extend(p for p in (path.with_suffix(".py"), path / "__init__.py") if p.is_file())
    for relative in starting:
        file = pathlib.Path(relative).relative_to("src")
        enqueue(".".join(file.with_suffix("").parts).removesuffix(".__init__"))
    seen, external, dynamic = set(), set(), set()
    while pending:
        path = pending.popleft()
        if path in seen:
            continue
        seen.add(path)
        name = path.relative_to(src).with_suffix("").parts
        package = name[:-1]
        for node in ast.walk(ast.parse(path.read_bytes())):
            if isinstance(node, ast.Import):
                imports = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                prefix = ".".join(package[:len(package)-node.level+1]) if node.level else ""
                target = ".".join(part for part in (prefix, node.module) if part)
                imports = [target, *[f"{target}.{alias.name}" for alias in node.names]]
            else:
                if isinstance(node, ast.Call):
                    function = ast.unparse(node.func)
                    if function.rsplit(".",1)[-1] in {"import_module","__import__","find_spec","entry_points","CDLL","run","Popen","compile","exec","eval"}:
                        dynamic.add((str(path.relative_to(src)), node.lineno, function))
                continue
            for module in filter(None, imports):
                top = module.split(".")[0]
                if top == "ariadne":
                    enqueue(module)
                elif top not in sys.stdlib_module_names:
                    external.add(top)
    return {str(p.relative_to(root)) for p in seen}, external, dynamic
local, external, dynamic = closure(candidate, changed)
assert not banned & external
print("Changed source modules", len(changed), "reachable Python source modules", len(local), "external import roots", sorted(external))
for item in sorted(dynamic):
    print("dynamic", *item)
package_map = md.packages_distributions()
def canonical(name):
    return re.sub("[-_.]+", "-", name).lower()
pending = deque(name for top in external for name in package_map[top])
versions = set()
from packaging.requirements import Requirement
while pending:
    dist = md.distribution(pending.popleft())
    key = canonical(dist.name), dist.version
    if key in versions:
        continue
    versions.add(key)
    for raw in dist.requires or ():
        req = Requirement(raw)
        if req.marker is None or req.marker.evaluate({"extra": ""}):
            pending.append(req.name)
assert not banned & {name for name,_ in versions}
locked = {(canonical(p["name"]),p["version"]) for p in read(candidate / "uv.lock")["package"]}
assert versions <= locked, versions - locked
print("Effective external distribution closure in lock", sorted(versions))
runtime = ["src/ariadne/capabilities/causal/workflow.py"]
old, old_external, old_dynamic = closure(base, runtime)
new, new_external, new_dynamic = closure(candidate, runtime)
assert (old, old_external, old_dynamic) == (new, new_external, new_dynamic)
assert all((base / path).read_bytes() == (candidate / path).read_bytes() for path in old)
print("Legacy planner closure identical",len(old), "modules", sorted(old_external))
legacy_test = "tests/product/test_enh_e5_g03_p03_causal_runtime_regression.py"
nav = [legacy_test, "frontend/navigation_state.js", "frontend/app.js", "frontend"]
assert not git("diff","--name-only","ff38f224","HEAD","--",*nav)
for path in nav:
    assert git("rev-parse",f"ff38f224:{path}") == git("rev-parse",f"HEAD:{path}")
    print("Unchanged navigation input",path,git("rev-parse",f"HEAD:{path}")[0])

```

## e11_g01_trial01_independent_cli_audit.py

SHA-256 `7db132823ba5475936d893c8b2a36b6e10f5d7b2ef283a7a118c1d2d8596d325`。

```python
import dataclasses
import hashlib
import importlib.util
import itertools
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import tomllib
from unittest.mock import patch

import pyarrow as pa
import pyarrow.parquet as pq
from ariadne.interfaces.cli.local_causal import command
from ariadne.interfaces.cli.local_causal.manifest_reader import LocalManifestReader
from ariadne.shared.local_fs import TrustedLocalRoot
from ariadne.shared.serialization import jcs

cwd = pathlib.Path.cwd()
fixture_path = cwd / "tests/enhancement/enh_e11/g01/integration/test_local_cli.py"
def fixture(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
fixture_cli = fixture("fixture_cli", fixture_path)
fixture_boundary = fixture("fixture_boundary", cwd / "tests/product/test_enh_e4_g07_p03_cli_boundary.py")
def digest(raw):
    return hashlib.sha256(raw).hexdigest()
def canonical_write(path, data):
    raw = jcs.canonical_bytes(data)
    path.write_bytes(raw)
    return digest(raw)
def audit(root, params=(), expected=(0, None), prior=True):
    result = subprocess.run([sys.executable, "-m", command.__name__, "--config", str(root/"study.json"),
                             "--output-root", str(root), "--json", *params], capture_output=True, text=True)
    streams = result.stdout + result.stderr
    assert str(root) not in streams and "data-z" not in streams
    assert len(result.stdout.strip().splitlines()) == 1, result.stderr
    data = json.loads(result.stdout)
    assert (result.returncode, data.get("reason_code")) == expected, (result.returncode, data, result.stderr)
    if not prior:
        assert not (root/".staging").exists() and not (root/"runs").exists()
    print("CLI", result.returncode, json.dumps(data, sort_keys=True), "stderr", result.stderr.strip())
    return data
def read(path):
    return json.loads(path.read_bytes())
def mutate_content(root, wire, key, payload):
    ref = wire["inputs"][key]
    ref["sha256"] = canonical_write(root / ref["relative_key"], payload)

with tempfile.TemporaryDirectory(dir=sys.argv[1], prefix="e11-independent-cli-") as temporary:
    p = pathlib.Path(temporary)
    for name in ["full", "corrupt_status", "invalid_question", "invalid_design_order", "old_row_flag", "row_opt_in", "noncontiguous_chisq", "noncontiguous_gsq", "e_lt_5", "absent_domain", "empty_bk", "conflicting_bk"]:
        root = p / name
        root.mkdir(mode=0o700)
        config = fixture_cli._inputs(root)
        wire = read(config)
        run = root / "runs" / wire["run_id"]
        print("case",name,flush=True)
        if name in {"full","corrupt_status"}:
            assert audit(root, ("--check-only",), prior=False)["technical_status"] == "PREFLIGHT_OK"
            assert audit(root)["technical_status"] == "COMPLETED"
            marker = read(run/"_COMMITTED.json")
            manifest = read(run/"manifest.json")
            assert manifest["runtime"]["repo_commit"] == os.environ["E11_CANDIDATE_SHA"]
            assert manifest["runtime"]["dirty"] is False
            assert marker["manifest_sha256"] == digest((run/"manifest.json").read_bytes())
            assert marker["request_hash"] == manifest["request_hash"] == digest(jcs.canonical_bytes(read(config)))
            assert set(x.name for x in run.iterdir()) == {"_COMMITTED.json","manifest.json","study.json","status.json","graph.json"}
            for a in manifest["artifacts"]:
                raw = (run/a["key"]).read_bytes()
                assert (len(raw),digest(raw)) == (a["size_bytes"],a["sha256"])
                assert raw == jcs.canonical_bytes(json.loads(raw))
            assert read(run/"graph.json")["provenance"]["source_refs"] == {k:wire["inputs"][k] for k in ["question","design","dataset"]}
            with TrustedLocalRoot.open(root, allowed_directory=root) as trusted:
                assert LocalManifestReader().read_run(trusted, wire["run_id"]).request_hash == marker["request_hash"]
            if name == "full":
                assert audit(root)["technical_status"] == "COMPLETED"
                assert (run/"manifest.json").read_bytes() == jcs.canonical_bytes(manifest)
            else:
                status = read(run/"status.json")
                status["technical_status"] = "SUCCESS"
                raw = jcs.canonical_bytes(status)
                (run/"status.json").write_bytes(raw)
                entry = next(a for a in manifest["artifacts"] if a["key"] == "status.json")
                entry.update(size_bytes=len(raw), sha256=digest(raw))
                marker["manifest_sha256"] = canonical_write(run/"manifest.json",manifest)
                canonical_write(run/"_COMMITTED.json",marker)
                audit(root,expected=(5,"SCHEMA_INVALID"))
            continue
        if name == "invalid_question":
            q = read(root/"inputs/q.json")
            q["question_id"] = "other"
            mutate_content(root,wire,"question",q)
        if name == "invalid_design_order":
            d = read(root/"inputs/d.json")
            d["variables"].reverse()
            mutate_content(root,wire,"design",d)
        if name == "old_row_flag":
            audit(root,("--allow-row-level-export",),expected=(2,"SCHEMA_INVALID"),prior=False)
            continue
        if name == "row_opt_in":
            wire["privacy"]["row_export_requested"] = True
        if name in {"empty_bk","conflicting_bk"}:
            edges = [list(fixture_cli.NAMES[:2])] if name=="conflicting_bk" else []
            bk = {"required_edges":edges, "forbidden_edges":edges}
            d = read(root/"inputs/d.json")
            d["background_knowledge"] = bk
            wire["method"]["config"]["background_knowledge"] = bk
            mutate_content(root,wire,"design",d)
        if name in {"noncontiguous_chisq","noncontiguous_gsq","e_lt_5","absent_domain"}:
            d = read(root/"inputs/d.json")
            for v in d["variables"]:
                v.update(measurement_scale="CATEGORICAL",category_codes=[0,2,4] if name=="absent_domain" else [0,2])
            mutate_content(root,wire,"design",d)
            rows = list(itertools.product([0,2],repeat=3))*(4 if name=="e_lt_5" else 5)
            path = root/"inputs/data.parquet"
            pq.write_table(pa.table(dict(zip(fixture_cli.NAMES,zip(*rows)))),path)
            wire["inputs"]["dataset"]["sha256"] = digest(path.read_bytes())
            wire["method"]["config"]["indep_test"] = "gsq" if name.endswith("gsq") else "chisq"
            print("Independent balanced-table minimum for observed levels per nonempty stratum",len(rows)//2//4)
        canonical_write(config,wire)
        if name.startswith("noncontiguous"):
            assert audit(root)["technical_status"] == "COMPLETED"
        else:
            expected = {"row_opt_in":(3,"PRIVACY_DENIED"),"empty_bk":(4,"BACKEND_SEMANTICS_UNVERIFIED"),"conflicting_bk":(4,"BACKEND_SEMANTICS_UNVERIFIED")}
            observed = audit(root,expected=expected.get(name,(2,"UNSUPPORTED_COMBINATION")),prior=False)

classification = fixture_boundary.test_all_analysis_cli_scripts_match_explicit_classifications
original_loader = tomllib.loads
classification()
print("AMD-004 exact six-entry positive PASS")
for action, name in itertools.product(("remove","redirect_in","redirect_out"), ("ariadne-discover","ariadne-causal-local")):
    def changed(config):
        result = original_loader(config)
        scripts = result["project"]["scripts"]
        if action == "remove":
            del scripts[name]
        elif action == "redirect_in":
            scripts[name] = "ariadne.interfaces.cli.other:main"
        else:
            scripts[name] = "ariadne.other:main"
        return result
    with patch.object(tomllib,"loads",changed):
        try:
            classification()
        except AssertionError:
            print("AMD-004 rejected", action,name)
        else:
            raise AssertionError((action,name))
def extra(config):
    result = original_loader(config)
    result["project"]["scripts"]["extra-case"] = "ariadne.interfaces.cli.other:main"
    return result
with patch.object(tomllib,"loads",extra):
    try:
        classification()
    except AssertionError:
        print("AMD-004 rejected extra in-namespace")
    else:
        raise AssertionError("accepted extra")

```

## e11_g01_trial01_independent_schema_audit.py

SHA-256 `1ff6742df6cdf52035adb44d6f577ec4f88afbfed30c6802ff73298443e6b3fc`。

```python
import hashlib
import inspect
import json
import pathlib
import sys

from jsonschema import Draft202012Validator
from causallearn.search.ConstraintBased.FCI import fci
from ariadne.causal.discovery.contracts import DiscoveryDesign
from ariadne.interfaces.cli.local_causal.config_decoder import StrictLocalConfigDecoder
from ariadne.scientific.causal_methods.discovery import FciBackend
from ariadne.shared.content_ref import ContractViolation
from ariadne.shared.serialization import jcs

schemas = pathlib.Path(sys.argv[1])
def validator(relative):
    raw = (schemas / relative).read_bytes()
    schema = json.loads(raw)
    print("Schema",relative,hashlib.sha256(raw).hexdigest())
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)
design = validator("e11_p1_m06_fci_design_profile_v1.schema.json")
question = validator("e11_p1_m06_fci_question_profile_v1.schema.json")
config = validator("e11_p1_m06_fci_method_config_v1.schema.json")
diag = validator("internal_scientific/e11_g01_discover_negative_diagnostics_draft1.schema.json")
q = {"question_id":"q","research_question":"fixture","population":"fixture","analysis_goal":"GRAPH_STRUCTURE"}
assert question.is_valid(q) and not question.is_valid(dict(q,unexpected=True))
mc = {"indep_test":"fisherz","alpha":0.05,"depth":0,"max_path_length":0,"background_knowledge":None}
for ci in ("fisherz","chisq","gsq"):
    assert config.is_valid(dict(mc,indep_test=ci))
assert not config.is_valid(dict(mc,indep_test="pc")) and not config.is_valid({})
dn = {"run_id":"q","operation":"DISCOVER","method_id":"P1-M06","reason_codes":["SCI_NO_ADMISSIBLE_PAG"]}
assert diag.is_valid(dn) and not diag.is_valid(dict(dn,reason_codes=["BACKEND_API_MISMATCH"]))
print("Question, Config and synthetic diagnostics positive/negative controls PASS")
bare = {"design_id":"d","question_id":"q","design_kind":"OBSERVATIONAL_GRAPH_DISCOVERY",
        "assumptions":{"causal_markov_declared":True,"faithfulness_declared":True,"acyclicity_declared":True,
                       "latent_confounding_possible":True,"sampling_unit":"row"},"background_knowledge":None}
for label,scale,tokens,expected_schema,expected_parser in [
    ("binary","CATEGORICAL","[0,1]",True,True),
    ("noncontiguous","CATEGORICAL","[0,2]",True,True),
    ("missing","CATEGORICAL",None,False,False),
    ("duplicate","CATEGORICAL","[0,0]",False,False),
    ("descending","CATEGORICAL","[1,0]",True,False),
    ("fractional","CATEGORICAL","[0,1.5]",False,False),
    ("decimal","CATEGORICAL","[0,1.0]",True,False),
    ("exponent","CATEGORICAL","[0,1e0]",True,False),
    ("boolean","CATEGORICAL","[0,true]",False,False),
    ("string","CATEGORICAL",'[0,"1"]',False,False),
    ("overflow","CATEGORICAL","[0,9223372036854775808]",True,False),
    ("ordinary_continuous","CONTINUOUS",None,True,True),
    ("continuous_with_codes","CONTINUOUS","[0,1]",False,False),
]:
    v = {"name":"x","measurement_scale":scale}
    if tokens:
        v["category_codes"] = json.loads(tokens)
    instance = dict(bare,variables=[v,dict(v,name="y")])
    structural = design.is_valid(instance)
    try:
        DiscoveryDesign.from_payload(instance,question_id="q",background_knowledge=None)
        semantic = True
    except ContractViolation:
        semantic = False
    assert (structural,semantic) == (expected_schema,expected_parser), label
    print("Design",label,"schema",structural,"parser",semantic)
gold_path = schemas / "e11_jcs_golden_vectors.json"
gold = json.loads(gold_path.read_bytes())
print("JCS vector SHA256",hashlib.sha256(gold_path.read_bytes()).hexdigest())
for item in gold["positive"]:
    expected = item["expected_canonical_utf8_json"].encode()
    encoded = jcs.canonical_bytes(item["input"])
    assert encoded == expected and hashlib.sha256(encoded).hexdigest() == item["expected_sha256"]
    print(item["id"],hashlib.sha256(encoded).hexdigest())
def expect_rejection(name, fn):
    try:
        fn()
    except (ValueError,ContractViolation):
        print(name,"rejected")
    else:
        raise AssertionError(name)
for raw in (b"NaN", b"Infinity", b"-Infinity"):
    expect_rejection("JCS-N01",lambda: jcs.parse_json(raw))
expect_rejection("JCS-N02 JSON",lambda: jcs.parse_json(b'{"k":1,"k":2}'))
expect_rejection("JCS-N02 YAML",lambda: StrictLocalConfigDecoder().decode(b"k: 1\nk: 2",declared_format="yaml"))
expect_rejection("JCS-N03",lambda: jcs.parse_json(br'"\ud800"'))
expect_rejection("JCS-N04",lambda: jcs.parse_json(b"9007199254740993"))
expect_rejection("JCS-N05",lambda: jcs.canonical_bytes(object()))
assert jcs.canonical_bytes("é") != jcs.canonical_bytes("e\u0301")
print("JCS-N06 NFC/NFD remain distinct")
expect_rejection("JCS-N07",lambda: StrictLocalConfigDecoder().decode(b'{"schema_version":"causal-analysis-spec/2"}',declared_format="json"))
observed = FciBackend().probe()
signature = inspect.signature(fci)
assert "node_names" in signature.parameters
assert observed.reason is None and observed.distribution_version == "0.1.4.8"
assert observed.api_signature_hash == hashlib.sha256(str(signature).encode()).hexdigest()
print("FCI backend", observed, "signature", signature)

```

## e11_g01_trial01_independent_wire_audit.py

SHA-256 `b6f1581d0c6f2dafb907d59f2d1700db351cc619cf7c7c6cddd27d3a7ae8eae4`。

```python
import hashlib
import importlib.util
import json
import pathlib
import sys
import tempfile
from jsonschema import Draft202012Validator
from ariadne.interfaces.cli.local_causal import command

schema_dir = pathlib.Path(sys.argv[1])
fixture_path = pathlib.Path("tests/enhancement/enh_e11/g01/integration/test_local_cli.py")
spec = importlib.util.spec_from_file_location("fixture",fixture_path)
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)
failures = []
with tempfile.TemporaryDirectory(dir=sys.argv[2],prefix="e11-independent-wire-") as d:
    p = pathlib.Path(d)
    config = fixture._inputs(p)
    assert command.main(["--config",str(config),"--output-root",str(p),"--json"]) == 0
    run = p/"runs"/fixture.RUN
    for kind, filename in [("study","study.json"),("status","status.json"),("manifest","manifest.json"),("graph","graph.json"),("commit_marker","_COMMITTED.json")]:
        raw_schema = (schema_dir/f"e11_local_{kind}_v1.schema.json").read_bytes()
        schema = json.loads(raw_schema)
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        document = json.loads((run/filename).read_bytes())
        invalid = list(validator.iter_errors(document))
        if invalid:
            for error in invalid:
                print("schema violation",kind,"path",list(error.path),"validation",error.validator,error.message)
            failures.append(kind)
        key = "marker_version" if kind == "commit_marker" else "schema_version"
        assert not validator.is_valid(dict(document,**{key:"unknown/0"}))
        print("Actual wire",kind,"valid",not invalid,"schema SHA256",hashlib.sha256(raw_schema).hexdigest())
assert not failures, failures

```

## e11_g01_trial01_independent_amendment_audit.py

SHA-256 `9121bb6984fb92ec015179f0da9629facbd70d86a5a0d40e55f887a0bede93c7`。

```python
import dataclasses
import importlib.util
import pathlib
import sys
import tempfile
from collections import Counter
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from unittest.mock import patch

from ariadne.capabilities.causal.ports.local_io import PublicationSessionToken
from ariadne.interfaces.cli.local_causal import command
from ariadne.interfaces.cli.local_causal.publication import PublishState
from ariadne.scientific.causal_methods.discovery import FciBackend
from ariadne.shared.content_ref import ContractViolation
from ariadne.shared.local_fs import TrustedLocalRoot
from ariadne.shared.serialization import jcs

def use_fixture(name):
    file = pathlib.Path("tests/enhancement/enh_e11/g01/integration") / ("test_" + name + ".py")
    spec = importlib.util.spec_from_file_location(name,file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
cli = use_fixture("local_cli")
publication = use_fixture("local_publication")
composition = command._compose()
assert len(composition.__dataclass_fields__) == 12
try:
    dataclasses.replace(composition, manifest_factory=None)
except TypeError:
    print("AMD-001 required manifest_factory TypeError")
else:
    raise AssertionError("factory dependency accepted as None")

class Proxy:
    def __init__(self, publisher, failure):
        self.publisher, self.failure = publisher, failure
        self.calls = Counter()

    def begin(self, **args):
        self.calls["begin"] += 1
        if self.failure == "begin":
            raise ContractViolation("PUBLICATION_FAILED","publication","fixture")
        self.args = args
        self.sink = self.publisher.begin(**args)
        return self.sink

    def abort(self, **args):
        self.calls["abort"] += 1
        assert args == dict(self.args,sink=self.sink,reason="PREPUBLICATION_FAILED")
        self.publisher.abort(**args)
        if self.failure == "cleanup":
            raise ContractViolation("PUBLICATION_FAILED","publication","synthetic secret should be absent")

    def seal(self, **args):
        self.calls["seal"] += 1
        if self.failure == "seal":
            raise ContractViolation("PUBLICATION_FAILED","publication","fixture")
        self.bundle = self.publisher.seal(**args)
        return self.bundle

    def publish(self, **args):
        self.calls["publish"] += 1
        if self.failure == "publish":
            raise ContractViolation("PUBLICATION_INDETERMINATE","publication","fixture")
        return self.publisher.publish(**args)
class Factory:
    def build(self, *, evidence):
        raise ContractViolation("SCHEMA_INVALID","publication","fixture")
class Runtime:
    def resources_available(self):
        return True
    def snapshot(self, capability):
        raise ContractViolation("RUNTIME_EVIDENCE_UNAVAILABLE","publication","fixture")

for label, phase, reason in [
    ("check-only",0,"PREFLIGHT_OK"),("begin",5,"PUBLICATION_FAILED"),("discovery",4,"BACKEND_EXECUTION_FAILED"),
    ("runtime",5,"RUNTIME_EVIDENCE_UNAVAILABLE"),("factory",5,"SCHEMA_INVALID"),
    ("seal",5,"PUBLICATION_FAILED"),("cleanup",5,"SCHEMA_INVALID"),
    ("publish",5,"PUBLICATION_INDETERMINATE"),
]:
    with tempfile.TemporaryDirectory(dir=sys.argv[1],prefix="e11-independent-amd-") as t:
        p = pathlib.Path(t)
        config = cli._inputs(p)
        proxy = Proxy(composition.publisher,label)
        changes = {"publisher":proxy}
        if label in ("factory","cleanup"):
            changes["manifest_factory"] = Factory()
        if label == "runtime":
            changes["runtime"] = Runtime()
        args = ["--config",str(config),"--output-root",str(p),"--json"]
        if label == "check-only":
            args += ["--check-only"]
        out, err = StringIO(), StringIO()
        def fit_injected(*args, **kwargs):
            raise ContractViolation("BACKEND_EXECUTION_FAILED","engine","fixture")
        selection = patch.object(FciBackend,"fit",fit_injected) if label=="discovery" else patch.object(FciBackend,"fit",FciBackend.fit)
        with patch.object(command,"_compose",return_value=dataclasses.replace(composition,**changes)), selection, redirect_stdout(out), redirect_stderr(err):
            assert command.main(args) == phase
        assert reason in out.getvalue()
        assert "synthetic secret" not in out.getvalue()+err.getvalue()
        assert proxy.calls["abort"] == (0 if label in ("begin","check-only","publish") else 1)
        assert proxy.calls["publish"] == (1 if label=="publish" else 0)
        assert proxy.calls["begin"] == (0 if label=="check-only" else 1)
        assert not (p/"runs").exists()
        if label!="publish":
            assert not list(p.glob(".staging/*/_COMMITTED.json"))
        else:
            assert proxy.sink._publisher.state is PublishState.VALIDATING
            proxy.sink._publisher.abort("TEST_CLEANUP")
        assert ("PUBLICATION_ABORT_FAILED" in err.getvalue()) == (label=="cleanup")
        print("AMD-002/003",label,"exit",phase,dict(proxy.calls),out.getvalue().strip(),err.getvalue().strip())

for field, bad in [("classification","ROW"),("row_export_requested",True),("output_shape","UNKNOWN")]:
    with tempfile.TemporaryDirectory(dir=sys.argv[1],prefix="e11-independent-privacy-") as t:
        p = pathlib.Path(t)
        with TrustedLocalRoot.open(p,allowed_directory=p) as root:
            adapter,sink,manifest,decision = publication._prepare(root,p)
            assert hasattr(decision,field), (field,dataclasses.fields(decision))
            try:
                adapter.seal(sink=sink,manifest=manifest,privacy=dataclasses.replace(decision,**{field:bad}))
            except ContractViolation as error:
                assert error.reason.code == "PRIVACY_POLICY_CONFLICT" and error.reason.phase == "privacy",error.reason
                assert not (p/"runs").exists() and not list(p.glob(".staging/*/_COMMITTED.json"))
                print("privacy field",field,error.reason.code)
            else:
                raise AssertionError(field)

```

## e11_g01_trial01_independent_ci_audit.py

SHA-256 `7f631d3292f7755f364214305aa86c854967fd0356935ea8e0cc780b26d2ecc1`。

```python
import importlib.util
import itertools
from pathlib import Path
from unittest.mock import patch

import numpy as np
from ariadne.scientific.causal_methods.discovery import FciBackend
from ariadne.scientific.causal_methods.fci_eligibility import ScientificEligibilityPolicy
from ariadne.scientific.ports.causal import LocalDiscoveryDispatcher
from ariadne.shared.content_ref import ContractViolation

spec = importlib.util.spec_from_file_location("fixture",Path("tests/enhancement/enh_e11/g01/integration/test_fci_discovery.py"))
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)
obs = FciBackend().probe()
assert obs.reason is None
registry = fixture._registry(obs,FciBackend)
rows = list(itertools.product((-1.0,1.0),repeat=3))*5
data = np.asarray(rows,dtype=np.float64)
full = np.corrcoef(data.T)
for x,y in itertools.combinations(range(3),2):
    other = next(iter(set(range(3))-{x,y}))
    for s in [(),(other,)]:
        order = [x,y,*s]
        matrix = full[np.ix_(order,order)]
        np.linalg.cholesky(matrix)
        eps_cond = np.linalg.cond(matrix,2)*np.finfo(np.float64).eps
        inverse = np.linalg.inv(matrix)
        residuals = [max(np.abs(prod - np.eye(len(order))).sum(axis=1)) for prod in (matrix@inverse,inverse@matrix)]
        partial = -inverse[0,1]/np.sqrt(inverse[0,0]*inverse[1,1])
        assert len(rows)>len(s)+3 and eps_cond<=1e-6 and max(residuals)<=1e-8 and abs(partial)<1
        print("float64 all-S",x,y,s,"condition*eps",eps_cond,"residual row sums",residuals,"partial r",partial)
req = fixture._request("fisherz",rows,registry)
evidence = ScientificEligibilityPolicy(lambda: True).check(req)[1]
assert evidence.expected_triples == evidence.examined_triples == 6
print("effective policy exhaustive count",evidence.examined_triples)
seen = []
sink = fixture.Sink()
def fail_if_called(*args, **kwargs):
    seen.append(1)
    raise AssertionError("FCI fit called")
with patch.object(FciBackend,"fit",fail_if_called):
    for label, invalid in [
        ("n=|S|+3",[(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]),
        ("rank deficient",[(x,x,z) for x,z in itertools.product((-1.,1.),repeat=2)]*8),
        ("near singular",[(x,x+1e-7*noise,z) for x,noise,z in itertools.product((-1.,1.),repeat=3)]*8),
    ]:
        try:
            LocalDiscoveryDispatcher(registry).discover(fixture._request("fisherz",invalid,registry),sink=sink)
        except ContractViolation as error:
            print("no fit",label,error.reason.code,error.reason.phase)
        else:
            raise AssertionError(label)
assert not seen and not sink.writes

import hashlib
import json
import sys
import tempfile
import pyarrow as pa
import pyarrow.parquet as pq
from ariadne.interfaces.cli.local_causal import command
with tempfile.TemporaryDirectory(dir=sys.argv[1],prefix="e11-ci-nonfinite-") as d:
    cli_spec = importlib.util.spec_from_file_location("clifixture",Path("tests/enhancement/enh_e11/g01/integration/test_local_cli.py"))
    cli = importlib.util.module_from_spec(cli_spec)
    cli_spec.loader.exec_module(cli)
    root = Path(d)
    study = cli._inputs(root)
    wire = json.loads(study.read_bytes())
    dataset = root/"inputs/data.parquet"
    bad = [(float("nan"),*row[1:]) if i == 0 else row for i,row in enumerate(rows)]
    pq.write_table(pa.table(dict(zip(cli.NAMES,zip(*bad)))),dataset)
    wire["inputs"]["dataset"]["sha256"] = hashlib.sha256(dataset.read_bytes()).hexdigest()
    study.write_text(json.dumps(wire))
    with patch.object(FciBackend,"fit",fail_if_called):
        assert command.main(["--config",str(study),"--output-root",str(root),"--json"]) == 2
    assert not seen and not (root/".staging").exists()
    print("Parquet NaN: fit count 0, staging absent")

```

初回補助プローブで発生した入力・観測ハーネスのエラーを修正し、同じ候補で再実行した。BK 規定は [011](ENH-E11-G01_01__011_bk_latent_negatives.md)、PrivacyDecision の型付き結果は [012](ENH-E11-G01_01__012_cli_error_privacy.md)、Parquet の NaN と no-fit の確認は [009](ENH-E11-G01_01__009_fci_api_eligibility.md) に記録した。
