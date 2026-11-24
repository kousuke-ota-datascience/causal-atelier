# ENH-E11 G01 P01 — Local Study, ContentRef, Canonical Codec

**DEC-G01-EXEC-01（Owner 2026-11-23採用・G01のみの実施順序変更）:** `combined_review/177_20261123_dec_g01_exec01_owner_adopted_evidence_rephasing.md`がG01の従前S09→S10→S11依存を部分的に上書きする。利用不能なPython3.12実測B02/B04、独立S09/B05科学審査は**Coding Entryの必要条件から外し、G01_999 PASSまでの必須受入条件へ移す**。事前Author契約整合と例外Ledgerを材料に、Ownerの**別個の暫定G01-S10 Freeze**、その後Ownerの**別個の限定G01-S11 Coding Authorization**を認める。どちらも現在**未承認**。限定許可はG01/P01–P05の実装・開発者テストのみ。実Python3.12 Schema/FCI、独立MAG/PAG/BK、実FS/Reader、T2/T3、独立07/999、Product v2回帰の要求・合格基準は維持。未検証をPASS扱いせず、non-null BKはFCI呼出前exit4 fail-closed、科学的真値や閾値の自己創作禁止。G01_999がPASSするまで下流Gate依存は解除しない。

**Document class:** Primary Execution Contract  
**Self-containment:** MUST — Assigned Coding Agentが本書だけでpackageのnormative execution responsibilityを理解できること。

- Gate: G01
- Trial: Trial01（未開始）
- Package: P01
- Parent 06 (traceability): 06_Ariadne_ENH-E11_G01_implementation_instruction.md
- P00 Plan (traceability): 06_G01_P00_work_package_plan.md
- Depends on: NONE
- Status at issuance: DRAFT / CODING_NOT_AUTHORIZED

## 1. Purpose
strict Study/ContentRef、Question/Design/Method Profile、Canonical JCSとManifest Valueを定義する。

## 2. Effective Gate constraints applicable to this package

このpackageが守るべきGate-level semanticsを、Parent 06 / P00を読まなくても実行判断できる粒度で記載する。

G01は正式Gate IDでPxxはbounded Coding Unit。Local laneとProduct v2を分離し旧CLI/Web/API/DB/Workerは改変しない。strict version/Method/EstimatorとJCSのハッシュ対象を検証し、PAGをDAG/ATEへ変換しない。OS root/Privacy/Atomic Publishの不適格はfail-closed、SCI不確実性をPASSに変換しない。Coding Authorization前の実装は禁止。

## 3. In scope — implementation ownership

| Class/module | Owned scope | Explicit boundary |
| --- | --- | --- |
| `ariadne.shared.content_ref.ContentRef` | 5-field immutable Ref; strict `from_payload` | Actual filesystem validation belongs to P02 |
| `ariadne.interfaces.cli.local_causal.study.LocalStudySpec` | E11 transport DTO and invariant validation | No separate scientific Domain |
| `ariadne.interfaces.cli.local_causal.config_decoder.LocalConfigDecoder` | strict YAML/JSON -> validated request | No unverified file access in pure parser |
| `ariadne.causal.design.study.ValidatedStudy` / `ariadne.causal.inference.contracts.EstimandRef` | Common validated scientific Target, including GRAPH_STRUCTURE | Existing Product ATE/ATT Enum unchanged |
| `ariadne.shared.serialization.jcs` | Strict RFC8785 JCS bytes/digest | Projection-specific Graph digest owned by P03 |
| `ariadne.interfaces.cli.local_causal.manifest.LocalRunManifest` / `ValidatedRunEvidence` / `ArtifactDescriptor` / `RuntimeEvidence` | Pure wire DTO, immutable typed evidence envelope, `from_payload/from_run_evidence/validate_invariants/to_canonical_bytes`; no I/O | P02 stages/reads exact bytes, P03 validates Graph meaning, P05 supplies verified input and cross-asset runtime facts |

The Package produces typed values, verified **schema** and canonical bytes; it does not claim verified physical input, Product GraphVersion ownership or independent Graph science.

## 4. Explicitly out of scope
他GateのMethod実装、旧Product v2変更、根拠なしのScience PASS、行出力自己許可、不適格なowner/mode/local FS、既存run上書き、Package外の便乗変更。

## 5. Entry criteria / required evidence
Gate 06/07のFreeze・Coding Authorization・固定branch HEAD確認。P01に先行する実装Packageは存在しないので依存Checkpointは不要。矛盾/依存未成立はBLOCKED。

dependency checkpoint / source state等はfactとして外部参照してよい。Entry rule自体は本書内に記載する。

## 6. Required implementation — executable Class contracts

### 6.1. `ContentRef` — 30_60 §11 / REF01–04

**Class/Module:** `ariadne.shared.content_ref.ContentRef`; immutable value. Fields and no implicit defaults:

| Field | Type | Invariant |
| --- | --- | --- |
| `identity` | `str` | nonempty logical identity |
| `relative_key` | `str` | relative safe POSIX key |
| `sha256` | `str` | lowercase hex SHA256 / 64 digits |
| `media_type` | `str` | nonempty explicit MIME |
| `schema_version` | `str\|None` | key required, may be null |

**Constructor/Factory:** Public ingress is `from_payload(payload: Mapping[str,JsonValue]) -> ContentRef`; frozen value construction cannot bypass schema/lexical validation. No mutable input references are retained. Exactly five fields, no unknown/missing; reject bad types, dot/dotdot, leading slash, Windows drive/UNC, backslash, empty components, NUL and unsafe Unicode/path grammar. Copy into immutable fields; do not retain user-provided mutable mapping.

**Pre/Post:** never open a file or assert content authenticity. A syntactically valid SHA string is not hash verification; `ContentReferencePort.verify(ref,*,root)` in P02 performs FD-bound actual-byte/hash validation. Errors are typed schema/path violations, not successful Ref with warning. No retry or I/O side effects.

### 6.2. `LocalStudySpec` / `ValidatedStudy` — 30_60 §12 / SPEC01–04

**Module/Class:** `ariadne.interfaces.cli.local_causal.study.LocalStudySpec`; immutable CLI envelope. Fields: `schema_version:Literal["e11-local-study/1"]`, `run_id:str`, `operation:LocalOperation`, `analysis_mode:AnalysisMode`, `question/design/dataset:ContentRef`, `graph/identification:ContentRef|None`, `estimand:EstimandRef`, `method:MethodRequest`, `inference:InferenceRequest`, `randomness:RandomnessSpec`, `privacy:LocalPrivacySpec`.

**Constructor/Factory:** Immutable LocalStudySpec is constructed only after strict Study DTO decoding, with all declared fields set. **Method:** `validate_local_invariants(self) -> tuple[Reason,...]`, pure; check version, safe run_id, required/ref-null rules, Operation/Estimand and Privacy intent. DTO construction alone is not `ValidatedStudy` proof. Convert using common scientific validator; Application cannot import this CLI DTO. Existing `CausalDesign.Estimand` supports ATE/ATT only: do not force the non-Effect GRAPH_STRUCTURE Target into it.

**G01 accepted subset:** `operation=DISCOVER`, `analysis_mode=EXPLORATORY`, required Question/Design/Dataset; `inputs.graph=null` and `inputs.identification=null`. `estimand={family:GRAPH_STRUCTURE,population:OBSERVED_VARIABLES,contrast:NOT_APPLICABLE}`; `inference={requested:false,confidence_level:null}`; `privacy={classification:AGGREGATE,row_export_requested:false}`. Row request is a denial in P05 (exit3); malformed structural combination is exit2. Never fabricate ATE, Effect Result, Identification or Science PASS.

### 6.3. `LocalConfigDecoder` — 30_60 §9 / SPEC01–04

**Port/Module:** `ariadne.interfaces.cli.local_causal.config_decoder.LocalConfigDecoder`. Protocol has no mutable per-run fields. Concrete can receive immutable schema registry and Method profile selection at composition time. No optional scientific-engine import.

~~~python
def decode(self, raw: bytes, *, declared_format: Literal["yaml","json"]) -> ValidatedStudy: ...
# private concrete helper, not a second public Port:
def decode_yaml(raw: bytes) -> LocalStudySpec: ...
~~~

**Required processing order:**
1. Select only declared YAML/JSON; reject unknown format, duplicate mapping keys, unsafe YAML object tags, excessive alias/nesting, invalid JSON numbers.
2. Validate explicit `e11-local-study/1` against `e11_local_study_v1.schema.json`, no legacy/versionless fallback; nested ContentRefs use 6.1.
3. Construct `LocalStudySpec`, call `validate_local_invariants`, and dispatch exactly (`DISCOVER`, `P1-M06`, `causal-learn`) to the P1-M06 Method config schema. All other G01 Operation/Method combos rejected, not routed to a different Method.
4. Validate Method config: five required keys `indep_test` (`fisherz/chisq/gsq`), `alpha` within (0,1), `depth` and `max_path_length` -1 or nonnegative int, `background_knowledge` null or typed required/forbidden pairs; unknown fields rejected. Do not silently substitute backend defaults.
5. Construct `ariadne.causal.design.study.ValidatedStudy` using shared scientific invariants and an explicit non-Effect `EstimandRef`. Pure parser must **not claim to have read** Question/Design/Dataset external files.

**Cross-asset validation obligation (delegated to P02/P05 after actual bytes verification):** Apply P1-M06 Question and Design JSON profiles on verified reference bytes. Require `question.question_id=design.question_id=Study.inputs.question.identity`; `design.variables[].name` equals Dataset column names *and ordering*; `design.background_knowledge` JCS-equal `Study.method.config.background_knowledge`. Fisherz requires all CONTINUOUS; chisq/gsq all CATEGORICAL and integer-encoded finite support. Do not auto-discretize/impute/standardize. Schema errors -> CLI 2, bad input bytes/root/hash -> CLI 3, unavailable backend -> CLI 4.

### 6.4. `ariadne.shared.serialization.jcs` — strict Codec / MAN01–03 / GRAPH01

Implement versioned deterministic `e11-json-jcs-rfc8785/1` canonicalization. Input is JSON semantics, not Python arbitrary objects. Reject NaN, ±Infinity, duplicate JSON keys, unpaired surrogates and unsupported non-JSON values. Match RFC8785 number representation, Unicode string handling and UTF-16 property sort. Never call Product `hash_mapping(default=str)` as a substitute.

**Different SHA256 domains remain distinct:**

| Digest | Bytes |
| --- | --- |
| `request_hash` | JCS of typed validated Study |
| `Graph.content_hash` | JCS of Graph meaning projection **excluding** `content_hash` (projection defined P03) |
| `ContentRef.sha256` | Exact completed artifact file bytes (P02) |
| `marker.manifest_sha256` | Exact completed `manifest.json` bytes (P02) |

Run the repository's `e11_jcs_golden_vectors.json` (7 positive/7 negative) against independently sourced, pre-registered RFC8785 expected byte vectors. No external ECMAScript runtime or cross-language parity execution is required. Self-generated expected fixtures are NOT independent references. No UTF normalization that changes the supplied code points.

### 6.5. `LocalRunManifest` / `ValidatedRunEvidence` — 30_62 §4 / MAN01–06

**Module/Class:** `ariadne.interfaces.cli.local_causal.manifest.LocalRunManifest`; immutable DTO using precisely `e11_local_manifest_v1.schema.json` public wire keys. **P01 also owns the immutable pure values** `ValidatedRunEvidence`, `RuntimeEvidence`, and `ArtifactDescriptor` in this module or a private P01-owned helper. These are *internal* Python values, not new public E11 JSON versions. No dependency on P02/P03/P04/P05 concrete classes is allowed.

#### 6.5.1. Exact factory input contract (normative; no unspecified upstream type)

```python
@dataclass(frozen=True)
class ArtifactDescriptor:
    key: str
    sha256: str
    size_bytes: int
    media_type: str
    privacy_class: Literal["AGGREGATE", "RESTRICTED_ROW_LEVEL"]
    visibility: Literal["PRIVATE", "RESTRICTED"]

@dataclass(frozen=True)
class RuntimeEvidence:
    repo_commit: str
    dirty: bool
    python_version: str
    platform: str
    uv_lock_sha256: str
    distributions: Mapping[str, JsonValue]
    api_probes: Mapping[str, JsonValue]

@dataclass(frozen=True)
class ValidatedRunEvidence:
    study: ValidatedStudy
    study_payload: Mapping[str, JsonValue]
    status_payload: Mapping[str, JsonValue]
    runtime: RuntimeEvidence
    stochastic: Mapping[str, JsonValue]
    artifact_descriptors: tuple[ArtifactDescriptor, ...]
    output_graph_ref: ContentRef | None
    graph_negative_reason_codes: tuple[str, ...]
    review_science_evidence_ref: ContentRef | None

class LocalRunManifest:
    @classmethod
    def from_payload(cls, payload: Mapping[str, JsonValue]) -> LocalRunManifest: ...
    @classmethod
    def from_run_evidence(cls, evidence: ValidatedRunEvidence) -> LocalRunManifest: ...
    def validate_invariants(self) -> tuple[Reason, ...]: ...
    def to_canonical_bytes(self) -> bytes: ...
```

#### 6.5.1a. Closed G01 scientific Graph-negative reason vocabulary — normative

**The P01 factory MUST NOT classify an arbitrary nonempty string tuple as scientific.** For G01 DISCOVER/P1-M06 the complete allowed science-negative code set is exactly one member:

~~~python
G01_GRAPH_NEGATIVE_SCIENCE_CODES = frozenset({"SCI_NO_ADMISSIBLE_PAG"})
~~~

**Exact pure acceptance boundary:** For a Graph-negative candidate, graph_negative_reason_codes must be a real tuple exactly ("SCI_NO_ADMISSIBLE_PAG",) and status_payload.reason_codes a JSON list exactly ["SCI_NO_ADMISSIBLE_PAG"]. No extra, missing, duplicate or mixed codes, aliases, case variations or unknown SCI_* values. Additionally require the usual negative-only artifact inventory (study.json, status.json, diagnostics.json), no graph ref, Status technical_status=COMPLETED, fixed G01 science axes, and null independent review ref. For a Graph-positive candidate require graph_negative_reason_codes == () and status_payload.reason_codes == [] exactly.

**Negative rejection is mandatory even when both inputs agree:** ("BACKEND_API_MISMATCH",) and ["BACKEND_API_MISMATCH"] MUST be rejected as SCHEMA_INVALID. So must BACKEND_SEMANTICS_UNVERIFIED, CAPABILITY_UNAVAILABLE, EXECUTION_FAILED, PUBLICATION_FAILED, SCHEMA_INVALID, HASH_INVALID, any unlisted SCI_* string, a mix containing an allowed and disallowed code, duplicate codes, or a Graph-positive candidate with a nonempty Status reason list. These are candidate-contract classification violations, never scientifically justified negative results.

**Scientific meaning and proof boundary:** SCI_NO_ADMISSIBLE_PAG is a *reserved* declaration that after an otherwise eligible, successfully executed and scientifically checked method there is demonstrably no admissible PAG under the declared scientific constraints. Its presence does NOT prove that this state occurs for causal-learn FCI. No actual G01 scientific case or independent reference proving such a result is currently established. In particular, malformed/missing Backend Graph, ineligible Dataset, unsupported or inconsistent BK, API/import/runtime failure, insufficient data, low power, uncertain PAG endpoints, and a valid empty-edge PAG do NOT satisfy this code. An empty-edge or uncertain PAG, if valid, is Graph-positive.

P01 validates this closed value vocabulary and typed fields *only*, not scientific truth or unforgeable P04 provenance. P04 may emit the scientific-negative variant only after a genuine method-specific scientific proof; absent that proof it must fail closed and not manufacture a negative. P05 independently validates the **actual P04 discriminated outcome** and supporting diagnostics before creating a candidate. If P04 actually failed, P05 must preserve the typed technical failure even when somebody relabeled its reason text as SCI_NO_ADMISSIBLE_PAG. P02/Reader independently verifies real bytes. A synthetic P01 negative fixture is permitted for pure structural tests, never evidence that a real science-negative producer is working.

- `study_payload` is the **validated typed E11 Study wire projection** of `study`, including exactly its full `schema_version/run_id/operation/analysis_mode/inputs/estimand/method/inference/randomness/privacy` fields. It is not arbitrary raw user YAML or an unverified replacement Study. P01 must check exact semantic equality of this projection and `ValidatedStudy`, including Method config and all five-field ContentRefs; a discrepancy is `SCHEMA_INVALID`. Compute `request_hash=SHA256(JCS(study_payload))` with §6.4; P05 writes `study.json` from precisely this validated projection. Do not hash an alternate serialization, inject a hash without checking, or treat a lexical ContentRef as physically verified.
- `status_payload` is a strict, immutable `e11-local-status/1` snapshot that P05 serializes as `status.json`; it must contain `schema_version/run_id/technical_status/identification_status/point_availability/inference_availability/science_acceptance/reason_codes/manifest_relative_path`. Reject missing/extra keys, invalid enum/types or a different run. For a *candidate successful G01 publication*, `technical_status=COMPLETED` in the prepared file and Manifest and `manifest_relative_path="runs/{run_id}/manifest.json"` for the same safe run_id; a null or different path cannot describe a publishable candidate. These fields are **candidate assertions, not evidence of publication**. P02 must withhold an externally returned `COMPLETED` outcome until committed independent Reader verification; failed publication never returns a successful run.
- `runtime` is the exact required wire runtime group: `repo_commit` (nonempty actual commit), `dirty` (bool), `python_version` (nonempty), `platform` (nonempty), `uv_lock_sha256` (lowercase 64-hex **byte** digest), `distributions` and `api_probes` (JSON objects). P05 supplies effective measurements; the pure factory checks schema only, does not import a Backend, perform a probe, or synthesize values. `stochastic` is a JSON-object snapshot of actual seed/stream/split/fold information when applicable, with no invented default. All mutable mappings/lists must be deep-copied into immutable internal values; do not keep external mutable aliases.
- `artifact_descriptors` are immutable descriptors returned by P02's staging `stage_bytes` from **the exact bytes already written**; P05 passes these to the P01 factory. P01 can validate their types, hash grammar and logical joins but cannot prove FD/path/bytes authenticity, owner/mode/atomicity or Reader success. P02 rechecks all physical facts independently. `ArtifactDescriptor` has **only** the six public schema keys above; do **not** add an `upstream_ref` or invent a new wire format.
- `output_graph_ref` is the generated output Graph's five-field `ContentRef`, supplied by P05 from the P03-validated Graph identity **and P02's actual staged `graph.json` descriptor**. Its `relative_key` names the prospective final `runs/{run_id}/graph.json` **relative to `TrustedLocalRoot`**, while the staged ArtifactDescriptor `key` is `graph.json` relative to the bundle root. P01 checks the exact path projection and bytes SHA without trying to open an uncommitted output; P02 opens staged bytes before commit and the final TrustedRoot-relative Ref **only after publication** via Reader. For G01 it is **not** the Study's input `inputs.graph`, which remains null. `graph_negative_reason_codes` is restricted to the exact closed singleton negative tuple in §6.5.1a (or () for Graph-positive), never arbitrary Backend/schema/I/O codes; P05 provides it from a typed negative. `review_science_evidence_ref` must be null in G01: run execution cannot self-approve independent science.
- The factory checks every field and does not trust the name `ValidatedRunEvidence` as proof of validity. Invalid shapes or cross-refs raise typed `SCHEMA_INVALID`/`HASH_INVALID`/`PRIVACY_POLICY_CONFLICT` with phase and reason. No disk I/O, mutable output, warning-only acceptance or silent defaulting.

#### 6.5.2. Deterministic public Manifest projection

The pure factory emits **only** these top-level wire keys, with the following origins:

| Wire key | Required value / provenance |
| --- | --- |
| `manifest_version` | `e11-local-manifest/1` |
| `run_id`, `operation`, `request_hash` | `study_payload.run_id`, `DISCOVER`, `SHA256(JCS(study_payload))` |
| `schema_dispatch` | `study="e11-local-study/1"`, `status="e11-local-status/1"`, `result=null`, `graph="e11-local-graph/1"` for positive or null for scientific-negative |
| `lineage` | `question/design/dataset` = exactly `study_payload.inputs.question/design/dataset`; `graph` = generated `output_graph_ref` for positive, null for negative; `identification=null`. All nonnull refs use exact five-field ContentRef wire form |
| `estimand` | Exact `study_payload.estimand`; G01 requires GRAPH_STRUCTURE / OBSERVED_VARIABLES / NOT_APPLICABLE |
| `execution` | `technical_status=status_payload.technical_status`, `analysis_mode=study_payload.analysis_mode`, `method=study_payload.method.id`, `backend=study_payload.method.backend`, `inference_config=study_payload.inference`; `scientific_axes` mirrors status identification/point/inference/science values without asserting independent approval |
| `runtime`, `stochastic` | Exact strictly typed supplied effective `runtime` and `stochastic` snapshots, never synthetic |
| `artifacts` | The supplied staged descriptors, keyed uniquely and ordered deterministically by ascending `key` in serialized arrays |
| `review` | `{"science_evidence_ref":null}` for G01, never a fabricated PASS |
| `canonical_codec_version` | `e11-json-jcs-rfc8785/1` |

`from_payload` independently validates this exact versioned public shape and rejects unknown keys, invalid operation-specific inventory, invalid Manifest-local reference forms, privacy/status invariants expressible in Manifest, and an output Graph Ref-to-descriptor mismatch. **It cannot recompute `request_hash` from Study or compare Status reason codes because neither external Study nor Status bytes are arguments to `from_payload`; those cross-file checks MUST occur in P02 Reader/P05 after actual file decode.** `from_run_evidence` MUST check the fuller Study↔Status↔Manifest value joins using its explicit typed evidence. `to_canonical_bytes` runs strict §6.4 JCS on the public projection; the Manifest contains neither its own SHA nor marker data. No Product v2 `CliManifest` reinterpretation.

#### 6.5.3. Exact G01 upstream-ref joins and bundle acceptance matrix

`upstream ref join` **means the following explicit pure equalities**, not a seventh ArtifactDescriptor field. Perform all checks before returning from either factory insofar as fields exist in the supplied Manifest/evidence. **Physical bytes and cross-file contents remain P02/P05/Reader checks**.

| Check | P01 pure rejection rule | Downstream independent recheck |
| --- | --- | --- |
| Study identity | `study_payload.run_id = status_payload.run_id = manifest.run_id`; `study_payload.operation=manifest.operation=DISCOVER`; recomputed `request_hash` matches Manifest | P02 Reader reopens Study/Status file bytes and checks both against Manifest and marker |
| Input refs | Each of `manifest.lineage.question/design/dataset` is **all-five-fields equal** to the corresponding `study_payload.inputs` ref; `study_payload.inputs.graph/identification` both null in G01 | P05 verifies physical input references via ContentReferencePort; Reader rechecks same root/hash |
| Method / estimand | `manifest.execution.method=study_payload.method.id="P1-M06"`, `backend=study_payload.method.backend="causal-learn"`, `analysis_mode="EXPLORATORY"`, `estimand=study_payload.estimand`, no requested inference | P05 compares verified Question/Design/Dataset, Method profile and effective Adapter; P02 Reader checks written files |
| Status axes | Manifest `execution.technical_status` equals Status `technical_status=COMPLETED` for candidate, and Status `manifest_relative_path` is exactly `runs/{run_id}/manifest.json`; `identification_status=NOT_APPLICABLE`, `point_availability=NOT_REQUESTED`, `inference_availability=NOT_REQUESTED`, `science_acceptance=NOT_EVALUATED` | Reader verifies **actual** status.json bytes and only then grants published status |
| Graph-positive | Exactly `study.json`, `status.json`, `graph.json` (not Manifest/Marker); `output_graph_ref` nonnull, `graph_negative_reason_codes=()` and `status_payload.reason_codes==[]`; `lineage.graph` exactly this ref; its `relative_key="runs/{run_id}/graph.json"` is a **TrustedRoot-relative final published location** and corresponds by stripping the exact `runs/{run_id}/` prefix to the bundle-root descriptor `key="graph.json"`; its `sha256` and `media_type` match that staged descriptor; `schema_version="e11-local-graph/1"`; dispatch graph version set | P03 validates Graph semantic hash/endpoints/provenance; P05/Reader check Graph file's actual content and its source refs |
| Scientific Graph-negative | Exactly `study.json`, `status.json`, `diagnostics.json`; `output_graph_ref=null`, `lineage.graph=null`, `schema_dispatch.graph=null`, `graph_negative_reason_codes == ("SCI_NO_ADMISSIBLE_PAG",)` and `status_payload.reason_codes == ["SCI_NO_ADMISSIBLE_PAG"]` exactly, no mixed/unknown/technical/duplicate reasons; no `graph.json` / Effect result | P05 validates typed scientific negative and diagnostics reason bytes; Reader validates actual negative sidecar; technical failures do not qualify |
| Artifact inventory | Every descriptor has unique safe POSIX key, lowercase SHA256 hex64, `size_bytes>0`, `media_type="application/json"`, `privacy_class="AGGREGATE"`, `visibility="PRIVATE"`; no unknown, extra, missing or duplicate key; no `result.json`, `manifest.json`, `_COMMITTED.json` or row data | P02 same-FD actual bytes SHA/size/MIME, private FS, atomic publication and full independent Reader |
| Review/privacy/runtime | `review.science_evidence_ref=null`, Study `privacy={classification:AGGREGATE,row_export_requested:false}`; no raw path, secrets, unsupported non-JSON value, self hash or unmeasured runtime invention | P05 enforces effective privacy and runtime provenance; Reader checks run/artifact privacy |

G01 has **two and only two** publishable DISCOVER variants above. An actual Backend exception, missing/malformed Graph, bad file/hash or privacy violation is a technical failure and must **not** be converted into a scientific-negative bundle. No Graph content-hash-versus-Artifact SHA equality: `Graph.content_hash` is the semantic hash of Graph without its own hash, while `ContentRef.sha256` and Descriptor SHA are the exact completed `graph.json` file-byte hash. The Graph's scientific provenance, graph internal ref semantics and file-to-wire value equality cannot be inferred from descriptors alone and are rechecked by P03/P05/P02 Reader.

#### 6.5.4. Failure, no-side-effect and handoff

P01 must reject rather than default: absent/wrong-type/unknown fields, source Study↔typed Study mismatch, Method/Status/run/hash mismatch, impossible positive/negative combination, invalid graph output ref, missing/extra/duplicate Artifact, bad privacy/row release, and false Science PASS. Return typed schema/hash/privacy reasons consistent with G01 CLI mapping, without mutating input or opening files. The `e11_local_manifest_v1.schema.json` and `e11_local_status_v1.schema.json` apply to serialized structure; P01's operation-specific semantic validator enforces the additional equalities above. `P02.stage_bytes` supplies actual descriptors; `P05` constructs the immutable evidence after staging and before seal; `P02.seal/publish/Reader` alone proves committed bytes. A candidate Manifest/Status carrying `COMPLETED` is **not** an externally returned completed run before Reader verification.

### 6.6. Dependency boundaries / handoff

P01 outputs `ContentRef`, `ValidatedStudy`, strict JCS/Manifest DTO and pure Profile validation; P02 verifies real File bytes and owns publication/readback, P03 owns `GraphEvidence`, P04 owns FCI runtime and P05 orchestrates. Do not make pure Decoder read files, do not let App import CLI concrete, do not modify Product v2 Reader/Writer or duplicate scientific eligibility logic.

## 7. Focused verification — WHAT and primary layer; no file-path authority

| DD ID / Gate test | Primary layer | Positive and negative evidence required |
| --- | --- | --- |
| REF01/04; 07-01/02 lexical | unit + contract | 5-field ContentRef, safe POSIX path, hash grammar, distinct bytes/digest claims; no actual-FD validity claimed |
| SPEC01–04; 07-01 | unit + contract | E11 dispatch vs legacy/unknown, YAML/JSON duplicate/unknown, Method Config/Estimand/inference/privacy failures; typed reason and no Backend import |
| MAN01–03; 07-04 | unit + contract | strict JCS independent 7+7 vectors, stable exact bytes, 4 distinct digest projections, no self hash/inventory |
| MAN04–06; 07-07/12 | contract | typed DISCOVER Graph-positive versus scientific-negative inventory/status, no Effect, no silent Product v2 upgrade |

**Additional focused MAN04/05 contract cases:** Construct both valid G01 evidence variants with staged-descriptor stand-ins (not claimed physical proofs), then test the exact reserved SCI_NO_ADMISSIBLE_PAG negative tuple/status list using a synthetic P01-only fixture; reject a technical code repeated in *both* fields, any unknown SCI_*, mixed or duplicate codes, and Graph-positive with nonempty Status reason_codes; then reject each missing/extra/duplicate descriptor, mismatched Study↔status run/hash/method, differing input five-field ref, wrong output Graph ref SHA/key/MIME, Graph-positive-with-diagnostics, Graph-negative-without-typed reason, missing science-negative diagnostics, false Science PASS/row output, and mutable evidence aliasing. Exercise `from_payload` and `from_run_evidence` on matching public projections. Never claim P02 FD/Reader verification from this suite.

**Required Package check:** Coding Agent creates or discovers G01-focused tests according to *instantiated 40 Operator placement policy*; current filename/pytest command is selected only after checkout/collection. No filename is normative here. Unit or synthetic typed evidence does not pass P02 physical REF02/03, P04 science, or P05 cross-asset trusted-byte joins. Verify each DD ID's relevant positive/negative cases, source SHA, fixture SHA, observed error/bytes and status. P01 DoD requires scoped focused tests and checkpoint evidence; unrun or unproved independent JCS reference stays BLOCKED.

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

- [ ] `ContentRef` 5 fields and `from_payload`, `LocalStudySpec.validate_local_invariants`, `LocalConfigDecoder.decode` implement strict versions, error classification and pure handoffs.
- [ ] Common `ValidatedStudy`/`EstimandRef` implements GRAPH_STRUCTURE without changing Product v2 ATE/ATT ABI or silently validating unread Question/Design files.
- [ ] Strict JCS bytes/digest and immutable `LocalRunManifest` factories/invariant/serialization complete; `ValidatedRunEvidence`/`RuntimeEvidence`/`ArtifactDescriptor` types, exact Study/Status projection, operation-specific inventory and upstream-ref equalities from §6.5 verified with positive/negative pure tests; independently verified golden vectors or explicit evidence-backed BLOCKED.
- [ ] G01 positive/negative typed bundle shapes, §6.5.1a closed science reason codes (technical-code masquerade, unknown, mixed and duplicate negatives), MAN01–06 pure constraints, no Effect/Manifest self-hash covered by focused tests; synthetic P01 cases do not establish real P04 science.
- [ ] **P01 covers REF01/04 lexical components; REF02/03 actual symlink/race/FD security are P02-owned and cannot be marked passed by P01.** Full cross-asset Question/Design/Dataset byte validation is P05-owned.
- [ ] Focused unit/contract verification cases and actual resolved test evidence, fixture/version/commit full SHA, DD-ID case-by-case evidence, package checkpoint report and `*_in_progress.md` recorded. Remaining P02/P03/P04/P05/G01-999 checks are not promoted to P01 PASS.

## 11. External reference policy

source / previous checkpoint / test output / provenanceは外部参照してよい。本書のimplementation rule、prohibited scope、completion criterionをParent 06 / P00へ委譲してはならない。

## 12. Stop rule

- package scope完了 -> `PACKAGE_COMPLETE`
- continuation不能 -> `PACKAGE_BLOCKED`
- Gate PASS / FAILは判定しない。
- next packageへ勝手に先行しない。

### Owner SIM-01/02 scope cut (2026-11-21, current G01 contract)

G01 supports non-root Linux effective UID owned private local ext4/XFS with directory 0700, file 0600, safe dirfd/O_NOFOLLOW, no path traversal/symlink escape and same-FS no-clobber publication/readback. Separate ACL/xattr-digest, statx mount-ID/namespace visibility attestation, and CI/container heuristic detection are **removed** as mandatory proof. This does not protect against root or same-UID actors. Retain real path/UID/mode/FS positive and negative tests. Strict RFC8785 JCS codec and all SHA256/semantic/version checks remain, but **external ECMAScript execution and Python-JavaScript parity as a blocking test are removed**; compare exact bytes to independent RFC8785 golden expectations. The independent FCI/PAG science oracle and all F03 atomic Publisher/Reader tests are unchanged. Historical PREP02 decisions are superseded solely within SIM-01/02, combined_review/131. No runtime tests, Gate999 or Coding Authorization are authorized.


## S02-01/02/06/07 対象Gateの確定契約（Owner採用・未実装）

G01は`P1-M06`のDISCOVERのみで、個票の出力を常に拒否する。Valid Studyの`privacy.row_export_requested=false`（省略の扱いはstrict Study schemaのdefault/requiredに従う）を要求し、trueはPrivacy exit3。廃止された追加CLI row許可flagを登録せず、渡された場合は不明オプションとしてconfig exit2。Contextは`LocalRunContext(root:TrustedLocalRoot,principal:LocalPrincipal)`、Privacy Portは`authorize(*,study,root,principal,output_shape)`であり、署名Policy/Study policy_refは存在しない。G05のみStudy単独opt-in（true）とOS/Method制約の全件ANDを満たす個票中間出力を担当する。

新Local Graphのimmutable identityは内容hash、parent/source科学証拠とContentRef。Product GraphVersion DBへlookup/write/edit/FIXせず、現行E11 Graph wireの`version_id`と`parent_version_id`はどちらもnullとし、non-nullは未対応importとして拒否する。既存ProductのGraphVersionServiceや旧v2は無変更。

OS/FS受入は有界な不変条件別の正負例（owner EUID・0700/0600・dirfd/O_NOFOLLOW・same FS・symlink/race・rename前後・post-rename indeterminate・Marker/Reader/hash）に限定する。冗長なfault-permutation全順列、statx mount-ID/namespace証明、ACL/xattr digest/コンテナ推測、電源断耐久保証は追加しない。JCS RFC8785 golden bytes、no-clobber、公開後整合性、独立PAG Science Oracleは維持する。Coding Agentが未承認の広いProof強化を推測で復活させない。


### S09-JCS-01 bounded repair (AMD-E11-G01-P01-003; Owner design decision adopted, formal 09/S10/S11 pending)

The deterministic RFC8785 number codec must be independent of ambient Decimal precision, rounding, exponent limits, traps and flags; it must not mutate caller context. Repair only _number and necessary imports in src/ariadne/shared/serialization/jcs.py. Preserve all public APIs, VERSION, number-domain rejection, Unicode/key sorting and hash domains. Add only tests/enhancement/enh_e11/g01/contract/test_jcs_context_independence.py; existing tests/fixtures and consumers unchanged. Test exact independent RFC8785 bytes/hash, reported precision-6 counterexample, bounded context variation, number boundaries and unchanged golden vectors. Do not infer ECMAScript shortest-roundtrip equivalence from Python repr alone. Actual valid legacy bundle readback and cross-context publication/Reader integrity, all G01 and affected Product/Scientific regression required. No implementation authorization from this section alone; completed P01 may be reopened only by explicit bounded Owner S11.
