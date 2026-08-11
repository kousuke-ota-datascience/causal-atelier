# E4-G05 Trial 01 Phase D D2 — 実行状況報告

## 結論

`PHASE_D_D2_COMPLETE`。Phase D の D2（legacy lifecycle/write branch shutdown と限定的 historical read compatibility）を完了した。Phase D 全体および D3、G05 全体の完了を意味しない。

- D2 production checkpoint: `ce3a9afd303d408d3b9b36fbb7a91349dbabe514`
- 親 D1 checkpoint: `e831e3f78d4791a2d4a0ef96f6ce80058c376fae`
- Product migration head: `20260809_product_0010`（変更なし）
- `git diff --check ce3a9afd^ ce3a9afd`: PASS

## 実施内容

### Product mutation authority

`ExploratoryWorkspaceService` と `PredictiveWorkflowService` は、canonical `ExecutionService` がない場合、Product execution operation の先頭で `LegacyProductAuthorityDisabled` を送出するよう固定した。したがって、optional dependency の有無によって canonical/Family ORM の書込み authority が切り替わる経路は存在しない。

FastAPI の `get_exploratory_workspace_service` と `get_predictive_workflow_service` はいずれも canonical `ExecutionService` を注入する。D2 で発見した `PredictiveSplitService.validate_and_save()` は、旧 `FamilyExecution`、`FamilyStageExecution`、`FamilyArtifact` を直接作成する Product API 経路だったため、canonical への偽装委譲は行わず `EXPLICIT_REJECT` に変更した。FastAPI provider にも canonical dependency を注入した。

残存する `PredictiveSplitService.get_partition_artifact()` は、historical `PARTITION_INDEX` artifact の限定 read-only adapter である。新規 execution の get/list/stage/result/artifact/lineage と lifecycle mutation は canonical projection/delegation を使用する。canonical ID lookup miss は Family table lookup に fallback しない。

### lifecycle / output branch の disposition

| surface | source | canonical dependency | Family read | Family write | D2 disposition |
| --- | --- | --- | --- | --- | --- |
| Exploratory submit / draft | `ExploratoryWorkspaceService` | mutation 時に必須 | historical branch は到達不能 | 到達不能 | `DELEGATE_CANONICAL` / missing DI は `EXPLICIT_REJECT` |
| Exploratory claim / process | `ExploratoryWorkspaceService` | N/A | なし | 到達不能 | `EXPLICIT_REJECT`（D1 回帰） |
| Predictive submit/cancel/retry/rerun/revise/prefill | `PredictiveWorkflowService` | mutation 時に必須 | canonical projection のみ | 到達不能 | `DELEGATE_CANONICAL` / missing DI は `EXPLICIT_REJECT` |
| Predictive claim / process | `PredictiveWorkflowService` | N/A | なし | 到達不能 | `EXPLICIT_REJECT`（D1 回帰） |
| Predictive split validation | `PredictiveSplitService.validate_and_save` | FastAPI composition で注入 | なし | 到達不能 | `EXPLICIT_REJECT` |
| historical partition artifact | `PredictiveSplitService.get_partition_artifact` | provider で注入 | `FamilyArtifact` のみ | なし | `BOUNDED_READ_ONLY` |
| Causal submit/cancel/retry | `ExecutionService` と execution router | canonical service | canonical repository | canonical repository | `CANONICAL_ONLY` |

旧 retry body に残る `FamilyResult`/`FamilyArtifact` delete、lineage delete、ArtifactStore delete は、canonical dependency guard より後ろにある到達不能な retained source である。D2 direct reject test は retry を実行しても Family の4 table に差分がなく、artifact store の delete が呼ばれないことを固定した。canonical lookup failure は `EntityNotFound` として終了し、旧 Family authority を再活性化しない（Phase C C4 authority audit 回帰を含む）。

## D2 completion checklist

すべて `DONE`。

- [x] Product lifecycle/composition inventory
- [x] canonical dependency 不在時の silent Family mutation 防止
- [x] FastAPI Exploratory/Predictive/split composition の canonical dependency 注入
- [x] Causal lifecycle/composition inventory（`ExecutionService` canonical-only）
- [x] Exploratory/Predictive submit の旧 write authority shutdown
- [x] cancel/retry/rerun/revise の canonical delegation と旧 branch shutdown
- [x] old Result/Artifact mutation と physical artifact delete の Product reachability 排除
- [x] retained legacy mutation の direct call は canonical delegate 又は explicit reject
- [x] historical compatibility は bounded read-only、canonical miss の silent fallback なし
- [x] missing/canonical lookup failure が old Family authority を起動しない
- [x] Product lifecycle operation による新規 Family row なし
- [x] D1 claim/process explicit-reject regression
- [x] D2 boundary/real PostgreSQL tests、Phase C/B、G02/G03/G04 regression
- [x] migration head と diff check
- [x] D2 production checkpoint commit

## 検証証跡

### Boundary tests

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q \
  tests/product/test_enh_e4_g05_phase_d_d2_legacy_lifecycle_shutdown.py \
  tests/product/test_enh_e4_g05_phase_d_d2_legacy_lifecycle_shutdown_postgres.py \
  tests/product/test_predictive_split_api_e3.py \
  tests/product/test_enh_e4_g05_phase_d_d1_legacy_claim_shutdown_postgres.py \
  tests/product/test_exploratory_api_worker_e2e_e3.py \
  tests/product/test_predictive_api_worker_e2e_e3.py \
  tests/product/test_predictive_explanation_e3.py \
  tests/product/test_enh_e3_api_worker_e2e.py
```

結果: exit 0, `18 passed, 2 skipped in 17.85s`。

### Standard PostgreSQL runner — D2 / Phase B/C / G02/G04

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g05_phase_d_d2_legacy_lifecycle_shutdown_postgres.py \
  tests/product/test_enh_e4_g05_phase_d_d1_legacy_claim_shutdown_postgres.py \
  tests/product/test_predictive_api_worker_e2e_e3.py::test_predictive_execution_plan_async_worker_results_artifacts_and_lineage \
  tests/product/test_enh_e4_g05_phase_c_retry_postgres.py \
  tests/product/test_enh_e4_g05_phase_c_rerun_postgres.py \
  tests/product/test_enh_e4_g05_phase_c_revise_postgres.py \
  tests/product/test_enh_e4_g05_phase_c_authority_audit_postgres.py \
  tests/product/test_enh_e4_g05_phase_b_exploratory_postgres.py \
  tests/product/test_enh_e4_g02_canonical_execution.py \
  tests/product/test_enh_e4_g04_result_artifact_postgres.py
```

結果: exit 0, `18 passed in 4.71s`。runner は clean Product DB から `20260809_product_0010 (head)` への migration を確認した。証跡: `test-results/postgres/run-20260809T101835Z.txt`。

### Standard PostgreSQL runner — G03

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g03_acceptance_postgres.py \
  tests/product/test_enh_e4_g03_generic_executor_boundary.py
```

結果: exit 0, `12 passed in 1.31s`。証跡: `test-results/postgres/run-20260809T101902Z.txt`。

## D2 architecture answers

| question | answer | 根拠 |
| --- | --- | --- |
| Q1 canonical dependency なしで旧 submit authority が復活するか | NO | service mutation guard と D2 direct reject test |
| Q2 cancel/retry/rerun/revise が Family lifecycle を mutation できるか | NO | canonical delegation 又は explicit reject、PostgreSQL row-count negative |
| Q3 retry が Family Result/Artifact を delete/reset できるか | NO | guard 前置、D2 direct reject/row-count negative |
| Q4 canonical lookup miss が旧 lifecycle へ fallback するか | NO | canonical-only lookup、Phase C C4 authority audit |
| Q5 historical read が mutation authority として再利用できるか | NO | bounded `get_partition_artifact` と canonical-only lifecycle |
| Q6 FastAPI composition が canonical dependency なしの legacy mutation service を生成できるか | NO | provider injection boundary test |

## 非対象・次工程

D3 および Phase D final checkpoint は未実施である。本書は D2 の in-progress evidence であり、`E4-G05_01_PhaseD_implementation_checkpoint_report.md` は作成しない。
