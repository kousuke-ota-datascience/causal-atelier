# G01 Trial 01 — Owner 271 追補実測証跡

- 実行対象 `72bcd6acaab6caf48827bf2bb6cd5e249afd658b`
- 受入契約 `211f8b75245b849c2a4b2c057d656ef191df4d28`
- 前回独立証跡 `f7d881597a7543b21df4751f466572b38c1cda34`
- 2026-11-25 JST、Python 3.12.16、causal-learn 0.1.4.8、Linux ext4、EUID 1000
- 判定と再利用条件は [001](ENH-E11-G01_01__001_candidate_identity.md) および [999](ENH-E11-G01_01__999_gate_decision.md) を参照。

## 実行コマンド

```sh
cd /mnt/wsl/workspace/repositories/causal-atelier/_tmp_work/ENH-E11-G01-Trial01-independent-candidate
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src E11_PROBE_ROOT=/mnt/wsl/workspace/repositories/causal-atelier/_tmp_work /mnt/wsl/workspace/repositories/causal-atelier/.venv/bin/python -u /tmp/e11-g01-271-mechanical.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src MPLCONFIGDIR=/tmp/e11-g01-271-matplotlib /mnt/wsl/workspace/repositories/causal-atelier/.venv/bin/python -u /tmp/e11-g01-271-science.py
```

上の2コマンドは最終実行で exit 0。機械プローブは実 product entry point と実 ext4 を使用し、指定した障害箇所だけを一時制御した。科学プローブの T2 は worker の fit を直接実行し、サブプロセス起動時間は計測範囲外。独立導出で得た参照を使い、正式 T3 としての実行・判定は未実施。以下は各最終実行の出力。準備中に fixture の import と計数器のスコープに起因するプローブエラーがあり、固定候補を保ったままプローブを修正して同一コマンドで再実行した。

## 機械プローブの出力

```text
006 VALIDATING valid abort closed FD and quarantined bytes; ABORTED rejected repeat
006 PUBLISHING/COMMITTED denied; wrong/null token preserves both stages, FDs, and existing final
006 PREPARING facade abort denied
006 INDETERMINATE facade abort denied
007/008 negative-envelope valid before controlled change; Reader refuses after SCHEMA_INVALID
007/008 duplicate-inventory valid before controlled change; Reader refuses after SCHEMA_INVALID
007/008 unsafe-relative-key valid before controlled change; Reader refuses after SCHEMA_INVALID
007/008 status-mismatch valid before controlled change; Reader refuses after SCHEMA_INVALID
007/008 symlink-status valid before controlled change; Reader refuses after NOT_COMMITTED
007/008 extra-row valid before controlled change; Reader refuses after PRIVATE_ARTIFACT_DENIED
007 AMD-001 malformed descriptor SCHEMA_INVALID
007 AMD-001 fabricated SHA HASH_INVALID
007 AMD-001 graph bare key SCHEMA_INVALID
007 AMD-001 graph MIME SCHEMA_INVALID
007 AMD-001 missing runtime SCHEMA_INVALID
007 AMD-001 invalid runtime facts SCHEMA_INVALID
007 AMD-001 status wrong run SCHEMA_INVALID
007 AMD-001 technical error as SCI SCHEMA_INVALID
009 inverse-linalg typed rejection; fit=0; writes=0
009 inverse-nonfinite typed rejection; fit=0; writes=0
009 partial-exact-one typed rejection; fit=0; writes=0
009 partial-over-one typed rejection; fit=0; writes=0
009 partial-nonfinite typed rejection; fit=0; writes=0
{"run_id": "test-local", "technical_status": "COMPLETED", "science_acceptance": "NOT_EVALUATED", "manifest_relative_path": "runs/test-local/manifest.json"}
013 same Policy.check at Application and selected Adapter [('accept', 'fisherz', 'ScientificEligibilityPolicy'), ('accept', 'fisherz', 'ScientificEligibilityPolicy')] registry count 1
008/012 stage exit 5 PUBLICATION_FAILED app abort 1 cleanup diagnostic False
008/012 graph-key exit 4 BACKEND_GRAPH_INVALID app abort 1 cleanup diagnostic False
008/012 graph-sha exit 4 BACKEND_GRAPH_INVALID app abort 1 cleanup diagnostic False
008/012 graph-mime exit 4 BACKEND_GRAPH_INVALID app abort 1 cleanup diagnostic False
008/012 status exit 5 SCHEMA_INVALID app abort 1 cleanup diagnostic True
008/012 privacy exit 3 PRIVACY_POLICY_CONFLICT app abort 1 cleanup diagnostic True
008/012 publish-before exit 5 PUBLICATION_FAILED app abort 0 cleanup diagnostic False
008/012 publish-after exit 5 PUBLICATION_INDETERMINATE app abort 0 cleanup diagnostic False
009 n=|S|+4 n=5 conditional PASS; invertible near-singular cond*eps 0.00044412767916224803
011/013 empty BK exit 4, fit=0, stage=0, JSON lines=1
011/013 contradictory BK exit 4, fit=0, stage=0, JSON lines=1
007 unsafe ContentRef '/absolute' SCHEMA_INVALID
007 unsafe ContentRef 'dir//file' SCHEMA_INVALID
007 unsafe ContentRef 'dir\\file' SCHEMA_INVALID
007 unsafe ContentRef 'bad\x00file' SCHEMA_INVALID
012 stale root inode replaced; seal denied PRIVACY_POLICY_CONFLICT Marker=0
013 immutable registry maps; P1-M06 sole entry; shared ScientificEligibilityPolicy source inspected
```

## 探索的 T2、参照導出、BK hazard の出力

```text
010 provisional analytic reference endpoint pairs {('X', 'M'): ('CIRCLE', 'ARROW'), ('M', 'Z'): ('ARROW', 'CIRCLE')} MAG class leaf marks [('TAIL', 'TAIL'), ('TAIL', 'ARROW'), ('ARROW', 'TAIL'), ('ARROW', 'ARROW')]
010 observed-collider population covariance [[1, 2, 0], [2, 14, 3], [0, 3, 1]] conditional X,Z given M -0.42857142857142855
010 exploratory T2 observed-collider replicates 100 n 512 seeds range(73000, 73100) fit seconds total 0.26 max 0.006 fixture sha256 9abdab6c030d429b8f6f828b44c07ed080c16a754b057b0b7f9eb79e815c7aae counts {'true_positive_edges': 200, 'false_positive_edges': 7, 'false_negative_edges': 0, 'exact_skeleton': 93, 'exact_pag': 93, 'empty_predictions': 0, 'CIRCLE_matches': 200, 'ARROW_matches': 186}
010 latent-collider population covariance [[5, 6, 0], [6, 19, 3], [0, 3, 1]] conditional X,Z given M -0.9473684210526315
010 exploratory T2 latent-collider replicates 100 n 512 seeds range(73000, 73100) fit seconds total 0.256 max 0.005 fixture sha256 966a9cc36a2ffd00937e37e76c33bc70ef6c86397acebb6ea0120675dfe0f084 counts {'true_positive_edges': 200, 'false_positive_edges': 6, 'false_negative_edges': 0, 'exact_skeleton': 94, 'exact_pag': 94, 'empty_predictions': 0, 'CIRCLE_matches': 200, 'ARROW_matches': 188}
011 latent/direct identical covariance [[2.0, 1.0], [1.0, 2.0]]
011 independently allowed ancestral complete graphs 13 Z endpoint options TAIL/ARROW backend produces {'Z': 'TAIL', 'Y': 'ARROW'} extra stdout lines 3 FCI.py sha256 8f0f14f9d31847efa30fa056a162f1f9d21d07595880c1ad2b099ec11e544ead
```

## 機械プローブソース

`/tmp/e11-g01-271-mechanical.py` SHA-256 `a665a9c94cdf60d18cf41d65195ab63c80622bf8d48475f98ad0ae311eea2241`。

```python
import copy
import errno
import hashlib
import importlib.util
import io
import itertools
import json
import os
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import numpy as np

from ariadne.capabilities.causal.ports.local_io import PublicationSessionToken
from ariadne.capabilities.causal.ports.manifest_factory import ManifestBuildEvidence, ManifestRuntimeFacts
from ariadne.causal.design.study import thaw_json
from ariadne.interfaces.cli.local_causal import command, publication
from ariadne.interfaces.cli.local_causal.config_decoder import StrictLocalConfigDecoder
from ariadne.interfaces.cli.local_causal.manifest_factory import LocalManifestFactoryAdapter
from ariadne.interfaces.cli.local_causal.manifest_reader import LocalManifestReader
from ariadne.shared.content_ref import ContentRef, ContractViolation
from ariadne.shared.local_fs import TrustedLocalRoot
from ariadne.shared.serialization import jcs

def fixture(name):
    location = Path("tests/enhancement/enh_e11/g01/integration") / f"test_{name}.py"
    spec = importlib.util.spec_from_file_location(name, location)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

p = fixture("local_publication")
cli = fixture("local_cli")
fci = fixture("fci_discovery")
outside = Path(os.environ["E11_PROBE_ROOT"])

def tmp():
    return TemporaryDirectory(dir=outside, prefix="e11-271-")

def denied(call, code=None):
    try:
        call()
    except ContractViolation as error:
        if code is not None:
            assert error.reason.code == code, error.reason
        return error.reason.code
    raise AssertionError("expected typed refusal")

def snapshot(root):
    return {path.relative_to(root).as_posix():path.read_bytes() for path in root.rglob("*") if path.is_file()}

def prep(root, path, **kwargs):
    token = PublicationSessionToken()
    begin = p.LocalPublicationAdapter.begin
    def bound(self, **args):
        return begin(self, **args, session=token)
    with patch.object(p.LocalPublicationAdapter, "begin", bound):
        facade, sink, man, decision = p._prepare(root, path, **kwargs)
    expected = dict(root=root, run_id=decision.run_id, request_hash=decision.request_hash, session=token, reason="probe")
    return facade, sink, man, decision, expected

def assert_closed(fd):
    try:
        os.fstat(fd)
    except OSError as error:
        assert error.errno == errno.EBADF
    else:
        raise AssertionError("FD still open")

with tmp() as directory:
    path = Path(directory)
    with TrustedLocalRoot.open(path, allowed_directory=path) as root:
        facade, sink, man, decision, expected = prep(root, path)
        concrete = sink._publisher
        facade.seal(sink=sink, manifest=man, privacy=decision)
        assert concrete.state.name == "VALIDATING"
        fd = concrete.staging_handle.directory
        before = snapshot(path)
        facade.abort(sink=sink, **expected)
        assert concrete.state.name == "ABORTED"
        assert_closed(fd)
        assert snapshot(path) == before and not (path/"runs").exists()
        denied(lambda: facade.abort(sink=sink, **expected), "PUBLICATION_FAILED")
        print("006 VALIDATING valid abort closed FD and quarantined bytes; ABORTED rejected repeat")
        facade, sink, man, decision, expected = prep(root, path)
        bundle = facade.seal(sink=sink, manifest=man, privacy=decision)
        rename = publication._rename_noreplace
        def during_rename(*args):
            assert sink._publisher.state.name == "PUBLISHING"
            denied(lambda: facade.abort(sink=sink, **expected), "PUBLICATION_FAILED")
            return rename(*args)
        with patch.object(publication, "_rename_noreplace", during_rename):
            facade.publish(bundle=bundle, root=root)
        assert sink._publisher.state.name == "COMMITTED"
        before = snapshot(path/"runs")
        denied(lambda: facade.abort(sink=sink, **expected), "PUBLICATION_FAILED")
        record = p._study(path)
        token_a, token_b = PublicationSessionToken(), PublicationSessionToken()
        first = facade.begin(root=root, run_id=decision.run_id,request_hash=decision.request_hash,session=token_a)
        second = facade.begin(root=root, run_id=decision.run_id,request_hash=decision.request_hash,session=token_b)
        for active in (first, second):
            active.stage_bytes("study.json", jcs.canonical_bytes(record), "application/json", "AGGREGATE")
        protected = snapshot(path)
        held = dict(expected,session=token_a)
        denied(lambda: facade.abort(sink=second, **held), "PUBLICATION_FAILED")
        denied(lambda: facade.abort(sink=first, **dict(held,session=None)), "PUBLICATION_FAILED")
        assert snapshot(path)==protected and snapshot(path/"runs")==before
        for active, token in ((first,token_a),(second,token_b)):
            os.fstat(active._publisher.staging_handle.directory)
            assert active._publisher.state.name == "STAGING"
            facade.abort(sink=active, **dict(held,session=token))
        print("006 PUBLISHING/COMMITTED denied; wrong/null token preserves both stages, FDs, and existing final")

for scenario in ("PREPARING","INDETERMINATE"):
    with tmp() as directory:
        path=Path(directory)
        with TrustedLocalRoot.open(path,allowed_directory=path) as root:
            if scenario=="PREPARING":
                facade=p.LocalPublicationAdapter(p.Policy())
                expected=dict(root=root,run_id=p.RUN,request_hash="a"*64,session=PublicationSessionToken(),reason="probe")
                original=publication.LocalArtifactPublisher.begin
                def while_preparing(self):
                    assert self.state.name=="PREPARING"
                    denied(lambda: facade.abort(sink=self._sink,**expected),"PUBLICATION_FAILED")
                    return original(self)
                with patch.object(publication.LocalArtifactPublisher,"begin",while_preparing):
                    sink=facade.begin(**{k:v for k,v in expected.items() if k!="reason"})
                facade.abort(sink=sink,**expected)
            else:
                facade,sink,man,decision,expected=prep(root,path)
                bundle=facade.seal(sink=sink,manifest=man,privacy=decision)
                fsync=os.fsync
                def fail(fd):
                    if (path/"runs"/p.RUN).exists():
                        raise OSError(errno.EIO,"injected")
                    fsync(fd)
                with patch.object(publication.os,"fsync",fail):
                    denied(lambda: facade.publish(bundle=bundle,root=root),"PUBLICATION_INDETERMINATE")
                assert sink._publisher.state.name=="INDETERMINATE"
                before=snapshot(path)
                denied(lambda: facade.abort(sink=sink,**expected),"PUBLICATION_FAILED")
                assert snapshot(path)==before
            print("006",scenario,"facade abort denied")

def sha(data):
    return hashlib.sha256(data).hexdigest()

for case in ("negative-envelope","duplicate-inventory","unsafe-relative-key","status-mismatch","symlink-status","extra-row"):
    with tmp() as directory:
        path=Path(directory)
        with TrustedLocalRoot.open(path,allowed_directory=path) as root:
            facade,sink,man,decision,expected=prep(root,path,negative=case=="negative-envelope")
            bundle=facade.seal(sink=sink,manifest=man,privacy=decision)
            facade.publish(bundle=bundle,root=root)
            reader=LocalManifestReader()
            assert reader.read_run(root,p.RUN).request_hash==decision.request_hash
            run=path/"runs"/p.RUN
            manifest=json.loads((run/"manifest.json").read_bytes())
            marker=json.loads((run/"_COMMITTED.json").read_bytes())
            if case=="negative-envelope":
                assert manifest["schema_dispatch"]["graph"] is manifest["schema_dispatch"]["result"] is None
                assert manifest["lineage"]["graph"] is None
                diag=json.loads((run/"diagnostics.json").read_bytes())
                assert diag=={"run_id":p.RUN,"operation":"DISCOVER","method_id":"P1-M06","reason_codes":["SCI_NO_ADMISSIBLE_PAG"]}
                assert json.loads((run/"status.json").read_bytes())["reason_codes"]==diag["reason_codes"]
                assert {entry["key"] for entry in manifest["artifacts"]}=={"diagnostics.json","status.json","study.json"}
                name="diagnostics.json"
                raw=jcs.canonical_bytes(dict(diag,reason_codes=["BACKEND_API_MISMATCH"]))
            if case=="duplicate-inventory":
                manifest["artifacts"].append(manifest["artifacts"][0])
            if case=="unsafe-relative-key":
                manifest["lineage"]["design"]["relative_key"]="../outside"
            if case=="status-mismatch":
                manifest["execution"]["technical_status"]="FAILED"
            if case=="symlink-status":
                source=run/"status.json"
                source.rename(path/"actual-status.json")
                source.symlink_to(path/"actual-status.json")
            if case=="extra-row":
                p._put(run/"private-row.json",b"{}")
            if case=="negative-envelope":
                (run/name).write_bytes(raw)
                item=next(d for d in manifest["artifacts"] if d["key"]==name)
                item.update(sha256=sha(raw),size_bytes=len(raw))
            raw=jcs.canonical_bytes(manifest)
            (run/"manifest.json").write_bytes(raw)
            (run/"_COMMITTED.json").write_bytes(jcs.canonical_bytes(dict(marker,manifest_sha256=sha(raw))))
            print("007/008",case,"valid before controlled change; Reader refuses after",denied(lambda:reader.read_run(root,p.RUN)))

with tmp() as directory:
    path=Path(directory)
    with TrustedLocalRoot.open(path,allowed_directory=path) as root:
        facade,sink,man,decision,expected=prep(root,path)
        wire=json.loads(man.to_canonical_bytes())
        status=json.loads(snapshot(path)[next(k for k in snapshot(path) if k.endswith("/status.json"))])
        study=p.StrictLocalConfigDecoder().decode(jcs.canonical_bytes(p._study(path)),declared_format="json")
        runtime=ManifestRuntimeFacts("fixture",False,"3.12","Linux","a"*64,{}, {})
        descriptors=tuple(fci.ArtifactDescriptor(**item) for item in wire["artifacts"])
        graph=ContentRef.from_payload(wire["lineage"]["graph"])
        data=dict(study=study,study_payload=study.to_payload(),status_payload=status,runtime=runtime,stochastic={},
                  artifact_descriptors=descriptors,output_graph_ref=graph,graph_negative_reason_codes=(),
                  review_science_evidence_ref=None)
        factory=LocalManifestFactoryAdapter()
        evidence=ManifestBuildEvidence(**data)
        status["run_id"]="changed-after-snapshot"
        assert factory.build(evidence=evidence).to_canonical_bytes()==man.to_canonical_bytes()
        data["status_payload"]=thaw_json(evidence.status_payload)
        i=next(i for i,d in enumerate(descriptors) if d.key=="graph.json")
        bad_descriptor=list(descriptors)
        bad_descriptor[i]=replace(descriptors[i],sha256="2"*64)
        negatives={
            "malformed descriptor":dict(artifact_descriptors=(object(),)),
            "fabricated SHA":dict(artifact_descriptors=tuple(bad_descriptor)),
            "graph bare key":dict(output_graph_ref=replace(graph,relative_key="graph.json")),
            "graph MIME":dict(output_graph_ref=replace(graph,media_type="text/plain")),
            "missing runtime":dict(runtime=None),
            "invalid runtime facts":dict(runtime=replace(runtime, python_version="")),
            "status wrong run":dict(status_payload=dict(data["status_payload"],run_id="other")),
            "technical error as SCI":dict(graph_negative_reason_codes=("BACKEND_API_MISMATCH",)),
        }
        for name, change in negatives.items():
            print("007 AMD-001",name,denied(lambda:factory.build(evidence=ManifestBuildEvidence(**(data|change)))))
        assert not list(path.glob(".staging/*/_COMMITTED.json")) and not (path/"runs").exists()
        facade.abort(sink=sink,**expected)

registry=fci._registry(fci.TEST_OBSERVATION,fci.FciBackend)
dispatcher=fci.LocalDiscoveryDispatcher(registry)
rows=list(itertools.product((-1.,1.),repeat=3))*5
calls=[]
def no_fit(*args,**kwargs):
    calls.append(1)
    raise AssertionError("unexpected FCI fit")
def inv_failure(*args):
    raise np.linalg.LinAlgError("injected inverse failure")
for label in ("inverse-linalg","inverse-nonfinite","partial-exact-one","partial-over-one","partial-nonfinite"):
    request=fci._request("fisherz",rows,registry)
    if label=="inverse-linalg":
        inverse=patch.object(np.linalg,"inv",side_effect=inv_failure)
    else:
        value=np.array([[1.,1.2],[1.2,1.]])
        if label=="inverse-nonfinite":
            value[0,1]=np.nan
        elif label=="partial-exact-one":
            value[0,1]=1.0
        elif label=="partial-nonfinite":
            value[0,0]=1e-308
            value[1,1]=1e308
            value[0,1]=np.finfo(np.float64).max
        inverse=patch.object(np.linalg,"inv",return_value=value)
    controls=[inverse,patch.object(fci.FciBackend,"fit",no_fit)]
    # Residual is bypassed in isolated partial-correlation controls only.
    if label.startswith("partial"):
        controls.extend([patch.object(np.linalg,"norm",return_value=0.)])
    from contextlib import ExitStack
    with ExitStack() as stack:
        for control in controls:
            stack.enter_context(control)
        sink=fci.Sink()
        assert denied(lambda:dispatcher.discover(request,sink=sink))=="ELIGIBILITY_UNRESOLVED"
        assert not calls and not sink.writes
    print("009",label,"typed rejection; fit=0; writes=0")

# Confirm the same implementation authorizes the application preflight and registry-selected adapter.
composition=command._compose()
registry=composition.capabilities.registry
checker=fci.ScientificEligibilityPolicy.check
observations=[]
def traced(self,request):
    try:
        result=checker(self,request)
        observations.append(("accept",request.capability.profile,type(self).__qualname__))
        return result
    except ContractViolation as error:
        observations.append(("reject",error.reason.code,type(self).__qualname__))
        raise
with tmp() as directory:
    path=Path(directory)
    config=cli._inputs(path)
    with patch.object(fci.ScientificEligibilityPolicy,"check",traced), patch.object(command,"_compose",return_value=composition):
        assert command.main(["--config",str(config),"--output-root",str(path),"--json"])==0
    assert len(observations)==2 and all(obs==("accept","fisherz","ScientificEligibilityPolicy") for obs in observations)
print("013 same Policy.check at Application and selected Adapter",observations, "registry count",len(registry.backend_factories))

# Supplement the existing typed abort matrix with actual staged data and publish transitions.
for fault in ("stage","graph-key","graph-sha","graph-mime","status","privacy","publish-before","publish-after"):
    with tmp() as directory:
        path=Path(directory)
        config=cli._inputs(path)
        live=command._compose()
        calls=[]
        composed=live.publisher
        abort=composed.abort
        start=composed.begin
        def trace_start(**kw):
            sink=start(**kw)
            calls.append(("begin",sink,kw))
            return sink
        def trace_abort(**kw):
            event,expected_sink,expected_values=calls[0]
            assert event=="begin" and kw["sink"] is expected_sink
            assert all(kw[k] is value if k in ("root","session") else kw[k]==value for k,value in expected_values.items())
            calls.append(("abort",))
            return abort(**kw)
        stage=publication._Sink.stage_bytes
        def stage_test(self,key,data,media_type,classification):
            if fault=="stage" and key=="study.json":
                raise ContractViolation("PUBLICATION_FAILED","publication","synthetic fixture")
            if fault=="status" and key=="status.json":
                data=jcs.canonical_bytes(dict(json.loads(data),run_id="wrong"))
            descriptor=stage(self,key,data,media_type,classification)
            if key=="graph.json":
                if fault=="graph-key":
                    return replace(descriptor,key="unrelated.json")
                if fault=="graph-sha":
                    return replace(descriptor,sha256="a"*64)
                if fault=="graph-mime":
                    return replace(descriptor,media_type="text/plain")
            return descriptor
        rename=publication._rename_noreplace
        def rename_test(*args):
            raise OSError(errno.EXDEV,"injected control")
        fsync=os.fsync
        def fsync_test(fd):
            if (path/"runs"/cli.RUN).exists():
                raise OSError(errno.EIO,"injected control")
            fsync(fd)
        expected_code={"stage":5,"graph-key":4,"graph-sha":4,"graph-mime":4,"status":5,
                       "privacy":3,"publish-before":5,"publish-after":5}[fault]
        with ExitStack() as stack:
            for control in (patch.object(command,"_compose",return_value=live),
                            patch.object(composed,"begin",side_effect=trace_start),
                            patch.object(composed,"abort",side_effect=trace_abort),
                            patch.object(publication._Sink,"stage_bytes",stage_test)):
                stack.enter_context(control)
            if fault=="publish-before":
                stack.enter_context(patch.object(publication,"_rename_noreplace",rename_test))
            if fault=="publish-after":
                stack.enter_context(patch.object(publication.os,"fsync",fsync_test))
            if fault=="privacy":
                controller=live.privacy
                authorize=controller.authorize
                seen=[]
                def second_denies(**kw):
                    decision=authorize(**kw)
                    seen.append(1)
                    return decision if len(seen)==1 else replace(decision,allowed=False)
                stack.enter_context(patch.object(type(controller),"authorize",side_effect=second_denies))
            output,errors=io.StringIO(),io.StringIO()
            with redirect_stdout(output),redirect_stderr(errors):
                actual=command.main(["--config",str(config),"--output-root",str(path),"--json"])
        result=json.loads(output.getvalue())
        assert actual==expected_code and result["technical_status"]=="FAILED", (fault,actual,result)
        assert result["science_acceptance"]=="NOT_EVALUATED" and "SCI_NO_ADMISSIBLE_PAG" not in output.getvalue()+errors.getvalue()
        assert str(path) not in output.getvalue()+errors.getvalue()
        if fault=="publish-after":
            assert result["reason_code"]=="PUBLICATION_INDETERMINATE"
            assert (path/"runs"/cli.RUN/"_COMMITTED.json").exists()
        else:
            assert not (path/"runs"/cli.RUN).exists()
        if not fault.startswith("publish"):
            assert not list(path.glob(".staging/*/_COMMITTED.json"))
        count=sum(event[0]=="abort" for event in calls)
        assert count==(0 if fault.startswith("publish") else 1)
        print("008/012",fault,"exit",actual,result["reason_code"],"app abort",count,"cleanup diagnostic","PUBLICATION_ABORT_FAILED" in errors.getvalue())


n5=[(1.,1.,1.),(-1.,1.,1.),(0.,-2.,1.),(0.,0.,-3.),(0.,0.,0.)]
minimum=fci._request("fisherz",n5,fci._registry(fci.TEST_OBSERVATION,fci.FciBackend))
assert fci.ScientificEligibilityPolicy(lambda:True).check(minimum)[1].examined_triples==6
near=np.array([[1.,1.-1e-12],[1.-1e-12,1.]])
assert np.isfinite(np.linalg.inv(near)).all()
assert np.linalg.cond(near)*np.finfo(np.float64).eps>1e-6
print("009 n=|S|+4 n=5 conditional PASS; invertible near-singular cond*eps",np.linalg.cond(near)*np.finfo(np.float64).eps)

calls = []
for pairs in ([],[[cli.NAMES[0],cli.NAMES[1]]]):
    with tmp() as directory:
        path=Path(directory)
        config=cli._inputs(path)
        wire=json.loads(config.read_bytes())
        design=path/"inputs/d.json"
        bk={"required_edges":pairs,"forbidden_edges":pairs}
        design.write_bytes(jcs.canonical_bytes(dict(json.loads(design.read_bytes()),background_knowledge=bk)))
        wire["inputs"]["design"]["sha256"]=sha(design.read_bytes())
        wire["method"]["config"]["background_knowledge"]=bk
        config.write_bytes(jcs.canonical_bytes(wire))
        output, errors=io.StringIO(),io.StringIO()
        with patch.object(command,"_compose",return_value=composition), patch.object(fci.FciBackend,"fit",no_fit), \
             patch.object(fci.ScientificEligibilityPolicy,"check",traced),redirect_stdout(output),redirect_stderr(errors):
            assert command.main(["--config",str(config),"--output-root",str(path),"--json"])==4
        envelope=json.loads(output.getvalue())
        assert envelope["reason_code"]=="BACKEND_SEMANTICS_UNVERIFIED"
        assert len(output.getvalue().splitlines())==1 and all(k not in output.getvalue()+errors.getvalue() for k in cli.NAMES)
        assert not calls and not (path/".staging").exists() and not (path/"runs").exists()
        assert observations[-1]==("reject","BACKEND_SEMANTICS_UNVERIFIED","ScientificEligibilityPolicy")
        print("011/013","empty BK" if not pairs else "contradictory BK","exit 4, fit=0, stage=0, JSON lines=1")


for key in ("/absolute","dir//file",r"dir\file","bad\x00file"):
    with tmp() as directory:
        path=Path(directory)
        with TrustedLocalRoot.open(path,allowed_directory=path) as root:
            facade,sink,man,decision,expected=prep(root,path)
            facade.publish(bundle=facade.seal(sink=sink,manifest=man,privacy=decision),root=root)
            run=path/"runs"/p.RUN
            marker=json.loads((run/"_COMMITTED.json").read_bytes())
            wire=json.loads((run/"manifest.json").read_bytes())
            wire["lineage"]["question"]["relative_key"]=key
            raw=jcs.canonical_bytes(wire)
            (run/"manifest.json").write_bytes(raw)
            (run/"_COMMITTED.json").write_bytes(jcs.canonical_bytes(dict(marker,manifest_sha256=sha(raw))))
            print("007 unsafe ContentRef",repr(key),denied(lambda:LocalManifestReader().read_run(root,p.RUN)))

with tmp() as directory:
    parent=Path(directory)
    path=parent/"root"
    path.mkdir(mode=0o700)
    with TrustedLocalRoot.open(path,allowed_directory=parent) as root:
        facade,sink,man,decision,expected=prep(root,path)
        old=parent/"moved"
        path.rename(old)
        path.mkdir(mode=0o700)
        code=denied(lambda:facade.seal(sink=sink,manifest=man,privacy=decision))
        assert not list(parent.rglob("_COMMITTED.json")) and not list(parent.rglob("runs"))
        print("012 stale root inode replaced; seal denied",code,"Marker=0")
from types import MappingProxyType
assert isinstance(registry.backend_factories,MappingProxyType) and isinstance(registry.descriptors,MappingProxyType)
assert tuple(registry.backend_factories)==("P1-M06",) and tuple(registry.descriptors)==("P1-M06",)
print("013 immutable registry maps; P1-M06 sole entry; shared ScientificEligibilityPolicy source inspected")
```

## 科学プローブソース

`/tmp/e11-g01-271-science.py` SHA-256 `dbdbb2da800f8cd0096c035d0ff3579e66a83a258161909d2c616860ab9d8da4`。

```python
import contextlib
import hashlib
import importlib.util
import inspect
import io
import itertools
import json
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np
from causallearn.graph.Edge import Edge
from causallearn.graph.Endpoint import Endpoint
from causallearn.graph.GeneralGraph import GeneralGraph
from causallearn.graph.GraphNode import GraphNode
from causallearn.search.ConstraintBased.FCI import fci_orient_bk
from causallearn.utils.PCUtils.BackgroundKnowledge import BackgroundKnowledge
from ariadne.scientific.causal_methods import _fci_worker

PROFILE={"indep_test":"fisherz","alpha":0.05,"depth":-1,"max_path_length":-1,"background_knowledge":None}
NAMES=["X","M","Z"]
N=512
PILOT_SEEDS=range(73000,73100)
# X-M-Z has one unshielded path, with a collider at M. All four
# combinations below are ancestral, maximal (marginal separator empty),
# and have identical separation of X and Z conditional on either () or (M,).
CLASS=list(itertools.product(("TAIL","ARROW"),repeat=2))
EXPECTED={("X","M"):("CIRCLE","ARROW"),("M","Z"):("ARROW","CIRCLE")}
print("010 provisional analytic reference endpoint pairs",EXPECTED,"MAG class leaf marks",CLASS)
for name,coeff in {
    "observed-collider":np.array([[1,0,0,0],[2,3,1,0],[0,1,0,0]]),
    "latent-collider":np.array([[2,0,1,0],[3,3,0,1],[0,1,0,0]]),
}.items():
    # columns are independent N(0,1). Latent: L->X and L->M; Z->M.
    # Latent projection is X<->M<-Z. Observed DAG is X->M<-Z.
    kov=coeff@coeff.T
    cross=kov[0,2]-kov[0,1]*kov[1,2]/kov[1,1]
    assert np.linalg.eigvalsh(kov)[0]>0 and kov[0,2]==0 and cross!=0
    assert kov[0,1]!=0 and kov[1,2]!=0
    for i,j,k in [(0,1,2),(1,2,0)]:
        assert kov[i,j]-kov[i,k]*kov[j,k]/kov[k,k]!=0
    print("010",name,"population covariance",kov.tolist(),"conditional X,Z given M",float(cross))
    with contextlib.redirect_stdout(io.StringIO()):
        abi=_fci_worker._run({"action":"probe"})
    counts=Counter()
    seconds=[]
    digest=hashlib.sha256()
    for seed in PILOT_SEEDS:
        rows=np.random.default_rng(seed).standard_normal((N,4)) @ coeff.T
        digest.update(np.ascontiguousarray(rows,dtype="<f8").tobytes())
        start=time.perf_counter()
        with contextlib.redirect_stdout(io.StringIO()):
            result=_fci_worker._run({"action":"fit","rows":rows.tolist(),"config":PROFILE,
                                     "columns":NAMES,"version":abi["version"],"api_signature_hash":abi["api_signature_hash"],
                                     "seed":seed})
        seconds.append(time.perf_counter()-start)
        if "error" in result:
            counts["backend_errors"]+=1
            continue
        assert result["nodes"]==NAMES
        observed={}
        for edge in result["edges"]:
            key=(edge["source"],edge["target"])
            marks=(edge["source_mark"],edge["target_mark"])
            if key not in EXPECTED:
                key=key[::-1]
                marks=marks[::-1]
            observed[key]=marks
        tp=len(EXPECTED.keys() & observed.keys())
        counts.update({"true_positive_edges":tp,"false_positive_edges":len(observed)-tp,"false_negative_edges":2-tp,
                       "exact_skeleton":observed.keys()==EXPECTED.keys(),"exact_pag":observed==EXPECTED,
                       "empty_predictions":not observed})
        for key,marks in EXPECTED.items():
            for index,mark in enumerate(marks):
                counts[f"{mark}_matches"]+=key in observed and observed[key][index]==mark
    print("010 exploratory T2",name,"replicates",len(PILOT_SEEDS),"n",N,"seeds",PILOT_SEEDS,
          "fit seconds total",round(sum(seconds),3),"max",round(max(seconds),3),
          "fixture sha256",digest.hexdigest(),"counts",dict(counts))

# Two-variable Gaussian non-identification. Matching SPD covariance determines the same law.
latent=np.array([[1.,1.,0.],[1.,0.,1.]])
direct=np.array([[np.sqrt(2),0.],[1/np.sqrt(2),np.sqrt(1.5)]])
assert np.allclose(latent@latent.T,direct@direct.T,rtol=0,atol=1e-15)
print("011 latent/direct identical covariance",(latent@latent.T).tolist())

# Complete skeleton admits no observed separation. Both ancestral MAGs satisfy a ban on Y->Z:
# Z->Q->Y with Z->Y, or Q->Z,Q->Y and Z<->Y. Therefore the Z endpoint is not forced to TAIL.
def ancestral_complete(options):
    directed={(a,b) for a,b in options if (b,a) not in options}
    edges=set(directed)
    while True:
        closure=edges|{(a,c) for a,b in edges for d,c in edges if b==d}
        if closure==edges:
            break
        edges=closure
    if any(a==b for a,b in edges):
        return False
    return all((a,b) not in edges for a,b in options if (b,a) in options)
pairs=[("Z","Y"),("Z","Q"),("Q","Y")]
allowed=[]
for values in itertools.product((0,1,2),repeat=3):
    if values[0]==1:
        continue
    arrows=set()
    for (a,b),v in zip(pairs,values):
        if v!=1: arrows.add((a,b))
        if v!=0: arrows.add((b,a))
    if ancestral_complete(arrows):
        allowed.append(values)
assert {v[0] for v in allowed}=={0,2}
z,y=GraphNode("Z"),GraphNode("Y")
graph=GeneralGraph([z,y])
graph.add_edge(Edge(z,y,Endpoint.CIRCLE,Endpoint.ARROW))
bk=BackgroundKnowledge()
bk.add_forbidden_by_node(y,z)
capture=io.StringIO()
with contextlib.redirect_stdout(capture):
    fci_orient_bk(bk,graph)
edge=graph.get_edge(z,y)
marks={edge.get_node1().get_name():edge.get_endpoint1().name,edge.get_node2().get_name():edge.get_endpoint2().name}
assert marks=={"Z":"TAIL","Y":"ARROW"} and capture.getvalue().strip()
source=Path(inspect.getsourcefile(fci_orient_bk)).read_bytes()
print("011 independently allowed ancestral complete graphs",len(allowed),"Z endpoint options TAIL/ARROW",
      "backend produces",marks,"extra stdout lines",len(capture.getvalue().splitlines()),
      "FCI.py sha256",hashlib.sha256(source).hexdigest())

```
