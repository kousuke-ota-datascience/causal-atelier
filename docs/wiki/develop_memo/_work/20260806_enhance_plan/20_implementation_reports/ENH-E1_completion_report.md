# ENH-E1 Implementation Completion Report

## 1. 判定

実装および自動検証は完了した。ただし、WP-9の必須項目であるBrowser E2Eは、実行環境のFirefox snap mount namespace制約により未実施である。このため、`06_Ariadne_ENH-E1_実装指示書.md` 14.3の意味での最終判定は **INCOMPLETE** とする。

## 2. 受入れ証跡

- Instruction baseline: `f5e6e5ad5774a3951af5af65b724c4b53aada56a`
- 実作業開始HEAD: `47b12a960f5c4858ebd506848858209ba22aa56d`
- Branch: `prototype/ariadne_mvp_e1_scientific_enhance`
- Completed commit: 未作成（worktree変更）
- Environment: Linux 6.8.0-136-generic x86_64 / Python 3.12.3
- Main package versions: numpy 2.2.6, pandas 3.0.2, scipy 1.13.1, statsmodels 0.14.6, SQLAlchemy 2.0.51, FastAPI 0.139.0
- Migration head: `20260806_product_0002`

## 3. Work Package Completion Reports

### WP-0 Requirements Gate

- Requirements: 全ENH-E1要件
- Evidence: 01〜06および改定後の要件・基本設計・詳細設計を確認した。
- Deviation: 指示書記載baselineと実作業開始HEADが一致しない。既存branchのHEADを保存して実装した。

### WP-1 Domain / Persistence Contract

- Requirements: FR-038, FR-046, FR-064, FR-065, NFR-003, NFR-004
- Changed files: `product/domain/{enums,execution,result,graph_version}.py`, `product/persistence/{orm_models,repositories}.py`, migration 0002
- Tests: `test_enh_e1_contract.py`, `test_postgres_contract.py`
- Evidence: Operation / Result Status / Graph Origin matrix、空DB upgrade、downgrade、再upgradeが成功。

### WP-2 Snapshot / API Contract

- Requirements: FR-035〜037, FR-051〜054, NFR-009〜011
- Changed files: `product/domain/analysis_spec.py`, `product/application/execution_service.py`, Web API schemas/router/error handler
- Tests: schema v2 unknown-field reject、override、snapshot hash、upstream mismatchを自動テスト。

### WP-3 Graph Provenance

- Requirements: FR-025〜029
- Changed files: Graph domain/service/router、Discovery adapter、frontend
- Tests: Graph Origin matrixおよびAPI E2Eで `DISCOVERED -> CONSTRAINT_ADJUSTED -> USER_EDITED`、parent/source、hash差を確認。

### WP-4 Identification / Data Eligibility

- Requirements: FR-038〜039, FR-050, FR-064〜067
- Changed files: Scientific Core port、Identification adapter、Worker
- Tests: randomized/back-door、non-identification、post-treatment、collider、missing node/column、duplicate unit、CPDAG/PAG review、poor overlap。

### WP-5 Estimation Gate / Diagnostics

- Requirements: FR-051〜055
- Changed files: ScientificValidationService、Inference adapter、Worker
- Tests: identification-first、non-identified reject、同一IdentificationをOLS/IPWで再利用、Treatment EffectとDiagnosticsの分離、Capability Registry完全性。

### WP-6 Refutation / Sensitivity

- Requirements: FR-056〜059
- Changed files: Refutation/Sensitivity adapters、Core adapter、Worker
- Tests: placebo、subset、adjustment-set variation、propensity clipping、seed再現性、上流lineage。表示文言は仮定の証明を明示的に否定する。

### WP-7 UI / CLI / Query

- Requirements: FR-046〜049, FR-054〜063, NFR-007〜008
- Changed files: frontend、identify/refute/sensitivity CLI、manifest、comparison/lineage query
- Tests: Frontend contract、CLI contract、recursive lineage、comparison compatibility、API E2E。
- Deviation: Browser E2Eは未実施。UIにはIdentification gate、Eligibility、override、capability、Refutation、Sensitivity、Result filter、Graph provenance/editorを実装済み。

### WP-8 Scientific Benchmark

- Requirements: NFR-013〜014
- Changed files: `tests/scientific_benchmarks/test_enh_e1_benchmarks.py`
- Command: `pytest -q -m scientific_benchmark`
- Result: `8 passed, 56 deselected`
- Evidence: deterministic gate、post-treatment、CPDAG/PAG、poor overlap、100 independent seedsのbias/coverage gate、refutation/sensitivity再現性。

### WP-9 Final Verification

- Unit/Component/API/Worker/Frontend contract: `61 passed, 3 skipped`
- PostgreSQL contract: `3 passed`
- Compose golden path: `PASS`（Discovery 3、Estimation 3、lineage/artifact/export）
- Backup/Restore: `pg_dump -Fc`および`pg_restore`成功、復元先のExecution 7件を確認。
- Static checks: `compileall`および`git diff --check`成功。
- Migration: 空DB upgrade / downgrade / re-upgrade成功。
- Browser E2E: 未実施。`/snap/bin/geckodriver`起動時にhost mount namespace変更が拒否された。

## 4. 要件・Testトレーサビリティ

| 要件 | Test / Evidence |
|---|---|
| FR-025〜029 | `test_enh_e1_contract.py::test_graph_origin_contract_matrix`, API E2E provenance chain |
| FR-035〜037 | `test_snapshot_v2_rejects_unknown_fields_and_incomplete_override`, snapshot tests |
| FR-038〜039, FR-064〜067 | scientific adapter tests、benchmark deterministic statuses |
| FR-050 | Identification API E2EのData Eligibility、poor-overlap benchmark |
| FR-051〜053 | API E2E identification-first/non-identification、override tests |
| FR-054〜055 | Capability registry contract、複数Estimator/Diagnostics E2E |
| FR-056〜059 | refutation/sensitivity adapter test、API E2E、benchmark reproducibility |
| FR-046〜049 | comparison/recursive lineage/API E2E/Annotation lineage |
| FR-060〜063 | analysis mode/schema validation、Frontend contract |
| NFR-009〜011 | canonical snapshot/hash tests、CLI manifest tests、seed reproducibility |
| NFR-012 | architecture/import boundary tests |
| NFR-013〜014 | `tests/scientific_benchmarks/`、marker分離実行 |
| NFR-015 | 本報告 |

## 5. Known Limitations / 未完了項目

1. Browser E2Eのみ未実施。実行可能なFirefox/Chromium + WebDriver環境で再検証が必要。
2. 既存データ保持は指示書どおりMigration要件外。旧schemaの非空DBへ0002を直接適用する場合は、既存ESTIMATIONのupstreamを補完できないため失敗する。空DB migrationは成功済み。
3. 元リポジトリ `/loc0/bigbrother/repositories/causal-atelier` はread-onlyであり、成果物は `/home/bigbrother/causal-atelier` にある。
