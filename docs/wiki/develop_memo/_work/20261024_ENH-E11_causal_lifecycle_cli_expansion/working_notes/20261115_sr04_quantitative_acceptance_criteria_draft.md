# ENH-E11 — SR-04 Quantitative Acceptance Criteria（策定Draft）

**文書区分:** working_notes／科学的定量Acceptance案。正式なScope・FR/NFR/AR・Architecture Decision・Gate06/07・Work Package・Coding許可ではない。  
**策定日:** 2026-11-15 JST。  
**対象branch:** prototype/ariadne_mvp。**本文の全数値は提案値**であり、Human ownerによるMethod/推論/計算予算の正式採用を意味しない。  
**状態:** QUANTITATIVE_AC_DRAFT / METHOD_COVERAGE_41_OF_41 / NEGATIVE_COVERAGE_28_OF_28 / CROSS_CONTRACT_9_OF_9 / METHOD_CONFIG_PENDING / SCIENCE_NOT_RUN / PENDING_FULL_CONCEPT_APPROVAL。  
**直接の先行資料:** [Method Acceptance Matrix](20261115_sr04_method_acceptance_matrix_draft.md)、[Scientific Fixture Catalog](20261115_sr04_scientific_fixture_catalog_draft.md)、[Reference Specification](20261115_sr04_reference_specification_draft.md)、[Owner判断記録02](../00_enhance_background/02_enhancement_concept_approval_record.md)、[D03 AR/G2](20261101_sr03_d03_remaining_2sls_weak_iv_review.md)、[D05 CATE/DRIV](20261115_sr03_d05_cate_driv_inference_scientific_contract_decision.md)、[D06 Graph uncertainty](20261115_sr03_d06_graph_uncertainty_identification_override_decision.md)。  
**Coverage計画:** Phase1 20件、Phase2 8件、Phase3 13件、横断9件。68 Scope行全体の承認・Traceability完了と同義ではない。

> **2026-11-16 Owner判断の反映:** [2026-11-16 DEC-SR04-01/02 正式個別判断](20261116_sr04_dec01_b1_dec02_driv_owner_decisions.md) により **B1-A**（加法線形IV構造係数）と **DRIV-A**（条件付き構造IV斜率、残差化条件付きモーメント）を**科学的semantic targetとして個別採用**した。本書中の「B1/DRIV formal estimand未決」は**当初Draft時点の記録**であり、現在の未決事項は**正式schema/enum、実効Backend/nuisance/final model、AR/CI、独立Reference実装、定量ACとScience/Gateの検証**である。全体構想は`PENDING_FULL_CONCEPT_APPROVAL`のまま。

> **2026-11-16 DEC-SR04-03／04 個別判断:** [DEC-SR04-03 FD-A](20261116_sr04_dec03_frontdoor_fd_a_owner_decision.md)、[DEC-SR04-04 GRAPH-A](20261116_sr04_dec04_graph_oracle_graph_a_owner_decision.md)の2件をOwnerが採用済み。P1-M07のFD-AとP1-M06/P3-M01〜03のGRAPH-AはOwnerのMethod/Oracle設計方針が確定。しかしAC-I01/02、AC-G03/04等の数値閾値は未承認・未実測。DGP/Independent REF/n/T/R/K/推論/CI testをfreezeするまではScience PASS禁止。 正式FR/NFR/AR・Architecture・Gate07・Coding・全体構想は未承認（`PENDING_FULL_CONCEPT_APPROVAL`）。この判断より前に記録された「Frontdoor初期Methodの未決」「Graph Oracle採用方針未決」は**Owner方針のみ**解消し、実装・独立Science Oracleの未完成は維持。

> **2026-11-16 DEC-SR04-05-1〜7をOwnerが採用済み:** [準実験7手法の独立技術判断](20261116_sr04_dec05_quasi_experimental_seven_methods_estimator_inference_decisions.md)。DEC-05-1〜7のEstimator/Inference方法論方針はOwner採用済み。しかしMethod×DGP×n/T/bandwidth/cluster/R/K/CI modeを正式freezeするまでAC-Q01〜Q05とAC-I01/02の数値合格を宣言しない。**SCMは初期point-only**で通常CIの未提供をHard Gate違反としない。 本書の旧「Quasi estimator/inference未決」は**採用するMethod baselineの方針だけ**後続判断で解消した。実効Backendと独立Science Benchmark/正式FR/ADR/Gateは依然OPEN、全体構想は`PENDING_FULL_CONCEPT_APPROVAL`。

> **2026-11-16 DEC-SR04-06採用済み（OWNER_ACCEPTED）:** [Negative Control／OLS partial R²・RVの採否案](20261116_sr04_dec06_negative_control_ols_rv_scope_decision_proposal.md)。AC-T01/T02/T03/R03（NCE/NCO）・AC-D03/R04（partial R²）のMethod採否判断案を策定した。R/K/size/power/RV数字Referenceと閾値は未freeze。 **DEC06-1〜5すべてのA案をHuman ownerが個別採用済み**。3 Methodの個別採否・X-04/05のD扱いは決定済み。ただし科学Benchmark／Gate07・正式FR/ADRおよび全体構想は未承認。

> **2026-11-16 DEC-SR04-07事前監査（Owner採否待ち）:** [定量Acceptance／Monte Carlo／Compute budget技術判断案](20261116_sr04_dec07_quant_mc_compute_budget_owner_decision_proposal.md)を作成。R6000はMCSE 0.002813657の出発候補に過ぎない。Gate-wide K=1024の説明例で真のfailure=.005・R6000のWilson上限は約.01000657、failure Hard Gate（<=.01）を満たさない。RとK、Pass確率・実効CPU費用を同時審査。 **DEC07-1〜7推奨AはOwner未採用**で、既存AC数値・R・K・Pilot・Compute budget／Gateは未freeze。

## 0. 目的、判断階層、禁止事項

### 0.1. 何を定量的に受け入れるか

SR-04-A/B/Cで定義したMethod/Fixture/独立Referenceについて、(i) 数式・型の決定論的適合、(ii) 既知真値に対する点推定誤差、(iii) 統計推論の被覆率と帰無サイズ、(iv) Graph復元、(v) Refutation/Sensitivityの診断能力、(vi) 非適格入力に対する拒否、を分離してGate07候補の数値契約とする。

**4層の判定:**

1. **科学対象の前提審査:** Estimand/Graph oracle/識別仮定/Method-specific inferenceが未確定なら当該科学評価セルはBLOCKED。未決の数値基準だけで識別対象を正当化しない。
2. **Contract（deterministic）:** schema/target/lineage/Graph/集合/拒否は原則全ケース100%一致。統計的許容幅で仕様逸脱を救済しない。
3. **Scientific（stochastic）:** 独立repetitionからBias・RMSE・coverage・size/power・Graph metricsを計算。Monte Carlo不確実性、非収束、推論不可を報告する。
4. **Gateの承認:** 定量ACの事前freeze・実測・独立review・根拠付きOwner採用が揃うまでScience PASSではない。

**最重要の禁止:** 真値不明のexclusion/monotonicity/parallel trends等の違反がデータから常に検出できることを合格条件にしない。Invalid DGPで科学的破綻を観察する試験と、宣言Graph/typed input上で明らかな不適格を拒否する試験を分ける。

### 0.2. 値の承認状態

| 区分 | 意味 | 本Draftの扱い |
|---|---|---|
| CANDIDATE_NUMERIC | 理論式・独立真値・数値工学から事前提案できる閾値 | 以下の数値案を提示。実装/合格認定にはOwner/Gate freezeが必要 |
| CONDITIONAL_NUMERIC | DGP誤差分散、実効Method/Inference、Reference確認後に限り有効な閾値 | 数値例を出すが未解決条件下ではBLOCKED |
| REQUIRES_CALIBRATION | 科学的Method特性・DGP難度・計算予算に依存し、単一数値では無効 | 数式、候補水準、pilot→事前freezeの意思決定を記載 |
| CONTRACT_EXACT | 正しく定義された離散契約の一致が必要 | 0件の違反、100%一致を提案 |
| NOT_APPLICABLE | そのMethodにはそもそも意味のない統計指標 | 無理にCI/Type-Iなどを割当てない |

**未承認の対象:** NCE/NCO/OLS partial R² Method採否、B1/DRIVの正式schema enumとMethod-specific実効Estimator/CI（semantic targetは2026-11-16採用済み）、Frontdoor具体stage、Graph PAG oracle、準実験の具体estimator/inference。これらには数値候補を置いてもSCIENCE_READYを付与しない。

## 1. 定量ACポリシー — 原則と提案閾値

### 1.1. AC-D：決定論的・契約一致（F0/F1/F3/F4）

| AC ID | 適用対象 | 提案受入基準 | 科学的根拠・例外 |
|---|---|---|---|
| AC-D01 | ID/Estimand/Graph status/enum/理由/Version/lineage | **不一致0件／全固定case100%一致** | 正誤が定義可能なtyped contract。未知の仮定違反の自動検出とは別 |
| AC-D02 | 有効な調整集合、識別式、DAG/CPDAG/PAG/Temporal endpoint | **定義済みGraph-oracle上で100%の正誤一致** | PAG oracle未導出はBLOCKEDであり真のDAG向きへの完全一致は要求しない |
| AC-D03 | 通常のfloat64固定sample代数値・独立Reference | abs(actual−ref) ≤ 1e−10 + 1e−8×max(1,abs(ref)) | **候補**。同じdtype・定義・rank成立・条件数κ₂≤1e8のwell-conditioned fixtureに限る |
| AC-D04 | exact rational/群差/Graph hash/JSON bool/status | 数学上/論理上の離散量は**完全一致**（整数・列挙・byte hash） | 演算順によるfloating sample値はD03。hashでは単なる意味的等価だけで許容しない |
| AC-D05 | 保存/再読込、集合components、null/無界flag、privacy/path | 集合・endpoint・schema/原因codeの**lossless round-trip 100%** | AR集合を通常の二数値CIへ損失変換しない。NaN/Infinity JSON不許可 |
| AC-D06 | 固定seed・完全一致environmentの再実行 | deterministic componentは同一実効出力。並列数値推定のfloatはD03適用 | byte-levelの再現性が非保証な並列演算は精度境界とconfig hashを明示して別許容 |
| AC-D07 | Fail-closed、旧Product/v2 regression、方法誤label | hard invalid fixtureの**誤許可0件**、legacy契約の期待差分0件 | 旧v2 overrideを新E11未識別ゲートへ流用禁止 |

**精度の非適用:** nearly singular、AR重根付近、finite-difference、SCM ill-conditioned weights、非一意解等は同じD03閾値で合否しない。condition number・symbolic/high-precision independent reference・set membershipを先行して別の方法別Numerical ACをfreezeし、条件未充足ならBLOCKED/REVIEWとする。

### 1.2. AC-A：AR confidence-set topology・端点

| AC ID | 対象 | 提案受入基準 |
|---|---|---|
| AC-A01 | DGP-024 AR-Q1〜Q4 | set kind（bounded/2-ray/half-line/all-real）**4/4一致**、connected components、順序、開閉、無界端点の符号全て一致 |
| AC-A02 | Regular simple rootの端点 | abs(endpoint−oracle) ≤ 1e−6×max(1,abs(oracle))。**係数の特異・重根・near-tangentは対象外**で別条件数に応じた精度契約 |
| AC-A03 | 集合所属判定 | 正確な独立二次不等式oracleで、各区間内部／外部／端点近傍の事前指定検査点について、端点上の浮動誤差帯を除く**誤判定0件** |
| AC-A04 | G2意味契約 | 正常just-ID ARでAVAILABLE/EMPTY **0件**、unbounded/disconnected/all-realを切断してfinite CI化**0件** |
| AC-A05 | 推論と点推定の分離 | sample first-stage=0等でpoint unavailableでもARが定義可能なら信頼集合を評価。ARが未定義/分散非PSDなら正常EMPTYではなくtyped failure **100%** |

B0/B1のheteroskedasticity-robust ARが数式どおり実装されたことと、そのcoverageが名目95%近傍になることは**別AC**。後者はAC-I。通常Wald CIをweak-IV robustと呼ばない。Q1〜Q4の形状oracleは代数unitであり、IIDサンプルでその形が現れる頻度は主張しない。

### 1.3. AC-I：CI・AR集合の被覆率と推論可用性（F2）

**確認的推論を提供するMethodに限る候補。** 名目confidence level=0.95、各事前登録した評価点・Estimand・DGP/難度/標本サイズセルについて以下を提案する。

| AC ID | 指標 | 提案受入基準 | 根拠／限界 |
|---|---|---|---|
| AC-I01 | regular DGPのpointwise CI coverage、AR set coverage | 真のcoverage pに対する多重性補正済み**片側Wilson下限 L(p) ≥ 0.93** | 名目0.95に対する最大2 percentage-pointの工学上の許容不足を提案。名目水準を数学的に保証したことにはならない |
| AC-I02 | regular eligible DGPの推論生成失敗率 | failure割合fに対する多重性補正済み**片側Wilson上限 U(f) ≤ 0.01** | 1%は健全なmethod/configに対する工学上の許容案。高難度weak-IVで推論が無界でも利用可なら失敗としない |
| AC-I03 | CIの意味 | pointwise(x) / average / simultaneousを正しく識別し、誤ったlabel **0件** | CATE 3点の各95% CIは同時95% bandではない |
| AC-I04 | interval width / set informativeness | 平均幅・median幅・分位点・AR集合形状率を全て報告。**一律上限は設けない** | 弱IVでは適切に無界/全実数となり得る。常に無界にする実装がcoverageだけで合格しないよう、強IV reference caseの有限性・形状もAC-Aで評価 |
| AC-I05 | 複数の推論設定 | inference method/backend/final model/nuisance/fold/bootstrap単位に別セルで評価 | 有限CI API取得は被覆の証拠ではない。S/T/X/DRLearnerに一律Bootstrapを強制しない |
| AC-I06 | 適用範囲外 | CI未対応・unsupported・対象不整合ではCI=null＋理由、confirmatory science-pass禁止 | exploratory適格なpoint-onlyはD05の方針に従い保存可能 |

**Coverageの分母を固定:** R_total＝全simulation repetitions、R_ci＝実際に区間/集合を返したrepetition、K_cover＝R_ci中にtruthが含まれた回数。conditional coverage＝K_cover/R_ci、availability＝R_ci/R_total。I01は**I02のavailability条件を同時に満たしたセル**でのみ判定可能。失敗を削って良く見せることは禁止。全repetitionに対するjoint success+coverage率も診断として報告する。

**方法条件:** Clusters/HAC等は初期B0/B1 ARの適用外。Pointwise CIの科学的推論Methodが未選定なら、I01を計算可能でも正式PASSしない。weak-IV B0/B1はIID heteroskedastic-robust asymptoticの適用条件を別に検査。

### 1.4. AC-T：帰無size・power・検出不能性

| AC ID | 指標 | 提案受入基準 |
|---|---|---|
| AC-T01 | 適格なnull下のType-I（nominal α=0.05） | 多重性補正済み**片側Wilson上限 U(size) ≤ 0.07**（2ポイントの工学許容） |
| AC-T02 | 明示的な対立下のpower | **候補**多重性補正済み片側Wilson下限 L(power) ≥ 0.80。ただし真の対立強度、n、null式、CI/testが**既に固定され計算予算が成立するケースのみ** |
| AC-T03 | Negative Controlの判断 | null非棄却から無交絡の証明を出力するケース **0件**。NCO非特異性の負例を必須 |
| AC-T04 | 仮定違反の科学的stress | バイアス、誤被覆、警告を定量記録。**exclusion等の隠れた違反を自動検出するpower閾値は設定しない** |
| AC-T05 | Type-I/Power対象外 | 単なるSubset安定性、Random CC、Graph fidelity、Sensitivity数値式には**無理に検定sizeを追加しない** |

T02は効果サイズが弱ければ任意の適切な方法でも達成不能になるため、Method未確定時の全件統一Hard Gateではない。各Methodの対立DGPと閾値を事前採用するまではREQUIRES_CALIBRATION。

### 1.5. AC-P：Bias・RMSE・Support・推論不確実性

| AC ID | 指標 | 提案受入基準 |
|---|---|---|
| AC-P01 | Bias | `bias_hat=(1/R_est)Σ(θhat_r−θ_true)`、`MCSE_bias=sd(θhat_r−θ_true)/sqrt(R_est)`。**regular well-specified DGPの提案:** `abs(bias_hat) + z_K * MCSE_bias <= 0.05 * s0` |
| AC-P02 | Outcome scaleの定義 | `s_0=SD[Y(0)]` または同等の**DGP指定固定母集団尺度**を事前選択し、未定義/ゼロなら別の物理単位・臨床/事業許容誤差を事前登録。標本実測値に適応して閾値を変えない |
| AC-P03 | RMSE | `sqrt(mean[(θhat_r−θ_true)^2])` とそのMonte Carlo SE（squared-errorのvariance・delta method/paired independent bootstrap）を報告。**regular well-specified caseの改善確認候補:** nを4倍にした際 `RMSE_large/RMSE_small ≤ 0.90`。Method別に事前登録が必要 |
| AC-P04 | 適用範囲と低support | CATE fixed x、ATT(g,t)、RD cutoff、IV structural coefficientなど**正しいestimand**ごとに別評価。extrapolation/positivity構造違反下のBias/RMSEは科学stressでありP01/P03の健全性gateに混ぜない |
| AC-P05 | Point estimator failure | well-specified regular caseに限り**点推定非有限/計算失敗率のWilson上限 ≤0.01**を提案。方法別最小sample/supportを固定すること |
| AC-P06 | PointとCIの関係 | Exploratoryでpoint-only可でもP01/P03の適格な精度検証は省略しない。ConfirmatoryはAC-Iも必須 |

**P01の0.05 s0、P03の0.90は一律科学理論から導かれる「正しい閾値」ではない。** DGPのoutcome noise variance、R/N、forest/DRIV/weak-IVのrate、正しいmodel class、panel/syntheticの実効サンプルサイズを固定してから方法別に再評価・採否する。現段階のP01/P03は**設計上の数値候補**であり、Methodが科学的に妥当でも不適切なノイズ/標本設計で偽FAILし得る。特にARや識別/GraphにP03を汎用適用しない。

### 1.6. AC-G：Graph discovery・endpoint・temporal復元

| AC ID | 指標 | 提案受入基準 |
|---|---|---|
| AC-G01 | Graph serialization/readback | known ground-truth edge type、lag、circle/arrow/tail、GraphVersion hashのlossless保存 **100%**（AC-D02/05と同一） |
| AC-G02 | CI-test null calibration | DGP指定のvalid nullでAC-T01を適用。serial dependence/conditional independenceの前提を別保持 |
| AC-G03 | adjacency precision/recall、FPR、F1、SHD・lag recovery | **DGP・n/T・alpha・CI test・Graph oracleが承認された正例**に限る暫定候補：strong-signal DGPでreplicate平均precision/recallの多重性補正済み下限が各≥0.80、FPRの上限が≤0.10。区間はreplicate単位の独立bootstrap等、方法を事前固定 |
| AC-G04 | endpoint accuracy（PAG/CPDAG） | **Oracle強制端点のみ**で方向正解率を評価。未決のorientationの真DAG方向と一致させるHard Gateは禁止。Endpoint候補≥0.80は**Graph oracle導出後にのみ審査** |
| AC-G05 | 複数edgeと時間seriesの依存 | edgeごとの数を独立repetitionとみなさず、DGP replicate単位で精度のMC intervalを作る。Graph metricの分母zero規則を固定 |
| AC-G06 | 未知PAG oracle | DGP-011等で独立PAG導出がない場合、scientific orientation判定は**BLOCKED**。契約上のendpoint忠実性のみ評価可能 |

**G03の0.80/0.10は初期engineering screening値であり、FCI/PCMCI全般の普遍的科学的適格性基準ではない。** DGPの変数数・隠れた交絡・edge強度・lag構造・sample TとCI-testのsizeをレビュー後、Method×DGP別の誤差許容量とMC不確実性を固定する。実際のTigramite/FCIでCI testがそのDGPに適格かを確認するまで「Graph accuracy PASS」は出さない。

### 1.7. AC-Q、AC-R：準実験、Refutation、Sensitivity

| AC ID | Method family | 定量候補 |
|---|---|---|
| AC-Q01 | 2×2 DiD／Event | 群別差・ATT(g,t)・event-time weightsの**exact sample/oracle parity D03**。Bias/RMSEは各正しいtargetでP01/P03 **条件付き** |
| AC-Q02 | ITS | level=2、slope=.1などの母集団真値に対するP01/P03候補。serial errorでiid CI/SEをvalid扱い **0件**。HAC/GLSの採否・coverageはPENDING |
| AC-Q03 | Sharp/Fuzzy RD | cutoffの片側極限／局所jump／局所WaldのD03真値一致（数式Reference）。bandwidth/local SE/weak local first-stage coverageはPENDING |
| AC-Q04 | SCM | DGP-017 noiselessでpost counterfactual誤差≤D03、donor weights=(.6,.4)は独立rank・一意解が確定した時のみD03。noise付きはP01/P03 **条件付き** |
| AC-Q05 | SDID | DGP-018 ATT=2の既知真値／unit-time weightとobjective valueを独立Referenceに照合。Method-specific optimization tolerance・SE/coverageはPENDING |
| AC-R01 | Placebo・NCの適格null test | 事前指定したnull/testがある時のみT01、十分な対立の強度を設定した時のみT02 |
| AC-R02 | Subset・Random CC・Bootstrap refutation | seed/transform/resample parity D03、sample/cluster unit一致D01/D07、refutation変動率は**report-only**（恣意的な「元効果との差5%以内」等は設けない） |
| AC-R03 | Observed NCE/NCO | opt-in、conditioningとnullの妥当性が承認された時のみT01/02＋typed rejection。Method Scope未決 |
| AC-R04 | OLS partial R²／RV | DGP-020既知OVB bias=0.2581988897…にD03のfloat tolerance、R² domain/status D01。RV値は独立数式Oracleと一緒にfreezeするまでBLOCKED |
| AC-R05 | Propensity sensitivity／ESS | 既知PSのweight、ESS=(Σw)^2/Σw²、clip/trim sampleのreference parity D03。科学的なbias/target変化は報告、改善保証をHard Gateにしない |

## 2. Monte Carlo計画・多重性・合格判定アルゴリズム

### 2.1. 原則ADEMP／測定誤差

Simulation designは Aims、Data Generating Mechanisms、Estimands、Methods、Performance Measures（ADEMP）を事前指定する。各Method-DGP configurationを一つの**evaluation cell**として識別し、truth、n、R、seed streams、method/params/inference、hardware/threads、失敗分母、metric、許容値、family multiplicityを事前登録する。

**反復独立性:** 同じDGPに対する各replicate間で独立RNG streamを用いる。同じreplicateを複数Methodへ共通入力することはpaired comparisonに有効だが、**同一replicateの複数x・複数edge・複数Methodは独立replicateとして水増ししない**。

Monte Carlo standard error：
- `MCSE(coverage_hat)=sqrt(p_hat(1−p_hat)/R_ci)`
- `MCSE(size_hat)=sqrt(p_hat(1−p_hat)/R_null)`
- `MCSE(bias_hat)=sd(θhat−truth)/sqrt(R_est)`
- `MCSE(RMSE)`はsquared errorsのMC varianceをもとにdelta method／independent replicate bootstrapから推定し、非有限/undefined失敗を別途報告する。

**標準設計提案（not frozen）:** regular CI/size確認のR=6,000独立repetitions/セル。p=.95でMCSE≈0.002814（約0.281 percentage points）、p=.05も同値。MCSE≤0.003だけならR≥ceil(.95×.05/.003²)=5,278。**これはMC誤差の精度設計であり、推論がvalidだという実証ではない。**

### 2.2. 全件multiplicityの扱い

Methodが41行あっても「41個」だけが統計判定数ではない。独立した評価セル内のcoverage、size、bias、Graph等について、**Gate07がHard Gateに用いる片側確率判定を列挙し総数Kをfreeze**する。

- Gate-family nominal family-wise α_gate=0.05（**提案**）。
- 各確率指標の片側Wilson score limitに使うzを `z_K=Φ^{-1}(1−0.05/K)` とするBonferroni（independent assumption不要）。
- Lower goalでは `L_Wilson(p_hat,R,z_K)≥p_min`、Upper goalでは `U_Wilson(p_hat,R,z_K)≤p_max`。Bias等の連続指標には同等のMC不確実性上限を設定し、**KにはHard Gateとして用いる比較を全て計上**する。重複カウントや後から外した失敗セルを認めない。
- 片側Wilsonの標準形： `center=(p_hat+z²/(2R))/(1+z²/R)`、`half=z*sqrt(p_hat(1−p_hat)/R+z²/(4R²))/(1+z²/R)`、lower=center−half、upper=center+half。**両側標準Wald p±zSEを小/稀なfailureに無批判に使わない**。
- KをMethod familyで別々に分割する案は将来審査可能だが、今回のDraftでは恣意的family分割で合格率を上げないため**全mandatory stochastic ACを一familyに仮置き**する。

**注意:** Bonferroniを適用しても、推定したcoverageと理論上の「95%被覆が成立する」主張は同義ではない。信頼性を評価する側のMC不確実性の補正であり、Method CIの信頼水準そのものを変更する操作ではない。 Kと各指標に要するR・CPU予算はGate前に再計算する。

### 2.3. Sampling plan（数値候補、method別再審査必須）

| Family / 試験Tier | Baseline (探索・開発用提案) | 科学的判定候補 | 実行可能性と適用制限 |
|---|---|---|---|
| RCT、Backdoor、OLS、IPW/AIPW regular | n∈{1,000,4,000}／pilot R=200 | inference/sizeセル R=6,000、n∈{1,000,4,000}の**採用セルを限定してfreeze** | variance・nuisance/PS推定・correct model定義待ち |
| Frontdoor（線形数値） | n∈{2,000,8,000}／pilot R=200 | R=6,000は**計算予算審査後の候補** | 適格stage/SEが不明な間はBLOCKED |
| 非IV CATE7 | n∈{2,000,8,000}、x∈{-0.75,0,0.75}／pilot R=100〜200 | 3点pointwise coverage、R=6,000/セル候補 | DGP-003/004のX支持域内のみ。Forest/Bootstrap多数fitの費用未測定 |
| DRIV（IV異質効果） | n∈{2,000,8,000}、**DGP-008のx∈{-1,+1}**／pilot R=100〜200 | 2点pointwiseのconditional-IV θ(x)、R=6,000/セルは候補 | x=0等の非IV CATE格子を流用禁止。final estimatorは切片を含め真値を表現可能な構成でのみ効果/CI評価。formal momentとconfig採用待ち |
| Wald/B0/B1/AR | n∈{2,000,8,000}と複数first-stage strength／pilot R=200 | weak-IVでも真値集合包含率のR=6,000候補 | 小標本exact保証なし。B1-A semantic target採用済み、schema enum・HC方式/coverage待ち |
| FCI/PCMCI+ / LPCMCI | time T∈{1,000,4,000}等、Graph数・burn-in・null edges固定 | 目標MCSEとoracle有効性からRを導く（初期pilot R=100） | PAG oracleなしでorientation PASS不可。R=6,000一律強制は現実性未審査 |
| DiD/Event/ITS/RDD/SCM/SDID | n_units、cohorts、T_pre/post、cutoff sample、donor数、bandwidthを**別々に固定** | inferential coverageを提供する候補MethodではR=6,000を出発点に精度・費用審査 | 「n=2,000」とだけ記載してpanel/cluster局所の有効情報を代用しない |
| Algebraic/JSON/typed negative | fixtureの固定input 1〜複数case | 全ケース100% exact／D03 tolerance | Monte CarloのR=6,000は不要。DGP-024の4集合形状を必須 |

**計算資源留保:** 上記R=6,000は実用リソースを測定していない提案であり、41 Method×全cellに無制限適用する承認ではない。重いEstimatorでは「Method・DGP・nの必須セル縮約」を独立科学reviewで決定し、Precision/Rを再設計する。**Rを下げるだけで同じ検出力・Science PASSを主張しない。**

### 2.4. 判定状態（形式enumは未承認）

**二値/割合閾値の三値判定（事前登録）:** coverage等の下側目標 p≥p_min に対して、Wilson L≥p_minならPASS候補、Wilson U<p_minならFAIL、それ以外はINCONCLUSIVE。failure/size等の上側目標 p≤p_max には、Wilson U≤p_maxならPASS候補、Wilson L>p_maxならFAIL、それ以外はINCONCLUSIVE。境界の数値丸め、K、片側/両側、比較の厳密な等号は事前定義する。

**連続量の三値判定:** Bias上限δでは U_bias=|bias_hat|+z_K MCSE_bias≤δならPASS候補、L_bias=max(0,|bias_hat|−z_K MCSE_bias)>δならFAIL、その他INCONCLUSIVE。RMSE比やGraph accuracyに対しては、replicate単位の適切なsimultaneous confidence boundを事前指定し、同様に区間の全体が許容域内/外にあるかを判定する。各replicateのedge/固定xを擬似独立標本にしない。

| 状態 | 条件 | Gate扱い |
|---|---|---|
| PASS_CANDIDATE | contractを満たし、独立Reference+pre-frozen全mandatory数値ACを満たす | ReviewerとOwnerのScience/Gate承認までは正式PASSではない |
| FAIL | 定義された確実な契約違反／十分な検証力で定量基準を逸脱 | failed evidence、原因分析、fixと再実行 |
| INCONCLUSIVE | MC区間が閾値を跨ぐ、R不足、K未確定、inference availability低下、境界精度不明 | **PASS扱い禁止**。事前に決めた増分R/独立seedかre-designが必要 |
| BLOCKED | Estimand、Graph oracle、Method Config、Reference、Scope等の未決 | 計算実行をもって解消しない。契約/承認先行 |
| NOT_APPLICABLE | 当該Methodには不要なmetric | 根拠を記録し、全件合格母数へ水増ししない |

**再実行:** Gate用のseed/generator/version/reference/thresholdをfreezeした後、失敗したcellを見てseed・DGP難度・許容値を黙って緩和しない。仕様変更時は別versionの審査と新たなpre-registered実験が必要。

### 2.5. 統合レビューで訂正した評価契約（2026-11-16）

1. **DRIVの評価支持域:** DGP-008ではXは二値{-1,+1}であり、3点の非IV CATE用gridとは異なる。DRIVのtruthはθ(-1)=1.5、θ(+1)=2.5。切片なしfinal modelなどモデルクラス誤指定のstressは、適格なDRIVのBias/CI Hard Gateと別セルで評価する。
2. **FCIのGraph oracle適格性:** DGP-011の同時点2観測変数だけで潜在交絡のbidirected edgeを識別できることを前提とする方向Accuracyは不適格。独立同値類が証明できるmotifでのみG04を適用し、それまではBLOCKED。
3. **横断ACへの登録:** 本書のAC-D04/D05/D06、AC-I04/I05/I06、AC-T04/T05、AC-P02/P04/P06の11ルールはMethod行に直接書かれていなくても有効な横断・report-only/適用範囲制約である。SR04-Fで明示的なSR04:X-IDと適用Method familyへバインドし、無責任なUNBOUNDを解消する。科学的閾値の承認は別。
4. **MarkDownと数式:** 本文の代数式のバッククォートescapeおよび`AC-P01`のパイプを修正した。数値閾値自体は前Draftから変更しない。
5. **数値ACの原則:** coverageの片側Wilson下限やGraph accuracyの候補値を、確定していないMethod configに先行して「正式採用」とすることは禁止。Monte Carlo R=6,000も計算予算・多重性Kのfreeze前は仮案。

## 3. Method別AC割当（全41 Method）

Policy略号：D=AC-D、A=AC-A、P=AC-P、I=AC-I、T=AC-T、G=AC-G、Q=AC-Q、R=AC-R。**P/I/T/G/Qの数値条件が未確定な行はCONDITIONAL/BLOCKEDであり、閾値一覧の存在だけでPASS可にはならない。**

### 3.1. Phase1（20件）

| Method ID | Positive DGP / Reference | Mandatory policy候補 | 独自の数値/対象・判定保留 |
|---|---|---|---|
| P1-M01 | DGP-001 / REF-G01,I01 | D01,D02,D07 | 無作為化Design/ATE exact。NEG-001拒否100% |
| P1-M02 | DGP-002,021 / REF-G01,I01 | D01,D02,D07 | 調整集合のvalidity、collider/mediator負例100% |
| P1-M03 | DGP-002,021 / REF-G01,I01 | D01,D02,D07 | DoWhyと独立Graphの識別式整合100%。optional backendの意味の検証 |
| P1-M04 | DGP-005 / REF-I02 | D01,D02,D07 | Frontdoor識別条件exact。数値推定M07と独立 |
| P1-M05 | DGP-006 / REF-I03 | D01,D02,D07 | IV候補の正しいtarget/対象label、無条件LATEへの誤昇格0 |
| P1-M06 | DGP-011,021 / REF-G02 | D02,G01,G02,G03,G04,G06 | FCI PAG oracle/同値類/CI-test別契約。orientation定量ACはBLOCKED |
| P1-M07 | DGP-005 / REF-E04 | D03,P01,P03,I01,I02 | Frontdoor線形stage/SE 未確定。ATE=3数値truth、適用条件付き |
| P1-M08 | DGP-001,022 / REF-E01 | D03,P01,P03,P05,I01,I02 | RCT ATE=2、null0。CI方式別に95% coverage |
| P1-M09 | DGP-002 / REF-E01,I01 | D03,P01,P03,P05,I01,I02 | OLS加法モデル。ATT一般化/heterogeneity targetに注意 |
| P1-M10 | DGP-002,003,023 / REF-E02 | D03,P01,P03,P05,I01,I02,R05 | IPW ATE=2/ATT=2.2、normalizationとestimated PSのSE別検証 |
| P1-M11 | DGP-002,003 / REF-E03 | D03,P01,P03,P05,I01,I02 | AIPW DR正否別試験。ATT IF/推論未決 |
| P1-M12 | DGP-022 / REF-R01 | D01,R01,T01 | Placebo nullのType-Iはnull/test採用後。因果性を保証しない |
| P1-M13 | DGP-001,002 / REF-R01 | D01,D03,R02 | Subset構成・seed parity、subset安定性はreport-only |
| P1-M14 | DGP-002 / REF-R01 | D01,D03,R02 | Random CC noise摂動。未観測交絡検出powerを要求しない |
| P1-M15 | DGP-001,002 / REF-R01 | D01,D03,R02 | Bootstrap refutation。resampling-unit/SE validity未選定ならCIはBLOCKED |
| P1-M16 | DGP-021,002 / REF-G01,R01 | D01,D02,R02 | 有効調整集合100%／誤調整拒否 |
| P1-M17 | DGP-002,023 / REF-E02 | D03,R05 | clipping/trim/ESS parity。改善を合格条件としない |
| P1-M18 | DGP-019 / REF-R02 | D01,T01,T02,T03,R03 | NCE正しいnullとstrength/n未確定。Owner採否済み／Science未実施 |
| P1-M19 | DGP-019 / REF-R02 | D01,T01,T02,T03,R03 | NCO無作為null variantと交絡特異性負例。Owner採否済み／Science未実施 |
| P1-M20 | DGP-020 / REF-R03 | D01,D03,R04 | classic OLS OVB=0.2581988897…、RV数値未実装/Owner採否済み／Science未実施 |

### 3.2. Phase2（8件）

| Method ID | Positive DGP / Reference | Mandatory policy候補 | 独自の数値/対象・判定保留 |
|---|---|---|---|
| P2-M01 | DGP-003 / REF-E05 | D01,P01,P03,P05,I01,I02,I03 | LinearDML CATE(x)=2+x、linear-final/asymptotic推論設定待ち |
| P2-M02 | DGP-004 / REF-E05 | D01,P01,P03,P05,I01,I02,I03 | CausalForestDML非線形CATE、forest inference/演算予算待ち |
| P2-M03 | DGP-003,004 / REF-E05,E03 | D01,P01,P03,P05,I01,I02,I03 | DRLearner finalモデル/Bootstrap方式別の被覆。finite CI APIは証拠外 |
| P2-M04 | DGP-004 / REF-E05,E03 | D01,P01,P03,P05,I01,I02,I03 | ForestDRLearner forest/DR推論の前提待ち |
| P2-M05 | DGP-002,003 / REF-E05 | D01,P01,P03,P05,I01,I02,I03 | S-Learner shared modelによる縮小、pointwise CIは構成別 |
| P2-M06 | DGP-003,004 / REF-E05 | D01,P01,P03,P05,I01,I02,I03 | T-Learner arm support、CIモデル別 |
| P2-M07 | DGP-003,004 / REF-E05 | D01,P01,P03,P05,I01,I02,I03 | X-Learner pseudo-outcomeとweight／支持域 |
| P2-M08 | DGP-008 / REF-E06 | D01,P01,P03,P05,I01,I02,I03 | DRIV-A θ_IV(x)の条件付き残差momentはOwner採用済み。実効projection/final model/CI未検証、LATE誤表示0 |

### 3.3. Phase3（13件）

| Method ID | Positive DGP / Reference | Mandatory policy候補 | 独自の数値/対象・判定保留 |
|---|---|---|---|
| P3-M01 | DGP-009 / REF-G03 | D01,G01,G02,G03,G05 | PCMCI lag Graph、CI-test正当性とTごとのGraph精度 |
| P3-M02 | DGP-010 / REF-G02,G03 | D01,G01,G02,G03,G04,G06 | PCMCI+、同時点Graph向きのOracle Pending |
| P3-M03 | DGP-011 / REF-G02,G03 | D01,G01,G02,G03,G04,G06 | LPCMCI、PAG/潜在交絡のOracle Pending |
| P3-M04 | DGP-012,013 / REF-Q01 | D03,P01,P03,I01,I02,Q01 | 2×2 DID/独立unit群差のvariance法は採用、staggeredは別Method contract。CI実効validation待ち |
| P3-M05 | DGP-013 / REF-Q01 | D03,P01,P03,I01,I02,Q01 | never-treated baselineのATT(g,t)・cohort-weighted aggregate・unit trajectory bootstrap方針採用。pointwise/joint CI未freeze |
| P3-M06 | DGP-014 / REF-Q02 | D03,P01,P03,I01,I02,Q02 | segmented regression＋HAC方針採用。lag/T/serial errorでcoverage未検証 |
| P3-M07 | DGP-015 / REF-Q03 | D03,P01,P03,I01,I02,Q03 | local-linear＋triangular kernel＋RBC CIを候補採用。実効rdrobust/bandwidth/masspoints未検証 |
| P3-M08 | DGP-016 / REF-Q03,I03 | D03,P01,P03,I01,I02,Q03 | local first-stage ratio＋joint local RBC推論を候補採用。weak local IVはfail-closed、B0 AR無断流用禁止 |
| P3-M09 | DGP-006 / REF-I03,E07 | D03,P01,P03,P05,D07 | Wald ratioとcomplier LATE。B0/B1のAR集合をWald単独Methodに無断要求しない |
| P3-M10 | DGP-006,024 / REF-E07,U01 | D03,P01,P03,P05,A01,A02,A03,A04,A05,I01,I02 | B0 Wald=2SLS sample parity、G2集合、AR coverage |
| P3-M11 | DGP-007,024 / REF-E08,U01 | D03,P01,P03,P05,A01,A02,A03,A04,A05,I01,I02 | B1 linear-IV structural coefficient、formal estimand/HC Config Pending |
| P3-M12 | DGP-017 / REF-Q04 | D03,P01,P03,Q04 | **Owner採用：初期Exploratory point-only**。Placebo/RMSPEは診断でありConfirmatory CIを保証しない |
| P3-M13 | DGP-018 / REF-Q05 | D03,P01,P03,I01,I02,Q05 | unit/time separately optimized weights＋weighted DID、unit-cluster bootstrap refit方針採用。few-treatedでCI不能 |

**注:** P3-M09 Wald ratio単独にはG2 AR confidence setの提供義務を無断追加しない。B0/B1で採用済みのAR推論を、Wald methodが内部参照する場合は実装設計で明記。P3-M08 Fuzzy RDにもB0/B1 ARの保証は自動適用しない。

## 4. Negative 28件・横断9件の定量対応

### 4.1. Negative fixture別のAcceptanceタイプ（28/28）

| NEG | Acceptance | 期待される定量的判定 |
|---|---|---|
| NEG-001 | D01,D07 | explicit invalid assignment/single arm 誤許可0 |
| NEG-002 | D02,D07 | collider/mediator valid誤認0 |
| NEG-003 | D02,D05,D07 | PAG/CPDAG強制DAG変換0 |
| NEG-004 | D02,D07 | 明示Graph上のFrontdoor破綻誤許可0 |
| NEG-005 | P01/P03 report | 線形モデルmisspecを研究stressとしてbias測定。自動不識別判定不要 |
| NEG-006 | D01,A05,I01 conditional | weak/zero first stageのpoint/inference status分離。AR coverageは有効IV条件下のみ |
| NEG-007 | D07 + T04 | 明示invalid IVは拒否、潜在invalid IVはNo Detection Guarantee |
| NEG-008 | D01,D07 + P report | B1の不適格C拒否、非線形stressの対象差を報告 |
| NEG-009 | D01 + P report | DRIV型・宣言moment違反拒否、隠れたexclusion違反検出保証なし |
| NEG-010 | D01,P04 | structural overlap 0と極端weightを区別 |
| NEG-011 | P01/P03 conditional | DR正否のnuisance ablation別bias/RMSE |
| NEG-012 | D01,D07 | split leakage・hash違反誤許可0、検出不能な統計的漏洩は研究stress |
| NEG-013 | D01,D07,I06 | support外とCI未可用を別status、誤区間表示0 |
| NEG-014 | D01,D07 | placebo未生成・同一列誤指定拒否 |
| NEG-015 | D01,D07 | subset arm消失をvalid扱い0 |
| NEG-016 | D01,D07 | wrong bootstrap unit/seed不備をvalid扱い0 |
| NEG-017 | D01,D07 | Random CCをNCの証拠と誤label0 |
| NEG-018 | D03,R05 | clipping/target/ESS reference数値一致 |
| NEG-019 | D01,T03,R03 | NCE/NCO invalid直接経路は明示Graphでreject。非棄却の誤解釈0 |
| NEG-020 | D01,D03,R04 | HC3/classic混同、domain違反、非OLSへ誤適用0 |
| NEG-021 | D01,G01,G06 | timestamp重複等の明示不正、PAG型破壊を拒否 |
| NEG-022 | Q01 / report | parallel trend/staggered TWFE stressの既知真値誤差を記録、全検出保証なし |
| NEG-023 | Q02,Q03 / report | concurrent shock/cutoff manipulation等の診断・局所効果を計測 |
| NEG-024 | Q04,Q05 / report | donor汚染/pre-fit悪化、target/weight出力検証 |
| NEG-025 | A01〜A05,D05 | ARの区間切断・EMPTY正常偽装・非PSDの誤許可0 |
| NEG-026 | T03,R03 | NCO有意≠A-Y交絡の特定、opt-in無し実行0 |
| NEG-027 | D01,D07 | 新E11 fail-closed、旧v2独立回帰の不正変更0 |
| NEG-028 | D01,D02,D05 | 親Graph改変・rationale欠落・endpoint喪失をreject |

### 4.2. 横断9 Case

| X ID | Acceptance | 提案水準 |
|---|---|---|
| X-01 | D01,D04,D07 | schema dispatch・contrast意味一致100%、旧v2誤昇格0 |
| X-02 | D01,D02,D07 | New E11 IdentificationResult→EstimatorSpec fail-closed誤許可0 |
| X-03 | D02,D05,D07 | GraphVersion改訂でoriginal不変、parent/edit rationaleと新識別証拠100% |
| X-04 | D05,A01〜A05,I03,I06 | G2 confidence set lossless、null/reason、set意味の誤表示0 |
| X-05 | D04,D06,D07 | version/seed/split/inputs/manifest hash、変更検知100% |
| X-06 | D01,D05,D07 | path traversal/個票無権限/partial writeの誤許可0 |
| X-07 | D01,D07 | optional deps未導入時のtyped unavailable正確率100%。GPL適合は別Legal Gate |
| X-08 | D01,D07 | 旧Product/v2 override回帰のsemantic drift 0、新E11誤解除0 |
| X-09 | D01,D07 | 68 Scope行と41 Method/9横断/後続Dispositionのtrace missing 0（全体Scope承認は別） |

## 5. False PASSを防ぐ反証・未確定依存

### 5.1. 主要な失敗パターン

1. **識別対象の誤採用:** DGP-006はLATE=2、ATE=3。WaldでATEが2と出てもLATEとしては正しくATEとしては誤り。B1の対象formal enumやDRIV conditional IV thetaが未確定ならBiasの数字は科学的受入証拠にならない。
2. **95%を表示しただけ:** CIを作れた事実は被覆率の情報を含まない。確認的判断はI01/I02、Method別推論設定と独立oracleが必要。
3. **invalid IVを発見したように扱う:** データからexclusionやmonotonicityが必ず検定できるわけではない。宣言上の明示違反拒否とlatent misspec stressを分ける。
4. **弱IVの常時全実数集合:** AR集合が適切に全実数となる場合を失敗にしない一方、強IV・十分情報のDGPとDGP-024代数形状でfinite reference・coverageを検証する。
5. **Forest/FCIを一律閾値で減点:** method rate、CI-test、Graph潜在交絡のoracleが異なる。P01/P03/G03の値はmethod/DGP/nと合わせてfreeze前に反証する。
6. **Simulationのp-value的後出し調整:** K・R・seed・許容差を結果を見て変更しない。pilotは探索データと判定用streamを厳密に分離し、成否未確定ならINCONCLUSIVEとする。

### 5.2. 依存・判断が必要な項目

| Priority | 残る決定 | 前提/Responsible workstream |
|---|---|---|
| OWNER_RESOLVED / SCIENCE_BLOCKER | B1-A構造係数targetは採用、異質性負例/正式enum/ARの実効HC法とcoverage待ち | SR03-R01、Reference E08/U01、Owner/Scientific Methods |
| OWNER_RESOLVED / SCIENCE_BLOCKER | DRIV-A conditional-IV構造斜率targetは採用、EconML final projection/nuisance/inference実証待ち | SR03-R02、Reference E06、Scientific Methods |
| BLOCKER | Frontdoor二段階実効stage、linear model追加仮定と推論 | SR04-C/P1-M07、DoWhy0.14 Method Probe |
| BLOCKER | DGP-011等のPAG/CPDAGの独立oracle | SR04-C/Graph Scientific Methods |
| BLOCKER | DiD/Event/ITS/RDD/SCM/SDIDの初期estimator/inference具体採否 | SR09、Quasi Method Owners |
| MAJOR | DGP-001〜024のnoise variance、sample unit/n/T、強度と弱IV条件の定義 | SR04-B/C科学レビュー |
| MAJOR | P01のs0、P03 RMSE率、G03/G04 Graph精度、T02 powerの適合性 | Method別pilot設計と閾値の事前科学的レビュー |
| MAJOR | mandatory K、MC反復R/compute budget/seed、CIのnominal levelと分母 | SR04-E environment、SR04-F trace、Gate07 |
| OWNER_DECISION_CLOSED / SCIENCE_BLOCKER | NCE/NCO/OLS partial R²＋point RVの個別採否はDEC06全Aで確定。null size/power・RV独立数値・正式要件/Gateは未承認 | SR-01/06、Scientific Methods・Architecture |
| MAJOR | 実効Backend lock、E9/旧Product v2、Tigramite SI GPLv3 | SR-02/10＋Architecture/Legal |
| MAJOR | 68 Scope→Method/横断/後続→FR/NFR/AR/Issue/Gate | SR-12、05 Traceability、正式全体承認 |

## 6. 事前登録テンプレートとGateへ渡す定量証跡

### 6.1. Per-cell acceptance contract例（説明用、非承認）

| Field | 例（受入Readyになる前に必須の値） |
|---|---|
| case_id | P2-M01:DGP-003:regular:x=0:n=4000:CI |
| method_id / target | P2-M01 / pointwise CATE(0)=2 |
| dgp/ref/source | DGP-003 / REF-E05 / generator+oracle SHA（現時点未生成） |
| model/estimand/inference | method-final version, backend effective version, fold/nuisance, CI method/alpha |
| n/R/seed streams | n=4000、R=6000 candidate、実際の独立seedリスト（未freeze） |
| validity | Backdoor/exchangeability/overlap、linear final、合法なX/W |
| requirement | I01 coverage L≥0.93、I02 failure U≤0.01、P01 bias upper ≤0.05s0（Method別採否保留） |
| familywise corrections | Kとz_K（他のmandatoryセル確定後） |
| evidence | oracle hash、simulation replicate-level file、aggregate metrics/MCSE、fail reason、reviewer署名 |
| decision | BLOCKED until effective config/ref/threshold approved; PASS_CANDIDATE only after execution |

### 6.2. 検証証跡の原則

- 1 Method＝最低1正例＋1負例を保持。41行のReferenceと28 Negative/9横断Caseへ、全行のAcceptance policy IDを対応付ける。
- Statusを `SPECIFIED`、`MATH_REVIEWED`、`CONFIG_FROZEN`、`REFERENCE_IMPLEMENTED`、`EXECUTED`、`SCIENCE_REVIEWED`、`GATE_ACCEPTED` 等に分離。**現在はSPECIFIED Draftのみ**。
- PR/ActionでAPI smokeがPASSしても、Monte Carloの成功replicate率・正式Science Gate状態は別に保持する。
- Methodごとの計算予算見積りと科学指標の測定精度が衝突する場合は、Method Scope・目標精度・複数実行TierをHuman ownerへ再提示。**恣意的に閾値を緩めて完了扱いしない**。
- 最終的なGitHub Source SHA・Reference SHA・DGP SHA・Threshold version・実効依存版とEnvironment hashをfreezeし、過去のGate判断を上書きしない。

## 7. 根拠と科学的射程

### 7.1. 一次・方法論の参照

1. Morris, White & Crowther (2019), [Using simulation studies to evaluate statistical methods](https://doi.org/10.1002/sim.8086) — ADEMP、Bias/Coverage・missing estimates、Monte Carlo standard error・反復数、再現性。**本書のRの算定と失敗分母の原則に直接利用。**
2. Brown, Cai & DasGupta (2001), [Interval Estimation for a Binomial Proportion](https://doi.org/10.1214/ss/1009213286) — 二項割合の標準Wald区間の問題とWilson score interval。**本書のcoverage/Type-I/Failure-rate判定のWilson選択を支持。**
3. [SR03-D03：AR/2SLS/G2](20261101_sr03_d03_remaining_2sls_weak_iv_review.md)、[SR03-D05：CATE inference](20261115_sr03_d05_cate_driv_inference_scientific_contract_decision.md)、[SR03-D06：Graph/Override](20261115_sr03_d06_graph_uncertainty_identification_override_decision.md) — 個別Human owner採用の意味とスコープ境界。
4. [Imbens & Angrist (1994), LATE](https://www.gsb.stanford.edu/faculty-research/publications/identification-estimation-local-average-treatment-effects)、[Davidson & MacKinnon (2014), AR set](https://academic.oup.com/ectj/article/17/2/S39/5056440) — complierと弱IV推論。
5. [Callaway & Sant'Anna (2021), DiD](https://doi.org/10.1016/j.jeconom.2020.12.001)、[Sun & Abraham (2021), Event Study](https://doi.org/10.1016/j.jeconom.2020.09.006) — Staggered adoption target/Estimator特異性。
6. [Tigramite公式docs](https://jakobrunge.github.io/tigramite/index.html)、[EconML公式reference](https://www.pywhy.org/EconML/reference.html)、[DoWhy TwoStageRegressionEstimator公式source](https://www.pywhy.org/dowhy/v0.14/_modules/dowhy/causal_estimators/two_stage_regression_estimator.html) — Libraryごとの実行条件候補。runtime/CI/科学的validityを保証する文献ではない。

### 7.2. 根拠から導けない数値

**ここに記載した0.93 coverage、0.07 size、0.01 failure、0.05s0 bias、0.90 RMSE比、Graph precision/recall 0.80等は、上記原著がAriadneに要求した閾値ではない。** 方法論から支持されるのは「指標の意味、MC誤差の算出、事前の基準・DGP/Estimand定義と独立評価の必要性」であり、Ariadneの工学上の許容リスクと計算予算は別の設計判断である。閾値の採否・変更には、科学的目的と受入リスクの根拠をHuman ownerが承認すること。

## 8. 策定の完了と次工程

**本Draft作成で完了したこと:** 41 Method/28 Negative/9横断ContractへAC policyを割当て、数値許容幅案（deterministic・AR・coverage・Type-I・failure・bias・RMSE・Graph）とMC設計・multiplicity/失敗の扱いを明記。SR04-D文書の**策定**に限る。

**未完・実装/Science不可:** 未決Estimand/Graph oracle/Inference、Method-specific cutoffの反証と採否、数値DGP nuisance/noiseの固定、R/n/T/K/seed/CPU・Backend lock、独立Referenceコードと実測、科学review、正式Scope・FR/NFR/AR・Architecture/Gate承認。SR04 blockerはOPEN。

**次の工程:** SR-04 Execution Environment Contract（依存/OS/seed/parallelism/runtime/Resource/Licensing）→ SR-04 Gate07 Traceability（41 Method×AC×DGP×NEG×Ref×FR/Issue/Gate）を策定する。同時にSR03-R01 B1とSR03-R02 DRIVのEstimandを先行解決し、Method別の数値閾値と科学的Acceptanceを確定させる。Codingの実行許可は発行しない。
