# 30_63_e11_method_adapters — E11全41 Method物理実装契約

## 1. Registryと実装責務

Method IDの正本は[10_32_scientific_method_scope.md](../10_requirements_definition/10_32_scientific_method_scope.md)。本書は全41 IDの**実装責務／Adapter Class／適格性・推論・結果型／受入テスト**を対応付ける。Methodの科学的限定は10_32のScope定義と整合させる。

Method Descriptorは `method_id, operation, estimand_family, design_kind, backend_id, extra, config_schema, eligibility_predicate, inference_registry_entry, result_schema, negative_reason_codes, reference_ids` を保持する。1 Methodで異なる構成がある場合はVersion付きvariantにより区別し、対象EstimandをMethod表示名だけで推測しない。

各Adapterは `class.method(request: ValidatedRequest, *, sink: StagingArtifactSink) -> TypedScientificOutcome` を契約とする。ConstructorはResourceの参照とBackend factoryのみを持ち、外部Estimatorの具体Objectは永続化しない。Runtimeのeffective Method/API/seed/fold/CI configを出力する。Backendの自動fallback禁止。

## 2. 全41件のAdapter allocation

| Method ID | Adapter / Estimand型 | 必須preflight／Result・Inference |
| --- | --- | --- |
| P1-M01 | `NativeIdentificationAdapter` / randomized identification | 割当機構・target、proofの型付き正規化 |
| P1-M02 | `NativeIdentificationAdapter` / backdoor ATE | adjustment/backdoor、Graph・Design適格性 |
| P1-M03 | `DoWhyIdentificationAdapter` / backdoor ATE | effective API、method-specific proof、Graph対応 |
| P1-M04 | `DoWhyIdentificationAdapter` / frontdoor ATE | 単一Mediator／識別仮定、数値FD-Aとは別 |
| P1-M05 | `DoWhyIdentificationAdapter` / IV identifying target | DoWhy内部ラベルをLATEと同一視せず対象未確定をBLOCK |
| P1-M06 | `FciDiscoveryAdapter` / PAG | circle/bidirected/latent・oracle、point estimation不可 |
| P1-M07 | `FrontdoorLinearAdapter` / restricted FD-A ATE | 線形Mediator/Outcomeモデルとno direct path仮定、別Reference・CI |
| P1-M08 | `NativeEffectAdapter` / randomized diff-in-means ATE | randomization、variance、seedとpopulation |
| P1-M09 | `NativeEffectAdapter` / OLS adopted ATE/ATT | linear model/contrast、robust varianceの採否 |
| P1-M10 | `WeightingEffectAdapter` / IPW ATE/ATT | propensity/overlap/balance/ESS/weights/CI |
| P1-M11 | `WeightingEffectAdapter` / AIPW ATE/ATT | nuisance/DR claimの条件、crossfit/variance |
| P1-M12 | `RefutationAdapter` / placebo treatment | 事前指定置換ルール、null診断、再現seed |
| P1-M13 | `RefutationAdapter` / data subset | Subset規則、sample/support、差分の解釈 |
| P1-M14 | `RefutationAdapter` / random common cause | 摂動DGP/seed、条件付き安定性 |
| P1-M15 | `RefutationAdapter` / bootstrap refutation | resampling unit/CI可用性、同一DGP |
| P1-M16 | `SensitivityAdapter` / adjustment set | Graph/Design/追加変数・post treatment適格性 |
| P1-M17 | `SensitivityAdapter` / propensity clipping | trim threshold、estimand変化、ESS/sample loss |
| P1-M18 | `ObservedNceAdapter` / negative control exposure | 実在Z・事前帰無・opt-in、条件付き関連/負結果 |
| P1-M19 | `ObservedNcoAdapter` / negative control outcome | 実在W・事前帰無・opt-in、条件付き関連/負結果 |
| P1-M20 | `OlsRvAdapter` / OLS partial R²、point RV(q=1) | 古典OLS係数/SE/df、非OLS拒否 |
| P2-M01 | `EconmlCateAdapter` / LinearDML CATE | X/W/treatment/outcome、inference registry、fold |
| P2-M02 | `EconmlCateAdapter` / CausalForestDML CATE | leaf/support/nuisance/CI API、row privacy |
| P2-M03 | `EconmlCateAdapter` / DRLearner CATE | binary treatment/propensity、inference method |
| P2-M04 | `EconmlCateAdapter` / ForestDRLearner CATE | propensity+forest inference/support |
| P2-M05 | `MetaLearnerAdapter` / S-Learner CATE | counterfactual prediction、point/CI制限 |
| P2-M06 | `MetaLearnerAdapter` / T-Learner CATE | treated/control support、point/CI制限 |
| P2-M07 | `MetaLearnerAdapter` / X-Learner CATE | cross-model weights、point/CI制限 |
| P2-M08 | `EconmlDrivAdapter` / IV heterogeneous structural slope | Z/A/X/W、IV relevance/exclusion、inference |
| P3-M01 | `TigramiteTemporalAdapter` / PCMCI | CI test/lag window、time-series order、graph |
| P3-M02 | `TigramiteTemporalAdapter` / PCMCI+ | contemporaneous endpoint、CPDAG-like oracle |
| P3-M03 | `TigramiteTemporalAdapter` / LPCMCI | PAG/latent/endpoint fidelity、lag |
| P3-M04 | `PanelQuasiAdapter` / DiD ATT | 2x2 vs staggered、parallel trends、SE/cluster |
| P3-M05 | `PanelQuasiAdapter` / Event Study | cohort/event time、pretrend、reference periods |
| P3-M06 | `InterruptedTsAdapter` / level/slope change | intervention date、seasonality/autocorrelation/HAC |
| P3-M07 | `RddAdapter` / Sharp RD local effect | bandwidth、kernel/order、density manipulation、CI |
| P3-M08 | `RddAdapter` / Fuzzy RD local complier effect | First stage、discontinuity ratio、local IV inference |
| P3-M09 | `WaldRatioAdapter` / B0 complier LATE reference | binary Z/A、IV assumptions、first stage |
| P3-M10 | `TwoSlsAdapter` / B0 just-identified LATE | zero controls、single Z/A、robust covariance、AR |
| P3-M11 | `TwoSlsAdapter` / B1 additive linear IV slope | single binary Z/A、predeclared C、robust AR |
| P3-M12 | `SyntheticControlAdapter` / treated-unit counterfactual gap | donor pretreatment fit/contamination、point-only |
| P3-M13 | `SyntheticDidAdapter` / panel average effect | donor and time weights、preperiod/variance method |

**41 Method：** P1=20、P2=8、P3=13。ここでの`P1/P2/P3`はMethod catalogのPhase接頭辞であり、Enhance Workflowの`P01〜Pxx` Work Package IDとは異なる。P1-M05の対象EstimandをMethod labelからLATEと推定せず、識別対象未確定は型付きBLOCKとする。MethodConfig・BackendVersion・Inference可用性・科学ReferenceをMethodに結び付ける。

## 3. 共通Adapter Contract

### 3.1. Module-level関数とResult処理

`scientific.local_adapters.*`：
- `check_design(request) -> EligibilityOutcome`：Method固有のRequired Columns、missing、Temporal/Panel units、instrument support、positivity等のReasonを収集。
- `run(request, *, sink: StagingArtifactSink) -> TypedScientificOutcome`：数値計算。返却するのはportable Result DTO、external library instanceは禁止。日時・randomnessは注入されたContextのみから取得。
- `describe_effective_backend() -> BackendEvidence`：実効Library/distribution、Python API、solver/nuisance/fold/CI config/seedを返す。
- `serialize(result) -> ArtifactBundle`：Graph/Result/Diagnosticsを型付きSchemaに純粋変換する。File I/Oはしない。保存はAdapterが渡された`StagingArtifactSink`を通じて行い、Finite/not-finiteを判定しnull+reasonを記録する。

### 3.2. Failure semantics

- 入力契約違反＝`CONFIG_INVALID / METHOD_INCOMPATIBLE`、Backend unavailable＝`CAPABILITY_UNAVAILABLE`。これらは他手法へのfallback要因にしない。
- 仮定未成立、positivity不足、弱IV、非識別、CI unavailable、negative-control nullは**科学的Status/Reason**。当該Methodに適格なPointやCIがないことを明示。
- Backendの数値例外、収束エラー、非有限推定を成功へ書き換えない。
- Confirmatory ResultはMethod別の妥当な推論がなければScience PASSとしない。

## 4. P1 推定器・Refutation/Negative Control

### 4.1. Estimation formulasと診断

- Diff-in-means：`mean(Y|A=1)-mean(Y|A=0)`。randomized designと割当/分散推論条件を先に検査。
- OLS：OutcomeモデルのTarget Contrastを明示し、係数とATE/ATTの対応はDesign・Model仮定で限定。robust HC variantの採用は事前固定。
- IPW：propensity `e(X)`、ATEの重み例 `A/e(X)+(1-A)/(1-e(X))`、ATTには別の標本対象・weight normalization。clip/trimでtargetが変化し得ることをResultへ記録。balance/ESSとoverlap必須。
- AIPW：outcome nuisance `m_a(X)` とpropensityのAugmented scoreを別統計量として実装。double robustnessは必要な推定仮定／十分な推定品質の代わりでない。nuisance/fold/seedと推論方針を記録。
- FD-A：Frontdoor識別（A→M→Y、適格なバックドア条件等）と線形二段階数値推定を分離。MediatorとOutcomeの条件付き回帰仕様・直接効果項や交互作用の扱いを固定し、`a_to_m * m_to_y`型の制限付き係数積が有効なDGPでのみ利用。一般Frontdoor識別をすべてこの算式へ還元しない。DGP-005/REF-E04と照合して正式化する。

### 4.2. Refutation / negative controls / sensitivity

- Placebo/Data subset/Random Common Cause/Bootstrapは同一base Effectのhash、変更条件・seed・resampling unitを固定。Refutationの統計的検定と因果識別自体を同一視しない。
- NCE/NCOは観測実在のZ/W、事前指定負の対照関係・条件付き帰無、同じDesign covariatesとデータ適格性を要求し、p値が大きいことを無交絡証明と報告しない。
- OLS RVは古典OLSのcoefficient/SE/dfを再現し、指定の `q=1` partial R² / robustness valueのみ対象。他Estimatorへ自動拡張しない。

### 4.3. Tests

`DD-E11-METH-P101`〜`P120`：各Method IDに対応する必須positive、unsupported config、negative（DGP/NEG/REF/ACは10_32に従う）。特にFR-188、FR-189/190/191/192、AR-030/031/032/033/044。

### 4.4. P1-M06 `FciDiscoveryAdapter`のMethod固有契約

`FciDiscoveryAdapter.preflight(request:ValidatedDiscoveryRequest) -> CapabilityOrEligibilityResult`は静的な適格性判定、`execute(request:ValidatedDiscoveryRequest, *, sink:StagingArtifactSink) -> DiscoveryGraphOutcome`はFCI結果のPAGへの正規化である。Product `ScientificCorePort.run_discovery`やPC Adapterへのaliasを禁止。

[FCI Method config schema](../23_api_interface_design/schema_drafts/e11_g01_fci_method_config_v1.schema.json)に従い`fisherz/chisq/gsq`、明示alpha/depth/max_path_length、null/required/forbidden directed BackgroundKnowledgeを検証する。DatasetとDesignの列名・順序、finite complete observations、CI別measurement scale、categorical support、観測独立性・標本規模、BK矛盾を確認し、未承認の欠損補完・離散化・CI代替をしない。特定の`causal-learn`版を科学的Method定義に固定せず、effective distribution/API/signature/endpoint accessorとlockをRuntimeで照合し、不一致は`BACKEND_API_MISMATCH`。

Backend nodeとDataset列を1:1で対応させ、node1/node2に対応するendpoint markの順序を保持する。PAG circle/bidirectedをDAGへ確定せず、重複・不正node/markを拒否し、GraphVersion/dual hashをDomainへ渡す。BKがPAGの不確定endpointを過剰確定する場合は独立motif検証なしに成功としない。2観測変数の潜在交絡を一意識別したとは報告しない。

`DD-E11-METH-P106`は実効API/eligibility、独立MAG/PAG同値類Oracle、BK/latent negativeの検証契約。Backendの出力を自らの正解Oracleにしない。

## 5. P2 CATE / DRIV

### 5.1. Non-IV 7 Method

LinearDML/CausalForestDML/DRLearner/ForestDRLearner/S/T/X-Learnerを単にCATEという名称で同等に扱わない。X=effect modifiers、W=confounders、nuisance models、treatment type、target population、crossfitting/final model、backend/versionをper Method Configとする。

- Result Point CATE(x)、Population summary、support/overlap診断を分離し、個票値は明示的に認可されたParquetのみ。Stdoutや小さなJSONへの個票全件混入を禁止。
- Inference RegistryはMethod/Backend/version/final estimator config別に `POINT_ONLY / SUPPORTED_CI / UNSUPPORTED / UNAVAILABLE / FAILED` を判定。Native bootstrapを統計的妥当性確認なしに汎用適用しない。
- Exploratory point-onlyは許すが、Confirmatoryは事前に宣言したtargetに適合するCIと独立Science Evidenceが必要。Pointwise CIとsimultaneous bandを区別する。

### 5.2. DRIV-A

Instrument Z、Treatment A、Effect modifier X、Control W、識別仮定とheterogeneous structural target `theta_IV(x)`を持つ。Non-IV `CATE(x)`、B0 complier LATE、B1 linear IV slopeと区別。weak IV・invalid IV・poor overlapをtyped negativeにし、一般化の範囲を限定する。

### 5.3. Tests

`DD-E11-METH-P201`〜`P208`：Method別inference availability、effective API、DGP-003/004/008、negative control/misspecification、privacy、CI pointwise coverage、Reference E05/E06。対応FR-193/194/195、AR-034/035。

## 6. P3 Graph / Temporal

### 6.1. Graph semantics

- FCIはPAG circle、bidirected、ambiguous orientationを保持し、そこからDAGを想像してpoint estimateへ通さない。
- PCMCI/PCMCI+/LPCMCIはCI test family、max lag、contemporaneous link、endpoint mark、時間方向規約をserializeする。MetaDataの `lag=-1` 等は明示Convention無しには意味を持たせない。
- GraphOracleは構造上の同値類／可識別方向／adjacency・endpointを比較し、学習したGraphの不確定な向きを真DAGへ罰則無しに変換しない。

### 6.2. Tests

`DD-E11-METH-P301`〜`P303`：DGP-009〜011、Graph Oracle、NEG-021/028、round-trip、sample ordering。対応FR-186/196、AR-028/036。

## 7. P3 Quasi / IV / SCM

### 7.1. DiD / Event / ITS

- DiD：2×2 ATTとstaggered adoptionを別Configuration/Estimandとし、staggeredに単純TWFE係数を普遍的ATTとして流用しない。parallel trendsとcohort support、cluster covarianceのunitを保存。
- Event Study：事前指定reference periodとevent-time vector、cohort composition、lead/pretrend診断を保持。post-intervention windowによる選択が推論に与える影響を記録。
- ITS：level/slope change、intervention date、seasonality/trend、serial covariance（HAC等）を方法別Configに固定。独立残差OLSのSEを無検証で採用しない。

### 7.2. Sharp/Fuzzy RD

- Sharp RD：cutoff周辺のlocal regression、bandwidth、polynomial order、kernel、density manipulation、covariate continuityの診断を出力。
- Fuzzy RD：cutoff近傍のTreatment first-stage jumpとOutcome jumpの比による局所IV効果。weak first stageやinstrument validityに注意。単なるSharp RDにlabelを変えるだけで代用しない。
- `rdrobust` 等の外部BackendはPython APIの実効版とrobust bias correction inferenceの利用可否を確認。GPLの顧客配布Legal approvalとは別。

### 7.3. Wald/B0/B1/AR

- B0（P3-M09/M10）：単一二値Z/A、無調整、単一内生Aのcomplier LATE。Wald ratioは縮約形Outcome差/First-stage Treatment差。分母0/弱い場合にfinite CIを強制しない。
- B1（P3-M11）：単一二値Z/A、事前指定C、additive linear IV構造の2SLS slope。一般ATE/ATTやB0と同一complier LATEと呼ばない。
- B0/B1の2SLSはfirst-stage/2nd-stage、heteroskedasticity-robust covariance、Instrument support/first-stage diagnosticsを保存。通常Wald区間はweak-IV robustでないことを明示。
- Anderson–Rubin：H0(β)の下で`Y - β A`のZとの関係を（B1では指定Cを条件付けて）検定、反転集合を作る。初期契約は独立観測・単一excluded Z・単一endogenous A・異分散頑健漸近推論の範囲。任意のcluster/HAC版へ自動拡張しない。β探索は有界gridだけではALL_REAL/非有界/非連結を判定できないためtail/bracketing/数値精度を検証。数学的にEMPTYなAR集合は汎用Codecで表現可能。ただし、非退化なB0/B1 just-identified HC1 AR反転では gA≠0、Var_HC1(βhat)>0 の条件からT_AR(βhat)=0で非空性が従う。そこでEMPTYが観測された場合はMethod別SCIENCE_INCONSISTENTとして検査する。first-stage=0、非正分散、rank欠損は別途型付き分岐にし、数値的な失敗と数学的EMPTYを混同しない。
- AR testがIVのexclusion/independence/monotonicityを証明すると解釈しない。CI coverageは独立Simulationで計測する。

**AR具体化（共通Source設計拘束）：** `Q=[1]`（B0）または`Q=[1,C]`（B1）をFull Rankで保持し、各βについて`Y−βA ~ Q+Z`のZ係数=0を**HC1・χ²(1)漸近検定**する方式を対象実装方式とする。残差化・quadratic inversionは全実数で行い、有限gridから非有界・空集合を断定しない。公式の数値/科学受入では独立reference・有効な分散・条件付きIV仮定を評価する。統計量、二次式、退化条件、Negative Matrixは本節のAR定義に従い、Method固有の独立Referenceと照合する。これはB0/B1の科学的な統計量・推論前提を規定するものであり、独立ReferenceとCoverage実測とは別である。

### 7.4. SCM / SDID

- SCM：donor poolの介入汚染を拒否し、pre-treatment fitとextrapolation、time-indexとweight optimization objectiveを保存する。初期は**point-only**であり未検証のplacebo intervalを付けない。
- Synthetic DiD：unit/time weights、pre/post period、面積とsupport、Method-specific standard errorを区別。SCMと同一Estimatorにはしない。

### 7.5. Tests

`DD-E11-METH-P304`〜`P313`：DGP-012〜018/024、REF-Q01〜Q05/REF-E07/E08、weak-IV negative、Graph/temporal control、CI/AR shape、donor/pretrend/first stage。対応FR-197〜200、AR-037〜041。Method別実効Backend/InferenceとReferenceは独立検証の対象となる。

## 8. Verification strategy and science boundaries

- `DD-E11-METH-P101〜P120 / P201〜P208 / P301〜P313`は41 Methodに対応する恒久的な受入義務ID。各Methodについてpositive DGP/独立Reference、negative Scenario、Method×Estimand/Backend/CI、canonical Result/Manifest readback、Product regression影響を検証する。
- 独立検証ではDGP version・seed・Method-specific推論・Monte Carlo SE/Coverage/多重性と適格Run分母を定義する。型・Schema一致は科学的Coverageや識別の証明ではない。
- 顧客Deliveryは実際のBundleのSBOM/Licenseと受領者別法務判定を別途必要とする。

参照：[E11 Domain/Ports](30_61_e11_local_domain_ports.md)、[Execution/Publisher](30_62_e11_local_execution_publication.md)、[CLI Port IF](../23_api_interface_design/23_41_e11_local_cli_scientific_ports.md)、[Method Scope](../10_requirements_definition/10_32_scientific_method_scope.md)。
