# ENH-E11 S05/B05 — AR HC1候補の数学・数値予備検査（Author review only）

**日付:** 2026-11-22  
**対象:** Owner DEC-S05-AR01=Aで独立科学審査対象とされたG08/P3-M10（B0 binary-Z/A LATE）およびP3-M11（B1指定C・加法線形structural slope）の *provisional HC1+χ²(1) AR inversion candidate*。  
**権限状態:** `AUTHOR_MATH_PREFLIGHT_COMPLETED / EXACT_AR_ALGORITHM_NOT_FROZEN / INDEPENDENT_SCIENCE_NOT_REVIEWED / T2_T3_NOT_RUN / S10_NOT_FROZEN / S11_CODING_NOT_AUTHORIZED`。本メモは独立Reviewerの承認ではなく、既承認の全実数AR要求を弱めない。

## 1. 検定量の候補数理導出

観測`n`、被説明`Y`、内生`A`、単一excluded instrument `Z`、指定済み外生`Q`（B0は切片、B1は切片+指定C）、デザイン`X=[Q,Z]`（列数`k`）とする。ここでは`rank(X)=k<n`を必要とする。

`hᵀ = e_kᵀ (XᵀX)⁻¹ Xᵀ` はOLSの`Z`係数抽出演算子。 `g_Y=hᵀY, g_A=hᵀA`、残差`u_Y=(I-P_X)Y, u_A=(I-P_X)A`。

候補`β`について`Y−βA`を`X`でOLS回帰したexcluded-Z係数は
`g(β)=g_Y−β g_A`。OLS HC1 Sandwichの当該係数分散は
`v(β)=[n/(n−k)]∑ᵢ hᵢ² (u_{Y,i}−β u_{A,i})²
       = V_A β² − 2V_{YA} β + V_Y`,
`V_A=κ∑hᵢ²u_A², V_{YA}=κ∑hᵢ²u_Yu_A, V_Y=κ∑hᵢ²u_Y², κ=n/(n−k)`。

`v(β)>0`の適格な範囲で、HC1 Wald型AR統計量候補
`T_AR(β)=[g_Y−βg_A]²/v(β)` を`q=χ²_{1,1−α}`と比較する。反転集合は二次不等式と分散ドメインの交差として
`S_α={β∈ℝ: v(β)>0 AND P(β)≤0}`、
`P(β)=(g_A²−qV_A)β² +(-2g_Yg_A+2qV_{YA})β +(g_Y²−qV_Y)`。

**重要:** `P(β)≤0`のみで`v(β)=0`を受理してはならない。`g(β)≠0,v=0`は通常の検定量が正則でなく、`g(β)=0,v=0`も`0/0`の未定義。数値上のepsilonで分散0を恣意的に正にしてはならない。Rank不足、nonpositive/degenerate variance、roundoffの型付きStatusは独立Reviewer確認待ち。

## 2. 全実数集合の位相

`P`の二次係数・判別式・根・`v(β)>0`を解析的に検証する。

- 二次係数正、実相異2根：一般には根に挟まれる有界区間（BOUNDED）。
- 二次係数負、実相異2根：両tailを含む非連結な二半直線（DISCONNECTED / UNBOUNDED）。
- 二次係数負、実根なし：一般には`P<0`が全域で成立しALL_REAL。ただし`v=0`を別除外。
- 判別式0、leading≈0、同時消去、分散退化：単点・全域・半直線・真の空集合等の境界や未定義を**epsilonの恣意的な数値定義ではなく**厳密符号・正規化・根隔離・interval evaluationで区別する。
- `g_A≠0`、`v(β̂)>0`のjust-identified標本で`β̂=g_Y/g_A`は`T_AR(β̂)=0`。したがって**非空性が必須**であり、見掛けのEMPTYを正常な結果として出してはならない。汎用CodecのEMPTY表現可否は別問題。

**限界:** この導出は候補HC1統計量の代数。実際のAR検定が所定のB0/B1標本設計・構造仮定下で正しいサイズ/被覆率を持つ証明ではない。悪いinstrumentや誤った`Q`仕様もARで救済されない。

## 3. 作成者側数値予備検査（独立科学Oracleではない）

Local container (not user's approved isolated Linux): Python **3.13.5**, NumPy **2.3.5**, SciPy **1.17.0**, Statsmodels **0.14.6**。Python 3.12+locked runtimeの実証ではない。

Fixed NumPy PCG64 seed、`n=220`、`Z∼Bernoulli(.5)`, `C,U,ε₀∼N(0,1)` independently、`ε=ε₀(1+0.5Z)`、`A=γZ+0.5U+0.3C`、`Y=1.5A+0.25C+ε`。B1 `X=[1,C,Z]`。`q=χ²_{1,.95}=3.841458820694124` (illustrative **unadjusted** α=.05; not G08 multiplicity-FWER threshold)。

| 位相 | γ | Seed | `P(β)`の二次/一次/定数係数（約） | 根（約） | `β̂=gY/gA`（約） |
|---|---:|---:|---|---|---:|
| BOUNDED | 1.4 | 0 | (2.39971531, −7.46929849, 5.71735508) | 1.3574923952, 1.7550845284 | 1.555065 |
| DISCONNECTED | 0.3 | 446 | (−0.00134560, 0.03145826, −0.14472359) | 6.2960971011, 17.0825345837 | 0.851086 |
| ALL_REAL | 0.3 | 392 | (−0.00144561, −0.01030121, −0.07720125) | 実根なし | 1.760054 |

各Caseで`v(β)`の全実数最小は正（それぞれ約 0.0245569、0.0277461、0.0250325）。`β̂`で`P(β̂)<0`を確認。5点`β=[0,1,2,5,-5]`で、別の`statsmodels.api.OLS(Y−βA,X).fit(cov_type="HC1")`が出す`Z`係数二乗/HC1分散と直接`g(β)²/v(β)`の差が`<1e−7`で一致（3 Case×5点）。同じOLS統計量の**ソフトウェア計算パリティ**であって、独立な弱IV真値・Coverage・全実数反転の完成証明ではない。

## 4. 必須の反証・独立審査（残件）

1. **サイズ・適用範囲**: binary Z/A B0 LATEのmoment/monotonicity/structural assumptions、B1 nuisance Cのlinear projection/conditional exogeneity、observational unit independence、heteroskedasticity下のweak-IV uniformityを科学原典と照合。i.i.d.のHC1をcluster/HACへ無審査で拡張禁止。
2. **独立Reference**: Statsmodels同型HC1実装とは異なる数式実装／exact rational または高精度root isolationを用いて、bounded, unbounded, disconnected, ALL_REAL, singleton, conditional EMPTY, zero/near-zero first stage, rank deficient, degenerate variance, near-multiple rootsを検証。異常が数学的EMPTYか数値FAILEDかを決める。
3. **Coverage**: 独立DGP真値、負例、null rejection、Monte Carlo SE、K/FWER=.05、T2 resource pilotとT3事前登録。ここで試した15組合せの数値一致からCoverageは推測できない。
4. **Backend/Lock/Schema**: approved Linux Python3.12 isolated environmentの実効versions/Distribution/Backend fitter/API/CIを固定。今回のLocal環境は代替しない。
5. **独立承認**: DEC-S05-AR01の指定通り、このHC1＋χ²候補を採用するか修正するかは独立科学Reviewerの数学・統計署名とOwnerの後続Freeze判断まで**未決**。G08 06/07へ確定算法として格上げしない。

参考の原著論文・研究: Mikusheva, *Robust confidence sets in the presence of weak instruments*, Journal of Econometrics (2010), https://www.sciencedirect.com/science/article/pii/S0304407609003029 （弱IV下でサイズを維持する検定の反転という枠組み）。本予備検査と文献自体は**P3-M10/M11の具体的HC1/χ²選択の独立検証ではない**。

**結論:** 候補HC1数式の代数的反転・最低限の三位相の数値再現は予備検査で成立。S05-B05独立科学実行・G08 AR算法FreezeをPASSにする根拠にはならない。
