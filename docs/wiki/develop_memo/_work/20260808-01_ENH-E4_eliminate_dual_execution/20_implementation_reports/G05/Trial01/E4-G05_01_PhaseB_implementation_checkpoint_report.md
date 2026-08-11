# E4-G05 Trial 01 Phase B Implementation Checkpoint Report

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Gate: E4-G05
- Trial: 01
- Phase: B — Exploratory canonical read/output convergence
- Phase Status: PHASE_B_COMPLETE
- Branch: `refactor/ariadne_mvp_e4`
- Phase baseline checkpoint: `b8a3f5502f82fcca8cb9634bd8368e3ebc9f0344`
- Phase starting commit: `5d0718ead97a55df81c4c6db1d2283a451c828f0`
- Phase checkpoint implementation commit: `b77e3febd9c6c48b553bc59cd8e5be29f2aba998`
- Report commit: e6c410de6ec4d928c6c3ec8b9647d6ff39a92008
- Migration head: `20260809_product_0010`
- Started at: UNKNOWN
- Finished at: `2026-08-09T07:49:54Z`

## 1. Input

- Phase implementation instruction: `docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/10_enhance_instruction/G05/06h01_Ariadne_ENH-E4_G05_PhaseB_実装指示書.md`
- Previous phase checkpoint/report: `b8a3f5502f82fcca8cb9634bd8368e3ebc9f0344` / `docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G05/Trial01/E4-G05_01_PhaseA_implementation_checkpoint_report.md`

## 2. Scope Implemented

Exploratory の Product-facing Result read と downstream draft 作成を canonical authority に収束させた。canonical runtime mode では `product_result` と、その所有者である `product_execution` を join して読む。`FamilyResultOrm` / `FamilyExecutionOrm` への lookup、canonical ID の lookup miss 時の旧表 fallback、read のための shadow write は追加していない。

既存の `FamilyResultResponse` 互換 shape は維持した。class 名は legacy のままだが、canonical Result を `ExploratoryResultProjection` へ変換してから API response を生成する。従って response compatibility のために旧 Family Result row は必要としない。

## 3. Files Changed

### Added

- `tests/product/test_enh_e4_g05_phase_b_exploratory_postgres.py`
- `docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/20_implementation_reports/G05/Trial01/E4-G05_01_PhaseB_implementation_checkpoint_report.md`

### Modified

- `src/ariadne/product/application/exploratory_service.py`
- `src/ariadne/interfaces/web_api/routers/exploration.py`

### Deleted

NONE

## 4. Implementation Details

- `get_execution` / `list_executions` の canonical Execution read は維持した。
- canonical mode の `list_results(project_id)` は canonical Result と canonical Execution を project / `EXPLORATORY` family で絞り込み、`ExploratoryResultProjection` を返す。
- canonical mode の `get_result(project_id, result_id)` は同じ ownership/family predicate を使う。不一致、別 project、CAUSAL Result は `EntityNotFound` となり、旧 Family Result を探索しない。
- projection は canonical Result の `result_type`、`scientific_status`、`summary_json`、`payload_json`、`diagnostics_json`、`warning_json`、`created_at`、canonical `stage_execution_id` をそのまま保持する。`schema_version` は Phase A contract の canonical payload field から読み、固定値・ResultType 推測・旧表補完を行わない。
- `create_analysis_draft` は canonical Result と canonical Execution context を使う。返却する `dataset_version_id` は canonical Execution、`analysis_view_id` は canonical Execution の immutable `analysis_spec_json` から取得する。
- `MOTIVATED` relation の `source_result_id` は canonical Result ID を保持する。G06 の lineage authority 統合は実施していない。

## 5. Automated Test Code Added / Changed

`test_enh_e4_g05_phase_b_exploratory_postgres.py` を追加した。

- canonical Exploratory execution の get/list read を確認する。
- fresh Session/UoW 後の canonical Result list/get projection を確認する。
- Result ID、project、Execution、StageExecution、family、typed ResultType、ScientificStatus、schema_version、summary、payload、diagnostics、warnings、created_at の保持を確認する。
- API の `_result` projection が `FamilyResultResponse` 相当の値を canonical projection だけで作れることを確認する。
- CAUSAL / PREDICTIVE の両 target に対する `create_analysis_draft`、canonical source Result ID、canonical dataset/view context、`MOTIVATED` relation を確認する。
- cross-project Result、non-EXPLORATORY canonical Result、invalid target family を拒否することを確認する。
- read/draft 操作前後の `FamilyExecutionOrm` と `FamilyResultOrm` row count が不変であることを確認する。

## 6. Migration

- Added migration: NONE
- Starting migration head: `20260809_product_0010`
- Ending migration head: `20260809_product_0010`
- Rationale: Phase B は read/projection convergence であり、Phase A の typed canonical Result contract で必要な値を lossless に取得できた。

## 7. Changes to Passed Gates / Earlier G05 Phases

- Phase A typed family Result/Artifact semantics は変更していない。
- G04 Result/Artifact PostgreSQL regression は standard runner で PASS した。
- Product PostgreSQL contract は standard runner で PASS した。
- G02/G03 の最終 G05 regression は Phase B scope 外であり、NOT_RUN である。

## 8. Known Limitations / Remaining G05 Work

- Phase C: Predictive read projection と mutation delegation は NOT_RUN。
- Phase D: old Exploratory/Predictive lifecycle authority shutdown と no-fallback final audit は NOT_RUN。
- Phase E: cross-family Golden Path、全 old-table row-count negative、G02/G03/G04 final regression、TD closure、G05 final report は NOT_RUN。

historical Family ORM read compatibility branch は残っているが、Product API injection による canonical runtime mode の canonical Result lookup に fallback はない。legacy source の retirement は G07 scope である。

## 9. Explicit Out-of-Scope Work

- Predictive convergence / mutation delegation
- old family `claim_next()` / `process_execution()` shutdown
- full old-table negative matrix、canonical failure no-fallback final audit
- cross-family final Golden Path、TD-001/002/003 closure、TD-004 inventory
- G06 lineage final consolidation、G07 legacy retirement
- E4-G05 final completion report と `READY_FOR_TEST`

## 10. Git Evidence

- `git rev-parse HEAD`（implementation checkpoint）: `b77e3febd9c6c48b553bc59cd8e5be29f2aba998`
- `git status --short`（implementation checkpoint 後）: Phase A instruction の user edit、untracked Phase B instruction、既存 report directory のみ。これらは checkpoint implementation commit に含めていない。
- implementation diff stat: `3 files changed, 309 insertions(+), 3 deletions(-)`。
- `git diff --check`: exit `0`。

## 11. Phase Verification Evidence

- Tested checkpoint SHA/state: `b77e3febd9c6c48b553bc59cd8e5be29f2aba998`。この implementation checkpoint を含む production/test state を report commit 前に standard runner で検証した。
- Exact command:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g05_phase_b_exploratory_postgres.py \
  tests/product/test_enh_e4_g05_phase_a_postgres.py \
  tests/product/test_enh_e4_g04_result_artifact_postgres.py \
  tests/product/test_postgres_contract.py
```

- Exit code: `0`
- Passed: `12`
- Failed: `0`
- Skipped: `0`
- Migration verification: `20260809_product_0010 (head)`
- Raw evidence: `test-results/postgres/run-20260809T074904Z.txt`, `test-results/postgres/run-20260809T074904Z.metadata.txt`
- 補足: 初回二回の失敗は新規 test seed が FK owner を flush する順序の不備だった。production source / schema defect ではない。Project、Artifact、Dataset、Execution、StageExecution の順に flush するよう test を修正し、最終 run は上記のとおり PASS した。

## 12. Next-Phase Handoff

- Next phase: Phase C
- Ready for Phase C: YES
- Gate READY_FOR_TEST: NO

Phase C は Predictive canonical read projection と lifecycle mutation delegation に限定して開始できる。Phase B の canonical Exploratory read/draft authority を旧 Family ORM に戻してはならない。

## 13. Design Block

- Contradiction: NONE
- Observed facts: Phase A canonical Result payload に schema/version が保存され、canonical Execution に project、family、dataset、analysis view snapshot が保存されている。
- Impact: 必要な Exploratory response/draft context は minimal projection で lossless に構成できた。
- Decision required: NONE
