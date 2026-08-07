# ENH-E3 Implementation Report Detail / 引継ぎ報告

- 作成日: 2026-08-07 UTC
- 対象branch: `prototype/ariadne_mvp_e3`
- ENH-E3 baseline: `3f87379bb3cbf18ba6f436877306959ddfd24163`
- 現在のimplementation commit: `f16c0a7bb25fbe3378585ba78921398638d1ecea`
- 現在の実装migration head: `20260807_product_0005`（Test Agentによるmigration検証待ち）
- 現在の実装指示正本: `00_enhance_plan_documents/06b_Ariadne_ENH-E3_実装再開指示書.md`
- 関連Gate証跡: `20_implementation_reports/ENH-E3_gate_execution_report.md`

## 1. 引継ぎ時点の結論

### 1.1. 事実

1. Gate G1はPASS済みである。
   - 実装commit: `526eec805a9299e680ecff7e8292f11a651f89ca`
   - 証跡commit: `4f597f0`
2. Gate G2はPASS済みである。
   - 実装commit: `065859d8e6ff40e7393f79928653ebefc8e139e1`
   - 証跡commit: `87099e10e84d92b466791436d6db203d8c658efe`
3. E3-3 Predictive Specification + Splitのtrial `001` implementation commitは`73a92c1b5899bc0d072df0faf8621b5171b00e5a`である。
4. Trial `001` Gate Decisionは`FAIL`であり、原因はPredictive Specification canonical/deterministic behaviorのautomated coverage欠落である。
5. Trial `002` implementation commit `fd4e332939f93cc35adbf4a03929818e47c04b7e`で、当該coverageを`tests/product/test_predictive_spec_e3.py`へ追加した。
6. Trial `002`ではproduction codeを変更していない。
7. G3 trial `002`はTest Agentにより全9報告項目PASS、full suite `157 passed, 4 skipped`、PostgreSQL contract `4 passed`と報告され、Gate Decisionは`PASS`である。
8. G4 trial `001` implementation commit `f16c0a7bb25fbe3378585ba78921398638d1ecea`でTraining + Evaluation backend vertical sliceを実装した。
9. G4は`READY_FOR_TEST`であり、Coding Agentはtestを実行していない。G5 / G6は未着手である。

### 1.2. 現在の判定

| Phase / Gate | 状態 | 根拠 |
| --- | --- | --- |
| E3-1A Generic Workflow Core | Completed | G1実装commitに収録、回帰PASS |
| E3-1B Causal Adapter / Regression | Completed | G1実装commitに収録、Causal回帰・Browser PASS |
| Gate G1 | **PASS** | `526eec8` / `4f597f0` |
| E3-2 Analysis View + Explore + Explore UI | Completed | G2実装commitに収録 |
| Gate G2 | **PASS** | `065859d` / `87099e1` |
| E3-3 Predictive Specification + Split | Completed | trial `002` implementation commit `fd4e332` |
| Gate G3 | **PASS** | trial `002` Test Agent Gate Decision |
| E3-4 / Gate G4 | **READY_FOR_TEST** | trial `001` implementation commit `f16c0a7` |
| E3-5 / Gate G5 | Not Started | G4 PASS前のため開始禁止 |
| E3-6 / Gate G6 | Not Started | 前段Gate未完了 |

## 2. Git / Working Tree状態

### 2.1. 確定commit列

```text
f16c0a7 feat: implement ENH-E3 G4 predictive training and evaluation
3c0447c test: record ENH-E3 G3 trial 002 audit evidence
908ce95 docs: hand off ENH-E3 G3 trial 002 for audit
fd4e332 test: cover ENH-E3 G3 predictive specification identity
5eb61a7 test: record ENH-E3 G3 trial 001 audit evidence
6540499 docs: hand off ENH-E3 G3 implementation for audit
73a92c1 feat: complete ENH-E3 G3 predictive specification and split
f4faffc ENH-E3 途中経過。GATE G2 Pass 済， G3 実施途中
87099e1 docs: record ENH-E3 G2 gate evidence
065859d feat: pass ENH-E3 G2 exploration gate
4f597f0 docs: record ENH-E3 G1 gate evidence
526eec8 feat: pass ENH-E3 G1 causal workflow gate
3f87379 ENH-E2
```

### 2.2. 途中経過commitに収録されたtracked変更

以下はG3作業中の差分として記録され、途中経過commit `f4faffc`へ収録された。

| File | 変更目的 |
| --- | --- |
| `src/ariadne/interfaces/web_api/app.py` | Predictive routerをProduct APIへ登録 |
| `src/ariadne/interfaces/web_api/dependencies.py` | `PredictiveSplitService` dependencyを追加 |
| `src/ariadne/interfaces/web_api/error_handlers.py` | `PredictiveValidationError`を専用code/path付き422へ変換 |
| `src/ariadne/product/application/exploratory_service.py` | Dataset / Analysis View読込を共有`AnalysisFrameProvider`へ委譲 |
| `tests/product/conftest.py` | G3テスト用の厳密なPredictive Specification factory fixtureを追加 |

当時のtracked差分の概算は5 files、52 insertions、22 deletionsであった。

### 2.3. 途中経過commitに収録されたG3新規ファイル

| File | 状態 / 責務 |
| --- | --- |
| `src/ariadne/capabilities/predictive/__init__.py` | Predictive G3 public APIをexport |
| `src/ariadne/capabilities/predictive/planner.py` | `predictive.split.v1`だけを含むG3限定一段Planを構築。Train以降は含めない |
| `src/ariadne/capabilities/predictive/validation.py` | strict schema、task/metric互換性、target/future/group/test leakageをBackend検証 |
| `src/ariadne/capabilities/predictive/splitting.py` | RANDOM / STRATIFIED / GROUP / TIME_BASEDの決定論的partition生成 |
| `src/ariadne/capabilities/predictive/split_runner.py` | Generic Executor上でpartitionを生成し、`partition-artifact/1`を作成 |
| `src/ariadne/interfaces/web_api/routers/predictive.py` | capabilities、split-validations、partition-artifact metadata API |
| `src/ariadne/product/application/analysis_frame_service.py` | Dataset Artifact hash検証、FIXED Analysis View再構築・manifest照合をFamily横断化 |
| `src/ariadne/product/application/predictive_split_service.py` | split実行、Execution/Stage/Artifact/Lineage永続化 |
| `tests/product/test_predictive_spec_e3.py` | task、availability、metric specification契約 |
| `tests/product/test_predictive_split_e3.py` | 4 split、決定性、temporal boundary、test isolation |
| `tests/product/test_predictive_leakage_e3.py` | target/future/group/overlap/population leakage |
| `tests/product/test_predictive_split_api_e3.py` | API→Artifact Store→DB→Lineageの統合契約 |

### 2.4. G3 implementation当時に完成物として扱わなかったファイル（履歴）

| File / Directory | 扱い |
| --- | --- |
| `src/ariadne/capabilities/predictive/metrics.py` | G3時点ではG4 Evaluation draft。G4 implementation commit `f16c0a7`へ収録 |
| `src/ariadne/product/domain/research_context.py` | G3時点では後段統合待ちのdraft。G4でPersistence/APIへ統合、UIは後送 |
| `src/ariadne/product/domain/lineage.py` | Domain draft。G2/G3は`LineageEdgeOrm`で必要な辺を永続化しているが、横断Lineage完成はG6 |
| 承認文書ディレクトリ、`_bkup/`、`document_inventory.json` | ユーザー入力。削除・一括stage禁止 |

trial `001` implementation commitでは対象fileだけを明示stageし、`metrics.py`、Research Context / Lineage draft、control documentを変更対象から除外した。

## 3. Work Package別の実装詳細

## 3.1. WP-0 Requirements Gate

### 状態

承認済み要件文書を正本として読み込み済み。独立したWP-0成果物commitは作成していない。

### 引継ぎ注意

- 実装順序は`06b_Ariadne_ENH-E3_実装再開指示書.md`を正本とする。
- 現在はG4 Test Agent判定前であるため、G5実装へ進んではならない。

## 3.2. WP-1 Domain / Migration

### 完了済み部分

- framework非依存Schema Registry / canonical JSON hash
- Analysis Family / versioned resource / Stage status enum
- Analysis Specification common envelope
- Analysis View domainと不変化
- Execution Plan / Stage / Attempt
- additive migration `20260807_product_0004`
- additive migration `20260807_product_0005`（G4 Test Agent検証待ち）
- generic family Execution / Stage / Result / Artifact / Lineage table
- Research Context永続化/API
- Analysis Specification共通CRUD/FIX/REVISE API

### 未完了部分

- Research Context UI
- 全Familyを統合したLineage query/export

## 3.3. WP-2 Generic Workflow Core — Completed / G1

主な確定source:

- `product/workflow/planner_registry.py`
- `product/workflow/runner_registry.py`
- `product/workflow/plan_validator.py`
- `product/workflow/bindings.py`
- `product/workflow/executor.py`
- `product/domain/execution_plan.py`
- `product/domain/stage_execution.py`

実装済み契約:

- Planner / Runner registration
- Plan schema、Stage key、DAG、Runner、input/output binding validation
- deterministic plan hash
- Stage Attempt履歴
- retry / cancel / compensation hook
- Executor内にFamily固有if/elifを置かない構成

## 3.4. WP-6 Causal Adapter / Regression — Completed / G1

`src/ariadne/capabilities/causal/workflow.py`で以下をGeneric Executorへ接続済み。

- DISCOVERY
- IDENTIFICATION
- ESTIMATION
- REFUTATION
- SENSITIVITY

既存WorkerのCausal処理は`CausalPlanner -> StageRunnerRegistry -> GenericExecutor -> CausalStageRunner`を通る。Causal固有validationと科学意味論はCapability内部に保持している。

## 3.5. WP-3 Analysis View — Completed for G2

実装済み:

- DRAFT作成・更新、validate、FIXED化
- FIXED後の上書き拒否とversion追加
- row filter / selected columns / derived columns
- missing-value policy
- temporal cutoff
- fixed-seed sampling
- arbitrary Python、network/filesystem、current time等の非決定式拒否
- empty population拒否
- source Dataset Artifact hash検証
- deterministic materialized hash / manifest
- Dataset Version -> Analysis View lineage

G3では同じ安全なDataset/View読込をPredictiveから再利用するため、`AnalysisFrameProvider`へ共通化中である。

## 3.6. WP-4 Explore — Completed for G2

実装済みOperation:

- PROFILE
- DISTRIBUTION
- ASSOCIATION
- GROUP_SUMMARY
- TIME_TREND
- CHART / Vega-Lite JSON Artifact

実装済みvertical slice:

```text
Explore UI
  -> POST exploration/executions (202 / QUEUED)
  -> Product Worker claim (QUEUED -> RUNNING)
  -> Generic Executor / Exploratory Runner
  -> saved Result / Artifact / Lineage
  -> UI再表示
  -> explicit Causal / Predictive draft handoff
```

Explore Resultは`analysis_family=EXPLORATORY`、画面にも非因果・非確認的である旨を表示する。API inline処理ではなくWorker claimへ修正済み。

### 残件

- Explore Resultへの観察メモ/限界Annotationは汎用Annotation統合側に残る。
- route-backed navigation / browser backはWP-7後段に残る。

## 3.7. WP-5 Predictive — G4 trial 001 READY_FOR_TEST

以下のG3記述はtrial `002`までに確定したSplit基盤の履歴である。G3はその後Test AgentによりPASSと判定された。

### Predictive Specification

現在のstrict schemaは以下を固定する。

- task type: `BINARY_CLASSIFICATION | REGRESSION`のみ
- prediction unit / target / prediction time / horizon
- intended use / deployment population
- feature set / excluded columns
- featureごとのavailability descriptor
- split strategy / ratiosまたはtime cutoff / seed
- evaluation primary / secondary metric
- 後続preprocessing/model/tuning/explanation spec envelope

未知field、欠落field、重複feature、不整合metricを拒否する。

### Leakage Validator

実装済み拒否（trial `001`ではCoding Agentによるテスト実行なし）:

- target列をfeatureへ含める
- prediction time後または`OUTCOME_WINDOW_END`等で利用可能になるfeature
- GROUP strategyを使わずgroup keyを指定する
- group key自体をmodel featureへ含める
- partition row overlap
- group intersection
- partition unionとsource populationの不一致
- TRAIN以外でpreprocessor fitする契約
- TESTをfeature/model/threshold selectionへ渡す契約
- time cutoff逆転およびtemporal partition境界重複

### Split Runner / Artifact

`PredictiveSplitRunner`はmodel trainingを行わず、以下だけを生成する。

- RANDOM / STRATIFIED / GROUP / TIME_BASED partition
- stable row ordinal
- partition counts
- class / group / time boundary summary
- source Dataset / Analysis View snapshot
- deterministic specification hash
- TESTの`selection_allowed=false` / `final_evaluation_only=true`
- canonical JSON `partition-artifact/1`

`PredictiveSplitService`はGeneric Executorの一段split Planを実行し、以下を既存`product_...` generic tableへ保存する。

- `FamilyExecutionOrm` (`analysis_family=PREDICTIVE`, `SUCCEEDED`)
- `FamilyStageExecutionOrm` (`predictive.split.v1`)
- `FamilyArtifactOrm` (`PARTITION_INDEX`, `partition-artifact/1`)
- Dataset Version -> Execution -> Artifact lineage
- Analysis View使用時はAnalysis View -> Execution lineage

G3では`product_0004`のgeneric tableを利用できるため、新migrationは追加していない。

### API

以下のrouterを実装済みである。

```text
GET  /api/v1/projects/{project_id}/predictive/capabilities
POST /api/v1/projects/{project_id}/predictive/split-validations
GET  /api/v1/projects/{project_id}/predictive/partition-artifacts/{artifact_id}
```

G3 trial `002`時点の`capabilities`は`gate=G3_SPLIT_ONLY`、`training_available=false`を返していた。G4 implementationでは`gate=G4_TRAINING_EVALUATION`へ更新した。

### G3 trial `002`時点で意図的に未実装だった範囲

- prepare runner
- train runner
- model registry / model fit
- hyperparameter selection
- evaluation runner / Prediction Result
- Model Artifact / preprocessor Artifact
- Model Card
- Explain runner
- Predictive UI

### G4 trial `001` implementation

- Research Context DRAFT / FIXED / immutable / relation / usage API
- Analysis Specification共通envelopeのvalidate / fix / revise lifecycle
- FIXED SpecificationからのExecution Plan API
- `SPLIT -> PREPARE -> TRAIN -> EVALUATE`のGeneric Workflow DAG
- TRAIN-only fitted preprocessor、Binary / Regression最小Model Registry
- frozen model / preprocessorによるTEST evaluation
- Training / Evaluation / Error Analysis Resultと4種Artifact
- Worker claim、202 submit、Execution lifecycle API、snapshot、lineage
- G4 capabilities。ExplanationはG5未完了として明示
- additive migration `20260807_product_0005`

## 3.8. WP-7 Frontend

### 完了済み

- Explore navigation / Analysis View / Exploration form / saved Result表示
- `EXPLORATORY`明示
- Worker terminal state polling
- Causal / Predictive draft handoffの明示

### 未完了

- Predictive workspace UI
- 6 routeのURL routing
- deep link / browser back
- Context / Dataset / Analysis View common selectorの全route統合

## 3.9. WP-8 Results / Lineage / Export

### 部分完了

- G2 ExploreとG3 splitで明示的LineageEdgeを保存
- Dataset / Analysis View / Execution / Result / Artifact間の必要辺を追加

### 未完了

- Explore / Causal / Predictive横断summary
- generic Result detail / comparison
- Project全体Lineage UI
- bundle export
- Predictive Result / Explanation lineage

## 3.10. WP-9 Verification

G1-G3のTest Agent監査は実施済み。G4 trial `001`はCoding Agent実装完了、Test Agent監査待ちである。

## 4. テスト実行履歴

## 4.1. Baseline

```text
command: UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q
result: 115 passed, 4 skipped in 28.79s
```

## 4.2. Gate G1

| Test | Result |
| --- | --- |
| 指示書6.2対象 + G1新規test | 123 passed, 4 skipped |
| full active suite | 127 passed, 4 skipped |
| Browser E2E | PASS、Chromium 151、E2E-04〜10 + E1a-additional |
| legacy import audit | 新規違反0 |

## 4.3. Gate G2

| Test | Result |
| --- | --- |
| G2 + G1 + frontend選択回帰 | 28 passed in 3.07s |
| full active suite | 139 passed, 4 skipped in 29.48s |
| PostgreSQL contract | 4 passed in 4.36s |
| migration clean upgrade | `0003 -> 0004` PASS |
| migration round trip | `0004 -> 0003 -> 0004` PASS |
| Browser E2E canonical command | PASS、E2E-02 + E2E-04〜10 + E1a-additional |
| Browser evidence | `test-results/browser_e2e/evidence.json` |

Browser中の4件の422 console errorは、既存runnerが意図的な不正入力を検証した結果であり、失敗ではない。

## 4.4. E3-3 / G3作業中

### 完走済み

```text
command:
  UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q \
    tests/product/test_predictive_spec_e3.py \
    tests/product/test_predictive_split_e3.py \
    tests/product/test_predictive_leakage_e3.py \
    tests/product/test_predictive_split_api_e3.py
result:
  11 passed in 2.41s
```

```text
command:
  UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q \
    tests/product/test_predictive_spec_e3.py \
    tests/product/test_predictive_split_e3.py \
    tests/product/test_predictive_leakage_e3.py \
    tests/product/test_predictive_split_api_e3.py \
    tests/product/test_analysis_view_e3.py \
    tests/product/test_exploratory_contract_e3.py \
    tests/product/test_exploratory_api_worker_e2e_e3.py \
    tests/product/test_exploratory_frontend_contract_e3.py \
    tests/product/test_enh_e3_workflow_core.py \
    tests/product/test_enh_e3_causal_workflow_regression.py \
    tests/product/test_architecture.py
result:
  38 passed in 5.75s
```

`python -m compileall -q src tests`および`git diff --check`もPASSしている。

### 修正済みの途中失敗

1. 最初のG3 test collection:
   - `tests`をpackageとしてimportしたため2 collection errors。
   - 製品実装の失敗ではない。
   - 共通spec builderを`tests/product/conftest.py` fixtureへ移し解消。
2. 次のG3 test run:
   - 9 passed、2 failed。
   - target leakageより先に一般的なfeature/excluded重複が発火していたため、専用`TARGET_LEAKAGE_DETECTED`を優先する順序へ修正。
   - SQLiteでExecution/Stage/ArtifactのFK insert順が未確定だったため、Execution、Stageごとに明示`flush()`を追加。
   - 修正後11 passed。

### 未完了 / 中断

```text
command: UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q
state: 46%進行後にユーザー操作で中断
observed before interruption: failure表示なし、4 skip表示あり
decision: 結果不成立。PASSとして扱わない
```

中断後に残存するpytest processは確認されていない。

## 4.5. Gate G3 trial 002 Test Agent evidence

| 項目 | 報告結果 |
| --- | --- |
| G3 reports `001`〜`008` | 全項目PASS |
| full active suite | `157 passed, 4 skipped` |
| PostgreSQL contract | `4 passed`（初回infrastructure retry後） |
| migration head | `20260807_product_0004` single head |
| Gate Decision | `PASS` |
| tested implementation | `fd4e332939f93cc35adbf4a03929818e47c04b7e` |
| handoff report commit | `908ce95` |
| audit evidence commit | `3c0447c` |

## 4.6. Gate G4 trial 001

- Coding Agentによるtest実行: NOT PERFORMED
- 対象27 Python fileのAST parse: success
- `git diff --check`: clean
- migration chain静的観察: `0001 -> 0002 -> 0003 -> 0004 -> 0005`
- Test Agentによるpytest / PostgreSQL / migration / benchmark監査: 未実施

## 5. 既知の設計判断・制約

### 5.1. 事実

- G3 split validation APIは重いtrainingではないため同期APIとして実装している。
- partition生成自体はGeneric Executorとregistered `PredictiveSplitRunner`を通る。
- split validationのExecutionは監査のためDBへ`SUCCEEDED`として保存する。
- TESTはArtifact内contractでselection input禁止としている。
- 同一spec/source/seedのsplit Artifact content hashは一致することをAPI testで確認している。
- G3は既存`product_0004` generic persistenceを利用し、新migrationを追加していない。
- G4ではheavy trainingを同期APIで実行せず、202 submit後にProduct Workerがclaimする。
- model objectはphysical Artifactへ保存し、Result JSONにはlibrary-neutral descriptorだけを保存する。
- ExplanationはG5範囲のため利用不可をcapabilitiesで明示する。

### 5.2. 検討余地

- `partition-artifacts/{id}`はmetadataを返すが、Stage間連携はHTTPではなくGeneric Workflow bindingを使用する。
- shared `AnalysisFrameProvider`はProduct applicationからExploratory compilerを再利用している。Family非依存componentへ移す余地はあるが、現在はView compilerの単一正本を優先した。
- Predictive split validationはAPI process内で実行する。将来、非常に大きいDatasetを扱う場合はasync Executionへ移す判断が必要だが、G3のsplit preview/validation契約では同期処理を採用している。
- G4のModel Registryは意図的にBinary / Regression各1 modelに限定し、candidate tuning / AutoMLは実装していない。

## 6. G3 trial handoff

### 6.1. Trial 001 decision

- implementation base commit: `f4faffc0afdec2abc6b0952bd4762952774de92a`
- implementation completed commit: `73a92c1b5899bc0d072df0faf8621b5171b00e5a`
- completion report: `G3_001_implementation_completion_report.md`
- Gate Decision: FAIL
- failure category: `REQUIRED_TEST_COVERAGE_MISSING`
- evidence commit: `5eb61a76a1c7f35407d6bc6316c633336e06b59f`

### 6.2. Trial 002 decision

- implementation base commit: `5eb61a76a1c7f35407d6bc6316c633336e06b59f`
- implementation completed commit: `fd4e332939f93cc35adbf4a03929818e47c04b7e`
- completion report: `G3_002_implementation_completion_report.md`
- changed production files: none
- changed test files: `tests/product/test_predictive_spec_e3.py`
- Coding Agent test execution: NOT PERFORMED
- Gate Decision: PASS
- Test Agent full suite: `157 passed, 4 skipped`
- Test evidence commit: `3c0447cc535b305701f3528de8f7ed89bff1add7`
- next allowed implementation action: G4 implementation

### 6.3. G4 trial 001 handoff

- implementation base commit: `3c0447cc535b305701f3528de8f7ed89bff1add7`
- implementation completed commit: `f16c0a7bb25fbe3378585ba78921398638d1ecea`
- completion report: `G4_001_implementation_completion_report.md`
- migration head: `20260807_product_0005`（検証待ち）
- Coding Agent test execution: NOT PERFORMED
- state: READY_FOR_TEST
- next allowed implementation action: G4 Test Agent監査結果を待つ

### 6.4. G4 Test Agent focus

- Research Context / Analysis Specification lifecycleとProject境界
- migration `0004 -> 0005 -> 0004 -> 0005`とsingle head
- 4-stage DAG、TRAIN-only preprocessing、TEST isolation
- Binary / Regression training/evaluation、metric、analytical status
- API 202 / Worker / cancel / retry / rerun / revise / prefill
- Snapshot / Artifact / Result / Lineage整合とfull active suite

## 7. 再開時の禁止事項

- G4 Test Agent PASS前にG5へ進まない。
- `git add .`で承認文書、backup、後続draftを混入させない。
- Coding AgentがG4のPASS / FAIL / BLOCKEDを判定しない。
- Research Context / Lineage domain draftの存在をもってWP-3 / WP-8全体completedと判定しない。
- G1/G2確定commitをrewriteしない。

## 8. 最終引継ぎ判定

```text
G1: PASS
G2: PASS
G3 Gate: PASS, trial 002 tested implementation fd4e332
G4 implementation: READY_FOR_TEST, trial 001 commit f16c0a7
G4 Gate: Test Agent decision pending
G5-G6: NOT STARTED
next allowed implementation action: wait for G4 trial 001 Gate Decision
```
