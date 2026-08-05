# Ariadne：Execution管理とMLflow実験追跡の責務分離

> **文書種別: 補足設計文書**
>
> 本文書は正本要件定義書（`docs/wiki/requirement_definition/01_web_service_requirements_v1.4.md`）を補足する設計文書です。
> 要件定義書との優先順位は **要件定義書 > 本文書** とします。
> 要件定義書との競合がある場合は要件定義書が正本です。
>
> **実装状況**: 本文書に記載された実装指針の一部は未実装です。
> 特に以下の項目は将来実装として扱います。
> - MLflow Tracking Port / MLflow Adapter / NullTracker（第8節）
> - WorkerによるMLflow Run ensureおよびDB列追加（第5節、第9節）
> - CLI BootstrapへのMLflow連携（第7節）
>
> 2026-08-04時点で完了した事項: Execution語彙への改称（第3節）、CLIのUUID fallback削除、
> `--execution-id`の削除と`--run-label`の導入、`ExecutionIdentity`型の追加
> （`docs/wiki/requirement_definition/traceability_matrix.md`参照）。

## 0. 目的

Ariadneの既存実装を修正し、以下の責務分離を実現してください。

1. 科学実験の追跡・比較はMLflowで管理する。
2. Ariadneは、Webアプリケーション固有の実行オーケストレーションを管理する。
3. Ariadne内の既存`Run`概念を`Execution`概念へ改称する。
4. CLIおよび実験用エントリーポイントでは、AriadneのExecutionを作成せず、MLflow Runのみを使用する。
5. Web/API経由の実行では、Ariadne ExecutionとMLflow Runの両方を作成し、相互に関連付ける。
6. AriadneのAPI、Worker、CLIには`mlflow-skinny`を使用する。
7. MLflow Tracking Server、UI、SQL Backend Storeが必要な場合は、完全版`mlflow`を使用する別コンテナとして構成する。

本作業では、既存コード、テスト、マイグレーション、ドキュメントを先に調査し、実装上の影響範囲を確定してから変更してください。

---

## 1. 用語と責務

### 1.1 Ariadne Execution

Ariadneの`Execution`は、Webアプリケーションにおける実行要求・ジョブ・オーケストレーションを表します。

Ariadneに残す責務は以下です。

* Projectとの関連
* User、Role、認可
* 実行要求の受付
* 冪等性キーとrequest hash
* ExecutionPlan
* Queue、Transactional Outbox
* Workerの割当て
* Lease、Heartbeat
* キャンセル要求
* リトライ
* StageExecution
* StageAttempt
* DatasetVersion、ConfigurationVersion等との関連
* Audit Log
* 実行状態
* MLflow Run IDとの対応

### 1.2 MLflow Run

MLflow Runは、科学的・分析的な実行記録を表します。

MLflowに記録する情報は以下です。

* アルゴリズム名
* 推定器名
* ハイパーパラメータ
* random seed
* 分析モード
* データセットIDおよびcontent hash
* 設定IDおよびcontent hash
* Git commit
* パッケージバージョン
* 依存関係またはlock file hash
* 実行環境
* 科学的メトリクス
* 推定値
* 診断結果
* Manifest
* グラフ
* レポート
* エラー情報
* 実行時間

MLflowをQueue、RBAC、冪等性、Worker Lease、Heartbeatの正本として使用しないでください。

---

## 2. ID設計

### 2.1 Web/API実行

Web/API経由の実行では、以下の2種類のIDを保持してください。

```text
execution_id:
    Ariadneが採番する実行管理ID

mlflow_run_id:
    MLflowが採番する科学実験追跡ID
```

Ariadne APIの正式なリソース識別子は`execution_id`とします。

```text
GET  /executions/{execution_id}
POST /executions/{execution_id}/cancel
POST /executions/{execution_id}/retry
GET  /executions/{execution_id}/events
GET  /executions/{execution_id}/artifacts
```

### 2.2 CLI実行

CLIおよび以下の実験用エントリーポイントでは、Ariadne Executionを作成しないでください。

```text
experiments/004_discovery_inference_integration/run.py
```

CLI実行の主IDはMLflowが採番する`mlflow_run_id`とします。

```text
CLI:
    execution_id = None
    mlflow_run_id = MLflowが採番
```

### 2.3 IDの曖昧な表現を禁止

共通モデル、Manifest、ExecutionPlan、ログに、名前空間不明の`run_id`を新規追加しないでください。

必要な場合は以下を明示してください。

```python
execution_id: str | None
mlflow_run_id: str | None
```

共通の識別コンテキストが必要なら、以下と同等の型を導入してください。

```python
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class ExecutionIdentity:
    origin: Literal["CLI", "WEB"]
    execution_id: str | None
    mlflow_run_id: str | None
    primary_namespace: Literal["MLFLOW", "ARIADNE"]
    primary_id: str
```

CLI実行では次の状態にしてください。

```python
ExecutionIdentity(
    origin="CLI",
    execution_id=None,
    mlflow_run_id=mlflow_run_id,
    primary_namespace="MLFLOW",
    primary_id=mlflow_run_id,
)
```

Web実行では次の状態にしてください。

```python
ExecutionIdentity(
    origin="WEB",
    execution_id=execution.id,
    mlflow_run_id=mlflow_run_id,
    primary_namespace="ARIADNE",
    primary_id=execution.id,
)
```

---

## 3. ドメイン用語の改称

以下を原則として一貫して改称してください。

| 旧名称                    | 新名称                                |
| ---------------------- | ---------------------------------- |
| `Run`                  | `Execution`                        |
| `RunService`           | `ExecutionService`                 |
| `run_id`               | `execution_id`                     |
| `StageRun`             | `StageExecution`                   |
| `stage_run_id`         | `stage_execution_id`               |
| `RunEvent`             | `ExecutionEvent`                   |
| `ValidationRun`        | 文脈を確認し、実行管理なら`ValidationExecution` |
| `RUN_CREATED`          | `EXECUTION_CREATED`                |
| `RUN_RETRY_QUEUED`     | `EXECUTION_RETRY_QUEUED`           |
| `EXECUTE_RUN`          | `EXECUTE_EXECUTION`                |
| `aggregate_type="RUN"` | `aggregate_type="EXECUTION"`       |
| `resource_type="RUN"`  | `resource_type="EXECUTION"`        |
| `/runs`                | `/executions`                      |

ただし、以下はMLflowの正式用語であるため変更しないでください。

```text
MLflow Run
mlflow_run_id
MlflowClient
start_run
create_run
```

### 3.1 パッケージ名について

本指示書ではサービス名をAriadneと呼称します。

既存のPython package/import namespaceである`causal_atelier`、リポジトリ名、公開パッケージ名は、別途明示された要件がない限り変更しないでください。

ユーザー向け表示、APIタイトル、ドキュメント等に旧サービス名が存在する場合は、Ariadneへ変更してください。ただし、永続識別子、import path、既存データとの互換性を壊す一括置換は禁止します。

---

## 4. DBマイグレーション

Alembic等、既存プロジェクトで採用されているマイグレーション方式に従ってください。

最低限、以下を移行してください。

```text
run                       → execution
stage_run                 → stage_execution
run_event                 → execution_event

run_id                    → execution_id
stage_run_id              → stage_execution_id
retry_of_run_id           → retry_of_execution_id
selected_attempt_id       → 必要に応じて名称を確認
```

関連する以下も漏れなく更新してください。

* Foreign Key
* Index
* Unique Constraint
* ORM relationship
* Repository query
* Outbox payload
* Audit resource type
* API schema
* JSON serializer
* テストfixture
* Seed data
* 開発用サンプルデータ
* ドキュメント

単純なdrop-and-createは行わず、既存データを保持するrename migrationを優先してください。

### 4.1 MLflow関連カラム

`Execution`に以下と同等の情報を追加してください。

```python
mlflow_experiment_id: str | None
mlflow_run_id: str | None
mlflow_tracking_status: str
mlflow_tracking_error: str | None
```

状態例は以下です。

```text
NOT_REQUIRED
PENDING
ACTIVE
FINISHED
ERROR
```

`mlflow_run_id`には一意制約を付与してください。ただしNULLを複数許容できるDB仕様を確認してください。

当面MLflow以外のTracking Providerを実装しないため、不要な汎用`ExternalRunBinding`抽象化は導入しないでください。

---

## 5. Web実行フロー

Web/API実行は以下の順序にしてください。

```text
1. POST /executionsを受信
2. 冪等性を検査
3. Ariadne Executionを作成
4. execution_idを採番
5. ExecutionPlanを固定
6. StageExecutionを作成
7. OutboxへEXECUTE_EXECUTIONを登録
8. APIレスポンスとしてexecution_idを返却
9. WorkerがExecutionを取得
10. WorkerがMLflow Runをensureする
11. mlflow_run_idをExecutionへ保存
12. パイプラインを実行
13. params、metrics、tags、artifactsをMLflowへ記録
14. MLflow RunをFINISHED、FAILED、KILLEDのいずれかで終了
15. Ariadne Executionの状態を確定
```

API受付時点では、原則としてMLflow Runを作成しないでください。

MLflow RunはWorkerが実際の実行を開始する時点で作成してください。

理由は以下です。

* Queue待機だけのExecutionをMLflow上の実行として扱わないため
* MLflow障害でExecution受付自体が失敗することを避けるため
* MLflow上の開始時刻を実際の計算開始時刻に近づけるため

---

## 6. CLI実行フロー

現在のCLIでPlannerまたはRunnerが独自のUUIDを生成している箇所を削除してください。

以下のような独自採番を残さないでください。

```python
args.run_id or config_run_id or uuid.uuid4().hex[:12]
```

CLI Bootstrapで先にMLflow Runを開始し、そのIDをApplication層へ注入してください。

概念例：

```python
with tracker.start_run(
    experiment_name=experiment_name,
    run_name=run_name,
    tags=tags,
) as tracking_run:
    identity = ExecutionIdentity(
        origin="CLI",
        execution_id=None,
        mlflow_run_id=tracking_run.run_id,
        primary_namespace="MLFLOW",
        primary_id=tracking_run.run_id,
    )

    result = execute(
        args,
        project_root,
        identity=identity,
    )
```

### 6.1 CLIオプション

曖昧な`--run-id`は廃止してください。

以下と同等のオプションを設けてください。

```text
--mlflow-tracking-uri
--mlflow-experiment
--mlflow-run-name
--resume-mlflow-run-id
--disable-mlflow
```

`--resume-mlflow-run-id`は、既存MLflow Runを明示的に再開する用途だけに使用してください。

人間が指定する名称は`run_name`、一意識別子はMLflowが採番する`run_id`としてください。

### 6.2 Tracking無効化

科学実験として実行する通常CLIでは、MLflowをデフォルトで有効にしてください。

ただし、単体テストや限定的なデバッグのため、明示的な`--disable-mlflow`またはNull Trackerを提供して構いません。

Trackingを無効化した場合もPlanner内で擬似MLflow IDを生成しないでください。

---

## 7. VALIDATE_ONLYおよびDRY_RUN

Webの以下の実行モードでは、原則としてMLflow Runを作成しないでください。

```text
VALIDATE_ONLY
DRY_RUN
```

これらはAriadne Executionとして記録してください。

```text
execution_id:
    作成する

mlflow_run_id:
    None

mlflow_tracking_status:
    NOT_REQUIRED
```

将来、検証結果自体をMLflowで比較する明示的要件が追加された場合のみ、設定可能なオプションとして対応してください。

---

## 8. MLflow Adapter

MLflow固有処理をCLI、Worker、Stage実装へ分散させないでください。

Application PortとInfrastructure Adapterを導入してください。

推奨配置例：

```text
src/causal_atelier/
├── application/
│   └── ports/
│       └── experiment_tracker.py
└── infrastructure/
    └── tracking/
        ├── mlflow_tracker.py
        └── null_tracker.py
```

Portは以下と同等の操作を提供してください。

```python
class ExperimentTracker(Protocol):
    def start_run(...) -> TrackingRunContext:
        ...

    def log_params(...) -> None:
        ...

    def log_metrics(...) -> None:
        ...

    def set_tags(...) -> None:
        ...

    def log_artifact(...) -> None:
        ...

    def finish_run(...) -> None:
        ...

    def find_run_by_execution_id(...) -> TrackingRunReference | None:
        ...
```

サーバーWorkerでは、暗黙のactive run状態への依存を最小化し、明示的な`mlflow_run_id`を扱う`MlflowClient`中心の実装にしてください。

CLIではcontext managerを使用して構いませんが、共通のタグ・パラメータ・成果物命名規則は同じAdapterまたは共通サービスに集約してください。

---

## 9. MLflow Runの冪等生成

Workerは再実行される可能性があるため、MLflow Runを毎回無条件に作成しないでください。

以下のensure処理を実装してください。

```text
1. Execution.mlflow_run_idが存在する
   → 既存Runを使用

2. DBにmlflow_run_idがない
   → MLflowからタグariadne.execution_idで検索

3. 一致するRunがある
   → Executionへmlflow_run_idを再保存

4. 存在しない
   → 新しいMLflow Runを作成

5. 作成したMLflow Runへ以下のタグを設定
   → ariadne.execution_id
   → ariadne.project_id
   → ariadne.execution_origin
```

最低限、以下のタグを使用してください。

### Web

```text
ariadne.execution_origin = WEB
ariadne.execution_id
ariadne.project_id
ariadne.pipeline_definition_version_id
ariadne.execution_mode
ariadne.code_commit
```

### CLI

```text
ariadne.execution_origin = CLI
ariadne.pipeline
ariadne.code_commit
```

---

## 10. MLflow Runの粒度

初期実装では、以下としてください。

```text
1 Ariadne Execution
=
1 MLflow Run
```

Stageごとのメトリクスや成果物は、名前空間またはartifact pathで分離してください。

例：

```text
metrics:
    discovery.edge_count
    discovery.runtime_seconds
    inference.ate
    inference.standard_error

artifacts:
    discovery/graph.json
    discovery/manifest.json
    inference/estimate.json
    inference/report.html
```

StageAttempt単位のMLflow child runは、現在の要件では必須としません。

ただし、将来nested runを導入できるよう、Tracking AdapterにStage固有処理を密結合させないでください。

---

## 11. MLflow依存関係

### 11.1 Ariadne API、Worker、CLI

完全版`mlflow`ではなく、原則として以下を使用してください。

```text
mlflow-skinny
```

既存の依存管理方式に従い、バージョンを明示的に固定してください。

### 11.2 MLflow Server

MLflow Tracking Server、UI、SQL Backend Storeを使用する環境では、Ariadneとは別コンテナを使用してください。

MLflow Serverコンテナでは完全版`mlflow`を使用してください。

Docker Composeを使用する場合は、MLflow Serverをoptional profileとして起動できる構成を推奨します。

概念例：

```yaml
services:
  mlflow-server:
    profiles: ["mlflow"]
    image: ghcr.io/mlflow/mlflow:<PINNED_VERSION>
    command:
      - mlflow
      - server
      - --host
      - "0.0.0.0"
      - --port
      - "5000"
```

実際のBackend Store、Artifact Store、認証設定は、既存インフラ構成を調査したうえで決定してください。

### 11.3 バージョン整合性

以下のバージョンは可能な限り完全一致させてください。

```text
Ariadneのmlflow-skinny
MLflow Serverコンテナのmlflow
```

少なくとも同一メジャー・マイナーバージョンに固定してください。

`latest`タグは使用しないでください。

---

## 12. 設定

以下と同等の環境変数を追加してください。

```text
MLFLOW_TRACKING_URI
MLFLOW_EXPERIMENT_NAME
MLFLOW_ENABLED
MLFLOW_TIMEOUT_SECONDS
MLFLOW_TAG_PREFIX
```

WebとCLIで設定解決方法を統一してください。

優先順位を明示してください。

例：

```text
CLI引数
>
環境変数
>
設定ファイル
>
デフォルト値
```

秘密情報をDB、Manifest、ログ、MLflow tagsへ出力しないでください。

---

## 13. API互換性

既存の`/runs` APIに利用者が存在する可能性を考慮してください。

互換性が必要な場合は、移行期間中のみ以下を提供してください。

```text
/runs
    deprecated alias of /executions

run_id
    deprecated alias of execution_id
```

OpenAPIにはdeprecatedであることを明記してください。

新しい内部コードでは、旧`run_id`名称を使用しないでください。

旧形式の読み込み互換を残す場合でも、新規書込みは新形式だけにしてください。

---

## 14. テスト要件

最低限、以下をテストしてください。

### 14.1 ドメイン・DB

* Executionの作成
* execution_idの採番
* 既存RunデータからExecutionへのマイグレーション
* Foreign Keyの保持
* idempotency keyの保持
* retry関係の保持
* StageExecutionおよびStageAttemptの保持
* mlflow_run_idの一意制約
* NULLのmlflow_run_idを複数保存可能

### 14.2 Web/API

* `POST /executions`
* `GET /executions/{execution_id}`
* cancel
* retry
* events
* artifacts
* Project権限
* idempotency
* deprecated `/runs`互換経路
* VALIDATE_ONLYでMLflow Runが作成されない
* DRY_RUNでMLflow Runが作成されない

### 14.3 Worker

* Execution開始時にMLflow Runが作成される
* `ariadne.execution_id`タグが付く
* 作成したmlflow_run_idがDBへ保存される
* Worker再実行時にMLflow Runが重複作成されない
* MLflow作成成功後、DB保存前に失敗した場合にタグ検索で回収できる
* 成功時にFINISHED
* 失敗時にFAILED
* キャンセル時にKILLED
* MLflow障害時にtracking statusとerrorが記録される

### 14.4 CLI

* CLI実行時にAriadne Executionが作成されない
* MLflowがrun_idを採番する
* MLflow IDがPlannerへ注入される
* PlannerがUUIDを生成しない
* `--resume-mlflow-run-id`が既存Runを再開する
* `--disable-mlflow`でNull Trackerが使用される
* 旧`--run-id`が削除またはdeprecatedになる
* `experiments/004_discovery_inference_integration/run.py`から同じ処理が使用される

### 14.5 Tracking Adapter

* MLflow SDKをmockした単体テスト
* paramsの型変換
* metricsの数値検証
* tagsの文字列化
* artifact path
* timeout
* retry
* secret redaction

---

## 15. ドキュメント

以下を更新してください。

* README
* Webサービス設計書
* CLI利用方法
* API仕様
* Docker Compose利用方法
* MLflow Serverの起動方法
* ローカルMLflow Trackingの設定
* 中央Tracking Serverへの接続方法
* ID体系
* ExecutionとMLflow Runの責務分担
* マイグレーション手順
* deprecated APIの廃止予定

ドキュメントではサービス名称をAriadneとしてください。

---

## 16. 完了条件

以下をすべて満たした場合に完了とします。

1. Ariadneの実行管理IDが`execution_id`へ改称されている。
2. Runドメイン用語がExecutionへ一貫して変更されている。
3. 既存DBデータを保持するマイグレーションが存在する。
4. CLI実行時にAriadne Executionが作成されない。
5. CLIの科学実験IDとしてMLflow run IDが使用される。
6. Web実行時にはexecution_idとmlflow_run_idの双方が保持される。
7. WebのMLflow RunはWorker実行開始時に作成される。
8. PlannerおよびRunnerが独自のRun IDを採番しない。
9. API、Worker、CLIで`mlflow-skinny`が使用される。
10. MLflow Serverは別コンテナとして任意起動できる。
11. MLflow ClientとServerのバージョンが固定・整合している。
12. VALIDATE_ONLYとDRY_RUNでは原則MLflow Runを作成しない。
13. MLflow Runの重複作成防止が実装されている。
14. 既存テストおよび追加テストが成功する。
15. 型チェック、lint、format、migration validationが成功する。

---

## 17. 実施手順

以下の順序で作業してください。

1. 現行コードとDBモデルの影響範囲を調査する。
2. 変更対象ファイル一覧と移行計画を提示する。
3. ドメイン用語とDBスキーマを変更する。
4. API、Repository、Service、Outbox、Auditを変更する。
5. MLflow Tracking Port／Adapterを追加する。
6. Web WorkerへMLflow連携を追加する。
7. CLI BootstrapへMLflow連携を追加する。
8. Planner内の独自ID採番を削除する。
9. `mlflow-skinny`依存を追加する。
10. optionalなMLflow Serverコンテナを追加する。
11. テストを追加・修正する。
12. ドキュメントを更新する。
13. 全テストと静的検査を実行する。
14. 変更内容、未解決事項、後方互換性上の注意点を報告する。

不明点があっても作業を停止せず、既存アーキテクチャとテストから最も整合的な判断を行い、その判断と前提を最終報告に明記してください。
