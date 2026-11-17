# ENH-E11 G01 P01 — Local Study, ContentRef, Canonical Codec

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
| `ariadne.interfaces.cli.local_causal.manifest.LocalRunManifest` | Pure wire DTO and `from_payload/from_run_evidence/validate_invariants/to_canonical_bytes` | Staging, Marker and readback belong to P02 |

The Package produces typed values, verified **schema** and canonical bytes; it does not claim verified physical input, Product GraphVersion ownership or independent Graph science.

## 4. Explicitly out of scope
他GateのMethod実装、旧Product v2変更、根拠なしのScience PASS、行出力自己許可、未承認ACL/mount、既存run上書き、Package外の便乗変更。

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

**G01 accepted subset:** `operation=DISCOVER`, `analysis_mode=EXPLORATORY`, required Question/Design/Dataset; `inputs.graph=null` and `inputs.identification=null`. `estimand={family:GRAPH_STRUCTURE,population:OBSERVED_VARIABLES,contrast:NOT_APPLICABLE}`; `inference={requested:false,confidence_level:null}`; `privacy={classification:AGGREGATE,row_export_requested:false,policy_ref:null}`. Row request is a denial in P05 (exit3); malformed structural combination is exit2. Never fabricate ATE, Effect Result, Identification or Science PASS.

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

Run the repository's `e11_jcs_golden_vectors.json` (7 positive/7 negative) against independent ECMAScript bytes; Python-only roundtripping does not establish cross-language conformance. No UTF normalization that changes the supplied code points.

### 6.5. `LocalRunManifest` — 30_62 §4 / MAN01–06

**Module/Class:** `ariadne.interfaces.cli.local_causal.manifest.LocalRunManifest`; immutable DTO. **Constructor/Factory:** Use the strict `from_payload` or `from_run_evidence` factories below; no raw dict cast can substitute for validation. Logical fields `manifest_version:Literal["e11-local-manifest/1"]`, `run_id`, `operation`, `request_hash`, `lineage` (typed refs), `execution_status` (technical and science independent), `runtime` (actual runtime evidence), `artifacts:tuple[ArtifactDescriptor,...]` and `review`. These are logical groups: public serialized keys must conform to `e11_local_manifest_v1.schema.json`, not a newly invented representation.

~~~python
@classmethod
def from_payload(cls, payload: Mapping[str,JsonValue]) -> LocalRunManifest: ...
@classmethod
def from_run_evidence(cls, evidence: ValidatedRunEvidence) -> LocalRunManifest: ...
def validate_invariants(self) -> tuple[Reason,...]: ...
def to_canonical_bytes(self) -> bytes: ...
~~~

**Factory invariants:** fixed E11 version, mandatory fields, no v2 fallback, typed status/lineage, actual environment/method/seed evidence (no synthetic values), safe unique artifact keys and hashes; cannot include raw secrets, row data, absolute source paths. Factories and invariant validation are pure; no disk I/O.

**DISCOVER Operation bundle:** Graph-success => actual `study.json/status.json/graph.json`, `schema_dispatch.graph="e11-local-graph/1"`, `result=null`. Valid scientific Graph-negative => `study.json/status.json/diagnostics.json` with nonempty typed reason, `graph=null` and `result=null`. Never create dummy Effect or silently omit diagnostics. P03 provides typed Graph; P02 creates files, marker and verifies Inventory. Neither `manifest.json` nor `_COMMITTED.json` may be listed in Manifest inventory. Each listed artifact requires exact bytes SHA, size, MIME, privacy class and visibility, plus upstream ref join.

**Status:** G01 independent Science approval is not produced by run: `identification_status=NOT_APPLICABLE`, `point_availability=NOT_REQUESTED`, `inference_availability=NOT_REQUESTED`, `science_acceptance=NOT_EVALUATED`. A return of `COMPLETED` is only valid after P02 publication/Reader; DTO creation alone never asserts completed publication. Errors: `SCHEMA_INVALID`, `VERSION_UNSUPPORTED`, `HASH_INVALID`, `PRIVACY_POLICY_CONFLICT` with typed reason and phase.

### 6.6. Dependency boundaries / handoff

P01 outputs `ContentRef`, `ValidatedStudy`, strict JCS/Manifest DTO and pure Profile validation; P02 verifies real File bytes and owns publication/readback, P03 owns `GraphEvidence`, P04 owns FCI runtime and P05 orchestrates. Do not make pure Decoder read files, do not let App import CLI concrete, do not modify Product v2 Reader/Writer or duplicate scientific eligibility logic.

## 7. Focused verification — WHAT and primary layer; no file-path authority

| DD ID / Gate test | Primary layer | Positive and negative evidence required |
| --- | --- | --- |
| REF01/04; 07-01/02 lexical | unit + contract | 5-field ContentRef, safe POSIX path, hash grammar, distinct bytes/digest claims; no actual-FD validity claimed |
| SPEC01–04; 07-01 | unit + contract | E11 dispatch vs legacy/unknown, YAML/JSON duplicate/unknown, Method Config/Estimand/inference/privacy failures; typed reason and no Backend import |
| MAN01–03; 07-04 | unit + contract | strict JCS independent 7+7 vectors, stable exact bytes, 4 distinct digest projections, no self hash/inventory |
| MAN04–06; 07-07/12 | contract | typed DISCOVER Graph-positive versus scientific-negative inventory/status, no Effect, no silent Product v2 upgrade |

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
- [ ] Strict JCS bytes/digest and immutable `LocalRunManifest` factories/invariant/serialization complete; independently verified golden vectors or explicit evidence-backed BLOCKED.
- [ ] G01 Operation success vs scientific-negative typed bundle shapes, MAN01–06 pure constraints, no Effect/Manifest self-hash are covered by focused tests.
- [ ] **P01 covers REF01/04 lexical components; REF02/03 actual symlink/race/FD security are P02-owned and cannot be marked passed by P01.** Full cross-asset Question/Design/Dataset byte validation is P05-owned.
- [ ] Focused unit/contract verification cases and actual resolved test evidence, fixture/version/commit full SHA, DD-ID case-by-case evidence, package checkpoint report and `*_in_progress.md` recorded. Remaining P02/P03/P04/P05/G01-999 checks are not promoted to P01 PASS.

## 11. External reference policy

source / previous checkpoint / test output / provenanceは外部参照してよい。本書のimplementation rule、prohibited scope、completion criterionをParent 06 / P00へ委譲してはならない。

## 12. Stop rule

- package scope完了 -> `PACKAGE_COMPLETE`
- continuation不能 -> `PACKAGE_BLOCKED`
- Gate PASS / FAILは判定しない。
- next packageへ勝手に先行しない。
