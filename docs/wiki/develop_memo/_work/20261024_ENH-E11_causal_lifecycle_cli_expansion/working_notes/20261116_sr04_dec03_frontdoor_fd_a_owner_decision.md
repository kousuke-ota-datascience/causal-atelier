# ENH-E11 — DEC-SR04-03：FD-A（Frontdoor数値推定）個別採用判断・科学的制約

**文書区分:** Human ownerの**個別設計判断**に対応する独立技術記録。全体構想、正式FR/NFR/AR/ADR/Gate06/07、実装許可、Science PASSではない。  
**判断日:** 2026-11-16（JST）。**判断主体:** Human owner（本ターンでFD-Aを明示採用）。  
**個別判断:** `DEC-SR04-03_FD-A_OWNER_ACCEPTED`。  
**科学的実装状態:** `DOWHY_STAGE_CONFIG_PENDING / REF_IMPL_PENDING / INFERENCE_COVERAGE_NOT_RUN`。  
**全体状態:** `PENDING_FULL_CONCEPT_APPROVAL / GATE07_NOT_FROZEN`。  
**正本:** 採用事実＝[02 Owner記録](../00_enhance_background/02_enhancement_concept_approval_record.md)；技術根拠・限界＝本ファイル；Method/Acceptance＝SR04 A〜F。  
**対応:** SCOPE:P1-08、P1-M04（Frontdoor Identification）、P1-M07（数値Estimator）、DGP-005、NEG-004/005、REF-I02/E04、AC-D01/D02/D03/P01/P03/I01/I02、ENV-DOWHY、Issue #16、PLAN:G02。

## 0. 結論・採否の範囲

| 案 | 内容 | Owner判断 | 科学的制限 |
|---|---|---|---|
| **FD-A** | Frontdoor識別を独立検証し、初期の**数値効果推定**を線形・単一Mediatorの二段階係数積に限定 | **採用** | 各stageの適格性・追加の線形仮定を要求。DoWhy API成功のみでは受入れない |
| FD-B | 一般非線形Frontdoorのg-functional数値積分を初期必須にする | 初期非採用 | 条件付き密度の推定、積分、影響関数/Bootstrapなどの独立設計が必要 |
| FD-C | 初期はFrontdoor識別だけとし数値推定を提供しない | 非採用 | 採用済みSR03-D02「Phase1に数値推定を含める」に抵触 |

**採用の意味:** Phase1でFrontdoor数値推定Capabilityを維持し、その**初期保証の正例Method仕様**として線形・単一MediatorのFD-Aを採る。これはFrontdoor識別が線形に限られるとの主張ではない。一般Frontdoor識別可能性とFD-Aモデル適格性は異なる。

## 1. 識別対象・追加仮定・数式

### 1.1. Frontdoorの非パラメトリック識別（先行条件）

Treatment `A`（初期正例は二値）、Mediator `M`（単一連続）、Outcome `Y`、未観測`U`。Frontdoor条件：**(i)** 全A→Y有向経路がMを経由、**(ii)** A→Mに未遮断Backdoorがない、**(iii)** M→YのBackdoorはAで遮断される。測定・一致性・適切なsupport/integrability、Graph/Design assumptionsの根拠を別記録。観測だけでこれらの未観測仮定を検証したと主張しない。

前提が成立すれば、

\[
\mathrm E[Y\mid\mathrm{do}(A=a)]
=\int p(m\mid a)\sum_{a'\in\{0,1\}}
 \mathrm E[Y\mid M=m,A=a']\,p(a')\,dm .
\]

二値Aの`a=1`と`a=0`に対する上式の差が**ATE**。識別式が成立しても、**任意の非線形データに対する線形二段階回帰の無偏性は従わない**。

### 1.2. FD-A：二段階の限定された統計モデル

DGP-005の構造式（各shockは必要な独立性を持つ）：

\[
A\sim\mathrm{Bernoulli}(\mathrm{logit}^{-1}(U)),\quad
M=1.5A+\varepsilon_M,\quad
Y=2M+U+\varepsilon_Y.
\]

UがAとYの未測定共通原因であることはFrontdoor識別を自動的に破らない。MにはA以外からU→Mの矢印なし、A→Yの直接矢印なし。サンプルの基準二段階モデル（切片付き）は、

\[
M_i=\alpha_0+\alpha_1 A_i+e_{M,i},
\]
\[
Y_i=\beta_0+\beta_1 M_i+\beta_2 A_i+e_{Y,i}.
\]

`Y∼1+M+A`とするのは、`M`→`Y`へのBackdoorをAで閉じるため。**Y∼1+Mだけを正しい第2段階と認めない**。このDGPでは`M`のinnovationが条件付きでUと独立であり、Aが二値なので`E[U|A]`は切片+Aで飽和表現できる。したがって母集団で\(\alpha_1=1.5\)、\(\beta_1=2\)、ATE = \(\alpha_1\beta_1=3\)。

**これらはDGP-005の限定Reference。** 一般的な線形Frontdoor・変動Treatment・効果修飾・交互作用・未知のbaselineを対象とした定理ではない。実際のEstimatorのtreatment contrast・standardization・stage共変量をMethod Specで別固定する。

### 1.3. 3系統の独立Reference

1. SCMのdo介入で計算したATE=3（母集団真値）。
2. 固定標本上で**独立した**OLS/QRによる\(\widehat\alpha_1\widehat\beta_1\)（sample parityのOracle）。
3. 非パラメトリックFrontdoorのg-functional：本DGPの条件付き分布を代入してATE=3（識別式の理論的Oracle）。

**sample exact parityと真値近似を分ける**。同じsampleでDoWhy内部処理と独立OLSの推定値が一致しない場合、stageの調整集合・定数項・データ除外や重み設定をまず検証する。

## 2. DoWhy adapterのMethod適格性と負例

### 2.1. Backend適合性は未確認

DoWhy 0.14の`frontdoor.two_stage_regression`は公式の線形二段階Estimatorである。ただし`mediation_first_stage_confounders`／`mediation_second_stage_confounders`等の実効ターゲットから、第1・2段の説明変数を構成する。**本DGPで第2段の調整にAが実際に入ることを、version-pinned probeで必ず確認する**。ライブラリのMethod名だけから`Y∼1+M+A`が実際に実行されたとは判断しない。

**Preflight候補:** Python3.12/Linux、`ENV-DOWHY`、DoWhy 0.14（SR02の単独/API smokeで観測した候補版。正式pinではない）、exact graph/identified estimand、stage1/stage2のbackdoor変数一覧、OLS coefficients/intercepts、`estimate_effect`値と符号、version/seed、入出力ハッシュ、nullable CI/inference metadataを記録。

候補版の`TwoStageRegressionEstimator`は線形モデル/単一Mediatorに限定されることを前提としているが、**0.14をプロジェクトで採用する決定、実装実行、推論Coverage PASSではない**。

### 2.2. Negative／Stressを分離

| Fixture | 正しい扱い | 偽受入を禁止すること |
|---|---|---|
| DGP-005正例 | 識別条件とFD-Aの線形追加仮定の両方を満たすものとして評価 | ATE=3との漸近的精度、sample OLS parity、CI availabilityを別評価 |
| NEG-004：M欠落、A→Y直接path、U→M追加 | **宣言Graphで違反が観測できる場合**typed reject／review。識別条件破綻の負例 | Hidden violationの全自動発見を保証しない |
| NEG-005：非線形M→Yや効果修飾 | Frontdoor自体は成立し得るが**FD-A線形モデルはmisspecified**。bias stressとして定量記録 | 非線形だからFrontdoor識別不可と偽表示しない |
| 追加：2nd stageにAを入れない | DoWhy effective configを診断し、独立Sample Referenceと比較 | 理論識別が成立することを理由に誤ったstage仕様を許可しない |
| 追加：Mの多重化、Tの非二値化、Cの未審査指定 | 初期保証外としてtyped ineligible/reviewまたはMethod別再承認 | 形式的にはfitできるだけで初期Science PASSへ昇格させない |
| 追加：未観測Backdoorの宣言無し | 必要なGraph/Assumption evidenceを要求 | 何も記録せず`IDENTIFIED`とすることを禁止 |

### 2.3. 推論とScience acceptance：未完了の義務

\(\widehat\alpha_1\widehat\beta_1\)の有限sample分布は各stageのOLS CIを単純に積にする方法では正当化できない。採用する確認的Inference（joint delta covariance・独立unit bootstrap等）はMethod Configと検証で確定する。Bootstrap候補なら**個体単位を再抽出し、stage1/2を再fit**、元のDGP構造に適格なことを確認。正例Coverage/interval availabilityはSR04-DのAC-I01/I02等の**提案閾値**とMethod別R/n/seed/K/compute budgetを事前freezeし、失敗分母と非有限値を含めて評価する。

**現時点:** `FD-A_OWNER_ACCEPTED`のみ。DoWhy effective stage未probe、独立Reference未実装、CI方式未確定、Science Benchmark未実行、正式Gate07未実施。

## 3. SR03／SR04とのTraceabilityと禁止条件

- **SR03-D02:** FrontdoorはPhase1で識別だけでなく数値推定を含む。FD-Aは**数値推定Methodの初期保証境界**を与える。
- **SR03-D04 E2/M2/R2:** 新E11 Methodを上流のIdentificationResult・estimand・Graph/Design/Question/Datum hashと照合し、非識別・要レビューを無断通過させない。旧Product/v2の回帰は不変。
- **SR03-D05:** interval availabilityと科学的被覆は別。計算可能な点推定を、推論品質の証拠なしにConfirmatory PASSとしない。
- **SR03-D06:** PAG/CPDAGの未確定方向をDAGに変換してFrontdoorのGraph条件を捏造しない。Graph再固定なら新versionから識別し直す。
- **SR04-F Gate07:** `P1-M04`識別と`P1-M07`数値推定を別行で審査。関係するDGP-005/NEG-004/005/REF-I02/E04の追跡を保つ。これらの独立科学Evidenceはまだない。

## 4. Owner判断の閉鎖と後続Blocker

| 項目 | 現在状態 | 解消要件 |
|---|---|---|
| DEC-SR04-03 FD-A選択 | **OWNER_DECISION_CLOSED** | 02 Owner記録とこの技術判断の整合 |
| DoWhy 0.14 version pin/stage正当性 | **TECHNICAL_BLOCKED** | stage confounder/OLS sample parityの実測 |
| Product/CLI/schema・正本Requirements | **FORMALIZATION_PENDING** | SR03 D04のversioned gateと正式FR/NFR/AR/Architecture |
| 独立REF-E04／CI科学妥当性 | **SCIENCE_NOT_RUN** | oracle code・負例・独立被覆/MC・review |
| Gate07／全体構想 | **NOT_APPROVED** | 正式Source SHA/Rule/EnvとOwner・独立Review |

**次の科学的作業:** Method Config/StageとCIの独立検証、Frontdoor一般式との差のStress、SR04-F evidence登録。**本判断はCodingを許可しない。**

## 5. 外部一次資料

1. [DoWhy v0.14 パッケージ・Estimator一覧](https://www.pywhy.org/dowhy/v0.14/dowhy.html) — `frontdoor.two_stage_regression`の公開Method名。
2. [DoWhy v0.14 推定ガイド](https://www.pywhy.org/dowhy/v0.14/user_guide/causal_tasks/estimating_causal_effects/index.html) — 線形のTwoStageRegressionEstimatorとFrontdoor適用。
3. [DoWhy TwoStageRegressionEstimatorの公式系列実装](https://www.pywhy.org/dowhy/v0.14/_modules/dowhy/causal_estimators/two_stage_regression_estimator.html) — stage調整集合の確認対象。将来の0.14実効probeに代わるものではない。
4. [SR04統合レビュー](20261116_sr04_af_integration_review_and_blocker_resolution.md) — FD-A/B/C比較と残余依存。
