# ENH-E11 — SR-04 Reference Specification（策定Draft）

**文書区分:** working_notes／科学的基準（Oracle）設計案。正式なScope・FR/NFR/AR・ADR・Gate 06/07・Work Package・Coding許可ではない。  
**策定日:** 2026-11-15 JST  
**参照:** [Method Acceptance Matrix（41 Method）](20261115_sr04_method_acceptance_matrix_draft.md)／[Scientific Fixture Catalog（DGP24、Stress28、横断9）](20261115_sr04_scientific_fixture_catalog_draft.md)／[Owner決定02](../00_enhance_background/02_enhancement_concept_approval_record.md)／[SR03-D03](20261101_sr03_d03_remaining_2sls_weak_iv_review.md)／[SR03-D05](20261115_sr03_d05_cate_driv_inference_scientific_contract_decision.md)／[SR03-D06](20261115_sr03_d06_graph_uncertainty_identification_override_decision.md)。  
**状態:** REFERENCE_SPEC_DRAFT / METHOD_COVERAGE_41_OF_41 / FORMULA_CANDIDATES_DEFINED / ORACLE_CODE_NOT_IMPLEMENTED / METHOD_CONFIG_PENDING / QUANTITATIVE_AC_PENDING / SCIENCE_NOT_RUN / FULL_CONCEPT_PENDING。  
**境界:** 2026-11-15時点の個別Human owner採用方針に従う。ここでの科学式・候補Configの記載は追加Methodの承認や正式Estimand enumの確定を意味しない。Source SHA／推論仕様／数値許容値／独立Reference実装はGate07で再固定する。

> **2026-11-16 Owner判断の反映:** [2026-11-16 DEC-SR04-01/02 正式個別判断](20261116_sr04_dec01_b1_dec02_driv_owner_decisions.md) により **B1-A**（加法線形IV構造係数）と **DRIV-A**（条件付き構造IV斜率、残差化条件付きモーメント）を**科学的semantic targetとして個別採用**した。本書中の「B1/DRIV formal estimand未決」は**当初Draft時点の記録**であり、現在の未決事項は**正式schema/enum、実効Backend/nuisance/final model、AR/CI、独立Reference実装、定量ACとScience/Gateの検証**である。全体構想は`PENDING_FULL_CONCEPT_APPROVAL`のまま。

> **2026-11-16 DEC-SR04-03／04 個別判断:** [DEC-SR04-03 FD-A](20261116_sr04_dec03_frontdoor_fd_a_owner_decision.md)、[DEC-SR04-04 GRAPH-A](20261116_sr04_dec04_graph_oracle_graph_a_owner_decision.md)の2件をOwnerが採用済み。REF-I02/E04のFD-A stage（M~1+A、Y~1+M+A）とREF-G02/G03のGRAPH-A独立Oracle原理は個別採用。ただし固定標本DoWhy 0.14 stage/parity、CI coverage、MAG/PAG/CPDAG同値類導出・数値Reference実装は未実施。 正式FR/NFR/AR・Architecture・Gate07・Coding・全体構想は未承認（`PENDING_FULL_CONCEPT_APPROVAL`）。この判断より前に記録された「Frontdoor初期Methodの未決」「Graph Oracle採用方針未決」は**Owner方針のみ**解消し、実装・独立Science Oracleの未完成は維持。

## 0. Referenceの役割と受入可能な主張

### 0.1. 四種類の「正解」を混ぜない

| Oracle kind | 何を正解にするか | 合格判定の種類 | 禁止する循環参照 |
|---|---|---|---|
| **STRUCTURAL_TRUTH** | DGPの潜在結果／SCMから導く母集団Estimand、時点・局所・条件付きtarget | 数式導出、解析積分・高精度数値積分との一致 | 被験Estimatorの推定値をtruthにする |
| **SAMPLE_REFERENCE** | 固定された同一サンプルに対する代数的計算値、回帰・重み・null統計量 | deterministic parity（丸め差のみ） | Ariadne adapterから参照値を読み戻して期待値に使う |
| **GRAPH_ORACLE** | 真の構造DAG、潜在射影、識別可能なCPDAG/PAG endpoint／lag情報 | 構造・等価類・条件付き独立性の検証 | 真のDAGの全矢印をそのままPAGの正解向きにする |
| **SAMPLING_REFERENCE** | Method固有の推論手順で導く検定統計量、CI/AR信頼集合、反復標本に対する理論的/漸近的性質 | pointwise coverage、size、power等（未固定閾値） | finite CI表示やBackend smokeをcoverageの証拠とする |

**設計上の区別:** 「DGPの真値を知る」と「そのEstimandが観測分布から識別可能」と「採用Estimatorがその真値を一貫推定する」と「そのCIに正しい被覆がある」は異なる命題。すべて個別のReview/Acceptanceとして保存する。

### 0.2. 独立性・証拠・状態管理

- **Referenceの独立性:** Source DGPの構造と数式はAriadneコードに依存させない。Oracle numerical implementationも被験Method adapter、DoWhy/EconML/Tigramiteの同じestimation/discovery routineを直接再利用しない。外部Packageと比較する場合は補助パリティ（SECONDARY_CHECK）に限定。
- **Source-of-truth:** (A) 数式・定理／方法の一次資料、(B) DGP構造・生成コードrevision、(C) 独立Oracle source/hash、(D) 固定sample/hash、(E) 実測evidenceを別欄で管理。内部メモの存在はScience PASSではない。
- **異種検証:** Closed form×独立Quadrature、matrix formula×独立回帰package、二次不等式×直接集合所属点検、Graph定理×手計算小Graph、といった**独立性の異なる二系統**で重大Referenceをcross-checkする。
- **状態候補（正式enumではない）:** DERIVATION_SPECIFIED／MATH_REVIEW_REQUIRED／REFERENCE_CODE_PENDING／CONFIG_PENDING／IMPLEMENTATION_PARITY_PENDING／SAMPLING_VALIDATION_PENDING／QUANTITATIVE_AC_PENDING／EVIDENCE_ACCEPTED／NOT_APPLICABLE。既存のScientificStatusへ無断移植しない。
- **Scope:** NCE/NCO・OLS partial R²はPhase1 Method候補だが正式採否保留。DRIVのIV_HETEROGENEOUS_EFFECT familyはD01既採用、DRIV-Aの具体的構造斜率とW残差化momentはOwner採用済み。B1-Aのsemantic kindも採用済みだが、両者の正式schema enumは未決。提案を済み扱いしない。

## 1. Reference registry — Method別に再利用する独立計算群

| REF ID | Oracle component | 真値・計算対象 | Evidence type |
|---|---|---|---|
| REF-G01 | DAG/Backdoor/Randomized Graph Oracle | d-separation、backdoor可否、調整集合、Graph固定条件 | 手計算小DAG＋別実装のGraph列挙 |
| REF-G02 | MAG/PAG/CPDAG Oracle | 潜在射影、Markov同値類、強制向きのみ；endpoint type | 理論的Graph導出＋独立列挙、**一部PENDING** |
| REF-G03 | Temporal Graph Oracle | DGP-009〜011のtime-unrolled親、lag、同時点、潜在交絡 | 生成構造＋独立CI/Graph判定 |
| REF-I01 | Backdoor/Randomized Identification Oracle | g-formulaとtarget population／支配する調整集合 | 代数・積分／Graph |
| REF-I02 | Frontdoor Identification Oracle | Frontdoor functional、A→M→Y総効果 | 非パラメトリック識別式／独立積分 |
| REF-I03 | IV Identification Oracle | 二値Z/A、Complier principal stratumとWald＝LATE条件 | 潜在結果の母集団列挙 |
| REF-E01 | Difference/OLS Reference | 同一標本平均差、切片・係数、HCと古典SE区別 | 代数線形方程式＋独立回帰結果 |
| REF-E02 | IPW/IPTW Reference | ATE/ATT weights、PS、ESS、clippingと対象 | 手計算重み・Monte Carlo |
| REF-E03 | AIPW Reference | ATE/ATT別のDR式、nuisanceの反証 | 独立 influence-function式＋MC |
| REF-E04 | Frontdoor Two-stage Reference | 適格な線形stage係数積、非線形Frontdoorとの非同等 | SAMPLE formula／DGP真値 |
| REF-E05 | CATE Truth and Nuisance Reference | τ(x)、oracle nuisance、固定x支持域 | 構造式＋高精度積分 |
| REF-E06 | DRIV Conditional-IV Reference | 指定momentのθ_IV(x)／投影target | 条件付き共分散の独立計算、**semantic target Owner採用／実効Method config・Inference未検証** |
| REF-E07 | B0/Wald/2SLS Reference | Group差比と2SLSの完全一致、complier真値 | 標本代数＋principal strata |
| REF-E08 | B1 2SLS Reference | Covariate-residualized単一IV係数β | FWL射影＋独立matrix IV |
| REF-U01 | AR Confidence-set Reference | Robust AR反転、全実数を含む集合形状 | 独立二次不等式・非有限端点検査 |
| REF-R01 | Refutation/Resampling Reference | Placebo、Subset、Random CC、Bootstrapのnull/seed | 独立変換・resampling単位検証 |
| REF-R02 | Negative Control Reference | 観測NCE/NCO条件付き関連nullの母集団値 | SCM相関/線形回帰母数、size/power |
| REF-R03 | Partial-R²/Robustness Value Reference | OVBの偏り式、R² grid、RVの定義 | 理論式＋独立reference、**RV数値式レビュー待ち** |
| REF-Q01 | DiD/Event Study Reference | 2×2 ATT、cohort-time ATT(g,t)、事前指定event-time aggregate | Potential outcomes／群別平均との差 |
| REF-Q02 | ITS Reference | 介入時点の水準・傾き変化、季節・AR誤差 | 生成回帰式／正しい依存共分散 |
| REF-Q03 | Sharp/Fuzzy RD Reference | cutoff両側極限、jump比、局所対象 | 解析極限＋local window独立推定 |
| REF-Q04 | Synthetic Control Reference | 既知donor重み、counterfactual、効果時系列 | 独立凸最適化／noiseless検証 |
| REF-Q05 | Synthetic DiD Reference | Unit/time weighting、構造上のATT | 独立panel算術／SDID一次式、**Method Config未決** |
| REF-X01 | Scientific Contract/Lineage Oracle | New E11 fail-closed、旧v2保存、manifest/hash/schema/privacy | Golden fixtureと型・readback検査 |

**計24 Reference component**（REF-G3 + I3 + E8 + U1 + R3 + Q5 + X1 = 24）。Methodによって複数Oracleを組み合わせるが、上表のIDはReferenceの責任単位であり新API class数を規定しない。

## 2. 識別・平均効果・Frontdoorの計算仕様

### 2.1. Randomized／Backdoor（REF-G01, REF-I01, REF-E01）

- **ATE:** τ_ATE = E[Y(1)-Y(0)]。DGP-001/002では2、DGP-003では2、DGP-004では7/3。
- **ATT:** τ_ATT = E[Y(1)-Y(0)|A=1]。DGP-003では2.2、DGP-004では38/15。ATTをATEのweightに置換しない。
- **Backdoor:** τ_ATE = ∫ {E[Y|A=1,X=x]-E[Y|A=0,X=x]}p(x)dx。適切なDAGとexchangeability/positivityが条件。ATTならp(x|A=1)で平均する。
- **Graph:** DGP-021のfork/confounder、collider、mediator variantごとにXの調整可否を理論的に導出する。特に総効果で媒介Mをadjustment setに無断投入しない。DGP-011のPAGをDAGへ改名して通さない。
- **Sample oracle:** 差の平均は (Σ_{A=1}Y/n1)−(Σ_{A=0}Y/n0)。OLSは固定design matrixのβ_hat=(X'X)^{-1}X'Y（rank確認、実装は安定なQR/SVD等）。真値比較と「同一sampleのOLS結果再現」は別。
- **限定:** 線形OLSでA係数を全ての異質性下のATE/ATTと認定しない。E11で対象に沿うinteraction/standardizationの採用をMethod別に審査。

### 2.2. Propensity IPW/AIPW（REF-E02/E03）

DGP-002〜004のe(x)=.5+.3x（positivity 0.2〜0.8）を**oracle propensity**として与え、実際の推定PSと区別する。

- ATE（Horvitz–Thompson型）のsample oracle: (1/n)Σ{A_iY_i/e_i−(1−A_i)Y_i/(1−e_i)}。Hájek型はarm別に正規化した二つの比の差で、有限sampleでは別物。Ariadneが採用するnormalizationをMethod configとして明記。
- ATT weighted outcome-form参考: treated平均Y − weighted-control平均Y、control weight e/(1−e)、treated weight 1。標本の比正規化方式を固定し、ATE weightの再利用を禁止。
- ESS = (Σw_i)^2/Σw_i²。arm別と全体の定義を別保存。clipping e→clip(e,l,u)とtrimming（行除外）の標的母集団・有限標本差を混同しない。
- AIPW ATE oracle: n^{-1}Σ[μ1(X_i)−μ0(X_i)+A_i{Y_i−μ1(X_i)}/e_i−(1−A_i){Y_i−μ0(X_i)}/(1−e_i)]。
- **AIPW ATTは別式をReference化することが必須**。ATE式へp(X|A=1)を掛けただけでは十分でない。DR条件はPS/Outcomeいずれかの正しい指定とその他の正則性に依存する。推論IFと推定PS・crossfitの影響を審査せず、oracle PSで得られる単純分散を一般の実装CIの正解としない。
- **ATT用の独立sample reference（統合レビュー追補）:** \(\widehat\tau_{ATT}=\frac{1}{n_1}\sum_i[A_i\{Y_i-\widehat\mu_0(X_i)\}-(1-A_i)\frac{\widehat e(X_i)}{1-\widehat e(X_i)}\{Y_i-\widehat\mu_0(X_i)\}]\)、\(n_1=\sum_i A_i\)。この**未正規化のcontrol残差項を使うATT-AIPW/DR形式**は、positivity/一貫性/条件付き交換可能性と nuisanceの一方の整合性等の下でATTを対象とする。実装がcontrol weightを別に正規化する場合は有限sampleで別Estimatorとなるため別sample oracleとする。\(\widehat\mu_0\)の学習fold、\(n_1\)のランダム性、推定PS込みのInfluence Function/CIはMethod別Science Reviewを要する。
- Known truth: DGP-003 τ_ATE=2、τ_ATT=2.2。nuisance oracle/PS misspec、overlap near/structural zero（DGP-023）を別Fixture。

### 2.3. Frontdoorの識別式と二段階の追加仮定（REF-I02/E04）

**一般Frontdoor識別**（二値A、単一連続Mの例）：

E[Y|do(A=a)] = ∫ p(m|A=a) { Σ_{a'∈{0,1}} E[Y|M=m,A=a']p(A=a') }dm。

識別の前提は全A→Y有向経路をMが遮断、A→Mに未遮断Backdoorなし、M→YのBackdoorがAで遮断されること等。**この式が成立することは線形two-stage回帰が十分であることを含意しない。**

DGP-005では A~Bern(logit⁻¹(U)), M=1.5A+εM, Y=2M+U+εY、UはAとYの共通原因。構造上ATE=(1.5)(2)=3。

- **数式Oracle:** α_AM=Cov(A,M)/Var(A)=1.5。第二段階をY∼1+M+Aで指定したとき、線形構造上Mのpartial slope α_MY|A=2。**候補**二段階reference値は1.5×2=3。
- **実装適合の確認点:** DoWhy 0.14のTwoStageRegressionEstimatorは線形モデル限定、初期実装はsingleton mediatorのみを受け付け、first/second stageが各backdoor confounderを参照する。version固定後に**実際のmediation_second_stage_confoundersにAが入るか**を明示的probeで確認する。Y∼Mだけの単純回帰を無条件に正答としない。
- **二重Reference:** (i) 真のSCMからのATE=3、(ii) 独立OLSの2係数積（固定sample）、(iii) 一般Frontdoor g-functionalの積分（正しい条件付き分布）。同じ値になるのは本DGPの条件下。DGP-005非線形variationで(i)/(iii)が識別されたまま(ii)がずれ得ることを検証。
- **推論:** 係数積のdelta、bootstrap等の具体方式・covariance・coverageは未決。APIで有限区間が出てもScience PASSは不可。DoWhy識別/数値を独立のEvidenceにする。

## 3. Graph Discovery（REF-G01〜G03）

### 3.1. FCI／CPDAG／PAG

1. DGP-021の**真のDAG**を保持し、潜在共通原因のあるDGP-011では観測変数への潜在射影MAGとその**Markov等価類PAG**を別のgraph truthとして導出する。Faithfulness/CI-test/powerを独立に審査。
2. **DAGの矢印とPAGのarrowhead/tail/circleは同一の正解ではない。** 観測分布から一意に方向が定まらない場合、真の生成DAGが既知でも当該向きを強制的に正解orientとして採用しない。
3. 小Graphの手計算・m-separation/CI表・潜在射影・Markov同値classの独立列挙を正本候補とする。FCI/LPCMCI実装結果を自身のGraph oracleにしない。DGP-011は現状「潜在射影/PAG endpoint導出待ち」であり、方向AccuracyのScience PASSを禁止。
4. Negative: circle等のendpoint・unoriented関係をDAGへ変換、GraphVersion/refixed parentの消失、未解決Graph→数値推定の自動許可を拒否する。
5. **統合レビュー追補:** DGP-011の同時点X/Yの2観測変数だけから、FCIが観測上のlatent common causeを一意に判定し、bidirected edgeを確定する期待値は設定できない。Gaussianの同じ観測共分散には、直接X→Yで説明する観測的に等価なモデルがある。**FCI positive oracle**は、独立にm-separationとPAGの強制端点を導出できる別の多変数Graph motifを設計する。現在のDGP-011は潜在交絡を含む**Stress/uncertainty fixture**としてのみ使用可能。LPCMCIの時間情報込みPAGは別Reference導出が必要。Tigramiteの`OracleCI`は独立Math Oracleの**補助的クロスチェック**であり同一Backendの結果を最終正解として使わない。

### 3.2. 時系列Graph PCMCI/PCMCI+/LPCMCI

- **PCMCI（DGP-009）:** VAR parent集合は X_{t-1}→X_t、Y_{t-1}→Y_t、X_{t-1}→Y_t（非ゼロ係数の構造）。burn-in、lag最大値、stationarity、独立shockをDGPに固定。
- **PCMCI+（DGP-010）:** 上の遅延関係に加えX_t→Y_tが生成構造。ただしmethod outputのtime-series CPDAGでその同時点向きが**強制されたか未強制か**は独立同値類Oracleにより決める。真の向きの一律回復をAcceptanceにしない。
- **LPCMCI（DGP-011）:** 潜在H_tが生む観測系列間の潜在交絡、遅延parent、PAG endpoint。正しいMAG/PAG oracle導出まで端点完全一致は保留。experimental/unsupported versionなら科学的なnegative resultを返す。
- **CI-test:** Partial correlation等を用いる場合、DGPが満たす分布仮定と条件付き独立性の基準を別指定。null calibration、lag別adjacency TPR/FPR、endpoint error、NaN/時刻重複・系列欠落を評価。時系列CI p値を因果効果の95% CIに転換しない。

## 4. CATEとDRIV（REF-E05/E06）

### 4.1. Backdoor CATE 7 Methodの共通truth

DGP-003：τ(x)=2+x。DGP-004：τ(x)=2+x+x²。xの候補固定gridは {-0.75,0,0.75}。
- DGP-003 truth=[1.25,2,2.75]。
- DGP-004 truth=[1.8125,2,3.3125]。
- 対象は「当該xでのE[Y(1)-Y(0)|X=x]」。全x同時信頼帯、個票の反実仮想誤差、母集団ATEを代替指標にしない。
- **Referenceの二重化:** Potential outcomesの生成関数で個々のY(1)-Y(0)を確定し、固定xで解析・integration（必要なら高精度）を行う。各Methodの学習器で取得したeffectを正解扱いしない。
- **Method別別件:** LinearDML linear finalとnonlinear misspec、CausalForestDML/ForestDRLearnerのforest inference、DRLearner final+nuisance、S/T/X arm support・pseudo-outcomeを区別。S/T/Xのpointwise CIはMethod/最終モデル/Bootstrap再学習単位ごとに被覆を独立評価。nuisanceをoracleに差し替えたcomponent testとend-to-end testは別。
- **探索/確認:** Exploratoryの科学的適格point-onlyを許容。Confirmatoryは対象を事前指定し、Method-specificに適切と検証されたInferenceを要する（D05既採用）。

### 4.2. DRIVのconditional-IV moment候補

DGP-008（X∈{-1,+1}）では、Z~N(0,1), T=(1+.2X)Z+.5U+εT, Y=(2+.5X)T+.3X+.8U+εY、外生ZはU,εから独立。

条件付きモーメント候補：
E[(Z−E[Z|X]){Y−E[Y|X]−θ_IV(X)(T−E[T|X])}|X]=0。

これにより、Cov(T,Z|X)=1+.2X、Cov(Y,Z|X)=(2+.5X)(1+.2X)、θ_IV(x)=Cov(Y,Z|x)/Cov(T,Z|x)=2+.5x。すなわちθ(-1)=1.5、θ(+1)=2.5。

**統合レビュー追補：条件付きIV斜率のReference候補を具体化。** DGP-008のXは\(\{-1,+1\}\)に限るので、評価点は\(x=-1,+1\)とし、非IV CATEの\(x=-0.75,0,+0.75\)を流用しない。\(\mathrm{Cov}(Y,Z\mid X=x)/\mathrm{Cov}(T,Z\mid X=x)\)は\(\theta(x)=2+0.5x\)。EconML DRIVの最終学習器がこの切片付き線形関数を表現することを**科学Benchmarkの前提条件**とする（例：version確認済みのintercept付きfinal estimator）。特に`DRIV`の`fit_cate_intercept=False`のまま、1変数Xを通した線形最終モデルで切片2を表現できると仮定してはならない。原則候補は`projection=False`、`opt_reweighted=False`、`cov_clip`閾値、`fit_cate_intercept=True`および`model_final`指定を明示して別途API probeする。**これは本実装に対する採用済み設定ではない。** 実効DRIV 0.17.0での互換性・Inference/coverageは未実証。

**科学的TargetはOwner採用したが、実装上まだ採用・検証していない部分:**
- **採用Target:** `CONDITIONAL_IV_STRUCTURAL_SLOPE`の条件付き残差化IV moment。**未検証:** 具体的EconML DRIVのorthogonal nuisance/pseudo-outcomeがそのmomentへ適合するか、`fit_cov_directly/projection/cov_clip/opt_reweighted`、`model_final`の表現力、treatment/instrument型、inference availability。
- **モデル射影の問題:** DRIVのfinal modelがθ(x)を正確に表現できない構成では、強いInstrument領域への重み付けを含むprojectionを返す可能性がある。**truth関数=実効の推定先のprojectionとは限らない**。DGP-008はθ(x)を表現できるfinal model候補を確定するまではScience benchmarkで「完全適格」としない。
- 非IV CATEやbinary-Z/A complier LATE、Phase3で初期非採用の条件付き効率的LATE「C」への自動同一視は禁止。formal `IV_HETEROGENEOUS_EFFECT` familyに属することと、特定θの確定は別の判断。
- Reference実装は条件付き共分散を**SCM解析値から独立に**導出し、candidate DRIV設定を採用版でprobe→bias・coverageを評価する。

## 5. IV/LATE/B0/B1・AR（REF-I03/E07/E08/U01）

### 5.1. Complier LATEとB0の代数oracle

DGP-006：principal strata (always=.25, complier=.50, never=.25)、τ_s=(0,2,8)。Z独立かつmonotonicity、exclusion成立。
- 母集団ATE=.25×0+.5×2+.25×8=3、complier LATE=2。
- ITT_A=E[A|Z=1]−E[A|Z=0]=.5、ITT_Y=1、**Wald LATE=ITT_Y/ITT_A=2**。
- 同一sample/同一complete-case/切片あり、1 excluded binary Z/1 endogenous binary A、Cなしの2SLS sample coefficient `β_hat_B0 = (mean(Y|Z=1)−mean(Y|Z=0))/(mean(A|Z=1)−mean(A|Z=0))`。これは数学的同値の**exact parity**（浮動小数点誤差を除く）。母集団LATE=2とのsample exact equalityを要求しない。
- First-stageが0ならβhat ratioは未定義。AR inferenceは識別弱化に対する別軸であり、point missingから必然的に推論missingとは結論しない。
- DGP-006にdefier/Z→Y追加したstressは仮定違反時の**性能評価**であり、隠れたinvalid IVをデータから必ず検出するOracleにはしない。

### 5.2. B1加法線形2SLSのreferenceと残余Estimand分類

Owner採用済み対象：二値Z/A、切片+事前指定の処置前C、1 excluded Z/1 endogenous A、Y=α+βA+γ'C+ε、E[ε|Z,C]=0という条件付きIV momentを要求する。独立観測、rankと外生性・構造式の科学的根拠を別保持する。

`W=[1,C]`、`M_W=I-W(W'W)^{-1}W'`、`z̃=M_WZ`、`ã=M_WA`、`ỹ=M_WY`（逆行列表記はrank条件下。実装は安定QR/SVD）。単一IVの標本Reference：

**`β_hat_B1 = (z̃' ỹ)/(z̃' ã)`**。

これは線形FWL residualizationによるjust-identified IV/2SLS係数であり、**一般のATE・ATT・complier LATE・CLATEを推定する保証ではない**。DGP-007は均質な構造効果β=2の**限定正例**。異質効果とC/Z割付の関係を変えた反例のpseudo-true estimandは別の積分・統計対象を導出してから採用する。

**母集団での線形射影Reference（統合レビュー追補）:** \(W=(1,C^\top)^\top\)、\(\tilde Z=Z-\Pi_W Z\) を母集団線形射影残差とする。rankとInstrument条件により \(\beta_{IV,lin}=E[\tilde ZY]/E[\tilde ZA]\)。\(Y=\alpha+\gamma^\top C+\tau(C)A+\varepsilon\)、\(E[\tilde Z\varepsilon]=0\) であれば \(\beta_{IV,lin}=E[\tilde ZA\tau(C)]/E[\tilde ZA]\)。異質効果下のこの射影比は、重みの正値性・complier性を追加証明しない限り**ATE/ATT/LATEとは呼べない**。DGP-007は\(\tau(C)\equiv2\)なので独立Referenceの真値=2。この代数上の定義でB1の**mathematical target ambiguityの一部を解消**したが、public enum/Method-supported population/heterogeneity contractは未採用。

**B1-Aの加法線形構造係数（均質効果、正しい処置前C/線形baseline、IV妥当性）は2026-11-16にOwner採用。** `LINEAR_IV_STRUCTURAL_COEFFICIENT`は採用された**semantic identifier**であり、正式schema enum/field/versionの発行ではない。B1をD01のIV_HETEROGENEOUS_EFFECTに自動分類することもしない。

### 5.3. IID異分散頑健ARの実装独立reference候補

**I2/G2の採用範囲:** 1 excluded IV/1 endogenous treatment、IID observation unit、heteroskedasticity-robustな**漸近**AR反転をB0/B1の初期基準とする。Cluster/HAC、over-ID、小標本exact coverageは対象外。ARはInstrumentのvalidityを証明しない。

**B0 sample Oracle:** `r_i(b)=Y_i-b A_i`、Zの2群差 `d(b)=mean(r|Z=1)-mean(r|Z=0)`、独立群差のrobust variance `V(b)=s²_1(r(b))/n_1+s²_0(r(b))/n_0`。Varianceの分母n_g vs n_g−1によるfinite-sample conventionと採用HC型をMethod Configで固定。候補AR test `AR(b)=d(b)^2/V(b)`、信頼集合 `C_α={b∈R: AR(b)≤χ²_{1,1−α}}`。弱IVでも識別が弱いこと自体ではこの検定の帰無サイズの漸近評価を禁止しない（その他の正則性が必要）。

DGP-024のsample moments `dY,dA,vYY,vYA,vAA` を固定した二次不等式：
`Q(b)=(dY−b dA)^2−q(vYY−2b vYA+b²vAA)≤0`、`q=χ²_{1,1−α}`。
- `Q`の係数を高精度で評価し、判別式・符号・零次・一次退化を厳密にcase-splitする。**有限grid内で集合端を切断しない**。
- DGP-024のAR-Q1=bounded interval、Q2=two disconnected unbounded rays、Q3=one unbounded half-line、Q4=all real。Q5のnon-PSD/zero-varianceは正常AR結果ではない。数値上のほぼ零と数学的零の扱いは参照の数値許容値で定義が必要。
- **代数的数値チェック（統合レビュー追補）:** α=.05、q=3.841458820694124の時、AR-Q1は[1.0518218236251204, 5.926895365726481]、AR-Q2は(-∞,-0.20315286487771517]∪[0.20315286487771517,∞)、AR-Q3は[-0.7248752638076998,∞)、AR-Q4は全実数。独立の数値二次方程式で計算した**係数/集合形状のsanity check**であり、raw iid sampleからのAR実装・coverageを検証したものではない。
- B0/B1の正常just-ID結果で`AVAILABLE/EMPTY`を許さない（G2既採用）。Degenerate covariance/inversionなら型付きfailureへ。汎用Resultの将来EMPTY表現は別の話。
- G2集合は有限/無界・連結/非連結をlossless componentsで表現。JSON Infinity/NaNを使わず、null端点＋unbounded flags、順序/重複/閉端点を検査。通常の2数値CIは単一有界区間である場合に限る導出view。

**B1 sample Oracle:** 外生regressorsを`W=[1,C]`、full matrix`F=[W,Z]`とする。各候補bにおいて`r(b)=Y-bA`をFへOLS、Z係数が0かを異分散頑健で検定し反転する。HC0を**独立Referenceとして提案**：

`u_Y = M_F Y`, `u_A = M_F A`, `z̃=M_W Z`、`S_Y(b)=Σ_i z̃_i(Y_i-bA_i)`、`V_Y(b)=Σ_i z̃_i²(u_{Y,i}-b u_{A,i})²`。

`AR_B1(b)=S_Y(b)²/V_Y(b)`、`C_α={b:S_Y(b)²−q V_Y(b)≤0}`（V_Y(b)>0の領域）。**検定不等式の左右辺がbの二次多項式**なので、全実数に対する二次不等式の解析で集合を再構成できる。full OLS sandwichで算出したZ coefficient Waldの平方と同じsample値になることを別系統でcross-checkする。HC1等へ変更する場合、定数補正と臨界値・適用範囲を改めてfreezeする（この提案は正式採用ではない）。

**反証:** `z̃'A`が0のsampleでは2SLS pointが未定義でもARは集合を返し得る。V_Y(b)=0又はrank欠落、数値不安定で正しくtestを定義できない時はtyped inference failure。single sampleのAR数値正解とMonte Carlo coverageは別々に検証。

## 6. 準実験・Temporal/SCMの独立Reference

### 6.1. DiD / Event Study（REF-Q01）

- DGP-012の2×2 ATTは `[E(Y|G=1,t=1)-E(Y|G=1,t=0)]-[E(Y|G=0,t=1)-E(Y|G=0,t=0)]=2`（母集団）。並行トレンド/no-anticipationの生成条件に依存し、sample値は誤差を含む。
- DGP-013 cohort `g∈{2,3,never}` に対し `ATT(g,t)=1+(t-g)`（t≥g）。Event-time kの真値は `Σ_{g∈S_k} w_{g,k} ATT(g,g+k)`、`Σ w=1`。重みとcohort supportが未freezeなら**event-time単一数値oracleはPENDING**。TWFE lead/lagがこれと同じ対象とはみなさない。
- 順序、calendar time、group-time cell、clusterとtreatment adoption構造、共通ショックを固定。pretrend placeboのp値非有意をparallel trends真の証明としない。
- 方法推奨候補を作っても、採用するstaggered ATT estimator・variance（cluster、bootstrap等）は正式決定待ち。

### 6.2. ITS（REF-Q02）

DGP-014：`Y_t(0)=1+.02t+sin(2πt/12)+ε_t`、`Y_t=Y_t(0)+1[t≥t0](2+.1(t-t0))`。
- 介入時点のlevel effect=2、post periodのslope change=.1。**回帰Oracleは季節項・時間傾向・intervention step・post-time interactionを含む線形設計行列**で係数を検証。
- ε_tがAR(1)ならiid SEを標準受入としない。HAC/GLSと自己相関推定の具体法は方法選択待ち。concurrent shock追加は構造変化検出と介入因果効果の区別を試す研究stress。

### 6.3. Sharp/Fuzzy RD（REF-Q03）

- DGP-015: cutoff c=0、`τ_RD = lim_{r↓0} E[Y|R=r]−lim_{r↑0} E[Y|R=r]=3`。片側条件付き平均を用いた定義を採る。cutoff周辺のlocal regression/robust bias correction/bandwidthは別Method仕様。
- DGP-016: `jump_A=.5`、`jump_Y=1.5`、`τ_FRD=jump_Y/jump_A=3`。**局所complier効果**であって全域complier LATEやATEへの自動変換をしない。
- density/covariate continuity、manipulation、mass points、bandwidth/momentの弱化は診断・科学stress。観測のみで連続性/除外の成立を無条件に保証しない。Fuzzy RDのCIへB0の無条件ARを無審査流用しない。

### 6.4. Synthetic Control / SDID（REF-Q04/Q05）

- DGP-017（理想SCM）で `Y_1(0,t)=.6 D_2(t)+.4 D_3(t)`、post outcomeに+2。Donor weights=(.6,.4)、post ATT_t=2。**識別しやすいReferenceにはpreperiod donor列の線形独立性と非負・和1制約での解の一意性を明示的に追加**する。noiselessで独立凸最適化／線形代数を照合、noiseありはstatistical tolerance。
- DGP-018の真のATT=2は処置後構造式で与える。SDIDの実装はunit weightsとtime weightsを別々に最適化するため、その2系統を混同しない独立計算が必要。**SDIDの具体loss/regularization/SE/denominatorの方式が未決**ならsample-weight parityのScience PASSは出せない。
- placebo treatment/donor contamination、poor pre-fit、cohort/time support、serial dependenceはMethod固有negative。placebo rankを通常の95% Gaussian CIへ言い換えない。

## 7. Refutation・Negative Control・Sensitivity（REF-R01〜R03）

### 7.1. Refutation系

- Placebo: 事前指定したnull生成規則（shuffle/independent assignment等）下で再推定した統計量分布。元効果が0である確証や因果性の証明ではない。
- Subset: サンプリング対象単位とsubset率、recomputeされたestimandの意味とsupportを明示。rare subgroup欠落時はinvalid test。
- Random Common Cause: 独立人工変数を追加する摂動の再現性。観測Negative Controlや未観測交絡感度とは別。
- Bootstrap refutation: 観測単位独立ならiid bootstrap、cluster/timeなら適用する再標本化を別決定。再fit/nuisance/seedを明記。source dataとbaseline estimatorの科学的正当性はこの検査から得られない。

### 7.2. Observed Negative Control（Scope method採否未決）

DGP-019では `U→A,Y` の潜在交絡と、`Z=U+εZ`、`W=U+εW` の対照変数を構成した。NCE/NCOは**その対照が因果的に無効な直接経路を持たない**こと、対象となるbiasを反映すること、条件付けの妥当性を研究者が根拠付きで宣言して初めて利用候補とする。
- NCE: `Y~A+Z`のZの条件付き関連nullが対象。γ=0はnull候補、γ>0は対立候補。ただし追加したconditioning setが因果DAG上適切かを必須検討。
- NCO: `W~A` のAの関連nullを対象とするなら、**null variantではAをUと独立にした割付**が必要。元の `A~Bern(logit⁻¹(U))` ではγ=0でもW~Aの関連が生じる。これはA-Y交絡の証明ではない。
- Null時のsize、対立時のpower、直接効果やconditioning違反のinvalid graphを別扱い。非棄却→無交絡と結論しない。opt-in未指定時の自動実行禁止。

### 7.3. Partial R²とRobustness Value（Scope method採否未決）

DGP-020のOLS coefficient、**古典OLS** `SE=.2`、`df=100`、`R²_{A~U|C}=.1`、`R²_{Y~U|A,C}=.15` に対し、OVB bias magnitude候補：

`|bias|=SE_classic * sqrt(df * R²_{Y~U|A,C} * R²_{A~U|C} / (1−R²_{A~U|C}))`
`=.2 sqrt(100×.15×.1/.9)=0.258198889747...`。

- 古典的回帰と条件付きpartial R²の定義に限定する。HC3 SEやAIPW/DR/IPWへ無断適用しない。
- RV（効果を0にしうるbalanced partial-R²）とRV_α（有意性まで変えるもの）は別定義。特に前者と後者を同じ数値のReferenceとして保存しない。
- RVの式と統計量はCinelli–Hazlett一次文献とPySensemakr等の**補助計算**で独立に照合した後にTruthとしてfreeze。現時点ではOVB数値例のみDERIVATION_SPECIFIED、RV数値はREFERENCE_CODE_PENDING。

## 8. Method→Reference対応表（全41行）

下記の `PENDING` はMethodをScopeから削除する意味ではない。対象のReference計算の科学的未確定を指す。

### 8.1. Phase1（20）

| Method | 独立Reference | 主たる固定Fixture・留保 |
|---|---|---|
| P1-M01 Native randomized ID | REF-G01,REF-I01 | DGP-001/NEG-001、割付とpopulation |
| P1-M02 Native backdoor ID | REF-G01,REF-I01 | DGP-002/021・NEG-002 |
| P1-M03 DoWhy backdoor ID | REF-G01,REF-I01 | DGP-002/021、API識別式と独立Graph |
| P1-M04 DoWhy frontdoor ID | REF-G01,REF-I02 | DGP-005、非パラメトリック識別 |
| P1-M05 DoWhy IV ID | REF-I03,REF-G01 | DGP-006、DoWhy label≠LATEの無条件証明 |
| P1-M06 FCI PAG | REF-G02 | DGP-011、PAG endpoint Oracle PENDING |
| P1-M07 Frontdoor two-stage | REF-I02,REF-E04 | DGP-005、version別stage Config PENDING |
| P1-M08 Difference | REF-E01 | DGP-001/022、群平均差 |
| P1-M09 OLS | REF-E01,REF-I01 | DGP-002、異質性target制限 |
| P1-M10 IPW | REF-E02 | DGP-002/003/023、ATE/ATT、normalization |
| P1-M11 AIPW | REF-E03 | DGP-002/003、ATT式とIF推論PENDING |
| P1-M12 Placebo | REF-R01 | DGP-022、Null recipe |
| P1-M13 Subset | REF-R01 | DGP-001/002、resampling unit |
| P1-M14 Random CC | REF-R01 | DGP-002、independent noise |
| P1-M15 Bootstrap refutation | REF-R01 | DGP-001/002、dependence-sensitive resampling |
| P1-M16 Adjustment Set | REF-G01,REF-R01 | DGP-021、valid setのみ |
| P1-M17 PS clipping | REF-E02,REF-R01 | DGP-002/023、clipping vs trimming |
| P1-M18 NCE | REF-R02 | DGP-019、Method Scope PENDING |
| P1-M19 NCO | REF-R02 | DGP-019 null variant、Method Scope PENDING |
| P1-M20 OLS partial R²/RV | REF-R03 | DGP-020、Method Scope／RV oracle PENDING |

### 8.2. Phase2（8）

| Method | 独立Reference | 主たる固定Fixture・留保 |
|---|---|---|
| P2-M01 LinearDML | REF-E05 | DGP-003、linear final/CI Config PENDING |
| P2-M02 CausalForestDML | REF-E05 | DGP-004、forest CI Config PENDING |
| P2-M03 DRLearner | REF-E05,REF-E03 | DGP-003/004、final-model CI Config PENDING |
| P2-M04 ForestDRLearner | REF-E05,REF-E03 | DGP-004、forest/DR推論 |
| P2-M05 S-Learner | REF-E05 | DGP-002/003、shared outcome model |
| P2-M06 T-Learner | REF-E05 | DGP-003/004、arm別support |
| P2-M07 X-Learner | REF-E05 | DGP-003/004、pseudo outcome/weights |
| P2-M08 DRIV | REF-E06 | DGP-008、DRIV-A target/momentはOwner採用／Backend実効fit・CI科学妥当性PENDING |

### 8.3. Phase3（13）

| Method | 独立Reference | 主たる固定Fixture・留保 |
|---|---|---|
| P3-M01 PCMCI | REF-G03 | DGP-009、lag structure/CI-test |
| P3-M02 PCMCI+ | REF-G03,REF-G02 | DGP-010、time-series CPDAG oracle PENDING |
| P3-M03 LPCMCI | REF-G03,REF-G02 | DGP-011、time-series PAG oracle PENDING |
| P3-M04 DiD | REF-Q01 | DGP-012/013、staggered estimator/SE PENDING |
| P3-M05 Event Study | REF-Q01 | DGP-013、aggregate weights/SE PENDING |
| P3-M06 ITS | REF-Q02 | DGP-014、HAC/GLS option PENDING |
| P3-M07 Sharp RDD | REF-Q03 | DGP-015、local regression/RBC PENDING |
| P3-M08 Fuzzy RDD | REF-Q03,REF-I03 | DGP-016、cutoff局所IV推論 PENDING |
| P3-M09 Wald ratio | REF-I03,REF-E07 | DGP-006、complier LATE。弱IVに対するAR集合はB0/B1（P3-M10/M11）側の義務でありWald単独Methodには追加しない |
| P3-M10 B0 2SLS | REF-E07,REF-U01 | DGP-006/024、Wald sample parity、AR |
| P3-M11 B1 2SLS | REF-E08,REF-U01 | DGP-007/024、B1-A構造係数はOwner採用／schema enum・2SLS/AR科学実証PENDING |
| P3-M12 Synthetic Control | REF-Q04 | DGP-017、donor rank/unique weight |
| P3-M13 Synthetic DiD | REF-Q05 | DGP-018、unit/time weighting Config PENDING |

**完全性条件:** 上の表は41 Method（P1 20/P2 8/P3 13）を一度ずつ定義し、各行に1以上の独立Referenceを付ける。Method Acceptance Matrix／Fixture CatalogのMethod IDの集合一致を静的検証する。Future scopeや未採用Cを別Methodとして追加しない。

## 9. Stress/Negative 28件のReference上の期待動作

| NEG IDs | 適用するOracleと科学的扱い | 判定対象 |
|---|---|---|
| NEG-001 | REF-I01/REF-E01 | 不適格割付または単一arm：データ・Design条件が明示不充足ならREJECT |
| NEG-002 | REF-G01 | collider/mediatorの不正調整をgraph-theoreticに拒否 |
| NEG-003 | REF-G02/REF-X01 | CPDAG/PAG endpoint fidelity、未確定を識別済みへ昇格しない |
| NEG-004 | REF-I02/REF-G01 | Graph上可視のFrontdoor破綻のみhard reject |
| NEG-005 | REF-I02/REF-E04 | 非線形モデル誤指定で推定bias。識別の成立と数値の失敗を分離 |
| NEG-006 | REF-I03/REF-E07/REF-U01 | weak/zero first stage。点推定・AR集合・診断を分離 |
| NEG-007 | REF-I03/REF-G01 | invalid/defierの明示宣言はreject。隠れた違反は統計的stress |
| NEG-008 | REF-E08 | B1の誤ったC/非線形性と対象Labelの契約違反を分離 |
| NEG-009 | REF-E06 | DRIV moment不一致/weak-IV、検出不可能な隠れたexclusion違反 |
| NEG-010 | REF-E02/REF-E05 | structural zero vs near-overlap、ESS、arm support |
| NEG-011 | REF-E03/REF-E05 | nuisance正否パターン別DR挙動。有限標本exact truthは不要 |
| NEG-012 | REF-E03/REF-E05/REF-X01 | fold leakageはtraceable contract reject、推論破綻stress |
| NEG-013 | REF-E05/REF-E06/REF-X01 | x support外/CI unavailable/Confirmatory nonvalidの別reason |
| NEG-014 | REF-R01 | placebo未生成、同列指定を拒否 |
| NEG-015 | REF-R01 | subsetでarm/subgroup消失、解析不能を記録 |
| NEG-016 | REF-R01 | cluster/timeにiid bootstrap誤適用、seed不明を拒否 |
| NEG-017 | REF-R01 | random CCをobserved NCと誤labelしない |
| NEG-018 | REF-E02 | clippingとtarget・weight定義の整合 |
| NEG-019 | REF-R02 | NCE/NCOの直接経路/null根拠不備。未観測の違反は自動検出保証なし |
| NEG-020 | REF-R03 | HC3誤用、R² domain、非OLSに適用を拒否 |
| NEG-021 | REF-G03/REF-G02 | duplicate time等machine invalidと非定常の疑義を分離 |
| NEG-022 | REF-Q01 | parallel trends/anticipation/TWFEの効果バイアス評価 |
| NEG-023 | REF-Q02/REF-Q03 | concurrent intervention、manipulation、bandwidth、弱局所IV |
| NEG-024 | REF-Q04/REF-Q05 | donor contamination/pre-fit/SDID weighting |
| NEG-025 | REF-U01/REF-X01 | AR集合切断／非PSD／EMPTY偽装を拒否 |
| NEG-026 | REF-R02 | NCO関連≠A-Y交絡、opt-in外の未指定NC実行禁止 |
| NEG-027 | REF-X01/REF-G01 | E11未識別／hash mismatchはfail-closed、旧v2独立回帰 |
| NEG-028 | REF-G02/REF-X01 | GraphVersion親/根拠/endpoint破壊を拒否、新識別 |

**NEGの期待動作enumは正式Schema未確定。** REJECT・WARN/REVIEW・BIAS_STRESS・DIAGNOSTIC・NO_DETECTION_GUARANTEEを区別して方法別に固定する。DGPで仮定を隠したinvalid IVを真として分析する場面に「必ずinvalidと検出して拒否」を合格条件にしない。

## 10. Reference evidence、crosscheck、Environment引渡し

### 10.1. Proposed Reference Artifact Contract

| Field | 意味・受入可能性 |
|---|---|
| reference_id / version / source_sha | REF registry・reference公式/論文ID・独立実装のrevision |
| fixture_id / variant / method_id | DGP/NEG/Methodの参照（41/41 coverage） |
| target_kind / definition / population / contrast | ATE、ATT、CATE(x)、complier LATE、B1構造係数、DRIV θ、局所ATT等 |
| oracle_kind / derivation_ref | STRUCTURAL_TRUTH/SAMPLE_REFERENCE/GRAPH_ORACLE/SAMPLING_REFERENCE |
| truth_value / truth_expression / set_components | 分布真値またはsample oracle、GraphとAR confidence setは別型 |
| uncertainty_level / nominal_alpha / pointwise | Method別CI/AR、値は後続freeze |
| input_data_hash / generator_hash / seed / rng_stream | DGP生成・乱数管理・集団の追跡 |
| backend_effective_version / config_hash / runtime | 実際の試行環境、推論実装の仕様 |
| oracle_computation_hash / independent_check_ref | 被験Methodから独立した計算証拠 |
| expected_reason / observed_reason / eligible_status | 科学的否定理由と実装のstatusを突合 |
| numerical_precision / tolerance_id / mc_replicates | Quantitative Acceptanceでfreeze（**未決**） |
| evidence_state / reviewer / approval_ref | Specification→Independent Review→Science tested→Gate decisionを分離 |

Referenceのtruthを被験Ariadne outputからコピーしない。正常な将来の方法拡張でreferenceを変更した場合はversion更新と承認差分を必須とし、過去Gate証拠の遡及書換えをしない。

### 10.2. 提案するReview sequence（実行・Coding許可ではない）

1. **数学的妥当性レビュー:** DGP真値と対象母集団、Frontdoor・B1・DRIVの追加仮定、PAG/CPDAGの識別可能向きと対象の矛盾を反証。
2. **独立Reference実装の設計承認:** 依存なしの小規模数学コード／高精度数値積分／Graph oracleと、独立パッケージ照合の組合せを固定。Method本体adapterを参考真値に使用しない。
3. **SR04-D:** Method別numerical AC（exact parity tolerance、MCSE、bias/RMSE、coverage、FPR/size/power、graph orientation）を真値・科学難度・sample/replicateごとに事前登録。
4. **SR04-E:** Python3.12/Linux、依存lockとlicense、seed/random stream、n/cluster/time、BLAS/thread、reproducibility/CI fail時の扱いを固定。
5. **SR04-F:** Reference ID→Method ID→DGP/NEG→FR/NFR/AR→Issue→Gate07 evidenceを全件追跡。承認ScopeとArchitecture Reviewを反映しないままGateを実行しない。
6. **Ownerが未採用のMethod/正式enumは保留:** NCE/NCO/RV、B1 kind、DRIV specific estimand、Frontdoor method limitations、各Quasi inferenceなどの明示審議を残す。

### 10.3. 作業メモ作成時点の自己点検（科学Benchmarkではない）

- 前Fixture CatalogのAR-Q1〜Q4について `q=χ²_{1,0.95}` を使う二次不等式の独立計算で、bounded/2-ray/half-line/all-realの形状を確認した。Sample生成・Ariadne AR実装・coverageの検証ではない。
- DGP-003 ATT=2.2、DGP-004 ATT=38/15、DGP-020 OVB bias=0.258198889747... を式から再計算した。**作成時点の導出sanity-checkのみ**であり、Reference実装としてversion/hash済みのartifactは作成していない。
- B1 FWL-HC0の二次不等式形を独立の線形代数で確認したが、HC0の正式選択・AR coverage・MethodのScientific PASSとは別。
- **未確認:** DoWhy 0.14のFrontdoor実効stage-confounder選択、EconML 0.17.0 DRIV最終Model config、FCI/LPCMCIの独立PAG Oracle、QuasiのInference実装とScience benchmarks。

## 11. 一次資料／公式技術仕様

1. [DoWhy 0.14: TwoStageRegressionEstimator implementation](https://www.pywhy.org/dowhy/v0.14/_modules/dowhy/causal_estimators/two_stage_regression_estimator.html) — linear model、singleton frontdoor、各stageのconfounder。
2. [EconML DRIV API（公開0.16系、0.17.0実動作とは区別）](https://www.pywhy.org/EconML/_autosummary/econml.iv.dr.DRIV.html) — conditional-IV estimator、projection/final-model weighting、nuisanceとinference設定。
3. [Tigramite 5.2 official documentation](https://jakobrunge.github.io/tigramite/index.html) — PCMCI/PCMCI+/LPCMCI、CI-tests、端点契約。
4. [Imbens & Angrist (1994), Identification and Estimation of LATE](https://www.gsb.stanford.edu/faculty-research/publications/identification-estimation-local-average-treatment-effects) — principal strata／complier対象。
5. [Davidson & MacKinnon (2014), AR confidence sets](https://academic.oup.com/ectj/article/17/2/S39/5056440) — confidence setと非空性。
6. [Callaway & Sant'Anna (2021), DiD multiple periods](https://doi.org/10.1016/j.jeconom.2020.12.001)、[Sun & Abraham (2021), Event Study](https://doi.org/10.1016/j.jeconom.2020.09.006) — staggered heterogeneity。
7. [Cinelli & Hazlett (2020), Making Sense of Sensitivity](https://doi.org/10.1111/rssb.12348)／[PySensemakr公式ドキュメント](https://pysensemakr.readthedocs.io/en/latest/modules/sensitivity_stats.html) — OVB partial R²とRV。
8. [Abadie, Diamond & Hainmueller (2010), SCM](https://doi.org/10.1198/jasa.2009.ap08746)、[Arkhangelsky et al. (2021), Synthetic DiD](https://doi.org/10.1257/aer.20190159)。

## 12. 完了状態／最短の次工程

**本工程の完了:** 全41 Method→Reference registry→DGP/NEGへ一対一の追跡可能な科学的基準候補を定義した。真値と固定sample parity、Graph等価類、推論・集合の検証を分離し、未採用の方法・未確定のEstimand/Method Configを明示した。

**未完であり、このDraftだけではScience PASS不可:** Reference code、Graph PAG oracle、Frontdoorの実効stage、B1 estimand正式分類、DRIV θ_IV(x)/projection、ATT-AIPW influence function、Quasi estimator/inference選定、RV式のreference、数値Tolerance/coverage、n/R/seed、Gate07証拠、FR/ADR・構想承認。

**直近推奨:** SR-04 Quantitative Acceptance Criteria草案へ進める前に、(A) B1/DRIVの科学的Estimand/候補Method Configを明示審議、(B) Frontdoor/ARの数式・参照レビューとPAG oracle構築依存をacceptance blockerとして正式登録する。Method毎に事前登録可能なAC数値とRを割り当てることが次の文書作業。実装はGate06/07とOwner承認後のみ。
