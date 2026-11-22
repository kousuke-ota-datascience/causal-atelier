# ENH-E11 G01 P05 — Local CLI, UseCase, Privacy, Legacy Regression

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

~~~python
def __init__(self, *, refs: ContentReferencePort, capabilities: MethodCapabilityPort,
             discovery: DiscoveryPort, identifier: IdentificationPort,
             estimators: EstimatorPort, diagnostics: DiagnosticPort,
             publisher: LocalPublicationPort, reader: LocalManifestReaderPort,
             privacy: LocalPrivacyPolicyPort,
             runtime: RuntimeEnvironmentPort, clock: ClockPort): ...
def preflight(self, spec: ValidatedStudy, context: LocalRunContext) -> PreflightReport: ...
def run(self, spec: ValidatedStudy, context: LocalRunContext) -> LocalRunOutcome: ...
~~~

**Constructor:** require every Port, no optional Backend import, no filesystem creation, no runtime scientific fit. Request-specific sink, status, graph, policy and run metadata remain local to `run`, not instance fields. `preflight`/`run` accept only common `ValidatedStudy`; never Application-import `LocalStudySpec`.

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
3. Evaluate `LocalPrivacyPolicyPort.authorize` **before row-producing or staging side effects** (G01 aggregate-only). G01 aggregate-only requires no additional approval; G05 local executor opt-in does not authorize individual rows in G01.
4. Obtain `StagingArtifactSink` through `LocalPublicationPort.begin(*,run_id,request_hash,root)`; sink must be bound to exact root/run/hash. Do not allocate final `runs/{run_id}` or hand final Path to scientific Adapter.
5. Call `DiscoveryPort.discover(ValidatedDiscoveryRequest,*,sink)`, through P04's selected FCI Adapter. The Result is a typed `GraphEvidence` (P03) or a justified scientific Graph-negative with nonempty reasons. Technical Backend/graph errors abort/leave uncommitted staging and map exit4; they are not "valid negative Graph" and cannot be published as SCI-negative.
6. Build G01 `study.json`, `status.json` and either `graph.json` (success) or `diagnostics.json` (valid Graph-negative). Build `LocalRunManifest.from_run_evidence` from exact bytes inventory. For both cases `schema_dispatch.result=null`, no `result.json`. Success `schema_dispatch.graph="e11-local-graph/1"`; scientific negative `graph=null` + mandatory diagnostics/reason. `Study.inputs.graph=null` remains input request; output Graph is separate.
7. Status axes remain independent: `identification_status=NOT_APPLICABLE`, `point_availability=NOT_REQUESTED`, `inference_availability=NOT_REQUESTED`, `science_acceptance=NOT_EVALUATED`. This CLI run cannot declare independent Science PASS. Actual technical completion is conditional on committed Reader result.
8. Seal via `LocalPublicationPort.seal(*,sink,manifest,privacy)`, publish via `publish(*,bundle,root)`; P02 alone owns staging/Marker/filesync/rename/readback and EEXIST reuse semantics. Use `LocalManifestReaderPort.verify(*,root,run_id)` for post-publication independent verification (idempotent second read is permitted); **return** `LocalRunOutcome(COMPLETED, verified ref, scientific axes)` only after success.
9. If post-rename outcome indeterminate, return typed publication failure (CLI exit5), never delete or repair a possibly published run. On pre-rename failure, abort scoped staging only. Incorrect request_hash on existing run -> conflict, no overwrite. Never conflate science-negative result (may be technical exit0 when fully published) with backend exception (exit4).

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
