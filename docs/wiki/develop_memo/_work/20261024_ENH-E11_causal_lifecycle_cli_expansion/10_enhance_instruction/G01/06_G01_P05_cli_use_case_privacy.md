# ENH-E11 G01 P05 — Local CLI, UseCase, Privacy, Legacy Regression

**DEC-G01-EXEC-01（Owner 2026-11-23採用・G01のみの実施順序変更）:** `combined_review/177_20261123_dec_g01_exec01_owner_adopted_evidence_rephasing.md`がG01の従前S09→S10→S11依存を部分的に上書きする。利用不能なPython3.12実測B02/B04、独立S09/B05科学審査は**Coding Entryの必要条件から外し、G01_999 PASSまでの必須受入条件へ移す**。事前Author契約整合と例外Ledgerを材料に、Ownerの**別個の暫定G01-S10 Freeze**、その後Ownerの**別個の限定G01-S11 Coding Authorization**を認める。どちらも現在**未承認**。限定許可はG01/P01–P05の実装・開発者テストのみ。実Python3.12 Schema/FCI、独立MAG/PAG/BK、実FS/Reader、T2/T3、独立07/999、Product v2回帰の要求・合格基準は維持。未検証をPASS扱いせず、non-null BKはFCI呼出前exit4 fail-closed、科学的真値や閾値の自己創作禁止。G01_999がPASSするまで下流Gate依存は解除しない。

**Document class:** Primary Execution Contract  
**Self-containment:** MUST — Assigned Coding Agentが本書だけでpackageのnormative execution responsibilityを理解できること。

- Gate: G01
- Trial: Trial01（未開始）
- Package: P05
- Parent 06 (traceability): 06_Ariadne_ENH-E11_G01_implementation_instruction.md
- P00 Plan (traceability): 06_G01_P00_work_package_plan.md
- Depends on: P02,P03,P04
- Status at issuance: DRAFT / CODING_NOT_AUTHORIZED

## 1. Purpose
DISCOVER-only CLIの全経路を統合し、Product v2を回帰保護する。

## 2. Effective Gate constraints applicable to this package

このpackageが守るべきGate-level semanticsを、Parent 06 / P00を読まなくても実行判断できる粒度で記載する。

G01は正式Gate IDでPxxはbounded Coding Unit。Local laneとProduct v2を分離し旧CLI/Web/API/DB/Workerは改変しない。strict version/Method/EstimatorとJCSのハッシュ対象を検証し、PAGをDAG/ATEへ変換しない。OS root/Privacy/Atomic Publishの不適格はfail-closed、SCI不確実性をPASSに変換しない。Coding Authorization前の実装は禁止。

## 3. In scope — implementation ownership

| Class / module | Owned by P05 | Boundary |
| --- | --- | --- |
| `ariadne.capabilities.causal.local_execution.LocalRunContext` | immutable trusted execution Context | TrustedRoot/Principal factory belongs to P02 composition |
| `ariadne.capabilities.causal.local_execution.LocalCausalUseCase` | Port injection; `preflight` / `run`; typed outcome; Operation-specific pipeline | No separate scientific estimator or FS publication algorithm |
| `ariadne.capabilities.causal.ports.local_privacy.LocalPrivacyPolicyPort` | typed authorization interface | Concrete is CLI layer, not Application import |
| `ariadne.interfaces.cli.local_causal.privacy.LocalPrivacyPolicy` | stateless privacy decisions, G01 aggregate-only | G05 local Study単独opt-in/row minimization is outside G01 |
| `ariadne.interfaces.cli.local_causal.command.main` | new explicit local CLI, error/JSON response | no changes to Product v2 entrypoints |
| Integration and Product regression | G01 complete DISCOVER vertical slice and legacy safeguards | Independent 07/999 decides Gate PASS |

P05 depends on P02, P03 and P04. P01 has already provided strict parser, Codec and Manifest DTO. Complete all actual cross-asset joins here; do not mistake the P01 pure decoder for a filesystem verifier.

## 4. Explicitly out of scope
他GateのMethod実装、旧Product v2変更、根拠なしのScience PASS、行出力自己許可、不適格なUID/owner/mode/local FS、既存run上書き、Package外の便乗変更。

## 5. Entry criteria / required evidence
Gate 06/07のFreeze・Coding Authorization・固定branch HEAD確認。Depends on P02,P03,P04の実装checkpoint full SHAとfocused検証を確認。矛盾/依存未成立はBLOCKED。

dependency checkpoint / source state等はfactとして外部参照してよい。Entry rule自体は本書内に記載する。

## 6. Required implementation — orchestration, Privacy and CLI

### 6.1. `LocalRunContext` and trusted CLI composition (30_62 §1.2/1.3)

**Module:** `ariadne.capabilities.causal.local_execution`. An immutable Context with fields:

| Field | Type | Construction/Trust |
| --- | --- | --- |
| `root` | `TrustedLocalRoot` | P02 verified root dirfd, owner/mode/local FS |
| `principal` | `LocalPrincipal` | actual effective OS actor, not Study claim |
| 
Only CLI composition root creates Context from verified capabilities. The User-supplied `--output-root` path is **not** itself a TrustedLocalRoot; reject unsafe root before using it. Input ContentRefs and output Bundle belong under same verified root but disjoint relative keys. Never import CLI Concrete into Application, never persist row/credential secrets in Context/Manifest. P05 refuses all row release requests unconditionally; there is no signing anchor in the active local CLI contract.

### 6.2. `LocalCausalUseCase` field/constructor contract (30_62 §1 / RUN01,03,04,06,07)

**Class:** `ariadne.capabilities.causal.local_execution.LocalCausalUseCase`; stateless reusable Application orchestration. Only immutable Constructor-injected Port fields:

| Field | Type | Role |
| --- | --- | --- |
| `refs` | `ContentReferencePort` | actual FD-bound input validation |
| `capabilities` | `MethodCapabilityPort` | validated Method/Backend/Profile |
| `discovery` | `DiscoveryPort` | selected FCI/PAG execution |
| `identifier` | `IdentificationPort` | downstream later Gate, no G01 call |
| `estimators` | `EstimatorPort` | downstream later Gate, no G01 call |
| `diagnostics` | `DiagnosticPort` | downstream later Gate, no G01 call |
| `publisher` | `LocalPublicationPort` | all output staging and single atomic commit |
| `reader` | `LocalManifestReaderPort` | independently verified committed readback |
| `privacy` | `LocalPrivacyPolicyPort` | typed no-row decision |
| `runtime` | `RuntimeEnvironmentPort` | real runtime/lock/environment facts |
| `clock` | `ClockPort` | injected time; no invented timestamps |
| `manifest_factory` | `LocalManifestFactoryPort` | Application-owned abstract Manifest building; CLI Adapter injected by composition root |

~~~python
def __init__(self, *, refs: ContentReferencePort, capabilities: MethodCapabilityPort,
             discovery: DiscoveryPort, identifier: IdentificationPort,
             estimators: EstimatorPort, diagnostics: DiagnosticPort,
             publisher: LocalPublicationPort, reader: LocalManifestReaderPort,
             privacy: LocalPrivacyPolicyPort,
             runtime: RuntimeEnvironmentPort, clock: ClockPort,
             manifest_factory: LocalManifestFactoryPort): ...
def preflight(self, spec: ValidatedStudy, context: LocalRunContext) -> PreflightReport: ...
def run(self, spec: ValidatedStudy, context: LocalRunContext) -> LocalRunOutcome: ...
~~~

**Constructor:** require every Port, no optional Backend import, no filesystem creation, no runtime scientific fit. Request-specific sink, status, graph, policy and run metadata remain local to `run`, not instance fields. `preflight`/`run` accept only common `ValidatedStudy`; never Application-import `LocalStudySpec`.

### 6.2a. Manifest boundary correction — DEC-G01-P05-MANIFEST-BOUNDARY-01=A (formal 09/S10/S11 pending)

The twelfth required constructor Port `ariadne.capabilities.causal.ports.manifest_factory.LocalManifestFactoryPort` has `build(*,evidence:ManifestBuildEvidence)->ManifestValue`. `ManifestBuildEvidence` is an Application-visible deeply immutable record with exactly `study:ValidatedStudy`, `study_payload`, `status_payload`, `runtime:ManifestRuntimeFacts`, `stochastic`, `artifact_descriptors:tuple[ArtifactDescriptorView,...]`, `output_graph_ref:ContentRef|None`, `graph_negative_reason_codes:tuple[str,...]`, and `review_science_evidence_ref:ContentRef|None`. Runtime fields are `repo_commit`, `dirty`, `python_version`, `platform`, `uv_lock_sha256`, `distributions`, `api_probes`. JSON mappings are immutable, JSON-valid snapshots; each descriptor has exactly the original six stage-returned fields. `ManifestValue` is the existing Application-side Protocol, not a concrete CLI import. CLI composition root creates and injects `ariadne.interfaces.cli.local_causal.manifest_factory.LocalManifestFactoryAdapter`; only this Adapter may convert neutral values into the P01 CLI `ValidatedRunEvidence` and call existing `LocalRunManifest.from_run_evidence`. The Adapter must not duplicate or bypass P01 checks or manufacture observed facts. Missing/invalid Factory or evidence fails closed before `seal`, Marker and rename. Other eleven Port signatures, P02 `LocalPublicationPort.seal`, public E11 wire and independent Reader remain unchanged. IF 23_41 §4.1a and DD 30_62 §1.8 are authoritative.

### 6.3. `preflight` processing and `--check-only` (RUN03/04/07)

**Precondition:** strict P01 `ValidatedStudy` and P02 `LocalRunContext`. Steps:
1. Validate run_id, E11 version, requested `DISCOVER` + `P1-M06` + `causal-learn` and `EXPLORATORY` + non-Effect GRAPH_STRUCTURE; identify unsupported combination without fallback.
2. Revalidate TrustedRoot/Principal, input ContentRef identities, actual Question/Design/Dataset bytes through `refs.verify` with P02 safe same-FD hash. P01 decoder is insufficient to verify these files.
3. Decode verified Question/Design with P1-M06 strict JSON profiles; check `question.question_id=design.question_id=Study.inputs.question.identity`, declared Dataset columns/order = Design variables, all CI measurement scales and BK JCS equivalence. Reject duplicates, unknown scales and inappropriate data; no auto-fix/imputation.
4. Resolve Method Capability via validated full `ValidatedCapabilityRequest` and `MethodCapabilityPort.resolve`; inspect static CI eligibility and effective Backend metadata without executing FCI or publishing any file. Unsupported/missing Backend must be typed; no substitute method.
5. Enforce G01 aggregate-only: **either** Study row request -> explicit PRIVACY_DENIED (exit3); no silent downgrade. For aggregate requests, verify effective Root/Principal; no independent approval authority is involved. `--check-only` never probes row release as if allowed.
6. Return `PreflightReport` with actual verified inputs, typed errors, capability and assumptions; `science_acceptance=NOT_EVALUATED`. **No scientific fit, staging directory, artifact, Manifest or Marker creation.**

### 6.4. `run` — one DISCOVER vertical slice (RUN01/03/04/06/07; DISC01–03)

**Algorithm (preserve this order and single-writer responsibilities):**

1. Execute `preflight(spec,context)` and fail closed on invalid Study, Reference, CI eligibility, Privacy or root. Reuse validated actual-byte evidence only if its FD/snapshot is still valid; otherwise reverify before scientific execution. No Model work before input security.
2. Bind approved Method/Backend/Profile, effective runtime evidence and seed to a `ValidatedDiscoveryRequest` (`ariadne.causal.discovery.contracts`) with the verified Question/Design/Dataset and input hashes. Check the selected Capability equals the Method that will execute.
3. Evaluate LocalPrivacyPolicyPort.authorize BEFORE staging, using exactly current validated Study, live TrustedRoot/Principal, declared DISCOVER_AGGREGATE_ONLY output shape. Its immutable PrivacyDecision binds allowed, run_id, strict JCS request_hash, live root dirfd identity, principal_uid, classification=AGGREGATE, row_export_requested=false and output_shape=DISCOVER_AGGREGATE_ONLY (P02 §6.3). Denied/missing/mismatched decision aborts before begin; no new human approval. The same decision is subsequently forwarded to seal; G05 row opt-in does not apply to G01.
4. Construct a fresh exact nominal `PublicationSessionToken()` from `ariadne.capabilities.causal.ports.local_io` for this attempt; retain it and the expected validated run_id/request_hash/root in local variables independent of the sink. Obtain `StagingArtifactSink` through `LocalPublicationPort.begin(*,run_id,request_hash,root,session=session)`; never reuse the token or reconstruct expectations from the sink. Do not allocate final `runs/{run_id}` or hand final Path to scientific Adapter.
5. Call `DiscoveryPort.discover(ValidatedDiscoveryRequest,*,sink)`, through P04's selected FCI Adapter. The Result is a typed `GraphEvidence` (P03) or a justified scientific Graph-negative with nonempty reasons. Technical Backend/graph errors abort/leave uncommitted staging and map exit4; they are not "valid negative Graph" and cannot be published as SCI-negative.
6. Build the validated typed `study_payload` identical to `ValidatedStudy` and a typed `e11-local-status/1` `status_payload` from the same run (for a publishable candidate: `technical_status=COMPLETED` and `manifest_relative_path="runs/{run_id}/manifest.json"`); use both as the exact serialized sources for `study.json`/`status.json`. Stage via P02 and collect *returned* exact-byte `ArtifactDescriptor`s. Stage either validated P03 `graph.json` and construct its five-field **output** `ContentRef` from the same descriptor and P03 Graph identity with TrustedRoot-relative future `relative_key="runs/{run_id}/graph.json"` (staged Descriptor key remains bundle-root-relative `graph.json`), **or** an authentic P04 discriminated scientific-negative with validated Method-specific evidence (not a Backend error), plus diagnostics.json, graph_negative_reason_codes=("SCI_NO_ADMISSIBLE_PAG",) and Status reason_codes=["SCI_NO_ADMISSIBLE_PAG"] exactly; never both. That code is reserved and currently has no established real P04 producer; do not synthesize a negative to pass tests. Even when caller-controlled strings match in both fields, a technical failure/missing or malformed Graph/unsupported BK must abort rather than publish a science-negative. Construct Application-owned immutable `ManifestBuildEvidence(study,study_payload,status_payload,runtime,stochastic,artifact_descriptors,output_graph_ref,graph_negative_reason_codes,review_science_evidence_ref=None)` from observed facts and the P02 stage-returned descriptors; pass it only through injected `LocalManifestFactoryPort.build(evidence=evidence) -> ManifestValue`. The CLI-root-injected `LocalManifestFactoryAdapter` alone converts to P01 nominal `RuntimeEvidence`/`ArtifactDescriptor`/`ValidatedRunEvidence` and invokes unchanged `LocalRunManifest.from_run_evidence`. Application must never import P01 CLI concrete DTOs or the CLI Factory. The factory checks pure input-ref↔lineage and output-graph-ref↔inventory joins; P05/P02 independently verify actual bytes and Graph/Status contents. For both cases `schema_dispatch.result=null`, no `result.json`. Success `schema_dispatch.graph="e11-local-graph/1"`; scientific negative `graph=null` + mandatory diagnostics/reason. `Study.inputs.graph=null` remains input request; `manifest.lineage.graph` is generated output Graph or null. Treat candidate `COMPLETED` serialized status as provisional until P02 publish and Reader verify; do not return completed early.
7. Status axes remain independent: `identification_status=NOT_APPLICABLE`, `point_availability=NOT_REQUESTED`, `inference_availability=NOT_REQUESTED`, `science_acceptance=NOT_EVALUATED`. This CLI run cannot declare independent Science PASS. Actual technical completion is conditional on committed Reader result.
8. Seal by LocalPublicationPort.seal(*,sink,manifest,privacy=<same prior PrivacyDecision>); facade MUST forward it to P02 Concrete validate(manifest,*,privacy). P02 independently recomputes policy from staged Study/current verified root/UID and actual inventory, rejects absent/denied/cross-run/root/UID/conflicting decision before Marker and rename. Publish via publish(*,bundle,root); P02 alone owns staging/Marker/filesync/rename/readback and EEXIST reuse semantics. Use `LocalManifestReaderPort.verify(*,root,run_id)` for post-publication independent verification (idempotent second read is permitted); **return** `LocalRunOutcome(COMPLETED, verified ref, scientific axes)` only after success.
9. If post-rename outcome indeterminate, return typed publication failure (CLI exit5), never delete or repair a possibly published run. After successful `begin` and before calling `publish`, any failure (Discovery, stage, runtime/Graph/Status joins, Manifest Factory, or `seal`) MUST invoke the existing injected `LocalPublicationPort.abort(*,sink,session,run_id,request_hash,root,reason)` with that exact sink and independently retained expected values, once; no CLI Concrete import/access. `reason` must be nonsecret. The P02 Adapter verifies sink/publisher/issuer/session/run/hash/root/policy identity and allowed state and delegates to existing concrete `LocalArtifactPublisher.abort(reason)` to close handles and quarantine private residue. It does not guarantee secure deletion. Never call this Application abort on an exception from `publish` or after publish has started, because rename may have succeeded or be indeterminate; those outcomes are controlled by the P02 Publisher and independent Reader. Preserve primary typed exception/exit classification and report cleanup exception separately, never suppress failure or claim rollback/COMPLETED/SCI-negative. Incorrect request_hash on existing run -> conflict, no overwrite. Never conflate science-negative result (may be technical exit0 when fully published) with backend exception (exit4).

**Operation dispatch:** Other operations (`IDENTIFY/ESTIMATE/REFUTE/SENSITIVITY/DIAGNOSE`) have defined ports but are **not implemented in G01**. Reject them as typed `UNSUPPORTED_COMBINATION` before anything executes, not as successful fallback to FCI. Subsequent Gate implementations will use `IdentifierPort/EstimatorPort/DiagnosticPort` and 23_42 Bundle matrix; preserve constructor API now without implementing their scientific methods.

### 6.5. LocalPrivacyPolicyPort and concrete — aggregate-only G01 contract

**Port module:** `ariadne.capabilities.causal.ports.local_privacy.LocalPrivacyPolicyPort`. Concrete `ariadne.interfaces.cli.local_causal.privacy.LocalPrivacyPolicy` is stateless: `__init__(self)->None`; it accepts call-local validated Study, effective Principal, private TrustedRoot and Method output shape. There is **no active third-party signer, trust registry, signing verifier Port, key or revocation dependency** in the E11 local CLI.

~~~python
def authorize(self, *, study: ValidatedStudy, root: TrustedLocalRoot, principal: LocalPrincipal,
              output_shape: OutputShape) -> PrivacyDecision: ...
def filter_export_columns(self, frame_schema: ColumnSchema, *,
                          decision: PrivacyDecision) -> ColumnSelection: ...
~~~

**G01 requirements:** `privacy.row_export_requested=false`（G01に追加CLI Study row requestなし）, trusted same-UID private root with valid owner/mode/local FS and aggregate-only verified output shape. **Studyのrow_export_requested=true** is invalid in G01, exit3 before any row bytes or Stage; no silent fallback. G01 never executes `filter_export_columns` for individual rows or creates `row_effects.parquet`.

G05 alone supports optional individual-row intermediate output by the executor's Study単独の明示opt-in, safe non-root Linux ext4/XFS private root and Method-specific approved row/column/byte bounds. This is not an independent human approval. The G05 decision cannot expand the G01 scientific or operation scope.

**Release invariant:** neither Publisher staging nor stdout/stderr/log stores individual rows/secret raw data; input Dataset may contain rows but only aggregate Graph/Diagnostics/Status is published. Test report should not contain row-level fixture payloads.

### 6.6. CLI `command.main` and version compatibility (30_62 §8.5; RUN06/07, PUB10/MAN06/READ06)

**Module/entrypoint:** `ariadne.interfaces.cli.local_causal.command.main(argv: list[str]|None) -> int` registered **only** as new `ariadne-causal-local` in `pyproject.toml`. Preserve old `ariadne-identify`, `ariadne-estimate`, `ariadne-refute`, `ariadne-sensitivity`, legacy `causal-analysis-spec/2`, `CliManifest(manifest_version="2.0")` and Product DB/Web/Worker path.

**CLI syntax:** `ariadne-causal-local --config STUDY.yaml --output-root ROOT [--check-only] [--json]`. File format must be explicitly determined and validated (not silently reinterpret Product v2). Construct Decoder, TrustedRoot Factory, Port adapters, selected FCI Method Registry and UseCase through **one** composition root; never import optional Method during ordinary CLI parsing.

| Exit | Trigger | Required stdout/stderr and persistence |
| --- | --- | --- |
| 0 | valid check-only static preflight, or full run with independently verified complete Bundle, **including legitimate scientific negative** | sanitized run_id/technical/science/manifest reference; check-only no write |
| 2 | unknown/legacy/versionless schema, method/Operation/Estimand/config inconsistency, duplicate YAML | config phase reason, no final run |
| 3 | invalid physical input/path/hash/root/owner/mount, Study row request in G01; invalid local privacy/UID | security/privacy reason, no rows or leak |
| 4 | selected Backend missing/version/API invalid or technical FCI error, malformed Backend graph | engine phase, no false committed marker |
| 5 | staging/FS syscall/rename collision/readback corruption/indeterminate result | publication phase; no false completed status, no overwrite |

For `--json` stdout emit exactly one syntactically valid sanitized JSON control envelope (no raw Dataset/secret/path). stderr uses typed upper-case reason code and phase, without raw row content. Exit0 **never** implies scientific PASS. Do not change old CLI exit/error semantics.

### 6.6a. Session-bound abort and bounded completed-P02 exception

IF 23_41 §4.1b and DD 30_62 §8.2a are authoritative. Application imports `PublicationSessionToken` from local_io, not CLI Concrete. Create one fresh token for each run attempt after preflight/Privacy authorization, before begin, and keep it and validated run_id, request_hash, and exact context.root independently of the returned sink. Invoke `publisher.begin(run_id=run_id,request_hash=request_hash,root=root,session=session)`. Only after begin returns successfully is abort eligible. Maintain a local pre-publish phase flag, set to false immediately before invoking publish (not after it returns). In the exception path while eligible, make exactly one attempt `publisher.abort(sink=sink,session=session,run_id=run_id,request_hash=request_hash,root=root,reason=sanitized_reason)`. Never obtain expected values from sink, reuse a token, or call sink.abort/private fields. Distinct attempts have distinct tokens even if Study/run/hash/root match. Per-session calls are sequential; distinct sessions may interleave.

Adapter checks the full independent identity predicate and STAGING/VALIDATING state specified in DD 30_62 §8.2a, then delegates unchanged concrete abort. A mismatched sink/issuer/token/run/hash/root/policy or invalid state fails without touching either session. Do not claim secure removal of quarantined bytes. Keep the primary typed error/exit category and report a secondary nonsecret cleanup fault separately. No abort before successful begin or after entering publish, even if publish raises. No false COMPLETED, scientific-negative or newly committed final Marker/run; preserve any pre-existing final run. Private staging Marker may exist after seal. Independent Reader remains mandatory. Check-only performs neither begin nor abort.

**Bounded exception:** later S11 may authorize only token and Port begin/abort in `src/ariadne/capabilities/causal/ports/local_io.py`, and Publisher constructor/private issuance fields plus Adapter begin/abort in `src/ariadne/interfaces/cli/local_causal/publication.py`, as specified in AMD-003. Existing direct constructor and begin callers without session remain compatible; such legacy sessions are ineligible for facade abort. Existing concrete begin/validate/commit/abort algorithms, Adapter seal/publish, scientific sink, P02 06/07/tests/checkpoints and P01/P03/P04 remain protected. No new Port collaborator, registry or public wire change. Formal 09/S10/S11 remain separate decisions.

### 6.7. Reuse/negative/rollback boundaries and DD ownership

| Owner | Reuse | Never do |
| --- | --- | --- |
| P01 DTO/Codec | strict E11 study, JCS, typed Manifest | reparse into a second looser Schema |
| P02 Port/FS | trusted FD verification, one run-atomic publisher, independent reader | direct `Path.rename` or file writes from UseCase |
| P03 Graph value | PAG/endpoint/Version/null/digest evidence | Product GraphVersion issuance or automatic identification |
| P04 Method/Discovery | selected FCI and typed negative, science Oracle | PC fallback, backend-specified arbitrary output path |
| P05 Application/CLI | ordered orchestration, no-row policy, status/exit | Web/API/DB/Worker or existing Product CLI rewrite |

Errors have typed `phase` and stable reason codes, no unbounded path/row values. Use `PreflightReport` for check-only, `LocalRunOutcome` for run result. On retry verify same request hash and existing run fully via P02; do not regenerate scientific truth or presume exactly-once execution. Package success is not G01_999 PASS.

## 7. Focused verification — integration, Privacy and protected legacy behavior

| DD / Gate item | Primary layer | Positive and negative assertions |
| --- | --- | --- |
| RUN01/03/04/07, MAN04, DISC01–03; 07-07 | contract + integration | DISCOVER Graph-positive/typed negative inventory, no Effect, typed Status/target/version |
| PRIV01–06; 07-11 | contract + integration | check-only fit/staging/publish all zero, Study row request rejected, unsafe root denied, stdout/staging no leaks |
| RUN06, PUB10, MAN06, READ06; 07-12 | actual existing Product v2 contract/integration suite + G01 enhancement checks | v2 CLI/result/manifest behavior unchanged and semantic/bytes compatibility |
| PUB07/READ03; 07-11 | real publication + CLI integration | exit4 vs exit5, no false COMMITTED after indeterminate/failed readback |

**Bounded Product regression test exception (DEC-G01-P05-CLI-CLASSIFICATION-01=A; AMD-E11-G01-P05-004):** After separate formal 09 approval, S10 refreeze and S11 reauthorization, modify only the CLI classification test `test_all_analysis_cli_scripts_are_explicitly_low_level_utilities` in `tests/product/test_enh_e4_g07_p03_cli_boundary.py` (rename permitted; explicit expected mappings may be local to this function). Preserve the existing five-member LOW_LEVEL_UTILITY constant and other test/helper bodies. Classify the approved new `ariadne-causal-local = "ariadne.interfaces.cli.local_causal.command:main"` as a distinct Local lifecycle CLI, not a low-level utility. Exhaustively compare all registrations targeting the `ariadne.interfaces.cli.` namespace to six fixed name-to-target mappings: `ariadne-discover = ariadne.interfaces.cli.discovery:main`, `ariadne-estimate = ariadne.interfaces.cli.estimation:main`, `ariadne-identify = ariadne.interfaces.cli.identification:main`, `ariadne-refute = ariadne.interfaces.cli.refutation:main`, `ariadne-sensitivity = ariadne.interfaces.cli.sensitivity:main`, and `ariadne-causal-local = ariadne.interfaces.cli.local_causal.command:main`. Assert the five legacy names equal LOW_LEVEL_UTILITY and are disjoint from the new Local lifecycle classification. Reject missing, redirected or unclassified CLI entries. Independent verification is specified in G01-07-12. Do not exclude the new namespace, skip/xfail the test, derive expected mappings from actual registrations, or add an entrypoint wrapper to evade the guard. This exception concerns one test, not legacy Product production code or other protected tests. Existing AMD-001/002/003 scope and acceptance remain binding. Preserve the Agent's uncommitted P05 implementation and status report; reconcile remote documentation changes without destructive reset/clean or overwriting local work. Rerun the affected test file and all focused and required Product/G01 regression suites before any P05 checkpoint. No implementation or test-code authorization is issued by this Author amendment alone.

**Required Package check:** Actual code test paths/pytest commands are resolved by 40 from candidate checkout; newly implemented cases start in G01 enhancement lifecycle. Existing Product v2 tests may remain in historical `tests/product/` or other current locations and are executed in place; no automatic mass migration or `tests/regression` promotion. All focused DD cases and current legacy suites must be collected and observed, with full source/fixture/env SHA, actual exit and failure phase. This Package cannot declare G01 Gate PASS or Science PASS without independent 07/999 evidence.

## 8. Protected contract / Transition Debt constraints
Product v2の既存CLI/Manifest/Result contractを回帰保護する。未完成のGraph/Science/個票認可を完成と見なさない。PREPARATION-03の技術判定はG01単一Gate維持（Owner承認待ち）。P02のOS/FS Publication、P04の独立FCI/PAG Science、P05のCLI統合・Privacy/旧v2回帰は別々の必須受入軸であり、全軸が同じFixed Candidate SHAで実証されるまでG01_999 PASS不可。OwnerのGate境界承認・06/07 Freeze/Coding AuthorizationまではPxx着手禁止。

## 9. Checkpoint / reporting rule

Package completion時:

1. implementation-affecting changeをcommitする。
2. implementation checkpoint full SHAを固定する。
3. `implementation_checkpoint_report`を作成する。
4. `*_in_progress.md`へexecution statusを記録する。
5. report-only commitが別ならcheckpoint SHAと区別する。

## 10. Package completion criteria — Definition of Done

- [ ] `LocalRunContext` trusted root/principal created by CLI composition, not Study YAML; `LocalCausalUseCase` 11 injected Port fields (no policy_verifier) and exact `preflight/run` signatures implemented.
- [ ] Preflight verifies actual Question/Design/Dataset bytes and Method/CI eligibility with zero fit/staging/publish; Run uses exact `CapabilityPort -> DiscoveryPort -> FCI -> LocalPublicationPort -> Reader` flow, no uncontrolled final Path write.
- [ ] `LocalPrivacyPolicyPort.authorize` and stateless CLI Concrete deny Study row request, unsafe owner/mode/local FS/Principal, with no aggregate fallback and zero row/secret leak; no Policy Anchor or signature verifier is created.
- [ ] Graph-positive vs valid science-negative Operation Bundle rules, Status axis separation, JCS/lineage/dual hash, no dummy Effect and no false COMMITTED implemented.
- [ ] New `ariadne-causal-local` command maps exits 0/2/3/4/5 by phase and emits sanitized single JSON response; old Product v2 CLI/contracts unchanged.
- [ ] P01–P04 dependency checkpoints confirmed; focused CLI integration and existing Product v2 contract/regression cases and full SHA/fixture/env/DD-ID evidence recorded. P05 PACKAGE_COMPLETE alone is not G01_999 PASS.

## 11. External reference policy

source / previous checkpoint / test output / provenanceは外部参照してよい。本書のimplementation rule、prohibited scope、completion criterionをParent 06 / P00へ委譲してはならない。

## 12. Stop rule

- package scope完了 -> `PACKAGE_COMPLETE`
- continuation不能 -> `PACKAGE_BLOCKED`
- Gate PASS / FAILは判定しない。
- next packageへ勝手に先行しない。


## S02-01/02/06/07 対象Gateの確定契約（Owner採用・未実装）

G01は`P1-M06`のDISCOVERのみで、個票の出力を常に拒否する。Valid Studyの`privacy.row_export_requested=false`（省略の扱いはstrict Study schemaのdefault/requiredに従う）を要求し、trueはPrivacy exit3。廃止された追加CLI row許可flagを登録せず、渡された場合は不明オプションとしてconfig exit2。Contextは`LocalRunContext(root:TrustedLocalRoot,principal:LocalPrincipal)`、Privacy Portは`authorize(*,study,root,principal,output_shape)`であり、署名Policy/Study policy_refは存在しない。G05のみStudy単独opt-in（true）とOS/Method制約の全件ANDを満たす個票中間出力を担当する。

新Local Graphのimmutable identityは内容hash、parent/source科学証拠とContentRef。Product GraphVersion DBへlookup/write/edit/FIXせず、現行E11 Graph wireの`version_id`と`parent_version_id`はどちらもnullとし、non-nullは未対応importとして拒否する。既存ProductのGraphVersionServiceや旧v2は無変更。

OS/FS受入は有界な不変条件別の正負例（owner EUID・0700/0600・dirfd/O_NOFOLLOW・same FS・symlink/race・rename前後・post-rename indeterminate・Marker/Reader/hash）に限定する。冗長なfault-permutation全順列、statx mount-ID/namespace証明、ACL/xattr digest/コンテナ推測、電源断耐久保証は追加しない。JCS RFC8785 golden bytes、no-clobber、公開後整合性、独立PAG Science Oracleは維持する。Coding Agentが未承認の広いProof強化を推測で復活させない。


### PrivacyDecision cross-layer trace (AMD-E11-G01-P02-001)

NFR-030/031 ↔ LDD 21_23/21_40 ↔ BD 22_09/22_12 ↔ IF 23_41/23_42 ↔ DD 30_62 ↔ G01/P02-P05 06 ↔ G01 07-05/06/11. At run step 3 P05 produces the run/root/UID-bound decision from the validated Study and keeps the exact result; at step 8 passes the same object to P02 seal. P02 is the final pre-publication policy evaluator. P05 cannot treat an initial allowed=True as sufficient for commit, create a second unbound decision, or authorize G01 row artifacts.


### G01 PrivacyDecision pass-through equality (clarification)

P05 obtains its initial decision from the configured trusted local policy, and passes its **immutable value**, unchanged, to P02 seal. `same prior PrivacyDecision` means all fields equal to the initial result, not that Publisher must prove the same allocated object or trusted issuer provenance. P02's trusted independent policy evaluation on actual staged bytes/root/UID/inventory is the final authority; a separate equal-value instance is not rejected by provenance alone. A discrepancy, current deny or row-output violation is rejected. No Policy Anchor or signature is added.


### P05 G01 Graph-negative typed diagnostic production boundary

On a **genuinely justified** P04 `SCI_NO_ADMISSIBLE_PAG` negative, P05 stages a strict internal G01/P1-M06 DISCOVER diagnostic JSON with exactly `run_id` (same Status/Manifest), `operation="DISCOVER"`, `method_id="P1-M06"`, `reason_codes=["SCI_NO_ADMISSIBLE_PAG"]`; its Status has the same singleton reason, technical status COMPLETED, and Manifest output Graph refs null. P05 must not synthesize a science-negative from a Backend/FCI exception, and P02/Reader must independently validate physical bytes and semantic joins. No additional required fields, public schema_version, changed P01 06, or P03/P04 science-contract relaxation.
