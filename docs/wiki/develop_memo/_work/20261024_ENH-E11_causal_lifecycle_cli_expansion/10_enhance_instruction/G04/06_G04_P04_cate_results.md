# ENH-E11 G04 P04 — cate_results

**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G04 / **Package:** P04 / **Trial:** NOT_STARTED  
**Depends on Pxx:** P01,P02,P03  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G04_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G04_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** 8 Method Result/CI可用性/Local CLIを統合。G05承認前の個票出力禁止。

**Scope:** 本PackageのClass/Methodと、それらが必要とする契約/適格性/Result Evidenceに限定。**Gate全体の保護意味:** 7種Non-IV CATEとDRIV IV異質効果を個別Estimand/Inferenceで提供する。

**科学/Designの必須制約:** Non-IV CATE、IV heterogeneous slope、B0 LATE、B1 linear slopeを同一視しない。G03依存はまとめReviewで検討。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** 8 Method Result/CI可用性/Local CLIを統合。G05承認前の個票出力禁止。

### 2A. 現行Source ABIと新規Methodの区別（`2cf28f59a324`）
- **実在:** `src/ariadne/scientific/core_adapter.py`の`ScientificCoreAdapter.run_estimation(self, input_: EstimationInput, output_dir: Path) -> list[ScientificResultDescriptor]`は旧Product Path API。 `src/ariadne/causal/inference/estimators/treatment_effect.py`には`TreatmentEffectEstimator.diff_in_means/ols/ipw/aipw`があるが、これらをEconML CATE/DRIVの実装済み証拠として扱わない。
- **Design-only:** `EconmlCateAdapter`/`MetaLearnerAdapter`/`EconmlDrivAdapter`およびE11 `EstimatorPort.estimate(ValidatedEstimatorRequest, *, sink:StagingArtifactSink)->EffectOutcome`は別の型付き契約。旧`ScientificCorePort.run_estimation`を変更しない。EconMLの実効Distribution・Estimator API・fit/predict/inference availabilityを選択Backend/Versionごとに実測し、欠落・非対応はMethod単位のtyped unavailableにする。旧数値Kernelを再利用できるのはTargetと契約が一致する場合だけ。
- **Ownership:** 新Scientific Kernelは他Family専用コピーを作らず、純粋計算に関する共有実装へ接続する。G01共通Registry/Publisher/Readerの多重実装は禁止。Concrete Adapter・Schema・Science Oracle未確定なら`BLOCKED_CONTRACT_AMBIGUITY`、Agentが推論APIを創作しない。

### 2B. Operation別Artifactと検証規則（外部DDを読まずに判定）
| Operation | 必須Artifact | 禁止・negative/Schema |
|---|---|---|
| DISCOVER | `study.json`, `status.json`, graph成功時は`graph.json` | `result.json`禁止。Graph無しの正当な科学負例は`diagnostics.json`＋reason、`schema_dispatch.graph=null`。Backend技術失敗は成功としない |
| IDENTIFY | `study.json`, `status.json`, `identification.json` | `result.json`禁止。識別否定もtyped結果にしてGraph/Design/Estimand/Proofのhash照合 |
| ESTIMATE | `study.json`, `status.json`, `result.json` | `schema_dispatch.result=e11-local-effect-result/1`。Point無しはnull＋reason、架空の推定値禁止 |
| REFUTE/SENSITIVITY/DIAGNOSE | `study.json`, `status.json`, `diagnostics.json` | Effectの再発行禁止。元Effect/Graph/Design hash、seedと適用条件を検証 |

全Operationに`manifest.json`（`e11-local-manifest/1`）と`_COMMITTED.json`（`e11-commit/1`）が必要で、いずれもArtifact inventory外。Inventoryは実在Artifactごとに相対POSIX key・SHA256・size・MediaType・Privacyを保持。`request_hash=SHA256(JCS(validated typed Study JSON))`、Markerの`manifest_sha256`はManifest実bytesのhashであり、Manifest自身には自己hashを持たせない。ReaderはMarker→Manifest→各Artifact→Operation Profile→上流HashをTrustedRoot下で独立検証。stagingから同一FS atomic no-clobber publish、未承認row Parquet禁止。旧Productのpath-based writerを型付きStagingSinkの代用として直接使用しない。

## 3. Class Placement, Signature, Reuse, Dependency Direction

| Class/Port | Designed module (DD30_61〜63) | Ownership boundary | Exact approved/design signature |
|---|---|---|---|
| `LocalCausalUseCase` | `ariadne.capabilities.causal.local_execution.LocalCausalUseCase` | Port/Value/Facade integration (no duplicate implementation) | preflight(self,spec:ValidatedStudy,context:LocalRunContext)->PreflightReport / run(self,spec:ValidatedStudy,context:LocalRunContext)->LocalRunOutcome |
| `EffectOutcome` | `ariadne.causal.inference.contracts.EffectOutcome` | Port/Value/Facade integration (no duplicate implementation) | validate_consistency() / to_result_payload() |
| `InferenceEvidence` | `ariadne.causal.inference.contracts.InferenceEvidence` | Port/Value/Facade integration (no duplicate implementation) | validate_for(mode,method) |
| `EstimatorPort` | `ariadne.scientific.ports.causal.EstimatorPort` | Port/Value/Facade integration (no duplicate implementation) | estimate(self, request:ValidatedEstimatorRequest, *, sink:StagingArtifactSink) -> EffectOutcome |

**Class/Method authority:** 本Pxx §3.1以降のField/Constructor/公開Method/前後条件は本書が一次規範である。新規EconML/MetaLearner/DRIV Adapterは本Packageが担当する場合のみ実装し、実効Backend API/Inference availabilityをprobeする。既存v2の公開ABIを維持し、結果だけのPackageは独立数値Kernelを作らない。

**Responsibility:** 本PackageはScientific Adapter数値本体を新規所有しない。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。

### 3. Embedded class-level implementation contracts

以下は本Pxxのnormative仕様。外部DDはprovenanceのみで、Agentに不足手順の補完を委譲しない。Designed Moduleの現物存在は未検証なので開始時にABI/Reuseを検査し、齟齬はBLOCKED。

### 3.1. `LocalCausalUseCase` — Constructor, fields, methods, invariants

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

**Application Context：** `LocalRunContext(root:TrustedLocalRoot,principal:LocalPrincipal)`のみを保持。CLI composition rootが実EUID/private Rootを検証。G04が個票を直接公開する権限はない。G05のみStudy単独opt-inとMethod/OS全件適格性で行出力。

**Application Port配置:** `ContentReferencePort`、`LocalPublicationPort`/`LocalManifestReaderPort`、`LocalPrivacyPolicyPort`。第三者Verifier/Trust Anchor/署名鍵はlocal CLIに要求しない。

#### Constructor / Factory

配置：`ariadne.capabilities.causal.local_execution.LocalCausalUseCase`。`LocalConfigDecoder`は**CLI composition root**に属し、Strict parse/Version検証済み`ariadne.causal.design.study.ValidatedStudy`のみApplicationへ渡す（Application内で別のdecodeを暗黙に行わない）。
注入Port：`refs:ContentReferencePort`、`capabilities:MethodCapabilityPort`、`discovery:DiscoveryPort`、`identifier:IdentificationPort`、`estimators:EstimatorPort`、`diagnostics:DiagnosticPort`、`publisher:LocalPublicationPort`、`reader:LocalManifestReaderPort`、`privacy:LocalPrivacyPolicyPort`、`runtime:RuntimeEnvironmentPort`、`clock:ClockPort`。

- **Constructor signature:** `__init__(self, *, refs:ContentReferencePort,capabilities:MethodCapabilityPort,discovery:DiscoveryPort,identifier:IdentificationPort,estimators:EstimatorPort,diagnostics:DiagnosticPort,publisher:LocalPublicationPort,reader:LocalManifestReaderPort,privacy:LocalPrivacyPolicyPort,runtime:RuntimeEnvironmentPort,clock:ClockPort)`。
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
7. 本書§2BのOperation別Graph/Identification/Effect/Diagnostics/Status・Lineageを検査する。G04では行出力を拒否し、G05のみStudy単独opt-inとEUID/private local FS・Method別RowSchemaによる許可後にG01 Staging→Publisher→Readerを利用する。
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

### 3.2. `EffectOutcome` — Constructor, fields, methods, invariants

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

### 3.3. `InferenceEvidence` — Constructor, fields, methods, invariants

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

### 3.4. `EstimatorPort` — Constructor, fields, methods, invariants

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

Protocol自体はI/Oを持たない。ConcreteはこのPxxの§3/§4で所有が指定されたAdapter/Façadeに限定し、MethodCapabilityPortでstrictに選択する。検証済Request→typed outcome＋staging sinkを守り、外部DDを未記載の実装規範として参照しない。Owner/実効ABIが未確定ならBLOCKEDで停止する。

#### 検証

DD-E11-EFF01〜05。

## 4. Required Method implementation / Class delegation (G04/P04)

1. **Preconditions:** 06/07/Pxx Freeze、G02/G03の要求されるlatest canonical 999、Owner Coding Authorization、fixed Source/lock、Pxx依存checkpointを検証。Method/Estimand/Inference/Backend/Graph/Design/Questionが不一致ならtyped reject。
2. `CATE(x)` Point ValueとPopulation Summary、Support/Overlap/Calibration/Uncertaintyを型付きで分け、Estimand/Target/InferenceStatus/Versionを保持。
3. G05の独立Row Authorizationが成立するまでは個票値をStdout、Result JSON、Manifest、Parquetへ出さない。Aggregationのみのsafe Result/ProfileをG01のPublisherへ渡す。
4. MethodごとにInference RegistryはPOINT_ONLY/SUPPORTED_CI/UNSUPPORTED/UNAVAILABLE/FAILEDを区別し、pointwise CIとsimultaneous bandを別Policyにする。
5. 旧Product v2のEffect/Graph/Status表現へ未対応のCATE Distribution/Uncertaintyを損失変換せず、E11 Result discriminatorとreadback integrityを守る。
6. **Sequence:** ValidatedStudy→LocalCausalUseCase→typed EstimatorPort/Adapter preflight→approved Backend computation→pure typed CATE/EffectOutcome→G01 StagingSink/atomic Publisher/Reader。Application/DomainからCLI DB/FSのConcreteへ逆依存しない。
7. **Failure and privacy:** unsupported inference、effect support不足、missing optional Backendは別Reason。Numerical failureを科学的Negativeに偽装しない。G05以前個票書込無し、Model object/Secret出力無し、旧v2公開ABI不変。

### 設計書で定義済みの実装意味論（本Packageの規範）

以下は既存30_62/30_63の設計規則のうち本Packageへ適用する本文内契約である。外部DDを読ませて仕様を補完することは禁止する。自Packageが所有しないClassは再実装しない。

LinearDML/CausalForestDML/DRLearner/ForestDRLearner/S/T/X-Learnerを単にCATEという名称で同等に扱わない。X=effect modifiers、W=confounders、nuisance models、treatment type、target population、crossfitting/final model、backend/versionをper Method Configとする。

- Result Point CATE(x)、Population summary、support/overlap診断を分離し、個票値は明示的に認可されたParquetのみ。Stdoutや小さなJSONへの個票全件混入を禁止。
- Inference RegistryはMethod/Backend/version/final estimator config別に `POINT_ONLY / SUPPORTED_CI / UNSUPPORTED / UNAVAILABLE / FAILED` を判定。Native bootstrapを統計的妥当性確認なしに汎用適用しない。
- Exploratory point-onlyは許すが、Confirmatoryは事前に宣言したtargetに適合するCIと独立Science Evidenceが必要。Pointwise CIとsimultaneous bandを区別する。

Instrument Z、Treatment A、Effect modifier X、Control W、識別仮定とheterogeneous structural target `theta_IV(x)`を持つ。Non-IV `CATE(x)`、B0 complier LATE、B1 linear IV slopeと区別。weak IV・invalid IV・poor overlapをtyped negativeにし、一般化の範囲を限定する。

**推定Target/Point・Inference可用性の区別は決定済み。未生成の独立Referenceや実API probeをScience PASSには使わない。**

## 5. Method-by-Method DGP/Negative/Reference Obligations

このPackageは新Method IDの科学Kernelを追加しない。既存のG01〜G09 Method/ResultとTyped Portを再利用する。

**Science proof boundary:** §5のDGP/NEG/REF/ACは検証義務であり、Test/Generator/独立Referenceの作成済みやPASSではない。Backend自己出力を真値にしない。FWER=.05・K/R/Compute/MC-SE/CI coverage・Method別Threshold未確定はBLOCKED。別文書を読ませて値を推測・補完しない。

## 6. Focused Verification Contract — WHAT, not physical filename

| Layer | Required behavior |
|---|---|
| unit | Value/Estimand/Method schema、negative、Hash/Status/No-False-PASS、pure Algorithm。 |
| contract | `Class.Method`入出力、Port/Backend Registry選択、typed evidence/Lineage、Version+Codec。 |
| integration | 必要な実Backend/CLI/FS/Atomic readback、optional Profile、既存Product v2回帰。 |
| scientific evidence | Method別DGP/NEG/independent reference、定量Simulation/coverage/MC-SE。 |

TestはLifecycle（enhancement/regression/characterization/benchmark/support/legacy）とLayer（unit/contract/integration/frontend/browser_e2e）を独立分類。新規は`tests/enhancement/enh_e11/g04/<layer>/`に原則配置、実Path/command/pytest collectionは40 Operatorがcurrent checkoutからdiscover。受入07をpathの文字列で置き換えない。Mock-onlyでreal Backend/FS/ScienceをPASSにしない。

### 6.1. Executable proof and invariant matrix

- Targeted Method DD-IDとDGP/NEG/REFは§5に全件明記。§4のEstimator別のX/W/nuisance/fold/effective inference条件を正例・負例として検証する。
- **Verification-specific contract:** `CATE(x)` Point ValueとPopulation Summary、Support/Overlap/Calibration/Uncertaintyを型付きで分け、Estimand/Target/InferenceStatus/Versionを保持。 G05の独立Row Authorizationが成立するまでは個票値をStdout、Result JSON、Manifest、Parquetへ出さない。Aggregationのみのsafe Result/ProfileをG01のPublisherへ渡す。 MethodごとにInference RegistryはPOINT_ONLY/SUPPORTED_CI/UNSUPPORTED/UNAVAILABLE/FAILEDを区別し、pointwise CIとsimultaneous bandを別Policyにする。 旧Product v2のEffect/Graph/Status表現へ未対応のCATE Distribution/Uncertaintyを損失変換せず、E11 Result discriminatorとreadback integrityを守る。
- Unitはpure Method/schema/result、不適格値、ContractはClass/Port/Inference RegistryとLineage、Integrationは実Backend/CLI/Pub-Readback/legacy regressionを実行。独立数値ReferenceはBackend自身から生成しない。
- Evidenceはsource/lock/fixture SHA、expected/actual, effective Backend/API, seed/fold, support/overlap, CI policy, testcase collection/command。科学的Coverage/Pilotは未生成ならBLOCKEDでありPASSを推測しない。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** 全required Pxx完了後Candidate Assembly。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、当該PxxのOptional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。本Pxxの依存契約・科学的Referenceが未解決なら当該ScopeだけをBLOCKEDとする。他Gateの未決を全Packageの一律停止条件にせず、Agentによる推測補完を禁止する。


## 8. Freeze-critical independent contract audit

Constructor/Instance Fields/Public Methodの責務は§3、Method固有処理は§4、DGP/NEG/REF/Focused acceptanceは§5〜6に含み、外部Gate06/07/DDに実装指示を委譲しない。残未決: CATE aggregate contract/row policy、G05と共有するresult shape/ColumnSelection、per method inference policyをFreeze前決定。 Backend実効API/Science Pilot/Reference/Method Config未確定のまま実装しない。Ownerの一括レビューで調停する。

## 9. OD-05 Owner-adopted Method Profile construction obligation

**Accepted authoring allocation (2026-11-19 JST):** G04/P04 is responsible for cross-cutting validation of the existing Method registry; it must not implement additional Method schemas or numerical adapters. Scientific constraints: DML/DR/MetaLearner X/W roles/seed/folds/CI eligibility、DRIV theta_IV(x). Retain the existing §§3–6 Class/Method/algorithm/DGP/NEG/REF/AC semantics. A profile must declare mandatory and conditional fields, type domains, effective Backend/API/Version, analysis_mode/inference eligibility, output status/artifact shape, and no implicit Backend defaults.

**Negative obligations:** unsupported method/profile/estimand, unknown fields, missing conditional fields, invalid Graph/Design/Question/DataRef identity, unavailable optional Backend, unsupported CI or invalid scientific assumptions are typed rejections; missing specific profile ⇒ `METHOD_PROFILE_UNAVAILABLE`. No silent fallback or `config={}` as a claim of support.

**Readiness:** This Owner decision allocates work; it does not assert that schemas, independent DGP/REF, Backend execution, K/R/MC-SE/coverage, Gate07/999, contract Freeze or Coding Authorization are complete. No new mathematical Target is adopted here.


## PREP-04.1 integration preflight (DRAFT)
- P2-M01 owner P01: all five strict profiles and DGP-003; NEG-011, NEG-012, NEG-013; REF-E05; no SCIENCE PASS from schema presence.
- P2-M02 owner P01: all five strict profiles and DGP-004; NEG-010, NEG-012, NEG-013; REF-E05; no SCIENCE PASS from schema presence.
- P2-M03 owner P01: all five strict profiles and DGP-003, DGP-004; NEG-011, NEG-012, NEG-013; REF-E05, REF-E03; no SCIENCE PASS from schema presence.
- P2-M04 owner P01: all five strict profiles and DGP-004; NEG-010, NEG-011, NEG-013; REF-E05, REF-E03; no SCIENCE PASS from schema presence.
- P2-M05 owner P02: all five strict profiles and DGP-002, DGP-003; NEG-010, NEG-012, NEG-013; REF-E05; no SCIENCE PASS from schema presence.
- P2-M06 owner P02: all five strict profiles and DGP-003, DGP-004; NEG-010, NEG-013; REF-E05; no SCIENCE PASS from schema presence.
- P2-M07 owner P02: all five strict profiles and DGP-003, DGP-004; NEG-011, NEG-012, NEG-013; REF-E05; no SCIENCE PASS from schema presence.
- P2-M08 owner P03: all five strict profiles and DGP-008; NEG-009, NEG-012, NEG-013; REF-E06; no SCIENCE PASS from schema presence.

## S02 / G04のSelf-contained Method・非スカラー出力契約（Owner承認）

対象`P2-M01〜P2-M08`の8件。5 Profile kindは`23_api_interface_design/schema_drafts/method_profiles/factored/e11_<kind>_factored_v1.json`（kind=method_config/question_profile/design_profile/output_profile/inference_profile）＋Method ID別overlayを再構成し、`e11_method_profile_dispatch_registry_draft1.json`で厳密dispatch/Blob SHA/Method正負例/標準Draft202012 Parityを確認。closed schema断片を`allOf`結合しない。未検証/unknown Methodには`METHOD_PROFILE_UNAVAILABLE`を返す。全8 MethodがEffect scalar `result.json`の`point=NOT_AVAILABLE`（ターゲットが関数であるため）と独立typed `cate_surface.json`をManifestに記載し、observed rowではない事前指定Design grid上の評価値・SHA・Method/Estimandを保存する。P2-M01〜07はnon-IV `NON_IV_CATE`、P2-M08は条件付きIV `CONDITIONAL_IV_STRUCTURAL_SLOPE`。両者を同一CATEと混同しない。個人レベル`X_i`やCATE値は公開しない。個票のbounded ParquetはG05のみが明示Study `row_export_requested=true`＋nonroot private ext4/XFS/Method別列行byte/memory capsで審査してG01 Sinkへ。共通SchemaはEconMLのmethod-specific inferenceを保証しない。

正規Context`LocalRunContext(root,principal)`とPrivacy Port`authorize(*,study,root,principal,output_shape)`。署名Verifier/Policy Anchor・Study`policy_ref`・追加CLI flagは撤廃。独立07は8 Methodの実Backend API、fitted inference、CI unsupportedをtyped、CATE grid mismatch/observed rows leak/IV target錯誤/Result scalar偽装/Manifest readback/hashの正負例を検査。既存KernelとProduct v2公開ABIを保護する。未実行をScience PASSにしない。

## S09 documented non-scalar output correction — P2-M01–M08 (2026-11-22)

The initial E11 output for each supported P2-M01–M08 `ESTIMATE` is a **non-scalar** conditional-effect function: P2-M01–07 = `NON_IV_CATE`; P2-M08 = `CONDITIONAL_IV_STRUCTURAL_SLOPE` (not ordinary CATE, B0 LATE or B1 coefficient). For a valid eligible run, `result.json` (`e11-local-effect-result/1`) must encode `point.availability=NOT_AVAILABLE`, `point.value=null`, and `point.reason.code=NON_SCALAR_TARGET` (not a top-level Result `point_availability` field); `status.json` separately reports `point_availability=NOT_AVAILABLE`; it must **not** present any fabricated scalar mean/ATE as the target. The Manifest inventories separate `cate_surface.json` with `schema_drafts/internal_scientific/e11_cate_surface_draft1.schema.json` semantics: method/estimand binding, immutable `predeclared_grid_ref`, `grid_origin`, unique typed `grid_key`, finite effects, inference availability and correct Study/source hashes. `observed_rows_included=false` is mandatory. Only predeclared **non-observed** design grid values are eligible; neither observed `X_i` nor individual effect rows may be placed there. User-specific row output remains a separate G05 Study-opt-in/private bounded Parquet path. If no admissible predeclared grid exists, fail with typed `GRID_UNSPECIFIED`, not an implicit training-data grid or empty-success file. JSON Schema shape is not proof of privacy or scientific correctness.

**P04 publication ownership:** validate and stage exactly the applicable `cate_surface.json` internal Artifact, strict Method/grid/estimand/source-hash binding and typed `result.json` non-scalar status through G01 Sink/Manifest/Reader. Enforce unique grid keys/finite values, row leakage zero, no observational dataset fallback, and prohibit a scalar mean masquerading as the target. One shared writer may be used, but never erase Method-specific constraints.
