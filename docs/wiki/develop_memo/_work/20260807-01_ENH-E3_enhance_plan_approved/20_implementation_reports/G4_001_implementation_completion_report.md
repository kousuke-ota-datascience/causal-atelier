# ENH-E3 G4 Trial 001 Implementation Completion Report

Gate: G4 Training + Evaluation

Trial: 001

Status: READY_FOR_TEST

Implementation base commit: `3c0447cc535b305701f3528de8f7ed89bff1add7`

Implementation completed commit: `f16c0a7bb25fbe3378585ba78921398638d1ecea`

Handoff report commit: omitted because this report is contained by that commit

Migration head: `20260807_product_0005` (statically inspected; migration execution not performed)

Working tree summary: implementation commit後は、ユーザー管理のuntracked control document `06b` / `07b`だけが残存

## Implemented scope

- `ResearchContextVersion`のDRAFT / FIXED、FIXED後immutable、version、relation、canonical hash、Project境界、usage API
- 共通`AnalysisSpecification` envelopeのDRAFT / FIXED、validate、immutable、revise lifecycle
- FIXED Predictive SpecificationからのExecution Plan作成・取得・validate
- `SPLIT -> PREPARE -> TRAIN -> EVALUATE`の4-stage DAGとregistered runner
- TRAIN rowsだけでfitするnumeric/categorical preprocessorとfitted preprocessor Artifact
- Binary Classification用`logistic_regression.v1`、Regression用`linear_regression.v1`の最小決定論的Model Registry
- TESTをTRAIN / tuningから構造的に分離し、frozen model/preprocessorだけで行うEVALUATE
- Classification / Regression metrics、Prediction Artifact、Training / Evaluation / Error Analysis Result
- Execution submit `202 Accepted`、Worker claim、list/get/stages/cancel/retry/rerun/revise/prefill
- Execution snapshot、Result / Artifact / Stage state、Artifact chainとLineage
- G4 capability表示。training/evaluation available、explanation unavailableを明示
- Research Context / Analysis Specification persistence不足を閉じる単一additive migration

## Changed production files

- `product_migrations/versions/20260807_product_0005_enh_e3_g4_predictive.py`
- `src/ariadne/capabilities/predictive/__init__.py`
- `src/ariadne/capabilities/predictive/metrics.py`
- `src/ariadne/capabilities/predictive/modeling.py`
- `src/ariadne/capabilities/predictive/planner.py`
- `src/ariadne/capabilities/predictive/preprocessing.py`
- `src/ariadne/capabilities/predictive/split_runner.py`
- `src/ariadne/capabilities/predictive/training_runners.py`
- `src/ariadne/capabilities/predictive/validation.py`
- `src/ariadne/interfaces/web_api/app.py`
- `src/ariadne/interfaces/web_api/dependencies.py`
- `src/ariadne/interfaces/web_api/error_handlers.py`
- `src/ariadne/interfaces/web_api/routers/executions.py`
- `src/ariadne/interfaces/web_api/routers/predictive.py`
- `src/ariadne/interfaces/web_api/routers/predictive_workflow.py`
- `src/ariadne/interfaces/web_api/routers/workspace_lifecycle.py`
- `src/ariadne/interfaces/worker/runner.py`
- `src/ariadne/product/application/predictive_workflow_service.py`
- `src/ariadne/product/application/workspace_lifecycle_service.py`
- `src/ariadne/product/persistence/orm_models.py`

## Changed test files

- `tests/product/test_research_context_e3.py`
- `tests/product/test_analysis_specification_e3.py`
- `tests/product/test_predictive_training_e3.py`
- `tests/product/test_predictive_evaluation_e3.py`
- `tests/product/test_predictive_api_worker_e2e_e3.py`
- `tests/scientific_benchmarks/test_predictive_e3_benchmarks.py`
- `tests/product/test_predictive_split_api_e3.py` — G4 capability契約へ更新

## Added migration

- revision: `20260807_product_0005`
- down revision: `20260807_product_0004`
- additive objects:
  - `product_research_context_version`
  - `product_analysis_specification`
  - `product_family_execution.research_context_version_id`
  - `product_family_execution.analysis_specification_id`
- 既存Resultの変更・削除なし

## Architecture guard check

- PREPAREはSPLIT後であり、DAG順序は`split, prepare, train, evaluate`
- Stage間連携はGeneric Workflow bindingを使用し、HTTP downloadを使用しない
- Generic ExecutorへPredictive固有分岐を追加していない
- preprocessor fitはTRAIN限定。VALIDATION / TESTはtransformのみ
- TRAIN input contractはTEST / evaluation bundleを含まない
- tuning selectionへTESTを含むSpecificationはFIX前にrejectする
- EVALUATEはfrozen model / frozen TRAIN-fitted preprocessorとfinal-evaluation-only TEST bundleを使用する
- model objectはArtifactへ保存し、Result JSONはlibrary-neutral descriptorを正本とする
- Execution technical statusとPredictive Result analytical statusは別fieldに保存する
- physical Artifact promotion失敗時は保存済みobjectをcompensateし、Stage successとの不整合を残さない
- Predictive UI、Explain Runner、Model Card、Cross-family summaryは追加していない

## Known deviations

- なし。

## Known limitations

- ExplanationはG5範囲のため`explanation_available=false`であり、非空`explanation_spec`をrejectする。
- G4のModel Registryは2 modelだけであり、candidate tuning / AutoMLは実装していない。
- Predictive UIはG5まで後送している。

## Files intentionally excluded

- `00_enhance_plan_documents/06b_Ariadne_ENH-E3_実装再開指示書.md`
- `00_enhance_plan_documents/07b_Ariadne_ENH-E3_テスト指示書.md`
- G5 / G6 production code、test code、report
- backup / inventory / approval document

## Required Test Agent focus

1. `20260807_product_0004 -> 0005` clean upgradeとsingle head
2. `0005 -> 0004 -> 0005` round tripおよび既存Result保持
3. Research Context / Analysis SpecificationのProject境界、FIXED immutable、revise、usage
4. Plan DAG、Runner registration、binding schemaとTEST非流入
5. Binary / Regressionのtraining determinism、task/model/metric compatibility
6. Classification / Regression metricsと明示的analytical status
7. API submit 202、Worker claim、Stage状態、cancel/retry/rerun/revise/prefill
8. Snapshot、Artifact metadata、Result、Lineage chain、promotion compensation
9. G1-G3、PostgreSQL、full active suiteの回帰

Test execution by Coding Agent: NOT PERFORMED

Static implementation check: target 27 Python files parsed successfully; `git diff --check` clean; migration chain statically observed as `0001 -> 0002 -> 0003 -> 0004 -> 0005`.
