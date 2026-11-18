# ENH-E11 G06 P01 — temporal_graph

**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G06 / **Package:** P01 / **Trial:** NOT_STARTED  
**Depends on Pxx:** NONE  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G06_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G06_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** G01 GraphValueを再利用しTemporalConvention/lag sign/time order/CI条件を検証。

**Scope:** 本PackageのClass/Methodと、それらが必要とする契約/適格性/Result Evidenceに限定。**Gate全体の保護意味:** Temporal Graphのlag/endpoint不確実性を保持しPCMCI系をMethod別に実行する。

**科学/Designの必須制約:** time index/lag sign、contemporaneous/latentと独立Graph oracle必須。PAGをDAGへ勝手に変換しない。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** G01 GraphValueを再利用しTemporalConvention/lag sign/time order/CI条件を検証。

### 2A. 既存Discovery ABIとTemporal Kernel境界（`2cf28f59a324`）
- **既存:** `src/ariadne/scientific/discovery/adapter.py`の`DiscoveryAdapter.run(self, input_: DiscoveryInput, output_dir: Path) -> list[ScientificResultDescriptor]`と`src/ariadne/scientific/core_adapter.py`の`ScientificCoreAdapter.run_discovery(self, input_: DiscoveryInput, output_dir: Path)`は公開Product Path API。E11 `DiscoveryPort.discover(self, request:ValidatedDiscoveryRequest, *, sink:StagingArtifactSink) -> DiscoveryGraphOutcome`とは入力・出力・Publication契約が異なる。変更・無検証Cast・旧Path writerの直接利用は禁止。
- **新規境界:** Tigramite PCMCI/PCMCI+/LPCMCIの実効API・CI test・Temporal endpointとlag sign/時刻原点をMethod別に検証。既存DiscoveryAdapterの存在だけをTigramite Method実装済み証拠としない。Design-only TemporalGraphEvidenceとTyped Portは§3で所有Class/方法を確定し、G01 GraphVersionService/Publisher/MethodRegistryを複製せず共有する。lag/time index、latent marks、CI kernelが不明なら`BLOCKED_CONTRACT_AMBIGUITY`。

### 2B. Operation別Artifact/Schema契約（このPackage本文が実装規範）
| Operation | 必須Artifact | 禁止・negative条件 |
|---|---|---|
| DISCOVER | `study.json`, `status.json`, Graph成功時`graph.json` | `result.json`禁止。科学的Graph無しは`diagnostics.json`＋nonempty reason、`schema_dispatch.graph=null`。Backend失敗との混同は禁止 |
| IDENTIFY | `study.json`, `status.json`, `identification.json` | Effect `result.json`禁止。識別negativeもtyped、Graph/Design/Estimand/Proof hashを照合 |
| ESTIMATE | `study.json`, `status.json`, `result.json` | `schema_dispatch.result=e11-local-effect-result/1`。point欠落はnull＋理由で表し、非識別への推定値偽装禁止 |
| REFUTE/SENSITIVITY/DIAGNOSE | `study.json`, `status.json`, `diagnostics.json` | Effect再発行禁止。上流Effect/Graph/Design hash、seed・適用条件の検証が必須 |

全Operationに`manifest.json`（`e11-local-manifest/1`）と`_COMMITTED.json`（`e11-commit/1`）を置くが、両者はArtifact Inventory外。Inventoryは実Fileの相対POSIX key・size bytes・SHA256・MediaType・Privacyを列挙。`request_hash=SHA256(JCS(validated typed Study JSON))`、Manifestに自己hashを入れずMarkerがManifestの実bytes SHA256を保持。Readerはmarker→manifest→artifact→Operation Profile→upstream hashをTrustedRoot内で検証。staging→atomic no-clobber publishを既存G01 Publisherで行い、Row Parquetは独立承認証拠の検証前にbytes生成すら禁止。Publication不正・欠損をScience negativeに変換しない。

## 3. Class Placement, Signature, Reuse, Dependency Direction

| Class/Port | Designed module (DD30_61〜63) | Ownership boundary | Exact approved/design signature |
|---|---|---|---|
| `GraphEvidence` | `ariadne.causal.discovery.graph_evidence.GraphEvidence` | Port/Value/Facade integration (no duplicate implementation) | from_canonical_json(raw:bytes) / canonical_payload() |
| `DiscoveryPort` | `ariadne.scientific.ports.causal.DiscoveryPort` | Port/Value/Facade integration (no duplicate implementation) | discover(self, request:ValidatedDiscoveryRequest, *, sink:StagingArtifactSink) -> DiscoveryGraphOutcome |
| `MethodCapabilityRegistry` | `ariadne.capabilities.causal.method_registry.MethodCapabilityRegistry` | Port/Value/Facade integration (no duplicate implementation) | describe(method_id) / resolve(method_id,backend_id,profile) / load_adapter(capability) |

**Method Adapter signature policy:** 新Adapterは原則`preflight(self,request:ValidatedMethodRequest)->EligibilityOutcome`／`execute(self,request:ValidatedMethodRequest,*,sink:StagingArtifactSink)->TypedScientificOutcome`。上表で指定された既存`run(self,input_,output_dir)`はその署名を保持。PortはApplication→Scientific kernelへ向かい、CLI Layerに別の科学数値実装を作らない。本Pxx§3.1以降のClass定義がField/Constructor/Methodの規範であり、外部DDはprovenanceのみ。Design未確定箇所や実Backend ABIを補完せずBLOCKEDで停止する。

**Responsibility:** 本PackageはScientific Adapter数値本体を新規所有しない。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。

### 3. Standalone Class/Method contracts

以下をNormative Contractとして本Pxxに展開する。DDはProvenanceのみ、別06/07はCodingの不足判断を補完するSourceにしない。Class存在とLegacy ABIは実Sourceで確認し、設計Classと混同しない。

### 3.1. `GraphEvidence` — inline Field/Constructor/Method contract

#### 識別情報・責務

**Class / module:** `ariadne.causal.discovery.graph_evidence.GraphEvidence`。PAG/CPDAG/DAG/temporal等の科学的Graph Evidenceを保持するimmutable Value。Product `GraphVersion`のVersion作成・編集・FIX権限を持たない。Wireの`version_id`はProduct GraphVersionの実在IDだけを指し、CLI単独Graphでは`null`とする。`source_graph_version_id`／`source_graph_parent_version_id`をWireの`version_id`／`parent_version_id`へ写像し、Product由来でないときは両者nullを要求する。

#### フィールド

| Field | Type | 制約 |
|---|---|---|
| `kind` | `GraphKind` | DAG/CPDAG/PAG等の区別 |
| `nodes` | `tuple[Node,...]` | unique identity |
| `edges` | `tuple[EndpointEdge,...]` | endpoint/lag/identityをlossless |
| `temporal` | `TemporalConvention|None` | lagの符号・基準時刻 |
| `source_graph_version_id` | `str|None` | 実在するProduct GraphVersionを参照。自身はVersionを発行しない |
| `source_graph_parent_version_id` | `str|None` | 実在する親GraphVersion ID。source_graph_version_idがnullなら必ずnull |
| `provenance, content_hash` | `GraphProvenance, str` | Graph意味射影に一致するdigest |

#### Constructor / Factory

`from_canonical_json(raw:bytes)->GraphEvidence`：strict Graph Schema＋意味Validator。不可逆PAG→DAG変換、未知node/endpoint/重複edge/lag規約欠落を拒否。

#### メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `from_canonical_json(raw:bytes)` | `GraphEvidence` | pure strict graph decode | schema、endpoint、lag、hash不整合 |
| `canonical_payload()` | `Mapping[str,JsonValue]` | lossless domain serialization | invalid/incomplete Graph |

#### 処理仕様

`EndpointEdge(source,target,source_mark,target_mark,lag)`のmarkはTAIL/ARROW/CIRCLE。Node順序を反転する場合はendpointも対応させる。PAGのbidirected/circleをDAGへ暗黙確定しない。FIXEDは編集状態であってScientific Truthではない。未確定GraphからのEffect識別は独立のEstimand別識別証拠を要求。

#### I/O・連携・失敗処理

Graph Valueの純粋操作はI/Oなし。既存Productの`endpoint_source`／`endpoint_target`と新Wireの`source_mark`／`target_mark`は明示した双方向変換Adapterで対応し、端点の順序反転とmarkの交換を同時に行う。既存`graph_semantics.validate_graph_document`に新Wire dictを無変換で渡さない。内部`content_hash=SHA256(JCS(Graphからcontent_hash自身を除く意味射影))`、外部`ContentRef.sha256=SHA256(完成Graph File実bytes)`を**別々に検証**。RevisionとFIXはProductの既存GraphVersionServiceが所有する。

#### 検証

`DD-E11-GRAPH01` FCI PAG circle/arrow/bidirected・standalone両Version null、`GRAPH02` PCMCI lag、`GRAPH03` silent PAG→DAG拒否、`GRAPH04` 実在するProduct GraphVersion/parent参照と再識別。FR-186/196、AR-028/036/043。

### 3.2. `DiscoveryPort` — inline Field/Constructor/Method contract

#### 識別情報・責務

**Protocol配置：** `ariadne.scientific.ports.causal.DiscoveryPort`。PAG/CPDAG等の科学的Graph Discovery実行を型付きで抽象化する。既存Productの`ScientificCorePort.run_discovery(input_,output_dir)`は旧APIとして維持し、共通純粋Scientific Kernelへの互換Bridgeを通す。

#### フィールド

N/A：Protocol自身のInstance Fieldは持たない。

#### Constructor / Factory

N/A：具体Adapterは同一Method RegistryのCapabilityとFactoryから構築し、選択済Method/Backendに対してのみ実行する。

#### メソッド

```python
class DiscoveryPort(Protocol):
    def discover(self, request: ValidatedDiscoveryRequest, *, sink: StagingArtifactSink) -> DiscoveryGraphOutcome: ...
```

#### 処理仕様

`ValidatedDiscoveryRequest`はVerified Study/Question/Design/Dataset、選択済`BackendCapabilityRecord`、CI適格性、seedとInput Hashを保持する。Graph生成成功か、理由付き科学的negativeのいずれかを`DiscoveryGraphOutcome`で返す。P1-M06では`FciDiscoveryAdapter.preflight/execute`へ委譲する。Backend例外・schema不正を科学的negativeへ変換しない。

#### I/O・連携・失敗処理

Graph/DiagnosticsのFile出力先は`StagingArtifactSink`のみ。Product GraphVersion writer、DB/UoW、旧`Path`直接書込はこのPortの責務にしない。

#### 検証

`DD-E11-DISC01`：Registry→Port→Adapterの正例と異Method不一致拒否。`DISC02`：Graph成功と科学的negativeの排他性・dummy Effect禁止。`DISC03`：Staging限定と旧Product run_discovery署名回帰。独立PAG Science Oracleは`DD-E11-METH-P106`の責務。

### 3.3. `MethodCapabilityRegistry` — inline Field/Constructor/Method contract

#### 識別情報・責務

- **Class:** `ariadne.capabilities.causal.method_registry.MethodCapabilityRegistry`。Product ScientificCoreAdapterとは別契約である。
- **責務:** 41 Method IDごとのOperation/Estimand/Eligibility/Inference/Backend/Profileをstrictに選択し、Version/API capabilityを検証し、Adapter importを遅延させる。外部Libraryの既定推論を黙認しない。
- **責務外:** Estimator計算、Local FS publication、Customer Delivery LegalのPASS。
- **関連契約:** 30_63 Method41 allocation、23_41 §6〜7。

#### フィールド

配置：`ariadne.capabilities.causal.method_registry.MethodCapabilityRegistry`。Method IDごとにOperation、Estimand Family、Design/Eligibility、Backend ID、推論方式、Profile/Extra、Adapter Factoryを宣言。外部libraryはresolution後にlazy import。Methodが同じでも対象Estimand・inference configが異なれば別個の互換性判断を要する。

| Field | Type | 生成元 | 可変性／制約 |
| --- | --- | --- | --- |
| `descriptors` | `Mapping[str, MethodDescriptor]` | pinned Method41 Registry | Immutable; Method ID unique; target Estimand/Inference explicit |
| `backend_factories` | `Mapping[str, AdapterFactory]` | composition root | Immutable; import lazy; only eligible Method/Profile |
| `effective_env` | `RuntimeEnvironmentPort` | runtime injection | Observed installed version/API; no fake availability |
| `inference_registry` | `InferenceRegistry` | fixed Method-specific policy | Immutable, point-only vs confirmatory separated |

#### Constructor / Factory

- **Constructor:** `__init__(self, descriptors, backend_factories, effective_env, inference_registry)`. Validate unique IDs, declared Operation/Estimand and versioned descriptor schema; do not import optional modules.
- **Factory** is a collaborator of Registry; 独立実装を置く場合も 独立Factoryを設ける場合も同じMethod×Backend×Inference不変条件に従う。
- **Failure:** Invalid registry/duplicate ID/unsupported policy fails during preflight without selecting unrelated Method or importing missing Backend.

#### メソッド

~~~python
def describe(self, method_id: str) -> MethodDescriptor: ...
def resolve(self, method_id: str, backend_id: str, profile: str) -> BackendCapabilityRecord: ...
def load_adapter(self, capability: BackendCapabilityRecord) -> ScientificAdapter: ...
~~~

`describe`はpure metadata。`resolve`でDistribution metadata、実効API signature/Version、指定Methodの利用可能性・Inference availabilityを検査。`load_adapter`だけがoptional importを実行する。Unavailable時は当該Methodのtyped reasonとし、core起動や旧v2を破壊しない。`pyproject.toml`・universal `uv.lock`・実効runtime・SBOM・Legalは別軸で記録。

| Method | Observable contract | Side effects / exceptions |
| --- | --- | --- |
| `describe(method_id)` | pinned descriptor | pure; unknown ID typed rejection |
| `resolve(method_id, backend_id, profile)` | effective Capability Record | inspect distribution/API/version; unavailable reason, never auto fallback |
| `load_adapter(capability)` | scientifically eligible Adapter | only this method may lazy import; import failure localized as capability error |

#### 処理仕様

1. Resolve declared Method ID and operation/estimand eligibility from frozen descriptor.
2. Check profile/extras and **effective installed distribution+API version**, not just `pyproject.toml` declaration.
3. Check Method-specific inference availability for requested analysis_mode. Backend default is not evidence of valid CI.
4. Return typed supported/unavailable/unsupported with reasons. Only eligible selected capability permits actual lazy import; never fallback to other Method.
5. Export effective config/version/seed/algorithm facts for Manifest, not a pre-run Science PASS.

#### I/O・連携・失敗処理

- **Input:** MethodRequest, Backend ID/Profile, versioned method descriptors, effective runtime probe.
- **Output:** `MethodDescriptor`, `BackendCapabilityRecord`, `ScientificAdapter` only after eligibility; external estimator objects never enter Domain persistence.
- **No DB/FS mutation** from `describe`/`resolve`; `load_adapter` may import optional modules.
- **Errors:** unknown method, incompatible estimand/inference, missing extra, incompatible API signature, import failure. Each is typed and does not disable core or legacy v2 startup. Combined env/BLAS conflicts are not silently ignored.

#### 検証

`DD-E11-CAP01`ENV-BASE隔離、`CAP02`単独3Profile、`CAP03`Combined API parity、`CAP04`Versionとunsupported mode、`CAP05`transitive package有無とMethod選択区別、`CAP06`Customer Delivery legal blocked。

**関連ID:** DD-E11-CAP01〜CAP06、FR-185/194/195/196/197/202、NFR-028〜030/032、AR-034/040、BD01-F08/F09/F12。

## 4. Required implementation steps — G06/P01

1. **Entry:** Current G06のFrozen06/07/Pxx、Owner Coding Authorization、Source/lock full SHA、当該06のupstream 999とPxx依存Checkpointを確認してから実装。Valid Study/Method/Design/Data/Estimand/Backendを境界で検証。
2. `TIME_SERIES_GRAPH`はG01の静的PAGと異なるTemporal Graph Value。Variable IDとlag、同時時刻Edge、Endpoint uncertainty、時刻方向を明示したVersion/Schemaに保持。
3. 観測時刻の増加方向、lag符号（過去→現在の非負距離等）は**設計採用したConventionを明示するまで未固定**。timestamp/variable order/lag bounds/self edges/duplicate endpointsの検証を先行させ、silent sign swapを禁止。
4. PAG circle/bidirected/LPCMCIのlatent uncertaintyをDAGへ潰さず、GraphEvidence共通Hash/Version contractを再利用する。G01 GraphVersion writerとは別Writerを作らない。
5. **I/O/Failure:** Approved Method Adapter preflight→selected Backend（必要時lazy import）→typed Scientific Outcome→G01 Staging Publisher/Reader。Invalid config、合法的Scientific negative、不確定CI、Backend failureを分離し、Resultにeffective Method/Backend/Seed/Time/Design Evidenceを保存。
6. **Non-goals:** 旧v2 Public ABI、Web/API/DB/Worker、G01 GraphVersion/Publisherの再実装、未承認row export、Backend実測なしのScience PASSを禁止。

### 設計で定義済みのGraph／Quasi意味論（自己完結した実装規範）

以下は既存の詳細設計に記載された規則を本Packageへ直接展開したもの。Designの決定済み部分を不明事項としてAgentに再判断させない。実効Backend/API probe、独立Graph/Counterfactual Oracle、推論可用性の未実測は別にBLOCKEDとする。

- FCIはPAG circle、bidirected、ambiguous orientationを保持し、そこからDAGを想像してpoint estimateへ通さない。
- PCMCI/PCMCI+/LPCMCIはCI test family、max lag、contemporaneous link、endpoint mark、時間方向規約をserializeする。MetaDataの `lag=-1` 等は明示Convention無しには意味を持たせない。
- GraphOracleは構造上の同値類／可識別方向／adjacency・endpointを比較し、学習したGraphの不確定な向きを真DAGへ罰則無しに変換しない。

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P3-M01` | PCMCI | CI test/lag window、time-series order、graph |
| `P3-M02` | PCMCI+ | contemporaneous endpoint、CPDAG-like oracle |
| `P3-M03` | LPCMCI | PAG/latent/endpoint fidelity、lag |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

## 5. Method-by-Method DGP/Negative/Reference Obligations

このPackageは新Method IDの科学Kernelを追加しない。既存のG01〜G09 Method/ResultとTyped Portを再利用する。

**Proof boundary:** §5のDGP/NEG/REF/ACは独立に実証すべき義務であり、Fixture/Oracleの実在やPASSを意味しない。Backend出力を自己正解にせず、時系列Graph/Quasi Methodごとの独立Referenceと実測で検証する。FWER=.05/K/R/CI coverage/MC-SE未確定はBLOCKED。外部資料から推測して決めない。

## 6. Focused Verification Contract — WHAT, not physical filename

| Layer | Required behavior |
|---|---|
| unit | Value/Estimand/Method schema、negative、Hash/Status/No-False-PASS、pure Algorithm。 |
| contract | `Class.Method`入出力、Port/Backend Registry選択、typed evidence/Lineage、Version+Codec。 |
| integration | 必要な実Backend/CLI/FS/Atomic readback、optional Profile、既存Product v2回帰。 |
| scientific evidence | Method別DGP/NEG/independent reference、定量Simulation/coverage/MC-SE。 |

TestはLifecycle（enhancement/regression/characterization/benchmark/support/legacy）とLayer（unit/contract/integration/frontend/browser_e2e）を独立分類。新規は`tests/enhancement/enh_e11/g06/<layer>/`に原則配置、実Path/command/pytest collectionは40 Operatorがcurrent checkoutからdiscover。受入07をpathの文字列で置き換えない。Mock-onlyでreal Backend/FS/ScienceをPASSにしない。

### 6.1. Method-specific independent verification obligations

- §5のDGP/NEG/REF/DD IDを、Science/Status/Method-config/Source-hashに対応させる。ID一覧はFixture実在や科学的PASSの証拠ではない。
- **Positive and negative matrix:** `TIME_SERIES_GRAPH`はG01の静的PAGと異なるTemporal Graph Value。Variable IDとlag、同時時刻Edge、Endpoint uncertainty、時刻方向を明示したVersion/Schemaに保持。 観測時刻の増加方向、lag符号（過去→現在の非負距離等）は**設計採用したConventionを明示するまで未固定**。timestamp/variable order/lag bounds/self edges/duplicate endpointsの検証を先行させ、silent sign swapを禁止。 PAG circle/bidirected/LPCMCIのlatent uncertaintyをDAGへ潰さず、GraphEvidence共通Hash/Version contractを再利用する。G01 GraphVersion writerとは別Writerを作らない。
- Pure Value/Graph/Design→unit、Port/Codec/typed Reason→contract、実Backend/Tigramite/Quasi/CLI/Pub-Readback/legacy v2→integration。科学Graph/EffectのReferenceはBackend出力とは別に事前固定する。
- Effective backend API/version, Test fixture/Source/lock SHA, seed, Data/Time ordering, CI/SE handling, observed outcome, actual test collection/command, FAIL/BLOCKED causeをEvidenceへ記録。必須RuntimeやOracleが未確定ならBLOCKED。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** P02,P03。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、当該PxxのOptional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。本Pxxの依存契約・科学的Referenceが未解決なら当該ScopeだけをBLOCKEDとする。他Gateの未決を全Packageの一律停止条件にせず、Agentによる推測補完を禁止する。


## 8. Freeze-only review: unresolved decisions

**Self-contained:** §3は全ClassのField/Constructor/Public Method/I-Oを、§4は実装分岐を、§5〜6は必要なMethod/DGP/NEG/REFと検証を本文で保持する。**BLOCKED before Freeze:** Temporal lag sign/contemporaneous endpoint conventionとGraphValue serialization/discriminatorのFreeze。 他文書の参照をCoding Agentに必須とせず、設計空白はOwner決定まで止める。

## 9. OD-05 Owner-adopted Method Profile construction obligation

**Accepted authoring allocation (2026-11-19 JST):** G06/P01 is responsible for cross-cutting validation of the existing Method registry; it must not implement additional Method schemas or numerical adapters. Scientific constraints: CI-test/temporal lag/zero-lag/PCMCI+/LPCMCI endpoint, latent uncertainty. Retain the existing §§3–6 Class/Method/algorithm/DGP/NEG/REF/AC semantics. A profile must declare mandatory and conditional fields, type domains, effective Backend/API/Version, analysis_mode/inference eligibility, output status/artifact shape, and no implicit Backend defaults.

**Negative obligations:** unsupported method/profile/estimand, unknown fields, missing conditional fields, invalid Graph/Design/Question/DataRef identity, unavailable optional Backend, unsupported CI or invalid scientific assumptions are typed rejections; missing specific profile ⇒ `METHOD_PROFILE_UNAVAILABLE`. No silent fallback or `config={}` as a claim of support.

**Readiness:** This Owner decision allocates work; it does not assert that schemas, independent DGP/REF, Backend execution, K/R/MC-SE/coverage, Gate07/999, contract Freeze or Coding Authorization are complete. No new mathematical Target is adopted here.
