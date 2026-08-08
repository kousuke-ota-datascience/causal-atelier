# Ariadne ENH-E3 テスト指示書（07b）

- 文書名: `07b_Ariadne_ENH-E3_テスト指示書.md`
- 対象ブランチ: `prototype/ariadne_mvp_e3`
- 適用対象: **Test Agent / Audit Agentのみ**
- 目的: Gate G3〜G6の独立検証、Gate判定、テスト証跡保存
- 状態: テスト正本

---

## 1. 本書の位置づけ

本書はENH-E3後続工程における**唯一のテスト・監査指示書**である。

Test Agentはテスト設計判断のために以下を参照してはならない。

- `00_enhance_plan_documents/01_Enhance構想・要件改定計画.md`
- `00_enhance_plan_documents/06_Ariadne_ENH-E3_実装指示書.md`
- `00_enhance_plan_documents/06a_Ariadne_ENH-E3_実装順序補正・段階Gate適用指示.md`
- `00_enhance_plan_documents/06b_Ariadne_ENH-E3_実装再開指示書.md`
- `10_Revised_requirements_definition_documents/` 配下の要件定義書・設計書
- `_bkup/`

テストに必要なAcceptance Criteriaは本書へ統合済みである。

Test Agentが参照してよいもの:

1. 本書
2. 対象trialの`20_implementation_reports/[GATE]_[trial]_implementation_completion_report.md`
3. current source code / automated test code / migrations
4. 過去の`30_test_report/`（trial番号と既知履歴確認のみ）
5. Git commit / diff / status
6. テスト実行によって生成されたlog / evidence

---

## 2. Test Agentの責務

Test Agentの責務は**テスト・監査・証跡記録だけ**である。

行うこと:

- implementation completion reportが指す実装commitを確認
- GateのAcceptance Criteriaを検証
- automated testsを実行
- Browser E2Eを必要Gateで実行
- PostgreSQL / migration検証を必要Gateで実行
- scientific benchmarkを必要Gateで実行
- static architecture / dependency auditを実行
- exact command / exit code / count / duration / logsを記録
- Gateを`PASS | FAIL | BLOCKED`のいずれかで判定
- `30_test_report/`配下にreportを作成
- reportだけをevidence commitしてよい

---

## 3. Test Agentの禁止事項

Test Agentは以下を行ってはならない。

- production codeを変更する
- automated test codeを変更する
- migrationを作成・修正する
- dependencyを追加・更新する
- formatterでsource codeを書換える
- bug fixを行う
- test assertionを弱める
- skip / xfailを追加する
- failing testを削除する
- product designを再設計する
- Coding Agentのimplementation reportを書換える
- Gate FAIL/BLOCKEDなのに次Gateをテストする
- 「概ねPASS」「主要項目PASS」等の曖昧判定
- 過去trialのPASSを寄せ集めて現在trialをPASSにする

テスト実行が生成する一時ファイルは許可するが、source treeへ恒久的なtest helperを追加してはならない。

必要なread-only検査用commandや一時scriptは`/tmp`等で実行してよい。

---

## 4. Gate Status

Gateの最終statusは以下の3値だけとする。

```text
PASS
FAIL
BLOCKED
```

### PASS

対象Gateの**当該trialに必要な全必須test itemがPASS**した場合のみ。

### FAIL

product implementationまたは必要なautomated test coverageに欠陥がある場合。

例:

- contract違反
- test failure
- required test fileが存在しない
- required assertionが欠落
- regression
- scientific / analytical invariant違反
- migration defect
- architecture dependency violation

### BLOCKED

product defectか否か判定できない環境・infrastructure要因で必須testを完走できない場合。

例:

- Docker runtime不可
- PostgreSQL起動不可
- Browser runtime不可
- permission / credential不足
- user interruption
- test infrastructure自体が破損し、product implementationと独立して実行不能

BLOCKEDはPASSではない。

---

## 5. Trial規約

trial番号は3桁連番。

```text
001
002
003
...
```

Coding Agentが同Gateを修正した後は必ず次trialとする。

同一trial内で同一commandを無制限に再実行してはならない。

- deterministic product failure: 原則再実行しない
- 明確な一時的environment failure: **1回だけ**再試行可
- 再試行した場合、最初のfailureと再試行理由を同reportへ記録する

必須testの途中でユーザー操作により中断された場合、そのtrialはPASSにしない。

---

## 6. Report格納規約

Directory:

```text
20260807-01_ENH-E3_enhance_plan_approved/
└── 30_test_report/
```

File name:

```text
[GATE]_[trial連番]_[テスト項目連番]_[テスト名称].md
```

例:

```text
G3_001_001_predictive_spec_contract.md
G3_001_002_target_future_group_leakage_rejection.md
G3_001_999_gate_decision.md
```

- Gate: `G3 | G4 | G5 | G6`
- trial: 3桁
- item: 3桁
- test name: lowercase snake_case
- Gate Decisionは`999`

---

## 7. Test Report必須書式

各test item reportに最低限以下を記録する。

```markdown
# [GATE] Trial [NNN] Test [NNN] — [name]

- Gate:
- Trial:
- Test item:
- Status: PASS | FAIL | BLOCKED | NOT_RUN
- Tested implementation commit:
- Handoff report commit / path:
- Branch:
- Migration head:
- Started at:
- Finished at:

## Purpose

## Acceptance Criteria

## Preconditions / Environment

## Commands Executed

## Exact Result
- exit code
- passed
- failed
- skipped
- duration

## Log / Evidence

## Findings
- product defect:
- test infrastructure issue:
- regression:
- deviation:
- none:

## Required Correction
FAIL時のみ。観察された契約違反を記載する。
設計案・実装修正案を指示しない。

## Decision Rationale

## Source Modification by Test Agent
NONE
```

successful testではstdout全部を冗長に複製する必要はないが、command、summary、exit code、durationを必ず残す。

failureでは原因判定に必要なtraceback / assertion / response body / logを省略しない。

---

## 8. Gate Decision Report必須書式

各trialの最後に:

```text
[GATE]_[trial]_999_gate_decision.md
```

を作成する。

最低限:

```markdown
# [GATE] Trial [NNN] Gate Decision

- Status: PASS | FAIL | BLOCKED
- Tested implementation commit:
- Handoff report:
- Test report set:
- Migration head:
- Test Agent source modification: NONE

## Item Summary
| Item | Name | Status | Report |

## Gate Acceptance Summary

## Blocking Findings

## Regression Summary

## Scientific / Analytical Contract Summary

## Reason for Decision

## Next Allowed Action
- PASS: Coding Agent may implement next Gate
- FAIL: Coding Agent may fix this Gate only
- BLOCKED: Product code must not be changed solely to bypass the block
```

---

## 9. 実装commitの固定

Test Agentは、対象implementation completion reportに記載されたimplementation commitをテスト対象として固定する。

handoff report commitがその後に存在する場合:

1. implementation commitとhandoff report commitの差分を確認する
2. source / migration / automated test code差分がなく、reportだけであることを確認する
3. current HEADでtestを実行してよい
4. tested implementation commitはreportへ明記する

もしhandoff後にsource codeが変更されている場合は`BLOCKED`とし、対象commitが不明確なままテストしない。

---

# 10. G3 Test Plan — Predictive Specification + Split

G3は本書適用開始時のActive Gateである。

過去にCoding Agent側で実行された`11 passed`、`38 passed`、途中までのfull pytestは参考履歴であり、Gate証跡として再利用しない。

## G3-001 Predictive Specification Contract

Report:

```text
G3_[trial]_001_predictive_spec_contract.md
```

最低限確認:

- `BINARY_CLASSIFICATION`受付
- `REGRESSION`受付
- unsupported task reject
- required prediction question fields
- unknown field reject
- duplicate feature reject
- task / metric compatibility
- specification canonical/deterministic behavior

Canonical test:

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q tests/product/test_predictive_spec_e3.py
```

## G3-002 Leakage Rejection

Report:

```text
G3_[trial]_002_target_future_group_leakage_rejection.md
```

最低限:

- target leakage reject
- future feature reject
- availability cutoff reject
- group key misuse reject
- group leakage reject
- row overlap reject
- population mismatch reject
- time boundary overlap/reversal reject
- TEST selection input reject

Canonical test:

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q tests/product/test_predictive_leakage_e3.py
```

## G3-003 Split Determinism / Isolation

Report:

```text
G3_[trial]_003_split_determinism_and_test_isolation.md
```

最低限:

- RANDOM
- STRATIFIED
- GROUP
- TIME_BASED
- same source/spec/seed → same partition
- no row overlap
- group isolation
- temporal ordering
- TEST metadata `selection_allowed=false`
- TEST metadata `final_evaluation_only=true`

Canonical test:

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q tests/product/test_predictive_split_e3.py
```

## G3-004 API / Artifact / Lineage

Report:

```text
G3_[trial]_004_predictive_split_api_artifact_lineage.md
```

最低限:

- capabilities
- split-validations
- partition artifact metadata
- dedicated validation error code/path
- Generic Executor経由
- `predictive.split.v1`
- PREDICTIVE execution
- partition artifact persistence
- Dataset → Execution → Artifact lineage
- Analysis View利用時のlineage
- same spec/source/seed artifact content hash

Canonical test:

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q tests/product/test_predictive_split_api_e3.py
```

## G3-005 G1/G2 / Architecture Regression

Report:

```text
G3_[trial]_005_g1_g2_architecture_regression.md
```

Canonical:

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q \
  tests/product/test_analysis_view_e3.py \
  tests/product/test_exploratory_contract_e3.py \
  tests/product/test_exploratory_api_worker_e2e_e3.py \
  tests/product/test_exploratory_frontend_contract_e3.py \
  tests/product/test_enh_e3_workflow_core.py \
  tests/product/test_enh_e3_causal_workflow_regression.py \
  tests/product/test_architecture.py
```

## G3-006 PostgreSQL Contract

Report:

```text
G3_[trial]_006_postgres_predictive_split_contract.md
```

G3 split API / persistenceについてSQLite固有動作でないことを確認する。

可能ならPostgreSQL test DB上で`test_predictive_split_api_e3.py`を実行する。

環境上実行不能ならG3をPASSにせず`BLOCKED`とする。

G3で新migrationを追加していないこと、migration headが意図せず分岐していないことも確認する。

## G3-007 Full Active Pytest

Report:

```text
G3_[trial]_007_full_active_pytest.md
```

必須:

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q
```

必ず完走する。

中断結果をPASS扱いしない。

## G3-008 Static Checks

Report:

```text
G3_[trial]_008_static_dependency_and_diff_checks.md
```

最低限:

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 \
uv run python -m compileall -q src tests

git diff --check
```

加えて静的監査:

- Generic ExecutorへPredictive固有if/elifが追加されていない
- Product/new Web APIからlegacyへの新規dependencyがない
- G3 implementation commitへ`metrics.py`、Research Context/Lineage draft、backup等が混入していない
- G3でTraining/Evaluation/Explain/UI実装が混入していない

## G3 Gate PASS Criteria

以下すべてPASS:

- item 001〜008
- G1/G2 regression
- full active pytest
- PostgreSQL persistence確認
- architecture/dependency violation 0
- Training以降のscope creep 0

G3ではBrowser E2Eを必須としない。

---

# 11. G4 Test Plan — Training + Evaluation

G4はG3 PASS後のみ。

## G4-001 Research Context / Analysis Specification Contract

Report:

```text
G4_[trial]_001_research_context_and_analysis_spec_contract.md
```

確認:

- Research Context DRAFT/FIXED
- FIXED immutable
- canonical hash
- same-project relation
- Analysis Specification common envelope
- Family validation
- FIXED immutable
- revise child DRAFT
- FIXED predictive specificationからPlan生成可能

Canonical test candidate:

```bash
uv run pytest -q \
  tests/product/test_research_context_e3.py \
  tests/product/test_analysis_specification_e3.py
```

同等testへ読み替える場合はreportへ対応を記載する。

## G4-002 Predictive Plan / Runner Registration

Report:

```text
G4_[trial]_002_predictive_plan_and_runner_registration.md
```

確認:

```text
predictive.split.v1
predictive.prepare.v1
predictive.train.v1
predictive.evaluate.v1
```

- Planner deterministic
- DAG/binding valid
- registered runners
- Generic ExecutorにFamily固有分岐なし
- Stage order/bindingが`SPLIT → PREPARE → TRAIN → EVALUATE`

## G4-003 Train-only Preprocessing

Report:

```text
G4_[trial]_003_train_only_preprocessing.md
```

必須:

- fitはTRAINだけ
- validation/testはtransform only
- global data statisticsをfitへ利用しない
- fitted preprocessor Artifact
- feature schema/order固定
- TESTをPREPARE input contractからfit可能に参照できない

Canonical:

```bash
uv run pytest -q tests/product/test_predictive_training_e3.py
```

## G4-004 Model Training / Validation Selection

Report:

```text
G4_[trial]_004_model_training_and_validation_selection.md
```

確認:

- classification supported model
- regression supported model
- task compatibility
- train/validation or CV only
- TEST不使用
- deterministic seed
- model Artifact
- selected hyperparameters / validation metric
- no external model object in Result JSON

## G4-005 Untouched Test Evaluation

Report:

```text
G4_[trial]_005_untouched_test_evaluation.md
```

確認:

- frozen model
- frozen preprocessor
- only EVALUATE can consume TEST
- test evaluation後にselectionへ戻らない
- prediction Artifact
- EVALUATION_RESULT
- insufficient test sample status

Canonical:

```bash
uv run pytest -q tests/product/test_predictive_evaluation_e3.py
```

## G4-006 Metrics / Diagnostics

Report:

```text
G4_[trial]_006_metric_task_compatibility_and_diagnostics.md
```

Classification:

- ROC-AUC
- PR-AUC
- log loss
- Brier
- threshold metrics
- class balance
- calibration

Regression:

- MAE
- RMSE
- R²
- residual summary

確認:

- task/metric mismatch reject
- sample count
- evaluation population
- analytical statusとtechnical status分離

## G4-007 Artifact / Lineage Integrity

Report:

```text
G4_[trial]_007_artifact_and_lineage_integrity.md
```

追跡:

```text
Context
→ Dataset/View
→ Spec
→ Plan
→ Execution
→ Split
→ Preprocessor
→ Model
→ Prediction
→ Evaluation
```

Artifact metadata:

- family
- type
- schema version
- media type
- hash
- size

## G4-008 Predictive API / Worker E2E

Report:

```text
G4_[trial]_008_predictive_api_worker_e2e.md
```

Canonical:

```bash
uv run pytest -q tests/product/test_predictive_api_worker_e2e_e3.py
```

確認:

- execution submit 202
- worker claim
- Generic Executor
- terminal state
- saved Result/Artifact
- cancellation/retry既存契約を破壊しない

## G4-009 Predictive Scientific Benchmark

Report:

```text
G4_[trial]_009_predictive_scientific_benchmark.md
```

Canonical:

```bash
uv run pytest -q tests/scientific_benchmarks/test_predictive_e3_benchmarks.py
```

benchmarkは最低限:

- train-only fit
- test isolation
- reproducibility
- classification metric sanity
- regression metric sanity
- deliberate leakage rejection

## G4-010 PostgreSQL / Migration

Report:

```text
G4_[trial]_010_postgres_and_migration_contract.md
```

- predictive execution persistenceをPostgreSQLで検証
- new migrationがある場合:
  - clean upgrade
  - downgrade
  - re-upgrade
  - single head
- migrationがない場合:
  - head unchanged
  - schema requirementを既存headが満たす

必須環境がなく検証不能ならBLOCKED。

## G4-011 G1〜G3 Regression

Report:

```text
G4_[trial]_011_g1_g3_regression.md
```

最低限G3のtargeted testsとG1/G2重要回帰を再実行する。

## G4-012 Full Active Pytest

Report:

```text
G4_[trial]_012_full_active_pytest.md
```

```bash
uv run pytest -q
```

## G4-013 Static Architecture

Report:

```text
G4_[trial]_013_static_dependency_and_diff_checks.md
```

- no Family if/elif in Generic Executor
- no new Product/new Web API → legacy import
- no model object / dtype object in canonical JSON
- no TEST path to PREPARE/TRAIN/TUNING
- no G5/G6 scope creep
- `git diff --check`
- `compileall`

G4ではfrontend変更がない限りBrowser E2Eを必須としない。

---

# 12. G5 Test Plan — Explain + Predictive UI

G5はG4 PASS後のみ。

## G5-001 Predictive Explanation Contract

Report:

```text
G5_[trial]_001_predictive_explanation_contract.md
```

Canonical:

```bash
uv run pytest -q tests/product/test_predictive_explanation_e3.py
```

確認:

- frozen modelを参照
- explanation dataset provenance
- sampling
- method
- background/reference data metadata
- model output scale
- global explanation
- supported local explanation
- unsupported combination → NOT_APPLICABLE
- Result type / status

## G5-002 Model Card / Lineage

Report:

```text
G5_[trial]_002_model_card_lineage.md
```

確認:

- intended use
- deployment population
- training data
- features
- split
- model
- validation/test metrics
- limitations/warnings
- runtime/code
- Spec/Dataset/Split/Model/Evaluation lineage

## G5-003 Predictive Frontend Contract

Report:

```text
G5_[trial]_003_predictive_frontend_contract.md
```

Canonical:

```bash
uv run pytest -q tests/product/test_predictive_frontend_contract_e3.py
```

確認:

- `/projects/{project_id}/predictive`
- Task/Feature/Split/Train/Evaluate/Explain
- Error analysis
- Model Card
- backend operation availability
- server-authoritative state
- 6 route shell認識

## G5-004 Predictive Browser E2E

Report:

```text
G5_[trial]_004_predictive_browser_e2e.md
```

Canonical runner:

```text
tests/browser_e2e/run_enh_e3_predictive.py
```

確認:

- deep link
- reload
- browser back
- execution polling
- saved result revisit
- error rendering

Browser環境が構築不能ならBLOCKED。

## G5-005 Terminology / Causal Claim Guard

Report:

```text
G5_[trial]_005_terminology_and_causal_claim_guard.md
```

確認:

- Predictive ExplanationをCausal Explanationと表現しない
- Treatment Effectと混同しない
- predictive feature importanceをcausal effectと表示しない
- Predictive一般結果名に`effect`を用いない
- Exportも同様

## G5-006 G1〜G4 Regression

Report:

```text
G5_[trial]_006_g1_g4_regression.md
```

G4までの必須targeted suiteを再実行。

## G5-007 Full Active Pytest

Report:

```text
G5_[trial]_007_full_active_pytest.md
```

```bash
uv run pytest -q
```

## G5-008 Static Architecture

Report:

```text
G5_[trial]_008_static_dependency_and_diff_checks.md
```

- architecture dependency
- no legacy import
- no scope creep into cross-family results
- `git diff --check`
- `compileall`

---

# 13. G6 Test Plan — Final ENH-E3 Gate

G6はG5 PASS後のみ。

## G6-001 Research Context / Six Routes

Report:

```text
G6_[trial]_001_research_context_workspace_and_six_routes.md
```

確認:

- Context CRUD/FIX/history/usage
- six independent route URLs
- common header/selectors
- deep link/reload/back
- fixed resource immutability
- no global Treatment/Outcome/Target role

## G6-002 Cross-analysis Lineage

Report:

```text
G6_[trial]_002_cross_analysis_lineage.md
```

Canonical:

```bash
uv run pytest -q tests/product/test_cross_analysis_lineage_e3.py
```

最低限:

- Context → Dataset
- Dataset → View
- Explore → Causal draft
- Explore → Predictive draft
- Execution → Result → Artifact
- Result → Annotation
- RERUN/REVISED lineage
- same-project restriction

## G6-003 Results Summary / Comparison

Report:

```text
G6_[trial]_003_result_summary_and_comparison.md
```

確認:

- same/compatible Result comparison
- invariant/changed conditions
- warning difference
- cross-family summary
- AUC/RMSE/ATE等を単一rankしない
- immutable stored Resultを比較で変更しない

## G6-004 Annotation / Export

Report:

```text
G6_[trial]_004_annotation_and_export.md
```

確認:

- supported Annotation targets
- rationale/assumptions/limitations/decision/next_actions
- history
- Manifest export
- Result summary
- Specification
- Artifact references
- Lineage references
- Result payloadとArtifact download分離

## G6-005 Full API / Worker E2E

Report:

```text
G6_[trial]_005_full_api_worker_e2e.md
```

Canonical:

```bash
uv run pytest -q tests/product/test_enh_e3_api_worker_e2e.py
```

## G6-006 Browser E2E E2E-01〜08

Report:

```text
G6_[trial]_006_e2e_01_08_browser.md
```

Canonical runner:

```text
tests/browser_e2e/run_enh_e3.py
```

最低限flow:

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
→ Results / Lineage
```

加えてE2E-01〜08相当シナリオが成立すること。

## G6-007 OpenAPI / CLI / Frontend / Architecture

Report:

```text
G6_[trial]_007_openapi_cli_frontend_architecture.md
```

既存canonical contract testsを使用し:

- OpenAPI
- CLI
- Frontend contract
- architecture dependency
- operation availability

を確認する。

## G6-008 Causal Scientific Benchmark

Report:

```text
G6_[trial]_008_causal_scientific_benchmark.md
```

既存Causal benchmarkを全てPASSさせる。

特に:

- identification precedence
- eligibility
- estimator gate
- RERUN / REVISED
- post-discovery warning
- scientific status semantics

の回帰0。

## G6-009 Predictive Scientific Benchmark

Report:

```text
G6_[trial]_009_predictive_scientific_benchmark.md
```

G4 benchmarkを再実行し:

- leakage prevention
- train-only fit
- test isolation
- reproducibility
- metric sanity
- explanation labeling

を確認する。

## G6-010 Migration Round Trip

Report:

```text
G6_[trial]_010_migration_round_trip.md
```

PostgreSQL test DBで:

- clean upgrade to head
- downgrade
- re-upgrade
- single migration head
- existing Result preservation

を確認する。

## G6-011 Full Active Pytest

Report:

```text
G6_[trial]_011_full_active_pytest.md
```

```bash
uv run pytest -q
```

必ず完走する。

## G6-012 Legacy Dependency Audit

Report:

```text
G6_[trial]_012_legacy_dependency_audit.md
```

Product Domain / Product application / new Web API / new Capabilityからlegacy packageへの新規依存が0であること。

## G6-013 Authorization / Sensitive Output

Report:

```text
G6_[trial]_013_authorization_and_sensitive_output.md
```

最低限:

- cross-project access rejection
- project role enforcement
- controlled Artifact download
- no secret in logs/artifacts
- prediction/local explanation sensitive output policy
- validation error path/code

---

# 14. Fail-fast実行順序

AI credit・実行資源の浪費を防ぐため、各Gateは以下の順序で実行する。

```text
cheap static / unit / contract
  ↓
targeted integration
  ↓
PostgreSQL / migration
  ↓
scientific benchmark
  ↓
full pytest
  ↓
Browser E2E（必要Gateのみ）
  ↓
Gate decision
```

ただしBrowser E2EがGateの主要受入条件であるG5/G6では、full pytest後に実行する。

明確なblocking failureが発生した場合:

- 残りの高コストtestを無条件に続けない
- failure reportを作る
- 実行済みitemを記録する
- 未実行itemはGate Decisionで`NOT_RUN_DUE_TO_PRIOR_FAILURE`とする
- Gateは`FAIL`

PASS判定をするtrialでは全必須itemを当該trial内で完走する。

---

# 15. Regression規則

後続Gateは前段Gateを壊していないことを確認する。

ただし全Gateで毎回Browser E2Eを重複実行しない。

- G3: G1/G2 targeted + full pytest。Browser不要
- G4: G1〜G3 targeted + full pytest。Browser不要（frontend変更がある場合を除く）
- G5: G1〜G4 targeted + full pytest + Predictive Browser E2E
- G6: 全targeted + full pytest + Full Browser E2E + scientific benchmarks

これによりGate安全性を維持しつつ不要な高コスト再実行を抑える。

---

# 16. Migration規則

migrationが追加されたGateでは必須:

1. current heads確認
2. single head確認
3. clean upgrade
4. downgrade
5. re-upgrade
6. PostgreSQL contract

migrationが追加されていないGateでは、不要なround-tripを毎回実行しない。

ただしG6では最終round-tripを必ず実行する。

---

# 17. Test Coverage不足の扱い

本書が要求するcritical contractを検証するautomated testが存在しない場合、Test Agentはsource testを書かない。

そのGateを`FAIL`とし、以下を報告する。

```text
Failure category: REQUIRED_TEST_COVERAGE_MISSING
Missing contract:
Expected test scope:
Observed existing coverage:
```

Coding Agentが次trialでtest codeを実装する。

---

# 18. Test自体の疑義

既存testが明らかに壊れている、環境依存でproduct defect判定不能、または本書とtest assertionが矛盾する場合:

- testを書換えない
- product codeを変更しない
- `BLOCKED`
- test name / assertion / observed mismatchをreport
- 作業指示者の判断を待つ

---

# 19. Evidence Commit

Test Agentは、test終了後に**test reportだけ**をcommitしてよい。

例:

```bash
git add docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/30_test_report/G4_002_*.md
git commit -m "test: record ENH-E3 G4 trial 002 audit evidence"
```

`git add .`は禁止。

source / migration / automated test codeをevidence commitへ含めない。

Browser runner等が生成した一時evidenceは、既存policy上version管理対象でない限りstageしない。

---

# 20. 最終G6 PASS条件

ENH-E3をテスト上PASSとできるのは、G6 trialで最低限以下が成立した場合のみ。

1. G1〜G5の先行GateがPASS済み
2. G6 item 001〜013がPASS
3. full active pytest PASS
4. Browser E2E PASS
5. Causal scientific benchmark PASS
6. Predictive scientific benchmark PASS
7. migration round trip PASS
8. legacy dependency violation 0
9. Causal scientific semantics regression 0
10. Predictive leakage/test isolation violation 0
11. Cross-analysis Lineage成立
12. six route deep link/reload/back成立
13. authorization / sensitive output contract成立

G6 PASS後のGate Decision reportには:

```text
ENH-E3 TEST/AUDIT STATUS: PASS
```

と記載してよい。

ただしTest AgentはCoding Agentの`ENH-E3_completion_report.md`を書換えない。

最終的なプロジェクト上のCompleted宣言は作業指示者が行う。

---

# 21. Test Agent開始時の実行指示

Test Agentは以下の順序だけで動く。

```text
1. 07bを読む
2. 対象Gate/trialのimplementation completion reportを読む
3. implementation commitを固定
4. prior trial reportからtrial番号整合を確認
5. 対象Gateのtest itemだけを実行
6. 各itemのMarkdown reportを作成
7. Gate Decision reportを作成
8. reportだけをevidence commit
9. PASS / FAIL / BLOCKEDを返して停止
```

Test Agentはcodeを修正しない。
