# ENH-E11 — SR-03 Frontdoor採用判断・LATE推定器の選択肢・EconML区間推定の原因調査

**作成日:** 2026-11-01（JST）  
**文書区分:** `working_notes`。オーナーの個別決定と未決事項を切り分けた技術検討。正本FR/AR・Gate承認を代替しない。  
**判断状況:** `FRONTDOOR_NUMERIC_PHASE1_ACCEPTED / LATE_ESTIMATOR_OPTIONS_PREPARED / ECONML_ROOT_CAUSE_IDENTIFIED / INTERVAL_BOOTSTRAP_API_PASS`。

## 0. INTRODUCTION

### 0.1. オーナーが明示した判断

- **SR03-D02／Frontdoor:** 「Phase 1に数値推定まで含める」を**採用**。DoWhy Frontdoorの**識別だけで完了させず、対応する数値Estimatorと科学的受入**をPhase1で実装する。識別結果と推定結果は別契約。
- **SR03-D03／LATE:** 初期推定器は未採用。選択肢を比較して提示するよう要求された。本メモは候補・推奨案であり決定記録ではない。
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

## 2. LATE初期推定器の候補（オーナー未決）

| 選択肢 | 学術的Estimand／実装 | 長所 | 制約・推論 |
|---|---|---|---|
| **A：Wald比（最小Reference）** | 二値Zと二値A、無条件IV独立性・exclusion・relevance・monotonicity下で`Δ_Z E[Y] / Δ_Z E[A]`（`Δ_Z`はZ=1とZ=0の群平均差） | Complier LATEと直接対応。数値パリティ・既知真値fixtureが容易 | First-stageがほぼ0だと不安定。通常の比のCIは弱IVに脆弱。無条件IVが不正なDesignへそのまま適用しない |
| **B：2SLS（線形IV）** | IVとTreatmentを用いた二段階最小二乗（統計的分散推定は全段階を考慮） | 共変量／複数Instrument／線形IVへ拡張。既存エコシステム利用容易 | 一般の2SLS係数を**無条件にcomplier LATE／ATEと同一視しない**。共変量付きでは重み付けされた局所効果等になり得る |
| **C：共変量調整付きDR／効率的LATE** | Instrument割当確率・Outcome/Treatment回帰、cross-fitting等を用いて条件付きIVのcomplier LATEを構成 | IVの独立性が共変量に条件付けてのみ成立するDesignに対応し得る | 識別式・モデル・positivity・推論・二重頑健性の適用条件を方法別実装／独立Benchmarkで検証する必要 |

**重要:** 二値Z・二値A・共変量なしのJust-identifiedな場合、**Wald比と2SLSの点推定値は代数的に一致**する。BがAと無条件に独立した科学方式ではない。**CはDRIVと同じではない**。EconML DRIVの連続Treatmentに対するIV heterogeneous effectを、二値Z/Aのcomplier LATEへ自動同定しない。

**技術側の推奨（未採用）:** **AをPhase3のLATE最小Reference、BをIV拡張・パリティ実装として採用する案**。Cは追加審議し、Phase2のDRIVは既存必須候補のまま別契約で維持する。

**弱IV推論の必須検討:** Reduced form、First-stage効果とSE、Instrument support、通常の比のCIに加え、弱識別下でのAnderson–Rubin等の**頑健なconfidence set**を検討する。単一の`F>10`規則でvalidityを認定しない。推論方式、非有界な区間・confidence setの扱い、シミュレーション許容基準はGate07で固定する。

### 2.1. オーナーに求める判断

`SR03-D03`：**A＋BをPhase3初期提供方式にするか**、Aのみを初期提供とするか、条件付きIV向けのCまで同じPhase3スコープに含めるか。提案の採否とCの次のowner/Issueは未確定。

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
- **オーナー判断待ち:** LATEの初期推定器（A/B/C）と、EconMLのCI必須水準・Method別採用推論。
- **追加実証:** EconML 0.17.0の4方式でBootstrap区間の有限数値出力を確認（API smoke）。同時導入環境で既存回帰27件PASS。
- **未実証:** DoWhy Frontdoorの数値推定／CI、IV/LATEの数値真値・弱IV推論、EconML Bootstrap CIの**被覆率・校正・適切な反復数**。
- **全体承認ではない:** `00_04`の68行と`02`の`PENDING_FULL_CONCEPT_APPROVAL`、SR-03全体の方法判定待ちは維持。
