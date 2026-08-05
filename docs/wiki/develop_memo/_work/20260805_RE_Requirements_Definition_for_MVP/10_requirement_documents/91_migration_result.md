# 91 実装移行結果レポート

- 更新日時: 2026-08-05 UTC
- Baseline commit: `bb059ffee047c777ab68a52393ebe492d579fca9`
- 対象: `41_ariadne_coding_agent_handoff_prompt_20260805.md` の Gate A〜I
- 判定: **完了**

## 1. 結論

Gate A〜Iの受入条件を満たした。新Web App / `/api/v1` / Product Worker / PostgreSQL Product DB / Local Artifact StoreだけでGolden Pathが完走した。正本業務EntityはProject、Dataset Version、Execution、Result、Artifact、Graph Version、Annotationの7件であり、ComparisonとLineageはQuery Projectionのままである。

根拠は、PostgreSQLを含む全36 Test、Compose起動、実Scientific Core Golden Path、backup/restore後の同一Golden Path、隔離DBでのAlembic downgrade/upgrade、runtime image検査である。

## 2. Phase別状態

| Phase | Gate | 状態 | 主な完了根拠 |
|---|---|---|---|
| Phase 0 | A | 完了 | Baseline固定、Test分類、互換性台帳、0 collection error |
| Phase 1 | B | 完了 | PC/GES、4 Estimator、Graph semantics、5 Scientific Status、DB非依存Adapter |
| Phase 2 | C | 完了 | 7 Entity、canonical snapshot、Project境界、FIXED Graph、Product baseline、DB制約 |
| Phase 3 | D/E | 完了 | atomic claim、Worker transaction、API v1、strict DTO、idempotency、CLI Manifest |
| Phase 4 | F | 完了 | 4 Workspaceを新APIだけで実装 |
| Phase 5 | G | 完了 | C2集合なし。Compatibility Adapterを実装せずC0へ整理 |
| Phase 6 | H | 完了 | Product Compose、backup/restore、Golden Path、rollback smoke |
| Phase 7 | I | 完了 | Legacy起動経路・CLI alias・DB接続を除去し、旧sourceをruntime package/imageから除外 |

## 3. 主な変更

### 3.1 Test baselineとCompatibility

- `tests/README.md`でActive Product、Scientific Characterization、Retired Legacy Control Planeを分類した。
- 旧Control Plane Testは`tests/legacy_archive/`へ隔離し、既定pytestの収集対象外とした。
- `41_互換性台帳.md`を追加した。実在client、owner、fixture、期限の根拠がないためC2集合は空とした。
- `ariadne-discovery`、`ariadne-inference`、`ariadne-pipeline` entrypointを削除した。

### 3.2 Scientific Core Adapter

- Scientific Statusを`VALID`、`NOT_IDENTIFIED`、`INSUFFICIENT_OVERLAP`、`INSUFFICIENT_SAMPLE`、`ESTIMATION_UNRELIABLE`へ統一した。
- DiscoveryはPC/GESを必須経路へ接続し、明示feature columns、対応済みconstraints、Graph type、endpoint semanticsを保持する。
- Estimationは既存`TreatmentEffectEstimator`とdiagnosticsへ接続し、Difference in means、OLS、IPW、AIPW、ATE/ATT、明示adjustment set、SE/CI、balance/overlap/sample-sizeを返す。
- EconML fallback、全列自動共変量化、未知parameterのsilent ignoreを削除した。
- 技術例外はtyped infrastructure errorとして上位へ伝播し、Scientific Resultへ変換しない。

### 3.3 Product Domain / Persistence

- Graph source Result、operation、Project、parent、endpoint semanticsを検証する。
- Estimationは同一Projectの`FIXED` Graph Versionだけを受け付ける。
- Annotation targetの存在、Project境界、XORをDomain/Application/DBで検証する。
- Execution Snapshotへobjective/rationale、Dataset/Graph ID+hash、operation、spec、method、parameters、seed、code/runtime versionを含め、key/NULL/numberをcanonical化した。
- Product PostgreSQL baseline `20260805_product_0001`と独立version table `alembic_version_product`を使用する。
- 業務7 tableに加え、技術用`product_idempotency` tableだけを追加した。
- FK、CHECK、UNIQUE、transaction rollbackをPostgreSQLで検証した。

### 3.4 Worker

- `SELECT ... FOR UPDATE SKIP LOCKED`、`RUNNING`、`started_at`、worker tokenを同一短時間transactionでcommitする。
- Dataset ArtifactとDataset Versionのhash、FIXED Graph hashをScientific Core呼出し前に検証する。
- Result、Artifact metadata、`SUCCEEDED`を同一DB transactionで保存する。
- DB保存失敗時は保存済みArtifactを削除する。
- Scientific negative outcomeはResult保存 + `SUCCEEDED`、technical exceptionは`FAILED`とした。retryでSnapshotは不変である。

### 3.5 Web API / CLI

- 全Endpointを`/api/v1`へ統一し、`GET /api/v1/projects`を設計と実装へ追加した。
- Dataset preview、Execution prefill、Result export、Artifact metadata/download、Comparison、Lineageを実装した。
- strict Pydantic DTO、unknown field reject、request ID付きError envelopeを実装した。
- Dataset Version、Execution Batch、Graph Version、Result exportにDB-backed idempotencyを実装した。PostgreSQL advisory lockで複数API process間の同時再送も直列化する。
- RouterはApplication/Query Serviceだけを利用し、private UoWを直接呼ばない。
- CLIは`ariadne-discover --config`と`ariadne-estimate --config`に統一し、DB/API Execution IDを生成しない。Manifest 1.0へ入力hash、analysis spec、code/runtime version、scientific status、summary、Artifact hashを保存する。
- CLI exit codeは0=成功/科学的負結果、2=config/input validation、3=input Artifact、4=technical core、5=output writeとした。

### 3.6 Web App

- Project / Data、Discovery、Inference、Results / Lineageの4 Workspaceへ全面置換した。
- Project選択/更新、Dataset登録/一覧/schema/hash/preview、PC/GES parameter grid、3 Graph以上の比較、Graph editor/FIXED、複数Estimator、ATE/ATT、adjustment set、assumptions、diagnostics、Annotation、Lineage、Artifact download/exportを提供する。
- Frontendの通信先は`/api/v1`だけであり、Legacy APIを参照しない。

### 3.7 Cutover / Legacy retirement

- DockerはPython 3.12 Product runtime、Product Alembic、API、Workerだけを含む。
- ComposeはPostgreSQL、migrate、API、Worker、Frontendだけを起動する。
- `ARIADNE_PRODUCT_DATABASE_URL`を必須とし、production SQLite/Legacy DB fallbackを削除した。
- Legacy package、旧tracking/storage/persistence/auth等の未使用Control Plane moduleをwheelとDocker build contextから除外した。Scientific Adapterが選択利用する`ariadne.causal`、preprocessing、configだけを残した。
- Runtime依存からMLflow、EconML、Dask、Azure SDK、AWS SDK、RData、JWTを削除した。Compose image内のinstall数は初回旧構成の138から新構成の59へ減少した。
- runtime image内で`ariadne.legacy`が解決不能であることを確認した。履歴参照用sourceは`src/ariadne/legacy/`に凍結しているが、wheel/image/起動構成には含まれない。

## 4. Test・運用検証結果

### 4.1 Frozen dependency / collect / 全Test

```text
$ UV_CACHE_DIR=/tmp/ariadne-uv-cache UV_PROJECT_ENVIRONMENT=/tmp/ariadne-py312-clean \
    uv sync --frozen --python 3.12 --offline
exit 0（旧runtime依存45 packageを環境から削除）

$ PYTHONDONTWRITEBYTECODE=1 /tmp/ariadne-py312-clean/bin/pytest -q --collect-only
36 tests collected / 0 error

$ ARIADNE_PRODUCT_TEST_DATABASE_URL=postgresql+psycopg://... \
    PYTHONDONTWRITEBYTECODE=1 /tmp/ariadne-py312-clean/bin/pytest -q
36 passed in 9.19s
```

TestにはScientific regression、Domain、Snapshot、Graph、API/Worker component、CLI、Architecture、PostgreSQLが含まれる。C2が空のためCompatibility Contract Testは対象外である。

### 4.2 PostgreSQL Integration

```text
$ pytest -q tests/product/test_postgres_contract.py
3 passed in 1.43s
```

確認内容:

- Product baselineと独立version table
- Legacy table不在
- FK / CHECK / UNIQUE
- transaction rollback
- 2 thread / 2 DB sessionによるatomic claim（同一Executionの取得は1 Workerだけ）

### 4.3 Compose / E2E

Cutover開始時に`docker compose down -v`を実行し、旧`metadata-data` / `artifact-data` volumeを削除した。これは空の新Product DBから構築する指示に基づく。外部backupがない限り、削除前volumeの内容は復元できない。

```text
$ docker compose up --build -d migrate api worker frontend
exit 0

$ docker compose ps
database healthy / api healthy / worker up / frontend up

$ curl http://localhost:8000/health/ready
{"status":"ok"}

$ python tests/product/compose_golden_path_smoke.py
discovery_results=3 / estimation_results=3 / status=PASS
```

Golden PathはDataset idempotent登録、preview、PC 2条件+GES、3 Result比較、FIXED Graph、OLS/IPW/AIPW、3 Result比較、Annotation、Lineage、Artifact download、Manifest exportを実Scientific Coreで実行する。最終imageでのroot Resultは`f710da13-43aa-4089-9f82-92a040ec0ac7`だった。

### 4.4 Backup / restore / rollback

```text
$ pg_dump -Fc ariadne
exit 0
$ pg_restore -d ariadne_restore /tmp/ariadne_product.dump
exit 0
```

復元直後にrevision `20260805_product_0001`、Project 2、Result 12、Artifact 26を確認した。復元DBを`ariadne`へ切替後、同じGolden PathがDiscovery 3件、Estimation 3件、`status=PASS`で完走した。

隔離`ariadne_rollback` DBで`upgrade head → downgrade base → upgrade head`を実行した。downgrade後の`product_%` table数は0、再upgradeはexit 0だった。検証用DBは確認後に削除した。

### 4.5 Architecture / runtime

- AST TestでProduct→Legacy/Legacy ORM、Scientific→Repository/Web schema/ORMを禁止した。
- Compose、entrypoint、wheel除外設定を静的Testした。
- Product API containerで`find_spec('ariadne.legacy') is None`を確認した。
- `uv build --offline`でsdist/wheel作成に成功した。

## 5. 設計との差分と判断

### 5.1 意図的な最小変更

- Web AppのProject選択に必要な`GET /api/v1/projects`を追加し、`23_API・インターフェース設計.md`へ反映した。代替案は固定Project IDの外部注入だが、4 Workspaceの自立性を損なうため採用しなかった。
- `product_idempotency`は技術用tableであり、第8業務Entityではない。
- C2の実在根拠がないためCompatibility Adapterを空実装せず、全旧契約をC0とした。
- 旧Control Plane sourceは履歴確認のため物理削除せず凍結した。ただしpackage/image/startup/DB接続から除外し、runtime dependencyにはしない。

## 6. 残課題

なし。MVP外機能（詳細RBAC、承認workflow、CATE/HTE、連続Treatment、IV/DiD/RDD等）は要件どおり未実装であり、残課題には数えない。
