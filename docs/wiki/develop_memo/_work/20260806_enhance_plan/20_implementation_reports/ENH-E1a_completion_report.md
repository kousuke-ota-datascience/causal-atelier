# ENH-E1a Reimplementation and Retest Completion Report

## 1. Final Decision

**COMPLETE**

事実: `AUD-E1-001`〜`AUD-E1-010`を下表のBehavior Testと実環境証跡で全件CLOSEDとした。全MUST要件、実Chromium E2E、11 scenarioの追加Scientific Benchmark、既存Golden Path、PostgreSQL、Migration、Backup/RestoreおよびCompleted Commitを確認した。主要Entityは既存7 Entityのままで、DB migrationは追加していない。

判断根拠: 指示書12.6の17条件をすべて満たす。defaultのfull pytestに表示される3 skipはPostgreSQL URL未設定時の条件付きtestであり、同じ3 testを隔離PostgreSQL URL付きで別途実行して全件PASSしたため、MUST要件の未実施skipではない。

## 2. Baseline and Completed Commit

- Baseline Commit: `d9908a11339194eadfd6d1af35b58bd9e3f2a2d0`
- Completed Commit (implementation): `cd645d7022eff9381bacb9d8e1635a4d76ec4e0c`
- Branch: `prototype/ariadne_mvp_e1_scientific_enhance`
- Migration head: `20260806_product_0002`
- Migration policy: ENH-E1a追加migrationなし。`revision_context`、`scientific_warnings`、`inferred_types`は既存Snapshot/Result JSONへ保存する。
- Design supplement: `10_Revised_requirements_definition_documents/31_ENH-E1a_設計追補.md`

注記: Git commitは内容アドレスなので、本報告書自身が格納されるcommit SHAを本文中へ自己参照できない。上記Completed Commitは検証対象の実装commitを指し、本報告書は後続documentation commitで格納する。

## 3. Changed Files

- Runtime/Product: `src/ariadne/product/{domain/analysis_spec.py,application/execution_service.py,application/scientific_validation_service.py,application/lineage_query_service.py}`
- Scientific Core: `src/ariadne/scientific/{identification/adapter.py,benchmark_report.py}`
- Interfaces: CLI 4 files、Web API router/schema 4 files、Worker 1 file、`frontend/{index.html,app.js}`
- Test: `tests/scientific/test_identification_e1a.py`、`tests/product/test_estimator_compatibility_e1a.py`、API/CLI/Frontend contract更新、`tests/scientific_benchmarks/test_enh_e1a_acceptance.py`、`tests/browser_e2e/run_enh_e1a.py`
- Reproducible environment: `compose.e1a.yaml`、`Dockerfile.browser-e2e`、`.dockerignore`、`.gitignore`、`pyproject.toml`、`uv.lock`
- Documentation: `31_ENH-E1a_設計追補.md`、本報告書
- Full implementation file list: `git show --name-only cd645d7022eff9381bacb9d8e1635a4d76ec4e0c`

## 4. Requirement / Audit Closure Matrix

| 監査ID | 要件ID | 設計文書・節 | 実装ファイル | Test Case | Test Command | 結果 | Evidence |
|---|---|---|---|---|---|---|---|
| AUD-E1-001 | WP-6, E2E-04〜06 | `31` §1, §5 | `frontend/*`, `compose.e1a.yaml`, `Dockerfile.browser-e2e` | 実UIによるIdentification-first、負結果、Graph provenance、E1a追加操作 | `docker compose ... --profile e2e run --build --rm browser-e2e` | CLOSED / PASS | `test-results/browser_e2e/evidence.json`, `trace.zip`, video, screenshots |
| AUD-E1-002 | FR-054 | `31` §2 | `scientific_validation_service.py`, CLI/API | 4軸、parameter、adjustment、overlap、API/CLI同一code | `pytest -q tests/product/test_estimator_compatibility_e1a.py tests/product/test_cli_contract.py` | CLOSED / PASS | behavior tests、Browserのbinary-outcome拒否 |
| AUD-E1-003 | NFR-013, NFR-014 | 指示書10、`tests/scientific_benchmarks/README.md` | `benchmark_report.py` | SB-E1A-001〜011、manifest/schema/threshold failure | `pytest -q -m scientific_benchmark` | CLOSED / 21 passed | `test-results/scientific_benchmarks/ariadne_ENH-E1a.json` |
| AUD-E1-004 | FR-050, FR-064, FR-065 | `31` §2 | `identification/adapter.py`, Worker | 文字列、非数値、列欠落、1 arm、小標本、propensity不能、artifact不能 | `pytest -q tests/scientific/test_identification_e1a.py tests/product/test_api_worker_e2e.py` | CLOSED / 22 passed | 負結果はExecution `SUCCEEDED`、artifact障害だけ`FAILED` |
| AUD-E1-005 | FR-038, FR-039 | `31` §3 | `identification/adapter.py` | Collider本人/子孫、無関係な高indegree node | 同上 | CLOSED / PASS | path-relative activated path evidence |
| AUD-E1-006 | FR-038, FR-039 | `31` §3 | `identification/adapter.py` | RANDOMIZED pre-treatment許可、post-treatment拒否 | 同上 | CLOSED / PASS | `test_randomized_design_*` |
| AUD-E1-007 | FR-064〜067 | `31` §3 | `identification/adapter.py` | CPDAG/PAG + 確定的不整合の優先順位 | 同上、benchmark SB-E1A-010 | CLOSED / PASS | `NOT_IDENTIFIED`が`REQUIRES_REVIEW`より優先 |
| AUD-E1-008 | FR-060〜062 | `31` §4 | `analysis_spec.py`, `execution_service.py`, `lineage_query_service.py` | RERUN/REVISED、理由必須、基準Execution lineage | `pytest -q tests/product/test_api_worker_e2e.py` + Browser | CLOSED / PASS | `revision_context`, `REVISED_FROM` |
| AUD-E1-009 | FR-063 | `31` §5 | `execution_service.py`, API/Worker/UI/CLI | exploratory負例、別Dataset負例、同Dataset confirmatory正例、決定論的source IDs | 同上 + Browser | CLOSED / PASS | `POST_SELECTION_INFERENCE_RISK`がSnapshot/Result/UIに保存 |
| AUD-E1-010 | NFR-015 | 指示書12 | 本報告書、全変更 | Full regression、PostgreSQL、migration、golden path、backup/restore | 下記全コマンド | CLOSED / PASS | Completed Commitと本matrix |

## 5. Work Package Completion Reports

### WP-0 Requirements Gate

- 要件正本と7 Entity方針を維持した。
- FR-062/063の保存位置が未定義だったため、実装前に最小設計追補を作成した。
- Baselineで `61 passed, 3 skipped`、benchmark `8 passed` を確認した。

### WP-1 Estimator Compatibility

- Estimand、Treatment Type、Outcome Type、Identification Strategyの4軸に加え、parameter、adjustment、diagnostic prerequisiteを受付時検証する。
- Product Domainへpandas/NumPy dtypeを保存せず、正規化typeと件数根拠だけを保存する。
- APIとCLIは共通validatorとmachine-readable error codeを使用する。

### WP-2 Eligibility / Technical State Separation

- prerequisite依存順でcheckを実行し、後続処理を`SKIPPED_DUE_TO_PREREQUISITE`または`NOT_APPLICABLE`として保存する。
- 科学的負結果をResultとして保存し、Executionは`SUCCEEDED`。Artifact読取障害は`FAILED`とする。
- statsmodelsの数値警告は外部warningへ漏らさず、`PROPENSITY_ESTIMATION` evidenceへ保存する。

### WP-3 Identification Validity

- Colliderを対象back-door path上のcollider/子孫に限定した。
- RANDOMIZEDではpre-treatment adjustmentを許可し、Treatmentの子孫だけを拒否する。
- 確定的不整合 > orientation review > identifiedのStatus優先順位を実装した。

### WP-4 Analysis Mode / Revision / Post-selection Warning

- 同条件再実行を`RERUN`、条件変更を`REVISED`として区別し、変更理由と差分を不変Snapshotへ保存する。
- 同一Project/Dataset Versionの先行DiscoveryがあるCONFIRMATORY Estimationへ決定論的警告を付与する。
- API response、Result warning、Lineage、Web UI、CLI manifestから再確認可能にした。

### WP-5 Scientific Benchmark

- 独立11 scenario、synthetic + statsmodels Longley由来semi-synthetic、複数seed、構造化artifact、閾値違反FAIL testを追加した。
- Gate: deterministic 1.0、post-treatment 1.0、non-identification 1.0、poor-overlap 1.0、最大標準化絶対bias `0.0069682631`、CI coverage `[0.96, 0.9666666667]`。

### WP-6 Browser E2E

- Playwright 1.62.0 / Chromium 151.0.7922.34を専用imageへ固定した。standalone WebDriverは使用しない。
- E2E-04、E2E-05、E2E-06、FR-062/063、RANDOMIZED正例、binary outcome拒否を実UI操作でPASSした。
- consoleの3件のHTTP 422は、変更理由なし、非識別推定、型非互換を意図的に送信した負ケースの期待応答である。

### WP-7 Full Regression / Reporting

- 全必須回帰、Migration往復、PostgreSQL contract、Golden Path、Backup/Restore、Architecture境界をPASSした。
- Completed Commitと本traceability matrixを作成した。

## 6. Test Commands and Results

| Command | Result |
|---|---|
| `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q` | `104 passed, 3 skipped in 24.82s` |
| `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q -m scientific_benchmark` | `21 passed, 86 deselected in 13.76s` |
| `ARIADNE_PRODUCT_TEST_DATABASE_URL=...:15432/ariadne .venv/bin/pytest -q tests/product/test_postgres_contract.py` | `3 passed in 3.16s` |
| `uv run pytest -q tests/product/test_api_worker_e2e.py tests/product/test_cli_contract.py tests/product/test_frontend_contract.py tests/product/test_architecture.py` | `19 passed in 13.54s` |
| `uv run pytest -q tests/scientific/test_identification_e1a.py tests/product/test_api_worker_e2e.py` | `22 passed`, warning 0 |
| `uv run python -m compileall -q src tests experiments` | PASS |
| `git diff --check` | PASS |
| Alembic `upgrade head -> downgrade 20260805_product_0001 -> upgrade head -> current` on `ariadne_e1a_migration_test` | PASS、final `20260806_product_0002 (head)` |
| `docker compose ... --profile e2e run --build --rm browser-e2e` | PASS、Project `d74f4b3d-48ce-4cb0-aa5b-c20dda1f97ad` |
| `ARIADNE_GOLDEN_PATH_BASE_URL=http://127.0.0.1:18000/api/v1 ... compose_golden_path_smoke.py` | PASS、Project `ab52b25e-672c-4e7e-807d-0406adc17df6`、Discovery 3、Estimation 3 |
| `pg_dump -Fc ariadne` + `pg_restore ... ariadne_e1a_restore_test` | PASS、dump 105273 bytes |

### Skip accounting

| Test | default skip理由 | 要件影響 | 完了判定 |
|---|---|---|---|
| `test_product_migration_contains_only_product_schema` | `ARIADNE_PRODUCT_TEST_DATABASE_URL`未設定 | なし。隔離PostgreSQLでPASS | 影響なし |
| `test_product_constraints_and_transaction_rollback` | 同上 | なし。隔離PostgreSQLでPASS | 影響なし |
| `test_claim_next_is_atomic_across_concurrent_workers` | 同上 | なし。隔離PostgreSQLでPASS | 影響なし |

MUST、Browser E2E、Scientific Benchmarkに未実施skipはない。

## 7. Environment and Artifacts

- OS: Linux 6.8.0-136-generic x86_64
- Python: 3.12.3; uv: 0.11.8; Docker Compose: 5.3.1
- Packages: ariadne 0.1.0; numpy 2.2.6; pandas 3.0.2; scipy 1.13.1; statsmodels 0.14.6; scikit-learn 1.6.1; SQLAlchemy 2.0.51; FastAPI 0.139.0; psycopg 3.3.4; pytest 9.0.3; Playwright 1.62.0
- Browser: Chromium 151.0.7922.34（Playwright bundled browser、standalone driverなし）
- Benchmark Artifact: `test-results/scientific_benchmarks/ariadne_ENH-E1a.json`（10316 bytes、`code_commit=cd645d7022eff9381bacb9d8e1635a4d76ec4e0c`、`gate_result=PASS`）
- Browser Artifacts: `test-results/browser_e2e/evidence.json`（2940 bytes）、`trace.zip`、video、screenshots
- Backup Artifact: `/tmp/ariadne-e1a-backup.dump`（105273 bytes）
- Backup/Restore entity counts: original = restored = Project 13、Dataset 14、Execution 104、Result 150、Graph 44、Artifact 152、Annotation 37（dump時点）

## 8. Known Limitations and Remaining Issues

- Known limitation: BenchmarkとBrowserのartifactは`.gitignore`対象であり、repositoryへcommitしない。各記載コマンドで決定論的に再生成する。
- Known limitation: 初回Browser runner buildには固定image/package取得のnetwork accessが必要。以後はDocker cacheで再実行可能である。
- Remaining implementation issues: なし。
- Workspace note: 作業開始時から未追跡だった監査書`07`と指示書`08`はユーザ所有物としてCompleted Commitへ含めていない。実装・検証結果への影響はない。
