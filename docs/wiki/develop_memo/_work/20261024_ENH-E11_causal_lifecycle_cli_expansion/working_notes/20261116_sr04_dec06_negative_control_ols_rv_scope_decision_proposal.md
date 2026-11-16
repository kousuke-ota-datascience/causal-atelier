# ENH-E11 — DEC-SR04-06：Observed Negative Controls／OLS Partial R²・RV Method採否（Owner採用済み・独立技術記録）

**文書区分:** Working Notes／Human ownerが2026-11-16に個別採用した科学的Method判断。**全体構想・正式FR/NFR/AR/ADR/Gate・Coding/Science PASSの承認ではない。**  
**策定・Owner採用日:** 2026-11-16 JST。Human ownerは本ターンで「推奨案で確定する」と明示指示した。  
**判断対象:** 00_04のP1-15／P1-17、A0上位X-04／X-05、SR-04 P1-M18/M19/M20。  
**現状態:** `DEC-SR04-06_A1_TO_A5_OWNER_ACCEPTED / SCIENCE_NOT_RUN / GATE07_NOT_FROZEN / PENDING_FULL_CONCEPT_APPROVAL`。  
**依拠:** [11月1日の方法検討記録](20261101_negative_control_unobserved_confounding_method_review.md)、[Scope68](../00_enhance_background/00_04_phase1_to_phase3_cli_scope_proposal.md)、[SR-04 A〜F統合レビュー](20261116_sr04_af_integration_review_and_blocker_resolution.md)。正式採用事実は[02 owner記録](../00_enhance_background/02_enhancement_concept_approval_record.md)第23項に反映する。**DEC-01〜05の採用を変更しない**。

## 0. 推奨する単一パッケージと代替案

| 採否案 | 初期Phase1の実装範囲 | 科学的・工程上の評価 | 今回の状態 |
|---|---|---|---|
| **DEC06-A（採用）** | P1-M18 Observed NCE、P1-M19 Observed NCO、P1-M20 古典OLS限定Partial R²＋point RVを**3件ともNとして初期候補採用**。個別opt-in・厳格な適格性と失敗型。非線形・広範SensitivityはD | 既存00_04の条件付きN候補を最小の科学的に定義可能なMethodとして具体化。想定EffectResultや既存R2/method statusの一般化をしない | **OWNER_ACCEPTED** |
| DEC06-B（初期非採用） | NCE/NCOのみN、Partial R²はDへ | 感度分析の初期対応が未実装のまま残り、P1-17の判断を再度後送 | 比較対象 |
| DEC06-C（初期非採用） | Partial R²のみN、Observed NCE/NCOはDへ | valid negative controlsがない研究での実装負担を避けられるが、P1-15の科学的反証機能が失われる | 比較対象 |
| DEC06-D（初期非採用） | NC inferenceで未観測交絡を自動補正し、RVをIPW/AIPW/DiD/CATEへ一般化 | 対象・識別仮定・数値Referenceが不定で、false-passリスクが高い。**推奨しない** | 初期不採用を推奨 |

**正式判断:** `DEC06-A`をHuman ownerが**採用**。5個の個別採否論点は §1〜5 を参照。3 Methodはいずれも**新E11 CLI-only の条件付き診断**であり、DoWhy placebo/random common causeと同義ではない。A0 X-04/X-05を3 Methodで全面充足したとは宣言しない。

## 1. DEC06-1：Observed Negative Control Exposure — P1-M18

### 1.1. Initial eligible design

Treatment `A`、Outcome `Y`、**観測した**対照Exposure `Z`、研究者のDAG根拠・測定順序、事前指定した条件付け集合`C_Z`。**Z→Y（直接・媒介経路）の想定上の非存在**と、A–Yに関して感知したいbias mechanismをZ–Yが共有しうる設計理由を別々に記載する。**「Zを観測した」という事実だけでNegative Controlの妥当性を証明できない。**

**限定的な統計検査候補:** 事前指定した連続Yの線形条件付き関連 \(\mathrm E[Y\mid Z,C_Z]=\alpha+\gamma_ZZ+\eta^\top C_Z\) に対して、\(\mathrm H_0:\gamma_Z=0\) を検定する。**`A`を`C_Z`に含めるかどうかは因果DAG・nullの選び方次第**。条件付けによってcolliderやmediator問題が生じうるため`Y∼A+Z`をすべてのNCEに強制してはならない。

出力：`observed_nce_coefficient`（**因果効果とは表示しない**）、model/null/conditioning、classic/robustとsample unitに適格なSE・pointwise CI・p値、DAG仮定・測定時点・データとMethod version、失敗理由。**有意を「未観測交絡の証明」、非有意を「無交絡の証明」としない**。同じbiased exposure-outcome relationと異なるselection/measurement/other mechanismの対照でもsignalになりうる。

### 1.2. Negative and calibration

`DGP-019`のNCE valid-null、shared-U-confounding、invalid-direct-Z→Yを**別variant**として登録。現行DGP019の`γ=0`を無条件なNCE null正例として流用しない。**分析で選んだ統計モデルに条件付きのnullが本当に成立するか、DGP方程式で検証してから**AC-T01サイズ試験を行う。NCE direct null破綻やpost-treatment/colliderを宣言Graphで確認できる場合はtyped reject／review、hidden違反を完全検出する要求はしない。Null下sizeと対立powerは別デザイン、R/K/seedはSR04-Dでfreeze。

**採用判断:** 初期`N`、`opt-in`、観測Zと検証可能なDesign根拠がない場合は`NOT_APPLICABLE`相当（正式status enum未承認）。非線形Y、NCを代理変数としてUのバイアスを自動補正、潜在交絡推定器は初期非採用。

## 2. DEC06-2：Observed Negative Control Outcome — P1-M19

**Eligibility:** **観測した**負の対照Outcome `W`に対し、A→Wの直接/媒介効果がないという研究Design上の根拠と、A–Y側で想定するbiasへの感度・共有構造の根拠を記載する。Wが処置前に測定されたという事実は役立つが、それだけで完全なnegative-control validityの証明ではない。未指定の処置履歴やanticipation、逆因果、選択の影響を評価する。

**限定的null検定候補:** 連続W、事前に登録した条件`C_W`のもと\(\mathrm E[W\mid A,C_W]=\alpha+\gamma_A A+\eta^\top C_W\)における\(\mathrm H_0:\gamma_A=0\)。**「A→Wの因果効果がない」だけでは「AとWの統計的関連が零」とは限らない**。共通原因があれば帰無は破れる。したがって実際にどの条件で帰無が成立すべきかを、研究者のGraph/Assignment/null-modelで宣言・検証する。

`DGP-019`の`A←U→W`では、A–Y側の`U→Y`係数が0であっても`W∼A`は関連し得る。これが**NCOの非特異性負例（NEG-026）**。Null下sizeの独立正例はAとUが独立な割当の別variantで作成し、交絡共有が異なる状況でも「有意＝A–Y交絡確証」とは呼ばない。

**採用判断:** 初期`N`、`opt-in`、観測W/nullとpre-treatmentの根拠が必要。後処置Outcome・null不成立でtyped review、非棄却を因果的成功とみなさない。Proxy control inference、double-negative control bridge/completenessによる同定・自動バイアス補正は初期対象外。

## 3. DEC06-3：Cinelli–Hazlett OLS Partial R²／Robustness Value — P1-M20

### 3.1. Applied estimator contract

対象は連続Yの**事前指定OLS \(\widehat\beta_A\)**。調整済み線形モデル`Y~1+A+C`を正確に再現したdesign matrix、欠測除外、残差df、**古典的OLS SE**と係数を保存・照合する。既存AriadneのHC3を用いる推論と、Cinelli–Hazlettの**classical OLS t/df based algebra**を混同しない。必要な再fitでは「原推定器のHC3 inferenceを置換」ではなく「感度診断専用のclassical OLS re-fit」である旨をResultに表示。

Two-axis parameter：
\[
r_A=R^2_{A\sim U\mid C},\qquad
r_Y=R^2_{Y\sim U\mid A,C}.
\]
\(0\le r_A<1\)、\(0\le r_Y\le1\)、残差df>0、model/full rank/finite SEを初期適格条件とする（境界での可計算性を数式Referenceが保証しない場合はfail-closed）。

Cinelli–HazlettのClassical OVB magnitude：
\[
|\mathrm{bias}|=
\mathrm{SE}_{\mathrm{classic}}(\widehat\beta_A)
\sqrt{\mathrm{df}\frac{r_A r_Y}{1-r_A}}.
\]

`DGP-020`の**既存独立数値例**はSE=.2、df=100、\(r_A=.10\)、\(r_Y=.15\)より\(|bias|\approx 0.258198889747\)。符号は未観測因子の関連方向に依存し、magnitudeを一意の補正符号で表示しない。真の未観測`U`の値をこのGridから推定したわけではない。

### 3.2. Point RV and RV for significance are different

OLS係数を0まで移動させるようなbalanced strength（`r_A=r_Y=r`）の`RV_q`は、原著の**点推定感度**を別定義として保持。一般の`q`（係数を`q`割合動かす）に対し\(f_q=q|\widehat t|/\sqrt{\mathrm{df}}\)と置くと、\[
r=\frac{\sqrt{f_q^4+4f_q^2}-f_q^2}{2}.
\]
`q=1`が点推定のnullまでのRV。これは採用候補の**独立代数Reference**であり、数値実装の比較・有限端点・閾値はGate07未実施。

`RV_{q,\alpha}`（指定信頼水準での統計的有意性に関するrobustness value）は**別の量**であり、t critical value、df変化、調整されたSEとその他の原著条件を扱う。初期Scopeでは**point RV_q（q=1）を最小必須**とし、`RV_{q,\alpha}`の計算法・原著とのparityを追加Reviewできるまでconfirmatory referenceとして採用しない。

### 3.3. Non-eligibility

IPW/AIPW/DML/CATE/IV/RDD/DiD等へ上のOLS係数式をコピーすること、HC3/cluster/HACで得たSEを`SE_classic`として投入すること、\(r_A=1\)の特異点やrank/df不適格、前提の無いデータマイニングによるUの「発見」はすべて対象外またはtyped failure。**RVが大きいことを因果効果の識別・真実性PASSとして扱わない**。

**採用判断:** 初期`N`。連続Yの**classic OLS係数感度**のみ必須、`RV_{q=1}`を数値Referenceの一部、RV for significanceやrobust/非OLS一般化は後続Decision。

## 4. DEC06-4/05：実行・表示・上位構想の残存境界

### DEC06-4：opt-in＋意味論的Fail-closed（採用）

- 実在NC変数（Z/W）・事前指定対照/null/conditioningと、仮定の根拠・必要となる解析unit・時間順序が揃う場合のみMethod適格。ないときは**自動生成や代替変数の捏造をしない**。任意のraw個票を成果物へコピーせず、Source hashesと必要最小限の診断要約のみ保存。
- 本当のHypothesis testでは、sample unit・cluster/serial dependenceによってSE/CI方式を別Method-specificに定義する。未検証CIはnull＋reason。`NO_SIGNAL`は`NO_CONFOUNDING`ではない。
- Existing`PLACEBO_TREATMENT`／`RANDOM_COMMON_CAUSE`／`ADJUSTMENT_SET`／`PROPENSITY_CLIPPING`の科学的意味・versionを壊さない。既存V2/旧Product経路の独立回帰は別Gate。
- `P1-M18/M19`はRefutation/Diagnostic、`P1-M20`はSensitivity。SCIENCE inference availability／model eligibility／technical failure／hypothesis-test resultを別レイヤー。正式enum/CLI pathはArchitecture/設計04待ち。

### DEC06-5：X-04/X-05のDeferred（採用）

`SCOPE:X-04`のSimulated Confounder／Graph Perturbation、`SCOPE:X-05`のIPW/AIPW/非線形Sensitivity一般化・その他Graph/Model sensitivityは**Phase1初期採用の3Methodでは提供完了と見なさず、明示的D（別Decision）**。研究用途の価値と科学的な別手法であることを残し、既存A0上位構想の未解決要件に対する**同等代替の自動承認をしない**。

## 5. Comparison：Owner判断票

| 判断ID | 推奨案 | 含むこと | 含まないこと | 02 Owner採否状態 |
|---|---|---|---|---|
| **DEC06-1** | A：Observed NCEをP1-M18として初期Nに含める | Zの因果null/共有bias/conditioningの事前検証、線形係数の条件付き関連null、opt-in | observed NCを自動同定、未観測交絡の因果確証・自動補正 | **OWNER_ACCEPTED** |
| **DEC06-2** | A：Observed NCOをP1-M19として初期Nに含める | Wの影響非存在、W∼A条件付きnull、非特異性Stress、opt-in | 「A→W無しなら常に関連0」という誤推論 | **OWNER_ACCEPTED** |
| **DEC06-3** | A：古典OLS partial R²＋point RVをP1-M20として初期Nに含める | 2軸grid、OVB magnitude、q=1 RV、classic SE/df re-fit | HC3をclassicと同一視、AIPW/CATE等への一般化 | **OWNER_ACCEPTED** |
| **DEC06-4** | A：NC指定無しはnot applicable、Failureとbias signalの区分 | explicit null/conditioning、null-size/power、statistical inference eligibility | 非棄却からunconfoundednessを認定 | **OWNER_ACCEPTED** |
| **DEC06-5** | A：上位X-04/X-05で未提供方式をDに残す | Simulated confounder、Graph perturbation、汎用Sensitivityに将来Review trigger | 3MethodだけでA0の全範囲をCLOSED | **OWNER_ACCEPTED** |

**Owner判断:** **DEC06-1〜5のA案をすべて採用済み**。これは既存SR-03・DEC-01〜05の単一方針と整合し、Phase1のMethod種類を3件追加した**初期Nの設計方針**を明確にする。採用後の具体的enum・科学的検証・依存・正式Scope全体承認は別。

## 6. Scientific Fixture・Oracle・定量AC・Trace

| Method | Scope（案） | 真値／設計 | Negative | Ref/Quant AC | Environment/Issue |
|---|---|---|---|---|---|
| P1-M18 NCE | SCOPE:P1-15, SCOPE:X-04 | DGP-019のNCE positive/nullとshared-bias対立を分離 | NEG-019, NEG-026 | REF-R02；AC-D01/T01/T02/T03/R03 | ENV-BASE；#16/#14 |
| P1-M19 NCO | SCOPE:P1-15, SCOPE:X-04 | DGP-019のNCO nullはA⊥U variant。γ=0だけではnull成立しない | NEG-019, NEG-026 | REF-R02；AC-D01/T01/T02/T03/R03 | ENV-BASE；#16/#14 |
| P1-M20 OLS partial R²/RV | SCOPE:P1-17, SCOPE:X-05 | DGP-020 OVB=0.258198889747、RV値は独立公式とのparityが残る | NEG-020 | REF-R03；AC-D01/D03/R04 | ENV-BASE；#16/#14 |

**科学的誤受入に対する検証**:
1. 適格なnull条件でType-I（AC-T01候補）、事前指定強度の対立でPower（AC-T02候補）を別セル。候補閾値・R/K/Monte Carlo budgetはまだ未freeze。個別サンプルで帰無が「絶対非有意」とはしない。
2. DGP019の`γ=0`とNCO `W∼A`のnullは**非同値**であることをReferenceとして固定。A–Y biasを特定できないNCO false signalを明記。
3. DGP020はモデルFit/標本OLS beta、classic SE、dfを同一design matrixで独立再計算。partial-R² RVの式・数値が違えばScience BLOCKED。補助実装`sensemakr`との差異をMethod/version別に検査する。
4. Data hash・GraphVersion/null evidence・status・seedを固定。未実施の検証を`Gate07 Evidence: PASS`と捏造しない。

## 7. 実装前のClosureと後続工程

| 判定レベル | 現状態 | Closure |
|---|---|---|
| DEC-SR04-06の5項目Owner採否 | **OWNER_DECISION_CLOSED** | Human ownerがDEC06-1〜5のA案を採用。02第23項に決定事実を登録 |
| Scientific Method Specification | **OWNER_SCOPE_BOUNDARY_ACCEPTED / DETAIL_PENDING** | 本文のnull・OLS式・適用範囲を正本案03/04へOwner採用後反映 |
| Runtime / Reference | **NOT_IMPLEMENTED** | 新E11 CLI enum/adapter、独立OLS/NC null size/RV sample reference |
| Quantitative acceptance | **NOT_FROZEN** | R/K/seed・AC-T01/02、D03 tolerance、Design-specific inference |
| Full concept / Gate / Coding | **OWNER_ACCEPTED** | 68 Scope・SR01〜12・正式FR/ADR/Architecture・Gate06/07批准 |

**後続の最短ルート:** Ownerは`DEC06-A（1〜5すべてA）`を採用済み。02採用記録と00_04/03/04の差分案に反映し、次は**DEC-SR04-07（Quantitative AC・Monte Carlo予算）**へ進む。具体的enum・Runtime・Null calibration・RVの数値Reference・Science Evidenceと正式FR/ADR/Gateは未承認・未実施。

## 8. 一次資料（直接性と限界）

1. Lipsitch, Tchetgen Tchetgen & Cohen (2010), *Negative controls: a tool for detecting confounding and bias in observational studies*, [PubMed](https://pubmed.ncbi.nlm.nih.gov/20335814/)、[原稿全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC3053408/)。NCE/NCOという2系統とbias診断の成立条件。
2. *Negative controls: Concepts and caveats* (2023), [原著全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC10515451/)。NCに対するSensitivity/Specificity・Nullと因果の非同値。
3. Cinelli & Hazlett (2020), *Making sense of sensitivity: Extending omitted variable bias*, [JRSS B原著](https://academic.oup.com/jrsssb/article/82/1/39/7056023)、[公式Supplementary](https://carloscinelli.com/files/Cinelli%20and%20Hazlett%20%282020%29%20-%20Making%20Sense%20of%20Sensitivity.pdf)。OLS partial R²と点推定/有意性RV。
4. [sensemakr 公式sensitvity_stats](https://carloscinelli.com/sensemakr/reference/sensitivity_stats.html) — 計算パリティ候補、同一式のバージョン確認が必要。
5. [既存のDEC06候補科学レビュー](20261101_negative_control_unobserved_confounding_method_review.md)、[SR-04 A Method](20261115_sr04_method_acceptance_matrix_draft.md)、[SR-04 B DGP](20261115_sr04_scientific_fixture_catalog_draft.md)、[SR-04 C Reference](20261115_sr04_reference_specification_draft.md)、[SR-04 D Quant AC](20261115_sr04_quantitative_acceptance_criteria_draft.md)、[SR-04 F Trace](20261115_sr04_gate07_traceability_draft.md)。これらは既存Draftであって実装済・Science Acceptedの根拠ではない。
