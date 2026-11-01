# ENH-E11 — Negative Control実装計画（条件付き提供・CLI-only）

**文書区分:** `working_notes`／実装計画**案**。正規Workflowの01〜05、Gate 06/07、Work Package契約を代替しない。  
**策定日:** 2026-11-01（日本時間）  
**対象:** `00_04_phase1_to_phase3_cli_scope_proposal.md` のP1-15・X-04、#16、技術審査SR-06  
**方針の根拠:** オーナーとの2026-11-01の会話で、「**適切なNegative Controlを指定できる研究に対し、科学的に解釈可能な反証分析を提供する**」という**原則を採用**。個々のMethod・正規FR/AC・Gateの承認を含まない。  
**状態:** `IMPLEMENTATION_PLAN_DRAFT / PRINCIPLE_ACCEPTED / METHOD_AND_GATE_NOT_APPROVED`  
**現行ソース参照SHA:** `ac580920ec68e32f58ea82236de0f97e1108f33a`。新規コード・科学的受入実行は未実施。

## 0. INTRODUCTION

### 0.1. 計画の目的

Ariadneの観測研究において、分析者が**科学的に妥当と考える観測された負の対照**を指定した場合に、期待する帰無関係とデータ上の関連との矛盾を診断し、交絡・選択バイアス・測定バイアス・モデル不適合等の可能性を報告できるようにする。

**Negative Controlは必ず実行する工程ではない。** 対照が設定されていない研究、または有効な対照を正当化できない研究で「Negative Control必須」を根拠に科学的実行を失敗させない。一方、**利用者が実行を明示要求した場合**は、適格性と結果を再現可能な形で出力する。未実施・不適格・検出なしは異なる状態とする。

### 0.2. 調査資料と科学的限界

- Lipsitch, Tchetgen Tchetgen & Cohen (2010), *Negative Controls: A Tool for Detecting Confounding and Bias in Observational Studies*, [Epidemiology／PMC全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC3053408/), DOI: [10.1097/EDE.0b013e3181d61eeb](https://doi.org/10.1097/EDE.0b013e3181d61eeb)。**因果効果がないはずの関係**と**バイアス構造の共有（U-comparability）**が両立することの必要性。
- Shi, Miao & Tchetgen Tchetgen (2020), *A Selective Review of Negative Control Methods in Epidemiology*, [PubMed](https://pubmed.ncbi.nlm.nih.gov/33996381/)。DetectionとCorrectionは区別する。
- [20261101_negative_control_unobserved_confounding_method_review.md](20261101_negative_control_unobserved_confounding_method_review.md)：NCE/NCOとOLS partial R²の科学的方式を分離。本書は**NCE/NCO検出の実装計画のみ**。Sensitivity実装計画は別に作る。
- 現行`src/ariadne/scientific/refutation/adapter.py`、`src/ariadne/interfaces/cli/{config_schema,scientific_stage}.py`、`src/ariadne/product/domain/analysis_spec.py`、`src/ariadne/causal/inference/estimators/linear_model.py`、`tests/product/test_cli_contract.py`、`tests/scientific_benchmarks/test_enh_e1a_acceptance.py`（上記SHA）。

**非目的:** 残余交絡がないことの証明、対照変数の妥当性の自動証明、検出された関連のバイアス源の同定、バイアス量の推定・補正、近接因果推論（proximal causal inference）による識別・推定、一般のCATE/IV/DiDへの適用保証。

## 1. ユーザー要件と利用シナリオ

### 1.1. 提供する価値（When／Question／Workflow／Outcome）

**シナリオ:** キャンペーンAが購入金額Yを変えたか調べる。対象者選定の交絡が懸念されるが、キャンペーンによって変わり得ない介入前の購入金額Wが測定されている。分析者は、Wを対照に使える時間・因果・共有バイアス上の根拠と、事前指定した調整集合Cを記録する。

**分析の問い:** 「AとWの間に、予想外の条件付き関連が残っているか。その結果を本来のA→Y推定の信頼性評価にどう解釈すべきか。」

**CLI利用:** 分析者が`ariadne-refute`向けの明示的な`NEGATIVE_CONTROL_OUTCOME`設定を作成し実行する。結果として係数・不確実性・帰無仮説の説明・対照変数の選定根拠・適格性warning・Manifestをローカルに保存する。**手法が設定されない通常の推定では自動実行しない。**

**科学的限界:** WがAから影響されないという前提だけでは十分ではない。WとYが懸念バイアス構造を共有すること、条件付きNullが科学的に妥当であることも必要。過去の購入金額Wは選定プロセスそのものの変数になり得るため、`W ~ A + C`の関連を直ちに「未測定交絡がある」と読まない。

### 1.2. 方式の最小対象

| Method ID（提案） | 明示入力 | 事前指定する統計的帰無 | 初期Reference適用 |
|---|---|---|---|
| `NEGATIVE_CONTROL_OUTCOME`（NCO） | 介入A、主Outcome Y、観測対照Outcome W、調整集合C_W、時間情報、null／共有バイアスの根拠 | **AがWを因果的に変えない**という設計に整合する条件付き関連Null。初期検査は`W ~ A + C_W`のA係数=0 | Aは数値の2値、Wは連続、C_Wは事前指定した数値共変量 |
| `NEGATIVE_CONTROL_EXPOSURE`（NCE） | 介入A、主Outcome Y、観測対照Exposure Z、調整集合C_Z、時間情報、null／共有バイアスの根拠 | **ZがYへ因果的に影響しない**という設計に整合する条件付き関連Null。初期検査は`Y ~ Z + C_Z`のZ係数=0 | Zは数値（2値または連続）、Yは連続、C_Zは事前指定した数値共変量 |

**注意:** `NCE: Z → A → Y`等の間接経路があり得る場合、単純なZ–Y係数=0を期待してよいとは限らない。また、AをC_Zへ機械的に追加するとcollider/mediator調整の問題を生む。**実際のDAGで帰無を正当化できる設計に限定**する。全Negative Controlが条件付き回帰のNullとして表現可能だとは主張しない。

## 2. 必須の科学的・契約不変条件

### 2.1. Opt-inと実施状態

1. **任意実行:** 通常のIdentification/EstimationにNCE/NCOを必須化しない。設定なしは`NOT_REQUESTED`相当として**レポートに記録可能**だが、NC結果を捏造せず、Scientific Gate失敗にしない。
2. **実行要求時:** `method`と適用対象の観測Z/W・null仕様・conditioning set・根拠・time order・検査対象datasetを明示的に要求。名前だけ指定して「自動で有効」と扱わない。
3. **条件を満たさない時:** `NOT_APPLICABLE`／`REQUIRES_REVIEW`等の**科学的な負結果**と理由を出す。技術障害・ファイル破損・API失敗は別の技術エラー。
4. **分析者の宣言≠証明:** nullやU-comparabilityの根拠は研究者の設計宣言であり、Ariadneが観測データから自動証明できない。DAGから観測可能な構造矛盾をチェックしても、未観測交絡の不存在・対照の妥当性は確定しない。

### 2.2. 出力と判定の科学的意味

- `DEVIATION_DETECTED`（事前指定したNullとの統計的矛盾のシグナル）、`NO_DEVIATION_DETECTED`（今回の検査で矛盾は検出されない）、`INCONCLUSIVE`（検出力・精度等の制約）、`NOT_APPLICABLE`、`REQUIRES_REVIEW`の**意味上の区分**を維持する。これは**新enumの確定ではない**。
- 帰無棄却／非棄却は、対照の因果的妥当性を保証せず、主効果の因果的妥当性のPASS/FAILでもない。**非有意を「交絡なし」と翻訳しない**。不確実性、推定された関連の大きさ、サンプル、powerの限界を併記する。
- Negative Controlの係数は**因果推定量でも主効果のバイアス量でもない**。主Estimand／Main Estimation Resultとは別Resultとして保存し、元の推定値を上書きしない。
- 検定の閾値`alpha`と、事前指定した臨床的・実務的意味のある差の基準は別物。効果量・CI・検査時点・多重検査の有無を記録し、解析後の好都合な対照選択を許容していたか明示する。

### 2.3. 適格性チェックの範囲

| 検査 | 機械的に判定できる内容 | 人の科学的判断に残る内容 |
|---|---|---|
| データ列 | Z/W、A/Y、Cの存在・型・単位・欠測・非定数・観測数 | 対照が共通バイアスの適切なプローブか |
| 行列・推論 | design matrix rank、残差df、共線性、標準誤差の有限性、群support | OLS加法/線形・独立観測等のモデル妥当性 |
| 時間・Graph | 明示された時間情報に反するpost-treatment指定、固定Graph内の明示因果経路など | Graphの不完全性、未知の矢印、anticipation、Nullを成立させる因果構造 |
| 帰無と調整 | 必須説明文字列・集合の整合、調整集合の重複・同一列の誤用 | Conditioningでcollider/mediator biasが生じないこと、Nullの適切さ |
| Provenance | 実行版・dataset/graph hash・seed・設定・変更履歴の記録 | 変数選定の実質的な科学的正当性 |

**現行線形回帰utilityの注意:** `fit_linear_regression`は`dof = max(n - p, 1)`としており、singular/df不足をエラーにする設計ではない。NCアダプタでは**fit前にfull column rankと`n - p > 0`を独立検査**し、無意味なSEを返さない。主Estimatorの既存挙動をこの拡張のために黙って変更しない。

## 3. 技術的な実装境界

### 3.1. 既存コードと変更候補

| 実装対象 | 現行状態 | 実装案 |
|---|---|---|
| `scientific/refutation/adapter.py` | `PLACEBO_TREATMENT`／`DATA_SUBSET`、数値のupstream効果推定値必須 | **NC専用strategy/serviceを分離**。観測データと研究デザイン・nullを入力とする。元推定値の有無をNC科学的実行の絶対前提にしない |
| `product/ports/scientific_core.py` | `RefutationInput`が`base_result: dict`必須 | 既存2方式の後方互換を保った**方法別input契約**。NCは`upstream_result`をoptional referenceとできる案をArchitecture Reviewで比較 |
| `interfaces/cli/config_schema.py` | Refutation CLIは2方式のみのLiteral | 新2方式を**版付きmethod discriminator**として許可し、mode-specific strict fieldsを定義。既存2.0設定の互換性を保持 |
| `product/domain/analysis_spec.py` | REFUTATION `operation_spec`の許可fieldはPlacebo/Subsets | NC別`negative_control_spec`（対照名、Null、C、time、理由、モデル・Inference）を条件付きで許可。unknown fieldは既存通り拒否 |
| `causal/inference/estimators/linear_model.py` | 低レベルOLS・HC0〜HC3・normal approximationが利用可能 | NCの基本回帰に**再利用可能かを先に検証**。full rank/df check、選択したcovariance/CIの説明をNC側で付加 |
| `interfaces/cli/scientific_stage.py`／Manifest | upstream Resultを必須読込、既存科学statusとlocal成果物 | NC経路のoptional upstream、方法別負結果、null根拠・hash、warning、dataset roleの安全な記録を追加 |
| `tests/scientific_benchmarks/`／`tests/product/test_cli_contract.py` | 既存RefutationとCLIの受入資料あり | NC独立fixturesと旧method互換の回帰を追加 |

**設計上の選択:** 新CLI entrypointを無制限に追加せず、当面は`ariadne-refute`の**明示的NC method**として検討する。旧CLI v2.0の`upstream_result`必須性が障害になるため、旧Methodの既存設定を壊さず、**新Methodに限りupstreamを任意とする**代替案を仕様承認時に比較する。正規schemaの版番号はこの段階で凍結しない。

### 3.2. ConfigとResultの意味上の草案

**提案Input（概念例・現行CLIでは実行不可）:**

```yaml
operation: REFUTATION
method: NEGATIVE_CONTROL_OUTCOME
dataset: path/to/observational.csv
analysis_spec:
  treatment: campaign_exposure
  primary_outcome: post_purchase
  negative_control:
    variable: pre_purchase
    control_type: OUTCOME
    expected_null: "coefficient(A in W ~ A + C) = 0"
    conditioning_set: [customer_age, pre_period_segment]
    selection_rationale: "pre-treatment outcome; reviewed for outcome comparability"
    shared_bias_rationale: "hypothesized targeting propensity influences A and W/Y"
    time_order_rationale: "W measured strictly before campaign"
  diagnostic_model: linear_ols
  inference:
    covariance: HC3
    reference_distribution: asymptotic_normal
    alpha: 0.05  # 計画例。正式閾値ではない
```

**提案Result（意味上の必須field）:** `method`、`control_variable`、`control_type`、`null_statement`、`conditioning_set`、`selection_rationale`、`shared_bias_rationale`、`time_order_rationale`、`model_spec`、`coefficient`、`standard_error`、`confidence_interval`、`p_value`、`alpha`、`n_input/n_complete`、`rank/df`、`scientific_disposition`、`limitations`、`upstream_reference(optional)`、`data/graph/config/backend_hash`。

**注意:** 例中`alpha:0.05`は提案configの使い方を示す**例示値**であり、科学的受入閾値や単一データでのPASS条件を決定していない。Resultの`scientific_disposition`は既存`ScientificStatus`へのmappingを設計時に確定する。Null非棄却が`PASSED_CAUSAL_VALIDITY`になるfieldは禁止する。

## 4. 実装Work Package候補（06/07の正式契約前）

| WP候補 | 主要作業と依存 | 成果物と終了条件 |
|---|---|---|
| **NC-WP00：Scientific Design** | 利用者方針と先行方法メモを入力。NCE/NCOのNull・共有バイアス・適用可能範囲を確定 | 事前登録に相当するDesign入力・拒否条件・Method互換行列のレビュー（まだ人の承認待ち） |
| **NC-WP01：Domain/Port Contract** | WP00完了後。Method別strict schema・optionality・Result/status・Manifest設計 | 旧Placebo/Subsetsと新NC入力の互換性、unknown field拒否、Null根拠の非空性をContract Testで示す |
| **NC-WP02：Eligibility** | WP01後。列／型／time／Graph上の明示矛盾／full rank/df／sample／null declarabilityの判定 | valid/invalid両経路の科学的負結果が機械テストできる。**対照の真の妥当性を自動認定しない** |
| **NC-WP03：NCO/NCE Diagnostics** | WP02後。条件付き線形回帰・HC3区間・係数とNull評価、各方式のresult | 事前指定したNullに対応する係数とSE/CIが参照実装と整合。主ATE/ATTを上書きしない |
| **NC-WP04：Local CLI/Artifacts** | WP01〜03後。explicit opt-in、optional upstream、local JSON/Manifest/exit、後方互換 | opt-inなしで現行分析を変えない。opt-in時の結果・非適用・provenanceが再現できる |
| **NC-WP05：Scientific Benchmarks** | WP03〜04後。valid-null、bias、invalid-control、negative result、coverage・回帰テスト | 統計試験と構造的失敗を別々に判定。効果量・false-positive rate・coverageは**事前固定された閾値**で評価 |
| **NC-WP06：Independent Verification** | WP01〜05の独立試験後。06/07でfreezeした条件を別主体で再検証 | Gate 07の独立テスト・Scientific status・成果物・承認証跡を保持。完了を本メモだけで宣言しない |

**並行化:** WP01のschemaとWP02のEligibility test design、WP03のReference numerical fixture設計は科学仕様が固定された後に一部並行できる。ただし、Methodの意味が未決のまま異なる実装を並走させない。

## 5. 科学的検証と受入基準の候補

### 5.1. 単体・契約・既知機構テスト

| Test候補 | データ／状況 | 期待する科学的振る舞い |
|---|---|---|
| `NC-T01` | Negative Control未指定で通常の推定を実行 | 既存CLI経路が後方互換。NCは**未実行**であり、エラーにも「交絡なし」にもしない |
| `NC-T02` | 事前指定NCO、A→W経路なし、設計上有効・null真のsimulation | NCO係数のnull分布、区間被覆、第一種過誤率を複数seedで評価。個別p値が必ず非有意になることを要求しない |
| `NC-T03` | NCOとA/Yが交絡Uを共有し、A–Wに予期しない関連が発生 | バイアスの**検出力曲線**と係数・CIが再現。単一標本で必ず有意になることは要求しない |
| `NC-T04` | 事前指定NCE、Z→Yの因果経路なし、共通バイアス無し | Null分布の校正・CI被覆がReferenceと整合 |
| `NC-T05` | NCEとA/Yが共通Uに関連し、Z–Yにnullからの逸脱が出る | 検出力を比較し、真のU有無の自動証明をしない |
| `NC-T06` | Z→A→Y、WがAの子孫、明示DAGにNull矛盾等 | データ上関係があっても**無根拠な「未測定交絡検出」へ短絡しない**。拒否・要レビューにする |
| `NC-T07` | Z/W欠落、conditioning不整合、rank欠損、df不足、非有限SE | `NOT_APPLICABLE`／`REQUIRES_REVIEW`相当＋reasonを出力。無意味な係数/CIを生成しない |
| `NC-T08` | 既存`PLACEBO_TREATMENT`／`DATA_SUBSET`とCLI v2.0 | 旧Method・入力・成果物の既存契約が不変 |
| `NC-T09` | Dataset hash／Graph／説明・モデル指定を変えて再実行 | 設定の変化がManifestへ反映。旧結果を暗黙に再利用しない |
| `NC-T10` | 結果の非有意、幅広いCI、低検出力、複数対照 | 「交絡なし」と表示しない。弱い検出力・多重検査・事後的対照選定の警告 |

### 5.2. 測定すべき指標（閾値はGateで承認後に固定）

実装テストでは少なくとも`Type-I error`、`CI coverage`、`power vs bias strength`、`estimate/reference parity`、`finite/rank/df validity`、`valid/invalid classification`、`local manifest reproducibility`、`existing refutation regression`を測定する。**この文書では数値許容閾値・試行回数・基準SHAを捏造しない**。実装開始前に独立検証担当がfixture・seed・alphaと判定を承認する。

## 6. 未決事項・依存・停止条件

### 6.1. オーナー・Architecture Reviewに提出する決定

| Decision | 推奨案 | 未決の判断・証跡 |
|---|---|---|
| `NC-D01` | NCは**任意実行**。適切な対照を指定できる研究でのみ診断を実行 | 原則は2026-11-01に受け入れ済み。これを正本の規定文とする承認・改定は未実施 |
| `NC-D02` | まず**観測NCO／NCEの両方**を、連続Outcomeの条件付き線形検査として提供 | 2方式とも必須Capabilityとするか、方法別適用範囲／非線形拡張をどう定義するか |
| `NC-D03` | 明示的なnull／共有バイアス根拠／C/timeをMethodごとに要求。データのみから「valid control」と自動判定しない | Graph矛盾検出の厳格度と人のレビュー権限 |
| `NC-D04` | 初期Referenceは既存OLS utility再利用・HC3等の分散指定を明示 | 単位独立性・クラスタ／時系列の場合の非適用、Referenceの数値パリティと対応版 |
| `NC-D05` | 既存`ariadne-refute`をMethod別に拡張する案 | upstream optional・config schema version・既存Resultの互換性 |
| `NC-D06` | Negative ControlはBias **detection**のみ | bias correction/proximal inference・自動対照探索を後続に送る判断 |

### 6.2. 依存条件と変更禁止事項

- **今回の計画で承認済みと言えるのは、ユーザーが明示した機能目的の原則のみ**。Methodの数、モデル、CLI fields、ScientificStatus、Benchmark閾値、Work Package/Gateの名前・freezeは提案状態。
- 既存Product側GAP-C01〜C04やcanonical lineageは、NC Local Manifestを追加しても自動的に閉鎖しない。
- 研究者の「これがvalid control」という宣言を「統計的に検証された事実」として保存しない。Declared assumptionsとmachine-checked factsの両方をResultに残す。
- 参照元00_04・要件改定03に本計画の**提案内容と採否未承認状態**を記録し、正式承認後に02→03/04→Gate 06/07へ展開する。

## 7. 次のアクション

### 7.1. 実装着手前に進める作業

1. `NC-D02〜D06`と、`NC-D01`の正式な正本文書化範囲をHuman ownerに審査してもらう。
2. Method別Null／conditioning setの可否に関するScientific DesignをArchitecture Reviewに付す。
3. FR/NFR/AR差分を03へ、Domain/CLI/Result/Manifestの設計を04へ書き込み、既存方法との互換性をレビューする。
4. 承認されたAC・数値閾値・test matrixからGate 06/07と正式なWPを確定し、その後にCoding／独立テストへ進む。

**本書の完成を以て、プログラム実装・Scientific Benchmark PASS・Gate承認は宣言しない。**
