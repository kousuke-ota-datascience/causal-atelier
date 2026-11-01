# ENH-E11 — Negative Control／未観測交絡Sensitivity：Phase 1方法論の具体化（技術検討メモ）

**記録日:** 2026-11-01（日本時間）  
**文書区分:** `working_notes`／科学的方式の比較・実装スコープ修正案。**00/01/02/03/04、Gate 06/07を代替する正式仕様ではない**。  
**対象:** `00_04`のP1-15／P1-17、X-04／X-05、技術審査SR-06、および#16。  
**現在の結論:** **METHOD_PROPOSAL_READY / OWNER_DECISION_PENDING / SCIENTIFIC_ACCEPTANCE_NOT_RUN**。Negative Controlの観測変数を用いた反証検査2種類と、線形回帰係数に限定したpartial R² Sensitivityを**Phase1の最小実行候補**として提案する。  
**現行参照SHA:** `9e8b291fdb770d676a3dfa9e8d3000ffaab8391c`（文書化開始時、受入Baselineではない）。

## 0. INTRODUCTION

### 0.1. 検討の目的

「Negative ControlとUnobserved-confounding Sensitivityを追加」と書くだけでは、**研究者がどの因果的な帰無仮説を検査し、どの仮定の強さに対する結論の脆弱性を報告できるか**が規定できない。目的・データ・数理モデル・操作・解釈・非適用例を分離して、00_04の「N（要審査）」に実質的な科学的意味を付与する。

本提案は**方法の選定と適用境界**に関する技術判断であり、同時にすべてのATE/ATT/CATE推定器へ対応するという約束ではない。採否、方法別coverage、推論の厳密な許容条件はHuman ownerとArchitecture Reviewで承認する。

### 0.2. 一次資料と既存実装の根拠

- **Negative controls（観測変数）:** Lipsitch, Tchetgen Tchetgen & Cohen (2010), *Epidemiology*, DOI [10.1097/EDE.0b013e3181d61eeb](https://doi.org/10.1097/EDE.0b013e3181d61eeb)。NCEとNCOの因果構造と検出条件を区別する。
- **Negative controlの解釈上の限界:** Shiら, *Negative controls: Concepts and caveats*, [PMC10515451](https://pmc.ncbi.nlm.nih.gov/articles/PMC10515451/)；負の対照が有意でも対象の未観測交絡を直接証明しない。
- **OVB/partial R²:** Cinelli & Hazlett (2020), *JRSS B* 82(1), 39–67, DOI [10.1111/rssb.12348](https://doi.org/10.1111/rssb.12348)。Robustness Valueは線形回帰係数に対する未観測交絡の部分決定係数の感度要約。
- **参照実装:** [sensemakr（OLS用）](https://github.com/carloscinelli/sensemakr)。DoWhyの[Refuting Effect Estimates](https://www.pywhy.org/dowhy/v0.13/user_guide/refuting_causal_estimates/refuting_effect_estimates/index.html)ではデータ変換型negative-control refuterとSensitivityを区別する。**DoWhyのrandom common cause／placebo／dummy outcomeと、本書で定義する観測NCE/NCOは同じ方法ではない**。
- **現行コード:** `src/ariadne/scientific/{refutation,sensitivity,inference}/adapter.py`、`src/ariadne/product/domain/analysis_spec.py`、`src/ariadne/interfaces/cli/{config_schema,scientific_stage}.py`（`prototype/ariadne_mvp`）。既存Refutationは`PLACEBO_TREATMENT`／`DATA_SUBSET`、Sensitivityは`ADJUSTMENT_SET`／`PROPENSITY_CLIPPING`のみ。現行CLIとDomain validationは新Methodを受け付けない。**新機能は現時点で実装済みではない**。

## 1. 科学的な区分と採用方針（案）

| ID | 方式（Phase1の提案Method ID） | 研究上の目的 | 今回の提案判定 |
|---|---|---|---|
| NC-E | `NEGATIVE_CONTROL_EXPOSURE` | 対象Yに因果的に影響しないと事前に根拠付けた観測ZとYの残差的関連を調べる | **N（条件付き採用候補）** |
| NC-O | `NEGATIVE_CONTROL_OUTCOME` | 対象Aから因果的に影響されないと事前に根拠付けた観測WとAの残差的関連を調べる | **N（条件付き採用候補）** |
| UC-OVB | `UNOBSERVED_CONFOUNDING_PARTIAL_R2` | 仮想未観測交絡Uが回帰係数の解釈を変える強さを定量化する | **N（OLS限定採用候補）** |
| EXTRA | simulated confounder／graph perturbation／全Estimand・全推定器へのSensitivity | 追加の手法別頑健性診断 | **D案（個別オーナー判断待ち）** |

上記の`N`は**承認前の実装候補**であり、科学的妥当性や実装可用性が検証されたという意味ではない。Method ID、科学status名、JSON field名はいずれも提案であり、採番・正規enumは未承認。

## 2. NC-E：Negative-Control Exposure

### 2.1. 研究状況・問い・前提

観測研究で、介入Aが結果Yに及ぼす効果を調べる際、Aと交絡構造を共有しうる観測変数Zを「負の対照Exposure」として事前選択する。

**事前に分析者が根拠を示す:** (i)想定した比較設定で**Z→Yの直接・媒介因果経路がないこと**（Aを介する可能性があれば、それを含めた適切な条件付きnullを設計）、(ii)A–Yの懸念バイアスとZ–Yが**検出したいバイアス構造を共有する**こと、(iii)Zが介入後に変化する変数ではないこと、(iv)調整集合Cと帰無比較条件がDAG・時間順序と整合すること。

これらは**データから自動的に証明できない**。Zに別の因果経路がある／調整によるcolliderが発生する場合、Z–Yの非ゼロ係数をA–Yの未観測交絡と解釈してはならない。

### 2.2. 検証計算と解釈

- 入力：`treatment_column=A`、`outcome_column=Y`、`negative_control_exposure=Z`、`null_conditioning_set=C_Z`、期待する帰無関係、DAG/Designの理由、連続Yを伴うモデル指定、診断用信頼区間。
- 初期Reference検定：**事前指定した線形モデル** `Y ~ Z + C_Z`（条件が科学的に正当な場合のみ`A`もC_Zへ含める）のZ係数が0であるという**条件付き関連の帰無仮説**を評価する。`C_Z`に何を入れるかはモデル・DAGで明示し、自動的にAを調整しない。
- 出力：Z係数（**因果効果と表示しない**）、標準誤差、CI、P値、conditioning set、nullの期待根拠、sample/support・モデル診断、検査に用いた仕様とprovenance。
- Interpretation：帰無関係と矛盾する観測は、当該対照が検出対象とする**バイアス、設計不成立、モデル仕様不良等のシグナル**になりうる。ただし未観測交絡の存在の確証ではない。帰無を棄却しなくても無交絡の証明ではなく、低検出力／共有バイアス不十分／相殺等を明示する。

### 2.3. 不適格・拒否条件

**観測されたZが存在しない**、Zの因果的nullが研究上正当化されない、Zが後処置・outcomeの子孫、調整集合が禁忌（collider／mediator等）、対照の独立変動が乏しい、サンプル不足、欠測で比較が不適切、線形係数が定義不能の場合は、0効果を生成せず`NOT_APPLICABLE`／`REQUIRES_REVIEW`等を返す。検出方法と拒否理由をManifestに残す。

## 3. NC-O：Negative-Control Outcome

### 3.1. 研究状況・問い・前提

介入前に測定した成果関連変数Wなど、**AがWに直接にも間接にも因果的影響を与えない**という仮定を明示でき、かつ本来のYの交絡バイアスと共通する仕組みを持つ観測Wを選ぶ。

**注意:** 単に「介入より前に測定した成果」を機械的にNCOと宣言しない。過去の介入履歴、anticipation、時間軸、逆因果、W→A等によってnullの設計が変わる。比較に用いる集合`C_W`をDAGから理由付けし、ZとWの因果方向を取り違えない。

### 3.2. 検証計算と解釈

- 入力：`negative_control_outcome=W`、`treatment=A`、`conditioning_set=C_W`、nullの事前根拠、モデル・Inference設定。
- 初期Reference検定：連続Wを対象として、事前指定した線形モデル `W ~ A + C_W` で**Aの条件付き関連係数が0**という帰無仮説を評価する。係数はWに対する**介入の因果推定量ではなく**、Negative-Control診断指標。
- 出力：係数、CI、P値、モデル診断、Wの時間情報／shared-bias根拠、結果の限界。
- Interpretation：帰無と矛盾する場合、A–Y推定で見落とした共通原因だけでなく選択バイアス・測定バイアス・モデル仕様・対照の不適格も検討する。Null非棄却からunconfoundednessを認定しない。

### 3.3. 不適格・拒否条件

WがAに影響されうる、Wの取得時刻・対照根拠が不明、AとWの間に対象の検査と無関係な因果経路がある、C_Wが科学的に不適切、観測変数不足、識別不能、強い共線性等では**科学的な非適用結果**を返す。

## 4. Unobserved-confounding Sensitivity：partial R²（Cinelli–Hazlett）

### 4.1. 最小対象を限定する理由

**今回の最小方式は、連続アウトカムYに対する事前指定した通常の線形OLS係数`A`の感度分析に限定する。** Aがbinaryであっても加法・定数効果などのモデル解釈を明示し、まず`ols`/`outcome_regression`に対する調整済み係数を評価する。真のATE/ATTの推定精度がこの検査だけで保証されるわけではない。

**現行実装に固有のギャップ:** `EstimationAdapter`は`robust_se="HC3"`を既定で使用する。Cinelli–Hazlettの通常のOLS `t`・`df`の公式を、**HC3の標準誤差と既存Resultの値へ無断適用しない**。実装方針として、(a)利用したOLS当該design matrix、完全ケース、係数、古典的OLS variance、残差自由度を再現可能な形で保存して検査対象と一致するか確認する、または(b)適切なrobust-covariance対応の科学的方式を別途立証する。最小方式の候補は(a)であり、既存HC3を使った主推論とは**区別した補助診断**として表示する。

IPW/AIPW、非線形推定、CATE、DiD、IV、RDD等へ**このOLS公式を一律適用しない**。対象外estimand/estimatorは`NOT_APPLICABLE`とし、方法別拡張は別審議。これは「未観測交絡Sensitivityを全方式へ提供した」と主張しないという制限である。

### 4.2. 数理的な入力・出力

観測済み調整共変量Cに条件付けて、潜在する交絡要因U（変数群であってよい）の強度を、次の**2軸**で表す。

- `r2_au_c = R²(A ~ U | C)`：Cを考慮した後、UがAの残差変動のどれだけを説明しうるか。
- `r2_yu_ac = R²(Y ~ U | A,C)`：A,Cを考慮した後、UがYの残差変動のどれだけを説明しうるか。

0≦partial R²≦1であり、**Uが実際に観測されたと主張する数値ではない**。0を含む事前指定gridを分析者が設定する（1などの特異点は式に応じて排除）。必要に応じて既存共変量との強さの比較を補助的に用いるが、**観測共変量と同じ強さだから現実の未観測Uもそれ以下である**と保証しない。

最小出力：
1. 元のOLSの処置係数`beta_A`、対応する古典OLS SE、残差自由度、推定対象と再計算した`t`、調整集合・データhash・fit設定。
2. 各gridの2軸partial R²、原著のOVB関係による**最悪方向の係数変化／感度曲線**、0へのcrossing（可能な場合）。
3. **Robustness Value（point estimateを0へ動かすために必要な等強度partial R²）**。推論上の有意性の閾値を変えるRVは、その計算法と自由度・分散前提を検証できた場合に**別フィールド**として追加する。
4. 研究者が指定した現実的な交絡強度の根拠、Reference covariates、解釈警告、対象外・特異点の負結果。

**閾値（RV値）が高い／低いことだけで「因果効果は本物／偽物」と機械的にPASS/FAILしない。** 問いは「仮定した未観測交絡がどれだけ強ければ効果の解釈が変化するか」である。

### 4.3. 今回の実装候補から明示的に除外するもの

- 未観測交絡の**実データ上での識別・存在判定**、未知Uの推定、バイアスの自動補正。
- IPW/AIPW/DR、ロジスティック、CATE、LATE、準実験等へOLS系partial R²をそのまま流用すること。
- DoWhyの`add_unobserved_common_cause`（仮想Uを加えて再推定するSimulation）は**科学的に別方式**。利用可能なoptionとして調査はできるが、今回のpartial R²を置換するものとは自動認定しない。
- すべての上位A0要求（outcome model variation、graph perturbation、sample inclusion等）を1方法で満たしたとの主張。

## 5. 共通のScientific Result／CLI契約（設計候補）

### 5.1. 必要な入出力

| 契約 | Negative Control | partial R² Sensitivity |
|---|---|---|
| 必須入力 | A/Y、**実在する**ZまたはW、conditioning set、事前帰無根拠・DAG/Design | Original estimator/estimand、OLS coefficient fitとC、2軸partial R² grid、null threshold |
| 検査対象 | 観測対照と対象の**条件付き関連** | 仮想Uの強度に対する**OLS係数の脆弱性** |
| 出力 | control type、null、係数・CI・P値、モデル診断、shared-bias仮定 | base beta/SE/df、grid、bias-adjusted coefficient・RV、benchmark根拠 |
| 科学的負結果 | null不適合、Z/W欠落、post-treatment、null不当、rank不足／検出力不足 | 非OLS、HC3と通常OLSの取り違え、非可逆design、0除算・特異点、データ不一致 |
| 来歴 | input hash、Spec/Graph、帰無根拠、data selection、参照method/version | input/fit hash、OLS設定、古典/robust共分散区別、grid、参照式版 |

**提案status語彙:** `BIAS_SIGNAL_DETECTED`、`NO_SIGNAL_DETECTED`、`INCONCLUSIVE`、`NOT_APPLICABLE`、`REQUIRES_REVIEW`。これらは**現在のScientificStatus enumとして存在するとは限らない**。既存`FAILURE_DETECTED`／`NO_FAILURE_DETECTED`／`INCONCLUSIVE`等とのmappingは、科学的意味を損なわずに設計04で決める。単純なP値の非有意を無条件の`PASS`としない。

### 5.2. CLI・契約スコープ

- `ariadne-refute`にobserved `NEGATIVE_CONTROL_EXPOSURE`と`NEGATIVE_CONTROL_OUTCOME`、`ariadne-sensitivity`に`UNOBSERVED_CONFOUNDING_PARTIAL_R2`を**候補Method ID**として追加。既存methodのenumや`config_version=2.0`を勝手に上書きせず、版管理と後方互換を検証する。
- 研究者が指定する対照変数とDAG仮定を、ランダムに生成した「偽Negative Control」で代用しない。
- 生データや個人情報を無断でManifestへダンプしない。test fixtureに必要なCSV/Parquetは最小化し、出力は正規JSONの診断とprovenanceに限定する。
- optional backendを使う方式は、依存欠落を科学的非適用と技術的実行失敗に分ける。**この3方式の採用がPython/DoWhy/EconMLの互換性確認を免除するものではない**。

## 6. 独立した科学的検証計画（Gate 07の入力、未freeze）

### 6.1. 既知真値・負例fixture

| Fixture | 生成する条件 | 期待する検証結果 |
|---|---|---|
| NC-E-VALID | 指定nullが真、検出対象バイアスなし、有効Z | 条件付き係数の校正・第一種過誤率／CI被覆の検証。個別標本のP値が必ず非有意とは要求しない |
| NC-E-CONFOUND | UがA/YとZ/Yの双方に関係し、指定nullから逸脱 | 検出力曲線とbias signal。false-negative可能性を含め報告 |
| NC-E-INVALID | Z→Yの実因果経路／禁忌なconditioning set | 設計不適格としてreject/review、未観測交絡の断定をしない |
| NC-O-VALID | A→Wの因果経路なし、事前指定nullが妥当 | null下のtype-I/CI calibration |
| NC-O-CONFOUND | UがA/YとA/Wの双方の共通原因、nullから逸脱 | bias検出率と信頼区間 |
| NC-O-INVALID | WがAの子孫／検査条件が違反 | reject/review、null無効を説明 |
| SENS-OLS-ZERO | U強度0、既知OLSモデル | 原係数と感度曲線の0点が一致 |
| SENS-OLS-REFERENCE | 線形生成モデルと、Uを観測したReference fit | OVB-adjusted coefficientとsensemakr/解析式との数値パリティ。**bias方向・SE/df**も比較 |
| SENS-OLS-REVERSAL | U強度を変えると符号・null crossingが起こる設定 | 事前計算のthreshold/RVとの一致と連続性 |
| SENS-INAPPLICABLE | HC3 SEを古典SEと誤用、IPW/AIPW、共線性、自由度不足 | 無根拠なRV・推定値を返さず非適用／明示的warning |

**数値基準は未設定:** α、許容誤差、CI被覆率の許容帯、power評価のサンプル量と乱数seed、Reference版はGate 07作成時に事前固定する。今回これらを科学的PASS済みとはしない。

### 6.2. 科学的反証の扱い

NCの帰無が棄却された場合でも、**選択した対照変数自体の無効、モデルmisspecification、選択/測定bias、unmeasured confounding等の複数説明**を出力で保持する。帰無が棄却されなくても、バイアスの不在は証明できない。Sensitivityで結果が頑健と出ても、**研究者が妥当と判断したUの強度範囲に対する結論**しか得られない。

## 7. オーナーに残す明示的な判断

| Decision | 提案内容 | 未承認の判断 |
|---|---|---|
| NC-DEC-01 | NC-E/NC-Oの**実在対照変数を用いるnull検査2種類**をP1-15の最小Nとして採用 | valid nullを説明できない入力を非適用とし、2種類とも実行必須か |
| NC-DEC-02 | 連続Yの線形条件付き関連を初期Reference implementationにする | 非線形／binary outcomeへの拡張期日と対応Issue |
| SENS-DEC-01 | **OLS限定Cinelli–Hazlett partial R²**をP1-17の最小Nとして採用 | IPW/AIPW等へ広げない範囲でもPhase1の価値を満たすか |
| SENS-DEC-02 | 古典OLS再現fitを明示し、既存HC3推論とは分離 | 古典OLS/robust推論のDesign差分、Reference実装と許容誤差 |
| X-DEC-04/05 | Simulated Confounder/Graph Perturbation/広範SensitivityをD案に残す | A0の要求との同等性・後続Owner/Issue・承認理由 |

**今回確定したのは科学的な候補定義と、その適用不能条件までの説明である。** 採否・実装見積り・数値Benchmark・Gate・Product正本改定は別工程の決定とする。
