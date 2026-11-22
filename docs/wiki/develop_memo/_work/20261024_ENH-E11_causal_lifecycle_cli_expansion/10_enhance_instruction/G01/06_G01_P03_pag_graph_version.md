# ENH-E11 G01 P03 — PAG Endpoint, GraphVersion, Non-effect Bundle

**Document class:** Primary Execution Contract  
**Self-containment:** MUST — Assigned Coding Agentが本書だけでpackageのnormative execution responsibilityを理解できること。

- Gate: G01
- Trial: Trial01（未開始）
- Package: P03
- Parent 06 (traceability): 06_Ariadne_ENH-E11_G01_implementation_instruction.md
- P00 Plan (traceability): 06_G01_P00_work_package_plan.md
- Depends on: P01
- Status at issuance: DRAFT / CODING_NOT_AUTHORIZED

## 1. Purpose
Graphの不確定性と版・同一性を損失なく保持する。

## 2. Effective Gate constraints applicable to this package

このpackageが守るべきGate-level semanticsを、Parent 06 / P00を読まなくても実行判断できる粒度で記載する。

G01は正式Gate IDでPxxはbounded Coding Unit。Local laneとProduct v2を分離し旧CLI/Web/API/DB/Workerは改変しない。strict version/Method/EstimatorとJCSのハッシュ対象を検証し、PAGをDAG/ATEへ変換しない。OS root/Privacy/Atomic Publishの不適格はfail-closed、SCI不確実性をPASSに変換しない。Coding Authorization前の実装は禁止。

## 3. In scope — implementation ownership

| Class / module | Owned by P03 | Explicitly not owned |
| --- | --- | --- |
| `ariadne.causal.discovery.graph_evidence.GraphEvidence` | immutable typed Graph, strict Factory, `canonical_payload`, meaning digest | Product GraphVersion editing/revision/FIX |
| `ariadne.shared.graph_semantics.GraphSemanticsValidator` | common DAG/CPDAG/PAG endpoint validator and compatibility wrapper | separate reimplemented validation logic in CLI |
| E11 wire ↔ Product graph translation | lossless endpoint-name mapping and bidirectional node-order/mark handling | no Product v2 schema change |
| DISCOVER Graph target and Bundle semantic checks | Graph-success or scientific negative; Graph/ContentRef dual hashes | P01 Manifest codec and P02 physical publication |

G01 `DISCOVER` creates a new immutable Graph value, not a Product GraphVersion. Version issuance is the existing `product.application.graph_version_service.GraphVersionService` sole authority.

## 4. Explicitly out of scope
他GateのMethod実装、旧Product v2変更、根拠なしのScience PASS、行出力自己許可、不適格なUID/owner/mode/local FS、既存run上書き、Package外の便乗変更。

## 5. Entry criteria / required evidence
Gate 06/07のFreeze・Coding Authorization・固定branch HEAD確認。Depends on P01の実装checkpoint full SHAとfocused検証を確認。矛盾/依存未成立はBLOCKED。

dependency checkpoint / source state等はfactとして外部参照してよい。Entry rule自体は本書内に記載する。

## 6. Required implementation — Graph semantics and Version provenance

### 6.1. `GraphEvidence` / `GraphSemanticsValidator` — 30_61 §1,6,7 / GRAPH01,03,04

**Class/Module:** `ariadne.causal.discovery.graph_evidence.GraphEvidence`; immutable value distinct from Product Entity. Instance fields:

| Field | Type and constraint |
| --- | --- |
| `kind` | `GraphKind` (DAG/CPDAG/PAG; no implicit cast) |
| `nodes` | `tuple[Node,...]`, nonempty unique IDs |
| `edges` | `tuple[EndpointEdge,...]` with source/target/marks/lag; no mutable backend objects |
| `temporal` | `TemporalConvention|None`; G01 FCI always null |
| `source_graph_version_id` | `str|None`, Product GraphVersion only if real |
| `source_graph_parent_version_id` | `str|None`, parent Product ID only if real |
| `provenance` | `GraphProvenance`, recorded scientific method/Backend/CI/assumptions |
| `content_hash` | `str`, lowercase 64hex of JCS Graph semantic projection |

~~~python
@classmethod
def from_canonical_json(cls, raw: bytes) -> GraphEvidence: ...
def canonical_payload(self) -> Mapping[str, JsonValue]: ...
~~~

**Constructor/Factory precondition:** strict JSON decode (duplicate key forbidden), `e11-local-graph/1` Schema, common Graph semantic validator and Graph digest verification. Reject unknown/missing nodes or edges, self-loop, duplicate/reversed edges, invalid endpoint mark, unsupported Graph kind/lag, inconsistent parent ID and missing/incorrect semantic digest. Constructor does not write files, edit Product Entities or call an optional backend.

**Postcondition:** `GraphEvidence` fully represents each declared endpoint/temporal/provenance/version reference losslessly; `canonical_payload` emits exactly the E11 public shape and permits a strict roundtrip back to the same graph identity. Serialize through P01 strict JCS; not Python dictionary order or Product `hash_mapping(default=str)`.

### 6.2. Wire mapping and endpoint invariants (GRAPH01/03)

**Wire keys:** `schema_version="e11-local-graph/1"`, `kind`, `version_id`, `parent_version_id`, `nodes`, `edges`, `temporal`, `provenance`, `content_hash`; no extra top-level fields.

**Edge type:** `EndpointEdge(source, target, source_mark, target_mark, lag)`; E11 wire edges have exactly `source, target, source_mark, target_mark, lag`. Allowed marks `TAIL,ARROW,CIRCLE`; G01 FCI `kind=PAG`, `lag=null`, `temporal=null`. Preserve nonidentifiability: `CIRCLE/CIRCLE`, `CIRCLE/ARROW`, `TAIL/CIRCLE`, `ARROW/ARROW` and all schema-/Graph-kind-legal endpoint pairs are not converted into a DAG. PAG bidirected is *one endpoint-pair edge*, not two causal effects.

**Normalization rule:** If nodes are reordered for canonical identity, normalize edge orientation by deterministic ID ordering and **simultaneously swap endpoint marks**. Edge (`a,b,TAIL,ARROW`) is semantically equivalent to reversed (`b,a,ARROW,TAIL`); reject duplicates even if reversed. Distinct endpoint pairs with same nodes are not silently merged. Preserve vertex IDs and exact mapping from Dataset observable columns; no backend `X1` name guessing.

**Product compatibility:** Existing `ariadne.product.domain.graph_semantics.validate_graph_document/canonical_graph` expects `endpoint_source/endpoint_target` whereas E11 wire expects `source_mark/target_mark`. Implement explicit mapping in an Adapter/common pure validator; never feed E11 Graph dict into old validator unchanged. Preserve existing Product import ABI via compatibility wrapper, do not fork two independent scientific semantic implementations. Note older Product validator handles DAG/CPDAG/PAG endpoint rules but may not validate G01 temporal and Product lineage; add those checks in GraphEvidence layer.

**Scientific constraint:** FCI discovery returns PAG uncertainty; a successful schema roundtrip is **not** independent MAG/PAG scientific correctness. Do not present undirected endpoints, fixed Graph state, or potential latent confounding as verified causal truth; `GraphEvidence` is evidence, not an Effect identification permission.

### 6.3. Local Graph identity and independent Product compatibility (GRAPH04)

Current `e11-local-graph/1` is **Local-only**: both `version_id` and `parent_version_id` are required and `const: null` in the active draft Schema. `GraphEvidence.from_canonical_json` must reject non-null values **even when the caller claims a real Product GraphVersion ID**; no Product DB lookup, creation or import occurs in the E11 Local wire. A local revision is a new immutable Graph artifact identified by its semantic `content_hash` and external ContentRef; scientific source/parent lineage belongs to validated `provenance` and referenced artifacts, not fabricated Product Version IDs.

| Situation | Current E11 Local wire | Required behavior |
| --- | --- | --- |
| G01 standalone `DISCOVER` | `version_id=null`, `parent_version_id=null` | Accept if graph/hash/provenance and endpoint semantics pass validation |
| Local scientific successor graph | Both Product Version fields null; scientific parent evidence in provenance/ContentRef | Preserve immutable scientific lineage and validate referenced hashes |
| Either Product Version field non-null in E11 Local wire | Outside current Local Schema | Strictly reject as unsupported Product import, without attempting a DB lookup |
| Existing Product GraphVersion with/without parent | Remains an **existing Product object**, not E11 Local graph wire | Keep legacy Product ABI, real Product ID/parent checks and existing `GraphVersionService`; test via a separate compatibility wrapper |

Internal `source_graph_version_id` and `source_graph_parent_version_id` are nullable for the Local adapter and must both remain `None` when producing or reading current E11 wire. A distinct compatibility bridge to the existing Product domain may inspect real Product IDs on Product objects, but must not serialize those IDs as accepted current Local wire. `GraphEvidence` has no `make_revision`, `edit`, `fix` or Version ID writer.

### 6.4. Dual-hash and content identity (GRAPH01 / MAN03–04)

1. Normalize/validate entire Graph *meaning* (including version keys and provenance) to the E11 schema. Construct the payload without its own `content_hash` field.
2. `Graph.content_hash = SHA256(JCS(Graph without content_hash))` using P01 `e11-json-jcs-rfc8785/1`. This semantic digest is stored **inside** the Graph.
3. Serialize the completed Graph including `content_hash` as strict JCS file bytes; external `ContentRef.sha256 = SHA256(exact saved graph.json bytes)` is computed by P02 when staging the artifact. These two hashes will **normally differ**; never cross-compare them as if same semantic object.
4. Validate that re-parsing the stored graph preserves semantic digest, endpoint pair identities, null Version fields and provenance. Reader joins Graph file bytes to Manifest Inventory and Study/run/method lineage; do not trust Graph's internal digest as proof that file was safely opened.

**Errors:** schema/duplicate/unknown node/endpoints/lag/digest -> typed Graph validation failure, not scientific `NOT_IDENTIFIED`; Product version mismatch/invented ID -> provenance/lineage failure. Graph errors cannot become a publication success by silently dropping edges.

### 6.5. DISCOVER output and interaction with P01/P04/P05 (GRAPH01, MAN03/04, DISC02)

- Valid graph path: P04 scientific adapter emits `DiscoveryGraphOutcome` containing validated `GraphEvidence`. P01 `LocalRunManifest` lists `study.json`, `status.json`, `graph.json`, `schema_dispatch.graph="e11-local-graph/1"`, `result=null`; P02 publishes actual bytes. No `result.json` or dummy ATE.
- Legitimate science-negative path: Graph absent by reasoned scientific determination, not because an exception was swallowed; `diagnostics.json` is mandatory with nonempty typed reason, `schema_dispatch.graph=null` and `result=null`. P05 must preserve technical-vs-science axes.
- Technical failure (malformed backend graph, unknown endpoint, missing runtime) is not automatically a negative scientific result and must not publish an invented valid PAG.
- P03 is usable with synthetic Graph fixtures before P04; scientific correctness belongs to independent GRAPH-A Oracle in P04/07. No temporal `GRAPH02` or Product Graph edit implementation in G01.

## 7. Focused verification — Graph identity, not science PASS

| DD / Gate | Primary layer | Positive and negative assertions |
| --- | --- | --- |
| GRAPH01; 07-03/04 | unit + contract | all G01 PAG endpoint pairs/reverse orientation, JCS semantic/file digests, lossless 100% |
| GRAPH03; 07-03 | unit + contract | duplicate (including reversed), self loop, illegal mark, unknown node, lag/temporal and implicit PAG→DAG rejection |
| GRAPH04; 07-03 | contract | standalone null/null, parent-without-version reject, strict non-null Product import rejection, scientific provenance parent preservation, legacy Product parent checks in a separate wrapper, no GraphEvidence version writer |
| MAN03/04; 07-07 | contract | Graph-success vs legitimate negative inventory and diagnostics, no Effect, correct Graph/ContentRef lineage |

**Required Package check:** Implement focused tests in an appropriate G01 enhancement layer under the 40 placement rule; resolve actual test files and collection during execution, not in P03 acceptance semantics. Use independent expected endpoint fixtures, not a self-generated backend Oracle. Scientific MAG/PAG recovery remains G01-07-09 (P04) and BLOCKED until independently proven. Report per DD ID PASS/FAIL/BLOCKED, actual endpoint/digest evidence, fixture and source SHA; do not claim a persisted Product GraphVersion.

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

- [ ] `GraphEvidence` field/constructor/Factory/`canonical_payload` matches 30_61 and strict E11 Schema with no Product Version Writer behavior.
- [ ] All G01 PAG endpoint pair orientations round-trip losslessly, malformed/self-loop/duplicate/reverse/unknown/lag negatives rejected; shared Product Graph validator mapping uses `endpoint_source/target` vs E11 `source_mark/target_mark` correctly.
- [ ] Current **all E11 Local Graph** wire `version_id=null,parent_version_id=null` strictly; scientific parent/reference lineage is expressed through immutable provenance/ContentRef/hash, **not** Product GraphVersion IDs. Non-null Local wire IDs are rejected. Optional real Product parent/version lineage is preserved only in the **separate existing Product compatibility bridge** and cannot be silently injected into `e11-local-graph/1`.
- [ ] Graph semantic JCS self-excluded digest and external exact-file-byte ContentRef digest distinguished; success vs scientific-negative Bundle has `result=null` and mandatory diagnostics on negative.
- [ ] Focused unit/contract Graph DD-ID verification cases executed and checkpoint/fixture/source full SHA recorded. Graph serialization PASS is not independent MAG/PAG scientific accuracy PASS.

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
