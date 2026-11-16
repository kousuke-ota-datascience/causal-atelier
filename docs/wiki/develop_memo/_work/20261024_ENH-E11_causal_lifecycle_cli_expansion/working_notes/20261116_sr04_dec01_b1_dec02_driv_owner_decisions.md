# ENH-E11 — DEC-SR04-01（B1-A）／DEC-SR04-02（DRIV-A）正式個別判断・科学的境界

**文書区分:** Human owner の個別設計判断に対応する独立技術記録。**全体構想・FR/NFR/AR・Architecture Decision・Gate06/07・Coding・Method Science PASSではない。**  
**判断日:** 2026-11-16（JST）。  
**判断主体:** Human owner。本ターンで「DEC-SR04-01（B1-A）とDEC-SR04-02（DRIV-A）の正式判断を実行」と指示された範囲に限って、統合レビューで推奨した**B1-A／DRIV-Aを採用**する。  
**個別判断状態:** \`DEC-SR04-01_B1-A_OWNER_ACCEPTED / DEC-SR04-02_DRIV-A_OWNER_ACCEPTED / SCIENTIFIC_IMPLEMENTATION_PENDING / INFERENCE_VALIDATION_PENDING / GATE07_NOT_FROZEN\`。  
**全体状態:** \`PENDING_FULL_CONCEPT_APPROVAL\`。正式schema enum/version、Method runtime configuration、認定された推論手順・独立数値Reference・Benchmark・Gateは未確定。  
**正本の責務分離:** 個別判断の採用事実は[02_enhancement_concept_approval_record.md](../00_enhance_background/02_enhancement_concept_approval_record.md)に追記。本書は選択肢比較・数式・科学的限界・負例/受入依存を保持。旧SR03 D01/D03/D04/D05/D06のOwner採用方針を変更しない。

## 0. 決定サマリー

| Decision | 採用案 | 決定する科学的意味 | 意図的に承認しないこと |
|---|---|---|---|
| **DEC-SR04-01：B1-A** | **採用** | 事前指定した処置前共変量 C を持つ、単一二値Z/A・just-identified**加法線形IV構造係数** \`β\`。均質処置係数と外生性・正しい線形baselineの根拠が必須 | 一般ATE/ATT/二値IV LATE/CLATEへの自動分類、異質性下の線形射影を同一Estimandとして承認、複数IVやcluster/HAC、正式Enum・2SLS/AR coverage |
| **DEC-SR04-02：DRIV-A** | **採用** | \`IV_HETEROGENEOUS_EFFECT\` familyに属する、部分線形構造の条件付き処置**斜率** \`θ_IV(x)\`。連続T/Zの条件付きIV momentと処置コントラストを明記 | 全Backend設定が同じθを推定する保証、最終学習器のミススペックによる射影を構造効果と表示、complier LATEや非IV CATEへの無審査同一視、0.17.0 runtime/CI/Science PASS |

**決定対象は「何を推定したいか／その対象を表現する契約」であり、Estimatorの利用可能性や統計的有効性の宣言ではない。** 両MethodをScopeから外さず、先行SR03の採用を実質変更しない。

## 1. DEC-SR04-01 — B1-A

### 1.1. 選択肢比較と判断理由

| 案 | 内容 | 採否 | 根拠 |
|---|---|---|---|
| **B1-A** | 均質な**加法線形構造係数β**を正式な科学的対象とする | **採用** | SR03-D03-1のS2／B0＋B1採用範囲に合致。対象・外生仮定・2SLSとARの対象が明瞭 |
| B1-B | 異質効果下でも残差化IV比（線形射影）を公開Estimandとする | **初期非採用** | 残差化IV係数を一般のATEやcomplier LATEとして解釈できず、作用の非負加重平均すら別証明が必要。数学的referenceとしては残す |
| B1-C | 条件付きcomplier LATE・効率的IV/DRを当初から必須化 | **非採用** | SR03-D03-4 C1で条件付きIV向けCを初期非採用とした判断に抵触 |

### 1.2. 科学的Estimand／識別／推定器の契約（採用）

**Observation:** IID個体 \`i\`、\`Z_i∈{0,1}\`（単一excluded IV）、\`A_i∈{0,1}\`（単一内生処置）、\`C_i\`（事前指定の処置前共変量；外生・full-rank）。一つの観測\`Y_i\`。

**構造式（対象を定義）**

\[
Y_i=\alpha+\beta A_i+\gamma^\top C_i+\varepsilon_i.
\]

**科学的条件:** 一貫性、IV独立性/除外、構造式の正しい線形baseline、均質な\`β\`、\`C\`が処置後変数・colliderではないこと、単一IVの関連性・rank、IID観測と適格なsupport。採用候補の強いIV外生性表現 \(\mathrm E[\varepsilon\mid Z,C]=0\) は十分条件。2SLSが実際に使う最小必要モーメントは\(\mathrm E[W\varepsilon]=0\)、\(\mathrm E[Z\varepsilon]=0\)（\`W=(1,C)\`）である。**このモーメントの存在はデータから外生性・除外を証明するものではない**。

**母集団Target:** \(M_W Z=Z-\Pi_W Z\) を\`Z\`の\`W\`空間への母集団線形射影残差とし、

\[
\beta_{\mathrm{IV,lin}}
=\frac{\mathrm E[(Z-\Pi_W Z)Y]}
       {\mathrm E[(Z-\Pi_W Z)A]}
=\beta
\]

（真の構造式・IVモーメント・分母非零の場合）。

**固定標本の数値Reference:**

\[
\widehat\beta_{\mathrm{2SLS}}
=\frac{\widetilde Z^\top\widetilde Y}
       {\widetilde Z^\top\widetilde A},
\quad \widetilde V=M_W V,\quad M_W=I-W(W^\top W)^{-1}W^\top.
\]

rank/数値条件は必須。推奨する行列演算は逆行列の明示計算ではなくQR/SVDによる残差化。B0の未調整Waldとの点推定一致をB1に要求しない。

**semantic kind（今回採用）:** \`LINEAR_IV_STRUCTURAL_COEFFICIENT\`を**科学的意味の識別子**として採用。これは正式CLI/schemaのenum値・field名・version番号を発行する決定ではない。A/B間の対照、対象母集団、単位、時間、Instrument、調整共変量、処置差をResultで記録する。B1から\`ATE\`/\`ATT\`/\`LATE\`/\`CLATE\`への自動変換を禁止。定数の潜在処置効果を追加で正当化できる場合に限りATE等と数値が等しくなり得るが、**数値一致とResultの意味論的再分類を区別する**。

**推論:** 先行SR03-D03 I2/G2のOwner採用を保持。B1はheteroskedasticity-robust asymptotic AR confidence-set inversionを初期基準とし、bounded/unbounded/disconnected/all-real集合をlossless保存、正常just-IDでEMPTYを禁止。HC0/HC1、first-stage、critical value、endpoint精度、coverage等は\`REF-U01\`／SR04-Dの独立科学検証待ち。Cluster/HAC、複数IV、連続A、非線形や異質処置効果は初期保証外。

### 1.3. 反証：残差化IV比 ≠ ATE（異質性の正例禁止）

**構造的な負例（検証設計に採用、現物コード未作成）:** \`C∈{0,1}\` 等確率、\`Z∼Bern(0.5)\`は独立。群C=0はZ=1のとき全員処置、C=1は確率1/4だけcomplier（他はnever）。潜在処置効果を\(\tau(C=0)=1,\tau(C=1)=3\)とし、除外・IV割付独立・単調性が成立している。

- 母集団ATEは \((1+3)/2=2\)。
- 残差化Instrumentと処置の共分散は群間relevanceに比例。**IV比は**
\[
\beta_{\mathrm{IV,lin}}
=\frac{0.5\cdot 1\cdot 1+0.5\cdot 0.25\cdot 3}
{0.5\cdot 1+0.5\cdot0.25}
=1.4.
\]

このIV比はこの単調・ランダム割付の特殊構成ではcomplier効果へ解釈可能だが、**採用したB1-Aの「一定β」という構造モデルは偽**。Methodが\`ATE=1.4\`と認定してはならない。元DGP-007の正例（β=2）と別の\`DGP-007-HET\`**variant候補**として、正式Fixture version化・科学レビューを待つ。

### 1.4. B1-Aの受入に残る依存

\`P3-M11\`／\`DGP-007\`／\`DGP-024\`／\`NEG-008,NEG-025\`／\`REF-E08,U01\`／\`AC-D03,P01,P03,A01〜A05,I01,I02\`。独立2SLS実装・AR集合の代数とiid生成sampleとのパリティ、強/弱IV下のcoverage、C指定誤り・異質性下でのステータス処理を実証。**Owner判断解消、Science/Inference Blocker維持**。

## 2. DEC-SR04-02 — DRIV-A

### 2.1. 選択肢比較と判断理由

| 案 | 内容 | 採否 | 根拠 |
|---|---|---|---|
| **DRIV-A** | 条件付きIV構造斜率\(\theta_{\rm IV}(x)\)を対象とする | **採用** | SR03-D01の独立\`IV_HETEROGENEOUS_EFFECT\` family、D05のMethod-specific契約と整合。母集団の既知真値を設定可能 |
| DRIV-B | 実際の最終Estimatorへの重み付き射影を正式対象にする | **初期非採用** | 最終学習器/重み付け/Backend versionで推定対象が変わる。設計QuestionのTargetを推定結果に後付けしやすい |
| DRIV-C | 二値IVのcomplier CLATE/LATEへ一律に同一視する | **非採用** | 連続Treatment/Instrumentの初期Scientific DGPと異なり、SR03-D01の分類を損なう |

### 2.2. Scientific Target／モーメント（採用）

**Observation:** IID \((Y,T,Z,X,W)\)。初期の**Science-positive fixture**は連続・単一スカラーTreatment \`T\`、連続・単一スカラーInstrument \`Z\`、効果修飾子\`X\`、外生共変量\`W\`を必要なら指定する。\`W\`は処置前・IV妥当性を損なわないものに限定。観測単位・対象母集団・\`T0→T1\`のコントラストを別記録。

**構造的に解釈可能なモデルの一例:**

\[
Y = \theta_{\mathrm{IV}}(X)T + h(X,W)+U,
\]

ただし\`Z\`が\`U\`に対する有効Instrumentであり、\(\theta_{\mathrm{IV}}(x)\)が同じ\`X=x\`の対象集団における\`T\`への構造斜率となるよう、外生性・除外・関連性・支持域・構造的線形性を要求する。**\(W\)内で異質な処置斜率を許す場合の比の重みづけ対象を、同じ\(\theta(X)\)と無審査同一視しない。**

\(m_V(X,W)=\mathrm E[V\mid X,W]\)、\(\widetilde V=V-m_V(X,W)\)に対し、**採用する条件付きIV識別モーメント**は

\[
\mathrm E[\widetilde Z
  \{\widetilde Y-\theta_{\mathrm{IV}}(X)\widetilde T\}
  \mid X=x]=0,
\]

そして

\[
\theta_{\mathrm{IV}}(x)
=
\frac{\mathrm E[\widetilde Z\widetilde Y\mid X=x]}
{\mathrm E[\widetilde Z\widetilde T\mid X=x]},
\qquad
\left|\mathrm E[\widetilde Z\widetilde T\mid X=x]\right|>0.
\]

**注意:** 上式は\`X,W\`で残差化した条件付きモーメントに対する**科学的Target契約**である。\`W\`を明示したとき、単純な\(\mathrm{Cov}(Y,Z\mid X=x)/\mathrm{Cov}(T,Z\mid X=x)\)に一般には等しくない。\`W=∅\`ならその単純ratioへ還元する。**DRIV内部のorthogonal/doubly-robust pseudo-outcome、covariance clipping、cross-fittingと同じものだという意味ではない**。実効Backendの推定式とTargetが一致するかは別のvalidation gateとする。

**Treatment contrast:** 構造的に線形なdose responseの条件下で、\(\mathrm{Effect}(x;T_0,T_1)=\theta_{\mathrm{IV}}(x)(T_1-T_0)\)。固定した\`T1-T0\`を明記しないままbinary treatment effect/ATEに改名しない。初期基準の例は単位増分\(\Delta T=1\)（数式Reference上）、単位・範囲・外挿支持域を明示。

**semantic kind（今回採用）:** family=\`IV_HETEROGENEOUS_EFFECT\`、具体Target=\`CONDITIONAL_IV_STRUCTURAL_SLOPE\`。これらは**科学的な識別子**。具体的なCLI/schema \`estimand_kind\` Enum/Result版・Field配置はD04/Architecture Review待ち。

### 2.3. DRIVのBaseline FixtureとBackendの区別

**DGP-008（Ownerが採用したScientific Targetの限定正例）:**

\[
X\in\{-1,1\},\quad Z,U\sim N(0,1)\ {\rm independent},
\]
\[
T=(1+0.2X)Z+0.5U+\varepsilon_T,\qquad
Y=(2+0.5X)T+0.3X+0.8U+\varepsilon_Y.
\]

\`W=∅\`、\`Z\`は\`U\`/shockと独立。従って
\(\theta_{\rm IV}(-1)=1.5\)、\(\theta_{\rm IV}(+1)=2.5\)。
**X=0やCATE7の\`x=-0.75,0,+0.75\`はsupport外**。初期Science-positiveの点評価は\`x=-1,+1\`のみ。

**EconMLの構成と推定Targetを分離する:** 現在公開されているDRIV公式APIには\`model_final\`、\`fit_cate_intercept\`、\`projection\`、\`opt_reweighted\`、\`fit_cov_directly\`、\`cov_clip\`、\`cv\`、\`discrete_treatment/instrument\`等が存在する。\`projection=True\`でZの代わりに\(\mathrm E[T\mid X,W,Z]\)を利用する変法になり、\`opt_reweighted\`は最終モデルの重み付け・射影を変更し得る。切片を表現できない\`model_final\`は真値\(\theta(x)=2+0.5x\)を表現できない。**これらは設定候補であって、EconML 0.17.0の該当Configの実効適合性・推論の科学的受入を意味しない。**

**初期に検証するConfig候補（未freeze）:** continuous T/Z（\`discrete_treatment=False\`, \`discrete_instrument=False\`）、\`projection=False\`、\`opt_reweighted=False\`、切片+Xの効果を表現する\`fit_cate_intercept\`/\`model_final\`、\`cov_clip\`値・nuisance/crossfit/CI inferenceを固定。**\`W\`を入れた構成は、このconditional-momentと利用可能なBackend nuisanceが適格かを別のDGP/Referenceで確認してからScience-positiveにする。** 非線形effect、binary-IV/T、複数IV、LATE/CLATEへの転用は本判断のScience-positive保証外だが、Phase2 Method候補としての存在は削らない。

**ExploratoryとConfirmatory:** 先行SR03-D05採用を維持。探索的にはScience eligibilityを満たすpoint-onlyを保存可能。確認的には対象・有効なMethod-specific inferenceを事前指定し、独立Known-truth Coverage/負例を通過することが必須。\`fit(..., inference='auto')\`がfinite intervalを返してもScience PASSではない。

### 2.4. DRIV-Aの反証と受入依存

- \`DGP-008\`／\`NEG-009,012,013\`／\`REF-E06\`／\`AC-P01/P03/P05/I01/I02/I03\`を追跡。条件付きIVの関連性・外生性・除外・構造線形性と対象/支持域の適格性を別々に評価。
- **Final misspec:** 切片なしの\(\theta(x)=bx\)形式では真値\(2+0.5x\)を表現できない。Estimatorの数値があっても\`CONDITIONAL_IV_STRUCTURAL_SLOPE\`の有効な近似と無条件に表示しない。重み付き射影は正しいTargetではなくmisspecification stressへ。
- **W-adjusted moment:** \`W≠∅\`で単純な\(\mathrm{Cov}(Y,Z\mid X)/\mathrm{Cov}(T,Z\mid X)\)を自動Truthにしない。残差化ReferenceとBackend nuisance/projectionの一致検証必須。
- **Weak/invalid IV:** \(\mathrm E[\tilde Z\tilde T\mid X]\)の小値、Instrumentの直接Y効果、隠れた交絡、train/test leakageを区別して記録。**隠れた除外制約違反を常に機械検出できるとはしない**。
- **0.17.0 runtime未実証:** DoWhy・EconML・Tigramite導入/API smokeはScientific benchmarkを代替しない。採用Configのeffective version、具体的nuisance、split、final model、\`inference\`、Coverage、failure、CPU予算を固定するまでは\`INFERENCE_SCIENCE_PENDING\`。

## 3. SR-03／SR-04既判断との非衝突

| 先行Decision | 保護する条件 |
|---|---|
| SR03-D01 A | \`IV_HETEROGENEOUS_EFFECT\` familyは非IV CATE/LATEと分離。DRIV-Aはその内部の具体target |
| SR03-D03 S2 | B0/B1範囲、B1の二値Z/A・処置前C、初期C1非採用は不変 |
| SR03-D03 I2/G2 | B0/B1のAR異分散頑健漸近、集合形状・EMPTY禁止は不変。DRIVへ自動移植しない |
| SR03-D04 V2/E2/M2/G2-Bridge/R2 | 新E11版付きfail-closed、strict normalized identification→estimator、既存Product/v2の互換・override維持 |
| SR03-D05 B×5 | non-IV CATE7とDRIVを分離、Method-specific inference/point vs CI/Exploratory vs Confirmatory |
| SR03-D06 B×5/A | PAG/CPDAG不確実性を点推定への強制許可に変換しない |

## 4. 判断後に解消する事項・Gate Evidence

| Work item | 新状態 | Closure definition |
|---|---|---|
| DEC-SR04-01（B1 formal target） | **OWNER_DECISION_CLOSED** | 本記録と02の採用事実が一致し、B1-A構造係数の数式と初期非対応範囲が明示された |
| DEC-SR04-02（DRIV formal target） | **OWNER_DECISION_CLOSED** | 本記録と02の採用事実が一致し、DRIV-Aの識別モーメントと具体target・W/contrastの科学的境界が明示された |
| B1科学的推定・Inference | **OPEN** | 独立\`REF-E08/U01\`数値実装、heteroskedastic AR、sample parity・弱IV被覆、Negative、backend/HC法 |
| DRIV科学的推定・Inference | **OPEN** | EconML 0.17.0のcandidate config actual fit/inference、W/no-W、真値と最終modelの適格性、Coverage、weak IV |
| SR04-D Quant AC | **NOT_FROZEN** | Method×DGP×n/R/K/seed/cov_clip等のMethod-specific ACを採用、予算実測 |
| SR04-F Gate07 | **NOT_FROZEN** | 独立Evidence、Source+Reference SHA、FR/ADR、Human owner科学Gate |
| ENH-E11全体構想 | **PENDING_FULL_CONCEPT_APPROVAL** | 68 Scope・SR-01〜12・FR/NFR/AR/Architectureの正式審査と承認 |

**次の科学的作業（Owner判断ではない）:** (1) B1-HET負例とARの独立Reference、(2) DRIVの\`W=∅\` baseline／\`W≠∅\` extensionの分離と0.17.0 runtime method probe、(3) DEC-SR04-03 Frontdoor、DEC-SR04-04 GraphのOwner判断。新たなScope削除・クラス/列挙値のコード生成・Gate採番は本判断の範囲外。

## 5. 技術・原著・公式仕様

- [EconML DRIV公式API](https://www.pywhy.org/EconML/_autosummary/econml.iv.dr.DRIV.html)および[公開実装](https://www.pywhy.org/EconML/_modules/econml/iv/dr/_dr.html)。現行公開ページは0.16系表記であり、SR02実測0.17.0の同一動作を保証するものではない。
- [EconML IV estimation concept](https://www.pywhy.org/EconML/spec/estimation_iv.html)。識別仮定とMethod algorithmの違い。
- [Imbens & Angrist (1994) LATE](https://www.gsb.stanford.edu/faculty-research/publications/identification-estimation-local-average-treatment-effects)。二値IVのcomplier効果と線形IV構造係数を区別。
- [SR03-D03 weak-IV B1/I2/G2審議](20261101_sr03_d03_remaining_2sls_weak_iv_review.md)、[SR03-D01 independent IV family](20261101_sr03_iv_heterogeneous_estimand_decision.md)、[SR04 A-F統合レビュー](20261116_sr04_af_integration_review_and_blocker_resolution.md)。

**記録完了の限界:** Human ownerのこの2件の意味論的方針は採用済み。しかし**独立Science Benchmark、推論Coverage、正式FR/ADR/Gate、Codingは未承認・未実施**。
