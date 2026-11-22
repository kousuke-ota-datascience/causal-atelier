# ENH-E11 G09 P01 — scm_point

**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G09 / **Package:** P01 / **Trial:** NOT_STARTED  
**Depends on Pxx:** NONE  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G09_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G09_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** Donor weights/pre-treatment RMSPE/fit・counterfactual gap。SCMは初期point-only。

**Scope:** 本PackageのClass/Methodと、それらが必要とする契約/適格性/Result Evidenceに限定。**Gate全体の保護意味:** Donor Designに基づきSCM point-onlyとSDID point/inferenceを区別する。

**科学/Designの必須制約:** Donor汚染・pre-fit・time support負例必須。SCMに未検証CIを付けない。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** Donor weights/pre-treatment RMSPE/fit・counterfactual gap。SCMは初期point-only。

### 2A. Existing Source ABIと合成対照Methodの所有（`2cf28f59a324`）
- **実在:** `src/ariadne/scientific/core_adapter.py`の`ScientificCoreAdapter.run_estimation(self, input_: EstimationInput, output_dir: Path)->list[ScientificResultDescriptor]`は旧Product Path API。 `src/ariadne/causal/inference/estimators/treatment_effect.py`の数値KernelはSCM/SDIDの実装済み証拠でない。
- **Design-only:** `SyntheticControlAdapter/SyntheticDidAdapter`は§3/§4のE11新規Scientific Adapter、`EstimatorPort.estimate(ValidatedEstimatorRequest, *, sink:StagingArtifactSink)->EffectOutcome`は型付きPort。旧Path API/旧Writerの公開ABIを維持し、共有純粋Kernelでのみ接続する。SCM point-onlyに未検証CIを付与しない。SDIDはunit/time weights、pre-period fit、donor eligibilityとadopted variance/inferenceを別検証。受入済みのEstimator Policyと独立REFがないMethodはBLOCKED。
- **Ownership:** G01共通Registry/Publisher/Reader、G07 Panel処理とScience Kernelの重複実装は禁止。Group/Unit/Timeのsupportが不足ならfallbackで推定成功にしない。

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
| `SyntheticControlAdapter` | `ariadne.scientific.causal_methods.quasi.SyntheticControlAdapter` | Method Adapter ownership | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` |
| `EffectOutcome` | `ariadne.causal.inference.contracts.EffectOutcome` | Port/Value/Facade integration (no duplicate implementation) | validate_consistency() / to_result_payload() |
| `InferenceEvidence` | `ariadne.causal.inference.contracts.InferenceEvidence` | Port/Value/Facade integration (no duplicate implementation) | validate_for(mode,method) |

**Method Adapter signature policy:** 新Adapterは原則`preflight(self,request:ValidatedMethodRequest)->EligibilityOutcome`／`execute(self,request:ValidatedMethodRequest,*,sink:StagingArtifactSink)->TypedScientificOutcome`。上表で指定された既存`run(self,input_,output_dir)`はその署名を保持。PortはApplication→Scientific kernelへ向かい、CLI Layerに別の科学数値実装を作らない。Class Field/Constructor/Public Methodは本Pxx§3.1以降の埋込契約が規範であり、DDは設計Provenanceに過ぎない。Solver/Inference APIなど未確定事項を補完しない。

**Responsibility:** Method Adapterを担当するClassは `SyntheticControlAdapter`。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。

### 3. Embedded executable Class/Method contracts

External DDはこのPackage契約のprovenanceのみ。以下のClass Field/Constructor/Signature/Process/FailureをこのPxxのNormative内容にする。実Source存在/ABIは開始時に確かめる。

### 3.1. `SyntheticControlAdapter` — self-contained class protocol

#### 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.quasi.SyntheticControlAdapter`。 EstimationのMethod実行Adapter。担当Method：`P3-M12`。**再利用:** 共通Panel/Time/Donor適格性とpoint-only inferenceを利用。入口がCLIであることを科学的な別実装の根拠にしない。

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
| `P3-M12` | treated-unit counterfactual gap | donor pretreatment fit/contamination、point-only |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本PackageのMethod/Science条件に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 検証

`DD-E11-METH-P312`（`P3-M12`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には本Packageに記載するMethod/DD/Scienceを優先し、この7区分の記載だけで科学的PASSとはしない。

### 3.2. `EffectOutcome` — self-contained class protocol

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

### 3.3. `InferenceEvidence` — self-contained class protocol

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

## 4. Required method execution — G09/P01

1. **Entry:** G09 Frozen06/07/Pxx、G01 upstream canonical 999、Owner Coding Authorization、Source/lock full SHA、Pxx Dependency checkpoint。Panel/Donor/Time/Estimand/Backend Profileをstrict preflight。
2. P3-M12 Synthetic Controlはintervention date、treated units、donor pool、pre/post time supportを固定し、donor介入汚染/欠測/不適格pre-periodを拒否。
3. Pre-treatment fit objective、donor weighting constraints、nonnegativity・sum-to-one等の採用PolicyとSolver/SeedをMethod configに明示し、Counterfactual Y0hat(t)、gap、post-period Targetを算出。
4. 初期はPOINT_ONLY。Placebo distributionを未検証CIと偽装せず、unsupported inferenceはtyped negative。Donorごとの重み/fit Evidenceが個票や秘密情報を含むなら許可されたaggregateだけ出力。
5. **Kernel and Port boundaries:** typed Request→Method capability→selected Scientific Adapter→shared numerical kernel→EffectOutcome/Diagnostic→G01 Publisher/Reader。Standalone CLI-specific solverやduplicate Registry禁止。
6. **Outcome and negative:** donor contamination/invalid time support/poor pre-fit/nonconvergence、unsupported CI、Backend unavailable、Scientific negative、technical errorを別扱い。Timestamp/seed/weights/profileのProofを保存。
7. **Protected behavior:** G05のPolicy承認なしに個票出力しない。Product v2とPassed-Gate Graph/Codec/Atomic/Privacyを保護する。

### 設計書の採用済み意味論（独立した本Package実装規範）

以下は30_62/30_63に明文化された数理・Port・互換性の契約をこのPxxへ取り込んだもの。Scopeは本Packageの§3/4に限り、他PackageのClassを再実装しない。

- SCM：donor poolの介入汚染を拒否し、pre-treatment fitとextrapolation、time-indexとweight optimization objectiveを保存する。初期は**point-only**であり未検証のplacebo intervalを付けない。

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P3-M12` | treated-unit counterfactual gap | donor pretreatment fit/contamination、point-only |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

**実際のBackend適格性・Config Schemaの未生成・独立OracleやCoverage証跡の不足は、上記Target/数理契約の未決とは区別する。** 実行後のScience判定を未検証のままPASSにしない。

## 5. Method-by-Method DGP/Negative/Reference Obligations

| Method | DD ID | Positive/Negative | Independent Reference | AC | 10_32 Readiness |
|---|---|---|---|---|---|
| `P3-M12` Synthetic Control／処置単位の時点別反実仮想ギャップ | `DD-E11-METH-P312` | DGP-017; NEG-024 | REF-Q04 | AC-D03, AC-P01, AC-P03, AC-Q04 | PLAN:G09 / OWNER_BASELINE_ACCEPTED_POINT_ONLY_SCIENCE_PENDING / NOT_GENERATED |

**Proof boundary:** §5のDGP/NEG/REF/ACを独立science obligationsとして扱う。SCM Point-onlyとSDIDの条件付きInferenceを別にし、Backend outputを自己Referenceとしない。Generator/OracleやFWER=.05/K/R/Coverage/MC-SEが未確定ならBLOCKED。外部DDを参照して推測しない。

## 6. Focused Verification Contract — WHAT, not physical filename

| Layer | Required behavior |
|---|---|
| unit | Value/Estimand/Method schema、negative、Hash/Status/No-False-PASS、pure Algorithm。 |
| contract | `Class.Method`入出力、Port/Backend Registry選択、typed evidence/Lineage、Version+Codec。 |
| integration | 必要な実Backend/CLI/FS/Atomic readback、optional Profile、既存Product v2回帰。 |
| scientific evidence | Method別DGP/NEG/independent reference、定量Simulation/coverage/MC-SE。 |

TestはLifecycle（enhancement/regression/characterization/benchmark/support/legacy）とLayer（unit/contract/integration/frontend/browser_e2e）を独立分類。新規は`tests/enhancement/enh_e11/g09/<layer>/`に原則配置、実Path/command/pytest collectionは40 Operatorがcurrent checkoutからdiscover。受入07をpathの文字列で置き換えない。Mock-onlyでreal Backend/FS/ScienceをPASSにしない。

### 6.1. Focused science and Port verification

- Method一覧§5のDGP/NEG/REF（P3-M12/M13に対応）を省略せず独立Referenceと照合し、Backend自己出力を正解に用いない。
- **Method-specific acceptance:** P3-M12 Synthetic Controlはintervention date、treated units、donor pool、pre/post time supportを固定し、donor介入汚染/欠測/不適格pre-periodを拒否。 Pre-treatment fit objective、donor weighting constraints、nonnegativity・sum-to-one等の採用PolicyとSolver/SeedをMethod configに明示し、Counterfactual Y0hat(t)、gap、post-period Targetを算出。 初期はPOINT_ONLY。Placebo distributionを未検証CIと偽装せず、unsupported inferenceはtyped negative。Donorごとの重み/fit Evidenceが個票や秘密情報を含むなら許可されたaggregateだけ出力。
- Unit=Design/Panel/Donor/Status/Result schema、Contract=Method/EstimatorPort/Manifest/Inference Policy、Integration=real solver/backend, CLI Publish/readback, protected v2 regression。実Policyと科学真値が不明ならBLOCKED。
- Actual source/lock/fixture SHA、seed、weights/preperiod diagnostics、point/CI availability、collected test path/commandとobserved vs expectedをEvidence化。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** P02,P03。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、当該PxxのOptional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。本Pxxの依存契約・科学的Referenceが未解決なら当該ScopeだけをBLOCKEDとする。他Gateの未決を全Packageの一律停止条件にせず、Agentによる推測補完を禁止する。


## 8. Self-contained Freeze stop

§3でField/Constructor/Public Method/I-Oを、§4で独自Algorithmと失敗時分岐を、§5〜6でDGP/NEG/REF/DDと証拠を本書内に規定する。**Open scientific/design item:** SCM optimizer constraints/objective, solver/seed, point-only evidence, independent REF-Q04. Method-specific API/quantitative science thresholdsが未決ならNo Coding Authorization。外部文書をNormative補完として要求しない。

## 9. OD-05 Owner-adopted Method Profile construction obligation

**Accepted authoring allocation (2026-11-19 JST):** G09/P01 is responsible for strict versioned Config/Question/Design/Output/Inference Profile authoring/registration for P3-M12. Scientific constraints: SCM donor selection/preperiod fit/point-only, SDID unit/time weights/panel inference. Retain existing §§3–6 Class/Method/algorithm/DGP/NEG/REF/AC semantics. Profiles declare conditional/mandatory fields, type domains, effective Backend/API/Version, analysis_mode/inference eligibility, output status/artifact shape, and no implicit backend defaults.

**Negative obligations:** unsupported method/profile/estimand, unknown fields, missing conditional fields, invalid Graph/Design/Question/DataRef identity, unavailable optional Backend, unsupported CI or invalid scientific assumptions are typed rejections; missing profile ⇒ `METHOD_PROFILE_UNAVAILABLE`. No silent fallback or `config={}` as a claim of support.

**Readiness:** Owner accepted work allocation only; this does not assert that individual schemas, independent DGP/REF, Backend execution, K/R/MC-SE/coverage, Gate07/999, Freeze or Coding Authorization are complete. For G08, exact HC1 AR numeric reference adoption history in PREP02-111 vs DD30_63 must be reconciled before Freeze without changing already adopted B0/B1/AR science bounds.


## PREP-04.1 embedded Method contract (NOT_FROZEN)

### P3-M12 (PREP-04.1 STRICT DRAFT / NOT_FROZEN)
- ESTIMATE target: 10_32 semantic target (not assigned canonical enum); Pxx owner=P01; SCM treated-unit gap and SDID panel-average effect are not interchangeable.
- Config required fields: weight_objective_spec_ref, preperiod_fit_spec_ref, donor_eligibility_spec_ref; types/const/ranges in method_config JSON Schema, no unknown keys/defaults; config={} fails.
- Question required: question_id/research_question/population/analysis_goal/estimand_family/contrast, matched against Study.
- Design required: design_id/question_id/design_kind; treated_unit, donor_units, time_index, preperiod_end, intervention_time, no_donor_contamination_ref; validate donor/treatment contamination, pre-period support, time ordering, upstream content hashes and panel eligibility.
- Positive output result.json/e11-local-effect-result/1; G01 hash/marker/manifest/Reader; privacy row output requires G05 approval. Negative case returns typed reason, not fake effect.
- Inference: SCM point-only; requested=false, confidence_level=null; no placebo interval.
- Independent DGP/NEG/REF DGP-017; NEG-024; REF-Q04 plus empty/unknown Config, wrong target/Time/Donor, pre-period leakage, missing upstream hash, backend unavailable, unsupported CI. Backend/License/independent oracle/K/R/FWER=.05/MC-SE/coverage not verified.


## S02簡素化・G09 Synthetic Counterfactual Profileの規範

担当Methodは`P3-M12` Synthetic Controlと`P3-M13` Synthetic DiD。5 Profile Kindは`23_api_interface_design/schema_drafts/method_profiles/factored/e11_<kind>_factored_v1.json`（method_config/question_profile/design_profile/output_profile/inference_profile）のshared core＋Method ID overlayを厳密に再構築する。Dispatch Registry/Blob SHA/200 Draft202012 positive/negative parityの証拠がないMethodは`METHOD_PROFILE_UNAVAILABLE`でfail-closed。P3-M12 SCMは**point-only**でCIを捏造しない。scalar Result.pointは`NOT_AVAILABLE`、内部`scm_gaps.json`に処置単位の時点別観測値・合成反実仮想・gap・Donor/Preperiod/Weightの独立ContentRefs/Hashを保持し、各時点`gap=observed-counterfactual`と時系列順序・donor contamination負例を検査する。P3-M13 SDIDは別のpanel平均ATTでありSCMと同一Estimand/推論を仮定しない。Method適格性・独立数値Oracle・実Backend/inferenceは未検証。

Context`LocalRunContext(root,principal)`と`LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)`を使用。Studyの`privacy.row_export_requested=true`とnonroot同一UID/private ext4/XFS/Method RowSchema/capsのAND判定による個票出力はG05のみ。本Gateでは個票の直接公開禁止。追加CLI flag、署名Verifier/Anchor、Study`policy_ref`を導入せず、Graph VersionはLocal content hash（Product Version IDs=null）で扱う。旧Product ABIとScientific Kernel共有/影響回帰/Source SHA固定、typed status／Manifest Readerの独立確認を維持し、未実行のScienceをPASSとしない。

## S09 documented SCM non-scalar gap contract — P3-M12 (2026-11-22)

The initial P3-M12 Synthetic Control scientific target is the **time-indexed treated-unit counterfactual gap**, not a scalar difference or confidence interval. For an eligible `ESTIMATE` run, `result.json` carries nested `point.availability=NOT_AVAILABLE`, `point.value=null`, `point.reason.code=NON_SCALAR_TARGET`, and `status.json` independently carries top-level `point_availability=NOT_AVAILABLE`; the Manifest must inventory `scm_gaps.json` with `schema_drafts/internal_scientific/e11_scm_gaps_draft1.schema.json` semantics: `method_id=P3-M12`, `study_ref`, treated-unit/preperiod/donor/weight-objective ContentRefs, typed `periods` spanning PRE and POST with finite `observed`, `counterfactual` and `gap=observed-counterfactual`, and `inference_status` point-only. The time key ordering and pre/post boundary, data source/Method/Study identity, donor contamination, optimization and exact Manifest/Marker/Reader hashes must be validated. Do not fabricate a scalar target, placebo CI or scalar SDID equivalence; P3-M13 SDID retains its own panel ATT/inference contract.

**P01:** Produce the scientifically typed SCM gap time vector plus donor/preperiod/objective evidence for the downstream P03 writer; do not present a treatment-period average as the only scientific target.
