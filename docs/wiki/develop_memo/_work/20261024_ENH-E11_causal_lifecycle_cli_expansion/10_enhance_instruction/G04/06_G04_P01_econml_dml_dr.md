# ENH-E11 G04 P01 — econml_dml_dr

**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G04 / **Package:** P01 / **Trial:** NOT_STARTED  
**Depends on Pxx:** NONE  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G04_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G04_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** EconML版/APIとX/W、crossfit/nuisance/propensity、Estimator別InferenceAvailableを検証。

**Scope:** 本PackageのClass/Methodと、それらが必要とする契約/適格性/Result Evidenceに限定。**Gate全体の保護意味:** 7種Non-IV CATEとDRIV IV異質効果を個別Estimand/Inferenceで提供する。

**科学/Designの必須制約:** Non-IV CATE、IV heterogeneous slope、B0 LATE、B1 linear slopeを同一視しない。G03依存はまとめReviewで検討。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** EconML版/APIとX/W、crossfit/nuisance/propensity、Estimator別InferenceAvailableを検証。

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
| `EconmlCateAdapter` | `ariadne.scientific.causal_methods.heterogeneity.EconmlCateAdapter` | Method Adapter ownership | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` |
| `EstimatorPort` | `ariadne.scientific.ports.causal.EstimatorPort` | Port/Value/Facade integration (no duplicate implementation) | estimate(self, request:ValidatedEstimatorRequest, *, sink:StagingArtifactSink) -> EffectOutcome |
| `InferenceEvidence` | `ariadne.causal.inference.contracts.InferenceEvidence` | Port/Value/Facade integration (no duplicate implementation) | validate_for(mode,method) |

**Class/Method authority:** 本Pxx §3.1以降のField/Constructor/公開Method/前後条件は本書が一次規範である。新規EconML/MetaLearner/DRIV Adapterは本Packageが担当する場合のみ実装し、実効Backend API/Inference availabilityをprobeする。既存v2の公開ABIを維持し、結果だけのPackageは独立数値Kernelを作らない。

**Responsibility:** Method Adapterを担当するClassは `EconmlCateAdapter`。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。

### 3. Embedded class-level implementation contracts

以下は本Pxxのnormative仕様。外部DDはprovenanceのみで、Agentに不足手順の補完を委譲しない。Designed Moduleの現物存在は未検証なので開始時にABI/Reuseを検査し、齟齬はBLOCKED。

### 3.1. `EconmlCateAdapter` — Constructor, fields, methods, invariants

#### 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.heterogeneity.EconmlCateAdapter`。 EstimationのMethod実行Adapter。担当Method：`P2-M01, P2-M02, P2-M03, P2-M04`。**再利用:** 既存CausalDesign・propensity/overlap検証を再利用しEconML固有APIを追加。入口がCLIであることを科学的な別実装の根拠にしない。

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
| `P2-M01` | LinearDML CATE | X/W/treatment/outcome、inference registry、fold |
| `P2-M02` | CausalForestDML CATE | leaf/support/nuisance/CI API、row privacy |
| `P2-M03` | DRLearner CATE | binary treatment/propensity、inference method |
| `P2-M04` | ForestDRLearner CATE | propensity+forest inference/support |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本Packageの科学的Target/推論/負例の節に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 検証

`DD-E11-METH-P201`（`P2-M01`）、`DD-E11-METH-P202`（`P2-M02`）、`DD-E11-METH-P203`（`P2-M03`）、`DD-E11-METH-P204`（`P2-M04`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には本Packageに記載したMethod別検証IDを優先し、この7区分の記載だけで科学的PASSとはしない。

### 3.2. `EstimatorPort` — Constructor, fields, methods, invariants

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

## 4. Required Method implementation / Class delegation (G04/P01)

1. **Preconditions:** 06/07/Pxx Freeze、G02/G03の要求されるlatest canonical 999、Owner Coding Authorization、fixed Source/lock、Pxx依存checkpointを検証。Method/Estimand/Inference/Backend/Graph/Design/Questionが不一致ならtyped reject。
2. `P2-M01` LinearDML: X=effect modifiers, W=confounders; Fold/nuisance outcome/treatment models、treatment type、Target CATE(x)を明示し、Estimatorのpoint/inference supportを別々に検証する。
3. `P2-M02` CausalForestDML: forest hyperparameters、leaf/support、nuisance/foldとCI APIを実効EconML Versionでprobe。pointwise CIと同時帯を混同しない。
4. `P2-M03` DRLearner / `P2-M04` ForestDRLearner: binary treatment support、propensity overlap/DR score、forest/Final model inferenceを構成別に検証し、Unsupported CIはResultに適切なReasonを付す。
5. EconMLライブラリをConstructor時にImportしない。Method registryでeffective distribution/API/extraを判定し、実行時に選択Methodだけlazy load。Model objectは外部へ返さない。
6. **Sequence:** ValidatedStudy→LocalCausalUseCase→typed EstimatorPort/Adapter preflight→approved Backend computation→pure typed CATE/EffectOutcome→G01 StagingSink/atomic Publisher/Reader。Application/DomainからCLI DB/FSのConcreteへ逆依存しない。
7. **Failure and privacy:** unsupported inference、effect support不足、missing optional Backendは別Reason。Numerical failureを科学的Negativeに偽装しない。G05以前個票書込無し、Model object/Secret出力無し、旧v2公開ABI不変。

### 設計書で定義済みの実装意味論（本Packageの規範）

以下は既存30_62/30_63の設計規則のうち本Packageへ適用する本文内契約である。外部DDを読ませて仕様を補完することは禁止する。自Packageが所有しないClassは再実装しない。

LinearDML/CausalForestDML/DRLearner/ForestDRLearner/S/T/X-Learnerを単にCATEという名称で同等に扱わない。X=effect modifiers、W=confounders、nuisance models、treatment type、target population、crossfitting/final model、backend/versionをper Method Configとする。

- Result Point CATE(x)、Population summary、support/overlap診断を分離し、個票値は明示的に認可されたParquetのみ。Stdoutや小さなJSONへの個票全件混入を禁止。
- Inference RegistryはMethod/Backend/version/final estimator config別に `POINT_ONLY / SUPPORTED_CI / UNSUPPORTED / UNAVAILABLE / FAILED` を判定。Native bootstrapを統計的妥当性確認なしに汎用適用しない。
- Exploratory point-onlyは許すが、Confirmatoryは事前に宣言したtargetに適合するCIと独立Science Evidenceが必要。Pointwise CIとsimultaneous bandを区別する。 

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P2-M01` | LinearDML CATE | X/W/treatment/outcome、inference registry、fold |
| `P2-M02` | CausalForestDML CATE | leaf/support/nuisance/CI API、row privacy |
| `P2-M03` | DRLearner CATE | binary treatment/propensity、inference method |
| `P2-M04` | ForestDRLearner CATE | propensity+forest inference/support |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

**推定Target/Point・Inference可用性の区別は決定済み。未生成の独立Referenceや実API probeをScience PASSには使わない。**

## 5. Method-by-Method DGP/Negative/Reference Obligations

| Method | DD ID | Positive/Negative | Independent Reference | AC | 10_32 Readiness |
|---|---|---|---|---|---|
| `P2-M01` LinearDML／CATE(x) | `DD-E11-METH-P201` | DGP-003; NEG-011, NEG-012, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P2-M02` CausalForestDML／CATE(x) | `DD-E11-METH-P202` | DGP-004; NEG-010, NEG-012, NEG-013 | REF-E05 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P2-M03` DRLearner／CATE(x) | `DD-E11-METH-P203` | DGP-003, DGP-004; NEG-011, NEG-012, NEG-013 | REF-E05, REF-E03 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P2-M04` ForestDRLearner／CATE(x) | `DD-E11-METH-P204` | DGP-004; NEG-010, NEG-011, NEG-013 | REF-E05, REF-E03 | AC-D01, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-I03 | PLAN:G04 / CONFIG_AND_AC_PENDING / NOT_GENERATED |

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
- **Verification-specific contract:** `P2-M01` LinearDML: X=effect modifiers, W=confounders; Fold/nuisance outcome/treatment models、treatment type、Target CATE(x)を明示し、Estimatorのpoint/inference supportを別々に検証する。 `P2-M02` CausalForestDML: forest hyperparameters、leaf/support、nuisance/foldとCI APIを実効EconML Versionでprobe。pointwise CIと同時帯を混同しない。 `P2-M03` DRLearner / `P2-M04` ForestDRLearner: binary treatment support、propensity overlap/DR score、forest/Final model inferenceを構成別に検証し、Unsupported CIはResultに適切なReasonを付す。 EconMLライブラリをConstructor時にImportしない。Method registryでeffective distribution/API/extraを判定し、実行時に選択Methodだけlazy load。Model objectは外部へ返さない。
- Unitはpure Method/schema/result、不適格値、ContractはClass/Port/Inference RegistryとLineage、Integrationは実Backend/CLI/Pub-Readback/legacy regressionを実行。独立数値ReferenceはBackend自身から生成しない。
- Evidenceはsource/lock/fixture SHA、expected/actual, effective Backend/API, seed/fold, support/overlap, CI policy, testcase collection/command。科学的Coverage/Pilotは未生成ならBLOCKEDでありPASSを推測しない。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** P02,P03,P04。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、当該PxxのOptional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。本Pxxの依存契約・科学的Referenceが未解決なら当該ScopeだけをBLOCKEDとする。他Gateの未決を全Packageの一律停止条件にせず、Agentによる推測補完を禁止する。


## 8. Freeze-critical independent contract audit

Constructor/Instance Fields/Public Methodの責務は§3、Method固有処理は§4、DGP/NEG/REF/Focused acceptanceは§5〜6に含み、外部Gate06/07/DDに実装指示を委譲しない。残未決: X/W roles、nuisance/Fold strategy、effective EconML APIとEstimator別CI methodが未固定ならBLOCKED。 Backend実効API/Science Pilot/Reference/Method Config未確定のまま実装しない。Ownerの一括レビューで調停する。

## 9. OD-05 Owner-adopted Method Profile construction obligation

**Accepted authoring allocation (2026-11-19 JST):** G04/P01 is responsible for strict versioned Config/Question/Design/Output/Inference Profile authoring/registration for P2-M01–M04. Scientific constraints: DML/DR/MetaLearner X/W roles/seed/folds/CI eligibility、DRIV theta_IV(x). Retain the existing §§3–6 Class/Method/algorithm/DGP/NEG/REF/AC semantics. A profile must declare mandatory and conditional fields, type domains, effective Backend/API/Version, analysis_mode/inference eligibility, output status/artifact shape, and no implicit Backend defaults.

**Negative obligations:** unsupported method/profile/estimand, unknown fields, missing conditional fields, invalid Graph/Design/Question/DataRef identity, unavailable optional Backend, unsupported CI or invalid scientific assumptions are typed rejections; missing specific profile ⇒ `METHOD_PROFILE_UNAVAILABLE`. No silent fallback or `config={}` as a claim of support.

**Readiness:** This Owner decision allocates work; it does not assert that schemas, independent DGP/REF, Backend execution, K/R/MC-SE/coverage, Gate07/999, contract Freeze or Coding Authorization are complete. No new mathematical Target is adopted here.


## PREP-04.1 embedded Method contracts (DRAFT)

### P2-M01 — strict Method contract (PREP-04.1 DRAFT / NOT_FROZEN)
- Method scope: ESTIMATE / CATE; Pxx=P01; preserve 10_32 scientific target, do not cast alternative estimands.
- Config mandatory fields: model_y_ref, model_t_ref, cv_folds, final_model_ref; versioned method_config Schema restricts type/const/range and extra keys, config={} is rejected, no backend defaults.
- Question mandatory: question_id/research_question/population/analysis_goal/estimand_family/contrast; Study target and references cross-validated.
- Design mandatory: design_id/question_id/design_kind plus treatment, outcome, effect_modifiers, controls, unconfoundedness_ref; validated data columns, roles, dataset support and assumption/Graph/temporal provenance. Declarations are not proof of causal truth. Exact types enforced by dedicated design_profile Schema.
- Positive output: result.json/e11-local-effect-result/1, point may be unavailable; individual row outputs only by G05 authority; status/marker/manifest and Reader hash/readback required; negative science typed and no fictitious positive.
- Inference: requested=false/null or true/numeric (0,1); real CI needs compatible versioned backend and independent coverage; unsupported→INFERENCE_UNAVAILABLE. CONFIRMATORY is not granted by schema syntax.
- Independent AC: DGP-003; NEG-011, NEG-012, NEG-013; REF-E05. Negative matrix includes empty/unknown/malformed config, wrong operation/target, missing/mismatched upstream hash, unsupported CI, unavailable backend and Method-specific NEG. Real backend and independent DGP/REF/K/R/MC-SE/FWER 0.05 remain NOT_VERIFIED.


### P2-M02 — strict Method contract (PREP-04.1 DRAFT / NOT_FROZEN)
- Method scope: ESTIMATE / CATE; Pxx=P01; preserve 10_32 scientific target, do not cast alternative estimands.
- Config mandatory fields: model_y_ref, model_t_ref, cv_folds, n_estimators, min_leaf_size; versioned method_config Schema restricts type/const/range and extra keys, config={} is rejected, no backend defaults.
- Question mandatory: question_id/research_question/population/analysis_goal/estimand_family/contrast; Study target and references cross-validated.
- Design mandatory: design_id/question_id/design_kind plus treatment, outcome, effect_modifiers, controls, unconfoundedness_ref; validated data columns, roles, dataset support and assumption/Graph/temporal provenance. Declarations are not proof of causal truth. Exact types enforced by dedicated design_profile Schema.
- Positive output: result.json/e11-local-effect-result/1, point may be unavailable; individual row outputs only by G05 authority; status/marker/manifest and Reader hash/readback required; negative science typed and no fictitious positive.
- Inference: requested=false/null or true/numeric (0,1); real CI needs compatible versioned backend and independent coverage; unsupported→INFERENCE_UNAVAILABLE. CONFIRMATORY is not granted by schema syntax.
- Independent AC: DGP-004; NEG-010, NEG-012, NEG-013; REF-E05. Negative matrix includes empty/unknown/malformed config, wrong operation/target, missing/mismatched upstream hash, unsupported CI, unavailable backend and Method-specific NEG. Real backend and independent DGP/REF/K/R/MC-SE/FWER 0.05 remain NOT_VERIFIED.


### P2-M03 — strict Method contract (PREP-04.1 DRAFT / NOT_FROZEN)
- Method scope: ESTIMATE / CATE; Pxx=P01; preserve 10_32 scientific target, do not cast alternative estimands.
- Config mandatory fields: outcome_model_ref, propensity_model_ref, cv_folds; versioned method_config Schema restricts type/const/range and extra keys, config={} is rejected, no backend defaults.
- Question mandatory: question_id/research_question/population/analysis_goal/estimand_family/contrast; Study target and references cross-validated.
- Design mandatory: design_id/question_id/design_kind plus treatment, outcome, effect_modifiers, controls, unconfoundedness_ref; validated data columns, roles, dataset support and assumption/Graph/temporal provenance. Declarations are not proof of causal truth. Exact types enforced by dedicated design_profile Schema.
- Positive output: result.json/e11-local-effect-result/1, point may be unavailable; individual row outputs only by G05 authority; status/marker/manifest and Reader hash/readback required; negative science typed and no fictitious positive.
- Inference: requested=false/null or true/numeric (0,1); real CI needs compatible versioned backend and independent coverage; unsupported→INFERENCE_UNAVAILABLE. CONFIRMATORY is not granted by schema syntax.
- Independent AC: DGP-003, DGP-004; NEG-011, NEG-012, NEG-013; REF-E05, REF-E03. Negative matrix includes empty/unknown/malformed config, wrong operation/target, missing/mismatched upstream hash, unsupported CI, unavailable backend and Method-specific NEG. Real backend and independent DGP/REF/K/R/MC-SE/FWER 0.05 remain NOT_VERIFIED.


### P2-M04 — strict Method contract (PREP-04.1 DRAFT / NOT_FROZEN)
- Method scope: ESTIMATE / CATE; Pxx=P01; preserve 10_32 scientific target, do not cast alternative estimands.
- Config mandatory fields: outcome_model_ref, propensity_model_ref, cv_folds, n_estimators, min_leaf_size; versioned method_config Schema restricts type/const/range and extra keys, config={} is rejected, no backend defaults.
- Question mandatory: question_id/research_question/population/analysis_goal/estimand_family/contrast; Study target and references cross-validated.
- Design mandatory: design_id/question_id/design_kind plus treatment, outcome, effect_modifiers, controls, unconfoundedness_ref; validated data columns, roles, dataset support and assumption/Graph/temporal provenance. Declarations are not proof of causal truth. Exact types enforced by dedicated design_profile Schema.
- Positive output: result.json/e11-local-effect-result/1, point may be unavailable; individual row outputs only by G05 authority; status/marker/manifest and Reader hash/readback required; negative science typed and no fictitious positive.
- Inference: requested=false/null or true/numeric (0,1); real CI needs compatible versioned backend and independent coverage; unsupported→INFERENCE_UNAVAILABLE. CONFIRMATORY is not granted by schema syntax.
- Independent AC: DGP-004; NEG-010, NEG-011, NEG-013; REF-E05, REF-E03. Negative matrix includes empty/unknown/malformed config, wrong operation/target, missing/mismatched upstream hash, unsupported CI, unavailable backend and Method-specific NEG. Real backend and independent DGP/REF/K/R/MC-SE/FWER 0.05 remain NOT_VERIFIED.
