# ENH-E11 G01 P04 — FCI Capability, Eligibility, Independent Graph Oracle

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
他GateのMethod実装、旧Product v2変更、根拠なしのScience PASS、行出力自己許可、未承認ACL/mount、既存run上書き、Package外の便乗変更。

## 5. Entry criteria / required evidence
Gate 06/07のFreeze・Coding Authorization・固定branch HEAD確認。Depends on P01,P03の実装checkpoint full SHAとfocused検証を確認。矛盾/依存未成立はBLOCKED。

dependency checkpoint / source state等はfactとして外部参照してよい。Entry rule自体は本書内に記載する。

## 6. Required implementation — capability, FCI and science evidence

### 6.1. `MethodCapabilityRegistry` (30_62 §2 / CAP01,04,05)

**Class/module:** `ariadne.capabilities.causal.method_registry.MethodCapabilityRegistry`. Immutable Constructor fields:

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

**Record module:** `ariadne.scientific.capabilities.BackendCapabilityRecord`. Immutable fields `method_id`, `backend_id`, `distribution_version`, `adapter_version`, `api_signature_hash`, `extra`, `profile`, `available` and `reason`. Construct from *effective observed* versions/probes; no fake defaults. Method `check(self, request: ValidatedCapabilityRequest) -> typed compatibility decision`; pure request-vs-capability assertion.

**Public Port:** `ariadne.scientific.ports.capability.MethodCapabilityPort.resolve(request: ValidatedCapabilityRequest) -> BackendCapabilityRecord`. Request includes Operation, Estimand, Design, Backend, profile and Inference constraints. Facade validates **all** and only then delegates to concrete `MethodCapabilityRegistry.resolve(method_id, backend_id, profile)`; do not pass a bare triple in lieu of a validated request. Same registry metadata and compatibility policy used by legacy `ScientificValidationService` via a common pure policy, not a fork.

**Failure:** `UNSUPPORTED_COMBINATION` for invalid user request (CLI exit2); Backend missing/incompatible distribution/API/optional import => typed unavailable/ENGINE (CLI exit4); no scientific negative or PASS inferred from capability response. Save effective Backend/version/API probe evidence in eventual Manifest via P05.

### 6.3. `DiscoveryPort` and selected-method dispatch (30_61 §5.5 / DISC01–03)

**Protocol module:** `ariadne.scientific.ports.causal.DiscoveryPort`; no Protocol Instance Fields or direct Product DB/FS.

~~~python
def discover(self, request: ValidatedDiscoveryRequest, *, sink: StagingArtifactSink) -> DiscoveryGraphOutcome: ...
~~~

**Request module:** `ariadne.causal.discovery.contracts.ValidatedDiscoveryRequest` contains verified Study/Question/Design/Dataset, selected `BackendCapabilityRecord`, CI-test eligibility, seed and upstream digests. Construction requires validated Factory semantics; type name alone does not validate an arbitrary dict.

**Dispatch:** `LocalCausalUseCase -> MethodCapabilityPort.resolve -> DiscoveryPort.discover -> Registry.load_adapter(selectedCapability) -> FciDiscoveryAdapter.preflight -> FciDiscoveryAdapter.execute`. Verify loaded Adapter matches Method and Backend of the record exactly. No direct `ScientificCorePort.run_discovery(DiscoveryInput,Path)` because its old API writes paths; any shared pure kernel must be bridged without signature changes or second FCI implementation. No fallback to PC/GES.

**Outcome:** `ariadne.causal.discovery.contracts.DiscoveryGraphOutcome` is either immutable valid `GraphEvidence` (P03) or typed legitimate scientific Graph-negative with nonempty reasons. Technical Backend exception, malformed Graph, schema or input is a technical failure, **not** an alternate "negative scientific discovery." Artifact output goes to `StagingArtifactSink` only; no write to final `runs/`.

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
4. BK existence/order, self/contradictory required/forbidden pairs, permitted graph/time precedence; if BK semantics may over-orient endpoints without independent motif regression -> `BACKEND_SEMANTICS_UNVERIFIED` and do not publish. `show_progress=false`, `verbose=false` are adapter-fixed, not user-config defaults.
5. Runtime Backend capability, installed `causal-learn` version and public API/accessor shape must be probed. Planned `0.1.4.8` from lock is a candidate only until actual import/distribution/API signature verified. If effective API differs -> `BACKEND_API_MISMATCH`; don't guess parameters or invoke alternate function.

**execute sequence (only after preflight eligible):**
1. Import selected FCI at selected Method load time only. Inspect actual signature against `causallearn.search.ConstraintBased.FCI.fci`, effective CI-test names, alpha/depth/max_path_length/BK and return shape; use real installed API, no undocumented positional guess.
2. Feed exact verified Dataset column ordering and declared config/seed; runtime records effective Backend/distribution/CI parameters, n, columns, randomness and result uncertainty; no unexpected conversion.
3. Graph node IDs: map actual Backend nodes to Dataset columns 1:1 by validated mapping; `X1/X2` or internal Node objects are not untrusted identities to string-replace. Unknown node, duplicate, ambiguous column mapping -> `BACKEND_GRAPH_NODE_MISMATCH`.
4. Each Edge: node1↔endpoint1 and node2↔endpoint2 paired **positionally**; map TAIL/ARROW/CIRCLE, canonical sort only by simultaneous endpoint swap (P03). Reject self loops/duplicates/unknown marks, do not infer latent-confounder truth from bidirected appearance or circle mark. `kind=PAG`, `temporal=null`, `lag=null`, standalone Product `version_id/parent_version_id=null`.
5. Construct `GraphEvidence` through its strict Validator, semantic `content_hash` and external staged File bytes via `StagingArtifactSink`. Return typed Outcome; no Product GraphVersion write, dummy Effect or standalone Science PASS.

### 6.5. Independent GRAPH-A oracle, BK and latent negatives (07-08/09/10; METH-P106)

**Reference must not come from FCI output.** Test-owned small Graph fixtures with >=3 observed nodes and explicit latent/DGP where appropriate. Independently derive true DAG -> latent projection MAG -> Markov equivalence class PAG. Oracle enumerates compelled/uncertain endpoints; never treat all arrows in generating DAG as compelled PAG arrows. Assert adjacency and compelled endpoint agreement while preserving circle uncertainty.

**Negative test design:** 2 observed nodes with latent confounding cannot establish uniquely identified latent structure from observational data; no latent "proven" label. Required/forbidden BK contradictions reject; forbidden edge must not result in unjustified TAIL certainty. Any identified upstream library semantic defect => typed BACKEND_SEMANTICS_UNVERIFIED, never patch library silently or publish as PASS.

**Distinguish 3 evidence types:** (A) **mechanical** serialization/PAG endpoint losslessness = 100% when defined (P03); (B) **deterministic science Oracle** matches independent MAG/PAG compelled edges (this Package); (C) **stochastic** Graph recovery performance in independently preregistered T2 Pilot→T3 with Owner DEC07 design. Tentative strong-signal adjacency precision/recall >=0.80, FPR <=0.10 are *pilot candidate* thresholds, not secretly final Hard AC. K, R, multiplicity, seed and compute budget become fixed before T3; never count Pilot replications in T3 sample. Missing Oracle/Environment/Hard AC -> science BLOCKED/INCONCLUSIVE, not PASS.

### 6.6. Error and upstream/downstream classification

| Source of error | Result | CLI/Publisher constraint |
| --- | --- | --- |
| Unsupported Method/Estimand/config | typed unsupported | exit2, no scientific run |
| Missing extra / API incompatible / engine exception | typed Backend error | exit4, no committed success |
| Malformed backend edge/node/endpoint | typed data/Backend semantic error | no false negative or valid PAG |
| Valid scientific negative | `DiscoveryGraphOutcome` with reason and no Graph | P05 may publish diagnostics/status via P02; not Science PASS |
| Valid Graph | typed `GraphEvidence` with provenance, dual hash | P05 stages via P02, independent Reader required |

G01 does not implement other 40 Methods, Product v2 GraphVersion edit, PCMCI or effect identification. Unregistered Method-specific Profile -> fail-closed.

## 7. Focused verification — tests and science evidence

| DD / G01-07 | Focused file / method | Assertion |
| --- | --- | --- |
| CAP01/04/05, DISC01; 07-08 | `component/test_g01_fci_method.py` | ENV-BASE missing extra isolated; correct Method/Profile/Operation; no fallback and lazy import |
| METH-P106, DISC02/03; 07-08 | same file | fisherz/chisq/gsq positive eligibility and missing/constant/ordinal/category support/BK negatives; selected Graph vs typed negative |
| METH-P106, GRAPH01/03; 07-09 | `scientific/test_g01_fci_graph_oracle.py` | independent MAG/PAG reference, not backend-derived expected, compelled/uncertain edge matches |
| METH-P106; 07-10 | same scientific file | 2-node latent no unique claim, BK overorientation/contradiction reject, no silent override |

~~~bash
uv run --no-sync python -m pytest tests/enhancement/enh_e11/g01/component/test_g01_fci_method.py -q
uv run --no-sync python -m pytest tests/enhancement/enh_e11/g01/scientific/test_g01_fci_graph_oracle.py -q
~~~

If independent Oracle/T2/T3 cannot yet execute, record explicit `BLOCKED` at relevant DD/test cells; pure component checks may still complete **without falsely claiming science PASS**. All evidence includes effective distribution/API, source/fixture SHA, observed graph/CI values, seed and whether reference is independent. Scientific independent Gate verification remains 07/999, not self-certified in P04.

## 8. Protected contract / Transition Debt constraints
Product v2の既存CLI/Manifest/Result contractを回帰保護する。未完成のGraph/Science/個票認可を完成と見なさない。PREPARATION-03の技術判定はG01単一Gate維持（Owner承認待ち）。P02のOS/FS Publication、P04の独立FCI/PAG Science、P05のCLI統合・Privacy/旧v2回帰は別々の必須受入軸であり、全軸が同じFixed Candidate SHAで実証されるまでG01_999 PASS不可。OwnerのGate境界承認・06/07 Freeze/Coding AuthorizationまではPxx着手禁止。

## 9. Checkpoint / reporting rule

Package completion時:

1. implementation-affecting changeをcommitする。
2. implementation checkpoint full SHAを固定する。
3. `implementation_checkpoint_report`を作成する。
4. `*_in_progress.md`へexecution statusを記録する。
5. report-only commitが別ならcheckpoint SHAと区別する。

## 10. Package completion criteria
Backend API/CI/BK invalid inputが拒否され、独立Oracle未完ならScience BLOCKEDを維持する。 集中検証の証跡・実装checkpoint SHA・Package Reportを揃える。未検証はBLOCKEDで止める。

## 11. External reference policy

source / previous checkpoint / test output / provenanceは外部参照してよい。本書のimplementation rule、prohibited scope、completion criterionをParent 06 / P00へ委譲してはならない。

## 12. Stop rule

- package scope完了 -> `PACKAGE_COMPLETE`
- continuation不能 -> `PACKAGE_BLOCKED`
- Gate PASS / FAILは判定しない。
- next packageへ勝手に先行しない。
