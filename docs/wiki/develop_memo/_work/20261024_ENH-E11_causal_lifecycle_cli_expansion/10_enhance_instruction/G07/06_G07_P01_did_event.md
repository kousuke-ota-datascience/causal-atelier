# ENH-E11 G07 P01 — did_event

**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G07 / **Package:** P01 / **Trial:** NOT_STARTED  
**Depends on Pxx:** NONE  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G07_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G07_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** Cohort/adoption timing/parallel trend/pretrend、reference period、cluster covarianceを保持。

**Scope:** 本PackageのClass/Methodと、それらが必要とする契約/適格性/Result Evidenceに限定。**Gate全体の保護意味:** DiD/Event/ITSをtiming・pretrend・cluster・serial correlation条件付きで実行する。

**科学/Designの必須制約:** 2x2とstaggered DiDを同一TWFE ATTへ還元せず、ITSにiid SEを無検証適用しない。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** Cohort/adoption timing/parallel trend/pretrend、reference period、cluster covarianceを保持。

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
| `PanelQuasiAdapter` | `ariadne.scientific.causal_methods.quasi.PanelQuasiAdapter` | Method Adapter ownership | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` |
| `EstimatorPort` | `ariadne.scientific.ports.causal.EstimatorPort` | Port/Value/Facade integration (no duplicate implementation) | estimate(self, request:ValidatedEstimatorRequest, *, sink:StagingArtifactSink) -> EffectOutcome |
| `EstimatorRequest` | `ariadne.causal.inference.contracts.EstimatorRequest` | Port/Value/Facade integration (no duplicate implementation) | validate_against(self, identification:IdentificationOutcome, design:CausalDesign, policy:EstimandEligibilityPolicy) -> ValidatedEstimatorRequest |

**Method Adapter signature policy:** 新Adapterは原則`preflight(self,request:ValidatedMethodRequest)->EligibilityOutcome`／`execute(self,request:ValidatedMethodRequest,*,sink:StagingArtifactSink)->TypedScientificOutcome`。上表で指定された既存`run(self,input_,output_dir)`はその署名を保持。PortはApplication→Scientific kernelへ向かい、CLI Layerに別の科学数値実装を作らない。本Pxx§3.1以降のClass定義がField/Constructor/Methodの規範であり、外部DDはprovenanceのみ。Design未確定箇所や実Backend ABIを補完せずBLOCKEDで停止する。

**Responsibility:** Method Adapterを担当するClassは `PanelQuasiAdapter`。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。

### 3. Standalone Class/Method contracts

以下をNormative Contractとして本Pxxに展開する。DDはProvenanceのみ、別06/07はCodingの不足判断を補完するSourceにしない。Class存在とLegacy ABIは実Sourceで確認し、設計Classと混同しない。

### 3.1. `PanelQuasiAdapter` — inline Field/Constructor/Method contract

#### 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.quasi.PanelQuasiAdapter`。 EstimationのMethod実行Adapter。担当Method：`P3-M04, P3-M05`。**再利用:** 共通Estimand/Design/Time validationを再利用しDiD/Event Study推定を追加。入口がCLIであることを科学的な別実装の根拠にしない。

#### フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedMethodRequest)` | `EligibilityOutcome` | Method/Estimand/Design/Backend Profileの静的適格性を型付きで返す。推定処理・File公開なし |
| `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` | `TypedScientificOutcome` | 適格なMethodだけ実行し、ArtifactはStagingへ。外部Backend Objectを返さない |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P3-M04` | DiD ATT | DID_2X2 positive / STAGGERED DEFERRED preflight rejection、parallel trends、SE/cluster |
| `P3-M05` | Event Study | cohort/event time、pretrend、reference periods |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本Pxx固有のMethod/Science contractに保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 検証

`DD-E11-METH-P304`（`P3-M04`）、`DD-E11-METH-P305`（`P3-M05`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には本PxxのMethod別DGP/NEG/REF/AC obligationsを優先し、この7区分の記載だけで科学的PASSとはしない。

### 3.2. `EstimatorPort` — inline Field/Constructor/Method contract

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

Protocol自体はI/Oを持たない。Concrete Adapterは本書§3/§4で所有が割り当てられたClassのみが実装し、単一MethodCapabilityPort経由で選択する。validated Request→typed outcome/staging sinkを守り、外部DDを未記載の実装規範の代用としない。Owner/ABIが未確定なら新Facadeを創作せずBLOCKED。

#### 検証

DD-E11-EFF01〜05。

### 3.3. `EstimatorRequest` — inline Field/Constructor/Method contract

#### 識別情報・責務

**Class / module:** `ariadne.causal.inference.contracts.EstimatorRequest`。Identification proofが適格な場合だけEstimatorへ渡すRequest Value。

#### フィールド

| Field | Type・制約 |
|---|---|
| `method_id, estimand_family` | Method×target一致 |
| `identification_ref` | 上流証拠参照 |
| `question/design/graph/dataset_hashes` | 完全な上流digest集合 |
| `method_config, inference_request` | Method/Inference適格なtyped config |

#### Constructor / Factory

`validate_against(identification,design,policy)->ValidatedEstimatorRequest`は入力と上流証拠を照合する型付きvalidator。Validation前の生RequestをAdapterへ送らない。

#### メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `validate_against(self, identification:IdentificationOutcome, design:CausalDesign, policy:EstimandEligibilityPolicy)` | `ValidatedEstimatorRequest` | pure eligibility check | scientific negative / schema validation区別 |

#### 処理仕様

Method-specific assumptions、Mediator/Instrument/support、Data Eligibility、Graph/Design/Question/Dataset hash全一致、CI要求を検証。不適格は`ScientificNegativeOutcome`としてBackend未呼出。Path/schema mismatchはtechnical validationとする。

#### I/O・連携・失敗処理

Value自身はI/Oなし。ScientificValidationServiceの既存適格性規則を共通pure policyとして再利用する。実Estimator I/O/Artifactは`EstimatorPort.estimate(...,sink)`を通す。

#### 検証

`DD-E11-ID01〜04`およびMethod固有Negative Tests。

## 4. Required implementation steps — G07/P01

1. **Entry:** Current G07のFrozen06/07/Pxx、Owner Coding Authorization、Source/lock full SHA、当該06のupstream 999とPxx依存Checkpointを確認してから実装。Valid Study/Method/Design/Data/Estimand/Backendを境界で検証。
2. `P3-M04` DiDは初期DID_2X2 ATTのみを正例とし、STAGGEREDはDEFERREDの科学的拒否負例として検証。Parallel trends/equilibrium、cohort/Time support、cluster covariance unitをPreflightし、TWFE係数を汎用staggered ATTへ転用しない。
3. `P3-M05` Event Studyはcohort/event-time window/reference period、lead/pretrend診断、post-treatment selection、unit/time indexを事前指定し、event-time vectorと基準期間をtyped schemaに残す。
4. 適格性に違反するCohort、no pre/post、cluster不足、pretrend失敗と不確実診断を型付きで分け、ATTとevent-timeの異なる推論を単一数値として扱わない。
5. **I/O/Failure:** Approved Method Adapter preflight→selected Backend（必要時lazy import）→typed Scientific Outcome→G01 Staging Publisher/Reader。Invalid config、合法的Scientific negative、不確定CI、Backend failureを分離し、Resultにeffective Method/Backend/Seed/Time/Design Evidenceを保存。
6. **Non-goals:** 旧v2 Public ABI、Web/API/DB/Worker、G01 GraphVersion/Publisherの再実装、未承認row export、Backend実測なしのScience PASSを禁止。

### 設計で定義済みのGraph／Quasi意味論（自己完結した実装規範）

以下は既存の詳細設計に記載された規則を本Packageへ直接展開したもの。Designの決定済み部分を不明事項としてAgentに再判断させない。実効Backend/API probe、独立Graph/Counterfactual Oracle、推論可用性の未実測は別にBLOCKEDとする。

- DiD：初期`DID_2X2` ATTのみを実行可能とし、staggeredは将来の別Configuration/EstimandとしてDEFERREDのまま保持し、staggeredに単純TWFE係数を普遍的ATTとして流用しない。parallel trendsとcohort support、cluster covarianceのunitを保存。
- Event Study：事前指定reference periodとevent-time vector、cohort composition、lead/pretrend診断を保持。post-intervention windowによる選択が推論に与える影響を記録。

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P3-M04` | DiD ATT | DID_2X2 positive / STAGGERED DEFERRED preflight rejection、parallel trends、SE/cluster |
| `P3-M05` | Event Study | cohort/event time、pretrend、reference periods |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

## 5. Method-by-Method DGP/Negative/Reference Obligations

| Method | DD ID | Positive/Negative | Independent Reference | AC | 10_32 Readiness |
|---|---|---|---|---|---|
| `P3-M04` DiD／初期DID_2X2 ATTのみ（STAGGERED=DEFERRED） | `DD-E11-METH-P304` | DGP-012（初期2×2正例）, DGP-013（P3-M04 STAGGEREDは将来・P3-M05は別）; NEG-022 | REF-Q01 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q01 | PLAN:G07 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P3-M05` Event Study／event-time効果 | `DD-E11-METH-P305` | DGP-013; NEG-022 | REF-Q01 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q01 | PLAN:G07 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |

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
- **Positive and negative matrix:** `P3-M04` DiDは初期DID_2X2 ATTのみを正例とし、STAGGEREDはDEFERREDの科学的拒否負例として検証。Parallel trends/equilibrium、cohort/Time support、cluster covariance unitをPreflightし、TWFE係数を汎用staggered ATTへ転用しない。 `P3-M05` Event Studyはcohort/event-time window/reference period、lead/pretrend診断、post-treatment selection、unit/time indexを事前指定し、event-time vectorと基準期間をtyped schemaに残す。 適格性に違反するCohort、no pre/post、cluster不足、pretrend失敗と不確実診断を型付きで分け、ATTとevent-timeの異なる推論を単一数値として扱わない。
- Pure Value/Graph/Design→unit、Port/Codec/typed Reason→contract、実Backend/Tigramite/Quasi/CLI/Pub-Readback/legacy v2→integration。科学Graph/EffectのReferenceはBackend出力とは別に事前固定する。
- Effective backend API/version, Test fixture/Source/lock SHA, seed, Data/Time ordering, CI/SE handling, observed outcome, actual test collection/command, FAIL/BLOCKED causeをEvidenceへ記録。必須RuntimeやOracleが未確定ならBLOCKED。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** P03。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、当該PxxのOptional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。本Pxxの依存契約・科学的Referenceが未解決なら当該ScopeだけをBLOCKEDとする。他Gateの未決を全Packageの一律停止条件にせず、Agentによる推測補完を禁止する。


## 8. Freeze-only review: unresolved decisions

**Self-contained:** §3は全ClassのField/Constructor/Public Method/I-Oを、§4は実装分岐を、§5〜6は必要なMethod/DGP/NEG/REFと検証を本文で保持する。**BLOCKED before Freeze:** DID_2X2 positive / STAGGERED DEFERRED preflight rejection DiDのEstimator/inference policyとcluster covariance、Event reference periodの承認。 他文書の参照をCoding Agentに必須とせず、設計空白はOwner決定まで止める。

## 9. OD-05 Owner-adopted Method Profile construction obligation

**Accepted authoring allocation (2026-11-19 JST):** G07/P01 is responsible for strict versioned Config/Question/Design/Output/Inference Profile authoring/registration for P3-M04,M05. Scientific constraints: DiD 初期2x2 ATTのみ／STAGGERED DEFERRED/cluster, event-time reference cohort, ITS level/slope/HAC. Retain existing §§3–6 Class/Method/algorithm/DGP/NEG/REF/AC semantics. Profiles declare conditional/mandatory fields, type domains, effective Backend/API/Version, analysis_mode/inference eligibility, output status/artifact shape, and no implicit backend defaults.

**Negative obligations:** unsupported method/profile/estimand, unknown fields, missing conditional fields, invalid Graph/Design/Question/DataRef identity, unavailable optional Backend, unsupported CI or invalid scientific assumptions are typed rejections; missing profile ⇒ `METHOD_PROFILE_UNAVAILABLE`. No silent fallback or `config={}` as a claim of support.

**Readiness:** Owner accepted work allocation only; this does not assert that individual schemas, independent DGP/REF, Backend execution, K/R/MC-SE/coverage, Gate07/999, Freeze or Coding Authorization are complete. For G08, exact HC1 AR numeric reference adoption history in PREP02-111 vs DD30_63 must be reconciled before Freeze without changing already adopted B0/B1/AR science bounds.


## PREP-04.1 embedded Method contracts (DRAFT)

### P3-M04 — strict Method contract (PREP-04.1 DRAFT / NOT_FROZEN)
- Scientific operation ESTIMATE, target=ATT, owner P01. Preserve DiD2x2/staggered/event-time/ITS/RD/B0/B1 distinct targets and Estimands; B0 LATE is not B1 structural IV coefficient.
- Config mandatory fields: design_variant, estimator_spec_ref, cluster_covariance_spec_ref. Strict type/const/domain as versioned method_config Schema, no unknown keys/defaults, reject config={}.
- Question mandatory: question_id, research_question, population, analysis_goal, estimand_family, contrast. Compare with Study/Design and upstream identification/graph hashes.
- Design mandatory: design_id, question_id, design_kind and unit_id, time_id, treatment, outcome, parallel_trends_assumption_ref. Panel units/cohorts/time, cutoff continuity, IV assumption declarations and first-stage support validated semantically; references do not establish assumptions as true.
- Output: positive result.json/e11-local-effect-result/1 and G01 Reader/Marker/Manifest/Hash. P3-M05 Event Study must write its already specified typed event_time_effects.json vector; ITS level/slope components retain their separate Method-specific output rules. Neither can be coerced to a scalar point.value or an AR confidence-set. Unavailable components require typed reason.
- Inference: requested=false/null or true/confidence-level(0,1) accepted as syntax only; actual method-specific finite/AR CI capability and coverage must be independently validated, otherwise INFERENCE_UNAVAILABLE. B0/B1 HC1 AR formula/authority discrepancy remains BLOCKED.
- Independent tests DGP-012（初期2×2正例）, DGP-013（P3-M04 STAGGEREDは将来・P3-M05は別）; NEG-022; REF-Q01. In addition empty/unknown key/wrong type or target, wrong temporal/cohort/cutoff/IV roles, absent assumption refs, weak/rank-deficient first stage, backend mismatch, unsupported CI and mis-hashed upstream rejected. Do not turn scientific negatives into technical failures or fallback.
- OPEN: actual backend API/License, proven inferential procedure, independent DGP/NEG/REF and prespecified K/R/FWER 0.05/MC-SE/coverage decision. NOT_FROZEN.


### P3-M05 — strict Method contract (PREP-04.1 DRAFT / NOT_FROZEN)
- Scientific operation ESTIMATE, target=10_32 semantic target (not assigned canonical enum), owner P01. Preserve DiD2x2/staggered/event-time/ITS/RD/B0/B1 distinct targets and Estimands; B0 LATE is not B1 structural IV coefficient.
- Config mandatory fields: event_window_start, event_window_end, reference_event_time, cohort_estimator_spec_ref, cluster_covariance_spec_ref. Strict type/const/domain as versioned method_config Schema, no unknown keys/defaults, reject config={}.
- Question mandatory: question_id, research_question, population, analysis_goal, estimand_family, contrast. Compare with Study/Design and upstream identification/graph hashes.
- Design mandatory: design_id, question_id, design_kind and unit_id, time_id, treatment, outcome, cohort_id, pretrend_assumption_ref. Panel units/cohorts/time, cutoff continuity, IV assumption declarations and first-stage support validated semantically; references do not establish assumptions as true.
- Output: positive result.json/e11-local-effect-result/1 and G01 Reader/Marker/Manifest/Hash. P3-M05 Event Study must write its already specified typed event_time_effects.json vector; ITS level/slope components retain their separate Method-specific output rules. Neither can be coerced to a scalar point.value or an AR confidence-set. Unavailable components require typed reason.
- Inference: requested=false/null or true/confidence-level(0,1) accepted as syntax only; actual method-specific finite/AR CI capability and coverage must be independently validated, otherwise INFERENCE_UNAVAILABLE. B0/B1 HC1 AR formula/authority discrepancy remains BLOCKED.
- Independent tests DGP-013; NEG-022; REF-Q01. In addition empty/unknown key/wrong type or target, wrong temporal/cohort/cutoff/IV roles, absent assumption refs, weak/rank-deficient first stage, backend mismatch, unsupported CI and mis-hashed upstream rejected. Do not turn scientific negatives into technical failures or fallback.
- OPEN: actual backend API/License, proven inferential procedure, independent DGP/NEG/REF and prespecified K/R/FWER 0.05/MC-SE/coverage decision. NOT_FROZEN.


## S02簡素化・G07 Quasi Method/Vector Outputの規範

担当Methodは`P3-M04` DiD、`P3-M05` Event Study、`P3-M06` ITSの3件。`23_api_interface_design/schema_drafts/method_profiles/factored/e11_<kind>_factored_v1.json`の5 kind（method_config/question_profile/design_profile/output_profile/inference_profile）からshared＋Method overlayを単一strict Schemaとして再構築し、Dispatch Registry、Blob SHA/標準Draft202012/parity/Method別正負例の証拠がなければ`METHOD_PROFILE_UNAVAILABLE`。DiDの2x2/staggered、Event Studyのcohort/time/reference period、ITSのlevel/slope/HAC/autocorrelationを混同しない。P3-M05ではscalar `result.json`のpointを`NOT_AVAILABLE`とし、cohort×event-timeのtyped `event_time_effects.json`と独立Manifest/ContentRefを発行。推論は実Method/Backendで対応が証明された場合のみAVAILABLE、指定period前のpretrend/介入時点負例とCI shape/Graph・Study lineageを独立07で検証する。

Contextは`LocalRunContext(root,principal)`、Privacy Portは`authorize(*,study,root,principal,output_shape)`。署名Verifier/Policy Anchor・`cli_row_flag`・Study `policy_ref`・追加CLI opt-inを設けない。個票はG05だけがStudy `row_export_requested=true`と非root同一UID private ext4/XFS/Method別capsをANDしてG01 Sinkへ。旧Product v2と共通KernelのABIを保護、科学Oracleと実Backend/CIを未実行ならScience BLOCKED。全Product Suite無条件実行ではなく影響閉包で回帰を決定、不明なら実行またはBLOCK。

## S09 documented Event Study vector contract — P3-M05 (2026-11-22)

P3-M05 `ESTIMATE` has an **event-time/cohort effect vector**, not a scalar target. For an eligible Event Study run, `result.json` has nested `point.availability=NOT_AVAILABLE`, `point.value=null`, `point.reason.code=NON_SCALAR_TARGET`, while `status.json` has top-level `point_availability=NOT_AVAILABLE`; the Manifest must inventory `event_time_effects.json` conforming to `schema_drafts/internal_scientific/e11_event_time_effects_draft1.schema.json`. It binds `method_id=P3-M05`, `study_ref`, `reference_period`, `time_unit`, cohort/event-time keyed `effects`, inference availability/interval references and `pretrend_diagnostics_ref`. The designated reference period and cohort/time support must be predeclared; unique event-time/cohort keys, finite effects, no invalid pretrend concealment, and exact readback/hash/lineage are required. Do not synthesize a scalar ATT/ATE from the vector or substitute an AR confidence set. Other Methods (DiD/ITS) retain their distinct output/inference contracts.

**P01:** Construct the typed event-time/cohort vector and reference/pretrend evidence without collapsing it into an ATT. Pass it to P03; do not create a parallel Bundle writer.

## Owner A frozen scope decision — DEC-S09-P3M04-01 (2026-11-22, instruction DRAFT)

**Owner DEC-S09-P3M04-01=A (2026-11-22):** P3-M04 initial science-executable variant is only `design_variant=DID_2X2` for two-group/two-period ATT; `STAGGERED` is a recognized future Config variant with capability `DEFERRED`, **not RETIRED** and not an eligible science target. Valid syntax does not imply execution. After strict validation, Method-level scientific preflight must reject `STAGGERED` with typed `SCIENCE_CONTRACT_NOT_AVAILABLE` / `CAPABILITY_UNAVAILABLE` (CLI exit4), before calling PanelQuasiAdapter/Estimator/Backend or any row-materializing scientific source; do not publish a successful `result.json`, `manifest.json` or committed success marker for that request. Unknown variant/invalid type/missing required Config are input-Schema failures (exit2). Do not fall back to DID_2X2, a TWFE coefficient, or P3-M05 Event Study. Valid DID_2X2 still needs Design, unit/time support, pre-declared parallel trends and cluster-covariance eligibility and independent DGP-012/NEG/REF-Q01 verification; no backend/science acceptance is yet established. DGP-013 remains relevant to P3-M05 and possible later STAGGERED research, but is not P3-M04 initial executable positive.

**Gate/Package-specific instruction:** P01: implement DID_2X2 ATT/legitimate unit-cluster inference only. Test deferred-STAGGERED preflight *before* actual estimator/Backend calls. No separate staggered estimator or data-driven scalar aggregation in this coding scope.
