# ENH-E11 G06 P03 — temporal_bundle

**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G06 / **Package:** P03 / **Trial:** NOT_STARTED  
**Depends on Pxx:** P01,P02  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G06_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G06_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** TIME_SERIES_GRAPH/Graph lossless hash/readbackとFCI旧Graphへの回帰。

**Scope:** 本PackageのClass/Methodと、それらが必要とする契約/適格性/Result Evidenceに限定。**Gate全体の保護意味:** Temporal Graphのlag/endpoint不確実性を保持しPCMCI系をMethod別に実行する。

**科学/Designの必須制約:** time index/lag sign、contemporaneous/latentと独立Graph oracle必須。PAGをDAGへ勝手に変換しない。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** TIME_SERIES_GRAPH/Graph lossless hash/readbackとFCI旧Graphへの回帰。

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
| `LocalCausalUseCase` | `ariadne.capabilities.causal.local_execution.LocalCausalUseCase` | Port/Value/Facade integration (no duplicate implementation) | preflight(self,spec:ValidatedStudy,context:LocalRunContext)->PreflightReport / run(self,spec:ValidatedStudy,context:LocalRunContext)->LocalRunOutcome |
| `GraphEvidence` | `ariadne.causal.discovery.graph_evidence.GraphEvidence` | Port/Value/Facade integration (no duplicate implementation) | from_canonical_json(raw:bytes) / canonical_payload() |
| `LocalManifestReader` | `ariadne.interfaces.cli.local_causal.manifest_reader.LocalManifestReader` | Port/Value/Facade integration (no duplicate implementation) | read_run(trusted_root:TrustedLocalRoot,run_id:RunId) |

**Method Adapter signature policy:** 新Adapterは原則`preflight(self,request:ValidatedMethodRequest)->EligibilityOutcome`／`execute(self,request:ValidatedMethodRequest,*,sink:StagingArtifactSink)->TypedScientificOutcome`。上表で指定された既存`run(self,input_,output_dir)`はその署名を保持。PortはApplication→Scientific kernelへ向かい、CLI Layerに別の科学数値実装を作らない。本Pxx§3.1以降のClass定義がField/Constructor/Methodの規範であり、外部DDはprovenanceのみ。Design未確定箇所や実Backend ABIを補完せずBLOCKEDで停止する。

**Responsibility:** 本PackageはScientific Adapter数値本体を新規所有しない。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。

### 3. Standalone Class/Method contracts

以下をNormative Contractとして本Pxxに展開する。DDはProvenanceのみ、別06/07はCodingの不足判断を補完するSourceにしない。Class存在とLegacy ABIは実Sourceで確認し、設計Classと混同しない。

### 3.1. `LocalCausalUseCase` — inline Field/Constructor/Method contract

### 1.1. 識別情報・責務

- **Class:** `ariadne.capabilities.causal.local_execution.LocalCausalUseCase`。既存Product Stage runnerとは別のLocal Class契約である。
- **責務:** versioned Local Studyのpreflight→identification→method eligibility→adapter execution→staging→publish→readbackを順序付け、科学的Negativeとtechnical failureを混同しない。
- **責務外:** Scientific Estimatorの数学本体、Product DB/UoW/Worker/Web API、実行済み独立Science PASSの宣言。
- **関連契約:** 23_41 §3〜5、23_42 §2/6/7、30_61 §1〜5、30_60 §11〜12、30_62 §7。

### 1.2. フィールド

**Constructor-injected Port fields:**

| Field | Type | Value origin | Mutable / constraint |
| --- | --- | --- | --- |
| `refs` | `ContentReferencePort` | composition root | immutable; trusted-root hash-bound read |
| `capabilities` | `MethodCapabilityPort` | composition root | immutable; effective profile and no silent fallback |
| `discovery` | `DiscoveryPort` | composition root | immutable; selected capabilityに束縛されたGraph Discovery |
| `identifier` | `IdentificationPort` | composition root | immutable; Domain proof/negative outcome |
| `estimators` | `EstimatorPort` | composition root | immutable; typed scientific result to staging |
| `diagnostics` | `DiagnosticPort` | composition root | immutable; method-specific typed diagnostics |
| `reader` | `LocalManifestReaderPort` | composition root | immutable; independent committed run readback |
| `policy_verifier` | `LocalPolicyVerifierPort` | composition root | immutable; preauthorization from independent authority |
| `privacy` | `LocalPrivacyPolicyPort` | composition root | immutable; explicit row release decision |
| `publisher` | `LocalPublicationPort` | composition root | immutable; all writes staged |
| `runtime` | `RuntimeEnvironmentPort` | composition root | immutable; effective provenance not fabricated |
| `clock` | `ClockPort` | composition root | immutable; injected timestamp authority |

No shared mutable per-run state is retained in the use-case object; per-run staged artifacts/status are returned via typed RunOutcome or scoped Context. UseCaseのper-run状態非共有を不変条件とする。

**Application Context：** `ariadne.capabilities.causal.local_execution.LocalRunContext`は`root: TrustedLocalRoot`、`principal: LocalPrincipal`、`cli_row_flag: bool`、`policy_anchor: TrustedPolicyAnchor|None`を持つimmutable value。OS Root/Principalの型Authorityは`ariadne.shared.local_fs`、生成責務はCLI composition rootのTrustedRoot Factory。現行CLIの入力ContentRefと出力Bundleは同じRoot下の異なる相対keyで扱う。Policy AnchorはCLI composition rootがStudy外のsecure runtime trust configurationから取得する。G01集計専用のとき`policy_anchor=null`を許容するが、行出力要求では欠落を拒否する。Study YAMLからContextの信頼属性を構築してはならない。

**Application Port配置：** `ariadne.capabilities.causal.ports.content_ref.ContentReferencePort`、`ariadne.capabilities.causal.ports.local_io.LocalPublicationPort/LocalManifestReaderPort`、`ariadne.capabilities.causal.ports.local_policy.LocalPolicyVerifierPort`、`ariadne.capabilities.causal.ports.local_privacy.LocalPrivacyPolicyPort`。`LocalPrivacyPolicy` ConcreteはLocalPrivacyPolicyPortの実装であり、ApplicationはCLI Concreteをimportしない。Policy verifierはStudyと独立のTrust Anchorで事前承認証拠を検証する。

### 1.3. Constructor / Factory

配置：`ariadne.capabilities.causal.local_execution.LocalCausalUseCase`。`LocalConfigDecoder`は**CLI composition root**に属し、Strict parse/Version検証済み`ariadne.causal.design.study.ValidatedStudy`のみApplicationへ渡す（Application内で別のdecodeを暗黙に行わない）。
注入Port：`refs: ContentReferencePort`、`capabilities: MethodCapabilityPort`、`discovery: DiscoveryPort`、`identifier: IdentificationPort`、`estimators: EstimatorPort`、`diagnostics: DiagnosticPort`、`publisher: LocalPublicationPort`、`reader: LocalManifestReaderPort`、`policy_verifier: LocalPolicyVerifierPort`、`privacy: LocalPrivacyPolicyPort`、`runtime: RuntimeEnvironmentPort`、`clock: ClockPort`。Constructor時にoptional Backendをimportしない。

- **Constructor signature:** `__init__(self, *, refs: ContentReferencePort, capabilities: MethodCapabilityPort, discovery: DiscoveryPort, identifier: IdentificationPort, estimators: EstimatorPort, diagnostics: DiagnosticPort, publisher: LocalPublicationPort, reader: LocalManifestReaderPort, policy_verifier: LocalPolicyVerifierPort, privacy: LocalPrivacyPolicyPort, runtime: RuntimeEnvironmentPort, clock: ClockPort)`。公開ApplicationはPort抽象にのみ依存する。
- **Precondition:** Required Ports non-null and no optional scientific Backend import at construction. Factory wiring belongs to CLI adapter, not Product Web API. 失敗は契約に対応する型付きErrorとして返す。
- **Postcondition:** A reusable stateless orchestration instance. Constructors must not create run directories or claim science readiness.

### 1.4. メソッド

~~~python
def preflight(self, spec: ValidatedStudy, context: LocalRunContext) -> PreflightReport: ...
def run(self, spec: ValidatedStudy, context: LocalRunContext) -> LocalRunOutcome: ...
~~~

preflightはversion／secure Input Ref／static capability／privacy／pathと科学的適格性の検証可能範囲を返す。DGPや独立科学受入済みであると報告しない。

| Signature | Returns | Side effects / errors |
| --- | --- | --- |
| `preflight(self, spec: ValidatedStudy, context: LocalRunContext) -> PreflightReport` | capability/eligibility/input diagnostic | trusted input read permitted, **no** scientific execution or bundle publication; invalid version/refs typed |
| `run(self, spec: ValidatedStudy, context: LocalRunContext) -> LocalRunOutcome` | technical + scientific axes, committed ref or typed negative | backend execution only after validated eligibility; publication only via Publisher; errors preserve kind |

### 1.5. 処理仕様

1. CLI composition rootが`schema_version`を明示dispatchし、strict YAML/JSON parseで`ValidatedStudy`を構築。旧v2と無版はE11解釈禁止。ApplicationはValidatedStudyを受け取る（再検証するべきInput/Ref/Method/Privacyの意味検査は実行する）。
2. Trusted Root配下でQuestion/Design/Graph/Dataset/Upstream Refをsecure openし、bytes hash・Graph/Estimand/Designの意味上の一致を検査。
3. Method IDのOperation/Estimand/Backend/extra/API versionをresolve。他Method/Backendへのsilent fallback禁止。
4. 選択済CapabilityをOperation別のValidated Requestに束縛する。`DISCOVER`では`DiscoveryPort.discover(ValidatedDiscoveryRequest, *, sink)`を呼び、同一Method Registryから解決したFCI Adapterを使用する。Identificationを要求せず、未確定Graphを識別済みと扱わない。その他OperationはIdentifier/Estimator/Diagnostic Portへ明示dispatchする。
5. Data EligibilityとEstimator Requestを再評価。NOT_IDENTIFIED、REQUIRES_REVIEW、PARTIALLY_IDENTIFIEDの自動点推定禁止。列挙された緩和可能WARNのみ理由付きoverride可。
6. Adapter実行。Outputはstaging sink限定。Method-specific inference、診断、scientific negative、effective env/seed/foldを収集。
7. 本書§2BのOperation別必須・禁止Artifactとschema_dispatchを直接検証し、typed Graph/Identification/Effect/Diagnostics、Status/Manifestを生成。`context.policy_anchor`を使って独立Policy verifierが取得した承認証拠、Study、CLI row flag、`context.principal`・Output shapeを`LocalPrivacyPolicyPort.authorize`で照合し、staging seal→一括publish→独立Reader readbackを行う。
8. `LocalRunOutcome`は `technical_status` と `identification_status/point/inference/science_acceptance` を別軸として返す。

**Precondition:** Input Spec passed strict schema/version check and trusted content refs. **Postcondition:** either immutable fully validated bundle with commit marker, or typed non-success/negative without false completed marker. Method/estimand/Graph conditional result is never guessed from a Backend label.

### 1.6. I/O・連携・失敗処理

`technical_status=COMPLETED`はVerified Manifestとcommit markerを持つ。Science negativeでも技術的には完了しうる。Config/入力/Backend/Publication exceptionをScientific Negativeに潰さない。途中失敗はcompleted marker無し。無効な上流proofではEstimatorを呼ばない。

- **I/O:** reads via ContentReferencePort, writes only via StagingArtifactSink/LocalPublicationPort. Each run has pinned request/content hash and effective API/seed evidence.
- **Transactions:** This is a Local FS unit, not a Product UoW. Publication atomicity and crash recovery specified in §3 and IF 23_42.
- **Errors:** invalid config/schema, missing/mismatched refs, unsupported capability, scientific negative, runtime failure and publication failure remain separately typed. **Retry/rollback:** idempotent same-hash readback allowed; another request hash with same run ID rejected; uncommitted staging never advertised as success.

### 1.7. 検証

`DD-E11-RUN01`正常pipeline、`RUN02`非識別でEstimator未呼出、`RUN03`wrong Backend/Estimand、`RUN04`confirmatory unsupported CI、`RUN05`Graph再固定は新識別、`RUN06`旧v2挙動不変、`RUN07`abort時はuncommitted。

| Acceptance | Required |
| --- | --- |
| Unit/Contract | Preflight performs zero Backend scientific calls; run calls Estimator only for proven eligible request; payload/status axes preserved |
| Negative | wrong version, hash mismatch, Graph uncertainty, unsupported CI, unavailable extra, no row export flag, publication failure |
| Regression | old v2 identify/estimate/refute/sensitivity and existing Product Stage runner unchanged |

**検証契約:** DD-E11-RUN01〜RUN07。関連要件：FR-185/187/201/202/203、NFR-029/032/036、AR-029/034/040。

### 3.2. `GraphEvidence` — inline Field/Constructor/Method contract

#### 1.1.1. 識別情報・責務

**Class / module:** `ariadne.causal.discovery.graph_evidence.GraphEvidence`。PAG/CPDAG/DAG/temporal等の科学的Graph Evidenceを保持するimmutable Value。Product `GraphVersion`のVersion作成・編集・FIX権限を持たない。Wireの`version_id`はProduct GraphVersionの実在IDだけを指し、CLI単独Graphでは`null`とする。`source_graph_version_id`／`source_graph_parent_version_id`をWireの`version_id`／`parent_version_id`へ写像し、Product由来でないときは両者nullを要求する。

#### 1.1.2. フィールド

| Field | Type | 制約 |
|---|---|---|
| `kind` | `GraphKind` | DAG/CPDAG/PAG等の区別 |
| `nodes` | `tuple[Node,...]` | unique identity |
| `edges` | `tuple[EndpointEdge,...]` | endpoint/lag/identityをlossless |
| `temporal` | `TemporalConvention|None` | lagの符号・基準時刻 |
| `source_graph_version_id` | `str|None` | 実在するProduct GraphVersionを参照。自身はVersionを発行しない |
| `source_graph_parent_version_id` | `str|None` | 実在する親GraphVersion ID。source_graph_version_idがnullなら必ずnull |
| `provenance, content_hash` | `GraphProvenance, str` | Graph意味射影に一致するdigest |

#### 1.1.3. Constructor / Factory

`from_canonical_json(raw:bytes)->GraphEvidence`：strict Graph Schema＋意味Validator。不可逆PAG→DAG変換、未知node/endpoint/重複edge/lag規約欠落を拒否。

#### 1.1.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `from_canonical_json(raw:bytes)` | `GraphEvidence` | pure strict graph decode | schema、endpoint、lag、hash不整合 |
| `canonical_payload()` | `Mapping[str,JsonValue]` | lossless domain serialization | invalid/incomplete Graph |

#### 1.1.5. 処理仕様

`EndpointEdge(source,target,source_mark,target_mark,lag)`のmarkはTAIL/ARROW/CIRCLE。Node順序を反転する場合はendpointも対応させる。PAGのbidirected/circleをDAGへ暗黙確定しない。FIXEDは編集状態であってScientific Truthではない。未確定GraphからのEffect識別は独立のEstimand別識別証拠を要求。

#### 1.1.6. I/O・連携・失敗処理

Graph Valueの純粋操作はI/Oなし。既存Productの`endpoint_source`／`endpoint_target`と新Wireの`source_mark`／`target_mark`は明示した双方向変換Adapterで対応し、端点の順序反転とmarkの交換を同時に行う。既存`graph_semantics.validate_graph_document`に新Wire dictを無変換で渡さない。内部`content_hash=SHA256(JCS(Graphからcontent_hash自身を除く意味射影))`、外部`ContentRef.sha256=SHA256(完成Graph File実bytes)`を**別々に検証**。RevisionとFIXはProductの既存GraphVersionServiceが所有する。

#### 1.1.7. 検証

`DD-E11-GRAPH01` FCI PAG circle/arrow/bidirected・standalone両Version null、`GRAPH02` PCMCI lag、`GRAPH03` silent PAG→DAG拒否、`GRAPH04` 実在するProduct GraphVersion/parent参照と再識別。FR-186/196、AR-028/036/043。

### 3.3. `LocalManifestReader` — inline Field/Constructor/Method contract

### 5.1. 識別情報・責務

- **Class/Module:** `ariadne.interfaces.cli.local_causal.manifest_reader.LocalManifestReader`。
- **責務:** committed runをMarker→Manifest→Artifactの順に検証し、`VerifiedLocalRun`を返す。存在だけでCOMMITTEDと判断しない。
- **責務外:** publish、legacy v2の無断E11解釈、科学的Oracle計算、実Artifactの編集。
- **参照:** IF `23_42` §6〜8。

### 5.2. フィールド

| Field | Type | Origin | Constraint |
| --- | --- | --- | --- |
| Instance fields | N/A（stateless Reader） | N/A | trusted root/run IDはper-call引数。Cacheが必要なら原本Root・run IDとhash一致を保持し、未検証値の再利用を禁止 |

### 5.3. Constructor / Factory

- `__init__()`は特別な依存なし（read_runへ検証済み`TrustedLocalRoot`を明示注入するstateless API）。共通`LocalManifestReaderPort.verify(root,run_id)`はConcrete `read_run`へ委譲するAdapter。`Path`単独をTrustedRootに昇格しない。
- Reader instanceに暗黙のworking directory・current Project・Product DB／OS principalを仮定させない。

### 5.4. メソッド

| Signature | Result | Side effect / failure |
| --- | --- | --- |
| `read_run(self, trusted_root: TrustedLocalRoot, run_id: RunId) -> VerifiedLocalRun` | Verified manifest and artifact descriptors | secure read only; marker/hash/version/root/permissions fail-closed |

### 5.5. 処理仕様

1. Trusted root・run_idとlocal execution principalを検証し、run directoryにsecure open。
2. `_COMMITTED.json`存在/strict schema/version/request hashを確認。
3. `manifest.json`を同一安全dirfd scopeでopen、markerに保存されたManifest SHA256と照合し、`LocalRunManifest`をstrict decode。
4. Artifactの相対key重複、SHA256/size/MediaType、privacy class、必要なLineage Refの一致を検査。
5. Private Parquetには出力Policy/OS principalの許可なしでrow-level bytesを返さない。
6. 未検証・partial・legacy・corruptのいずれでも`VerifiedLocalRun`を返さない。

### 5.6. I/O・連携・失敗処理

- **Caller:** Local causal UseCaseのReadback／CLI status command、publisherのpublication verification。
- **I/O:** Trusted Rootからread-only。symlink/TOCTOUとstale marker防止のためopenされた同一File Descriptorに対しhashを確認。
- **Errors:** `NOT_COMMITTED`, `MANIFEST_HASH_MISMATCH`, `ARTIFACT_HASH_MISMATCH`, `VERSION_UNSUPPORTED`, `PRIVATE_ARTIFACT_DENIED`等を区分。
- **Retry:** 不完全runを勝手に修復／削除しない。既存同hash runの再利用は完全Readback PASSに限定。

### 5.7. 検証

`DD-E11-READ01` valid; `READ02` marker missing; `READ03` corrupted bytes/size; `READ04` wrong version; `READ05` individual export suppression; `READ06` old v2 not E11; `READ07` symlink/path race。関連要件：IF IO-E11-01〜09、FR-201〜203、NFR-031/032、BD01-F03/F05/F06/F12。

## 4. Required implementation steps — G06/P03

1. **Entry:** Current G06のFrozen06/07/Pxx、Owner Coding Authorization、Source/lock full SHA、当該06のupstream 999とPxx依存Checkpointを確認してから実装。Valid Study/Method/Design/Data/Estimand/Backendを境界で検証。
2. Temporal Design/GraphEvidence/lag/endpointはtyped ResultとVersioned `TIME_SERIES_GRAPH`で保存し、静的PAG/Effectを捏造しない。
3. G01のStagingSink/Manifest/Publisher/ReaderにTemporal Graph profileを追加し、Method・effective CI・time index/lag convention・Backend/seedをArtifact metadataに保持。
4. ReaderはContentRef full bytes、canonical Graph payload、Endpoint/lag/variable orderingとVersionを再検証し、不一致はGraph corruptionとしてfail-closed。
5. **I/O/Failure:** Approved Method Adapter preflight→selected Backend（必要時lazy import）→typed Scientific Outcome→G01 Staging Publisher/Reader。Invalid config、合法的Scientific negative、不確定CI、Backend failureを分離し、Resultにeffective Method/Backend/Seed/Time/Design Evidenceを保存。
6. **Non-goals:** 旧v2 Public ABI、Web/API/DB/Worker、G01 GraphVersion/Publisherの再実装、未承認row export、Backend実測なしのScience PASSを禁止。

### 設計で定義済みのGraph／Quasi意味論（自己完結した実装規範）

以下は既存の詳細設計に記載された規則を本Packageへ直接展開したもの。Designの決定済み部分を不明事項としてAgentに再判断させない。実効Backend/API probe、独立Graph/Counterfactual Oracle、推論可用性の未実測は別にBLOCKEDとする。

- FCIはPAG circle、bidirected、ambiguous orientationを保持し、そこからDAGを想像してpoint estimateへ通さない。
- PCMCI/PCMCI+/LPCMCIはCI test family、max lag、contemporaneous link、endpoint mark、時間方向規約をserializeする。MetaDataの `lag=-1` 等は明示Convention無しには意味を持たせない。
- GraphOracleは構造上の同値類／可識別方向／adjacency・endpointを比較し、学習したGraphの不確定な向きを真DAGへ罰則無しに変換しない。

`LocalRunManifest.to_canonical_bytes`は`e11-json-jcs-rfc8785/1`のstrict JCSで符号化しProductの`hash_mapping(default=str)`は用いない。request hashはValidatedStudy意味射影、Graph内部hashは自己fieldを除く意味射影、ContentRefとMarkerが指すManifest hashは保存実bytes。Markerはinventory外に置き、非Effect操作の`schema_dispatch.result=null`を認める。これだけでIDENTIFY/REFUTE/SENSITIVITY/DIAGNOSEの成果物を省略してよいことにはならない。23_42 §2.1のOperation Bundle ValidatorがGraph/Identification/Effect/Diagnosticsの必須性、Status、Method、upstream hashを結合検証する。

Concrete `LocalManifestReader.read_run(trusted_root:TrustedLocalRoot,run_id:RunId)`は公開`LocalManifestReaderPort.verify(*,root:TrustedLocalRoot,run_id:RunId)`から委譲される。Marker→Manifest→Artifact bytes/type/hash/size→cross-refsとPrivacyを検証する。入力Schema不正はexit2、公開済みbundle readback破損はphase=PUBLICATIONのexit5。修復・自動削除は行わない。

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
- **Positive and negative matrix:** Temporal Design/GraphEvidence/lag/endpointはtyped ResultとVersioned `TIME_SERIES_GRAPH`で保存し、静的PAG/Effectを捏造しない。 G01のStagingSink/Manifest/Publisher/ReaderにTemporal Graph profileを追加し、Method・effective CI・time index/lag convention・Backend/seedをArtifact metadataに保持。 ReaderはContentRef full bytes、canonical Graph payload、Endpoint/lag/variable orderingとVersionを再検証し、不一致はGraph corruptionとしてfail-closed。
- Pure Value/Graph/Design→unit、Port/Codec/typed Reason→contract、実Backend/Tigramite/Quasi/CLI/Pub-Readback/legacy v2→integration。科学Graph/EffectのReferenceはBackend出力とは別に事前固定する。
- Effective backend API/version, Test fixture/Source/lock SHA, seed, Data/Time ordering, CI/SE handling, observed outcome, actual test collection/command, FAIL/BLOCKED causeをEvidenceへ記録。必須RuntimeやOracleが未確定ならBLOCKED。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** 全required Pxx完了後Candidate Assembly。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、Optional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。G05 Row Writer/Trust Anchor等の設計不在、G02 IV target、G08 AR独立reference等を推測で解決しない。


## 8. Freeze-only review: unresolved decisions

**Self-contained:** §3は全ClassのField/Constructor/Public Method/I-Oを、§4は実装分岐を、§5〜6は必要なMethod/DGP/NEG/REFと検証を本文で保持する。**BLOCKED before Freeze:** Temporal Result/Graph codec profile、Reader/Manifest schema・source hashの確定。 他文書の参照をCoding Agentに必須とせず、設計空白はOwner決定まで止める。
