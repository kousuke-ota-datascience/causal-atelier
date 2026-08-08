# Ariadne ENH-E3 実装再開指示書（06b）

- 文書名: `06b_Ariadne_ENH-E3_実装再開指示書.md`
- 対象ブランチ: `prototype/ariadne_mvp_e3`
- ENH-E3 baseline: `3f87379bb3cbf18ba6f436877306959ddfd24163`
- 最終確認済みG2証跡HEAD: `87099e10e84d92b466791436d6db203d8c658efe`
- 最終確認済みMigration head: `20260807_product_0004`
- 作成目的: Gate G3以降の実装作業を、上位要件定義書・設計書・旧実装指示書を再読せずに再開・完遂するための単独正本
- 適用対象: **Coding Agentのみ**
- 状態: 実装再開用正本

---

## 1. 本書の位置づけ

本書は、ENH-E3の後続実装に関する**唯一の実装指示書**である。

Coding Agentは、実装判断のために以下を参照してはならない。

- `00_enhance_plan_documents/01_Enhance構想・要件改定計画.md`
- `00_enhance_plan_documents/06_Ariadne_ENH-E3_実装指示書.md`
- `00_enhance_plan_documents/06a_Ariadne_ENH-E3_実装順序補正・段階Gate適用指示.md`
- `10_Revised_requirements_definition_documents/` 配下の全要件定義書・設計書
- `_bkup/` 配下の旧文書

これらの内容のうち後続実装に必要な事項は、本書へ統合済みである。

Coding Agentが参照してよいものは以下に限定する。

1. 本書
2. 現在のsource code / migration / automated test code / package configuration
3. `20_implementation_reports/` 配下の自身の実装報告書
4. `30_test_report/` 配下の、対象Gateに対する最新Test Agent報告書
5. Gitのcommit / diff / status情報

既存コードは「現状」を示すが、要件の正本ではない。本書と既存コードが矛盾する場合は本書を優先する。

---

## 2. Coding Agentの責務と禁止事項

### 2.1. Coding Agentが行うこと

Coding Agentの責務は**実装のみ**である。

具体的には以下を行う。

- 指定Gateのproduction codeを実装・修正する
- 指定Gateで必要なautomated test codeを作成・修正する
- 必要なadditive migrationを作成する
- 実装対象の型、Schema、API、Persistence、UIを本書どおり整合させる
- source code commitを作成する
- 実装完了報告書を作成する
- `ENH-E3_implementation_report_detail.md`を事実ベースで更新する

### 2.2. Coding Agentが行ってはならないこと

Coding Agentは以下を行ってはならない。

- `pytest`、Browser E2E、scientific benchmark等の**テスト実行**
- migration upgrade / downgrade / re-upgradeの**検証実行**
- Gate PASS / FAIL / BLOCKEDの判定
- 仕様・プロダクト設計の再設計
- 上位要件定義書・設計書の再読による要件探索
- テストをPASSさせるためのskip / xfail化、assertion緩和、テスト削除
- 対象Gate外の便乗リファクタリング
- G1/G2確定実装の再設計
- `git add .`
- 承認文書、backup、他Gate draftの一括stage
- Test Agentが報告していない不具合を推測して広範囲に改修すること
- FAIL/BLOCKED Gateを越えて次Gateへ進むこと

formatter等のコード生成・整形は、対象ファイルだけに限定され、テスト実行を伴わない場合のみ許可する。

### 2.3. 設計上の疑義

本書だけでは実装判断不能な矛盾を検出した場合、自己判断で契約を変更しない。

その場合は実装完了報告書に以下を記載して停止する。

- `Status: DESIGN_BLOCKED`
- 矛盾箇所
- 影響するGate
- 最小の選択肢
- 既存コード上の観察事実

---

## 3. Agent間の情報伝達規約

ENH-E3後続工程では、Agent同士を直接会話させず、Repository上の文書を媒介とする。

### 3.1. 情報フロー

```text
作業指示者
  │
  └─ 06b 実装再開指示書
       ↓
Coding Agent
  │
  ├─ 20_implementation_reports/
  │    ├─ [GATE]_[trial]_implementation_completion_report.md
  │    └─ ENH-E3_implementation_report_detail.md
  │
  └──────────────→ Test Agent
                    ↑
                    │ 07b テスト指示書
                    │
                    └─ 30_test_report/
                         └─ [GATE]_[trial]_[item]_[test_name].md
                              ↓
                         Coding Agent（FAIL時のみ）
```

### 3.2. Coding AgentがTest Reportを読む条件

- 同一Gateの最新Gate Decisionが`FAIL`の場合のみ、同trialのTest Reportを修正入力として読む。
- `PASS`の場合は次Gateへ進める。
- `BLOCKED`の場合はproduct codeを変更せず停止する。
- Test Reportの記載が本書と矛盾する場合は本書を優先し、`DESIGN_BLOCKED`として作業指示者へ返す。

---

## 4. Gate運用

### 4.1. 確定済みGate

| Gate | Status | 取扱い |
|---|---|---|
| G1 Generic Workflow Core + Causal Regression | PASS | 再実装禁止 |
| G2 Analysis View + Explore | PASS | 再実装禁止 |
| G3 Predictive Specification + Split | NOT PASSED | **現在の実装対象** |
| G4 Training + Evaluation | NOT STARTED | G3 PASS後のみ |
| G5 Explain + Predictive UI | NOT STARTED | G4 PASS後のみ |
| G6 Cross-analysis Lineage + Full E2E | NOT STARTED | G5 PASS後のみ |

G1/G2は既存証跡により確定済みであり、後続Gate都合だけを理由に再設計・再実装しない。

ただし後続Gateとの接続に不可避なshared interface変更が必要な場合のみ、影響を最小化して変更できる。その場合は実装完了報告書へ以下を必須記載する。

- 変更したG1/G2確定ファイル
- 変更が不可避な理由
- 既存契約を変えていない根拠
- Test Agentに再確認させる回帰範囲

### 4.2. Gateごとの停止

Coding Agentは**一回の作業で一つのGateだけ**実装する。

各Gateについて以下を行ったら必ず停止する。

1. 対象Gate実装完了
2. source code commit作成
3. implementation completion report作成
4. report commit作成
5. `READY_FOR_TEST`として作業終了

次Gateへ自動進行してはならない。

### 4.3. Trial番号

trialは3桁連番とする。

- 初回: `001`
- FAIL後の修正: `002`
- 以降同様

Coding Agentは、対象Gateの`30_test_report/`を確認し、次に必要なtrial番号を決定する。

G3は本書適用後の独立監査をtrial `001`とする。

---

## 5. 現在状態の固定

### 5.1. 最終確認済み状態

最終確認済みのENH-E3状態は以下である。

- G1: PASS
- G2: PASS
- G3 implementation: IN PROGRESS
- G3 targeted testsの過去実行: 11 passed
- G1/G2/architectureを含む過去選択回帰: 38 passed
- G3差分を含むfull pytest: 46%地点でユーザー操作により中断
- G3: **PASSとして扱わない**
- G4-G6: 未着手

上記過去テスト結果は履歴情報であり、Test AgentによるG3独立監査の代替にはならない。

### 5.2. G3着手前のGit状態

最終確認済みG2証跡HEAD:

```text
87099e10e84d92b466791436d6db203d8c658efe
```

本書・07b等のcontrol documentだけが後からcommitされ、branch HEADが上記から進んでいてもよい。

Coding Agentは、実装開始時に以下だけ確認する。

```bash
git rev-parse HEAD
git status --short
git diff --stat
```

control documentだけの差分は実装差分とみなさない。

### 5.3. G3作業中として認識済みのtracked変更

- `src/ariadne/interfaces/web_api/app.py`
- `src/ariadne/interfaces/web_api/dependencies.py`
- `src/ariadne/interfaces/web_api/error_handlers.py`
- `src/ariadne/product/application/exploratory_service.py`
- `tests/product/conftest.py`

### 5.4. G3作業中として認識済みの新規ファイル

- `src/ariadne/capabilities/predictive/__init__.py`
- `src/ariadne/capabilities/predictive/planner.py`
- `src/ariadne/capabilities/predictive/validation.py`
- `src/ariadne/capabilities/predictive/splitting.py`
- `src/ariadne/capabilities/predictive/split_runner.py`
- `src/ariadne/interfaces/web_api/routers/predictive.py`
- `src/ariadne/product/application/analysis_frame_service.py`
- `src/ariadne/product/application/predictive_split_service.py`
- `tests/product/test_predictive_spec_e3.py`
- `tests/product/test_predictive_split_e3.py`
- `tests/product/test_predictive_leakage_e3.py`
- `tests/product/test_predictive_split_api_e3.py`

### 5.5. 保存済みだがG3完成物ではないもの

以下はG3 commitへ混入させない。

- `src/ariadne/capabilities/predictive/metrics.py` — G4 draft
- `src/ariadne/product/domain/research_context.py` — 後続統合用draft
- `src/ariadne/product/domain/lineage.py` — 後続統合用draft
- 承認文書ディレクトリ
- `_bkup/`
- `document_inventory.json`

これらは削除しない。後続Gate開始後に、本書の契約と一致する部分だけを資産として利用してよい。

---

# 6. Gate G3 — Predictive Specification + Split

## 6.1. G3の目的

G3では、モデル学習に進む前にPrediction Problemとpartition契約を固定する。

G3ではTraining / Evaluation / Explain / Predictive UIを実装してはならない。

## 6.2. Predictive Specification

Schema version:

```text
predictive-analysis-spec/1
```

対応task:

```text
BINARY_CLASSIFICATION
REGRESSION
```

それ以外は明示的にrejectする。

Specificationは最低限以下を保持する。

```text
task_type
prediction_question
  prediction_unit
  target
  prediction_time
  horizon
  intended_use
  deployment_population
feature_spec
  feature_columns
  availability descriptors / cutoff
  excluded_columns
split_spec
  strategy
  train / validation / test ratio または time cutoff
  group_column
  stratify
  seed
evaluation_spec
  primary metric
  secondary metrics
preprocessing_spec
model_spec
tuning_spec
explanation_spec
```

後段spec envelopeは保持してよいが、G3では実行しない。

未知field、必須field欠落、重複feature、task/metric不整合をrejectする。

## 6.3. Leakage / isolation契約

Backendで最低限以下をrejectする。

- target列をfeatureに含める
- target derivative
- prediction time後に利用可能となるfeature
- `OUTCOME_WINDOW_END`等、予測時点で利用できないfeature
- GROUP strategyなしでgroup keyを指定する
- group key自体をmodel featureに含める
- partition row overlap
- group intersection
- partition unionとsource populationの不一致
- temporal boundary逆転・重複
- TRAIN以外でpreprocessorをfitする契約
- TESTをfeature selection / model selection / threshold selectionへ渡す契約

専用validation errorはfield pathとmachine-readable codeを返す。

## 6.4. Split

対応strategy:

```text
RANDOM
STRATIFIED
GROUP
TIME_BASED
```

splitは同一source / spec / seedで決定論的であること。

partition Artifactは以下を保持する。

- stable row ordinalまたはstable row identifier
- train / validation / test partition
- partition counts
- class / group / temporal boundary summary
- source Dataset Version
- optional Analysis View
- source snapshot / hash
- specification hash
- `selection_allowed=false` for TEST
- `final_evaluation_only=true` for TEST

Artifact schema:

```text
partition-artifact/1
```

## 6.5. G3 Workflow / Persistence

G3 split preview/validationは重いTrainingではないため同期APIでよい。

ただしpartition生成は必ず、

```text
Predictive Planner
  → Generic Executor
  → registered predictive.split.v1 runner
```

を通す。

Generic ExecutorへPredictive固有if/elifを追加してはならない。

split executionは既存generic persistenceへ保存する。

最低限:

- Family Execution: `analysis_family=PREDICTIVE`
- Stage Execution: `predictive.split.v1`
- Artifact: `PARTITION_INDEX`, `partition-artifact/1`
- Dataset Version → Execution → Artifact lineage
- Analysis View利用時: Analysis View → Execution lineage

G3のためだけの新migrationは追加しない。

## 6.6. G3 API

最低限以下を維持する。

```text
GET  /api/v1/projects/{project_id}/predictive/capabilities
POST /api/v1/projects/{project_id}/predictive/split-validations
GET  /api/v1/projects/{project_id}/predictive/partition-artifacts/{artifact_id}
```

G3時点のcapabilitiesはTraining未提供を誤表示しない。

## 6.7. G3で禁止

以下をG3実装commitへ含めない。

- `predictive.prepare.v1`
- `predictive.train.v1`
- model fitting
- hyperparameter selection
- `predictive.evaluate.v1`
- prediction artifact
- Model Card
- `predictive.explain.v1`
- Predictive UI

## 6.8. G3完了時

G3 code/test filesだけを明示stageする。

`git add .`は禁止。

Coding Agentはテストを実行せず、実装完了報告書を作成し`READY_FOR_TEST`で停止する。

---

# 7. Gate G4 — Training + Evaluation

G4は、Test AgentがG3を`PASS`とした後だけ開始する。

## 7.1. G4の目的

G4ではPredictive backend vertical sliceを完成させる。

最終workflowは以下とする。

```text
SPLIT
  ↓
PREPARE
  ↓
TRAIN
  ↓
EVALUATE
```

**PREPAREをSPLITより前に置かない。**

G3で確立したpartition Artifactを、Generic Workflowのoutput/input bindingまたはArtifact Store Port経由で下流へ渡す。

HTTP download APIをStage間データ連携に使用しない。

## 7.2. G4前提Platform closure

G4のfull predictive executionをplaceholderなしで成立させるため、以下の未完了基盤をG4内で閉じる。

### 7.2.1. Research Context backend

最低限:

- `ResearchContextVersion`
- DRAFT / FIXED
- FIXED後immutable
- context key / version number
- problem statement
- one or more research questions
- significance
- hypotheses
- decision context
- relation
- canonical hash
- 同一Project境界

API:

```text
POST  /api/v1/projects/{project_id}/research-contexts
GET   /api/v1/projects/{project_id}/research-contexts
GET   /api/v1/projects/{project_id}/research-contexts/{context_id}
PATCH /api/v1/projects/{project_id}/research-contexts/{context_id}
POST  /api/v1/projects/{project_id}/research-contexts/{context_id}/fix
GET   /api/v1/projects/{project_id}/research-contexts/{context_id}/usage
```

Research Context UIはG6まで後送してよい。

### 7.2.2. Analysis Specification common lifecycle

共通Envelope:

```text
schema_version = analysis-specification/1
analysis_family
research_context_version_id
dataset_version_id
analysis_view_id
analysis_mode
family_spec_schema_version
family_spec
revision_context
warnings
```

API:

```text
POST  /api/v1/projects/{project_id}/analysis-specifications
GET   /api/v1/projects/{project_id}/analysis-specifications
GET   /api/v1/projects/{project_id}/analysis-specifications/{spec_id}
PATCH /api/v1/projects/{project_id}/analysis-specifications/{spec_id}
POST  /api/v1/projects/{project_id}/analysis-specifications/{spec_id}/validate
POST  /api/v1/projects/{project_id}/analysis-specifications/{spec_id}/fix
POST  /api/v1/projects/{project_id}/analysis-specifications/{spec_id}/revise
```

FIXED Specificationを上書きしてはならない。

Predictive full executionはFIXED Specificationを入力とする。

### 7.2.3. Execution Plan / Execution API

既存Generic Workflow Coreを利用し、必要なAPIが未実装なら以下を実装する。

```text
POST /api/v1/projects/{project_id}/execution-plans
GET  /api/v1/projects/{project_id}/execution-plans/{plan_id}
POST /api/v1/projects/{project_id}/execution-plans/{plan_id}/validate

POST /api/v1/projects/{project_id}/executions
GET  /api/v1/projects/{project_id}/executions
GET  /api/v1/projects/{project_id}/executions/{execution_id}
GET  /api/v1/projects/{project_id}/executions/{execution_id}/stages
POST /api/v1/projects/{project_id}/executions/{execution_id}/cancel
POST /api/v1/projects/{project_id}/executions/{execution_id}/retry
POST /api/v1/projects/{project_id}/executions/{execution_id}/rerun
POST /api/v1/projects/{project_id}/executions/{execution_id}/revise
GET  /api/v1/projects/{project_id}/executions/{execution_id}/prefill
```

重いTrainingは同期APIで実行しない。

Execution submitは`202 Accepted` + Execution参照を返し、Workerがclaimする。

Execution snapshotには最低限以下を固定する。

- Research Context ID / hash
- Dataset Version ID / hash
- optional Analysis View ID / hash
- Specification ID / hash
- Plan ID / hash
- code / runtime / library / schema versions
- seed

## 7.3. Predictive Planner

G4以降のPredictive Plannerは、少なくとも以下のregistered stageを解決する。

```text
predictive.split.v1
predictive.prepare.v1
predictive.train.v1
predictive.evaluate.v1
```

PlanはDAGとしてinput/output contractを持つ。

Generic ExecutorへFamily固有分岐を追加しない。

## 7.4. PREPARE

PREPAREの責務:

- feature frameを構築する
- preprocessing definitionを解決する
- **fit対象はTRAIN rowsのみ**
- validation / testにはtransformのみ
- fitted preprocessorをArtifact化
- output feature schemaとfeature orderを固定
- 外部dtype objectを正本JSONへ保存しない

重要な構造的制約:

> `predictive.prepare.v1`のinput contractにTESTをfit可能な形で渡してはならない。

## 7.5. TRAIN

Input:

- TRAIN partition
- VALIDATION partitionまたはCV folds
- fitted preprocessor / preprocessing contract
- model spec
- tuning spec
- seed

TEST partitionはTRAINへ渡してはならない。

Model Registryはtask compatibilityを宣言する。

ENH-E3ではmodel zooを作らない。

最低限:

- Binary Classificationに使用可能な登録model
- Regressionに使用可能な登録model
- library-neutral model identifier
- supported task
- parameter schema
- deterministic seed handling

既存dependencyで実装可能な最小構成を優先する。

Tuningを実装する場合:

- TRAIN / VALIDATIONまたはCVのみ
- finite deterministic candidate set
- objective metricを明示
- TEST metricをobjectiveへ渡さない
- AutoML探索基盤を新設しない

Output:

- fitted model Artifact
- fitted preprocessor Artifact
- training history
- selected hyperparameters
- validation metric
- reproducibility metadata

model objectは物理Artifactとし、Result JSONにはlibrary-neutral descriptorのみ保存する。

## 7.6. EVALUATE

EVALUATEは**frozen model**と**frozen preprocessor**だけを使用する。

EVALUATEだけがuntouched TEST partitionへアクセスできる。

TESTを評価後にmodel selectionへ戻してはならない。

生成:

- prediction Artifact
- `EVALUATION_RESULT`
- 必要な`ERROR_ANALYSIS_RESULT`
- metrics
- diagnostics
- evaluation population
- sample count

Classification最低限:

- ROC-AUC
- PR-AUC
- log loss
- Brier score
- threshold metrics
- class balance
- calibration情報

Regression最低限:

- MAE
- RMSE
- R²
- residual summary

task typeとmetricの不整合をrejectする。

## 7.7. Predictive Result status

許可status:

```text
SPLIT_RESULT:
  PASS | WARN | FAIL

TRAINING_RESULT:
  TRAINED | TRAINED_WITH_WARNINGS | FAILED_VALIDATION

EVALUATION_RESULT:
  EVALUATED | EVALUATED_WITH_WARNINGS | INSUFFICIENT_TEST_SAMPLE

ERROR_ANALYSIS_RESULT:
  GENERATED | GENERATED_WITH_WARNINGS
```

Execution technical statusとanalytical statusを混同しない。

## 7.8. Artifact / Lineage

最低限以下を追跡可能にする。

```text
Research Context
  ↓
Dataset Version / Analysis View
  ↓
Predictive Specification
  ↓
Execution Plan
  ↓
Execution
  ↓
SPLIT Artifact
  ↓
PREPROCESSOR Artifact
  ↓
MODEL Artifact
  ↓
PREDICTION Artifact
  ↓
EVALUATION Result
```

Artifact metadataにはfamily / type / schema version / media type / hash / sizeを保持する。

Stage間artifactはArtifact Store PortまたはGeneric Workflow bindingで解決する。

## 7.9. G4 API capability表示

`predictive/capabilities`は少なくとも以下を返せるようにする。

- supported task types
- split strategies
- preprocessing steps
- model registry entries
- metrics
- compatibility information

ExplanationはG5未完了であることを明示する。

## 7.10. G4 migration

既存`20260807_product_0004`を再利用できる場合は再利用する。

Research Context / Analysis Specification等の永続化に不足Table/Columnがある場合だけ、**単一headを維持するadditive migration**を追加する。

既存Resultを破壊・削除しない。

## 7.11. G4で禁止

- Predictive UIの完成
- Explain Runner
- Model Card完成
- Cross-family Result summary
- Project Lineage UI
- 便乗したCausal再設計
- model zoo / AutoML framework
- TESTをTRAIN/PREPARE/TUNINGへ渡すshortcut

---

# 8. Gate G5 — Explain + Predictive UI

G5はTest AgentがG4を`PASS`とした後だけ開始する。

## 8.1. Explain Runner

registered stage:

```text
predictive.explain.v1
```

Input:

- frozen model
- frozen preprocessor
- explicit explanation dataset
- explanation specification
- sampling definition

保存:

- explanation method
- explanation dataset provenance
- sampling
- background/reference data metadata
- model output scale
- global explanation
- local explanation（対応model / methodで生成可能な場合）
- warnings / limitations

Result:

```text
PREDICTIVE_EXPLANATION_RESULT
```

許可status:

```text
GENERATED
GENERATED_WITH_WARNINGS
NOT_APPLICABLE
```

重い説明libraryを追加すること自体を目的化しない。

既存dependencyで安定して説明できるmodel/methodを優先し、未対応組合せは曖昧な近似値を返さず`NOT_APPLICABLE`とする。

## 8.2. 科学的Terminology Guard

以下をUI、Result、Exportの全てで強制する。

```text
Predictive Explanation
≠ Causal Explanation
≠ Treatment Effect
```

Predictive feature importanceやlocal explanationをcausal effectとして表示・命名・説明してはならない。

Predictive画面の一般結果名として`effect`を使用しない。

## 8.3. Model Card

`MODEL_CARD_RESULT`を生成する。

最低限:

- intended use
- deployment population
- training data / Dataset / Analysis View
- feature set
- split strategy
- model descriptor
- selected hyperparameters
- validation / test metrics
- limitations
- warnings
- code/runtime metadata

Lineage:

```text
Model Card
  → Specification
  → Dataset / Analysis View
  → Split
  → Preprocessor
  → Model
  → Evaluation
```

## 8.4. Predictive Workspace UI

route:

```text
/projects/{project_id}/predictive
```

最低限表示・操作:

- active Research Context
- selected Dataset Version / Analysis View
- Prediction Task
- Feature specification
- Split specification / validation result
- Training execution
- Evaluation
- Error analysis
- Explanation
- Model Card
- Execution status
- Result / Artifact references

Backend operation availabilityをbutton enablementの正本とする。

client local stateだけで実行可否を判断しない。

## 8.5. Routing

G5でroute-backed ProjectShell基盤を完成させる。

以下の6 routeを独立URLとして認識できる状態にする。

```text
/projects/{project_id}/context
/projects/{project_id}/data
/projects/{project_id}/explore
/projects/{project_id}/causal
/projects/{project_id}/predictive
/projects/{project_id}/results
```

G5の必須受入対象はPredictive routeのdeep link / reload / browser backである。

Context / Results routeの最終機能実装はG6で完了してよい。

## 8.6. G5で禁止

- Cross-family metricを単一scoreへ正規化する
- AUC/RMSEとATE等を同じ尺度でrankする
- Predictive explanationを因果説明として表現する
- G6のLineage/Exportを便乗して全面実装する

---

# 9. Gate G6 — Cross-analysis Lineage + Full Product Closure

G6はTest AgentがG5を`PASS`とした後だけ開始する。

G6はENH-E3の未完了MUST範囲を閉じる最終統合Gateである。

## 9.1. Research Context UI / Workspace

`/projects/{project_id}/context`で最低限以下を扱う。

- Project topic / objective / decision context / memo
- Research Context DRAFT作成
- Context編集
- FIXED化
- version履歴
- Research Question
- Hypothesis
- relation
- Context usage / related Analysis / Result

FIXED Contextを上書きしない。

## 9.2. Common Header / Selectors

全6 routeで共通して表示する。

- Project name / status
- active Research Context Version
- selected Dataset Version
- selected Analysis View
- current role
- unsaved draft indicator

Data layerにTreatment / Outcome / Target等のFamily固有roleをglobal固定しない。

## 9.3. Results / Comparison

API最低限:

```text
GET  /api/v1/projects/{project_id}/results
GET  /api/v1/projects/{project_id}/results/{result_id}
POST /api/v1/projects/{project_id}/comparisons
GET  /api/v1/projects/{project_id}/results/summary
```

定量比較は同一または明示的compatible Result Typeに限定する。

Cross-family summaryは関係を示すが、異種metricをrankしない。

表示可能な関係例:

- shared Context
- shared Dataset / Analysis View
- Exploratory Result motivated Causal/Predictive Analysis
- Predictive Result generated a causal hypothesis
- selected / rejected Result and rationale

## 9.4. Lineage

API最低限:

```text
GET  /api/v1/projects/{project_id}/results/{result_id}/lineage
GET  /api/v1/projects/{project_id}/lineage
POST /api/v1/projects/{project_id}/lineage-links
```

最低限追跡可能にする。

```text
Research Context
  ↓
Dataset Version
  ├─ Analysis View
  ├─ Exploratory Analysis
  ├─ Causal Analysis
  └─ Predictive Analysis
```

さらに:

```text
Exploratory Result → Causal Analysis
Exploratory Result → Predictive Analysis
Dataset Version → Analysis View
Execution → Result → Artifact
Result → Annotation
Result → Research Context
base Execution → RERUN / REVISED Execution
```

LineageEdgeは同一Project内だけ許可する。

relation typeは少なくとも既存modelに整合する形で以下を扱う。

```text
USED_INPUT
GENERATED
DERIVED_FROM
REVISED_FROM
SUPPORTED_BY
MOTIVATED
SELECTED
REJECTED
```

foreign keyで表現できる所有関係をLineageEdgeへ二重正本化しない。

## 9.5. Annotation

最低限target:

- Project
- ResearchContextVersion
- AnalysisView
- AnalysisSpecification
- Execution
- Result
- GraphVersion

内容:

- statement
- rationale
- assumptions
- limitations
- decision
- next_actions
- update history

## 9.6. Artifact / Export

API最低限:

```text
GET  /api/v1/projects/{project_id}/artifacts/{artifact_id}
GET  /api/v1/projects/{project_id}/artifacts/{artifact_id}/download
POST /api/v1/projects/{project_id}/exports
```

Exportは最低限:

- Manifest
- Result summary
- Specification
- Artifact references
- Lineage references

Result payloadと物理Artifact downloadを分離する。

## 9.7. Security / privacy closure

最低限:

- Project ownership / role validation
- cross-project Resource / Lineage rejection
- controlled Artifact download
- secretをArtifact / logへ露出しない
- prediction row / local explanationを機微出力として扱える
- validation errorにfield pathとcodeを保持

## 9.8. Frontend closure

6 routeすべてについて:

- independent URL
- deep link
- reload
- browser back
- common selector整合
- backend authoritative state
- stateを色だけで伝えない

Results routeでは:

- Family明示
- analytical status
- warnings / limitations
- Result比較
- Lineage
- Annotation
- Artifact
- Export

を扱う。

## 9.9. ENH-E3 final E2E

少なくとも以下の流れをProductとして成立させる。

```text
Research Context
→ Dataset Version
→ Analysis View
→ Explore
→ Saved Exploration
→ Predictive Specification
→ Split
→ Prepare
→ Train
→ Evaluate
→ Explain
→ Causal Analysis
→ Results / Comparison / Lineage / Annotation / Export
```

既存Causal scientific semanticsを変更してはならない。

---

# 10. Architecture Guard

全Gateで以下を守る。

## 10.1. Dependency

- Product DomainはWeb Framework、ORM、ML library、legacy packageへ依存しない
- Product / new Web APIから`ariadne.legacy`への新規依存を追加しない
- Family-specific validationはCapability側に置く
- Generic ExecutorへFamily固有if/elifを追加しない

## 10.2. Schema / JSON

- Schema versionを持つ
- unknown fieldをrejectする
- canonical JSON / hashは決定的
- NaN / Infinity / external objectを正本JSONへ保存しない
- model object / dtype objectをResult JSONへ保存しない

## 10.3. Workflow

- Plannerは実行しない
- Execution Planはimmutable
- Stage Typeはnamespace / name / version
- missing runner / cycle / missing binding / schema mismatchをPlan validationでreject
- technical retryと条件変更を分離する
- successしたExecutionとanalytical positive resultを同義にしない

## 10.4. Artifact

- temporary objectを成功前にfinal URIとして公開しない
- metadata / Artifact / Lineage / Stage successの整合をUnit of Workで扱う
- promotion失敗にはcompensation可能な構造を維持する

## 10.5. Scientific / analytical

- Exploratory Resultをcausal conclusionへ自動昇格しない
- Predictive performanceはcausal effectを意味しない
- Predictive Explanationはcausal explanationではない
- test partitionをselectionへ使わない
- preprocessing fitはtrain限定
- time/group leakageをBackendでreject
- AUC / RMSE / ATE等を単一scoreへ正規化しない

---

# 11. Automated Test Codeの作成責務

Coding Agentは、各Gateで要求されるtest codeが存在しない場合に**test codeを実装する**。

ただし**実行はしない**。

最低限のcanonical file名:

## G3

```text
tests/product/test_predictive_spec_e3.py
tests/product/test_predictive_split_e3.py
tests/product/test_predictive_leakage_e3.py
tests/product/test_predictive_split_api_e3.py
```

## G4

```text
tests/product/test_research_context_e3.py
tests/product/test_analysis_specification_e3.py
tests/product/test_predictive_training_e3.py
tests/product/test_predictive_evaluation_e3.py
tests/product/test_predictive_api_worker_e2e_e3.py
tests/scientific_benchmarks/test_predictive_e3_benchmarks.py
```

## G5

```text
tests/product/test_predictive_explanation_e3.py
tests/product/test_predictive_frontend_contract_e3.py
tests/browser_e2e/run_enh_e3_predictive.py
```

## G6

```text
tests/product/test_cross_analysis_lineage_e3.py
tests/product/test_results_lineage_export_e3.py
tests/product/test_enh_e3_api_worker_e2e.py
tests/browser_e2e/run_enh_e3.py
```

既に同等testが存在する場合、重複test suiteを新設せず既存testを拡張してよい。

Test Agentが独立して判定できるよう、assertionは具体的な契約を検証する。

---

# 12. FAIL後の修正規則

Test Agentから`FAIL`が返った場合:

1. 同Gateから出ない
2. failing reportだけでなく同trialのGate Decisionを読む
3. failureを再現するためのテスト実行はCoding Agentでは行わない
4. Reportに記載された観察事実とsourceを静的に分析する
5. 原因に必要な最小変更だけ行う
6. PASS済み項目の便乗改修をしない
7. 新しいsource code commitを作る
8. 次trialのimplementation completion reportを作る
9. `READY_FOR_TEST`で停止する

Test Agentが解決方法を提案していても、それは要件変更権限を持たない。

本書のarchitecture guardに反する修正は行わない。

---

# 13. BLOCKED後の規則

Test Agentから`BLOCKED`が返った場合、Coding Agentはproduct codeを変更しない。

例:

- Docker / DB / Browser runtimeが起動不能
- credential / permission不足
- external service unavailable
- test infrastructure破損

Coding Agentは`WAITING_FOR_INSTRUCTION`として停止する。

---

# 14. Commit規約

## 14.1. Implementation commit

対象Gateのsource / migration / automated test codeだけを明示stageする。

例:

```bash
git add <explicit-file-1> <explicit-file-2> ...
git commit -m "feat: implement ENH-E3 G4 predictive training and evaluation"
```

`git add .`は禁止。

## 14.2. Handoff report commit

Implementation commit後、そのhashを取得してimplementation completion reportへ記載する。

その後、reportだけをcommitする。

```bash
git add docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/...
git commit -m "docs: hand off ENH-E3 G4 implementation for audit"
```

Test Agentはimplementation commit hashとhandoff report commit hashの双方を記録する。

---

# 15. Implementation Completion Report

各trialで以下を作成する。

```text
20_implementation_reports/[GATE]_[trial]_implementation_completion_report.md
```

例:

```text
20_implementation_reports/G3_001_implementation_completion_report.md
```

最低限以下を記載する。

```text
Gate:
Trial:
Status: READY_FOR_TEST | DESIGN_BLOCKED
Implementation base commit:
Implementation completed commit:
Handoff report commit: （commit後に自己参照できないため省略可）
Migration head:
Working tree summary:
Implemented scope:
Changed production files:
Changed test files:
Added migration:
Architecture guard check:
Known deviations:
Known limitations:
Files intentionally excluded:
Required Test Agent focus:
Test execution by Coding Agent: NOT PERFORMED
```

Coding Agentは「PASS」「Gate Completed」と記載してはならない。

---

# 16. Cumulative Implementation Report

各trial終了時に以下も更新する。

```text
20_implementation_reports/ENH-E3_implementation_report_detail.md
```

更新内容は事実だけとする。

- current implementation commit
- Gate implementation state
- changed files
- unresolved items
- Test Agentの最新Gate decision
- next allowed implementation action

過去のPASS証跡を削除・書換えない。

---

# 17. G6実装完了時のCompletion Report

G6 implementation終了時は以下も作成する。

```text
20_implementation_reports/ENH-E3_completion_report.md
```

ただしCoding Agentが記載できる最終状態は:

```text
IMPLEMENTATION_COMPLETE_AWAITING_G6_AUDIT
```

までとする。

最低限:

1. baseline
2. final implementation commit
3. migration head
4. implemented scope
5. changed files
6. architecture compliance
7. predictive leakage controls
8. causal regression protection
9. deviations
10. unresolved issues
11. test execution was delegated to Test Agent
12. final product completion decision is pending G6 audit

ENH-E3の最終`Completed`判定はCoding Agentが行わない。

---

# 18. Coding Agent開始時の実行指示

本書を受け取ったCoding Agentは、以下の順序だけで動く。

```text
1. 現在のGit stateを確認
2. 30_test_reportの最新Gate Decisionを確認
3. Active Gateを一つだけ決定
4. Active Gate以外を実装対象から除外
5. source / existing testsを読む
6. 本書との差分だけ実装
7. automated test codeを必要に応じて作成
8. implementation commit
9. implementation completion report
10. cumulative implementation report更新
11. handoff report commit
12. READY_FOR_TESTで停止
```

本書作成時点のActive Gateは**G3**である。

G3のTest Agent PASSがない限りG4へ進んではならない。
