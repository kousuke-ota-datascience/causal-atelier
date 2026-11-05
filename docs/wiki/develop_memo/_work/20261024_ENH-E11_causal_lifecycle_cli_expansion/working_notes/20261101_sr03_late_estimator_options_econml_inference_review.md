# ENH-E11 — SR-03 Frontdoor採用判断・LATE推定器の選択肢・EconML区間推定の原因調査

**作成日:** 2026-11-01（JST）  
**文書区分:** `working_notes`。オーナーの個別決定と未決事項を切り分けた技術検討。正本FR/AR・Gate承認を代替しない。  
**判断状況:** `FRONTDOOR_NUMERIC_PHASE1_ACCEPTED / LATE_A_PLUS_B_OWNER_ACCEPTED / ECONML_ROOT_CAUSE_IDENTIFIED / INTERVAL_BOOTSTRAP_API_PASS`。

## 0. INTRODUCTION

### 0.1. オーナーが明示した判断

- **SR03-D02／Frontdoor:** 「Phase 1に数値推定まで含める」を**採用**。DoWhy Frontdoorの**識別だけで完了させず、対応する数値Estimatorと科学的受入**をPhase1で実装する。識別結果と推定結果は別契約。
- **SR03-D03／LATE（2026-11-01の明示採用）:** **Phase3初期提供＝A（Wald比をReference）＋B（2SLSにも対応）**。**C（条件付きIV向けDR／効率的LATE）は追加審議**。方式選択の個別判断は完了したが、弱IV頑健推論の具体方式、2SLS追加設計、科学Benchmark・Gate受入は未承認。
- **SR03-D05／EconMLの区間推定:** 0.17.0で未取得だった理由と、Ariadne連携による機能劣化かを検証するよう要求された。**前回試験はEconMLを独立スクリプトから直接呼んでおり、Ariadneへの新CATE Adapter組込みを経由していない。よって「Ariadneが機能をspoiledした」という因果的解釈には証拠がない。**

### 0.2. 証拠資料

- [SR-02実行証拠](20261101_sr02_backend_runtime_probe_results.md)／[SR-02の直接呼出しスクリプト](https://github.com/kousuke-ota-datascience/causal-atelier/blob/721fc9bf3e6d23b110618023ee2147648370453d/scripts/verification/enh_e11_sr02_probe.py)。
- [EconML 0.17.0 `metalearners/_metalearners.py`](https://github.com/py-why/EconML/blob/v0.17.0/econml/metalearners/_metalearners.py) — `SLearner/TLearner/XLearner.fit`は`inference=None`が既定、`bootstrap`を明示的にサポート。
- [EconML 0.17.0 `dr/_drlearner.py`](https://github.com/py-why/EconML/blob/v0.17.0/econml/dr/_drlearner.py) — `DRLearner.fit`は`inference='auto'`が既定。最終モデルとの組合せで推論可能性が異なる。
- [EconML 0.17.0 `inference/_inference.py`](https://github.com/py-why/EconML/blob/v0.17.0/econml/inference/_inference.py) — 最終モデルの`prediction_stderr`がないと、標準誤差を生成できず点推定しか返さない経路がある。
- [EconML公式Inference説明](https://www.pywhy.org/EconML/spec/inference.html) — Bootstrap、OLS/Statsmodels、Honest Forest BLBで異なる推論手段（公開文書は0.16系列であり、0.17のソースと区別）。
- Imbens & Angrist (1994), [Identification and Estimation of Local Average Treatment Effects](https://www.gsb.stanford.edu/faculty-research/publications/identification-estimation-local-average-treatment-effects)。
- [Angrist/Imbens方式を含むIVの方法論的整理](https://www.cambridge.org/core/journals/political-analysis/article/how-much-should-we-trust-instrumental-variable-estimates-in-political-science-practical-advice-based-on-67-replicated-studies/70A232CA0CD55FE8B97E93543CDD6361)（Just-identifiedなWald比と2SLSの一致）。
- [Lee & Porter (2026), AEA Journal of Economic Perspectives](https://www.aeaweb.org/articles?id=10.1257/jep.20251464) — 単一IV下の通常CI／弱IV頑健な推論の違い。**科学Benchmarkは別途必要**。

## 1. FrontdoorのPhase1提供範囲（オーナー採用）

### 1.1. 実装・受入の最低要件

1. `FRONTDOOR`の識別を満たすGraph・観測Mediator Mと支援仮定を受け付ける。前提はGraphから全て自動証明できるとはしない。
2. Phase1で**識別式だけでなく数値効果推定**を行う。最初の候補はDoWhy `frontdoor.two_stage_regression`。このEstimatorは**線形性・段階モデル仕様など追加の制約**を課すため、Frontdoor criterion成立と推定器妥当性を別判定する。
3. Target estimandを`ATE`、集団・介入コントラスト・Mの役割とMへの調整根拠を明示。媒介効果の自然直接／間接効果を、Phase1のFrontdoor総効果と混同しない。
4. **数値推定の既知真値・負例・CI可用性を受入までに科学Benchmarkへ**。Frontdoor identificationのみをPhase1完了と報告しない。
5. 現在のSR-02はFrontdoor識別API成功のみ。DoWhy 0.14の**数値推定実行・数値パリティは未試験**であり、「Phase1に含める」という判断と「既に動作」は別。

## 2. LATE初期推定器の比較・採用判断（A＋B採用、C追加審議）

| 選択肢 | 学術的Estimand／実装 | 長所 | 制約・推論 |
|---|---|---|---|
| **A：Wald比（最小Reference）** | 二値Zと二値A、無条件IV独立性・exclusion・relevance・monotonicity下で`Δ_Z E[Y] / Δ_Z E[A]`（`Δ_Z`はZ=1とZ=0の群平均差） | Complier LATEと直接対応。数値パリティ・既知真値fixtureが容易 | First-stageがほぼ0だと不安定。通常の比のCIは弱IVに脆弱。無条件IVが不正なDesignへそのまま適用しない |
| **B：2SLS（線形IV）** | IVとTreatmentを用いた二段階最小二乗（統計的分散推定は全段階を考慮） | 共変量／複数Instrument／線形IVへ拡張。既存エコシステム利用容易 | 一般の2SLS係数を**無条件にcomplier LATE／ATEと同一視しない**。共変量付きでは重み付けされた局所効果等になり得る |
| **C：共変量調整付きDR／効率的LATE** | Instrument割当確率・Outcome/Treatment回帰、cross-fitting等を用いて条件付きIVのcomplier LATEを構成 | IVの独立性が共変量に条件付けてのみ成立するDesignに対応し得る | 識別式・モデル・positivity・推論・二重頑健性の適用条件を方法別実装／独立Benchmarkで検証する必要 |

**重要:** 二値Z・二値A・共変量なしのJust-identifiedな場合、**Wald比と2SLSの点推定値は代数的に一致**する。BがAと無条件に独立した科学方式ではない。**CはDRIVと同じではない**。EconML DRIVの連続Treatmentに対するIV heterogeneous effectを、二値Z/Aのcomplier LATEへ自動同定しない。

**オーナー採用（2026-11-01）:** **AをPhase3の二値Z/A・complier LATEの基準推定器、Bを線形IVの追加推定器として初期提供**。Cは**採用ではなく追加審議**。Phase2のDRIVは既存の必須候補のまま**IV異質効果の別契約**で維持する。独立familyの採否・比較・科学的定義の管理先は[ファイルD01](20261101_sr03_iv_heterogeneous_estimand_decision.md)とし、本書はLATE A＋BおよびEconML推論の比較・証拠を管理する。2SLSでの一般の共変量・複数IV対応が同じLATEを推定するとの自動保証はしない。

**弱IV推論の必須検討（採用Method A/B共通）:** Reduced formとFirst-stage効果・SE・Instrument supportを報告し、**通常の比／2SLS正規近似CIが弱IV下で妥当とは限らない**ことを結果に表す。**D03-2 I2によりAR反転を初期基準の弱IV頑健推論として2026-11-05に採用済み**（[詳細](20261101_sr03_d03_remaining_2sls_weak_iv_review.md)、G2 schema・coverageは未承認）であり、非有界／非連結集合を有限な上下限へ偽装しない。単一の`F>10`規則でexclusion・independence・monotonicityを証明しない。正しいIV用SEと通常OLSの二段階SEを区別する。具体Method・閾値・科学的被覆率はGate07で決定する。

### 2.1. オーナーに求める判断

`SR03-D03`：**A＋B採用済み**。**D03-1の初期2SLS範囲はS2（B0＋B1）として2026-11-05に追加採用済み**。**D03-2 I2（AR反転）も2026-11-05に採用済み**。残る判断は**(iii) CIの非有界／非連結等の型と受入基準、(iv) Cの追加審議時期・責任者**。S2の正確な保証条件・非採用案・実証条件は[残余D03審議ファイル](20261101_sr03_d03_remaining_2sls_weak_iv_review.md)で一元管理し、ここに重複記載しない。Cの採否は未決。

**D03残余の審議責務:** 2SLS初期保証範囲（**S2採用済み**）、弱IV頑健推論、confidence setの型、Cの再審議責任は[SR03-D03残余技術審議](20261101_sr03_d03_remaining_2sls_weak_iv_review.md)を詳細根拠・選択肢比較の唯一の管理先とする。本書の当初A/B/C比較・採用事実・EconML CI実測は維持する。**I2は採用済み、G2/C1はオーナー採否待ち**であり、科学Benchmarkも未実施。

### 2.2. 識別対象・適格性・拒否条件（個別採用に伴う明確化）

- **基本Estimand:** 二値Instrument Zと二値Treatment Aについて、`A(1)>A(0)`のcomplier集団における`E[Y(1)-Y(0)|complier]`。基本の無調整Wald比は**Instrument independenceが無条件に成立するDesign**を対象とする。Assumptionの`relevance/independence/exclusion/monotonicity/consistency`を研究者の根拠として保存する。これらは観測データで自動証明できない。
- **2SLSパリティの基本Fixture:** 切片あり・単一二値Z・二値A・共変量なし・just-identifiedで**Wald比＝2SLSの点推定値**。2SLS拡張時の共変量、複数Z、連続Aには別のEstimand／支持仮定・明示的な対象ラベルを設け、complier LATE／ATEへの黙示変換を禁じる。
- **First Stageの数値的・科学的境界:** `Δ_Z E[A]`が0の比は定義できない。小さい場合も通常の比／2SLSのWald型区間のカバレッジは保証されない。Instrumentationの弱さと、独立性・除外制約等の違反は別種の不確実性として記録する。
- **弱IVへの推論:** First-stage効果・SE・Instrument support・弱識別warningを必須検討し、**AR反転方式はD03-2 I2として採用済み**。具体的な数値実装、科学的検証、区間形状のschemaは別審査する。有限区間しか表現できないResult契約に、非有界・非連結confidence setを無理に押し込まない。
- **負結果:** invalid instrument、first stage 0、推定対象不一致、弱識別下の通常CI不適格、仮定根拠不足に、それぞれ異なる理由codeを付与する案。**原著で導かれる識別仮定とソフトウェア上の機械検証を混同しない**。

**詳細契約・fixture:** [SR-03科学契約 §3.1](20261101_sr03_identification_estimand_estimator_contract_review.md)。

## 3. EconML「区間推定不可」の原因（一次ソースと直接呼出しによる切り分け）

| Estimator | SR-02での設定 | 0.17.0ソースで確認した仕様 | 判断 |
|---|---|---|---|
| `SLearner`／`TLearner`／`XLearner` | `fit(...)`、`inference`未指定 | `fit(..., inference=None)`が既定。**bootstrap明示指定をサポート** | 今回はCI推論を起動していない。ライブラリ全体のCI機能欠如ではない |
| `DRLearner` | `model_final=RandomForestRegressor`、`inference`未指定（既定`auto`） | `auto`は最終モデルからの`prediction_stderr`等の条件に依存。sklearnの当該RandomForestRegressorはそのAPIを提供しない | 今回のモデル選択で自動推論が点推定のみに留まる条件。**別の最終モデル／bootstrapを検証する** |
| `LinearDML`／`CausalForestDML`／`ForestDRLearner`／`DRIV` | 既定の推論条件 | SR-02でfinite interval取得 | **API取得の成功のみ**。CI coverageを証明しない |

**重要な切分け:** SR-02では`scripts/verification/enh_e11_sr02_probe.py`が`from econml...`したインスタンスの`fit/effect/effect_interval`を直接呼んだ。Ariadneの新規CATE実装はまだ無く、**Ariadneによる区間推論機能の劣化・損失と評価できる証拠が存在しない**。

**実証結果（2026-11-01）:** [GitHub Actions Run #41272111463](https://github.com/kousuke-ota-datascience/causal-atelier/actions/runs/41272111463)／[EconML単独のMethod別証拠](https://github.com/kousuke-ota-datascience/causal-atelier/issues/14#issuecomment-6553260358)／[3ライブラリ同時環境の証拠](https://github.com/kousuke-ota-datascience/causal-atelier/issues/14#issuecomment-6553261944)。EconML 0.17.0／Python 3.12.15で`BootstrapInference(n_bootstrap_samples=12,n_jobs=1)`を明示した場合、**DRLearner・SLearner・TLearner・XLearnerの4方式すべてで`effect_interval`がFINITEとなり、API smokeにPASS**。初回の`inference=None/auto`構成では取得できなかった区間が、**推論方式を明示することで取得可能**と実証された。Ariadneの新規CATE Adapterは使っていない。**12反復はCI計算経路の確認専用であり、被覆率・interval calibration・必要bootstrap反復数の科学受入を意味しない。**

## 4. 適用範囲と未完了事項

- **オーナー判断済み:** Frontdoor数値推定までPhase1のNとして提供。
- **オーナー判断済み:** Phase3 LATE初期は**A＝Wald比＋B＝2SLS**。Cは追加審議とし、初期採用Methodには含めない。
- **未確定:** **I2 AR方式は採用済み**。B1の具体的な識別・AR実装と科学検証、Cの後続審議・責任者、EconMLのCI必須水準・Method別採用推論。**D03-1のS2（B0＋B1）という初期提供範囲の判断自体は完了。**
- **追加実証:** EconML 0.17.0の4方式でBootstrap区間の有限数値出力を確認（API smoke）。同時導入環境で既存回帰27件PASS。
- **未実証:** DoWhy Frontdoorの数値推定／CI、IV/LATEの数値真値・弱IV推論、EconML Bootstrap CIの**被覆率・校正・適切な反復数**。
- **全体承認ではない:** `00_04`の68行と`02`の`PENDING_FULL_CONCEPT_APPROVAL`、SR-03全体の方法判定待ちは維持。
