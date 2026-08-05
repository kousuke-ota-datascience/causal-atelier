# 99 実装移行結果レポート

- 作成日時: 2026-08-05 07:29 UTC
- 対象計画: `40_実装移行計画.md`
- 対象設計: `30_詳細設計.md`
- 実施範囲: Phase 0〜3（Baseline固定 / Scientific Core Adapter / Product Domain+DB / 新API+Worker+CLI）

---

## 1. 実施概要

移行計画に従い、前身コードをそのまま改修するのではなく、新Product Domainを独立して新規構築し、前身コードを `legacy/` 配下に凍結する方式で実施した。

---

## 2. ディレクトリ構造の変更

### 2.1 新規作成パッケージ

```
src/ariadne/
├── product/               # 新Domain / Application / Persistence
│   ├── domain/            # 7 Entity + enums + errors
│   ├── ports/             # Repository / UoW / ArtifactStore / ScientificCore / Clock
│   ├── application/       # Application Service群
│   └── persistence/       # SQLAlchemy ORM + Repository実装 + UoW + SessionFactory
├── interfaces/
│   ├── web_api/           # 新FastAPI アプリケーション
│   │   ├── routers/       # 6ルーター
│   │   ├── schemas/       # Pydantic Response / Request DTO
│   │   ├── dependencies.py
│   │   └── error_handlers.py
│   ├── worker/            # 新Execution Worker
│   │   ├── execution_processor.py
│   │   └── runner.py
│   └── cli/               # 新CLI
│       ├── discovery.py   # ariadne-discover
│       ├── estimation.py  # ariadne-estimate
│       └── manifest.py
├── scientific/            # causal/ へのAdapter
│   ├── core_adapter.py    # ScientificCorePort 実装
│   ├── discovery/adapter.py
│   └── inference/adapter.py
└── adapters/
    └── local_artifact_store.py  # ArtifactStorePort 実装
```

### 2.2 凍結（legacy/）

前身の Control Plane を `src/ariadne/legacy/` に移動し、新コードからの参照を禁止する。

```
src/ariadne/legacy/
├── application/   # 旧 Application Service群 (Pipeline / run_execution等)
├── domain/        # 旧 ORM Entity (metadata.py)
├── workers/       # 旧 Worker
├── etl/           # CompleteJourney ETL
└── interfaces/
    ├── api/       # 旧 FastAPI ルーター
    └── cli/       # 旧 CLI (discovery / inference / pipeline)
```

### 2.3 継続利用（REUSE / ADAPT）

| パッケージ | 判定 | 扱い |
|---|---|---|
| `ariadne.causal.*` | ADAPT | `scientific/` アダプター経由で利用 |
| `ariadne.preprocessing.*` | REUSE候補 | 直接参照可（純粋関数） |
| `ariadne.infrastructure.*` | — | 凍結対象外・既存設定として残存 |
| `ariadne.shared.*` | REUSE | 直接参照可 |

---

## 3. 新規実装ファイル一覧

### 3.1 product/domain/ （7 Entity + 共通）

| ファイル | 内容 |
|---|---|
| `enums.py` | ProjectStatus / ExecutionOperation / ExecutionStatus / GraphVersionStatus / GraphType / ResultType / ScientificStatus |
| `errors.py` | EntityNotFound / ProjectBoundaryViolation / InvalidStateTransition / InvalidAnalysisSpec / GraphAlreadyFixed 等 |
| `project.py` | `update_metadata()` / `archive()` |
| `artifact.py` | Artifact値保持 |
| `dataset_version.py` | DatasetVersion値保持 |
| `execution.py` | `mark_running()` / `mark_succeeded()` / `mark_failed()` / `request_cancel()` / `increment_retry()` |
| `result.py` | Result値保持 |
| `graph_version.py` | `apply_edit()` / `fix()` |
| `annotation.py` | `update_content()` + target XOR バリデーション |

### 3.2 product/ports/

| ファイル | 内容 |
|---|---|
| `repositories.py` | 7 Repository Protocol |
| `unit_of_work.py` | UnitOfWork Protocol |
| `artifact_store.py` | ArtifactStorePort Protocol + StoredArtifact |
| `scientific_core.py` | ScientificCorePort Protocol + DiscoveryInput / EstimationInput / Output |
| `clock.py` | ClockPort Protocol + SystemClock |

### 3.3 product/application/

| ファイル | 主要 use case |
|---|---|
| `project_data_service.py` | `create_project` / `update_project` / `register_dataset_version` |
| `execution_service.py` | `create_execution_batch` / `get_execution` / `request_cancel` / `retry_execution` |
| `graph_version_service.py` | `create_from_discovery_result` / `update_draft` / `fix_graph` |
| `annotation_service.py` | `create_annotation` / `update_annotation` |
| `comparison_query_service.py` | `compare(result_ids)` → ComparisonView |
| `lineage_query_service.py` | `get_lineage(result_id)` → LineageView |

### 3.4 product/persistence/

| ファイル | 内容 |
|---|---|
| `orm_models.py` | ProductBase + 7 ORM クラス（テーブル名プレフィックス `product_`） |
| `repositories.py` | Sql*Repository 7クラス（ORM ↔ Domain Entity マッピング含む） |
| `unit_of_work.py` | SqlUnitOfWork（contextmanager対応） |
| `database.py` | SessionFactory + `create_all_tables` |

### 3.5 interfaces/web_api/ ルーター

| ルーター | エンドポイント |
|---|---|
| projects | POST `/projects`, GET/PATCH `/projects/{id}` |
| dataset_versions | POST `/projects/{id}/dataset-versions`, GET一覧/単体 |
| executions | POST `/projects/{id}/execution-batches`, GET一覧/単体, POST cancel/retry |
| results | GET `/executions/{id}/results`, GET `/results/{id}` |
| comparisons | POST `/comparisons/query` |
| lineage | GET `/results/{id}/lineage` |
| graph_versions | POST/GET/PATCH, POST fix |
| annotations | POST/GET/PATCH |

### 3.6 interfaces/worker/

| ファイル | 内容 |
|---|---|
| `execution_processor.py` | claim → Scientific呼出し → Artifact保存 → Result/Execution更新 (1 transaction) |
| `runner.py` | SQLポーリングループ + SIGTERM/SIGINT ハンドリング |

### 3.7 interfaces/cli/

| コマンド | 実体 | 出力 |
|---|---|---|
| `ariadne-discover` | `cli/discovery.py:main` | `manifest.json` + Artifact |
| `ariadne-estimate` | `cli/estimation.py:main` | `manifest.json` + Artifact |

Exit code: 0=正常（科学的負結果含む）, 3=入力ファイルエラー, 4=Scientific Coreエラー

### 3.8 scientific/

| ファイル | 内容 |
|---|---|
| `core_adapter.py` | `ScientificCoreAdapter`（ScientificCorePort実装） |
| `discovery/adapter.py` | `DiscoveryAdapter` → `causal.discovery.CausalDiscovery` 呼出し |
| `inference/adapter.py` | `EstimationAdapter` → `causal.inference.estimators` 呼出し（fallback: econml直接） |

### 3.9 adapters/

| ファイル | 内容 |
|---|---|
| `local_artifact_store.py` | `LocalArtifactStore`（shutil + SHA-256） |

---

## 4. DB スキーマ

### 4.1 新規テーブル（`product_` プレフィックス）

| テーブル名 | 主要カラム | 備考 |
|---|---|---|
| `product_project` | project_id, name, topic, objective, memo, status, created_at, updated_at | status CHECK: ACTIVE/ARCHIVED |
| `product_artifact` | artifact_id, project_id, execution_id, result_id, artifact_type, object_key (UNIQUE), content_hash, media_type, size_bytes | size_bytes >= 0 |
| `product_dataset_version` | dataset_version_id, project_id, source_artifact_id (UNIQUE), dataset_key, version_label, content_hash | UQ(project_id, dataset_key, version_label), UQ(project_id, dataset_key, content_hash) |
| `product_execution` | execution_id, project_id, dataset_version_id, input_graph_version_id, batch_key, operation, snapshot_hash, status, worker_token | operation CHECK: DISCOVERY/ESTIMATION, status CHECK: 5値 |
| `product_result` | result_id, execution_id, result_type, scientific_status, summary_json, payload_json, diagnostics_json, warning_json | — |
| `product_graph_version` | graph_version_id, project_id, source_result_id, parent_graph_version_id, graph_json, content_hash, status | status CHECK: DRAFT/FIXED |
| `product_annotation` | annotation_id, project_id, target_result_id, target_graph_version_id, statement, assumptions_json, limitations_json | target XOR CHECK |

### 4.2 マイグレーション環境

| 項目 | 設定 |
|---|---|
| 設定ファイル | `alembic_product.ini` |
| スクリプトディレクトリ | `product_migrations/` |
| バージョンテーブル | `alembic_version_product`（legacy と分離） |
| ベースラインリビジョン | `20260805_product_0001` |
| 環境変数 | `ARIADNE_PRODUCT_DATABASE_URL`（なければ `ARIADNE_DATABASE_URL` にfallback） |

---

## 5. エントリポイント変更

### 変更後 (`pyproject.toml`)

```toml
[project.scripts]
# 新 product CLI
ariadne-discover = "ariadne.interfaces.cli.discovery:main"
ariadne-estimate = "ariadne.interfaces.cli.estimation:main"
# 新 API / Worker
ariadne-api     = "ariadne.interfaces.web_api.app:main"
ariadne-worker  = "ariadne.interfaces.worker.runner:main"
# Legacy CLI エイリアス（非推奨 – 互換期間終了後に削除）
ariadne-discovery = "ariadne.legacy.interfaces.cli.discovery:main"
ariadne-inference = "ariadne.legacy.interfaces.cli.inference:main"
ariadne-pipeline  = "ariadne.legacy.interfaces.cli.pipeline:main"
```

---

## 6. 依存方向の確認

### 6.1 `product/` からの外部依存

`src/ariadne/product/` 配下から `ariadne.causal.*`・`ariadne.legacy.*` への参照：**0件**

```
$ grep -r "from ariadne\." src/ariadne/product/ \
  | grep -v "ariadne\.product\." | grep -v "ariadne\.legacy\."
(no output)
```

### 6.2 `scientific/` からの参照

- `ariadne.causal.discovery.algorithms.CausalDiscovery`（関数内遅延import）
- `ariadne.causal.inference.estimators.run_ate_estimation`（関数内遅延import + ImportError fallback）

Product Domain は `ScientificCorePort` 越しにのみ参照する。

---

## 7. 動作確認

### 7.1 モジュール import 確認（全件 OK）

| モジュール | 結果 |
|---|---|
| `ariadne.product.domain` | OK |
| `ariadne.product.ports` | OK |
| `ariadne.product.application` | OK |
| `ariadne.product.persistence.orm_models` | OK |
| `ariadne.product.persistence.unit_of_work` | OK |
| `ariadne.scientific.core_adapter` | OK |
| `ariadne.adapters.local_artifact_store` | OK |
| `ariadne.interfaces.web_api.app` | OK |
| `ariadne.interfaces.worker.runner` | OK |
| `ariadne.interfaces.cli.discovery` | OK |
| `ariadne.interfaces.cli.estimation` | OK |

### 7.2 DB スキーマ作成確認

SQLite で `ProductBase.metadata.create_all()` を実行し、7テーブル全件作成を確認。

```
product_project, product_artifact, product_dataset_version,
product_execution, product_result, product_graph_version, product_annotation
```

### 7.3 Smoke テスト（Project → DatasetVersion → ExecutionBatch）

```
Project:  9e3813a1 status=ACTIVE
DatasetV: 184f322f hash=54ec13df
Batch:    71084b1f execution=bd7d7bd8
Exec:     status=QUEUED algo=pc
Smoke test PASSED
```

---

## 8. 残作業（Phase 4 以降）

| Phase | 内容 | 状態 |
|---|---|---|
| Phase 4 | Web App（4 Workspace フロントエンド） | 未着手 |
| Phase 5 | Compatibility Adapter（C2対象 endpoint） | 未着手 |
| Phase 6 | Cutover（Legacy write停止・新DB構築・smoke test） | 未着手 |
| Phase 7 | Legacy廃止・互換縮退 | 未着手 |

### 8.1 次に実施すべき作業

1. **Architecture Test** — `product/` → `legacy/` の import 禁止を自動 test 化（`tests/unit/test_architecture.py`）
2. **Unit Test** — Entity 状態遷移・Comparison 分類・Lineage traversal
3. **Repository Integration Test** — FK / CHECK / UNIQUE 制約・Execution claim 排他性
4. **`alembic_product.ini`** — `product_migrations/` を参照する ini ファイルの作成
5. **`product/application/artifact_service.py`** — `get_dataset_preview` など読取 service の追加
6. **Worker の `claim_next` の transaction 分離** — RUNNING 更新を claim と同一 transaction にする実装の強化

---

## 9. ファイル数サマリー

| 区分 | ファイル数 |
|---|---|
| 新規実装（product / scientific / adapters / interfaces） | 55 |
| legacy/ に移動した前身コード | 76 |
| 継続利用（causal / preprocessing / infrastructure / shared） | 85 |
