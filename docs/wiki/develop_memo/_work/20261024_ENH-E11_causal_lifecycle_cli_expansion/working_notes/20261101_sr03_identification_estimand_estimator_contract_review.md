# ENH-E11 — SR-03 Identification × Estimand × Estimator 契約設計案

**作成日:** 2026-11-01（JST）  
**文書区分:** \`working_notes\`／科学的意味・互換性・設計差分の**技術提案**。正規Workflow文書、オーナー承認、Gate 06/07 freezeではない。  
**対象:** SR-03、00_04 P1-06〜08・P1-10・P2-01〜14・P3-12/15、UC-02/04/08、Issue #16/#18/#22/#24。  
**判定:** \`SR03_DESIGN_PROPOSAL_PREPARED / HUMAN_METHOD_APPROVAL_PENDING / IMPLEMENTATION_NOT_STARTED\`。  
**観察Baseline:** \`prototype/ariadne_mvp\` / \`721fc9bf3e6d23b110618023ee2147648370453d\`（調査開始時。最新の正式受入SHAではない）。  
**実測根拠:** [SR-02 Backend smoke結果](20261101_sr02_backend_runtime_probe_results.md)、[Run #41270427977](https://github.com/kousuke-ota-datascience/causal-atelier/actions/runs/41270427977)。DoWhy 0.14／EconML 0.17.0はAPI smokeに合格したが、Frontdoor/IV数値推定・科学Benchmarkは未実施。

## 0. INTRODUCTION

### 0.1. 目的と禁止する誤変換

研究者の「**誰に対する、どの介入比較の、何の効果**」というCausalQuestionを先に定義し、その識別を正当化できるGraph/Assumptionから、推定可能なEstimatorにだけ接続する。ライブラリのAPIやResultのフィールド名をEstimandの意味の代わりにしない。

**禁止事項:** (a) IVを指定しただけでATE／LATEを自動認定、(b) DoWhyの\`nonparametric-ate\`という内部labelを、IVで推定された結果の対象集団の証拠として表示、(c) \`REQUIRES_REVIEW\`のPAG/CPDAGをDAGへ黙って方向付け、(d) CATEを一般の予測スコア差に置換、(e) \`effect()\`が動いたことを\`effect_interval()\`利用可能／科学的に妥当と認定、(f) 欠けた推論区間をゼロ幅や架空の標準誤差で補完。

### 0.2. 科学的方法の一次根拠

- [DoWhy 0.14公式API](https://www.pywhy.org/dowhy/v0.14/dowhy.html)：Backdoor/Frontdoor/IVの識別と\`backdoor.linear_regression\`、\`frontdoor.two_stage_regression\`、\`iv.instrumental_variable\`等の推定APIを**明確に別段階**として規定。API文書に存在するだけではAriadneのfit/CIが検証済みにならない。
- [DoWhy 0.14 Simple Example](https://www.pywhy.org/dowhy/v0.14/example_notebooks/dowhy_simple_example.html)：識別と推定の分離。\`proceed_when_unidentifiable=True\`は交絡を無視して処理するオプションであり**Scientific PASSの根拠に使わない**。
- [Imbens & Angrist (1994), *Econometrica*, 62(2), 467–475](https://www.gsb.stanford.edu/faculty-research/publications/identification-estimation-local-average-treatment-effects)：一般のvalid IVがATEを自動識別するわけではなく、単調性条件下ではcomplierのLATEを識別すること。
- [EconMLのunconfoundedness下での推定器群](https://www.pywhy.org/EconML/spec/estimation.html)、[IV推定器群](https://www.pywhy.org/EconML/spec/estimation_iv.html)：Backdoor型CATEとIV型異質効果の識別前提は異なる。**公開ドキュメントが0.16系の場合、採用候補0.17.0に対する実装確認とは分ける**。
- [Hernán & Robins, *Causal Inference: What If*](https://www.hsph.harvard.edu/miguel-hernan/causal-inference-book/)：Consistency、Exchangeability、Positivity、対象集団の明示。

## 1. 現行コード・SR-02との照合（事実）

### 1.1. 既存Contract

| 層 | 現行の事実 | SR-03で必要な差分 |
|---|---|---|
| \`product/domain/analysis_spec.py\` | \`causal_question.estimand\`は\`ATE/ATT\`、\`identification_strategy\`は\`RANDOMIZED/BACKDOOR\`のみ許可 | \`CATE\`／\`LATE\`（必要に応じCLATE/局所IV異質効果）とFrontdoor／IVを、**Versioned Schemaと条件別Validator**として追加 |
| \`product/ports/scientific_core.py\` | \`IdentificationInput\`と\`EstimationInput\`は別。後者は\`upstream_result: dict\`を持つ | 科学的な\`IdentifiedEstimand\`の識別子・対象・assumptions・許可Estimatorを上流Resultとして固定し、強いtyped envelopeを提案 |
| \`scientific/identification/adapter.py\` | Native Randomized/Backdoorのみ。DAG以外は\`REQUIRES_REVIEW\`。IdentificationとEligibilityが別Result | DoWhy optional識別を**明示的なstrategy**で追加。DAG／PAGなどのorientation未確定を保存 |
| \`scientific/inference/adapter.py\` | 2値Treatment、ATE/ATT、DAG、diff/OLS/IPW/AIPWのみ | Methodごとの処置型・計算対象・conditional IV／CATE・必要inputを分離。既存推定器とResultを回帰保護 |
| \`interfaces/cli/estimation.py\` | upstream識別statusに\`IDENTIFIED\`だけでなく\`REQUIRES_REVIEW\`を許容する。ただし下流Adapterは非DAGを拒否 | **安全な見直しが必要:** \`REQUIRES_REVIEW\`を**推定許可の十分条件としない**。DAGであっても承認済みIdentifiedEstimandが無ければ新Methodを実行させない |
| \`ScientificStatus\` | \`IDENTIFIED/NOT_IDENTIFIED/PARTIALLY_IDENTIFIED/REQUIRES_REVIEW/ESTIMATED/ESTIMATION_UNRELIABLE\`等は存在する | Statusを分ける（識別・推定・推論availability）。\`UNCERTAINTY_NOT_AVAILABLE\`は現行enumでは**未定義**の提案用補助code |

**補足:** ATEとATTを既存OLSの同じ加法定数係数で表す場合、母集団で異質性があると同一推定対象を意味しない。既存実装の動作を保護するが、これを新しい全Estimandの科学的同等性の根拠としない。

### 1.2. SR-02で実際に実証されたこと

- DoWhy：Backdoor／Frontdoor／IVの識別API、Backdoorの数値推定が合成データでPASS。**Frontdoor/IV数値推定は未検証**。
- EconML：LinearDML、CausalForestDML、DRLearner、ForestDRLearner、S/T/X-Learner、DRIVの**8種類でfit/effectを実行**。今回の構成で有限な区間が出たのはLinearDML、CausalForestDML、ForestDRLearner、DRIV。
- DRLearnerは今回のforest final modelで\`Only point estimates are available!\`、S/T/X-Learnerは\`inference is None\`。これを「永久にCI不可」と一般化しない。
- DRIV smokeは**連続Treatment・Instrument Z**を使用した\`fit/effect\`の実行証拠。**complier LATE/CLATEを識別・回復したという証拠ではない**。

## 2. Estimand定義と区別すべき対象

### 2.1. 基本Estimand（2値Treatmentの代表式）

| Estimand ID候補 | 科学的定義 | 対象 |
|---|---|---|
| \`ATE\` | \(E[Y(1)-Y(0)]\) | 明示したtarget populationの平均 |
| \`ATT\` | \(E[Y(1)-Y(0)\mid A=1]\) | 実際にTreatmentを受けた部分集団の平均 |
| \`CATE\` | \(\tau(x)=E[Y(1)-Y(0)\mid X=x]\) | 事前指定したeffect-modifierの値\`x\`の条件付き平均。ここで\`X\`と交絡調整\`W\`の役割を分離する |
| \`LATE\` | \(E[Y(1)-Y(0)\mid A(1)>A(0)]\) | **二値Z／二値A**の標準的monotonicity IV設定におけるcomplier集団 |
| \`IV_HETEROGENEOUS_EFFECT\`（**別ID案**） | \(\theta_{\mathrm{IV}}(x)\) を識別モーメントと処置コントラストで明記 | DRIV等。追加仮定によってconditional LATEやstructural effectに対応し得るが、無条件にCATE/LATEと改名しない |

**重要:** \`CATE\`と\`LATE\`は対象集団・conditioningが異なる。\`E[Y(1)-Y(0)|X=x]\`と\`E[Y(1)-Y(0)|X=x,\mathrm{complier}]\`は原則別物。連続Treatment／連続Instrumentの線形IV係数は、**二値IVのcomplier LATEを意味しない**。Treatment contrast（T0/T1、dose increment）、comparator、Xの定義、対象集団・観測単位・時間をすべてResultの一部とする。

### 2.2. 必須の科学的仮定

- **Backdoor（ATE/ATT/CATE）:** SUTVA/consistency、対象介入の明確化、条件付きExchangeability（測定済み共変量による無交絡）、対象でのPositivity、調整変数の時間先行と禁止経路非調整。CATEはmodifier値でのsupportと学習・評価分割を要する。
- **Frontdoor（代表的ATE）:** すべてのA→Y有向因果経路を観測Mediator Mが横切ること、A→Mの未遮断Backdoor経路なし、Aで条件付けるとM→Yの全Backdoor経路が遮断されること、適切なsupport／consistency。**Mは中間変数であり、P1-15のNegative Controlではない。** データだけで各仮定は証明できない。
- **IV→LATE（二値Z/A）:** relevance（First stage）、Zの割当が潜在Treatment/Outcomeに独立（無条件または明示した共変量に条件付けて）、exclusion、monotonicity（defierなし）、SUTVA/consistency、必要なconditional positivity。観測だけでexclusion／monotonicityを証明しない。
- **IV→その他のEstimand:** 線形constant-effect／homogeneous structural model、特殊な応答関数などの**別途明示された仮定**なしにIV係数をATEとして表示しない。
- **IV＋ML（DRIV）:** conditional moments、Instrument relevance、nuisance modelの要件、cross-fitting、識別する局所的／構造的効果の定義を別指定。**\`DRIV.fit\`が成功しただけでLATE・一般CATEは確定しない。**

## 3. IdentificationStrategy × Estimand × Estimator互換性表（案）

**凡例:** \`CANDIDATE\`＝適切な仮定・実装・科学Benchmarkの後に可能／\`ID_ONLY\`＝現時点で識別APIのみ実証／\`EST_API_PROBED\`＝数値推定APIまで実証／\`CONDITIONAL\`＝追加仮定の明示が必要／\`NOT_EQUIVALENT\`＝無断変換禁止。**これらは正式なCapability status enumではない**。

| Strategy／Graph | Target estimand | Estimator・Phase | 科学的Eligibility | SR-02実行証拠／設計判定 |
|---|---|---|---|---|
| \`RANDOMIZED\`／DAGまたは真正な割付Design | ATE | Native difference-in-means、OLS | 割付の独立・consistency、両群support | 既存機能\`R\`。新契約の導入で破壊しない |
| \`BACKDOOR\`／DAG | ATE | Native OLS、IPW、AIPW、DoWhy regression | 共変量C、無交絡、positivity。推定器固有のモデル条件 | Native \`R\`／DoWhy \`EST_API_PROBED\` |
| \`BACKDOOR\`／DAG | ATT | Native IPW/AIPWほか対応推定器 | ATT対象集団のtreatment armとoverlap、適切なATT weight／outcome model | Native \`R\`。ATE weightと取り違えない |
| \`BACKDOOR\`／DAG | CATE | LinearDML・CausalForestDML・DRLearner・ForestDRLearner・S/T/X-Learner（Phase2） | X(effect modifier)／W(confounders)、support、実効treatment type、cross-fitting／nuisance（Method別） | 8候補中上記7を\`EST_API_PROBED\`、**科学Benchmark未実施** |
| \`FRONTDOOR\`／因果DAG | ATE | DoWhy \`frontdoor.two_stage_regression\`（候補） | Frontdoor criterion、M/列、support、2段階モデル仕様による追加仮定 | **\`ID_ONLY\`**。式の識別と、2段階回帰による**モデル依存の数値推定**は別 |
| \`FRONTDOOR\` | CATE／ATT | Method別追加計画 | 条件付き効果／対象集団の識別式と推定法を**独立に導出** | **\`NOT_EQUIVALENT\`**：Frontdoor ATE識別が直ちにCATE/ATT対応とはならない |
| \`IV\`／明示したvalid Instrument | LATE（二値Z/A） | Wald ratio／2SLS（条件付きの推定契約として候補） | relevance、independence、exclusion、monotonicity、complier population | **\`ID_ONLY\`**。数値推定・first stage・weak IV診断は未実行 |
| \`IV\`／明示したvalid Instrument | ATE | 2SLS等は**追加構造仮定付き**に限る | Constant treatment effect等の識別根拠・分布条件 | **\`CONDITIONAL\`**。通常のLATEをATEとlabelしない |
| \`IV\`／IV識別仮定＋X | IV_HETEROGENEOUS_EFFECT（CLATE等は別契約） | EconML DRIV（Phase2） | Instrument／Treatment型、条件付きfirst-stage、conditional moment、crossfit | \`EST_API_PROBED\`（連続T）だが**CLATEの証拠なし** |
| \`CPDAG/PAG\`（未解決） | ATE／ATT／CATE／LATE | 数値推定へ**直結禁止** | Effectの識別が方向未確定でも成立すると別途証明する、または研究者が版付きGraphを確定する | \`REQUIRES_REVIEW\`（FCI PAGが出たから推定可能とはしない） |
| その他の準実験（RDD/DiD/SCM） | RD local effect／ATT等 | Phase3専用Design/Estimator | 局所性・cutoff・parallel trends・donor support等 | **別契約**、IV/ATE/CATEへ自動正規化しない |

**注:** 「API probe PASS」は適切なEstimandの推定精度やCI coverage、識別仮定を検証したという意味ではない。DRIVを本表の\`CATE\`行へ黙って含めず、IV異質効果として独立行にした。

## 4. Proposed Versioned Scientific Contracts（設計案）

### 4.1. \`CausalQuestion\`（研究者が固定）

最小Field案：\`question_id\`、\`estimand_kind\`、\`population/target_population\`、\`treatment/comparator\`、\`treatment_values/T0/T1\`、\`outcome\`、\`unit/time\`、\`effect_modifiers\`（CATEなど）、\`instrument\`（IV系のみ）、\`principal_stratum\`（LATEでは\`complier\`を条件付きに指定）、\`design_ref\`、\`schema_version\`。観測行ごとの予測とTarget populationの平均を混同しない。

### 4.2. \`CausalDesign\`（仮定と研究者の宣言）

\`identification_strategy\`、\`graph_id/hash/graph_type\`、\`adjustment_set\`、\`mediators\`、\`instruments\`、\`effect_modifiers\`、\`assumptions\`（code／説明／assessor／根拠／検証可能性）、\`dataset_role/hash\`、\`population/support\`、\`instrument_assignment\`、\`monotonicity_scope\`、\`method_choice_reason\`。

**必要な条件別schema:** RANDOMIZED/BACKDOORではZ/Mを強制しない。FRONTDOORはMとcriterionに対応するGraphの宣言、IV/LATEはInstrument Z、first-stage、exclusion/independence/monotonicityの根拠、CATEはX（effect modifiers）を必須条件にする。すべてのMethodへ同じ入力欄を強制しない。

### 4.3. \`IdentificationResult\`（上流Result）

\`schema_version\`、\`identification_result_id\`、\`question_hash\`、\`design_hash\`、\`graph_hash\`、\`dataset_hash\`、\`strategy\`、\`estimand_kind\`、\`estimand_expression\`、\`target_population\`、\`assumptions_declared\`／\`assumptions_checked\`、\`status\`、\`reason_codes\`、\`eligible_estimator_families\`（推奨であり最終認定ではない）、\`backend/version\`、\`lineage_hash\`。

**Status契約:** \`IDENTIFIED\`は「指定したEstimandが指定したGraph/仮定下で識別できる**と評価された**」を意味し、「仮定が現実に真」とは意味しない。\`PARTIALLY_IDENTIFIED\`は境界を出力した場合だけ。\`NOT_IDENTIFIED\`と\`REQUIRES_REVIEW\`は**下流の新Method数値推定への自動通過禁止**。既存\`allow_partial_identification\`を数値点推定へ自動変換しない。

### 4.4. \`EstimatorSpec\`（Method固有の互換性）

\`method_id\`、\`backend/version\`、\`identification_result_id\`、\`supported_estimand_kinds\`、\`supported_treatment_types\`、\`required_columns\`、\`instrument/mediator_needed\`、\`nuisance_models\`、\`crossfit/seed/splits\`、\`inference_mode\`、\`confidence_intervals_capability\`、\`model_assumptions\`、\`negative_case_rules\`、\`reference_fixture_id\`。

実行前に**実際のQuestion／識別結果／Estimator Spec**を突合せ、非互換なら実装を呼ばない。Methodの対応表は採用Backend version単位に保持する。調整用共変量WとCATEのmodifiers Xは異なる機能を持つので別に管理する。

### 4.5. \`EffectResult\`（数値推定・推論を分離）

\`schema_version\`、\`question_id/hash\`、\`identification_result_id\`、\`estimator_spec_id\`、\`estimand_kind\`、\`population/contrast\`、\`effect_point\`、\`uncertainty_status\`、\`confidence_interval\`（非対応なら\`null\`）、\`confidence_level\`、\`inference_method\`、\`support_diagnostics\`、\`first_stage_diagnostics\`（IV）、\`assumptions_and_limitations\`、\`backend/version\`、\`data/graph/config hash\`、\`result_artifact_ref\`、\`scientific_status\`。

- **3つの独立軸:** (i)識別状態、(ii)点推定状態、(iii)不確実性/区間推定可用性。既存\`ScientificStatus\`を尊重しつつ、補助\`uncertainty_status\`案\`AVAILABLE/UNAVAILABLE/FAILED/NOT_REQUESTED\`を検討する。
- \`IDENTIFIED\`≠\`ESTIMATED\`。区間が無くとも**実施済みの点推定**はその事実を記録し、区間不足を明示する。ただし**Methodの受入要件がCI必須ならScience Acceptanceは未達**。
- 個票CATEは適用したXのsupport/missingness・権限と個票Parquetの出力許可を記録し、普通の平均効果Resultと分離する。

## 5. Execution／Eligibility／Failureの状態機械（案）

### 5.1. 実行前条件の順番

1. \`CausalQuestion\`とtarget estimand／contrast／populationを固定する。
2. \`Graph/Design\`を検証し、識別根拠を評価する。GraphがCPDAG/PAGの場合、方向不確定を保持し、確定DAGとして扱わない。
3. \`IdentificationResult.status=IDENTIFIED\`か、承認済み**別の識別証明**がある場合のみ下流Estimation候補に進む（後者の運用は要Architecture Review）。\`REQUIRES_REVIEW\`は研究者への差戻し。
4. \`EstimatorSpec\`の\`estimand/strategy/treatment type/instrument or mediator/support\`を照合する。未適合なら\`NOT_APPLICABLE\`や理由付き\`REQUIRES_REVIEW\`。**未知のFieldや不正値はconfig error**として分類。
5. \`fit/effect\`と任意の\`interval\`を独立実行し、\`EffectResult\`に3軸状態を保持。弱いInstrument/overlap不足/推論モデル欠落を無理に点推定PASSしない。
6. 個票・要約ArtifactとManifestにQuestion→Identification→Estimator→Resultのimmutable hashを保存する。

### 5.2. Failure taxonomyと具体例

| 状況 | 科学的な帰結案 | 数値推定の扱い |
|---|---|---|
| DAG上、指定Backdoor setで未遮断経路あり | \`NOT_IDENTIFIED\` | 不実行。誤ったAdjustmentで効果数値を生成しない |
| PAG/CPDAGで向き不確定 | \`REQUIRES_REVIEW\` | 不実行。新規方向付けを行うには研究者の明示的Graph改訂 |
| Frontdoor criterionに違反・Mが未観測 | \`NOT_IDENTIFIED\`／\`REQUIRES_REVIEW\` | 不実行。MをNCO等で代用しない |
| IVがweak／first stage低い | \`REQUIRES_REVIEW\`／\`ESTIMATION_UNRELIABLE\` | 原則として確実な数値推定として採用しない。**単純な固定F閾値のみでvalid IVを証明しない** |
| Exclusion／monotonicityの説明・根拠欠落 | \`REQUIRES_REVIEW\` | LATEを出力しない。統計検定の非有意を仮定成立と解釈しない |
| DRIVを連続TでfitしたがLATEとlabel要求 | \`NOT_APPLICABLE\`（estimand mismatch） | LATEとして保存せずIV_HETEROGENEOUS_EFFECTとして別契約に戻す |
| CATEのXで一方のTreatment armのsupport欠落 | \`INSUFFICIENT_OVERLAP\`／\`REQUIRES_REVIEW\` | 当該X域は外挿・非適用として区別。無警告個票出力禁止 |
| Estimator点推定は出力、CI APIが不提供 | \`ESTIMATED\`＋\`uncertainty_status=UNAVAILABLE\` | CI=\`null\`、理由codeを保持。CI必須Gateなら不合格 |
| backend optional dependencyが未導入 | 技術的\`DEPENDENCY_UNAVAILABLE\`（提案code） | 科学的\`NOT_IDENTIFIED\`と混同しない |
| 上流Result hash・dataset/Graphが不一致 | 契約エラー | 実行拒否。既存manifestの流用禁止 |

**注:** 新しいreason/uncertainty codeは今回**提案**したもので、既存Domain enumに存在するとは主張しない。正式schema/exit codeと既存\`validation_override\`互換は設計04で確定する。

## 6. 科学的検証に必要なFixture（SR-04／Gate 07へ引渡し）

| Fixture ID | 入力の既知構造 | 確認すべき性質 |
|---|---|---|
| \`SR03-T01\` | Randomized Bernoulli A、定数／異質な効果、n十分 | ATE／ATTと真値・対象集団の整合。異質時にOLS定数効果をATTと同一視しない |
| \`SR03-T02\` | 既知Backdoor DAGとopen path／collider | 正しいAdjustmentのみ識別し、誤Adjustmentでfail。既存Rを回帰保護 |
| \`SR03-T03\` | Frontdoor criterionが成り立つDAG、A–Yに潜在交絡 | 識別式と推定器が別契約。2段階モデルの誤指定／M無しで失敗 |
| \`SR03-T04\` | FrontdoorのA→M交絡／M→Y背後経路／全有向経路未媒介 | 正しい\`NOT_IDENTIFIED\`。曖昧DAGを自動修復しない |
| \`SR03-T05\` | Binary Z・Binary A・monotone compliance、Y(1)-Y(0)に異質性 | Wald／推定LATEと真のcomplier LATEを比較。Population ATEとは区別 |
| \`SR03-T06\` | Invalid／weak-IV、exclusion違反、defier存在 | 弱Instrumentや単調性の不明を警告・review、LATEと断定しない |
| \`SR03-T07\` | Conditional backdoorでXによる真の異質効果 | 7種の非IV CATE推定器の点推定、support、XとWの分離を確認 |
| \`SR03-T08\` | DRIV用連続T・Zと二値Z/Aのcomplier設計を分離 | 連続TのIV heterogeneous effectをLATEと誤表記しない。各estimand別精度 |
| \`SR03-T09\` | EconML final modelの推論不可／inference None | \`effect\`はあっても\`effect_interval\`を作らず\`null\`＋理由を返す |
| \`SR03-T10\` | PAG/CPDAG、識別Result \`REQUIRES_REVIEW\` | CLIから新Methodを実行不可。確認者による新Graph固定時は版と根拠を保存 |
| \`SR03-T11\` | 別Question／dataset／Graph hashの識別Manifestを流用 | mismatchで拒否。対象の違うestimandへ数値を流用不可 |
| \`SR03-T12\` | Optional backend欠落・API version差 | 正規エラー／version記録。科学的NOT_IDENTIFIEDと区別 |

**定量合格基準は未定:** MSE/RMSE、bias tolerance、CI coverage、weak-IV検査、各seed/replicate数、既存CLI回帰許容度はReference方式と同時にGate 07で事前固定する。Fixture定義だけで科学Benchmark PASSとしない。

## 7. 技術判断・Architecture Review／オーナーに残す選択

| Decision | 推奨する設計案 | 明示的な承認が必要な点 |
|---|---|---|
| \`SR03-D01\` | Questionの\`ATE/ATT/CATE/LATE/IV_HETEROGENEOUS_EFFECT\`を区別。最後はIV用別IDとする | IV heterogeneous effectを当初から独立Estimandとして要件化するか |
| \`SR03-D02\` | DoWhy FrontdoorはATE識別とモデル依存の2段階推定を別Capabilityにする | Phase1でFrontdoor**数値推定まで必須**とするか、識別のみを第1段階とするか |
| \`SR03-D03\` | LATEは二値Z/Aのcomplier対象を基本仕様とし、連続IV/2SLSは別効果とする | Phase3で必要なIV/LATE推定器とinferential requirement |
| \`SR03-D04\` | DoWhy識別→Ariadne normalised ID result→EconML estimatorを**明示Strategy/Estimand検査**で接続 | 新Methodのschema版、旧manifestの互換・\`REQUIRES_REVIEW\`扱い |
| \`SR03-D05\` | CATEの非IV 7手法・DRIVを別経路にし、CI availabilityをMethod/構成別に保持 | 推定MethodごとにCI必須か、点推定のみのCapabilityを承認できるか |
| \`SR03-D06\` | PAG/CPDAGは保留し、別の識別証拠がない場合数値推定を禁止 | \`PARTIALLY_IDENTIFIED\`・Graph refixの将来受入範囲とowner override |

**本メモの判断の性質:** 科学的な互換性・禁止変換はレビュー上の**推奨不変条件**。個々のMethodの採否、FR/NFR/AR正本、Result schema、CLI config version、GateとWork Packageの**オーナー承認は別**。SR-03は\`DESIGN_PROPOSAL_PREPARED\`であり\`APPROVED\`でも\`SCIENCE_PASS\`でもない。

## 8. 変更先・実施順序

1. 00_04のP1-08・P2-09・P3-12／§7に「識別→対象→推定」の参照と条件を加える。68行のDispositionは維持。
2. 03（要件差分案）と04（設計差分案）に\`SR03-D01〜06\`、contract envelopeと状態機械を提案として追記。正式な正本要件と混同しない。
3. Architecture ReviewでDomain/ScientificCore/CLIのauthority、schema/Manifest version、既存Backdoor契約の後方互換を判断。
4. 未検証のFrontdoor/IV estimateとCI・CLATE等を**別のSR-02/04技術実証**として実行。Source/API存在だけで推定可とは宣言しない。
5. Approved scopeに対してMethod別科学Benchmarkとnegative fixtureを定量化してGate 06/07へ展開する。**この段階では実装しない。**
