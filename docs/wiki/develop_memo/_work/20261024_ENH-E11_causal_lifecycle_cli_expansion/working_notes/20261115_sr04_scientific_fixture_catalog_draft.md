# ENH-E11 — SR-04 Scientific Fixture Catalog（策定Draft）

**文書区分:** working_notes／科学的検証データ仕様案。正式Scope・FR/NFR/AR・ADR・Gate06/07・Work Packageではない。  
**作成:** 2026-11-15 JST  
**対象:** prototype/ariadne_mvp。先行Method Matrix＝[20261115_sr04_method_acceptance_matrix_draft.md](20261115_sr04_method_acceptance_matrix_draft.md)（41 method rows）。  
**確認したOwner決定正本:** [02_enhancement_concept_approval_record.md](../00_enhance_background/02_enhancement_concept_approval_record.md)。  
**状態:** SCIENTIFIC_FIXTURE_CATALOG_DRAFT / ALL_41_MAPPED / ORACLE_IMPLEMENTATION_PENDING / NUMERICAL_ACCEPTANCE_PENDING / SCIENCE_NOT_RUN / PENDING_FULL_CONCEPT_APPROVAL。  
**非承認事項:** ここで導入するDGP数値・検証例・候補Estimand・負例パラメータを正式なMethod仕様、実装結果、数値Acceptance、科学的保証として採用しない。

## 0. 目的と契約

### 0.1. 目的

SR-04 Method Acceptance Matrixの全41行について、**試験入力の生成構造／既知真値／oracleの出自／意図的な破綻条件／受入アサーション**を一意に追跡可能にする。Graph探索・識別・効果推定・診断・Sensitivityは科学的対象が異なるため、共通の「推定誤差 < x」だけでは判定しない。

Phase1=20、Phase2=8、Phase3=13の計41行と、横断契約X-01〜09を個別参照する。各DGPは再利用可能な**科学的シナリオ**であり、各Methodへの利用行が**Fixture Case**である。1 DGPが複数Methodをカバーしても、各Methodの証拠行は統合しない。

### 0.2. Fixtureの正規化フィールド（案）

| Field | 意味・必要性 |
|---|---|
| fixture_case_id | 一意の実行ケースID：Method ID + 正負例/variant/replicateを結び付ける（正式schema未確定） |
| sr04_method_id / scope_row_id | 対応する41行のIDと68行Scope ID。後続FR/Issue/AC/Gateとの連鎖 |
| dgp_id / stress_id | 生成規則と変更条件。数学上の無効性と入力形式の不正を分離 |
| unit / treatment / outcome / instrument / mediator / time | 変数役割・型・cluster/time単位・介入対比・population |
| estimand_definition / truth | 母集団・complier・時点・局所・条件付き効果等の定義と真値、またはGraph/識別式 |
| oracle_type / derivation / precision | CLOSED_FORM、ALGEBRA、HIGH_PRECISION_QUADRATURE、INDEPENDENT_REFERENCE、GRAPH_ORACLE、MONTE_CARLO_DESIGN。API出力を同じAPIのoracleとしない |
| identification_assumptions | DGP内で真とした因果仮定と、研究者が宣言すべき未観測仮定を区別 |
| inference_contract | None/CI/AR set/graph test/diagnostic等、Method別推論方式と名目水準・pointwise対象 |
| sampling_plan | n、time length、cohort size、seed stream、replicate、resampling unit、条件別強度（後続でfreeze） |
| expected_behavior | EXACT_MATCH / STATISTICAL_AC / REJECT_TYPED / WARN_OR_REVIEW / DIAGNOSTIC_ONLY / NO_DETECTION_GUARANTEE |
| oracle_evidence / execution_evidence | 独立oracle結果と被験Ariadne結果を別hashに保存。現在は未生成 |
| scope_status / approval_ref | 既存/候補/Owner未決の区分、Human採用記録とGate判断の参照 |

**契約上の重要な禁止:** 観測分布から識別不能なexclusion/independence/monotonicityの違反を、常に自動発見する検査にはしない。真値既知の違反DGPを投入し**推定の破綻を研究上評価する試験**と、Designに明示された仮定矛盾を**型付きで拒否する契約試験**を分離する。一般に「negative fixture = 必ず reject」ではない。

**正例の種類:** (A) deterministic/algebraic unit fixture、(B) random finite-sample parity/contract、(C) repeated-sampling statistical fixture、(D) graph-target fixture。有限標本の1回の推定値を母集団真値と完全一致させない。

## 1. 共通DGPカタログ — 明示的な真値

表中の数値は**試験設計の提案値**であり、科学Benchmarkの実行結果ではない。連続乱数の平均0誤差は特記なければ他の外生乱数と独立。SUTVA/consistencyは構成上定義し、標本データだけから実証したとはしない。

| DGP ID | 生成構造（事前登録する形） | 母集団の正解／科学的対象 |
|---|---|---|
| DGP-001 | X~Unif[-1,1], A~Bern(0.5)独立, Y=1+2A+X+ε | RCT。ATE=ATT=2、CATE(x)=2。null変種はDGP-022 |
| DGP-002 | X~Unif[-1,1], e(X)=0.5+0.3X, A~Bern(e(X)), Y=X+2A+ε | Backdoor加法線形。ATE=ATT=2、PS既知、両armの真のpositivity 0.2〜0.8 |
| DGP-003 | DGP-002のYを X+(2+X)A+ε に変更 | CATE(x)=2+x、ATE=2、ATT=2.2。E[X|A=1]=0.2。ATE/ATTは明確に異なる |
| DGP-004 | X,eはDGP-002、Y(0)=sin(πX)+ε、Y(1)=Y(0)+2+X+X² | 非線形CATE(x)=2+x+x²、ATE=7/3、ATT=38/15。選択したxでpointwise評価 |
| DGP-005 | U~N(0,1), A~Bern(logit^-1(U)), M=1.5A+εM, Y=2M+U+εY。UはA,Yの潜在共通原因、A→Y直接効果なし | Frontdoor ATE=3。Frontdoorの非パラメトリック識別と**線形二段階数値法**の成立を別に検証。第2段階の正しい調整条件も固定する |
| DGP-006 | Z~Bern(0.5)が型Sと独立。型S=(always,complier,never)、P=(.25,.50,.25)、A(z)=(1,z,0)、Y(a)=λS+τS a+ε、τS=(0,2,8) | 単調二値IV。ITT_A=.5、ITT_Y=1、Wald=complier LATE=2、母集団ATE=3。λSは任意の型別定数でZ独立 |
| DGP-007 | C,U~独立N(0,1), Z~Bern(.5)独立、A~Bern(logit^-1(-.2+.8Z+.3C+.7U)), Y=1+2A+.5C+U+ε | B1の加法線形構造係数β=2。1 excluded Z/1 endogenous A/処置前C。E[U+ε|Z,C]=0。**本DGPでATE=2でも一般のB1=LATE/ATEは導かない** |
| DGP-008 | X∈{-1,+1}等確率。Z,U独立標準正規、T=(1+.2X)Z+.5U+εT、Y=(2+.5X)T+.3X+.8U+εY | 連続T,Zの条件付きIV構造傾き候補θ(-1)=1.5、θ(+1)=2.5。Cov(Y,Z|X)/Cov(T,Z|X)と一致。**DRIVの正式estimand/momentは未決** |
| DGP-009 | stationary VAR: X_t=.5X_{t-1}+εX_t、Y_t=.4Y_{t-1}+.7X_{t-1}+εY_t | PCMCI用lagged truth: X(-1)→X, Y(-1)→Y, X(-1)→Y。burn-inとCI-test/lagを別固定 |
| DGP-010 | X_t=.5X_{t-1}+εX_t、Y_t=.3Y_{t-1}+.8X_t+εY_t、独立shock | PCMCI+用同時点X_t→Y_tを含むDAG。time-series CPDAGとして識別できる向きは独立Graph oracleで決定 |
| DGP-011 | 潜在H_tと独立shock、X_t=.5X_{t-1}+H_t+εX_t、Y_t=.4Y_{t-1}+H_t+εY_t | LPCMCI／FCIの潜在共通原因。潜在射影および等価類のPAG endpointは**独立Graph oracleの導出待ち**。DAG向きの強制禁止 |
| DGP-012 | G∈{0,1}, t∈{0,1}, Y_it(0)=α_i+λ_t+ε_it、G=1,t=1でのみ+2 | 2×2 DiD ATT=2。parallel untreated trend/no anticipationを構成上満たす |
| DGP-013 | cohort g∈{2,3,never}, t=0..4, Y(0)=α_i+λ_t+ε、t≥gでτ(g,t)=1+(t-g) | Group-time ATT(g,t)=1+(t-g)。Event-time合成真値は**cohort weightとrisk-setを事前指定**して計算 |
| DGP-014 | Y_t(0)=1+.02t+sin(2πt/12)+ε_t (ε_tは定常AR(1))、t≥t0で+2+.1(t-t0) | ITSの介入直後level=2・相対slope=.1。因果解釈は同時ショック無し等に条件付き |
| DGP-015 | R~Unif[-1,1], A=1[R≥0], Y(0)=.5+R+ε、Y(1)=Y(0)+3+.5R | Sharp RD cutoff=0 の局所効果=3。グローバルATEとは区別 |
| DGP-016 | R~Unif[-1,1], Z=1[R≥0]、型S=(always,complier,never)をRと独立にP=(.2,.5,.3)で生成、A(Z)=(1,Z,0)、Y(a)=m_S(R)+τ_S a+ε、τ_complier=3 | Fuzzy RD cutoff=0: treatment jump=.5、outcome jump=1.5、局所complier効果=3。各m_Sはcutoffで連続 |
| DGP-017 | Donor series D2,D3の十分に異なる無介入時系列を生成、treated Y1(0)=.6D2+.4D3、介入後のみ+2 | 理想的SCM。正しいdonor weights=(.6,.4)、処置後効果=2。noiseless基準とnoise付き別variant |
| DGP-018 | Unit×Time panel、Y_it(0)=α_i+λ_t+ℓ_i f_t+ε_it、treated unitsに共通介入後+2。pre periodとcontrol supportを設計 | SDIDの真の対象ATT=2。識別しやすさは因子support・pre-fit・重みのcalibration依存。DGP指定のみで推定器の一致を保証しない |
| DGP-019 | U~N、A~Bern(logit^-1(U))、Y=2A+γU+εY、観測NCE Z=U+εZ、NCO W=U+εW。ZはYに直接作用せず、AはWに作用しない | γ>0でUはA-Y未測定交絡。NCEのY~A+Z条件付き関連は候補診断。NCE帰無のγ=0と、NCO帰無のA~Bern(.5)独立U（Y=2A+γU+εY、W=U+εW）を**別variant**として指定する。元のA~Bern(logit^-1(U))ではNCOのW~A関連が**γ=0でも生じる**ため、A-Y交絡の特異的証拠ではない |
| DGP-020 | 古典OLS係数と残差df、partial R² 2軸を独立referenceへ与える。例: se_classic=.2, df=100, R²_AU=.1, R²_YU=.15 | OVB感度の絶対bias例: .2 sqrt[100×.1×.15/(1-.1)] ≈.25819889。R²軸・df・SE定義はCinelli–Hazlett方式と照合。RVは独立実装/reference待ち |
| DGP-021 | DAG grammar: fork X→A, X→Y, A→Y／mediator A→M→Y／collider A→K←Yの各独立Graph仕様 | Backdoor調整集合の可否／不正なconditioningをgraph-theoretic oracleで判定。Graph単位で混ぜず別variant |
| DGP-022 | DGP-001の介入効果を0へ変更。placebo A*は仕様に従う独立再割付か事前指定shuffle | null効果=0。Placebo/Random CC/Subset/Bootstrapについて対象と再推定分布を別定義 |
| DGP-023 | Discrete X∈{-1,+1}でA=1[X=+1]とする構造的positivity違反、またはDGP-002をe∈{.01,.99}へ変更した近傍variant | 前者はX strataでconditional overlap=0、後者は理論positivity>0だがfinite-sample/ESS不良。両者を同一statusとしない |
| DGP-024 | **AR inversionの代数Oracle**: dY=sample Z群差Y、dA=sample Z群差A、vYY/vAA/vYA=その群差のrobust共分散。q=χ²(1,1-α)、Q(b)=(dY-b dA)^2-q(vYY-2b vYA+b² vAA) | Confidence set={b∈R:Q(b)≤0}。有限、非連結、非有界、全実数の**可能形状**を全実数の二次不等式として判定。Method実行の代替ではなく集合schema/反転計算の独立reference |

### 1.1. Oracleの導出を曖昧にしない例

1. **DGP-003のATT:** X~Unif[-1,1]、e=.5+.3XよりP(A=1)=.5、E[Xe(X)]=.3E[X²]=.1、E[X|A=1]=.2、したがってATT=2.2。ATE=2。
2. **DGP-004のATE/ATT:** E[X²]=1/3、E[X³]=0。ATE=2+1/3=7/3。ATT=2+E[X|A=1]+E[X²|A=1]=2+1/5+1/3=38/15。
3. **DGP-005:** Aの全効果は A→M の1.5とM→Yの2の積で3。U→A,YはBackdoorを破るが、Frontdoor条件を構造上満たす。DoWhy二段階回帰の具体stage調整・実効version・Inference対応を独立に確認する。
4. **DGP-006:** Z=1と0の差はcomplierだけがTreatmentを変えるのでITT_A=.5、ITT_Y=.5×2=1。ratio=2、ATE=.25×0+.5×2+.25×8=3。
5. **DGP-008:** X固定でCov(T,Z|X)=1+.2X、Cov(Y,Z|X)=(2+.5X)(1+.2X)。条件付きratio=2+.5X。これは**候補の構造IV傾き**のoracleであり、DRIV一般モデルの科学的適合性を未承認のまま証明したものではない。
6. **DGP-016:** cutoffの両側でcomplierだけ処置が切り替わるのでjump_A=.5、jump_Y=.5×3=1.5、ratio=3。RDD固有の局所推論を必要とし、DGP-006の無条件Wald ARへ無断転用しない。

### 1.2. AR集合の決定論的Oracle（DGP-024のsubcase）

正の分散・有効な共分散を持つ次の**モーメント入力例**を、q=χ²_1(0.95)として扱う。これは「観測可能なサンプルデータの生成確認済み」ではなく、**二次不等式・JSON集合のunit reference**である。実際のIIDデータから導いた係数・異分散robust covarianceとのパリティは別の統合fixtureで検証する。

| Subcase | (dY,dA,vYY,vAA,vYA) | 期待する集合 |
|---|---|---|
| AR-Q1 | (6,3,1,1,0) | bounded single interval |
| AR-Q2 | (2,0,1,1,0) | disconnected two unbounded rays（q<4） |
| AR-Q3 | (1,sqrt(q),1,1,0) | one unbounded half-line。二次項が厳密に相殺される |
| AR-Q4 | (0,0,1,1,0) | all real。点推定の比は不定でも集合は有効となり得る |
| AR-Q5 | 非PSD共分散、分散零で検定定義不能、NaN/Infinity endpoint | **invalid reference/inference failure**。B0/B1の正常AVAILABLE/EMPTYとして出さない |

**重要な検証:** q依存のnear-tangent係数、浮動小数点根の安定性、有限gridによる端点切断禁止、G2改訂のnull端点／boundedness flag／component sort／union正規化／JSON round-trip、point/inference/scienceの別statusを独立に評価。弱IVなら必ず非有界になる、とは主張しない。ARはexclusion違反を直さない。

## 2. Negative / Stress Fixtureカタログ

列「期待動作」は**拒否の保証／診断／統計的性能／研究上の反証**を分ける。実データに潜む破綻を検出できるという偽のAcceptanceを設けない。

| Stress ID | 基礎DGP・変化 | 期待動作・反証の対象 |
|---|---|---|
| NEG-001 | DGP-001で処置片群のみ、割付Design根拠空欄 | EXPLICIT_INVALIDならREJECT_TYPED。無作為化根拠の申告欠落は識別不可 |
| NEG-002 | DGP-021でcollider Kを調整、媒介Mを総効果の調整に使用 | graph-theoretic拒否または明示review。悪い集合を有効Backdoorと認めない |
| NEG-003 | CPDAG/PAGを入力しDAGに黙って変換／未解決Graphを識別済と表記 | REJECT_TYPED。端点忠実性とD04/E2・D06のfail-closed |
| NEG-004 | DGP-005で媒介M欠落／直接A→Y追加／U→Mを追加 | Frontdoor識別条件の不成立が**宣言Graph上で見える時**拒否。未観測の違反を必ず発見する義務はない |
| NEG-005 | DGP-005のYモデルに非線形M又は効果修飾を追加、元の線形2-stageを適用 | MODEL_MISSPEC_STRESS。bias/RMSEを測定。Graph識別は成立し得るので自動「未識別」としない |
| NEG-006 | DGP-006でcomplier比率0/微小、またはZ群片側欠落 | weak/zero first stageのpointとinference分離。数学的に不定なratioはpoint unavailable。ARは別判定 |
| NEG-007 | DGP-006にZ→Y直接矢印／Z-U相関／defierを追加 | **仮定違反DGP**。Graph/Designに明示した違反はREJECT_TYPED、隠れた違反はNO_DETECTION_GUARANTEE＋bias測定 |
| NEG-008 | DGP-007のCを欠落/後処置変数に変更、Y baselineに未指定非線形項 | B1構造モデル/Design不適格またはmisspec stress。B1係数を一般LATEにラベル変換しない |
| NEG-009 | DGP-008でconditional first-stageを0近傍、Z→Y直接、T/Z型不適合 | DRIV moment/relevance/stressを分離。隠れたexclusion違反は自動検出保証なし |
| NEG-010 | DGP-023のpositivity破綻／near-violation、少数arm | 明示structural support欠落は拒否。極端weightはESS/overlap警告とbias/coverage検証 |
| NEG-011 | DGP-003/004で正しくないPS/outcome nuisanceの組合せ | AIPW/DRLearner等の**Method定義された条件で**nuisance単独正解／双方不正を別評価。『DRだから全条件で正しい』は禁止 |
| NEG-012 | Train/test fold混同、cross-fittingでvalidation label漏洩、same-sample nuisance再利用 | leakage contract違反はREJECT_TYPED、推論歪みは独立反復で評価 |
| NEG-013 | CATE評価xをsupport外に変更／推論設定None／不適合final estimator | point/CI/科学statusを分離、CI=null＋理由。finite CIだけではconfirmatory不可 |
| NEG-014 | DGP-022でPlacebo treatmentを元Aと同じ列に誤指定、又は再割付null不適格 | REJECT_TYPED。placeboの推定対象とnullを誤って構成しない |
| NEG-015 | Data subsetでrare subgroupを消失、残存sample不足 | subset受入不可を理由付き記録。元研究の因果性を保証したとは表示しない |
| NEG-016 | Bootstrapのiid resampleをcluster/timeに適用、seed未保存、nuisance再fit省略 | resampling-unit不適合・再現性失敗。新Inferenceへのbootstrap自動流用禁止 |
| NEG-017 | Random Common Causeを実際の未観測交絡補正と称する、又はrandom変数がconstant | 誤意味label・degenerate perturbation拒否 |
| NEG-018 | Propensity clippingの閾値・weight定義変更、対象母集団の誤表示 | weight/ESS/trimmingとtargetの差分を監査。clippingだけでbiasが改善する保証はない |
| NEG-019 | DGP-019のNCEでZ→Y直接経路を追加、NCOでA→Wを追加、null/conditioning根拠無し | 明示違反は不適格。非棄却を「無交絡PASS」にしない。γ=0でもNCO-W~A関連があり得る |
| NEG-020 | DGP-020でHC3 SEをclassic SEと誤表示、partial R²∉[0,1)、指定外IPW/AIPWへ適用 | REJECT_TYPED。感度grid/benchmark/reference versionを固定 |
| NEG-021 | DGP-009〜011で重複timestamp、欠測、非定常、CI-test misspec、PAG endpointの強制DAG化 | machine validation可能なものだけ拒否。stationarityの統計判定は仮定成立の証明ではない |
| NEG-022 | DGP-012/013でparallel trends破綻、no anticipation違反、staggered TWFE contaminated | known-truth bias/stress、宣言矛盾時だけreject。pretrend非有意で平行性証明としない |
| NEG-023 | DGP-014〜016で同時介入、cutoff manipulation、mass points、弱いRD first-stage、悪いbandwidth | Design診断＋局所効果・SEのstress。density-test無棄却を完全保証としない |
| NEG-024 | DGP-017/018でpost donor汚染、poor prefit、donor support不足、unit/time weight混同 | SCM/SDID対象のbias、pre-fit/ESS、placebo診断、targetとCIの誤解釈防止 |
| NEG-025 | DGP-024で有限grid切断、AR-Q2を単一区間化、AR-Q4をEMPTY化、非PSD共分散 | Lossless confidence set/typed failure。Wald通常CIを弱IV頑健と表示しない |
| NEG-026 | DGP-019のγ=0だがU→A,Wは維持（NCOの偽警告stress）、又はNCE/NCO未指定 | NCO関連≠A-Y交絡の論理的証明。NCO null-size評価はAがUと独立の別variantで行い、未指定のopt-in診断を自動実行しない |
| NEG-027 | 未承認Identification、Question/Graph/Design/Dataset hash mismatch、旧v2 override | 新E11はREJECT_TYPED。旧Product/v2の独立回帰は現行挙動を保護 |
| NEG-028 | GraphVersion再固定時に親を改変、編集根拠なし、又は旧PAG矢印を欠損 | REJECT_TYPED／レビュー。元Graphを不変保存し、新識別を要求 |

## 3. Method×Fixture Coverage — 41/41（Draft）

**列の読み方:** 各行には少なくとも1つの正例DGPと1つのnegative/stress、そして期待する科学的判定がある。複数Methodで同じDGPを使ってもMetric/Estimand/Gate evidenceは独立に保持する。

### 3.1. Phase1（20 Method）

| SR04 Method ID | Positive DGP / oracle | Stress ID | このMethod固有の主assertion |
|---|---|---|---|
| P1-M01 Randomized ID | DGP-001 / assignment design | NEG-001,027 | ATEのID式とDesign evidence、非適格のtyped拒否 |
| P1-M02 Native Backdoor ID | DGP-002,021 / DAG adjustment | NEG-002,003 | valid adjustmentとcollider/mediator禁止 |
| P1-M03 DoWhy Backdoor ID | DGP-002,021 / independent graph oracle | NEG-002,027 | Native/DoWhy式の意味パリティ、backend success≠valid ID |
| P1-M04 DoWhy Frontdoor ID | DGP-005 / FD criterion | NEG-004 | Frontdoor IDとYのATE=3。数値推定は別case |
| P1-M05 DoWhy IV ID | DGP-006 / IV candidate & ITT | NEG-006,007 | IV式と識別対象のlabelを分離、LATE自動認定禁止 |
| P1-M06 FCI PAG | DGP-011,021 / independent PAG oracle **PENDING** | NEG-003,021,028 | adjacency/endpoint/calibration、circle保持 |
| P1-M07 Frontdoor estimator | DGP-005 / ATE=3 / linear-stage reference **PENDING** | NEG-004,005 | 追加線形仮定下bias/coverage（CI Method未定） |
| P1-M08 diff-in-means | DGP-001 / ATE=2、DGP-022 / null=0 | NEG-001,010 | 群別平均差・推論の参照一致 |
| P1-M09 OLS | DGP-002 / β=2、DGP-003 / total targetを別審査 | NEG-002,008,020 | additive model正解とeffect heterogeneity誤label拒否 |
| P1-M10 IPW | DGP-002,003 / ATE=2、ATT=2.2 | NEG-010,018 | estimand別weight、ESS、estimated-PS込み推論 |
| P1-M11 AIPW | DGP-002,003 / truth & nuisance oracle | NEG-010,011,012 | 単独nuisance正解時DR挙動、ATE/ATTの別式 |
| P1-M12 Placebo | DGP-022 / null=0 | NEG-014 | placebo null、再推定可否、Type-Iの方法別確認 |
| P1-M13 Data subset | DGP-001,002 / stable truth | NEG-015 | resample単位/seed/target population consistency |
| P1-M14 Random Common Cause | DGP-002 / independent noise variable | NEG-017 | 摂動の再現と真のNC/未観測交絡との意味分離 |
| P1-M15 Bootstrap refutation | DGP-001,002 / repeat-sample reference | NEG-016 | iid前提／resampling validity／run repeatability |
| P1-M16 Adjustment set sensitivity | DGP-021,002 / graph-valid sets | NEG-002 | 候補集合は有効Graph上でのみ感度比較 |
| P1-M17 PS clipping sensitivity | DGP-002,023 / known PS | NEG-010,018 | clipping/trim/target変化、ESSとbias |
| P1-M18 NCE null diagnostic **scope pending** | DGP-019 / γ=0帰無とγ>0対立のY~A+Z | NEG-019,026 | 対照妥当性とnullのsize/powerを別判定 |
| P1-M19 NCO null diagnostic **scope pending** | DGP-019 / NCO帰無の無作為割付variantとW~A対立variant | NEG-019,026 | Null下sizeとU→A,W下power、A→W不存在、特異性欠如を別々に確認 |
| P1-M20 partial R²/RV **scope pending** | DGP-020 / OVB closed-form | NEG-020 | partial-R² grid/parity、classic SEのみ |

### 3.2. Phase2（8 Method）

| SR04 Method ID | Positive DGP / oracle | Stress ID | このMethod固有の主assertion |
|---|---|---|---|
| P2-M01 LinearDML | DGP-003 / CATE(x)=2+x | NEG-011,012,013 | nuisance/crossfit、linear final、fixed-x pointwise CI |
| P2-M02 CausalForestDML | DGP-004 / CATE(x)=2+x+x² | NEG-010,012,013 | nonlinear CATE、forest推論とpointwise coverage |
| P2-M03 DRLearner | DGP-003,004 / conditional truth | NEG-011,012,013 | DR pseudo-outcome、final-model-specific inference |
| P2-M04 ForestDRLearner | DGP-004 / conditional truth | NEG-010,011,013 | forest DR条件とMethod-specific interval |
| P2-M05 S-Learner | DGP-002,003 / constant/linear effect | NEG-010,012,013 | treatment feature、shrinkage bias、bootstrap条件 |
| P2-M06 T-Learner | DGP-003,004 / arm-specific oracle | NEG-010,013 | arm-specific supportとeffect差、CI未対応時null |
| P2-M07 X-Learner | DGP-003,004 / pseudo-outcome oracle | NEG-011,012,013 | imbalance weightingとpseudo-outcome漏洩 |
| P2-M08 DRIV | DGP-008 / θ_IV(-1)=1.5, θ_IV(+1)=2.5 **provisional target** | NEG-009,012,013 | continuous IV moment/estimand適合、LATE/CATEへ自動rename禁止 |

### 3.3. Phase3（13 Method）

| SR04 Method ID | Positive DGP / oracle | Stress ID | このMethod固有の主assertion |
|---|---|---|---|
| P3-M01 PCMCI | DGP-009 / lag graph | NEG-021 | lag parent recovery、CI test、time order |
| P3-M02 PCMCI+ | DGP-009,010 / contemporaneous CPDAG **oracle pending** | NEG-021,028 | lag+同時点の未確定向きの忠実保持 |
| P3-M03 LPCMCI | DGP-011 / temporal PAG **oracle pending** | NEG-021,028 | latent common cause/endpoint fidelity |
| P3-M04 DiD | DGP-012 / ATT=2、DGP-013 / ATT(g,t) | NEG-022 | parallel trends、cohort-time target、cluster inference |
| P3-M05 Event Study | DGP-013 / τ(g,t) dynamic | NEG-022 | event-time aggregate weights固定、TWFE contamination |
| P3-M06 ITS | DGP-014 / level=2,slope=.1 | NEG-023 | seasonal trend/HAC/autocorrelation・同時介入 |
| P3-M07 Sharp RDD | DGP-015 / local jump=3 | NEG-023 | cutoff/bandwidth/local estimand/density diagnosis |
| P3-M08 Fuzzy RDD | DGP-016 / local LATE=3 | NEG-006,023 | first-stage jump=.5、局所IV推論は独立検証 |
| P3-M09 Wald ratio | DGP-006 / complier LATE=2,ATE=3 | NEG-006,007 | population/complier label、zero denom、weak-IV inference分離 |
| P3-M10 B0 just-ID 2SLS | DGP-006 / sample Wald exact parity, AR-Q1..4 | NEG-006,025 | 同一sample点の代数パリティ＋AR集合lossless |
| P3-M11 B1 linear IV 2SLS | DGP-007 / β=2、AR-Q1..4 algebra oracle | NEG-008,025 | covariate residualization、未決Estimand enum、AR robust inference |
| P3-M12 Synthetic Control | DGP-017 / w=(.6,.4)、post effect=2 | NEG-024 | pre-fit, non-contaminated donors, placeboとCIの区別 |
| P3-M13 Synthetic DiD | DGP-018 / panel ATT=2 | NEG-024 | unit/time weight混同防止、panel target、依存構造 |

**Coverage上の注意:** P1-M05はDoWhyによるIV識別候補であり、P3-M09〜11のMethodをAPI呼び出し可能というだけで適格化しない。P1-M07のFrontdoor ATEはP1-M04の識別だけでは合格しない。P3-M08は局所RD/IVであり、無条件WaldのAR分布を無審査で継承しない。P2-M08はD03のCではない。

## 4. CATE・DRIV・B1の残余研究仕様

### 4.1. B1：構造係数とLATEを分離

**採用済:** B1は二値Z/A、処置前共変量C、切片あり、単一excluded Z・単一endogenous A、加法線形構造モデル。初期ARは独立単位＋異分散頑健漸近。正式Estimand分類と因果的interpretationの境界は未決。

- DGP-007は科学的に適格な**同質構造効果β=2**の確認用。この特殊DGPではATE等も2となるが、等価性を一般法則としてコード化しない。
- B1異質性stress: C別に効果θ(C)とZ→A first-stageを変化させる。母集団ATE、LATE、線形射影2SLSのpseudo-true targetを**別の式・独立数値積分**で算出するまでは「既知真値B1」の正例にしない。
- B1 ARの検定式、residualization/covariance、inversionの数値分岐は別oracleでfreeze。DGP-024は集合算術unit専用であり、B1の完全AR coverageを証明しない。
- **承認待ち:** estimand_kindのenum/target definition、Cの適格性、必要なexogeneityの形式、Model misspec時の対象status。

### 4.2. DRIV：構造IV候補DGPを正式Estimandと混同しない

- DGP-008の条件付きmoment候補は E[(Z-E[Z|X]){Y-E[Y|X]-θ(X)(T-E[T|X])}|X]=0。ここでθ(X)=2+.5X。
- このDGPは連続T/Zでの**構造的単位Treatment傾き**を定義し、二値Z/Aのcomplier LATEを定義しない。Xを固定した構造効果が、全非IV CATE契約と一般に等しいという主張でもない。
- **未決:** DRIVのestimand definition、nuisance条件、IV moment、discrete_treatment/instrumentの対応表、final projectionの重み、inference availability。EconMLの特定final modelが条件付きtargetを厳密に回復するかは、採用versionと設定に依存する。
- 受入はAPI smoke→独立moment oracle→bias/coverage→negative stressの順で進め、探索的point-onlyと確認的interval-requiredを別判定する。

### 4.3. CATEの固定評価点とInference

DGP-003ではx=(-.75,0,+.75)を**事前指定候補**とし、truth=(1.25,2,2.75)。DGP-004では同じxでtruth=(1.8125,2,3.3125)。区間対象はこの3点におけるpointwise CATEであり、全x同時confidence bandではない。支持域、処置arm、nuisance/forest/bootstrapの推論適格性をmethod-specificに固定する。

DRLearnerとS/T/X-LearnerでBootstrapInferenceによるfinite CI APIが観測されたことは、名目coverage成立の証拠ではない。旧probeの12反復を科学的な最小反復数として採用しない。

## 5. Scientific Benchmark Protocol（策定範囲と未決）

### 5.1. 試験の階層

| Level | 目的 | 必要な独立性と結果 |
|---|---|---|
| F0 Schema/unit | Case ID、Graph endpoint、DGP-024の集合、hash、reason enum | deterministic、exact/algebraic match。統計的誤差を持ち込まない |
| F1 Numerical integration | 正しいdatasetに対するMethod別推定値／seed／参照式 | 真値＋数値比較。外部Libraryの出力を唯一のreferenceにしない |
| F2 Scientific Monte Carlo | 反復DGPのbias/RMSE/Type-I/coverage/power/Graph FPR | replicateとseed stream固定、失敗率を分母ごと報告 |
| F3 Contract negative | 非適格とwarning/reviewの科学的理由、誤label、防止すべきエスカレーション | 機械検証可能なinvalid入力にREJECT_TYPED。隠れた違反は自動検出要求しない |
| F4 Product/v2 regression | D04 R2 legacy preserve＋version dispatch | 既存動作とのcompatible regression、新E11 fail-closedを分離 |

### 5.2. 定量評価定義

- Point estimator: bias=mean(estimate-truth)、RMSE=sqrt[mean((estimate-truth)^2)]、nonfinite/unavailable率、条件付きX/estimandの誤label率。ATE/ATT/CATE/LATE/ATT(g,t)/RD/SCM targetは別母集団を固定する。
- CI: 名目1-αと真値との包含率、失敗を除いた条件付きcoverageと、**全replicateを分母としたinference availability**を併記。MCSE=sqrt[p_hat(1-p_hat)/R]。nominal−observedの実質差の閾値とMonte Carlo測定誤差を混同しない。
- AR Confidence Set: truth∈set の包含率を**無界・非連結・全実数を含めて**判定。setの型、有限grid検査、端点/sectionの正規化、ratio point unavailableと推論availabilityの独立性を記録。
- Graph: adjacency FPR/TPR, endpoint error, lag recall/false edge, alpha/CI-test calibration。PAG/CPDAG oracleが未確定なら方向AccuracyのPASSを出さない。
- Refutation/NC: 配布されたnullのType-Iと対立下power、反復変換法、統計検定の対象・conditioning set。妥当なnegative control無しの研究で自動実行しない。
- Quasi: observation unit/cluster/timeで標本設計、pre-period・cohort/time/cutoff support、placebo/nullの実験単位、設計別分散。iid bootstrapを汎用にしない。
- Sensitivity: 独立計算式パリティ、input domain、classic SEとHC3の区別、grid/RVのreference値。誤用に反応するtyped failure。
- Scientific gateの最終値は**Method×DGP難度×n×inference配置**ごとに事前固定。単一の恣意的bias/coverage cutoffを全Methodへ課さない。

### 5.3. 実行条件（未freeze）

| Parameter | 仕様候補／現状態 |
|---|---|
| Python / OS | owner既採用基準＝Python3.12／Linux。実際のpatch version、CPUとBLAS/thread、library lockは未freeze |
| Backend | DoWhy、EconML、TigramiteはMethod別optional。SR-02で0.14/0.17.0/5.2.10.1 API smoke済み、科学的受入と同一ではない |
| DGP parameter & truth | DGP-001〜024は初期候補。上記数値/式は**策定案**。oracle独立実装・丸め規則・計算精度のreviewが必要 |
| sample n / panel size / burn-in | method-specific、低/中/高support・weak-IV・不均衡の複数水準を含め後続決定。ここで数値freezeしない |
| Monte Carlo R / seed | 事前にundercoverage等の最小検出差とMCSEから決定。seed listとtrain/test splitは分析本体から独立にfreeze |
| nominal α | 候補0.05。確認的推論level・familywise vs pointwise・検定の参照分布は正式承認待ち |
| Reference | 数式導出＋独立数値oracle＋必要時外部reference実装。Reference実装のバージョン/ハッシュを保存 |
| Negative controls | 機能原則は採用済、具体NCE/NCO MethodはScope未承認。nullの正当化・Design graph・opt-in必須 |
| Distribution/license | Methodごとの依存versionと別にTigramite使用の顧客SI納入GPLv3審査が必要 |

## 6. 横断Contract Case（SR04 Matrix X-01〜X-09）

| ID | 固定入力／反例 | 最小期待結果 |
|---|---|---|
| X-01 | 同一Question/Estimandの有効E11 schemaとinvalid v2混在 | version dispatch、Model role/contrast、legacy不変 |
| X-02 | DGP-021 valid DAGとDGP-011未解決PAG、識別Result/EstimatorSpec mismatch | new CLI gate fail-closed。Graphの型からIDENTIFIEDを偽造しない |
| X-03 | DGP-011 PAGのserialize/readback→研究者DAG refix | endpoint fidelity、元Graph不変、parent/rationale、新Graph hash、再識別 |
| X-04 | DGP-024 AR-Q1〜Q5とCATEのCIなし結果 | confidence_setとconfidence_interval分離、null＋reason、lossless union |
| X-05 | 同一DGP/seed/configで再実行、Dataset/Question/Graph hash改ざん | byte/hash/manifest lineage trace、mis-match拒否、backend実効versionを明示 |
| X-06 | 個票CATE artifact path traversal、権限なし出力、正当Parquet readback | unsafe拒否、安全なlocal file/atomic write/checksum/privacy規則 |
| X-07 | DoWhy/EconML/Tigramiteのoptional module欠落・version不整合 | method specific unavailable、別Methodの可用性は保護。GPLv3顧客配布は別承認 |
| X-08 | 旧Product/v2 REQUIRES_REVIEW+overrideケースと新E11拒否ケース | 旧回帰保持、新E11に旧overrideが横流しされない |
| X-09 | 68 Scope各行のMethod・横断・後続のDispositionと41 Method行 | 無応答行／二重scope/承認済み偽装を検出。FR/NFR/AR/Issue/Gateのtrace先を固定 |

## 7. Referenceと一次資料

- [SR-03のEstimand・識別相関表](20261101_sr03_identification_estimand_estimator_contract_review.md)、[D03 AR/2SLS/G2](20261101_sr03_d03_remaining_2sls_weak_iv_review.md)、[D05 CATE/DRIV](20261115_sr03_d05_cate_driv_inference_scientific_contract_decision.md)、[D06 Graph uncertainty](20261115_sr03_d06_graph_uncertainty_identification_override_decision.md)。
- [EconML DRIV API](https://econml.azurewebsites.net/_autosummary/econml.iv.dr.DRIV.html) — 連続/離散T,Zと条件付き対象、final projection・inference options。採用候補0.17.0で実効signatureを再検証。
- [DoWhy TwoStageRegressionEstimator公式API](https://www.pywhy.org/dowhy/main/dowhy.causal_estimators.html) — Frontdoor二段階線形法。採用候補0.14でstage仕様を確認。
- [Tigramite公式方法と条件](https://jakobrunge.github.io/tigramite/index.html) — PCMCI/PCMCI+/LPCMCIとCI test。
- [Imbens & Angrist (1994), LATE](https://www.gsb.stanford.edu/faculty-research/publications/identification-estimation-local-average-treatment-effects) — binary IVのcomplier対象。
- [Davidson & MacKinnon (2014), AR confidence sets](https://academic.oup.com/ectj/article/17/2/S39/5056440) — AR集合の非空性と弱IV。
- [Callaway & Sant'Anna (2021), multiple-period DiD](https://doi.org/10.1016/j.jeconom.2020.12.001)／[Sun & Abraham (2021), event study](https://doi.org/10.1016/j.jeconom.2020.09.006)。
- [Cinelli & Hazlett (2020), Making Sense of Sensitivity](https://doi.org/10.1111/rssb.12348) — partial R²/Omitted Variable Bias/RVの定義。実数値パリティを別実装で確認する。
- [Abadie, Diamond, Hainmueller (2010), Synthetic Control](https://doi.org/10.1198/jasa.2009.ap08746)／[Arkhangelsky et al. (2021), Synthetic DiD](https://doi.org/10.1257/aer.20190159)。

## 8. 対象全件カバレッジ・未決と次工程

**Draft完了条件:** 41 MethodすべてをDGP/負例/科学assertionへマッピング、DGPごとの真値・oracle型を列挙、前提違反と契約不備を区分、SR-03未決を未決として残し、SR-04/Gate07の検証プロトコル・横断Caseへ追跡できること。

**未完（実装・科学受入前の必須作業）:**
1. **SR03-R01:** B1正式Estimand kind/表現、どの仮定で何の対象となるかを確定し、DGP-007以外の異質性反例のoracle式を独立に導出。
2. **SR03-R02:** DRIVのMethod-specific conditional moment・型・projectionと対応するestimand、DGP-008の採用可否を科学review。
3. **SR04-C:** 独立reference/oracle、特にFrontdoor二段階、FCI/LPCMCI PAG endpoints、B1 AR、DRIV、RDD/SDIDの適用範囲。
4. **SR04-D:** n/R/seed、bias/RMSE/coverage/Type-I/power/graph accuracyの定量許容基準を事前freeze。
5. **SR04-E/F:** 実効依存lock/再現環境/リソース管理、実装前Contractの型、41 Method＋9横断ケース→FR/Issue/Gate07のTraceability。
6. **並行の正式承認:** SR-01〜12の残余、68行Scope、NCE/NCO/RV候補のOwner採否、FR/NFR/AR、Architecture Review、承認Snapshot SHA。未完ならGate/Codingに進めない。

**明示的に未実施:** 本catalogに基づくDGP generatorの作成、EconML/DoWhy/Tigramite実行、pytest、Monte Carlo、数値Reference実行、Result/Manifest変更、Product DB/UI/Worker変更、Gate07 Science PASS、正式要件への反映。
