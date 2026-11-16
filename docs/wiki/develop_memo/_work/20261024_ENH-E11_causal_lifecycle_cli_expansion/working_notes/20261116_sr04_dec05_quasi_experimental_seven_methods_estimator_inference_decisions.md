# ENH-E11 — DEC-SR04-05：準実験7手法のEstimator／Inference 個別科学契約・Owner判断記録

**文書区分:** SR04 Quasi-Experimental Methods科学的判断／独立技術記録。正式FR/NFR/AR、ADR、Gate06/07、実装・Science PASSではない。  
**判断日:** 2026-11-16 JST。**判断主体:** Human owner（本ターンで「DEC-SR04-05：準実験7手法のEstimator／Inference契約を実行」と指示）。  
**個別判断:** `DEC-SR04-05_BASELINE_CONTRACT_OWNER_ACCEPTED / METHOD_SPECIFICATION_BOUNDARY_DECIDED / INFERENCE_VALIDITY_PENDING / BACKEND_SELECTION_PENDING / SCIENCE_NOT_RUN`。  
**全体:** `PENDING_FULL_CONCEPT_APPROVAL / GATE07_NOT_FROZEN`。  
**正本:** [02 Human owner記録](../00_enhance_background/02_enhancement_concept_approval_record.md)に7手法の基準契約の採用事実、本書に代替案・前提・数式・未実証を置く。SR04 A〜FへMethod ID・Fixture・AC・environment・証拠の対応を要約する。  
**先行条件:** 00_04 Scope P3-07〜11/13/14 は未承認の全体提案、SR03 D03のIV/B0/B1とD04 fail-closed契約、SR04 DEC-01〜04の採用方針を改変しない。**7手法のMethodとしての初期ベースラインの選定と、個別Issue/正式Scope/数値受入の承認は別。**

## 0. 7件の採用決定と科学的な保証レベル

| Subdecision | Method | 初期科学Target | 採用するEstimator方針 | Confirmatory Inferenceの適格方式 | 現時点の限界 |
|---|---|---|---|---|---|
| **DEC-05-1** | P3-M04 DiD | 2×2 ATT | 群×時点の平均差の差。staggered ATT(g,t)は別Estimator契約 | 独立単位に対するcluster-by-unit asymptotic SEを一次候補。十分な独立単位・群両側のsupport必須 | sample/inference科学Benchmark未実施 |
| **DEC-05-2** | P3-M05 Event Study | cohort-time ATT(g,t)のevent-time aggregate ATT(e) | **not** naive staggered TWFE lead/lag。never-treated control、preperiod g−1基準のgroup-time DIDを推定し、事前指定の非負cohort weightsで集約 | 個体・群cohortを保持し、unit trajectoryのcohort-stratified bootstrapで全time/cellを再fit。pointwise/simultaneousを別version | 分散の推定・多重性・cohort support未検証 |
| **DEC-05-3** | P3-M06 ITS | 介入直後level変化β_L、post slope変化β_S、指定時点効果 | segmented OLS + 指定済みtime trend・seasonality・intervention indicator | **HAC/Newey-West型covarianceを一次候補**。自己相関程度に応じたGLS/AR errorは別法 | 同時ショック不在の因果識別はデータから保証できない |
| **DEC-05-4** | P3-M07 Sharp RDD | cutoff cにおける局所平均処置効果 | cutoffの左右でlocal-linear（p=1）・triangular kernel、事前指定bandwidth selector | **robust bias-corrected (RBC) CI**を確認的候補とし、local-quadratic bias correction（q=2）/robust variance/追加bandwidthを版付きで記録 | Python rdrobustは実効pin・lock/API/配布評価未実施 |
| **DEC-05-5** | P3-M08 Fuzzy RDD | cutoff局所complier LATE（reduced-form / first-stageジャンプ） | 同一cutoffでのlocal polynomialの結果ジャンプと処置ジャンプの**比** | **局所Fuzzy RD RBC推論**を一次候補。分子/分母の同時依存と弱いcutoff first-stageをMethod固有に扱う | 0 first stage/弱局所IVではstandard Wald/RBCを無条件有効視しない |
| **DEC-05-6** | P3-M12 Synthetic Control | treated unitの時点別ギャップτ_tおよび明示post-period aggregate | 未介入・干渉のないdonorによるsimplex-constrained preperiod convex weights | **一般的な95%CIは初期提供の必須としない。Point+in-space placebo/RMSPEは探索的診断のみ。** Validなrandomization assignmentを別途事前指定した場合のrandomization inferenceは将来のconfirmatory候補 | 単一treated unitのplacebo順位≠通常CI、近似rank/重み一意性検証待ち |
| **DEC-05-7** | P3-M13 Synthetic DiD | 処置群・処置後期間のweighted panel ATT | preperiodから**unit weights と time weightsを独立推定**し、weighted two-way fixed effectsをfit | 十分なtreated/control independent unitsが存在するblock designで、**unit cluster bootstrap、毎回weights/ATT再推定**を一次候補。few treatedではCI null/requires_review | weights regularizer/optimizer/cluster coverage未検証 |

**本決定のレベル:** 7つのEstimator familyと、適格性に条件付きのInference **方法論的契約を採用**。特定ライブラリの実装、bandwidth・HAC lag・Bootstrap R・CI algorithm backend名・依存lock・正式schema enum・合格率を承認したものではない。**Exploratory point-only と confirmatory valid inference を分離**し、法則の異なるMethodへCIを横流ししない。

## 1. 候補案の比較と非採用理由

| Decision | A：最小定義（採用） | B：汎用化・安易な共用（非採用） | C：初期除外／推論不正（非採用） |
|---|---|---|---|
| 05-1 DiD | 2×2 のATTを基準に単位cluster。staggeredはgroup-timeへ分岐 | heterogeneous staggeredに単一TWFE係数を一般ATTとして扱う | 平行トレンドの非有意pretestだけで因果PASS |
| 05-2 Event | cohort×time target→事前weightでevent-time集約 | naive TWFE leads/lagsを全cohortの動的効果とする | 事後cohort/data支持域選択に無調整CI |
| 05-3 ITS | segmented+seasonality、HAC | 誤差独立のOLS SEをそのまま科学CIにする | level/slope変化だけで他の共時介入を排除したと扱う |
| 05-4 Sharp RD | local-linear+RBC+bandwidth diagnostics | global polynomial/naive local CIを無批判に同等採用 | cutoffを見ず線形予測誤差を局所効果と呼ぶ |
| 05-5 Fuzzy RD | local IV ratio+joint local inference | P3-M09の無条件Wald/ARを同一Estimator/coverage保証で転用 | denominator弱化で不正な有限CIを必ず返す |
| 05-6 SCM | convex donor weights+pre-fit+point、Placeboは診断 | donor placebo順位を一般的な95%信頼区間と表示 | 妥当な単一treated inferenceが未固定でSCM自体をScopeから削除 |
| 05-7 SDID | unit/time separate weights + weighted TWFE / cluster refit | donor weightsだけのSCMや単純TWFEをSDIDと呼ぶ | 1 treated unitへのnaive bootstrapを95%CIとして自動採用 |

**共通の判断原則:** 研究Designが許す因果Estimandと、計算可能な統計量・区間の存在を分ける。cluster数/Time長/bandwidth/rank/positivity等が足りないときは`INFERENCE_UNAVAILABLE`または`REQUIRES_REVIEW`（具体enumはD04で未承認）。**未実証CIがfiniteだからConfirmatory許可**は不可。

## 2. DEC-05-1：2×2 DiD（P3-M04）

### 2.1. 対象・正例

\[
ATT_{2\times2}=\mathrm E[Y_{1}(1)-Y_1(0)\mid G=1].
\]

二時点`t=0,1`、群`G=1` treated／`G=0` untreated、no anticipation、無処置潜在結果の**parallel trends in expectation**、SUTVA/no spillover、positive independent unit supportが条件。

\[
\hat\tau_{DID}=
(\bar Y_{G=1,t=1}-\bar Y_{G=1,t=0})
-(\bar Y_{G=0,t=1}-\bar Y_{G=0,t=0}).
\]

DGP-012はATT=2。グループ時点平均ではなく、unit trajectoryを使う長形式データのunit ID、event timeとtreatment timingをManifestに保存。二時点を越えるstaggered-designを単純TWFEへ暗黙切替しない。

### 2.2. 推論

**一次候補:** treated/controlの**独立unit cluster**に対するheteroskedasticity-robust/cluster-asymptotic SE。2x2 balanced panelではunit change \(\Delta Y_i=Y_{i1}-Y_{i0}\)の**群別平均差**として分散を独立群の標本平均分散の和から導ける。この単位別change分散を独立Sample Oracleとする。unit IDが無い、同一unitが独立でない、少数独立単位・一群に観測が無い場合にはconfirmatory CIを認定しない。bootstrapは設計とcluster単位が適合する場合の代替検証に留める。

**NEG-022:** untreated parallel trends failure、anticipation、group assignmentとpotential outcomesの交絡、群間spillover。観測pretrendの非有意はparallel trendsの証明ではない。

## 3. DEC-05-2：Staggered Event Study（P3-M05）

### 3.1. group-time estimandと固定control定義

cohort \(G_i=g\) は**初回処置時点**、never-treated \(G_i=\infty\)、absorbing treatmentを初期条件とする。

\[
ATT(g,t)=\mathrm E[Y_{it}(g)-Y_{it}(0)\mid G_i=g],\quad t\ge g.
\]

**初期baseline:** 一貫した`never-treated`をcontrol、`g-1`をbase periodにして、

\[
\hat{ATT}(g,t)=
[\overline{Y_t-Y_{g-1}}]_{G=g}
-
[\overline{Y_t-Y_{g-1}}]_{G=\infty}.
\]

差分の設計自体がcausalになるのはno anticipationと各`(g,t)`に関するparallel untreated trends、control comparability、cohort/period支持域に依存。covariate conditional PT/OR/IPW/DRは初期positive外の拡張とし、別のMethod科学Reviewなしに追加しない。

event time \(e=t-g\) のaggregateは

\[
ATT(e)=\sum_{g\in\mathcal G_e}w_{g,e}ATT(g,g+e),
\quad
w_{g,e}\ge0,\quad\sum_{g\in\mathcal G_e}w_{g,e}=1.
\]

**デフォルト重み候補:** 各`e`で利用可能なtreated cohortの**対象unit数比例weight**。母集団cohort mix、`\mathcal G_e`とcohort size、対象post horizonを事前登録し、`e`ごとにsupportが変わるため異なるaggregate populationであることをManifestに明示。nonnegativeでなくなるTWFE暗黙weightは禁止。

DGP-013は\(g=2,3,\mathrm{never}\)、\(t=0..4\)、\(\tau(g,t)=1+(t-g)\) for \(t\ge g\)。post effectは`e=0→1`, `e=1→2`等だが、`e`ごとの対象cohort構成は変化する。preperiod pseudo leadは実処置効果でなく**pretrend diagnostic**と呼ぶ。

### 3.2. 推論

**一次候補:** **stratified unit trajectory bootstrap**（cohortごとに独立unitを再標本化、同一unitの全時点を保持）でcohort-time ATTを全て再計算し、事前固定したweightでevent-time系列を再集約。cohortの組成、同一個体の時間依存、共通control群を尊重する。単一event-timeの95%CIは**pointwise**であり、全event-time同時信頼帯は事前にmax-stat等の別校正を要求。treated/cohort/controlの独立unit support不足なら`CI_UNAVAILABLE`。最終Bootstrap定義／studentization／replicate R・KはSR04-D/Eのfreeze待ち。

**NEG-022:** 異質動的効果のTWFE污染、anticipation/parallel trends failure、cohort-time空セル、処置済みunitの誤ったcontrol流用。naive TWFE leadの非ゼロはそのままanticipationの証明ではない。

## 4. DEC-05-3：ITS（P3-M06）

**Initial target:** 介入時点`t0`のlevel変化\(\beta_L\)、介入後のtrend増分\(\beta_S\)と、post horizon \(h\) の\(\tau(t_0+h)=\beta_L+\beta_S h\)。介入前のmean patternおよび季節性が無介入でも継続し、他の同時ショックがない**強いCounterfactual仮定**に条件付き。

\[
Y_t=\beta_0+\beta_1t+\beta_L I(t\ge t_0)
+\beta_S(t-t_0)I(t\ge t_0)
+s(t)+u_t.
\]

**Estimator baseline:** segmented OLS、`s(t)`の事前指定（DGP-014なら周期12のsine/cosine）、介入位置、burn-in・lag・欠測を固定する。DGP-014は\(\beta_L=2\)、\(\beta_S=0.1\)。AIC等でseasonality/介入時点を都合良く事後選択するなら別Selective-Inference検証が必要。

**Inference baseline:** HAC/Newey-West型Covariance、lag `L`はn/T・残差依存の事前診断に基づいて事前freezeし、必要な弱依存・T漸近条件を明示する。HACが大標本で成立しない小T・非定常・長期依存には`CI_UNAVAILABLE`または別Method審査。AR(1) GLSは対照・拡張候補であり同じCoverageを無条件には主張しない。DGP-014のAR(1)誤差でiid OLS SEをvalidなCIとして報告することを`NEG-023`で拒否／stress。

**Causal claim:** segmented coefficientが見つかっても、政策以外の共時ショックやreporting changesを排除した因果効果と等価にはならない。Graph/Design assumptionは機械検証済みの証拠と分析者の宣言を区別する。

## 5. DEC-05-4／05-5：Sharp・Fuzzy RDD（P3-M07/M08）

### 5.1. Sharp RDD

\[
\tau_{SRD}
=\lim_{r\downarrow c}\mathrm E[Y\mid R=r]
-\lim_{r\uparrow c}\mathrm E[Y\mid R=r],
\quad A=1[R\ge c].
\]

**Baseline estimator:** `c`事前指定、左右の**local linear p=1**、triangular kernel、`rdbwselect`など適格に版固定したdata-driven bandwidth候補を使う。local sample数、mass points/score density、covariate balanceなどを診断。DGP-015の`c=0`、局所効果=3。global polynomialや全域ATEとは区別。

**Inference:** `q=2`のlocal-quadratic bias correctionに基づく**RBC CI**を初期Confirmatory候補に採用。通常のpoint estimate、bias-corrected estimate、RBC区間と実効bandwidth `h,b`／vceを別フィールド。少数local support/Manipulation/近傍positivity不成立ではCIをfail-closed。density testが非棄却であってもscore manipulation不在の証明ではない。

### 5.2. Fuzzy RDD

threshold assignment \(Z=1[R\ge c]\) のとき、局所効果は、

\[
\tau_{FRD}
=\frac{\lim_{r\downarrow c}\mathrm E[Y\mid R=r]
-\lim_{r\uparrow c}\mathrm E[Y\mid R=r]}
{\lim_{r\downarrow c}\mathrm E[A\mid R=r]
-\lim_{r\uparrow c}\mathrm E[A\mid R=r]}.
\]

cutoff近傍の潜在Outcome/処置反応の連続性、除外、単調性、局所first stageの正値が揃う場合の**局所complier LATE**であり、Sharp RDDの局所ITTまたはB0の全域LATEとは異なる。DGP-016は\(\Delta A=0.5\)、\(\Delta Y=1.5\)、\(\tau=3\)。

**Estimator/Inference baseline:** 同一cutoffのlocal polynomialで\(\widehat{\Delta Y},\widehat{\Delta A}\)を推定し、両者の**同時共分散を含める**Fuzzy-RDに適格なRBC procedureを主候補とする。候補ソフトウェアのPython版`rdrobust`はsharp/fuzzy双方のlocal-polynomial point & RBC CIを公開。**特定versionの採用/導入/License/数値parityはまだ承認・probeしていない**。

**Weak local IV:** \(\Delta A\)が0/小さいとき通常のlocal Wald ratio/normal CIが有効とは限らない。P3-M09/10/11のB0/B1弱IV AR集合を**そのままRD用推論として流用しない**。弱局所IV専用のrobust CI/集合推論を追加審議し科学Benchmarkを通すまではconfirmatory不可／理由付き`INFERENCE_UNAVAILABLE`。Bootstrapに置き換えるだけで弱IV問題が解消すると主張しない。

**NEG-023:** heaping/mass points、cutoff manipulation、bandwidth過大、局所first-stage collapse、invalid exclusion/monotonicity、併走政策。これらは観測された設計矛盾と潜在仮定違反を分離し、後者の全自動検出を約束しない。

## 6. DEC-05-6：Synthetic Control（P3-M12）

**Initial population:** 単一treated unit `i=1`と事前指定の未処置donors `j=2..J+1`、処置時刻`t0`を境にno treatment contamination/no interference。対象は\(\tau_{1t}=Y_{1t}-Y_{1t}(0)\) for \(t\ge t0\)と、明示的平均\(\frac{1}{T_\mathrm{post}}\sum\tau_{1t}\)。

**Estimator baseline:** 前処置期の`Y`行列から、

\[
\hat w=\arg\min_{w\in\Delta_J}
 \sum_{t<t_0}\Big(Y_{1t}-\sum_{j=2}^{J+1}w_jY_{jt}\Big)^2,
\quad \Delta_J=\{w_j\ge0,\ \sum_jw_j=1\}.
\]

\(\hat{Y}_{1t}(0)=\sum_j\hat w_jY_{jt}\)、\(\hat\tau_{1t}=Y_{1t}-\hat Y_{1t}(0)\)。DGP-017のnoiseless正例で\(\hat w=(0.6,0.4)\)、post \(\tau=2\)。**重みの一意性**はdonor preperiod軌跡のrank・simplex制約と解の条件に依存し、\(\hat Y\)が真値でも唯一weightsを必ず要求しない。正例ではrankを事前検査する。

**Inference:** **初期defaultはExploratory point estimateのみ**。in-space placeboのpost/pre RMSPE ratioやrankは**診断**であり、無条件のfrequentist 95%CIや同等p-valueではない。もし交換可能性・treatment assignment mechanismを事前に具体化しrandomization testの統計量・処置割当可能集合を定義できる特別な研究なら、別の`RANDOMIZATION_INFERENCE_ELIGIBLE`Method cellとして審査可能。**confirmatoryにCIが得られない研究ではCI=null + reason、科学的に有効なCIを捏造しない。** SCMをMethod提供範囲から削除する判断ではない。

**NEG-024:** treatedとの共通因子support欠如、donor被処置、poor pre-fit、介入後donor汚染、非一意解・unstable weights、placebo CI偽表示。pre-fitが良いだけでunobserved counterfactual validityを証明しない。

## 7. DEC-05-7：Synthetic DiD（P3-M13）

**Initial population/design:** Balanced panel、unitごとに明確な介入時刻、初期正例は`T_pre/T_post`が全treated unitsで同じabsorbing block、donor/control unitは同時期に未介入。対象はtreated × postの平均ATT。多cohortのstaggered SDIDはこの初期保証外。

**Estimator baseline:** pre-period/control情報により、control-unit simplex weights \(\hat\omega\)（intercept/regularization条件付き）、pre-time simplex weights \(\hat\lambda\) を**別々の最適化問題**で推定し、treated/post weightsを事前固定する。その後、二方向固定効果を含むweighted DiD regressionで

\[
\hat\tau_{\mathrm{SDID}}=
\arg\min_{\tau,\alpha_i,\beta_t,\mu}
 \sum_{i,t}\hat\omega_i\hat\lambda_t
 (Y_{it}-\mu-\alpha_i-\beta_t-\tau W_{it})^2
\]

の\(\tau\)とする。\(\hat\omega,\hat\lambda\)の制約・intercept・ridge/regularization・標準化・solver toleranceは**原著アルゴリズムの版付き仕様を再現**する。単にdonor-weightsだけで時点に同じ重みを適用した推定器や、単純TWFEはSDIDとは呼ばない。

**DGP-018:** latent factorを持つpanelでの真値ATT=2。weight recoverabilityとfactor supportが悪いケースも別Stressを構築し、真値=2はpoint estimateが有限sampleで常に2になる保証ではない。

**Inference:** independent unit clustersが十分あるとき、treated/controlを適切に保持した**unit cluster bootstrap**を採用候補とし、各resampleで**unit/time weights双方、TWFE係数、ATTを再推定**。treated unitが1件あるいは極端に少ない場合、naive bootstrapをvalidな95%CIと扱わず、別途assignment design・placebo / jackknife inferenceの適格性評価が必要。re-estimation cost/optim solver failures/availabilityをRの分母へ含める。適格なseparation/regularization/inferenceを実効Backendが提供するかはまだ未検証。

**NEG-024:** donor被処置、rank不足、T_pre不足、unit/time weights混同、bootstrapでweights固定、処置群消失resample、post-treatment leakage。各処置はDesign-specific failureとstatistical bias stressを区別する。

## 8. Backend・Environment・Delivery

| Method group | 最小Profile候補 | backend決定の条件 | License／再現性 |
|---|---|---|---|
| DiD/Event | ENV-BASE + linear regression/panel/units bootstrap | `statsmodels`/独立NumPy算式のパリティ。新packageの採用までは承認しない | cluster ID、cohort/relative time、n_units、effective versions |
| ITS | ENV-BASE + statsmodels候補 | HAC lag/seasonality/GLS optionsをpinしDGP-014で独立sample parity | lag/seasonal order、effective T、thread/seed |
| Sharp/Fuzzy RD | ENV-BASE + **rdrobust optional候補** | Python `rdrobust` version/API、p/q/bandwidth selector/vce、fuzzy resultと独立Oracle | License/Distribution（個別SI）、optional-extras/uv.lock必須 |
| SCM | ENV-BASE + constrained optimizer | simplex/solver tolerance/uniqueness、pre-fit/donor eligibilityとfail-closed | solver/effective BLAS/weights hash |
| SDID | ENV-BASE + independent SDID implementation or version-pinned library候補 | **原著unit/time optimization**の再現性、regularization/solver/weighted two-way fit/cluster resample | Package license、regularization hash、weights/readback、CPU budget |

**現時点での実績:** SR02のDoWhy/EconML/Tigramite install/API smokeは、RD/SCM/SDIDや今回の7件のエンドツーエンド科学的受入ではない。Python `rdrobust`の存在・R/BahaviorのREADMEもAriadneのpython3.12/uv.lock/CLI adapterでのAPI成功を意味しない。プロジェクトの既存依存/extrasを変更した事実はない。個別SI納入のLicense Gateを飛ばさない。

## 9. Gate07 Trace・定量AC・試験計画

| Method | Scope | DGP positive | Negative | Independent Reference | Quant AC | PLAN Gate / Issue |
|---|---|---|---|---|---|---|
| P3-M04 DiD | P3-07 | DGP-012 (2×2 ATT=2) | NEG-022 | REF-Q01 | AC-D03/P01/P03/I01/I02/Q01 | G07 / #21 |
| P3-M05 Event | P3-08 | DGP-013 ATT(g,t)=1+(t−g) | NEG-022 | REF-Q01 | AC-D03/P01/P03/I01/I02/Q01 | G07 / #21 |
| P3-M06 ITS | P3-09 | DGP-014 level2/slope.1 | NEG-023 | REF-Q02 | AC-D03/P01/P03/I01/I02/Q02 | G07 / #21 |
| P3-M07 Sharp RD | P3-10 | DGP-015 cutoff τ=3 | NEG-023 | REF-Q03 | AC-D03/P01/P03/I01/I02/Q03 | G08 / #22 |
| P3-M08 Fuzzy RD | P3-11 | DGP-016 jumpA=.5, jumpY=1.5, LATE=3 | NEG-006/023 | REF-Q03/I03 | AC-D03/P01/P03/I01/I02/Q03 | G08 / #22 |
| P3-M12 SCM | P3-13 | DGP-017 w=(.6,.4), post τ=2 | NEG-024 | REF-Q04 | AC-D03/P01/P03/Q04（**I01/I02無しのpoint-only初期**） | G09 / #23 |
| P3-M13 SDID | P3-14 | DGP-018 ATT=2 | NEG-024 | REF-Q05 | AC-D03/P01/P03/I01/I02/Q05 | G09 / #23 |

**Hard requirements vs conditional acceptance:**
- Known-truth deterministic/reference parityをAC-D03/Q01〜05と結び付け、noiseless/linear正例とstochastic bias/covを区別。
- CIを初期にConfirmatory candidateとした6手法はMethod-specific assumptions、十分な独立情報、実効SE推定、pointwise coverageを科学的に認証して初めてConfirmatory。**SCMは初期defaultをpoint-only**としてCI availability failureを「不適格な実装」の代わりに「設計上提供しない」旨として型付きにする。SCMにAC-I01/I02を暗黙追加しない。
- DGP/Noise/cluster等の実験計画、R/K/MCSE/閾値・error budgetとCompute budgetはSR04-D/Eでfreeze予定。R=6000を7Method一律に承認・実行しない。
- Method名・「DiD」だけでは、parallel trendやlocal continuity・SCM factor supportの実証ではない。実装可能性（API smoke）、識別条件、構造真値、CI coverage、Decision authorityを別Gateにする。

## 10. 残余と次のOwner／Science工程

| Item | Owner意思決定 | Science/implementation closure |
|---|---|---|
| DEC-SR04-05-1〜7（Method別baseline科学契約） | **OWNER_ACCEPTED** | 本書と02の採用事実を対応付けた |
| DiD/Event cluster / cohort inference | **POLICY_ACCEPTED** | unit/cohort/CIのversionと独立coverage、few-cluster limitを実証 |
| ITS HAC | **POLICY_ACCEPTED** | T長・HAC bandwidth/lags・serial dependenceでcoverage実証 |
| Sharp/Fuzzy RD local/RBC | **POLICY_ACCEPTED** | rdrobust Python実効版/License/weak-IV/bandwidthを検証 |
| SCM point-only + placebo diagnostic | **POLICY_ACCEPTED** | donor rank/identifiability、noiseless sample parity。Confirmatoryの個別randomization inferenceは別Decision |
| SDID unit/time weights + bootstrap | **POLICY_ACCEPTED** | solver/weights/cluster bootstrap refit、few-treated failureを検証 |
| 数値AC/Environment/Schema/Gate | **NOT_FROZEN** | 03/04/05正本、SR04-D/E/F、独立Reference・Monte Carlo・Owner Gate |
| ENH-E11全体Scope | **PENDING_FULL_CONCEPT_APPROVAL** | 68 ScopeとSR-01〜12、FR/NFR/AR/Architectureの個別承認が必要 |

**次のOwner decision候補:** DEC-SR04-06（NCE/NCO/OLS partial R²/RVのMethod採否）→DEC-SR04-07/08（Quant/Environment）→DEC-09（Scope/Architecture/Gate）。DEC-05自体の選択肢議論を無期限化しない。**本ファイル作成ではコード・依存・独立Science Benchmark・正式Gateを実行していない。**

## 11. 直接根拠と限界

1. [Callaway & Sant'Anna (2021), *Difference-in-Differences with Multiple Time Periods*](https://doi.org/10.1016/j.jeconom.2020.12.001) — group-time ATT、集約、clusterに適合するBootstrapと同時推論。**本Projectのcohort/bootstrap設計が既にvalidとの証明ではない**。
2. [Sun & Abraham (2021), *Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects*](https://doi.org/10.1016/j.jeconom.2020.09.006) — staggered leads/lags TWFEの汚染。正例のevent-time estimatorは別実装で再検証。
3. [Bernal, Cummins & Gasparrini (2017), ITS tutorial](https://doi.org/10.1093/ije/dyw098) — trend/seasonality/autocorrelation、介入外の影響の制限。
4. [Calonico, Cattaneo & Titiunik (2014), Robust Data-Driven Inference in the RD Design](https://doi.org/10.1177/1536867X1401400413)、[rdpackages公式Python版](https://github.com/rdpackages/rdrobust) — Sharp/Fuzzyで局所多項式とRBC。採用版/License/実効Ariadne対応は未確認。
5. [Abadie, Diamond & Hainmueller, Synthetic Control](https://www.nber.org/papers/w12831)、[Abadie (2021), *Using Synthetic Controls*](https://doi.org/10.1257/jel.20191450) — donor feasibility、前処置fit、placebo inferenceの仮定依存。
6. [Arkhangelsky et al. (2021), *Synthetic Difference-in-Differences*](https://doi.org/10.1257/aer.20190159)、[NBER working paper](https://www.nber.org/papers/w25532) — unit/time weight、weighted DID、bootstrap等の条件。
7. [SR04統合レビュー](20261116_sr04_af_integration_review_and_blocker_resolution.md)、[SR04 F Gate07 Traceability](20261115_sr04_gate07_traceability_draft.md) — 7 MethodとScope/Fixture/ACの既存紐付け。

**完了の限界:** 7 Methodの設計基準と初期推定/推論の**Owner方針判断**を実施した。科学的な適格性・Inference validity・正式FR/ADR/新Schema・Gate07 PASSは未実証・未承認。
