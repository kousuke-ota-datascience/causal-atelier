# ENH-E11 G08 P04 — rdd_iv_result

**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G08 / **Package:** P04 / **Trial:** NOT_STARTED  
**Depends on Pxx:** P01,P02,P03  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G08_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G08_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** RDD/IV別Result、bounded/unbounded/disconnected AR、独立Reference/Coverage/weak IV検証とReader。

**Scope:** 本PackageのClass/Methodと、それらが必要とする契約/適格性/Result Evidenceに限定。**Gate全体の保護意味:** Sharp/Fuzzy RDDとB0/B1 IV/2SLSを局所Estimand・弱IV AR集合付きで提供する。

**科学/Designの必須制約:** B0 complier LATEとB1 structural slopeを区別。HC1 AR集合をfinite gridだけで判定しない。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** RDD/IV別Result、bounded/unbounded/disconnected AR、独立Reference/Coverage/weak IV検証とReader。

### 2A. Existing Source verified vs E11 RDD/IV API（`2cf28f59a324`）
- **現行ABI:** `src/ariadne/scientific/core_adapter.py`の`ScientificCoreAdapter.run_estimation(self, input_: EstimationInput, output_dir: Path)->list[ScientificResultDescriptor]`は旧Product Path API。 `src/ariadne/causal/inference/estimators/treatment_effect.py`の`TreatmentEffectEstimator`は既存diff/OLS/IPW/AIPW数値Kernelだが、Sharp/Fuzzy RD、Wald、B0/B1 2SLS、Anderson–Rubinの実装済み証拠ではない。旧APIを変更・無検証castせず新Typed EstimatorPortへ共有純粋Kernelを接続する。
- **新規科学境界:** `RddAdapter/WaldRatioAdapter/TwoSlsAdapter`は§3/§4の設計Class。P3-M09/M10のB0 binary Z/A complier LATE、P3-M11のB1 C調整付きstructural IV slopeを混同しない。HC1 Anderson–Rubinは各候補βの`Y-βA ~ [Q,Z]`でZ係数のzero testを反転し、全実数/非有界/非連結/退化を含む集合をlossless保存。有限gridは全実数tailの証明でない。Independent REF、分散/退化処理・推論受入の未決は`BLOCKED_SCIENCE_REFERENCE_UNRESOLVED`、Agent独断で閾値を選択しない。
- **Ownership:** G01 Registry/GraphVersion/Publisher/Reader、G03 Scientific Coreを二重実装しない。既存Method内の共通計算が新Estimandと一致しない場合は使い回さない。

### 2B. Standalone Operation/Result/Manifest契約
| Operation | 必須Artifact | 禁止・Negative |
|---|---|---|
| DISCOVER | `study.json`・`status.json`・Graph成功なら`graph.json` | `result.json`禁止。科学的Graph無しは`diagnostics.json`と理由必須、`schema_dispatch.graph=null`。Backend失敗との混同禁止 |
| IDENTIFY | `study.json`・`status.json`・`identification.json` | Effect `result.json`禁止。非識別もtypedでGraph/Design/Estimand/Proofのhash照合 |
| ESTIMATE | `study.json`・`status.json`・`result.json` | `schema_dispatch.result=e11-local-effect-result/1`。Point無しはnull＋reason、科学PASSと混同禁止 |
| REFUTE/SENSITIVITY/DIAGNOSE | `study.json`・`status.json`・`diagnostics.json` | Effectの再発行禁止、元Effect/Graph/Design hash、seed/適用条件の照合 |

全Operationに`manifest.json`（`e11-local-manifest/1`）と`_COMMITTED.json`（`e11-commit/1`）、ただし両者はArtifact Inventory外。Inventoryは実Fileの相対POSIX key、実bytes SHA256/size/MediaType/Privacyを網羅。 `request_hash=SHA256(JCS(validated typed Study JSON))`。Manifestに自己hashを格納せず、Markerの`manifest_sha256`にManifest実bytes hashを保存。ReaderはMarker→Manifest→実File→Operation/Profile→上流hashをTrustedRootで検証し、一致しない未コミット/破損データを拒否。Outputは既存G01のStaging→同一FS atomic no-clobber publish、個票bytesはG05独立承認以前に生成禁止。各Methodのpoint/uncertainty/science_acceptance/statusを別軸で保持し、計算成功はScience PASSでない。

## 3. Class Placement, Signature, Reuse, Dependency Direction

| Class/Port | Designed module (DD30_61〜63) | Ownership boundary | Exact approved/design signature |
|---|---|---|---|
| `LocalCausalUseCase` | `ariadne.capabilities.causal.local_execution.LocalCausalUseCase` | Port/Value/Facade integration (no duplicate implementation) | preflight(self,spec:ValidatedStudy,context:LocalRunContext)->PreflightReport / run(self,spec:ValidatedStudy,context:LocalRunContext)->LocalRunOutcome |
| `EffectOutcome` | `ariadne.causal.inference.contracts.EffectOutcome` | Port/Value/Facade integration (no duplicate implementation) | validate_consistency() / to_result_payload() |
| `InferenceEvidence` | `ariadne.causal.inference.contracts.InferenceEvidence` | Port/Value/Facade integration (no duplicate implementation) | validate_for(mode,method) |
| `ARConfidenceSet` | `ariadne.causal.inference.confidence_sets.ARConfidenceSet` | Port/Value/Facade integration (no duplicate implementation) | from_components(level,components,evidence) / contains(beta:float) / to_payload()/from_payload(payload) |

**Method Adapter signature policy:** 新Adapterは原則`preflight(self,request:ValidatedMethodRequest)->EligibilityOutcome`／`execute(self,request:ValidatedMethodRequest,*,sink:StagingArtifactSink)->TypedScientificOutcome`。上表で指定された既存`run(self,input_,output_dir)`はその署名を保持。PortはApplication→Scientific kernelへ向かい、CLI Layerに別の科学数値実装を作らない。Constructor/Field/公開MethodとARConfidenceSetの境界は本Pxx§3.1以降の埋込Class契約が規範。外部DDはProvenanceのみ、未知のConcrete型を推測しない。

**Responsibility:** 本PackageはScientific Adapter数値本体を新規所有しない。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。

### 3. Standalone Class-level contracts (normative)

Class Fields/Constructor/Method/Pre/Post/Failureは以下で本Package内に定義する。外部DDはprovenanceに限り、Agentが参照しなければ実装できない仕様を残さない。Designed Module≠Source実装済み。ABIはSource照合する。

### 3.1. `LocalCausalUseCase` — full fields/constructor/methods

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
| `policy_verifier` | `LocalPolicyVerifierPort` | composition root | immutable; preauthorization from independent authority |
| `privacy` | `LocalPrivacyPolicyPort` | composition root | immutable; explicit row release decision |
| `publisher` | `LocalPublicationPort` | composition root | immutable; all writes staged |
| `runtime` | `RuntimeEnvironmentPort` | composition root | immutable; effective provenance not fabricated |
| `clock` | `ClockPort` | composition root | immutable; injected timestamp authority |

No shared mutable per-run state is retained in the use-case object; per-run staged artifacts/status are returned via typed RunOutcome or scoped Context. UseCaseのper-run状態非共有を不変条件とする。

**Application Context：** `ariadne.capabilities.causal.local_execution.LocalRunContext`は`root: TrustedLocalRoot`、`principal: LocalPrincipal`、`cli_row_flag: bool`、`policy_anchor: TrustedPolicyAnchor|None`を持つimmutable value。OS Root/Principalの型Authorityは`ariadne.shared.local_fs`、生成責務はCLI composition rootのTrustedRoot Factory。現行CLIの入力ContentRefと出力Bundleは同じRoot下の異なる相対keyで扱う。Policy AnchorはCLI composition rootがStudy外のsecure runtime trust configurationから取得する。G01集計専用のとき`policy_anchor=null`を許容するが、行出力要求では欠落を拒否する。Study YAMLからContextの信頼属性を構築してはならない。

**Application Port配置：** `ariadne.capabilities.causal.ports.content_ref.ContentReferencePort`、`ariadne.capabilities.causal.ports.local_io.LocalPublicationPort/LocalManifestReaderPort`、`ariadne.capabilities.causal.ports.local_policy.LocalPolicyVerifierPort`、`ariadne.capabilities.causal.ports.local_privacy.LocalPrivacyPolicyPort`。`LocalPrivacyPolicy` ConcreteはLocalPrivacyPolicyPortの実装であり、ApplicationはCLI Concreteをimportしない。Policy verifierはStudyと独立のTrust Anchorで事前承認証拠を検証する。

#### Constructor / Factory

配置：`ariadne.capabilities.causal.local_execution.LocalCausalUseCase`。`LocalConfigDecoder`は**CLI composition root**に属し、Strict parse/Version検証済み`ariadne.causal.design.study.ValidatedStudy`のみApplicationへ渡す（Application内で別のdecodeを暗黙に行わない）。
注入Port：`refs: ContentReferencePort`、`capabilities: MethodCapabilityPort`、`discovery: DiscoveryPort`、`identifier: IdentificationPort`、`estimators: EstimatorPort`、`diagnostics: DiagnosticPort`、`publisher: LocalPublicationPort`、`reader: LocalManifestReaderPort`、`policy_verifier: LocalPolicyVerifierPort`、`privacy: LocalPrivacyPolicyPort`、`runtime: RuntimeEnvironmentPort`、`clock: ClockPort`。Constructor時にoptional Backendをimportしない。

- **Constructor signature:** `__init__(self, *, refs: ContentReferencePort, capabilities: MethodCapabilityPort, discovery: DiscoveryPort, identifier: IdentificationPort, estimators: EstimatorPort, diagnostics: DiagnosticPort, publisher: LocalPublicationPort, reader: LocalManifestReaderPort, policy_verifier: LocalPolicyVerifierPort, privacy: LocalPrivacyPolicyPort, runtime: RuntimeEnvironmentPort, clock: ClockPort)`。公開ApplicationはPort抽象にのみ依存する。
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
7. 本書§2BのOperation別必須/禁止Artifactとschema_dispatchを検証し、typed Graph/Identification/Effect/Diagnostics、Status/Manifestを生成。`context.policy_anchor`を使って独立Policy verifierが取得した承認証拠、Study、CLI row flag、`context.principal`・Output shapeを`LocalPrivacyPolicyPort.authorize`で照合し、staging seal→一括publish→独立Reader readbackを行う。
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

### 3.2. `EffectOutcome` — full fields/constructor/methods

#### 識別情報・責務

**Class / module:** `ariadne.causal.inference.contracts.EffectOutcome`。点推定・Inference・ScienceAcceptance・lineageを別軸で保持する。Productの既存`ScientificResultDescriptor`へ無検証castしない。

#### フィールド

| Field | Type・制約 |
|---|---|
| `result_id, estimand` | immutable result/target |
| `point_availability, point_value` | finite value または null + reason |
| `inference` | `InferenceEvidence` |
| `science_acceptance` | 推論可用性とは独立した審査状態 |
| `diagnostics` | `tuple[DiagnosticRef,...]`。Method別typed診断参照 |
| `method_evidence, upstream_hashes` | typed Backend evidenceとlineage |

#### Constructor / Factory

Constructor/Factoryはtyped statusと上流lineageを持つEvidenceから生成。不正なEffect/Estimand一致やfalse PASSを拒否。

#### メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `validate_consistency()` | typed validation result | pure point/CI/science consistency | nonfinite point、null reason欠落 |
| `to_result_payload()` | typed Result payload | pure typed result projection。JCS byte encodingは共通Codec | incompatible schema/estimand |

#### 処理仕様

Pointの存在≠Science PASS。Technical、Identification、Point、Inference、ScienceAcceptanceの状態を混同せず、Method固有estimand/CIを検査。

#### I/O・連携・失敗処理

ValueのI/Oなし。request hashは`SHA256(JCS(validated typed Study JSON))`、Graph内部hash、ContentRef実bytes hash、Manifest bytes hashを分離。Codec`e11-json-jcs-rfc8785/1`、Productの`hash_mapping(default=str)` fallback禁止。

#### 検証

`DD-E11-EFF01` point-only、`EFF02` Science独立、`EFF03` backend mismatch、`EFF04` canonical finite、`EFF05` old Product regression。FR-202、NFR-030/032/036、AR-034/040。

### 3.3. `InferenceEvidence` — full fields/constructor/methods

#### 識別情報・責務

**Class / module:** `ariadne.causal.inference.contracts.InferenceEvidence`。Inferenceの可用性と実際のFinite CI／AR集合を型付きで保持する。

#### フィールド

| Field | Type | 制約 |
|---|---|---|
| `availability` | `InferenceAvailability` | AVAILABLE/UNAVAILABLE/FAILED/NOT_REQUESTED等 |
| `kind` | Method-specific enum | 実効推論方式 |
| `interval, confidence_set` | `FiniteInterval|None, ARConfidenceSet|None` | AVAILABLEなら正当な片方ちょうど1つ |
| `reason` | `ScientificReason|None` | nonAVAILABLEでは必須 |
| `method_config` | typed config | Backend/Method/Estimandに適合 |

#### Constructor / Factory

Constructor/Factoryはavailabilityとevidenceの排他性、およびreason整合を検査。実行済みCIをデフォルト値で捏造しない。

#### メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `validate_for(mode,method)` | Validated inference / typed reason | pure Method/analysis-mode適格性検査 | unsupported confirmatory inference |

#### 処理仕様

EXPLORATORY point-onlyとCONFIRMATORY inference要件を分離する。FiniteIntervalとARConfidenceSetを丸め合わせず、SCM point-onlyを確証CIと報告しない。

#### I/O・連携・失敗処理

Value操作I/Oなし。Backend provenance・coverageの計算は30_63へ委譲。

#### 検証

`DD-E11-AR04/AR05`、`DD-E11-EFF01/02`、Method-specific CI availability、independent coverage。

### 3.4. `ARConfidenceSet` — full fields/constructor/methods

#### 識別情報・責務

**Class / module:** `ariadne.causal.inference.confidence_sets.ARConfidenceSet`。Anderson–Rubin反転の損失ない数学集合を表すValue。

#### フィールド

| Field | Type | 制約 |
|---|---|---|
| `confidence_level` | `float` | 0 < level < 1 |
| `components` | `tuple[ExtendedRealInterval,...]` | EMPTYは0件。finite/±∞をtagged endpointsで表現 |
| `topology` | `SetTopology` | EMPTY/ALL_REAL/DISCONNECTED/UNBOUNDED/BOUNDED |
| `inversion_evidence` | `ContentRef` | 成功した数学的反転の証拠 |

#### Constructor / Factory

`from_components(level,components,evidence)->ARConfidenceSet`：finite endpoint、順序、open/closed、重複/接触区間の数学的正規化。

#### メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `from_components(level,components,evidence)` | `ARConfidenceSet` | pure set normalization | invalid endpoint/topology |
| `contains(beta:float)` | `bool` | endpoint条件で判定 | NaN/invalid β |
| `to_payload() / from_payload(payload)` | JSON / Value | Lossless roundtrip | malformed topology / JSON非有限数値 |

#### 処理仕様

Topology分類はEMPTY→ALL_REAL→DISCONNECTED→UNBOUNDED→BOUNDED。ALL_REALは(-∞,+∞)一成分。∞端点はopen、双方openで接触する2区間は1点gapを残すため結合しない。数学的EMPTYは`AVAILABLE + inversion_evidence`と両立、計算失敗`FAILED+reason`とは別。B0/B1 just-identified HC1 ARで`g_A≠0`かつ`Var_HC1(βhat)>0`等の非退化条件が成立する場合`T_AR(βhat)=0`により非空が必要となり、**Method別validator**でEMPTYを拒否。

#### I/O・連携・失敗処理

Valueはpure。JSONのNaN/Infinity数値は禁止、tagged endpointで表現。実AR反転・HC1・coverageはMethod Adapterと独立科学検証に委譲。

#### 検証

`DD-E11-AR01` 5分類、`AR02` generic EMPTYとjust-identified条件分離、`AR03` lossless roundtrip、`AR04` null reason、`AR05` confirmatory fail-closed。FR-202、AR-040、NFR-036。

## 4. G08/P04 required scientific and code execution

1. **Preconditions:** G08 Frozen06/07/Pxx、G01/G02 upstream canonical 999、Owner Coding Authorization、fixed candidate Source/lock、Pxx checkpointsを照合。Method/Design/IV assumptions/Estimand/Inference/Backend selectionをpreflightで検証。
2. RDのlocal effect、Fuzzy RDのlocal complier effect、B0 LATE、B1 IV structural slopeは別Estimand-family/targetとしてTyped EffectOutcomeを作る。
3. ARConfidenceSetは有限単一区間に無理に変換しない。Point, CI, weak-IV diagnostics, first-stage, Method assumptions, Technical vs Scientific statusを別Fieldで持たせる。
4. G01のManifest/Status/Publisher/Readerを再利用してconfidence setのunbounded/disconnected/empty roundtripを実測し、旧v2未対応のRangeに黙ってキャストしない。
5. **Dataflow:** Typed ValidatedMethodRequest→Method Adapter eligibility→selected numeric kernel/effective Backend→EffectOutcome/ARConfidenceSet→G01 StagingSink/Atomic Publisher/Reader。外部Backend model objectやRaw row/SecretsをResultへ含めない。
6. **Typed failure:** Zero denominator, rank/HC1 variance degeneracy, unsupported CI, invalid design, optional backend unavailable, numerical FAILED, legitimate scientific weak IVを明確に区別。Technical exit0はScience PASSでない。

### 設計書の採用済み意味論（独立した本Package実装規範）

以下は30_62/30_63に明文化された数理・Port・互換性の契約をこのPxxへ取り込んだもの。Scopeは本Packageの§3/4に限り、他PackageのClassを再実装しない。

- Sharp RD：cutoff周辺のlocal regression、bandwidth、polynomial order、kernel、density manipulation、covariate continuityの診断を出力。
- Fuzzy RD：cutoff近傍のTreatment first-stage jumpとOutcome jumpの比による局所IV効果。weak first stageやinstrument validityに注意。単なるSharp RDにlabelを変えるだけで代用しない。
- `rdrobust` 等の外部BackendはPython APIの実効版とrobust bias correction inferenceの利用可否を確認。GPLの顧客配布Legal approvalとは別。

- B0（P3-M09/M10）：単一二値Z/A、無調整、単一内生Aのcomplier LATE。Wald ratioは縮約形Outcome差/First-stage Treatment差。分母0/弱い場合にfinite CIを強制しない。
- B1（P3-M11）：単一二値Z/A、事前指定C、additive linear IV構造の2SLS slope。一般ATE/ATTやB0と同一complier LATEと呼ばない。
- B0/B1の2SLSはfirst-stage/2nd-stage、heteroskedasticity-robust covariance、Instrument support/first-stage diagnosticsを保存。通常Wald区間はweak-IV robustでないことを明示。
- Anderson–Rubin：H0(β)の下で`Y - β A`のZとの関係を（B1では指定Cを条件付けて）検定、反転集合を作る。初期契約は独立観測・単一excluded Z・単一endogenous A・異分散頑健漸近推論の範囲。任意のcluster/HAC版へ自動拡張しない。β探索は有界gridだけではALL_REAL/非有界/非連結を判定できないためtail/bracketing/数値精度を検証。数学的にEMPTYなAR集合は汎用Codecで表現可能。ただし、非退化なB0/B1 just-identified HC1 AR反転では gA≠0、Var_HC1(βhat)>0 の条件からT_AR(βhat)=0で非空性が従う。そこでEMPTYが観測された場合はMethod別SCIENCE_INCONSISTENTとして検査する。first-stage=0、非正分散、rank欠損は別途型付き分岐にし、数値的な失敗と数学的EMPTYを混同しない。
- AR testがIVのexclusion/independence/monotonicityを証明すると解釈しない。CI coverageは独立Simulationで計測する。

**AR具体化（共通Source設計拘束）：** `Q=[1]`（B0）または`Q=[1,C]`（B1）をFull Rankで保持し、各βについて`Y−βA ~ Q+Z`のZ係数=0を**HC1・χ²(1)漸近検定**する方式を対象実装方式とする。残差化・quadratic inversionは全実数で行い、有限gridから非有界・空集合を断定しない。公式の数値/科学受入では独立reference・有効な分散・条件付きIV仮定を評価する。統計量、二次式、退化条件、Negative Matrixは本節のAR定義に従い、Method固有の独立Referenceと照合する。これはB0/B1の科学的な統計量・推論前提を規定するものであり、独立ReferenceとCoverage実測とは別である。

**実際のBackend適格性・Config Schemaの未生成・独立OracleやCoverage証跡の不足は、上記Target/数理契約の未決とは区別する。** 実行後のScience判定を未検証のままPASSにしない。

## 5. Method-by-Method DGP/Negative/Reference Obligations

このPackageは新Method IDの科学Kernelを追加しない。既存のG01〜G09 Method/ResultとTyped Portを再利用する。

**Proof boundary:** Method別§5のDGP/NEG/REF/ACは独立検証義務。実数全体のHC1 AR inversion・弱IV退化・LATE/structural slopeの区別は§4で規定。独立Oracleの不在、FWER=.05/K/R/Compute/MC-SE/coverageの未決はBLOCKEDであり、Backend自身の出力や有限GridからScience PASSを作らない。

## 6. Focused Verification Contract — WHAT, not physical filename

| Layer | Required behavior |
|---|---|
| unit | Value/Estimand/Method schema、negative、Hash/Status/No-False-PASS、pure Algorithm。 |
| contract | `Class.Method`入出力、Port/Backend Registry選択、typed evidence/Lineage、Version+Codec。 |
| integration | 必要な実Backend/CLI/FS/Atomic readback、optional Profile、既存Product v2回帰。 |
| scientific evidence | Method別DGP/NEG/independent reference、定量Simulation/coverage/MC-SE。 |

TestはLifecycle（enhancement/regression/characterization/benchmark/support/legacy）とLayer（unit/contract/integration/frontend/browser_e2e）を独立分類。新規は`tests/enhancement/enh_e11/g08/<layer>/`に原則配置、実Path/command/pytest collectionは40 Operatorがcurrent checkoutからdiscover。受入07をpathの文字列で置き換えない。Mock-onlyでreal Backend/FS/ScienceをPASSにしない。

### 6.1. Deterministic/independent scientific proof matrix

- §5の各Method DGP/NEG/REF/DD/ACを保持。Positive DGPとindependent ReferenceをBackend予測から作らない。
- **Mandatory focused cases:** RDのlocal effect、Fuzzy RDのlocal complier effect、B0 LATE、B1 IV structural slopeは別Estimand-family/targetとしてTyped EffectOutcomeを作る。 ARConfidenceSetは有限単一区間に無理に変換しない。Point, CI, weak-IV diagnostics, first-stage, Method assumptions, Technical vs Scientific statusを別Fieldで持たせる。 G01のManifest/Status/Publisher/Readerを再利用してconfidence setのunbounded/disconnected/empty roundtripを実測し、旧v2未対応のRangeに黙ってキャストしない。
- Unit: domain/Estimand/AR set serialization/edge cases; Contract: Class.Method、typed outputs、result discriminator/lineage; Integration: 実Backend、IV instrument/data support、real Publisher/readback、旧Product v2回帰。Weak IV / negative assumptions/HC1 confidence inversionは独立算出Referenceと照合。
- Environment/Backend/API、Source+fixture+lock SHA、DGP/negative、実行Command/Collection、Expected/Observed、Scientific vs Technical outcomeをEvidence化。未確定Oracle/quant K/R/coverageならBLOCKED、Science PASSは出さない。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** 全required Pxx完了後Candidate Assembly。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、当該PxxのOptional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。本Pxxの依存契約・科学的Referenceが未解決なら当該ScopeだけをBLOCKEDとする。他Gateの未決を全Packageの一律停止条件にせず、Agentによる推測補完を禁止する。


## 8. Freeze-critical standalone gaps

本PackageはClass Field/Constructor/Methodを§3、数理処理順序/分岐を§4、科学的DGP/NEG/REFとAcceptanceを§5〜6で内部定義する。**残課題:** RD/IV/ARのEstimand区別およびAR ConfidenceSetのlossless表現は設計済み。未完了なのは対応するstrict Method Profile、Schema/Manifestの負例Fixtureおよび実効readback/独立Reference検証。 P3-M10/M11で有限gridだけのAR反転を実装することは禁止。OwnerがFreeze時に独立数理/Backend/ConfigとScience受入条件を明示的に判定する。
