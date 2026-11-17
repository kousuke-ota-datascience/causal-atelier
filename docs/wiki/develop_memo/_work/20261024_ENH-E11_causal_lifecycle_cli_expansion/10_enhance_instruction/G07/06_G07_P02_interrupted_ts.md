# ENH-E11 G07 P02 — interrupted_ts

**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G07 / **Package:** P02 / **Trial:** NOT_STARTED  
**Depends on Pxx:** NONE  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G07_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G07_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** Intervention level/slope、seasonality、serial covariance/HACのmethod-specific evidence。

**Scope:** 本PackageのClass/Methodと、それらが必要とする契約/適格性/Result Evidenceに限定。**Gate全体の保護意味:** DiD/Event/ITSをtiming・pretrend・cluster・serial correlation条件付きで実行する。

**科学/Designの必須制約:** 2x2とstaggered DiDを同一TWFE ATTへ還元せず、ITSにiid SEを無検証適用しない。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** Intervention level/slope、seasonality、serial covariance/HACのmethod-specific evidence。

### 2A. Product Scientific Coreとの再利用境界（`2cf28f59a324`）
- **実在:** `src/ariadne/scientific/core_adapter.py`の`ScientificCoreAdapter.run_estimation(self, input_: EstimationInput, output_dir: Path)->list[ScientificResultDescriptor]`は旧Product Path API。`src/ariadne/causal/inference/estimators/treatment_effect.py`の`TreatmentEffectEstimator`はdiff/OLS/IPW/AIPW等の既存数値Kernelであり、DiD/Event/ITSの実装済み証拠ではない。旧API・DTO・WriterのABIを変更しない。
- **新規:** PanelQuasiAdapter/InterruptedTsAdapterは§3のDesign Classとして実装。Panel単位・処置開始時点・staggered cohort・参照期・cluster/NW-HAC covarianceの対象/単位を明示した合法的Request→typed Effectを作る。旧Kernel再利用は同一estimand/varianceで数理的に適合する場合のみ。E11 `EstimatorPort.estimate(..., *, sink:StagingArtifactSink)`へのBridgeは共通Scientific Kernelを経由し、G01 Registry/Publisherを新規生成しない。Owner未承認のEstimator/Inference Policyは`BLOCKED_CONTRACT_AMBIGUITY`。

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
| `InterruptedTsAdapter` | `ariadne.scientific.causal_methods.quasi.InterruptedTsAdapter` | Method Adapter ownership | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` |
| `EstimatorPort` | `ariadne.scientific.ports.causal.EstimatorPort` | Port/Value/Facade integration (no duplicate implementation) | estimate(self, request:ValidatedEstimatorRequest, *, sink:StagingArtifactSink) -> EffectOutcome |
| `InferenceEvidence` | `ariadne.causal.inference.contracts.InferenceEvidence` | Port/Value/Facade integration (no duplicate implementation) | validate_for(mode,method) |

**Method Adapter signature policy:** 新Adapterは原則`preflight(self,request:ValidatedMethodRequest)->EligibilityOutcome`／`execute(self,request:ValidatedMethodRequest,*,sink:StagingArtifactSink)->TypedScientificOutcome`。上表で指定された既存`run(self,input_,output_dir)`はその署名を保持。PortはApplication→Scientific kernelへ向かい、CLI Layerに別の科学数値実装を作らない。本Pxx§3.1以降のClass定義がField/Constructor/Methodの規範であり、外部DDはprovenanceのみ。Design未確定箇所や実Backend ABIを補完せずBLOCKEDで停止する。

**Responsibility:** Method Adapterを担当するClassは `InterruptedTsAdapter`。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。

### 3. Standalone Class/Method contracts

以下をNormative Contractとして本Pxxに展開する。DDはProvenanceのみ、別06/07はCodingの不足判断を補完するSourceにしない。Class存在とLegacy ABIは実Sourceで確認し、設計Classと混同しない。

### 3.1. `InterruptedTsAdapter` — inline Field/Constructor/Method contract

#### 1.17.1. 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.quasi.InterruptedTsAdapter`。 EstimationのMethod実行Adapter。担当Method：`P3-M06`。**再利用:** 共通Time/Design検証を再利用しITS HAC推論を追加。入口がCLIであることを科学的な別実装の根拠にしない。

#### 1.17.2. フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### 1.17.3. Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### 1.17.4. メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedMethodRequest)` | `EligibilityOutcome` | Method/Estimand/Design/Backend Profileの静的適格性を型付きで返す。推定処理・File公開なし |
| `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` | `TypedScientificOutcome` | 適格なMethodだけ実行し、ArtifactはStagingへ。外部Backend Objectを返さない |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 1.17.5. 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P3-M06` | level/slope change | intervention date、seasonality/autocorrelation/HAC |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本Pxx固有のMethod/Science contractに保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### 1.17.6. I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 1.17.7. 検証

`DD-E11-METH-P306`（`P3-M06`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には本PxxのMethod別DGP/NEG/REF/AC obligationsを優先し、この7区分の記載だけで科学的PASSとはしない。

### 3.2. `EstimatorPort` — inline Field/Constructor/Method contract

#### 5.2.1. 識別情報・責務

**Protocol配置：ariadne.scientific.ports.causal.EstimatorPort。** 既存Product `ScientificCorePort`のv2メソッドを保持し、旧APIと型付きPortは共通科学計算を用いる互換Bridgeで接続する。

#### 5.2.2. フィールド

N/A：Protocol自身はinstance fieldを所有しない。

#### 5.2.3. Constructor / Factory

N/A：Protocolに具体Factoryはない。Concreteの依存関係注入はAdapterの責務。

#### 5.2.4. メソッド

```python
class EstimatorPort(Protocol):
    def estimate(self, request: ValidatedEstimatorRequest, *, sink: StagingArtifactSink) -> EffectOutcome: ...
```

#### 5.2.5. 処理仕様

識別・Method適格なRequestのみ実行し、ArtifactをStagingSinkへ限定。科学的PreconditionはWeb/CLI共通であり、CLI optionやHTTP状態ではない。

#### 5.2.6. I/O・連携・失敗処理

Protocol自体はI/Oを持たない。Concrete Adapterは本書§3/§4で所有が割り当てられたClassのみが実装し、単一MethodCapabilityPort経由で選択する。validated Request→typed outcome/staging sinkを守り、外部DDを未記載の実装規範の代用としない。Owner/ABIが未確定なら新Facadeを創作せずBLOCKED。

#### 5.2.7. 検証

DD-E11-EFF01〜05。

### 3.3. `InferenceEvidence` — inline Field/Constructor/Method contract

#### 3.2.1. 識別情報・責務

**Class / module:** `ariadne.causal.inference.contracts.InferenceEvidence`。Inferenceの可用性と実際のFinite CI／AR集合を型付きで保持する。

#### 3.2.2. フィールド

| Field | Type | 制約 |
|---|---|---|
| `availability` | `InferenceAvailability` | AVAILABLE/UNAVAILABLE/FAILED/NOT_REQUESTED等 |
| `kind` | Method-specific enum | 実効推論方式 |
| `interval, confidence_set` | `FiniteInterval|None, ARConfidenceSet|None` | AVAILABLEなら正当な片方ちょうど1つ |
| `reason` | `ScientificReason|None` | nonAVAILABLEでは必須 |
| `method_config` | typed config | Backend/Method/Estimandに適合 |

#### 3.2.3. Constructor / Factory

Constructor/Factoryはavailabilityとevidenceの排他性、およびreason整合を検査。実行済みCIをデフォルト値で捏造しない。

#### 3.2.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `validate_for(mode,method)` | Validated inference / typed reason | pure Method/analysis-mode適格性検査 | unsupported confirmatory inference |

#### 3.2.5. 処理仕様

EXPLORATORY point-onlyとCONFIRMATORY inference要件を分離する。FiniteIntervalとARConfidenceSetを丸め合わせず、SCM point-onlyを確証CIと報告しない。

#### 3.2.6. I/O・連携・失敗処理

Value操作I/Oなし。Backend provenance・coverageの計算は30_63へ委譲。

#### 3.2.7. 検証

`DD-E11-AR04/AR05`、`DD-E11-EFF01/02`、Method-specific CI availability、independent coverage。

## 4. Required implementation steps — G07/P02

1. **Entry:** Current G07のFrozen06/07/Pxx、Owner Coding Authorization、Source/lock full SHA、当該06のupstream 999とPxx依存Checkpointを確認してから実装。Valid Study/Method/Design/Data/Estimand/Backendを境界で検証。
2. `P3-M06` Interrupted Time Seriesはintervention date、pre/post trend、level/slope change、季節性とserial correlationをMethod configで固定する。
3. HAC/autocorrelation-aware inferenceの適格性を実際の残差/series length/lag設計で確認し、iid OLS SEを無検証でConfirmed CIへ流用しない。
4. Causal interruption designのAssumptionとObservational trendの違いを記録し、InterruptedTsAdapterがtyped level/slope effectsとUncertainty Evidenceを出力。
5. **I/O/Failure:** Approved Method Adapter preflight→selected Backend（必要時lazy import）→typed Scientific Outcome→G01 Staging Publisher/Reader。Invalid config、合法的Scientific negative、不確定CI、Backend failureを分離し、Resultにeffective Method/Backend/Seed/Time/Design Evidenceを保存。
6. **Non-goals:** 旧v2 Public ABI、Web/API/DB/Worker、G01 GraphVersion/Publisherの再実装、未承認row export、Backend実測なしのScience PASSを禁止。

## 5. Method-by-Method DGP/Negative/Reference Obligations

| Method | DD ID | Positive/Negative | Independent Reference | AC | 10_32 Readiness |
|---|---|---|---|---|---|
| `P3-M06` Interrupted Time Series／介入時点のlevel | `DD-E11-METH-P306` | DGP-014; NEG-023 | REF-Q02 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q02 | PLAN:G07 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |

**Proof boundary:** §5のDGP/NEG/REF/ACは独立に実証すべき義務であり、Fixture/Oracleの実在やPASSを意味しない。Backend出力を自己正解にせず、時系列Graph/Quasi Methodごとの独立Referenceと実測で検証する。FWER=.05/K/R/CI coverage/MC-SE未確定はBLOCKED。外部資料から推測して決めない。

## 6. Focused Verification Contract — WHAT, not physical filename

| Layer | Required behavior |
|---|---|
| unit | Value/Estimand/Method schema、negative、Hash/Status/No-False-PASS、pure Algorithm。 |
| contract | `Class.Method`入出力、Port/Backend Registry選択、typed evidence/Lineage、Version+Codec。 |
| integration | 必要な実Backend/CLI/FS/Atomic readback、optional Profile、既存Product v2回帰。 |
| scientific evidence | Method別DGP/NEG/independent reference、定量Simulation/coverage/MC-SE。 |

TestはLifecycle（enhancement/regression/characterization/benchmark/support/legacy）とLayer（unit/contract/integration/frontend/browser_e2e）を独立分類。新規は`tests/enhancement/enh_e11/g07/<layer>/`に原則配置、実Path/command/pytest collectionは40 Operatorがcurrent checkoutからdiscover。受入07をpathの文字列で置き換えない。Mock-onlyでreal Backend/FS/ScienceをPASSにしない。

### 6.1. Method-specific independent verification obligations

- §5のDGP/NEG/REF/DD IDを、Science/Status/Method-config/Source-hashに対応させる。ID一覧はFixture実在や科学的PASSの証拠ではない。
- **Positive and negative matrix:** `P3-M06` Interrupted Time Seriesはintervention date、pre/post trend、level/slope change、季節性とserial correlationをMethod configで固定する。 HAC/autocorrelation-aware inferenceの適格性を実際の残差/series length/lag設計で確認し、iid OLS SEを無検証でConfirmed CIへ流用しない。 Causal interruption designのAssumptionとObservational trendの違いを記録し、InterruptedTsAdapterがtyped level/slope effectsとUncertainty Evidenceを出力。
- Pure Value/Graph/Design→unit、Port/Codec/typed Reason→contract、実Backend/Tigramite/Quasi/CLI/Pub-Readback/legacy v2→integration。科学Graph/EffectのReferenceはBackend出力とは別に事前固定する。
- Effective backend API/version, Test fixture/Source/lock SHA, seed, Data/Time ordering, CI/SE handling, observed outcome, actual test collection/command, FAIL/BLOCKED causeをEvidenceへ記録。必須RuntimeやOracleが未確定ならBLOCKED。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** P03。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、Optional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。G05 Row Writer/Trust Anchor等の設計不在、G02 IV target、G08 AR独立reference等を推測で解決しない。


## 8. Freeze-only review: unresolved decisions

**Self-contained:** §3は全ClassのField/Constructor/Public Method/I-Oを、§4は実装分岐を、§5〜6は必要なMethod/DGP/NEG/REFと検証を本文で保持する。**BLOCKED before Freeze:** ITS季節性/Trend、HAC/serial-covariance method、CIの推論適格性。 他文書の参照をCoding Agentに必須とせず、設計空白はOwner決定まで止める。
