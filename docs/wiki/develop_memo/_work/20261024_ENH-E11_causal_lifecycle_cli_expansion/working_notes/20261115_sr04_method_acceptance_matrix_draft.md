# ENH-E11 — SR-04 Method Acceptance Matrix（策定Draft）

**文書区分:** `working_notes`／科学的Acceptance設計案。正式FR/NFR/AR、承認Scope、Architecture ADR、Gate06/07、Work Package、Science PASSではない。
**策定日:** 2026-11-15（JST）
**参照branch/SHA:** `prototype/ariadne_mvp` / `e751849a550285d7b99e62755b5cecd8b3986cce`（入力照合Snapshot。受入用freezeではない）
**状態:** `SR04_MATRIX_DRAFT / METHOD_SPEC_PENDING / QUANTITATIVE_AC_PENDING / SCIENCE_NOT_RUN / FULL_CONCEPT_PENDING`
**直接の入力:** [00_04 68行Scope案](../00_enhance_background/00_04_phase1_to_phase3_cli_scope_proposal.md)、[SR-01〜12審査](20261029_cli_scope_review.md)、[SR-03横断](20261101_sr03_identification_estimand_estimator_contract_review.md)、[D03](20261101_sr03_d03_remaining_2sls_weak_iv_review.md)、[D04](20261115_sr03_d04_identification_estimator_contract_options.md)、[D05](20261115_sr03_d05_cate_driv_inference_scientific_contract_decision.md)、[D06](20261115_sr03_d06_graph_uncertainty_identification_override_decision.md)、[02 owner判断](../00_enhance_background/02_enhancement_concept_approval_record.md)。

> **2026-11-16 Owner判断の反映:** [2026-11-16 DEC-SR04-01/02 正式個別判断](20261116_sr04_dec01_b1_dec02_driv_owner_decisions.md) により **B1-A**（加法線形IV構造係数）と **DRIV-A**（条件付き構造IV斜率、残差化条件付きモーメント）を**科学的semantic targetとして個別採用**した。本書中の「B1/DRIV formal estimand未決」は**当初Draft時点の記録**であり、現在の未決事項は**正式schema/enum、実効Backend/nuisance/final model、AR/CI、独立Reference実装、定量ACとScience/Gateの検証**である。全体構想は`PENDING_FULL_CONCEPT_APPROVAL`のまま。

## 0. INTRODUCTION

### 0.1. 目的と非目標

`Method ID → 入力Design/型 → 対象Estimand/Graph target → 識別・推定仮定 → 推論 → Known-truth → Negative Case → Acceptance evidence` を41行の**Method実行・科学検証単位**に展開する。00_04の68行は要求と横断機能を含むため、Method件数とは一致しない。表の行数は計画上の分割であり、正式Method数の承認ではない。

- Phase1: 20行（既存再利用・新規候補・条件付き候補を含む）。
- Phase2: 8行（非IV CATE7＋DRIV1。列挙候補を削減しない）。
- Phase3: 13行（Temporal3＋準実験7＋Wald/B0/B1 3）。
- Methodではない横断要件（schema/lineage/privacy/CLI/version/GraphRefix等）は §5 で受け入れ、Method行を水増ししない。
- `NCE/NCO`、`UNOBSERVED_CONFOUNDING_PARTIAL_R2`、A0上位例外はオーナー採用待ちの候補。前者の「適切なNegative Controlへの任意提供」原則だけは既採用。
- **一切の数値Threshold・Method実装・CI科学妥当性・Scope正式承認をこのDraftで宣言しない。**

### 0.2. 行の規則と合否を混ぜない原則

各行の共通契約: `sr04_id`、`scope_row_id`、`operation_kind`、`scientific_target`、`analysis_unit/population/contrast`、`eligible_design/data_type`、`assumptions_declared`、`assumptions_machine_checked`、`estimator/inference_config`、`known_truth_fixture`、`negative_fixtures`、`metrics`、`acceptance_rule`、`reference_source/version`、`backend_version/seed/split`、`status/reasons`、`evidence_ref`、`scope_status`、`approval_ref`。

**異なる対象の受入指標を混用禁止:** Graph Discovery は adjacency/endpoint/lag とCI-test校正、Identificationは式・適格性・拒否、Effect Estimationはbias/RMSEとMethodに適した推論、Refutation/Sensitivityは計算・null・適用境界・参照値の一致を評価。GraphのCI-test p値は処置効果の信頼区間ではない。

`EXPLORATORY` でも識別・Method適格性の検査は緩めない。`CONFIRMATORY` は事前指定した対象と正当化・検証済みの推論証拠を要求する（D05）。標本で得たfinite CI、Method名、Backend API smoke、非有意なnegative controlはそれぞれScience PASSではない。

**分類の取り扱い:** 下表の「識別済」「因果効果」「構造係数」は指定した仮定下での目標。仮定が現実に成立した証明としない。無効データを統計的に必ず検出できるというAcceptanceを課さない。既知違反のDGPではバイアスの露呈や失敗経路を試験し、観測に基づく自動検出を保証しない。

## 1. Phase 1：科学的識別・探索・平均効果・反証

### 1.1. Identification / Graph Discovery

| SR04 ID | Scope ID | Method／対象 | 適格なDesign・条件 | Known-truth正例 | Negative Case／主な受入 |
|---|---|---|---|---|---|
| P1-M01 | P1-06 | Native Randomized identification／ATE候補 | 実際の割付Design、T/Yの型、Consistencyとsupport | 無作為割付のDAGと一致するATEの識別 | 割付根拠欠落・Treatment単一群なら拒否。識別式、reason、target一致 |
| P1-M02 | P1-06/07 | Native Backdoor identification／ATE・ATT | 固定DAG、事前の交絡集合、禁止変数を調整しない | 既知DAGの正当なadjustment set | collider／mediator誤調整、Graph未解決なら誤ったIDENTIFIEDを出さない |
| P1-M03 | P1-08 | DoWhy Backdoor identification／ATE候補 | DoWhy optional、識別式・Graphとadjustmentの一致 | 既知DAGのBackdoor式をNative/referenceと照合 | 仮定不足・非適格Graph。API成功のみでScience PASSにしない |
| P1-M04 | P1-08 | DoWhy Frontdoor identification／ATE候補 | 全A→Y経路をMが遮断、Frontdoor条件、support | 未観測A-Y交絡あり・有効Mの既知DAGと識別式 | M欠落／A-MまたはM-Yの不適切交絡。数値推定との区別 |
| P1-M05 | P1-08 | DoWhy IV identification／**方法固有の対象は未確定** | 候補IV、独立性・exclusion・relevance等の根拠 | 有効二値Z/AのGraphでIV式 | invalid IV／弱いfirst stage／LATEへの誤変換を禁止。D03採用を自動拡張しない |
| P1-M06 | P1-09 | FCI／PAGと等価類 | 因果Markov・faithfulness、CI test適格性、潜在交絡・sample size | **独立に同値類を導出できるGraph motifのPAG endpoints**。DGP-011の2変数同時点Graphはlatent存在の一意識別正例としない | 偽のDAG向き確定、circle/arrow/tailの消失。不適格CI test、adjacency/endpoint精度・readback |

### 1.2. Effect Estimation（既存＋Frontdoor）

| SR04 ID | Scope ID | Method／Estimand | 適格なDesign・条件 | Known-truth正例 | Negative Case／主な受入 |
|---|---|---|---|---|---|
| P1-M07 | P1-08 | Frontdoor two-stage regression／ATE（D02採用） | P1-M04の識別＋DoWhy実装に整合した段階モデル（線形性等を要審査） | 線形で真値既知のFrontdoor DGP／ATEの数値精度 | 非線形・モデル誤指定、M不足、support不足。識別成功を推定成功と取り違えない |
| P1-M08 | P1-11 | Native diff-in-means／ATE | Randomized、2群support、独立観測など | 既知無作為割付ATE、基準値と一致 | 観測交絡、群欠落、CI不適格。点推定・推論を別判定 |
| P1-M09 | P1-11/17 | Native OLS／採用済み契約範囲のATE/ATT表現 | 線形モデル仮定、調整変数、estimand定義の一致 | 正しい加法モデルと参照OLS | effect heterogeneity下のATE/ATT誤ラベル、悪い調整、SE方式取り違え |
| P1-M10 | P1-11/12 | Native IPW／ATE・ATT（別fixture） | propensity・positivity、ATE/ATT固有weight、clipping/normalization | 正しいPS、既知ATE/ATTのbias/ESS/coverage | 極端なweight、overlap不足、誤重み、PS推定込みSEの不適格 |
| P1-M11 | P1-11/12 | Native AIPW／ATE・ATT（別fixture） | outcome/PS、対象に整合したDR式、crossfit分離 | PSのみ正しい／outcomeのみ正しい等の既知真値DGP | 両nuisance誤指定、leakage、overlap不足、推論被覆不足 |

### 1.3. Refutation / Sensitivity / Negative Control

| SR04 ID | Scope ID | Method／対象 | 適格なDesign・条件 | Known-truth正例 | Negative Case／主な受入 |
|---|---|---|---|---|---|
| P1-M12 | P1-13 | Placebo Treatment refutation／null診断 | placebo mechanism、元Estimator再実行可能、seed固定 | 帰無で効果0のsynthetic placebo | 偽陽性、介入の破壊不十分、元効果の因果妥当性証明との混同 |
| P1-M13 | P1-13 | Data Subset refutation／安定性 | subset法・sampling unit・supportを明示 | iid安定DGPでsubset再推定分布が再現 | rare subgroup消失、biased subset、seed再実行不一致 |
| P1-M14 | P1-14 | Random Common Cause refutation／摂動安定性 | 合法な追加乱数変数、乱数は真のnegative controlではない | 独立ノイズ追加下で効果推定の安定性 | 変数が真の交絡因子だったと偽称しない。random seed/変動幅記録 |
| P1-M15 | P1-14 | Bootstrap refutation／再標本化安定性 | 再標本化単位と独立性・依存構造、モデル再fit | 既知DGPの再標本化結果・再実行一致 | 時系列/clusterへのiid bootstrap誤用、反復・seed不明 |
| P1-M16 | P1-16 | Adjustment Set Sensitivity／設計変更 | 候補集合がDAG上有効であること | 複数の有効調整集合で真値との整合 | collider/mediator投入、誤調整を『robust』と表示しない |
| P1-M17 | P1-16 | Propensity Clipping Sensitivity／truncation効果 | 推定PS、trim/clip ruleと対象母集団を明示 | overlap良好／悪化DGPでESS・biasの変化を測定 | clippingのtarget変化、極端weight、CIを無条件有効扱いしない |
| P1-M18 | P1-15/X-04 | Observed NCE null diagnostic／条件付き関連の反証候補 | 研究者opt-in、NCEのoutcome直接効果なし・共有bias仮定、DAGに整合したconditioning | 有効対照、交絡あり/なしでnullのsize/powerを分離 | 負の対照でない変数、根拠欠落、非有意から無交絡証明は禁止。Method採否保留 |
| P1-M19 | P1-15/X-04 | Observed NCO null diagnostic／条件付き関連の反証候補 | 研究者opt-in、NCOが処置の影響を受けない・共有bias仮定 | 有効対照、交絡あり/なしの既知DGP | 事後変数、同一Outcomeの混同、nullの誤適用。Method採否保留 |
| P1-M20 | P1-17/X-05 | OLS partial R² / RV sensitivity／指定OLS係数 | 連続Y、古典OLS SE/df、2軸partial R²、対象係数を固定 | 数式独立実装／sensemakr等と係数・RV・grid照合 | HC3 SEの無断流用、IPW/AIPW/CATEへ誤適用、R²の範囲外。正式採否保留 |

## 2. Phase 2：非IV CATE 7種類とIV異質効果1種類

**共通の前提:** Backdoor型CATEは適切なeffect modifiers `X`、confounders `W`、consistency、conditional exchangeability、support/positivityを要求。方法によってbinary/discrete/continuous treatmentの対応範囲は異なるので採用Backend version＋具体的constructor/fit設定で再確認。固定した`x`でのpointwise coverageと全`x`同時被覆は別。DRIVだけはIV専用契約。

| SR04 ID | Scope ID | Method／対象 | 固有の適格性・推論候補（未採用） | Known-truth正例 | Negative Case／主な受入 |
|---|---|---|---|---|---|
| P2-M01 | P2-02 | LinearDML／CATE(x) | nuisance/crossfit、linear final、native/asymptotic inference候補 | 線形異質性、固定xのbias/RMSE/coverage | 非線形misspec、leakage、低support、区間と対象の誤対応 |
| P2-M02 | P2-03 | CausalForestDML／CATE(x) | forest/heterogeneity、honesty設定、方法固有inference | 非線形異質性、固定xの効果/coverage | 少数arm、極端overlap、外挿、forest推論条件違反 |
| P2-M03 | P2-04 | DRLearner／CATE(x) | propensity/outcome pseudo-outcome、final model、nativeまたはbootstrap候補 | 少なくとも一方nuisance適切なDGP（条件別） | forest finalでCI unavailable、bootstrap API成功だけでScience認定しない |
| P2-M04 | P2-05 | ForestDRLearner／CATE(x) | DR nuisances、forest推論・support | 非線形異質性、固定x coverage | nuisance misspec＋弱support、uncertainty失敗 |
| P2-M05 | P2-06 | S-Learner／CATE(x) | Treatmentを特徴量に含む1 outcome model、推論は構成別 | 定数・線形効果を再現するDGP | Treatment feature無視・強い正則化による縮小、bootstrap不適格 |
| P2-M06 | P2-07 | T-Learner／CATE(x) | 処置armごとのoutcome model、各arm support | group別outcome既知のDGP | 極端arm imbalance、未観測領域外挿、推論不能 |
| P2-M07 | P2-08 | X-Learner／CATE(x) | pseudo-outcome、arm-specific models、weighting | 不均衡群と既知異質性のDGP | propensity/weighting不適格、pseudo-outcome leakage、被覆不足 |
| P2-M08 | P2-09 | DRIV／**IV_HETEROGENEOUS_EFFECT**（DRIV-A構造斜率はOwner採用、Method/Inference未検証） | conditional IV moment、Instrument/Treatment/contrast型、IV assumptions、nuisance/crossfit、IV固有inference | DGP-008の**x=-1,+1のみ**でθ=1.5,2.5を評価。切片付きfinal model適格性は必須 | 無効/弱いIV、moment・projection不一致、通常CATE・complier LATEへの無根拠変換 |

**既存実証の限界:** 2026-11-01 EconML 0.17.0直接probeでは8 Methodのfit/effectが動作し、追加BootstrapでDRLearner/S/T/Xのfinite CI API取得を確認したが、Ariadne新adapter、bias、coverageは未実証。初期提供候補8手法は削減しない。［[SR-02 probe](20261101_sr02_backend_runtime_probe_results.md)／[D05](20261115_sr03_d05_cate_driv_inference_scientific_contract_decision.md)］

## 3. Phase 3：Temporal・準実験・IV

### 3.1. Graph Discovery と準実験の推定

| SR04 ID | Scope ID | Method／科学的対象 | 固有の適格性・推論候補（未採用） | Known-truth正例 | Negative Case／主な受入 |
|---|---|---|---|---|---|
| P3-M01 | P3-02 | PCMCI／time-lagged graph | causal stationarity、同時点直接linkなし・latent confounderなし、CI test適合 | 既知VAR/非線形時系列のlagged parent recovery | 偽同時点edge、非定常、CI misspec、lag/FPR/recall |
| P3-M02 | P3-03 | PCMCI+／time-series CPDAG | 同時点linkを許容・潜在交絡なし、CI test・time order | lagged＋contemporaneousの既知Graph | 未確定方向を偽のDAG化、CI-test不適格、endpoint fidelity |
| P3-M03 | P3-04 | LPCMCI／time-series PAG | 潜在交絡を許容、causal stationarity等、experimental statusに注意 | latent common causeを含む既知Graph | circle/tail/arrow消失、既知latent Graphを強制DAG化 |
| P3-M04 | P3-07 | DiD／ATT（2×2とstaggeredは別契約） | 無介入時のparallel trends、no anticipation、valid comparison、cluster等 | 2×2既知ATT；staggeredではcohort-time ATTを指定 | 異質性＋staggeredで単純TWFEを正解としない、pretrend有意差非検出を保証としない |
| P3-M05 | P3-08 | Event Study／event-time効果 | timing、cohort、参照期、anticipation、group-time support | 動的真値 `ATT(g,t)` からevent-time aggregate | TWFE lead/lag汚染、empty cohort-time cell、事後選択CIの誤用 |
| P3-M06 | P3-09 | Interrupted Time Series／介入時点のlevel/slope変化 | 介入外の同時ショック除外、ベースline/seasonality/autocorrモデル | 既知step/trend change＋季節性・自己相関 | concurrent intervention、偽トレンド、iid SEの誤用。因果性を単なる構造変化と区別 |
| P3-M07 | P3-10 | Sharp RDD／cutoff局所効果 | 完全sharp assignment、cutoff、running variable局所連続性、bandwidth | cutoffで既知jumpの局所効果 | manipulation/score mass、bandwidth過大、global model代用、robust bias-corrected CI未承認 |
| P3-M08 | P3-11 | Fuzzy RDD／cutoff局所complier効果 | cutoffでTreatment確率jump、連続性、exclusion、monotonicity、局所first-stage | cutoff近傍の既知局所Wald効果 | weak cutoff first stage、sharp RDDへの混同、P3-M09の全域Wald/ARを自動適用しない |
| P3-M09 | P3-12 | Wald ratio／binary Z/A complier LATE | 無条件IV独立性、exclusion、monotonicity、relevance、2群support | 既知LATE；B0と標本点推定パリティ | first-stage=0/weak、invalid IV、通常比CIを弱IV頑健扱いしない |
| P3-M10 | P3-12 | B0 just-identified 2SLS／binary Z/A complier LATE | 切片、共変量なし、単一excluded Z/内生A、I2異分散頑健AR反転 | Waldとの代数的一致とAR集合の形状/被覆 | zero/weak first stage、AR EMPTY正常扱い、finite grid切断 |
| P3-M11 | P3-12 | B1 additive linear 2SLS／**B1-A加法線形IV構造係数（semantic target Owner採用）** | pre-treatment C、単一Z/A、正しい加法線形構造・IV moment、I2 AR反転 | 線形構造係数既知のDGP、独立AR reference | C非線形・異質性でcomplier LATEへ誤変換、rank/cluster/HAC不適格 |
| P3-M12 | P3-13 | Synthetic Control／処置単位の時点別反実仮想ギャップ | 介入前fit、非汚染donor、安定な因子構造等の根拠 | latent factor＋既知介入効果 | donor汚染、pre-fit不十分、placebo順位だけを通常CI扱いしない |
| P3-M13 | P3-14 | Synthetic DiD／panel平均介入効果 | balanced panel等、unit/time weight、実施者の割付パターン | 既知panel ATT/平均効果、unit/time weight参照 | 時間重み・単位重み混同、欠落対照・介入前support、SE方式未固定 |

### 3.2. B1と弱IV・集合の特記事項

- **2026-11-16の決定:** B1-Aの加法線形IV構造係数`LINEAR_IV_STRUCTURAL_COEFFICIENT`という科学的意味はOwner採用済み。具体的な`estimand_kind`正式schema enum/fieldは未決。D03が採用したB0/B1範囲を変更せず、LATE/ATE/IV_HETEROGENEOUS_EFFECTとの形式的対応は別審査。Method名=Estimandとしない。
- **採用済:** B0/B1の弱IV推論基準は独立観測＋異分散頑健漸近AR inversion（I2）、G2型付き集合：bounded/unbounded/disconnected/all-real、正常EMPTY不可。初期Confidence Setを通常finite CIへ損失変換しない。
- **未決:** AR test statistic/covariance/critical value、端点計算法・小標本・covered truthのMonte Carlo、degenerate分岐とeffective null confidence setの参照実装。
- **別物:** Fuzzy RDDの局所IVはcutoff付近の局所化・bias/SE構造を必要とする。B0/B1のAR保証を自動継承しない。
- **旧v2:** Product/v2 `REQUIRES_REVIEW + override` は回帰保護。新E11は科学的非識別・hash mismatchをfail-closedにする。

## 4. Inference / Quantitative Acceptance の横断仕様

### 4.1. 指標割当（方法種別別。閾値未承認）

| 対象種別 | 最低限の評価指標候補 | 推論の評価方式 |
|---|---|---|
| Graph discovery | adjacency precision/recall/FPR、endpoint orientation accuracy、lag recovery、Graph round-trip | CI-testごとnull size/powerの検証。処置効果CI coverageと混同しない |
| Identification | 既知Graphと対象estimandの式一致、false permission/false rejection、status/reasons | CIではなく識別論理・条件別負例・偽のtarget昇格拒否 |
| Effect estimation | bias、RMSE、MAE、nonfinite率、sample/support/ESS、対象ごとの誤表示率 | Method別の分散・confidence intervalまたはconfidence set、固定xでpointwise coverage、Type-Iなど |
| Refutation / NC | 帰無時Type-I、指定違反DGPでのpower、再現性、モデル依存 | 適切なnull検定や摂動分布を対象別に評価。非棄却は無交絡証明でない |
| Sensitivity | 独立数式/referenceとの一致、grid/RV、対象係数・SEの整合、適用境界 | 計算式・benchmark点とmodel仮定、結果の解釈を検証 |
| Quasi / Temporal | Method固有の局所・cohort・時点・Graph target、pretrend/cutoff/lag/donor診断 | cluster/HAC、bias correction、placebo/permutation/bootstrap等はMethod別に適用条件を固定 |

### 4.2. CI coverageの事前計画

名目レベル `1-alpha`、独立したMonte Carlo `R` 回に対するcoverage `p_hat` について、`MCSE ≈ sqrt(p_hat*(1-p_hat)/R)`。これは**反復シミュレーションによる推定誤差**であり、真の被覆許容差ではない。実質的許容帯・検出したいundercoverage、DGP難易度、反復数を先に定め、seed群・n・分割・backend・ハードウェア・failureの扱いを事前に固定する。CIがAVAILABLEの試行だけを恣意的に条件付けてcoverageを過大評価しない。nonfiniteや推論失敗を別分母で報告する。

**評価点:** CATEは事前に固定したsupport内のx grid、局所RDはcutoff、DiD/Eventはcohort/time、IVは母集団とcomplier/structural対象を厳密指定。pointwiseとsimultaneousの保証を混同しない。Method別の`EXPLORATORY`と`CONFIRMATORY`で要求水準を区別する。

**暫定的受入Rule（提案、正式判定ではない）:** Contract integrityを満たさない方法はScienceへ進めない。正しいEstimandのKnown-truthで測定し、対象としているbias/RMSEやType-I・coverage基準を事前に満たし、negative caseでは不適格の理由を正しく出し、旧v2とlineage等の横断条件を満たして初めてGate07のScience PASS候補とする。Graph/Refutationでは同一数値指標を強制しない。

## 5. 共通Contract／回帰／運用Acceptance

| ID | 横断対象・関連Scope | Acceptance候補 |
|---|---|---|
| X-01 | E11 versioned local schema／P1-01〜03,P2-01/10,P3-01/15 | Question/Design/Graph/Dataset/Estimand/contrastとMethodの型・Version整合、invalid入力reject、legacy v2 dispatchを保護 |
| X-02 | Normalized IdentificationResult→EstimatorSpec／D04 | method-specific fail-closed。NOT_IDENTIFIED/REQUIRES_REVIEW/PARTIALを直接pointへ接続しない |
| X-03 | GraphVersion refix／P1-04/05/09,D06 | CPDAG/PAG endpointをround-trip、旧Graph不変、研究者新Version parent/rationale/assumptions保存、新識別Resultを要求 |
| X-04 | EffectResult inference／D03/D05/D06 | point_status/uncertainty_status/science_statusの分離、CI=null+reason、AR setのlossless JSON、Partial-ID識別集合との意味分離 |
| X-05 | Lineage reproducibility／P1-02/18,P2-12/15,P3-17 | dataset/graph/question/design/manifest/artifact hash、実効Backend version/seed/split/params。欠落、不一致時は技術契約エラー |
| X-06 | Local Artifact/privacy／P2-15,P3-17 | 個票CATE Parquetはprivacy/opt-in、path正規化、atomic書込み、readback、checksumを試験 |
| X-07 | Backend optional dep／SR-02 | DoWhy/EconML/Tigramiteのmethodごとにlock・import・version適格性と欠落時のtyped unavailable。SI納入前Tigramite GPLv3適合は別審査 |
| X-08 | Legacy Product/v2／D04 R2 | 既存`causal-analysis-spec/2`・Product/v2のread/execute/override/Resultを既存回帰で保護。新E11 Methodを旧manifestに黙って昇格させない |
| X-09 | Traceability／SR-01〜12 | 68 Scope行を維持し、Method行・横断行・excluded/deferred行へ対応。FR/NFR/AR、Issue、Gate、evidenceへ追跡できること |

## 6. 優先未決事項、依存、閉鎖

| Priority | 未決事項 | 先行Output／受入前提 | 引渡し先 |
|---|---|---|---|
| OWNER_RESOLVED / SCIENCE_BLOCKER | B1-A意味論はOwner採用、正式schema enum／IV・AR数値実証が未決 | B1のtarget/仮定／LATEとの互換性を明記。D03採用を無断変更しない | SR-03残余→03/04／Science Methods |
| BLOCKER | Frontdoor数値推定のMethod適用範囲 | 線形DGP、二段階式、追加仮定、偏り、CI availabilityを独立に評価 | SR-04／P1-M07 |
| OWNER_RESOLVED / SCIENCE_BLOCKER | DRIV-A構造斜率／W残差化momentはOwner採用、実効Backend/CI未確定 | T/Z型、対象集団、条件付きmoment・instrument relevance、真値fixture | SR-03残余／SR-04／P2-M08 |
| BLOCKER | B0/B1 ARの具体統計量／端点参照 | just-ID AR非空・集合形状・弱IV頑健漸近条件、独立reference | SR-04／P3-M10/M11 |
| BLOCKER | DiD/Event/RDD/ITS/SC/SDIDの初期EstimatorとInference選定 | Method別targetとbaseline参照、cluster/HAC/局所等の推論境界 | SR-09＋SR-04 |
| MAJOR | EconML8のInferenceConfig | Backend version・最終モデルごとにpoint/CI能力とcoverage、Exploratory/Confirmatory | SR-07＋SR-04 |
| MAJOR | PCMCI系とFCIのCI test/endpoint・latents | 仮定・CI testがDGPへ適合すること、Graph結果の忠実保持 | SR-08＋SR-04 |
| MAJOR | NCE/NCO・OLS partial R²の正式Scope採否 | opt-in原則のみ既採用。2診断＋OLS限定方式の採否はHuman owner待ち | SR-01/05/06 |
| MAJOR | 数値閾値・Monte Carlo設計 | Reference truth、DGP/n/seed、effect error、coverage/Type-I基準の事前登録 | SR-04→Gate07 |
| MAJOR | 実行・配布・privacy・version lock | 既存Product/v2回帰、atomic/lineage、安全出力、optional+license | SR-02/10／Architecture Review |
| MAJOR | A0上位要求・Product GAP帰属 | 68行の処遇・担当役割・IssueとClosure evidenceの承認 | SR-01/05 |
| MAJOR | 68行→Method/横断/後続→Gateの完全照合 | 5% samplingではなく全68行のscope disposition確認 | SR-12／05 |

**SR-04計画Draftの完了:** 全対象を行ID付きで列挙し、対象・成功・負例・主要指標・未決を表現したこと。**SR-04 blocker解消の条件:** Method固有Estimand/Design/推論/Science acceptance、計算可能なfixture/reference、負例、数値判定Rule、依存version、責任と追跡の正式な確定。**Gate07 Science PASSはfreezeされた契約の実行・独立再検証後のみ。**

### 6.1. 統合レビューによる科学的適用境界の修正（2026-11-16）

- P1-M06のFCIは、潜在交絡を含む生成SCMそのものをPAGの完全向きOracleとはしない。2観測変数だけのDGP-011をlatent有無の識別成功Fixtureとして要求することは不適切である。多変数Graphで独立同値類を証明してからorientation Accuracyを定義する。
- P2-M08のDGP-008で利用可能なXは{-1,+1}だけであり、非IV CATE用の3点評価格子を転用禁止。条件付きIV斜率を表現できるfinal modelのintercept/weights/projectionを事前指定する。
- P3-M09のWald単独Methodには、B0/B1のG2-AR信頼集合を自動必須化しない。逆にP3-M10/M11ではAR集合とCoverageを必須検証候補として保持する。
- 以上は科学的に不適切な**検証条件の是正**であり、Method契約・Backend/Owner/Science PASSの承認ではない。

## 7. 参照した一次資料・公式仕様（要点）

- [Tigramite 5.2公式docs](https://jakobrunge.github.io/tigramite/index.html) — PCMCI/PCMCI+/LPCMCIの対象とCI-test。
- [EconML reference](https://www.pywhy.org/EconML/reference.html) — estimator分類。公開0.16系資料と実probe 0.17.0を混同しない。
- [Davidson & MacKinnon (2014), AR confidence sets](https://doi.org/10.1111/ectj.12015) — AR集合形状、just-identifiedの非空性。
- [Callaway & Sant'Anna (2021), multiple-period DiD](https://doi.org/10.1016/j.jeconom.2020.12.001) — staggered導入とgroup-time効果。
- [Sun & Abraham (2021), event study](https://doi.org/10.1016/j.jeconom.2020.09.006) — TWFE lead/lag汚染。
- [Cattaneo, Idrobo & Titiunik, RD Extensions](https://www.cambridge.org/core/elements/abs/practical-introduction-to-regression-discontinuity-designs/C6A70A32359115510AAC370A7869AE2F) — 局所推定・設計診断。
- [Abadie, Diamond & Hainmueller (2010), SCM](https://doi.org/10.1198/jasa.2009.ap08746) — donorとpre-period fit。
- [Arkhangelsky et al. (2021), SDID](https://doi.org/10.1257/aer.20190159) — unit/time weighting。
- [DoWhy TwoStageRegressionEstimator](https://www.pywhy.org/dowhy/v0.9.1/_modules/dowhy/causal_estimators/two_stage_regression_estimator.html) — 二段階線形推定の契約。採用候補0.14で追加probeが必要。
