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
他GateのMethod実装、旧Product v2変更、根拠なしのScience PASS、行出力自己許可、未承認ACL/mount、既存run上書き、Package外の便乗変更。

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

### 6.3. Product Version identity/parent mapping (GRAPH04)

| Situation | `version_id` | `parent_version_id` | Required outcome |
| --- | --- | --- | --- |
| CLI standalone `DISCOVER` (G01 main path) | `null` | `null` | valid; Graph identity by semantic content hash + external ContentRef |
| Existing Product GraphVersion no parent | actual Product ID | `null` | only when verified Product origin/linkage |
| Existing Product GraphVersion with parent | actual Product ID | actual parent Product ID | same Project, actual parent lineage verified by Product owner |
| Non-null parent with null version | `null` | actual parent ID | reject by Schema + semantic validator |
| Invented local UUID masquerading as Product Version | arbitrary ID | any | reject; CLI may not assign Product ID |

**Domain field mapping:** `source_graph_version_id ↔ version_id`, `source_graph_parent_version_id ↔ parent_version_id`. Both keys are present and nullable in wire; parent nonnull implies version nonnull. Runtime real-ID existence and parent association are verified **at Product integration authority**, not assumed by a pure JSON parser without DB access. G01 output must always be null/null. No `GraphEvidence.make_revision`, `edit`, `fix` or Version ID issuing. The single writer remains existing `GraphVersionService` with Project/parent checks; P03 must not modify or recreate it.

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

| DD / 07 | Test file | Positive and negative assertions |
| --- | --- | --- |
| GRAPH01; 07-03/04 | `unit/test_g01_graph_roundtrip.py` | all legal G01 PAG endpoint combinations, reverse orientation swap, JCS semantic/content byte digest, 100% lossless |
| GRAPH03; 07-03 | same | duplicate edge (including reverse), self loop, wrong mark, unknown node, illegal lag/temporal, implicit PAG→DAG conversion rejected |
| GRAPH04; 07-03 | same | standalone null/null, parent without Version rejection, Product version/parent preservation, no `make_revision` |
| MAN03/04; 07-07 | same, `unit/test_g01_spec_schema_codec.py` | Graph-success/negative inventory shape, no dummy Effect, correct Graph/ContentRef/hash provenance |

~~~bash
uv run --no-sync python -m pytest tests/enhancement/enh_e11/g01/unit/test_g01_graph_roundtrip.py -q
~~~

Use independent expected endpoint fixtures; avoid comparing Backend output to itself as an Oracle. Real FCI MAG/PAG equivalence is `G01-07-09` (P04) and remains BLOCKED until independently proven. P03 reports per-DD-ID PASS/FAIL/BLOCKED with fixture SHA and real vs synthetic flag; never claims a Product GraphVersion persisted without the Product authority.

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
全部の定義済みPAG endpoint round-tripが100%で、PAG→DAG silent conversionも旧Graph mutateも0。 集中検証の証跡・実装checkpoint SHA・Package Reportを揃える。未検証はBLOCKEDで止める。

## 11. External reference policy

source / previous checkpoint / test output / provenanceは外部参照してよい。本書のimplementation rule、prohibited scope、completion criterionをParent 06 / P00へ委譲してはならない。

## 12. Stop rule

- package scope完了 -> `PACKAGE_COMPLETE`
- continuation不能 -> `PACKAGE_BLOCKED`
- Gate PASS / FAILは判定しない。
- next packageへ勝手に先行しない。
