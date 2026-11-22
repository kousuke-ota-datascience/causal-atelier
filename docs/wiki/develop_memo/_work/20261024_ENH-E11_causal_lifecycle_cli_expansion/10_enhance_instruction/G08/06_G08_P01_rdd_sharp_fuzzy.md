# ENH-E11 G08 P01 — rdd_sharp_fuzzy

**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G08 / **Package:** P01 / **Trial:** NOT_STARTED  
**Depends on Pxx:** NONE  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G08_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G08_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** cutoff/bandwidth/densityとFuzzy first stage、RBC CI API availabilityを検証。

**Scope:** 本PackageのClass/Methodと、それらが必要とする契約/適格性/Result Evidenceに限定。**Gate全体の保護意味:** Sharp/Fuzzy RDDとB0/B1 IV/2SLSを局所Estimand・弱IV AR集合付きで提供する。

**科学/Designの必須制約:** B0 complier LATEとB1 structural slopeを区別。HC1 AR集合をfinite gridだけで判定しない。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** cutoff/bandwidth/densityとFuzzy first stage、RBC CI API availabilityを検証。

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
| `RddAdapter` | `ariadne.scientific.causal_methods.quasi.RddAdapter` | Method Adapter ownership | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` |
| `EstimatorPort` | `ariadne.scientific.ports.causal.EstimatorPort` | Port/Value/Facade integration (no duplicate implementation) | estimate(self, request:ValidatedEstimatorRequest, *, sink:StagingArtifactSink) -> EffectOutcome |
| `InferenceEvidence` | `ariadne.causal.inference.contracts.InferenceEvidence` | Port/Value/Facade integration (no duplicate implementation) | validate_for(mode,method) |

**Method Adapter signature policy:** 新Adapterは原則`preflight(self,request:ValidatedMethodRequest)->EligibilityOutcome`／`execute(self,request:ValidatedMethodRequest,*,sink:StagingArtifactSink)->TypedScientificOutcome`。上表で指定された既存`run(self,input_,output_dir)`はその署名を保持。PortはApplication→Scientific kernelへ向かい、CLI Layerに別の科学数値実装を作らない。Constructor/Field/公開MethodとARConfidenceSetの境界は本Pxx§3.1以降の埋込Class契約が規範。外部DDはProvenanceのみ、未知のConcrete型を推測しない。

**Responsibility:** Method Adapterを担当するClassは `RddAdapter`。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。

### 3. Standalone Class-level contracts (normative)

Class Fields/Constructor/Method/Pre/Post/Failureは以下で本Package内に定義する。外部DDはprovenanceに限り、Agentが参照しなければ実装できない仕様を残さない。Designed Module≠Source実装済み。ABIはSource照合する。

### 3.1. `RddAdapter` — full fields/constructor/methods

#### 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.quasi.RddAdapter`。 EstimationのMethod実行Adapter。担当Method：`P3-M07, P3-M08`。**再利用:** 共通IV/EstimandとScientific CIを再利用しSharp/Fuzzyを明示区別。入口がCLIであることを科学的な別実装の根拠にしない。

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
| `P3-M07` | Sharp RD local effect | bandwidth、kernel/order、density manipulation、CI |
| `P3-M08` | Fuzzy RD local complier effect | First stage、discontinuity ratio、local IV inference |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本Package内の数理定義とMethod別科学契約に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 検証

`DD-E11-METH-P307`（`P3-M07`）、`DD-E11-METH-P308`（`P3-M08`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には本Packageの各Method DGP/NEG/REF一覧を優先し、この7区分の記載だけで科学的PASSとはしない。

### 3.2. `EstimatorPort` — full fields/constructor/methods

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

ProtocolはI/O無し。Concreteは本Pxx§3/§4の所有Class/Factoryのみ、単一MethodCapabilityPortで厳格選択。validated Request→typed outcomeを守り、実装時に外部DDの規範を推測補完しない。Concrete Owner/ABIが本書で確定しなければBLOCKED。

#### 検証

DD-E11-EFF01〜05。

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

## 4. G08/P01 required scientific and code execution

1. **Preconditions:** G08 Frozen06/07/Pxx、G01/G02 upstream canonical 999、Owner Coding Authorization、fixed candidate Source/lock、Pxx checkpointsを照合。Method/Design/IV assumptions/Estimand/Inference/Backend selectionをpreflightで検証。
2. `P3-M07` Sharp RDはrunning variable R、cutoff c、Bandwidth h、Kernel、Local polynomial order、covariates、Outcome discontinuityをMethod Configで固定し、cutoff近傍だけのTargetを推定。
3. `P3-M08` Fuzzy RDは同一cutoffにおけるOutcome jumpをTreatment first-stage jumpで割った局所IV/Complier effectとし、sharpの単なる別ラベルにしない。Zero/weak first-stageではfinite inferenceを捏造しない。
4. Assignment manipulation/density continuity、Covariate continuity、Bandwidth support、left/right sample countとRobust bias correction APIを検証する。`rdrobust`等の配布License適格性と数値推定Scienceは別判定。
5. **Dataflow:** Typed ValidatedMethodRequest→Method Adapter eligibility→selected numeric kernel/effective Backend→EffectOutcome/ARConfidenceSet→G01 StagingSink/Atomic Publisher/Reader。外部Backend model objectやRaw row/SecretsをResultへ含めない。
6. **Typed failure:** Zero denominator, rank/HC1 variance degeneracy, unsupported CI, invalid design, optional backend unavailable, numerical FAILED, legitimate scientific weak IVを明確に区別。Technical exit0はScience PASSでない。

### 設計書の採用済み意味論（独立した本Package実装規範）

以下は30_62/30_63に明文化された数理・Port・互換性の契約をこのPxxへ取り込んだもの。Scopeは本Packageの§3/4に限り、他PackageのClassを再実装しない。

- Sharp RD：cutoff周辺のlocal regression、bandwidth、polynomial order、kernel、density manipulation、covariate continuityの診断を出力。
- Fuzzy RD：cutoff近傍のTreatment first-stage jumpとOutcome jumpの比による局所IV効果。weak first stageやinstrument validityに注意。単なるSharp RDにlabelを変えるだけで代用しない。
- `rdrobust` 等の外部BackendはPython APIの実効版とrobust bias correction inferenceの利用可否を確認。GPLの顧客配布Legal approvalとは別。

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P3-M07` | Sharp RD local effect | bandwidth、kernel/order、density manipulation、CI |
| `P3-M08` | Fuzzy RD local complier effect | First stage、discontinuity ratio、local IV inference |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

**実際のBackend適格性・Config Schemaの未生成・独立OracleやCoverage証跡の不足は、上記Target/数理契約の未決とは区別する。** 実行後のScience判定を未検証のままPASSにしない。

## 5. Method-by-Method DGP/Negative/Reference Obligations

| Method | DD ID | Positive/Negative | Independent Reference | AC | 10_32 Readiness |
|---|---|---|---|---|---|
| `P3-M07` Sharp RDD／cutoff局所効果 | `DD-E11-METH-P307` | DGP-015; NEG-023 | REF-Q03 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q03 | PLAN:G08 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P3-M08` Fuzzy RDD／cutoff局所complier効果 | `DD-E11-METH-P308` | DGP-016; NEG-006, NEG-023 | REF-Q03, REF-I03 | AC-D03, AC-P01, AC-P03, AC-I01, AC-I02, AC-Q03 | PLAN:G08 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |

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
- **Mandatory focused cases:** `P3-M07` Sharp RDはrunning variable R、cutoff c、Bandwidth h、Kernel、Local polynomial order、covariates、Outcome discontinuityをMethod Configで固定し、cutoff近傍だけのTargetを推定。 `P3-M08` Fuzzy RDは同一cutoffにおけるOutcome jumpをTreatment first-stage jumpで割った局所IV/Complier effectとし、sharpの単なる別ラベルにしない。Zero/weak first-stageではfinite inferenceを捏造しない。 Assignment manipulation/density continuity、Covariate continuity、Bandwidth support、left/right sample countとRobust bias correction APIを検証する。`rdrobust`等の配布License適格性と数値推定Scienceは別判定。
- Unit: domain/Estimand/AR set serialization/edge cases; Contract: Class.Method、typed outputs、result discriminator/lineage; Integration: 実Backend、IV instrument/data support、real Publisher/readback、旧Product v2回帰。Weak IV / negative assumptions/HC1 confidence inversionは独立算出Referenceと照合。
- Environment/Backend/API、Source+fixture+lock SHA、DGP/negative、実行Command/Collection、Expected/Observed、Scientific vs Technical outcomeをEvidence化。未確定Oracle/quant K/R/coverageならBLOCKED、Science PASSは出さない。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** P04。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、当該PxxのOptional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。本Pxxの依存契約・科学的Referenceが未解決なら当該ScopeだけをBLOCKEDとする。他Gateの未決を全Packageの一律停止条件にせず、Agentによる推測補完を禁止する。


## 8. Freeze-critical standalone gaps

本PackageはClass Field/Constructor/Methodを§3、数理処理順序/分岐を§4、科学的DGP/NEG/REFとAcceptanceを§5〜6で内部定義する。**残未決:** RDDのBandwidth/kernel/order、実効Backend API、density/continuity testとLicense決定。 P3-M10/M11で有限gridだけのAR反転を実装することは禁止。OwnerがFreeze時に独立数理/Backend/ConfigとScience受入条件を明示的に判定する。

## 9. OD-05 Owner-adopted Method Profile construction obligation

**Accepted authoring allocation (2026-11-19 JST):** G08/P01 is responsible for strict versioned Config/Question/Design/Output/Inference Profile authoring/registration for P3-M07,M08. Scientific constraints: sharp/fuzzy RD bandwidth/kernel, B0/B1 binary Z/A/C and full-real weak-IV-robust AR target (HC1 χ²(1) inversion is provisional and not yet accepted). Retain existing §§3–6 Class/Method/algorithm/DGP/NEG/REF/AC semantics. Profiles declare conditional/mandatory fields, type domains, effective Backend/API/Version, analysis_mode/inference eligibility, output status/artifact shape, and no implicit backend defaults.

**Negative obligations:** unsupported method/profile/estimand, unknown fields, missing conditional fields, invalid Graph/Design/Question/DataRef identity, unavailable optional Backend, unsupported CI or invalid scientific assumptions are typed rejections; missing profile ⇒ `METHOD_PROFILE_UNAVAILABLE`. No silent fallback or `config={}` as a claim of support.

**Readiness:** Owner accepted work allocation only; this does not assert that individual schemas, independent DGP/REF, Backend execution, K/R/MC-SE/coverage, Gate07/999, Freeze or Coding Authorization are complete. For G08, exact HC1 AR numeric reference adoption history in PREP02-111 vs DD30_63 must be reconciled before Freeze without changing already adopted B0/B1/AR science bounds.


## PREP-04.1 embedded Method contracts (DRAFT)

### P3-M07 — strict Method contract (PREP-04.1 DRAFT / NOT_FROZEN)
- Scientific operation ESTIMATE, target=10_32 semantic target (not assigned canonical enum), owner P01. Preserve DiD2x2/staggered/event-time/ITS/RD/B0/B1 distinct targets and Estimands; B0 LATE is not B1 structural IV coefficient.
- Config mandatory fields: bandwidth, polynomial_order, kernel_spec_ref, cutoff. Strict type/const/domain as versioned method_config Schema, no unknown keys/defaults, reject config={}.
- Question mandatory: question_id, research_question, population, analysis_goal, estimand_family, contrast. Compare with Study/Design and upstream identification/graph hashes.
- Design mandatory: design_id, question_id, design_kind and running_variable, outcome, treatment, cutoff, continuity_assumption_ref, density_check_ref. Panel units/cohorts/time, cutoff continuity, IV assumption declarations and first-stage support validated semantically; references do not establish assumptions as true.
- Output: positive result.json/e11-local-effect-result/1 and G01 Reader/Marker/Manifest/Hash. AR confidence-set topology applies only to approved B0/B1 AR inference (P3-M10/M11), not to RD/Wald by default; when AR is applicable preserve ALL_REAL/UNBOUNDED/DISCONNECTED/BOUNDED, distinguish mathematical EMPTY from numerical FAILED, and reject finite-grid full-real claims.
- Inference: requested=false/null or true/confidence-level(0,1) accepted as syntax only; actual method-specific finite/AR CI capability and coverage must be independently validated, otherwise INFERENCE_UNAVAILABLE. B0/B1 HC1 AR formula/authority discrepancy remains BLOCKED.
- Independent tests DGP-015; NEG-023; REF-Q03. In addition empty/unknown key/wrong type or target, wrong temporal/cohort/cutoff/IV roles, absent assumption refs, weak/rank-deficient first stage, backend mismatch, unsupported CI and mis-hashed upstream rejected. Do not turn scientific negatives into technical failures or fallback.
- OPEN: actual backend API/License, proven inferential procedure, independent DGP/NEG/REF and prespecified K/R/FWER 0.05/MC-SE/coverage decision. NOT_FROZEN.


### P3-M08 — strict Method contract (PREP-04.1 DRAFT / NOT_FROZEN)
- Scientific operation ESTIMATE, target=10_32 semantic target (not assigned canonical enum), owner P01. Preserve DiD2x2/staggered/event-time/ITS/RD/B0/B1 distinct targets and Estimands; B0 LATE is not B1 structural IV coefficient.
- Config mandatory fields: bandwidth, polynomial_order, kernel_spec_ref, cutoff, first_stage_diagnostic_ref. Strict type/const/domain as versioned method_config Schema, no unknown keys/defaults, reject config={}.
- Question mandatory: question_id, research_question, population, analysis_goal, estimand_family, contrast. Compare with Study/Design and upstream identification/graph hashes.
- Design mandatory: design_id, question_id, design_kind and running_variable, outcome, treatment, cutoff, local_iv_assumptions_ref, first_stage_evidence_ref. Panel units/cohorts/time, cutoff continuity, IV assumption declarations and first-stage support validated semantically; references do not establish assumptions as true.
- Output: positive result.json/e11-local-effect-result/1 and G01 Reader/Marker/Manifest/Hash. AR confidence-set topology applies only to approved B0/B1 AR inference (P3-M10/M11), not to RD/Wald by default; when AR is applicable preserve ALL_REAL/UNBOUNDED/DISCONNECTED/BOUNDED, distinguish mathematical EMPTY from numerical FAILED, and reject finite-grid full-real claims.
- Inference: requested=false/null or true/confidence-level(0,1) accepted as syntax only; actual method-specific finite/AR CI capability and coverage must be independently validated, otherwise INFERENCE_UNAVAILABLE. B0/B1 HC1 AR formula/authority discrepancy remains BLOCKED.
- Independent tests DGP-016; NEG-006, NEG-023; REF-Q03, REF-I03. In addition empty/unknown key/wrong type or target, wrong temporal/cohort/cutoff/IV roles, absent assumption refs, weak/rank-deficient first stage, backend mismatch, unsupported CI and mis-hashed upstream rejected. Do not turn scientific negatives into technical failures or fallback.
- OPEN: actual backend API/License, proven inferential procedure, independent DGP/NEG/REF and prespecified K/R/FWER 0.05/MC-SE/coverage decision. NOT_FROZEN.


## S02・DEC-S05-AR01：G08 Method ProfileとAR Authorityの正規境界

担当Methodは`P3-M07` Sharp RDD、`P3-M08` Fuzzy RDD、`P3-M09` Binary Wald、`P3-M10` B0 2SLS、`P3-M11` B1 2SLSの5件。`23_api_interface_design/schema_drafts/method_profiles/factored/e11_<kind>_factored_v1.json`の5 Profile Kind（method_config/question_profile/design_profile/output_profile/inference_profile）をshared core＋exact Method ID overlayへ再構成し、Dispatch Registry、200 Schema標準Draft202012/Blob SHA/正負例の検証なしには`METHOD_PROFILE_UNAVAILABLE`。Method別EstimandとInferenceを保つ。B0は二値Z/A・無調整complier LATE、B1は事前Cを含む構造的`LINEAR_IV_STRUCTURAL_COEFFICIENT`、Fuzzy RDはcutoff局所complier効果であり、名称だけでATE/ATT/CATEへのcast不可。

**DEC-S05-AR01（Owner A採用）**：全実数領域での弱IV robust Anderson–Rubin信頼集合（bounded/unbounded/disconnected/ALL_REAL、退化・EMPTY等の明示判定）は既承認必須。HC1 OLS係数＋χ²(1)漸近検定＋二次式反転という**具体的計算法は独立科学Reviewerの妥当性確認前の実装候補でありFreezeしていない**。本Pxx/06/07に既存のHC1記述があっても、Ownerがそれを最終承認したと解釈しない。レビュー済み数理導出、全実数位相/弱IV/zero first-stage/分散退化/coverage、独立Oracle/実効Backend、T2-T3事前登録とOwnerによる契約確定がない場合、G08の当該方法は`BLOCKED_SCIENCE_METHOD_NOT_FROZEN`でGate999 PASS禁止。Point estimatorの可用性からAR可用性を推論しない。P3-M09 WaldにはARが自動付帯しない。

共通`LocalRunContext(root,principal)`、`LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)`。署名Verifier/Policy Anchor・CLI row flag・Study `policy_ref`なし。G08は個票を公開しない。共通Scientific Kernelと既存Product v2を保護する。G10では41 Method全件の有効Science証拠が必要だが、推移的依存閉包のSHAが完全不変なら証拠再利用を認め、変更/不明分のみ再実行/BLOCK。
