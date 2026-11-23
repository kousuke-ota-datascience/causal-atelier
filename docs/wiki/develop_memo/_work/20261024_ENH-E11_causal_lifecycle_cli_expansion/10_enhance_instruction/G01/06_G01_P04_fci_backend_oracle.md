# ENH-E11 G01 P04 — FCI Capability, Eligibility, Independent Graph Oracle

**DEC-G01-EXEC-01（Owner 2026-11-23採用・G01のみの実施順序変更）:** `combined_review/177_20261123_dec_g01_exec01_owner_adopted_evidence_rephasing.md`がG01の従前S09→S10→S11依存を部分的に上書きする。利用不能なPython3.12実測B02/B04、独立S09/B05科学審査は**Coding Entryの必要条件から外し、G01_999 PASSまでの必須受入条件へ移す**。事前Author契約整合と例外Ledgerを材料に、Ownerの**別個の暫定G01-S10 Freeze**、その後Ownerの**別個の限定G01-S11 Coding Authorization**を認める。どちらも現在**未承認**。限定許可はG01/P01–P05の実装・開発者テストのみ。実Python3.12 Schema/FCI、独立MAG/PAG/BK、実FS/Reader、T2/T3、独立07/999、Product v2回帰の要求・合格基準は維持。未検証をPASS扱いせず、non-null BKはFCI呼出前exit4 fail-closed、科学的真値や閾値の自己創作禁止。G01_999がPASSするまで下流Gate依存は解除しない。

**Document class:** Primary Execution Contract  
**Self-containment:** MUST — Assigned Coding Agentが本書だけでpackageのnormative execution responsibilityを理解できること。

- Gate: G01
- Trial: Trial01（未開始）
- Package: P04
- Parent 06 (traceability): 06_Ariadne_ENH-E11_G01_implementation_instruction.md
- P00 Plan (traceability): 06_G01_P00_work_package_plan.md
- Depends on: P01,P03
- Status at issuance: DRAFT / CODING_NOT_AUTHORIZED

## 1. Purpose
FCI/PAG Adapterの技術的・科学的適格性を分離して実証する。

## 2. Effective Gate constraints applicable to this package

このpackageが守るべきGate-level semanticsを、Parent 06 / P00を読まなくても実行判断できる粒度で記載する。

G01は正式Gate IDでPxxはbounded Coding Unit。Local laneとProduct v2を分離し旧CLI/Web/API/DB/Workerは改変しない。strict version/Method/EstimatorとJCSのハッシュ対象を検証し、PAGをDAG/ATEへ変換しない。OS root/Privacy/Atomic Publishの不適格はfail-closed、SCI不確実性をPASSに変換しない。Coding Authorization前の実装は禁止。

## 3. In scope — implementation ownership

| Class / Port | This Package owns | Reuse boundary |
| --- | --- | --- |
| `ariadne.capabilities.causal.method_registry.MethodCapabilityRegistry` | 41 Method metadata authority; G01 selected P1-M06 only | Product `ScientificValidationService` shared eligibility policy; no duplicate rules |
| `ariadne.scientific.capabilities.BackendCapabilityRecord` | immutable effective version/API/extra/availability evidence | No optional import in Value |
| `ariadne.scientific.ports.capability.MethodCapabilityPort` | Operation/Estimand/Inference-aware typed `resolve` façade | Do not infer request eligibility from 3 IDs |
| `ariadne.scientific.ports.causal.DiscoveryPort` | typed `discover(request,*,sink)` method-bound dispatcher | Product `ScientificCorePort.run_discovery` ABI unchanged |
| `ariadne.scientific.causal_methods.discovery.FciDiscoveryAdapter` | `preflight`/`execute` with selected `causal-learn` FCI | Existing PC is not FCI; no duplicate algorithm |
| G01 independent Graph Oracle fixture/test harness | independently derived observed MAG/PAG reference, BK and latent negatives | 07 scientific acceptance authority retained |

P04 depends on P01 and P03. P02 publication is **not** a prerequisite to pure component/Science preflight tests; adapter output may go into an isolated fake StagingSink, but this never certifies real publication.

## 4. Explicitly out of scope
他GateのMethod実装、旧Product v2変更、根拠なしのScience PASS、行出力自己許可、不適格なUID/owner/mode/local FS、既存run上書き、Package外の便乗変更。

## 5. Entry criteria / required evidence
Gate 06/07のFreeze・Coding Authorization・固定branch HEAD確認。Depends on P01,P03の実装checkpoint full SHAとfocused検証を確認。矛盾/依存未成立はBLOCKED。

dependency checkpoint / source state等はfactとして外部参照してよい。Entry rule自体は本書内に記載する。

## 6. Required implementation — capability, FCI and science evidence

### 6.1. `MethodCapabilityRegistry` (30_62 §2 / CAP01,04,05)

**Class/Module:** `ariadne.capabilities.causal.method_registry.MethodCapabilityRegistry`. Immutable Constructor fields:

| Field | Type | Invariant |
| --- | --- | --- |
| `descriptors` | `Mapping[str,MethodDescriptor]` | unique pinned ID; Operation/Estimand/Inference explicit |
| `backend_factories` | `Mapping[str,AdapterFactory]` | eligible Method/Profile only, lazy import |
| `effective_env` | `RuntimeEnvironmentPort` | observed environment version/signatures |
| `inference_registry` | `InferenceRegistry` | point-only / confirmatory separated |

~~~python
def __init__(self, descriptors, backend_factories, effective_env, inference_registry): ...
def describe(self, method_id: str) -> MethodDescriptor: ...
def resolve(self, method_id: str, backend_id: str, profile: str) -> BackendCapabilityRecord: ...
def load_adapter(self, capability: BackendCapabilityRecord) -> ScientificAdapter: ...
~~~

**Preconditions:** validate unique descriptors, Method IDs from approved Method41 authority, Operation/Estimand/Inference capabilities and versioned descriptor schema at Construction. No Backend import, scientific Fit or FS publication at constructor/`describe`/`resolve`. `describe` returns pure metadata, unknown ID typed reject.

**resolve flow:** approved selected Method (`P1-M06`), explicit Backend `causal-learn` and declared eligible profile -> effective installed distribution/ABI, relevant extra, chosen CI, inference/analysis mode and API probes -> immutable capability record. Backend default or `pyproject.toml` declaration does not establish runtime availability. Do not use StageRunnerRegistry as second Method registry. Unsupported Method/Backend/version -> typed nonavailable/unsupported, never silent fallback or import unrelated method. `load_adapter` alone lazy-imports approved optional engine; a missing import changes only selected Method's availability, not legacy startup.

### 6.2. `BackendCapabilityRecord` and `MethodCapabilityPort` (30_62 §7/8.1; CAP04/05)

**Record Module:** `ariadne.scientific.capabilities.BackendCapabilityRecord`. Immutable fields `method_id`, `backend_id`, `distribution_version`, `adapter_version`, `api_signature_hash`, `extra`, `profile`, `available` and `reason`. Construct from *effective observed* versions/probes; no fake defaults. Method `check(self, request: ValidatedCapabilityRequest) -> typed compatibility decision`; pure request-vs-capability assertion.

**Public Port:** `ariadne.scientific.ports.capability.MethodCapabilityPort.resolve(request: ValidatedCapabilityRequest) -> BackendCapabilityRecord`. Request includes Operation, Estimand, Design, Backend, profile and Inference constraints. Facade validates **all** and only then delegates to concrete `MethodCapabilityRegistry.resolve(method_id, backend_id, profile)`; do not pass a bare triple in lieu of a validated request. Same registry metadata and compatibility policy used by legacy `ScientificValidationService` via a common pure policy, not a fork.

**Failure:** `UNSUPPORTED_COMBINATION` for invalid user request (CLI exit2); Backend missing/incompatible distribution/API/optional import => typed unavailable/ENGINE (CLI exit4); no scientific negative or PASS inferred from capability response. Save effective Backend/version/API probe evidence in eventual Manifest via P05.

### 6.3. `DiscoveryPort` and selected-method dispatch (30_61 §5.5 / DISC01–03)

**Protocol Module:** `ariadne.scientific.ports.causal.DiscoveryPort`; no Protocol Instance Fields or direct Product DB/FS.

~~~python
def discover(self, request: ValidatedDiscoveryRequest, *, sink: StagingArtifactSink) -> DiscoveryGraphOutcome: ...
~~~

**Request module:** `ariadne.causal.discovery.contracts.ValidatedDiscoveryRequest` contains verified Study/Question/Design/Dataset, selected `BackendCapabilityRecord`, CI-test eligibility, seed and upstream digests. Construction requires validated Factory semantics; type name alone does not validate an arbitrary dict.

**Dispatch:** `LocalCausalUseCase -> MethodCapabilityPort.resolve -> DiscoveryPort.discover -> Registry.load_adapter(selectedCapability) -> FciDiscoveryAdapter.preflight -> FciDiscoveryAdapter.execute`. Verify loaded Adapter matches Method and Backend of the record exactly. No direct `ScientificCorePort.run_discovery(DiscoveryInput,Path)` because its old API writes paths; any shared pure kernel must be bridged without signature changes or second FCI implementation. No fallback to PC/GES.

**Outcome:** `ariadne.causal.discovery.contracts.DiscoveryGraphOutcome` is either immutable valid `GraphEvidence` (P03) or typed legitimate scientific Graph-negative with nonempty reasons. Technical Backend exception, malformed Graph, schema or input is a technical failure, **not** an alternate "negative scientific discovery." For G01 the only P01-accepted scientific-negative code is SCI_NO_ADMISSIBLE_PAG. Its meaning is a scientifically *proved* absence of any admissible PAG after otherwise eligible successful FCI and method-specific verification; no actual producer/proof is established currently. Do not emit this code without that verified scientific evidence. An empty-edge or uncertain PAG remains a valid Graph if its GraphEvidence validates. Backend/API/eligibility/BK errors are typed technical errors even if a caller attempts to relabel their string. Artifact output goes to `StagingArtifactSink` only; no write to final `runs/`.

### 6.4. `FciDiscoveryAdapter` exact signatures and Instance Fields (30_63 §1.3/4.4; METH-P106)

**Class/module:** `ariadne.scientific.causal_methods.discovery.FciDiscoveryAdapter`. Instance Fields: `method_descriptor: MethodDescriptor`, `backend_factory: BackendFactory`, `policy: ScientificEligibilityPolicy`. Validated per-run ScientificContext belongs to request, **not** reusable instance field.

~~~python
def __init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy): ...
def preflight(self, request: ValidatedDiscoveryRequest) -> CapabilityOrEligibilityResult: ...
def execute(self, request: ValidatedDiscoveryRequest, *, sink: StagingArtifactSink) -> DiscoveryGraphOutcome: ...
~~~

**Constructor:** descriptor must identify `P1-M06`/`DISCOVER`/`GRAPH_STRUCTURE` and approved Backend/Profile. No optional engine import, fit or artifact writing; wrong descriptor fails typed. Only this typed pair is public; do not also overload `ValidatedMethodRequest`.

**preflight sequence (zero FCI fit):**
1. Strict method config from `e11_p1_m06_fci_method_config_v1.schema.json`: `indep_test=fisherz/chisq/gsq`, `0<alpha<1`, `depth/max_path_length` integers -1 or >=0; BK null or directed required/forbidden pairs, no unknown keys.
2. Verified Question/Design/Dataset: ID and variable-order join (P01/P02), rows complete/finite, unique variable names and valid n/sample/independence assumptions; do **not** claim untestable Markov/faithfulness assumptions have been proven.
3. CI-specific admissibility: fisherz requires continuous complete numeric, nonconstant and documented Gaussian-assumption limitations; chisq/gsq require declared integer-coded categorical variables and sufficient category/conditioning support. Mixed types, missing values, constants, inadequate sample/support and incompatible CI -> typed reject. No silent imputation, binning or CI switch.
4. BK existence/order, self/contradictory required/forbidden pairs, permitted graph/time precedence. In pinned `causal-learn 0.1.4.8`, `FCI.py` `fci_orient_bk` (lines 267–293) runs for **any non-null BK including empty arrays**, prints unconditional messages independent of `verbose=false/show_progress=false`, and for forbidden edges uses `add_directed_edge`, which can create scientifically unsupported TAIL endpoints (upstream py-why/causal-learn#266 OPEN). **Fail closed before Backend call** with `BACKEND_SEMANTICS_UNVERIFIED` / capability-unavailable exit4 for non-null BK until **both** independent MAG/PAG motif preservation and exact `--json` stdout/log containment are real-tested; do not rewrite BK to null or fallback. Null BK remains candidate eligible after other preflight checks; no Backend fit PASS asserted.
5. Runtime Backend capability, installed `causal-learn` version and public API/accessor shape must be probed. Planned `0.1.4.8` from lock is a candidate only until actual import/distribution/API signature verified. If effective API differs -> `BACKEND_API_MISMATCH`; don't guess parameters or invoke alternate function.

**execute sequence (only after preflight eligible):**
1. Import selected FCI at selected Method load time only. Inspect actual signature against `causallearn.search.ConstraintBased.FCI.fci`, effective CI-test names, alpha/depth/max_path_length/BK and return shape; use real installed API, no undocumented positional guess.
2. Feed exact verified Dataset column ordering and declared config/seed; runtime records effective Backend/distribution/CI parameters, n, columns, randomness and result uncertainty; no unexpected conversion.
3. Graph node IDs: pinned `causal-learn 0.1.4.8` FCI exposes `node_names`; explicitly provide the **declared exact ordered Dataset variable names** and verify GraphNode/Edge 1:1 identity, not unverified `X1/X2` string replacement. Detect duplicate/unknown/out-of-order names or incompatible actual installed API as typed `BACKEND_GRAPH_NODE_MISMATCH` / `BACKEND_API_MISMATCH`. Tagged-source presence of `node_names` does not substitute actual Python3.12 import/fitted result.
4. Each Edge: node1↔endpoint1 and node2↔endpoint2 paired **positionally**; map TAIL/ARROW/CIRCLE, canonical sort only by simultaneous endpoint swap (P03). Reject self loops/duplicates/unknown marks, do not infer latent-confounder truth from bidirected appearance or circle mark. `kind=PAG`, `temporal=null`, `lag=null`, standalone Product `version_id/parent_version_id=null`.
5. Construct `GraphEvidence` through its strict Validator, semantic `content_hash` and external staged File bytes via `StagingArtifactSink`. Return typed Outcome; no Product GraphVersion write, dummy Effect or standalone Science PASS.


**DEC-G01-P04-CATEGORY-DOMAIN-01=A — declared categorical input authority (Owner-approved design decision; formal 09/S10/S11 pending).** The only P1-M06 Design schema for active dispatch is `e11_p1_m06_fci_design_profile_v1.schema.json`. Do not choose the older G01 Design draft as a fallback. Each `Design.variables[]` CATEGORICAL entry requires `category_codes` as complete ascending unique integer universe with at least two codes; CONTINUOUS forbids this field. Negative/noncontiguous integer codes are allowed; reject JSON numeric lexical variants `1.0`/`1e0`, bool, strings, null, unsorted/duplicate codes or values unrepresentable by the verified Dataset/Backend integer adapter. Schema's `type:integer` alone does not guarantee lexical exactness, so use strict token/semantic checks; never silently cast. Match Design names/positions and observed Dataset column values to the declared codes and keep unobserved declared levels (not `np.unique`). For every unordered X/Y and each conditioning subset S, iterate the **full declared** S-category Cartesian product, and every declared X/Y cell, including absent levels. Empty S strata, missing X/Y marginal, zero df, or E<5 rejects before FCI; incomplete enumeration/verification blocks before FCI and never emits SCI_NO_ADMISSIBLE_PAG. S=empty means one global table over all declared X/Y codes. A category-free previously valid Design must now fail G01/P1-M06 strict validation, while continuous Design stays structurally unchanged. The Design source is already verified via Study.inputs.design ContentRef; new bytes require new file SHA and Study JCS request_hash, and eventual Graph provenance source refs must match. No public E11 wire or completed P01/P03 source modification.

### DEC-G01-P04-CI-ELIG-01 — Owner adopted A: conservative exhaustive CI preflight (formal 09/S10/S11 pending)

For G01/P1-M06, before invoking the FCI backend, enumerate every unordered pair (X,Y) from the p ordered observed variables V and every S subset of V excluding X,Y, including the empty set and |S|=p-2. The required count is C(p,2)*2^(p-2). The FCI Possible-D-Sep stage in the pinned causal-learn 0.1.4.8 source may inspect conditioning sets beyond the user-configured adjacency-search depth; neither depth nor max_path_length may truncate this preflight. This screening is a deliberately conservative sufficient G01 policy, not a claim that FCI uses every triple.

- fisherz: require declared continuous complete finite, nonconstant numeric columns; for every triple require n > |S|+3 and a finite, positive-definite and reliably invertible empirical correlation submatrix over X,Y,S. Reject singular cases; if numerical reliability cannot be established, return unresolved/blocked rather than PASS. Gaussianity, independent observations and faithfulness are scientific assumptions, not proved by preflight. A numeric condition-number tolerance is not newly authorized.
- chisq and gsq: require exact integer-coded categorical values compatible with declared category domains; Backend implicit recoding does not validate them. For each triple and each declared conditioning category combination S=s, require positive stratum count, nondegenerate X-by-Y contingency table with positive degrees of freedom, and null-independence expected count E(x,y|s)=N(x,+|s)*N(+,y|s)/N(+,+|s) >= 5 for every declared X/Y cell. Empty/unsupported strata, a zero-degree table, or any expected count below 5 are ineligible. The adopted A proposal treats 5 as a conservative G01 screening floor, not a universal statistical validity guarantee.
- Exhaustive review must finish; absent verified resources, exhausted budget, unresolved category domain or unstable numerical matrix gives a typed eligibility-unresolved/technical block before FCI. Never truncate, skip difficult triples, silently switch CI, or label error SCI_NO_ADMISSIBLE_PAG. No new public wire/exit code is authorized. A fixed maximum-p/resource limit or numerical stability tolerance, if necessary for deterministic positive eligibility, remains a separate specification requiring justification.
- Log only non-row eligibility evidence: method/CI, p,n, total and examined triple counts, aggregate minimum expected count, typed reason and evaluation completeness; no raw observations, secret values or variable-name leakage in CLI JSON. Non-null BK remains pre-FCI rejected as separately agreed. Passing these screens is not FCI fit, independence-assumption verification, correct PAG, or independent science acceptance.

Independent tests must cover FisherZ n=|S|+3 (reject) and n=|S|+4 (only algebraically sufficient), singular/near-singular matrices, discrete E=5 versus E<5, fully supported and marginal-only-supported categorical tables, declared empty strata, depth=0 with possible larger FCI conditioning sets, wrong categorical codes, incomplete enumeration and zero Backend invocation on all preflight failures. Keep G01-07-09/10 and G01_999 obligations unchanged.

### 6.5. Independent GRAPH-A oracle, BK and latent negatives (07-08/09/10; METH-P106)

**Reference must not come from FCI output.** Test-owned small Graph fixtures with >=3 observed nodes and explicit latent/DGP where appropriate. Independently derive true DAG -> latent projection MAG -> Markov equivalence class PAG. Oracle enumerates compelled/uncertain endpoints; never treat all arrows in generating DAG as compelled PAG arrows. Assert adjacency and compelled endpoint agreement while preserving circle uncertainty.

**Negative test design:** 2 observed nodes with latent confounding cannot establish uniquely identified latent structure. Required/forbidden BK contradictions reject; a forbidden edge must not force an unjustified TAIL. Add the tagged 0.1.4.8 *non-null BK with empty arrays* stdout-contamination negative: FCI's unconditional `print` is reached despite fixed `verbose=false/show_progress=false`; preflight must deny this request before invocation and return only typed JSON control/status, no variable-name console leakage. Any identified upstream FCI semantic defect => typed `BACKEND_SEMANTICS_UNVERIFIED`, never patch library silently, drop constraints, or publish a falsely certain PAG. See `combined_review/175_20261122_g01_fci_0148_tagged_source_bk_stdout_preflight.md`.

**Distinguish 3 evidence types:** (A) **mechanical** serialization/PAG endpoint losslessness = 100% when defined (P03); (B) **deterministic science Oracle** matches independent MAG/PAG compelled edges (this Package); (C) **stochastic** Graph recovery performance in independently preregistered T2 Pilot→T3 with Owner DEC07 design. Tentative strong-signal adjacency precision/recall >=0.80, FPR <=0.10 are *pilot candidate* thresholds, not secretly final Hard AC. K, R, multiplicity, seed and compute budget become fixed before T3; never count Pilot replications in T3 sample. Missing Oracle/Environment/Hard AC -> science BLOCKED/INCONCLUSIVE, not PASS.

### 6.6. Error and upstream/downstream classification

| Source of error | Result | CLI/Publisher constraint |
| --- | --- | --- |
| Unsupported Method/Estimand/config | typed unsupported | exit2, no scientific run |
| Missing extra / API incompatible / engine exception | typed Backend error | exit4, no committed success |
| Malformed backend edge/node/endpoint | typed data/Backend semantic error | no false negative or valid PAG |
| Valid scientific negative (if Method proof exists) | Typed P04 scientific-negative, exact SCI_NO_ADMISSIBLE_PAG and validated scientific proof of no admissible PAG; **not** a missing/malformed Graph or technical error | P05 may publish only after authentic P04 provenance and diagnostics are verified; otherwise fail closed; no Science PASS |
| Valid Graph | typed `GraphEvidence` with provenance, dual hash | P05 stages via P02, independent Reader required |

G01 does not implement other 40 Methods, Product v2 GraphVersion edit, PCMCI or effect identification. Unregistered Method-specific Profile -> fail-closed.

## 7. Focused verification — contract/integration/scientific evidence

| DD / G01-07 | Primary proof layer | Required observable assertions |
| --- | --- | --- |
| CAP01/04/05, DISC01; 07-08 | contract + effective Backend integration | Env isolation, selected Method/Profile/Operation, no fallback, optional import lazy |
| METH-P106, DISC02/03; 07-08 | contract + effective Backend integration | fisherz/chisq/gsq positive eligibility and data/missing/constant/category/BK negatives; typed outcome |
| METH-P106, GRAPH01/03; 07-09 | deterministic independent Graph contract + actual Backend integration | independent DAG→MAG→PAG reference, compelled/uncertain endpoints, not backend self-oracle |
| METH-P106; 07-10 | contract + effective Backend integration | 2-node latent nonidentifiability, BK overorientation/contradiction refusal, no silent correction |
| T2/T3 science acceptance | independent quantitative scientific evaluation | preregistered cell/K/R/seed/compute; empirical data distinct from deterministic contract and Pilot distinct from T3 |

**Required Package check:** New G01 tests begin in enhancement lifecycle, with `contract` for deterministic scientific reference and `integration` for actual selected FCI/backend invocation. The separate reusable `characterization/benchmark` lifecycle is selected only by explicit decision; no `scientific` G01 layer directory is mandated. Current physical test paths/commands are resolved by 40 at execution, after existence and collection checks. Missing independent science or runtime evidence => individual Gate07 scientific cell BLOCKED; **T2/T3 performance execution does not block P04 coding checkpoint**, but cannot be reported PASS without actual independent evidence. Include real effective library/API and source/fixture/env SHA.

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

- [ ] `MethodCapabilityRegistry` Field/Constructor/`describe/resolve/load_adapter` and `BackendCapabilityRecord`/`MethodCapabilityPort.resolve` honor one Method authority, effective Backend/API evidence, lazy optional import and no fallback.
- [ ] `DiscoveryPort.discover`, `ValidatedDiscoveryRequest` and `FciDiscoveryAdapter.__init__/preflight/execute` have typed selected-Method dispatch, G01 CI/BK/Data admissibility, 1:1 Backend node/endpoint translation and staging-only output.
- [ ] Component-level actual `causal-learn` API/eligibility positive/negative tests run where the approved Backend is available. Unavailable runtime/API yields a typed BLOCKED/ENGINE result, not fabricated Backend availability.
- [ ] Independent GRAPH-A fixture/test harness specifies latent projection/MAG/PAG compelled/uncertain endpoints and BK/2-node negative cases, independently of FCI output; independent Graph-A Oracle contract cases and harness implemented, with current evidence honestly labeled.
- [ ] **T2 Pilot/T3 quantitative acceptance belongs to independent G01-07/999 on a fixed Trial Candidate SHA, not a precondition for P04 coding checkpoint.** If no scientific Oracle evidence exists, no Science PASS; record precise remaining BLOCKED cells.
- [ ] P04 focused component code/tests and checkpoint report (full source/fixture/env SHA) are complete; Product ScientificCorePort ABI unchanged, no hidden PC/other-Method fallback.

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
