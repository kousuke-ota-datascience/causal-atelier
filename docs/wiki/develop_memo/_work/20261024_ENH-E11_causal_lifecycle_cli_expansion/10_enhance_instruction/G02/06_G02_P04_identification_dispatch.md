# ENH-E11 G02 P04 — identification_dispatch

**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G02 / **Package:** P04 / **Trial:** NOT_STARTED  
**Depends on Pxx:** P01,P02,P03  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G02_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G02_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** IDENTIFY/ESTIMATEのOperation別必須Bundleと未識別時Estimator未呼出、旧v2互換を実証。

**Scope:** 本PackageのClass/Methodと、それらが必要とする契約/適格性/Result Evidenceに限定。**Gate全体の保護意味:** Native/DoWhy識別、推定適格性、FD-A限定線形効果を安全に区別する。

**科学/Designの必須制約:** P1-M05はOwner採用の`B0_BINARY_IV`・二値Z/A無調整complier `LATE_COMPLIER`の**条件付き識別のみ**。実効DoWhy IV式・Graph/Design仮定・Hashを明示的に検証し、display labelからLATEへcastしない。Method Profile/Backend/独立Scienceは未実証。 FD-A識別成立と数値推定成立は別。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** IDENTIFY/ESTIMATEのOperation別必須Bundleと未識別時Estimator未呼出、旧v2互換を実証。

### 2A. 既存SourceとのABI境界（HEAD `2cf28f59a324`で実体を確認）
- **実在する公開API:** `src/ariadne/scientific/core_adapter.py`の`ScientificCoreAdapter.run_identification(self, input_: IdentificationInput, output_dir: Path) -> list[ScientificResultDescriptor]`は`src/ariadne/scientific/identification/adapter.py`の`IdentificationAdapter.run(self, input_: IdentificationInput, output_dir: Path) -> list[ScientificResultDescriptor]`へ委譲する。後者の既存Randomized/Backdoor処理を再利用する。DoWhy IV/Frontdoor数値推定/MethodCapabilityRegistryの存在は、このABIだけからは導けない。
- **旧と新は異なる契約:** 上記`run(..., output_dir:Path)`は既存Productのpath-based API。`IdentificationPort.identify(ValidatedIdentificationRequest)->IdentificationOutcome`、`EstimatorPort.estimate(..., *, sink:StagingArtifactSink)->EffectOutcome`はE11の**設計中**の型付きPortであり、既存実装済みと仮定しない。既存旧API/旧DTO/旧Path Writerを変更・無検証cast・新型付きPortから直接公開先へ出力することは禁止。共通の純粋Scientific Kernelを通す互換Bridgeで、旧呼出しを不変に保ち、E11側は検証済Request/typed responseとstaging sinkで完結させる。
- **Ownership:** G01で設ける共通Local Facade/Registry/Publisher/Reader/GraphVersion契約を各Packageが再定義しない。本Packageで新設するAdapterだけを§3/4に従い実装。実Sourceとの署名差・Facade owner未定・Backend config未承認は`BLOCKED_CONTRACT_AMBIGUITY`としてCoding開始前に報告し、外部設計から推測して署名を補完しない。

### 2B. Operation別Artifact/Schema/Publisher契約（実行規範）
| Operation | 成功時に必須 | 禁止・負例 |
|---|---|---|
| DISCOVER | `study.json`、`status.json`、Graph生成時`graph.json` | `result.json`禁止。Graph無しの正当な科学負例は`diagnostics.json`＋非空reason、`schema_dispatch.graph=null`。Backend技術失敗を科学的negativeに変換しない |
| IDENTIFY | `study.json`、`status.json`、`identification.json` | `result.json`禁止。識別/非識別ともGraph・Design・Estimand・Proofのhashを照合する |
| ESTIMATE | `study.json`、`status.json`、`result.json` | `schema_dispatch.result=e11-local-effect-result/1`。無推定のpointはnull＋typed reason、仮の推定値禁止 |
| REFUTE/SENSITIVITY/DIAGNOSE | `study.json`、`status.json`、`diagnostics.json` | Effect再発行禁止。元Effect/Graph/Design hash、seed、適用条件を必ず照合 |

全Operationで`manifest.json`（`e11-local-manifest/1`）と`_COMMITTED.json`（`e11-commit/1`）を必須とし、両者はartifact inventory外。Inventoryには実Artifactの相対POSIX key・SHA256・bytes size・MediaType・Privacyを列挙。`schema_dispatch.result`はESTIMATE以外null。Readerはcommit marker→manifest実bytes hash→artifact bytes/hash/size→Operation別必須/禁止・upstream content hashを同一TrustedRoot内で検査する。`request_hash=SHA256(JCS(validated typed Study JSON))`、manifestは自己hashを持たず、markerがmanifestの実bytes hashを保持する。Stageのみからatomic no-clobber publishし、既存G01のPublisher/Readerを再利用。行レベルParquetの作成はG05の独立事前承認検証以前は禁止。

## 3. Class Placement, Signature, Reuse, Dependency Direction

| Class/Port | Designed module (DD30_61〜63) | Ownership boundary | Exact approved/design signature |
|---|---|---|---|
| `LocalCausalUseCase` | `ariadne.capabilities.causal.local_execution.LocalCausalUseCase` | Port/Value/Facade integration (no duplicate implementation) | preflight(self,spec:ValidatedStudy,context:LocalRunContext)->PreflightReport / run(self,spec:ValidatedStudy,context:LocalRunContext)->LocalRunOutcome |
| `IdentificationPort` | `ariadne.scientific.ports.causal.IdentificationPort` | Port/Value/Facade integration (no duplicate implementation) | identify(self, request:ValidatedIdentificationRequest) -> IdentificationOutcome |
| `EstimatorPort` | `ariadne.scientific.ports.causal.EstimatorPort` | Port/Value/Facade integration (no duplicate implementation) | estimate(self, request:ValidatedEstimatorRequest, *, sink:StagingArtifactSink) -> EffectOutcome |
| `LocalRunManifest` | `ariadne.interfaces.cli.local_causal.manifest.LocalRunManifest` | Port/Value/Facade integration (no duplicate implementation) | to_canonical_bytes() |

**Class/Method signature authority:** 本Pxx §3.1以降の埋込契約が各ClassのFields/Constructor/Public Method/Pre-Post/Failureの一次規範である。Method Adapterを本Packageが所有する場合のみそのMethodのpreflight/executeを実装し、既存run ABIは変更しない。統合専用Packageが新Adapterを創作してはならず、DomainからCLI Concreteへ逆依存しない。

**Responsibility:** 本PackageはScientific Adapter数値本体を新規所有しない。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。



### 3. Embedded class contracts — no external normative dependency

以下のClass定義は実装対象を自ら規定する。DD30_61/62/63へのPathはprovenanceのみであり、Coding Agentに外部DDを読んで仕様を補完させない。設計Classは実装済みを意味しない。既存実装は開始時に現実のmodule/ABIを検証し、衝突があればBLOCKEDとしてGate Freeze前に解決する。

### 3.1. `LocalCausalUseCase` — embedded executable class contract

#### 識別情報・責務

- **Class:** `ariadne.capabilities.causal.local_execution.LocalCausalUseCase`。既存Product Stage runnerとは別のLocal Class契約である。
- **責務:** versioned Local Studyのpreflight→identification→method eligibility→adapter execution→staging→publish→readbackを順序付け、科学的Negativeとtechnical failureを混同しない。
- **責務外:** Scientific Estimatorの数学本体、Product DB/UoW/Worker/Web API、実行済み独立Science PASSの宣言。
- **関連契約:** 23_41 §3〜5、23_42 §2/6/7、30_61 §1〜5、30_60 §11〜12、30_62 §7。

#### フィールド

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
| `privacy` | `LocalPrivacyPolicyPort` | composition root | immutable; explicit row release decision |
| `publisher` | `LocalPublicationPort` | composition root | immutable; all writes staged |
| `runtime` | `RuntimeEnvironmentPort` | composition root | immutable; effective provenance not fabricated |
| `clock` | `ClockPort` | composition root | immutable; injected timestamp authority |

No shared mutable per-run state is retained in the use-case object; per-run staged artifacts/status are returned via typed RunOutcome or scoped Context. UseCaseのper-run状態非共有を不変条件とする。

**Application Context：** `ariadne.capabilities.causal.local_execution.LocalRunContext`は`root:TrustedLocalRoot`、`principal:LocalPrincipal`のみ保持。CLI composition rootが実EUID/Private Rootを検証し、行出力はG05以外拒否する。署名Policy Anchorや追加CLI Flagは不要。

**Application Port配置：** `ariadne.capabilities.causal.ports.content_ref.ContentReferencePort`、`ariadne.capabilities.causal.ports.local_io.LocalPublicationPort/LocalManifestReaderPort`、`ariadne.capabilities.causal.ports.local_privacy.LocalPrivacyPolicyPort`。`LocalPrivacyPolicy` ConcreteはLocalPrivacyPolicyPortの実装であり、ApplicationはCLI Concreteをimportしない。第三者署名VerifierはLocal CLIの現行契約に存在しない。

#### Constructor / Factory

配置：`ariadne.capabilities.causal.local_execution.LocalCausalUseCase`。`LocalConfigDecoder`は**CLI composition root**に属し、Strict parse/Version検証済み`ariadne.causal.design.study.ValidatedStudy`のみApplicationへ渡す（Application内で別のdecodeを暗黙に行わない）。
注入Port：`refs: ContentReferencePort`、`capabilities: MethodCapabilityPort`、`discovery: DiscoveryPort`、`identifier: IdentificationPort`、`estimators: EstimatorPort`、`diagnostics: DiagnosticPort`、`publisher: LocalPublicationPort`、`reader: LocalManifestReaderPort`、`privacy: LocalPrivacyPolicyPort`、`runtime: RuntimeEnvironmentPort`、`clock: ClockPort`。Constructor時にoptional Backendをimportしない。

- **Constructor signature:** `__init__(self, *, refs: ContentReferencePort, capabilities: MethodCapabilityPort, discovery: DiscoveryPort, identifier: IdentificationPort, estimators: EstimatorPort, diagnostics: DiagnosticPort, publisher: LocalPublicationPort, reader: LocalManifestReaderPort, privacy: LocalPrivacyPolicyPort, runtime: RuntimeEnvironmentPort, clock: ClockPort)`。公開ApplicationはPort抽象にのみ依存する。
- **Precondition:** Required Ports non-null and no optional scientific Backend import at construction. Factory wiring belongs to CLI adapter, not Product Web API. 失敗は契約に対応する型付きErrorとして返す。
- **Postcondition:** A reusable stateless orchestration instance. Constructors must not create run directories or claim science readiness.

#### メソッド

~~~python
def preflight(self, spec: ValidatedStudy, context: LocalRunContext) -> PreflightReport: ...
def run(self, spec: ValidatedStudy, context: LocalRunContext) -> LocalRunOutcome: ...
~~~

preflightはversion／secure Input Ref／static capability／privacy／pathと科学的適格性の検証可能範囲を返す。DGPや独立科学受入済みであると報告しない。

| Signature | Returns | Side effects / errors |
| --- | --- | --- |
| `preflight(self, spec: ValidatedStudy, context: LocalRunContext) -> PreflightReport` | capability/eligibility/input diagnostic | trusted input read permitted, **no** scientific execution or bundle publication; invalid version/refs typed |
| `run(self, spec: ValidatedStudy, context: LocalRunContext) -> LocalRunOutcome` | technical + scientific axes, committed ref or typed negative | backend execution only after validated eligibility; publication only via Publisher; errors preserve kind |

#### 処理仕様

1. CLI composition rootが`schema_version`を明示dispatchし、strict YAML/JSON parseで`ValidatedStudy`を構築。旧v2と無版はE11解釈禁止。ApplicationはValidatedStudyを受け取る（再検証するべきInput/Ref/Method/Privacyの意味検査は実行する）。
2. Trusted Root配下でQuestion/Design/Graph/Dataset/Upstream Refをsecure openし、bytes hash・Graph/Estimand/Designの意味上の一致を検査。
3. Method IDのOperation/Estimand/Backend/extra/API versionをresolve。他Method/Backendへのsilent fallback禁止。
4. 選択済CapabilityをOperation別のValidated Requestに束縛する。`DISCOVER`では`DiscoveryPort.discover(ValidatedDiscoveryRequest, *, sink)`を呼び、同一Method Registryから解決したFCI Adapterを使用する。Identificationを要求せず、未確定Graphを識別済みと扱わない。その他OperationはIdentifier/Estimator/Diagnostic Portへ明示dispatchする。
5. Data EligibilityとEstimator Requestを再評価。NOT_IDENTIFIED、REQUIRES_REVIEW、PARTIALLY_IDENTIFIEDの自動点推定禁止。列挙された緩和可能WARNのみ理由付きoverride可。
6. Adapter実行。Outputはstaging sink限定。Method-specific inference、診断、scientific negative、effective env/seed/foldを収集。
7. 本書§2BのOperation別必須・禁止Artifactとschema_dispatchを直接検証し、typed Graph/Identification/Effect/Diagnostics、Status/Manifestを生成。ValidatedStudy、context.root/principal、Method OutputShapeを`LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)`で照合し、staging seal→一括publish→独立Reader readbackを行う。
8. `LocalRunOutcome`は `technical_status` と `identification_status/point/inference/science_acceptance` を別軸として返す。

**Precondition:** Input Spec passed strict schema/version check and trusted content refs. **Postcondition:** either immutable fully validated bundle with commit marker, or typed non-success/negative without false completed marker. Method/estimand/Graph conditional result is never guessed from a Backend label.

#### I/O・連携・失敗処理

`technical_status=COMPLETED`はVerified Manifestとcommit markerを持つ。Science negativeでも技術的には完了しうる。Config/入力/Backend/Publication exceptionをScientific Negativeに潰さない。途中失敗はcompleted marker無し。無効な上流proofではEstimatorを呼ばない。

- **I/O:** reads via ContentReferencePort, writes only via StagingArtifactSink/LocalPublicationPort. Each run has pinned request/content hash and effective API/seed evidence.
- **Transactions:** This is a Local FS unit, not a Product UoW. Publication atomicity and crash recovery specified in §3 and IF 23_42.
- **Errors:** invalid config/schema, missing/mismatched refs, unsupported capability, scientific negative, runtime failure and publication failure remain separately typed. **Retry/rollback:** idempotent same-hash readback allowed; another request hash with same run ID rejected; uncommitted staging never advertised as success.

#### 検証

`DD-E11-RUN01`正常pipeline、`RUN02`非識別でEstimator未呼出、`RUN03`wrong Backend/Estimand、`RUN04`confirmatory unsupported CI、`RUN05`Graph再固定は新識別、`RUN06`旧v2挙動不変、`RUN07`abort時はuncommitted。

| Acceptance | Required |
| --- | --- |
| Unit/Contract | Preflight performs zero Backend scientific calls; run calls Estimator only for proven eligible request; payload/status axes preserved |
| Negative | wrong version, hash mismatch, Graph uncertainty, unsupported CI, unavailable extra, no row export flag, publication failure |
| Regression | old v2 identify/estimate/refute/sensitivity and existing Product Stage runner unchanged |

**検証契約:** DD-E11-RUN01〜RUN07。関連要件：FR-185/187/201/202/203、NFR-029/032/036、AR-029/034/040。

### 3.2. `IdentificationPort` — embedded executable class contract

#### 識別情報・責務

**Protocol配置：ariadne.scientific.ports.causal.IdentificationPort。** 既存Product `ScientificCorePort`のv2メソッドを保持し、旧APIと型付きPortは共通科学計算を用いる互換Bridgeで接続する。

#### フィールド

N/A：Protocol自身はinstance fieldを所有しない。

#### Constructor / Factory

N/A：Protocolに具体Factoryはない。Concreteの依存関係注入はAdapterの責務。

#### メソッド

```python
class IdentificationPort(Protocol):
    def identify(self, request: ValidatedIdentificationRequest) -> IdentificationOutcome: ...
```

#### 処理仕様

IdentificationとEvidenceの意味を守り、非識別をIDENTIFIEDと偽装しない。科学的PreconditionはWeb/CLI共通であり、CLI optionやHTTP状態ではない。

#### I/O・連携・失敗処理

Protocol本体はI/Oなし。Concrete Adapterは本Packageの§3/§4で明示された所有Classのみが実装し、選択は単一MethodCapabilityPortから行う。validated request→typed outcomeを守り、外部DDの参照を実装規範の代用にしない。配置やOwnerが本Packageで決まらない場合はBLOCKEDとして新Facadeを創作しない。

#### 検証

DD-E11-ID01〜04。

### 3.3. `EstimatorPort` — embedded executable class contract

#### 識別情報・責務

**Protocol配置：ariadne.scientific.ports.causal.EstimatorPort。** 既存Product `ScientificCorePort`のv2メソッドを保持し、旧APIと型付きPortは共通科学計算を用いる互換Bridgeで接続する。

#### フィールド

N/A：Protocol自身はinstance fieldを所有しない。

#### Constructor / Factory

N/A：Protocolに具体Factoryはない。Concreteの依存関係注入はAdapterの責務。

#### メソッド

```python
class EstimatorPort(Protocol):
    def estimate(self, request: ValidatedEstimatorRequest, *, sink: StagingArtifactSink) -> EffectOutcome: ...
```

#### 処理仕様

識別・Method適格なRequestのみ実行し、ArtifactをStagingSinkへ限定。科学的PreconditionはWeb/CLI共通であり、CLI optionやHTTP状態ではない。

#### I/O・連携・失敗処理

Protocol本体はI/Oなし。Concrete Adapterは本Packageの§3/§4で明示された所有Classのみが実装し、選択は単一MethodCapabilityPortから行う。validated request→typed outcomeを守り、外部DDの参照を実装規範の代用にしない。配置やOwnerが本Packageで決まらない場合はBLOCKEDとして新Facadeを創作しない。

#### 検証

DD-E11-EFF01〜05。

### 3.4. `LocalRunManifest` — embedded executable class contract

#### 識別情報・責務

- **Class/Module:** `ariadne.interfaces.cli.local_causal.manifest.LocalRunManifest`、immutable typed DTO。
- **責務:** 1 Local runのidentity、lineage、Method/Science/Runtime、artifact inventoryをversioned schemaで保持し、canonical bytesのauthorityを定義する。
- **責務外:** file open、hash verificationのI/O、実効科学計算、Local OS permission enforcement。
- **参照:** IF `23_42` §6、`23_41` §5。Existing Product CliManifestとは別schema。

#### フィールド

| Field | Type | Origin | Constraint |
| --- | --- | --- | --- |
| `manifest_version` | `Literal["e11-local-manifest/1"]` | Schema | mandatory, no v2 fallback |
| `run_id, operation, request_hash` | `str, LocalOperation, str` | validated Study | fixed identity, digest hex64 |
| `lineage` | typed refs + hashes | Question/Design/Graph/Dataset/Identification | graph/estimand/adapter provenance lossless |
| `execution_status` | typed technical + scientific axes | LocalRunOutcome | actual facts, independent science not faked |
| `runtime` | `RuntimeEvidence` | effective probe | Python/backend/lock/seed/fold/BLAS explicit |
| `artifacts` | `tuple[ArtifactDescriptor,...]` | Publisher stage validation | relative keys, size, hash, media, privacy |
| `review` | evidence refs + legal release state | SCI + policy | absent proof remains null / NOT_EVALUATED |

この表は論理的なField groupingであり、wireの厳格なversion/Schema検証は23_42に従う。

#### Constructor / Factory

- **Factory:** `from_payload(payload: Mapping[str, JsonValue]) -> LocalRunManifest`、`from_run_evidence(evidence: ValidatedRunEvidence) -> LocalRunManifest`。
- **Precondition:** strict schema/version + no unknown critical keys; content hash references are normalized; `Manifest` must **not** include its own bytes hash; marker is outside Artifact list. Factories do not read the filesystem.
- **N/A:** runtime backend import is not part of this DTO. Factoryはstrict Schema違反を型付きErrorとして返す。

#### メソッド

| Signature | Result | Side effect / failure |
| --- | --- | --- |
| `validate_invariants(self) -> tuple[Reason,...]` | typed reasons | pure; reject broken cross-refs, privacy and science axis inconsistency |
| `to_canonical_bytes(self) -> bytes` | canonical versioned JSON bytes | pure deterministic encoding; reject NaN/Infinity/raw credentials |
| `from_payload(payload) -> LocalRunManifest` | immutable DTO | pure strict decode; unsupported version rejected |

#### 処理仕様

1. Normalize schema version and all typed scientific statuses without collapsing negative outcomes.
2. Validate artifact keys unique and safe relative; no absolute input path/secret/row data in Manifest.
3. Validate lineage digest/target and effective runtime evidence with missing values distinguished from fabricated defaults.
4. Produce canonical bytes deterministically, independent of map insertion order or local time display. Result identity is a logical run identity, **not** evidence of successful file publication.

#### I/O・連携・失敗処理

- `LocalArtifactPublisher` creates Manifest bytes; Reader consumes those same canonical bytes. Marker stores SHA256 of Manifest bytes, not a self-reference.
- **I/O:** N/A in DTO; byte serialization is pure. Actual file I/O/permission, partial bundle, crash and retry belong to Publisher/Reader.
- **Failure:** `SCHEMA_INVALID`, `VERSION_UNSUPPORTED`, `HASH_INVALID`, `PRIVACY_POLICY_CONFLICT`; no automatic v2 upgrade.

#### 検証

`DD-E11-MAN01` canonical bytes roundtrip; `MAN02` unknown version/unknown critical; `MAN03` marker outside artifact list; `MAN04` science negative vs technical outcome independent; `MAN05` absolute path/raw secret/row data rejection; `MAN06` legacy v2 readback isolation。関連要件：FR-201/202/203、NFR-029/030/032、AR-040、BD01-F06/F07/F12。

## 4. Required execution — class-to-method contract (G02/P04)

1. **Entry:** G02 06/07・本PxxがFrozen、Owner Coding Authorization発行、G01 latest canonical 999 PASS、依存Pxx checkpoint SHAと実際のbranch source/lock一致を確認。不一致は開始禁止。
2. `LocalCausalUseCase`のIDENTIFY/ESTIMATE routingをMethodRegistry→IdentificationPort→必要なValidatedEstimatorRequest→EstimatorPortへ接続。既存G01のPublisher/Reader/Privacy/GraphVersionを再実装しない。
3. 識別ProofのVersion/Graph/Design/HashとEstimatorRequestのEstimand/Population/Contrastを突合し、不一致やunidentified状態では数値Estimatorを起動しない。
4. 結果Discriminatorは識別のみならeffect null、合法的推定の場合だけEffect Result。Status/Manifest/ReaderをG01の正規CodecとPublisherでround-tripする。旧v2 CLI/ScientificCorePortの公開ABI維持。
5. **Common postcondition:** preflight→typed eligibility→selected backend/科学Kernel→validated typed outcome→G01正規StagingSink。Staging外のfinal run path、Resultと未承認の個票出力へ直接書かない。Technical exit0はScience PASSを意味しない。
6. **Prohibited:** 類似名称によるMethod置換、旧v2のSignature/Graph/Codec改変、mock-onlyによるScience PASS、unsupported CIの捏造。Backend failureと正当な科学的負結果を識別する。

**Science-specific method constraints incorporated here:** Identification/Estimationの分離とoperation別Manifestを維持。

### 設計書で定義済みの科学・型契約（このPxxに展開済みの規範）

以下は30_63の確定記述のうち本Packageに該当する部分を**本文へ複製した実装規則**であり、DDへの外部参照によって補完する規則ではない。担当外Methodの記述がある場合は担当Classを追加実装しない。

41 Method IDは固定Catalog識別子であり、各IDにOperation、Estimand、Backend/Profile、Method Config Schema、Question/Design Evidence Profile、Inference Policy、Output Artifact Profileを登録する。Class割当があることだけでは実行可能性を意味しない。`ValidatedMethodRequest`は登録済みstrict Method Schemaとcross-asset semantic Validatorの双方に成功した場合のみFactoryから生成する。

P1-M06は`e11_p1_m06_fci_method_config_v1.schema.json`、専用Question/Design internal profilesを使用する。他のMethodについてconfig/profile未定義のまま`config={}`やBackend defaultで通すことを禁止し、`METHOD_PROFILE_UNAVAILABLE`等のtyped reasonでfail-closedにする。各Method提供前に対応Gateで正規Schema、条件付き必須項目、negative fixturesを確定し登録する。Gate IDはSchema dispatchのキーにしない。

`ariadne.scientific.causal_methods.*`：
- `check_design(request) -> EligibilityOutcome`：Method固有のRequired Columns、missing、Temporal/Panel units、instrument support、positivity等のReasonを収集。
- `run(request, *, sink: StagingArtifactSink) -> TypedScientificOutcome`：数値計算。返却するのはportable Result DTO、external library instanceは禁止。日時・randomnessは注入されたContextのみから取得。
- `describe_effective_backend() -> BackendEvidence`：実効Library/distribution、Python API、solver/nuisance/fold/CI config/seedを返す。
- `serialize(result) -> ArtifactBundle`：Graph/Result/Diagnosticsを型付きSchemaに純粋変換する。File I/Oはしない。保存はAdapterが渡された`StagingArtifactSink`を通じて行い、Finite/not-finiteを判定しnull+reasonを記録する。

- 入力契約違反＝`CONFIG_INVALID / METHOD_INCOMPATIBLE`、Backend unavailable＝`CAPABILITY_UNAVAILABLE`。これらは他手法へのfallback要因にしない。
- 仮定未成立、positivity不足、弱IV、非識別、CI unavailable、negative-control nullは**科学的Status/Reason**。当該Methodに適格なPointやCIがないことを明示。
- Backendの数値例外、収束エラー、非有限推定を成功へ書き換えない。
- Confirmatory ResultはMethod別の妥当な推論がなければScience PASSとしない。

**未実測のBackend/Independent Reference/Method固有Schema/定量閾値は上記契約が未定義であることとは異なる。** 採用済みTarget/数理規則をAgent裁量で変更せず、未実測はScience/Freezeの該当判定でBLOCKEDとする。

**OD-01 dispatch norm:** `P1-M05`の`IDENTIFY`は条件付きcomplier `LATE_COMPLIER` Proofを`identification.json`へ保持。Effect/point/CI file禁止、B1/DRIV/ATE requestや無効Hash/InstrumentはEstimator呼出前にtyped拒否。G08数値推定をこのPackageで実装しない。P1-M05を含む各Method固有strict Profileが未登録の場合、全Gateを成功にしない。

## 5. Method-by-Method DGP/Negative/Reference Obligations

このPackageは新Method IDの科学Kernelを追加しない。既存のG01〜G09 Method/ResultとTyped Portを再利用する。

**Proof boundary:** 本Pxx§5のDGP/NEG/REF/ACは全件独立科学検証義務である。IDの列挙は実Fixture/独立Reference生成済みやPASSを意味しない。Backend自己出力を真値としない。FWER=.05・K/R/Compute/MC-SE/CI coverageと閾値はFreeze前に決定し、未確定はBLOCKED。別文書を読んで値を推測・補完しない。

## 6. Focused Verification Contract — WHAT, not physical filename

| Layer | Required behavior |
|---|---|
| unit | Value/Estimand/Method schema、negative、Hash/Status/No-False-PASS、pure Algorithm。 |
| contract | `Class.Method`入出力、Port/Backend Registry選択、typed evidence/Lineage、Version+Codec。 |
| integration | 必要な実Backend/CLI/FS/Atomic readback、optional Profile、既存Product v2回帰。 |
| scientific evidence | Method別DGP/NEG/independent reference、定量Simulation/coverage/MC-SE。 |

TestはLifecycle（enhancement/regression/characterization/benchmark/support/legacy）とLayer（unit/contract/integration/frontend/browser_e2e）を独立分類。新規は`tests/enhancement/enh_e11/g02/<layer>/`に原則配置、実Path/command/pytest collectionは40 Operatorがcurrent checkoutからdiscover。受入07をpathの文字列で置き換えない。Mock-onlyでreal Backend/FS/ScienceをPASSにしない。

### 6.1. Package-specific executable evidence

- 対象MethodとDD IDは§5の各行を一つも省略しない。DGP/NEG/REFの名前は検証対象IDであり、**実測/fixtureが作成済みという主張ではない**。
- **必須Focused Contract:** `LocalCausalUseCase`のIDENTIFY/ESTIMATE routingをMethodRegistry→IdentificationPort→必要なValidatedEstimatorRequest→EstimatorPortへ接続。既存G01のPublisher/Reader/Privacy/GraphVersionを再実装しない。 識別ProofのVersion/Graph/Design/HashとEstimatorRequestのEstimand/Population/Contrastを突合し、不一致やunidentified状態では数値Estimatorを起動しない。 結果Discriminatorは識別のみならeffect null、合法的推定の場合だけEffect Result。Status/Manifest/ReaderをG01の正規CodecとPublisherでround-tripする。旧v2 CLI/ScientificCorePortの公開ABI維持。
- Test discovery/pathは40に委譲するが、何を検証するか（出力Status、Method target、reason、既存ABI不変、科学Oracleと適格Backend）は本文と§5に保持する。Unit/Contract/実Backend integrationを役割ごとに実施し、適用不能なものはReasonを明示する。
- EvidenceにClass.Module/Method/入力形、正例・負例のexpected vs actual、使用Backend version/API/seed、source+fixture SHA、effective Method/Estimand/Inference、pytest collect/command、PASS/FAIL/BLOCKEDを記録する。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** 全required Pxx完了後Candidate Assembly。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、当該PxxのOptional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。本Pxxの依存契約・科学的Referenceが未解決なら当該ScopeだけをBLOCKEDとする。他Gateの未決を全Packageの一律停止条件にせず、Agentによる推測補完を禁止する。


## 8. Freeze-critical independence audit (review DRAFT)

- **Self-containment:** Class Fields/Constructor/public Method/処理は§3.1以降、Package固有順序は§4、Methodと独立検証IDは§5〜6で与える。他の06/P00/07やDDをNormative手順の補完材料にしない。
- **Remaining review:** upstream Proof→Estimator eligibility/Manifestのcross-operation schema具体性。 Method-specific Schema/Backend/独立Fixture/Science quantitative thresholdを実際に固定する。未確定部分を実装推測で埋めず、対象MethodをBLOCKEDとして扱う。


## PREP-04.1 Dispatch-specific Negative Matrix (DRAFT / NOT_FROZEN)
- P1-M01: Require registered five strict internal profiles for IDENTIFY; fail on empty/unknown config, mismatched Study/Question/Design target, backend/API incompatible, and inference unavailability; NEG-001, NEG-027. No profile fallback.
- P1-M02: Require registered five strict internal profiles for IDENTIFY; fail on empty/unknown config, mismatched Study/Question/Design target, backend/API incompatible, and inference unavailability; NEG-002, NEG-003. No profile fallback.
- P1-M03: Require registered five strict internal profiles for IDENTIFY; fail on empty/unknown config, mismatched Study/Question/Design target, backend/API incompatible, and inference unavailability; NEG-002, NEG-027. No profile fallback.
- P1-M04: Require registered five strict internal profiles for IDENTIFY; fail on empty/unknown config, mismatched Study/Question/Design target, backend/API incompatible, and inference unavailability; NEG-004. No profile fallback.
- P1-M05: Require registered five strict internal profiles for IDENTIFY; fail on empty/unknown config, mismatched Study/Question/Design target, backend/API incompatible, and inference unavailability; NEG-006, NEG-007. No profile fallback.
- P1-M07: Require registered five strict internal profiles for ESTIMATE; fail on empty/unknown config, mismatched Study/Question/Design target, backend/API incompatible, and inference unavailability; NEG-004, NEG-005. No profile fallback.


## S02：担当Method Profile・共通署名の規範（G02 / Owner承認）

担当Methodは`P1-M01, P1-M02, P1-M03, P1-M04, P1-M05, P1-M07`。共通5 Profile Kind（method_config/question_profile/design_profile/output_profile/inference_profile）を`23_api_interface_design/schema_drafts/method_profiles/factored/e11_<kind>_factored_v1.json`から読み、exact Method IDのoverlayと共通Schemaを単一JSON Schemaに再構成する。Dispatch Registry `e11_method_profile_dispatch_registry_draft1.json`を照合し、Git Blob SHA・Draft202012 Schema・正例/負例が未確認なら`METHOD_PROFILE_UNAVAILABLE`でfail-closed。閉objectの別々の`allOf`合成で`additionalProperties:false`を破綻させない。Operation/Estimand/Backend/CI・DGP/NEG/REF/ACはMethodごとの科学契約に従い、共通化から科学Targetを推測しない。特にP1-M05はB0二値IV/無調整complier `LATE_COMPLIER`の条件付きIDENTIFY専用で数値Effectを生成しない。

`LocalRunContext(root:TrustedLocalRoot,principal:LocalPrincipal)`と`LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)`を共通署名とし、署名PolicyVerifier/Anchor・`cli_row_flag`・Study`privacy.policy_ref`は実装しない。G05以外では個票直接出力禁止、G05でもStudy `row_export_requested=true`と非root同一UID/private ext4/XFS・Method Schema/capsが全件必要。新Local GraphはProduct Version ID=null、content hashと科学由来を使い、Product DB GraphVersionをlookup/生成しない。既存Scientific Kernel・旧Product v2を保護し、回帰は影響閉包に基づいて選択、未知影響なら試験またはBLOCK。Method固有の実Backend/Inference・独立科学Referenceは未確認であり、Science PASSとはしない。
