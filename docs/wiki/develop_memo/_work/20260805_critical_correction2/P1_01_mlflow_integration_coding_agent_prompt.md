# Coding Agent Prompt: P1 MLflow連携の実装

## 0. ミッション

Ariadneに、要件で定義されたMLflow連携を実装してください。

対象は単なる`mlflow.start_run()`の追加ではありません。以下を一貫した設計として完成させてください。

- `execution`のMLflow関連列
- DB制約とAlembic migration
- Application Port
- MLflow AdapterおよびNull Adapter
- Web/API、Worker、CLIの責務分離
- WorkerでのMLflow Run冪等生成
- Ariadne ExecutionとMLflow Runの相互関連付け
- params、metrics、tags、artifacts、終了状態の記録
- MLflow障害状態の永続化
- retry、cancel、Worker再実行時の整合性
- secret redaction
- unit、integration、PostgreSQL、Worker、CLI、障害系テスト
- 文書および要件トレーサビリティ

既存実装、テスト、migration、要件を先に調査し、実装済みの機能を重複作成しないでください。

---

## 1. 規範方針

本作業では、以下を正本方針とします。

### 1.1 Ariadne Executionの責務

Ariadne Executionは、Web/API経由の実行要求とオーケストレーションを管理します。

- Project、User、Role、認可
- 実行要求受付
- 冪等性keyとrequest hash
- Execution Plan
- QueueとTransactional Outbox
- Worker割当て
- Lease、Heartbeat
- Cancel、Retry
- Stage Execution、Stage Attempt
- Dataset Version、Configuration Version等との関連
- Audit Log
- 実行状態
- MLflow Run IDとの対応

### 1.2 MLflow Runの責務

MLflow Runは、科学的・分析的な実行追跡を管理します。

- algorithm名
- estimator名
- hyperparameter
- random seed
- analysis mode
- Dataset IDおよびcontent hash
- Configuration IDおよびcontent hash
- Git commit
- package version
- dependency lock hash
- execution environment
- scientific metrics
- estimate
- diagnostic
- Manifest
- graph
- report
- error情報
- runtime

MLflowをQueue、RBAC、冪等性、Worker lease、Heartbeatの正本にしてはなりません。

### 1.3 Web/API実行

- Web/APIはAriadne Executionを作成する
- 正式なAriadne IDは`execution_id`
- API受付時点では原則としてMLflow Runを作成しない
- Workerが実処理を開始する時点でMLflow Runをensureする
- 1 Ariadne Execution = 1 MLflow Runを初期実装の原則とする
- `DRY_RUN`と`VALIDATE_ONLY`ではMLflow Runを作成しない
- MLflow障害でExecution受付自体を失敗させない

### 1.4 CLIおよび実験entry point

- CLIはAriadne Executionを作成しない
- CLIの科学実験IDはMLflowが採番する`mlflow_run_id`
- CLIはMLflow Runを開始してからApplication層へidentityを注入する
- Planner／Runnerは独自のRun IDや擬似MLflow IDを生成しない
- `--disable-mlflow`時はNull Trackerを用い、IDを捏造しない

要件正本がrepository内で別方針に改訂済みの場合は、実装前に差異を報告し、最新の規範文書を優先してください。矛盾を推測で埋めないでください。

---

## 2. 作業前に必ず調査する対象

配置が異なる場合はrepository内検索で実体を特定してください。

### 2.1 要件・設計

- `docs/wiki/requirement_definition/01_web_service_requirements_v1.3.md`
- 後継版がある場合は最新版
- 最新のデータモデル定義書
- `Execution管理とMLflow実験追跡の責務分離.md`
- API仕様
- CLI仕様
- Worker／Outbox仕様
- reproducibility文書
- compose／deployment文書

### 2.2 実装

- `pyproject.toml`
- `compose.yaml`
- `.env.example`
- `src/ariadne/domain/metadata.py`
- `src/ariadne/application/run_execution/`
- `src/ariadne/application/ports/`
- `src/ariadne/infrastructure/tracking/`
- `src/ariadne/interfaces/api/`
- `src/ariadne/interfaces/cli/`
- `src/ariadne/workers/`
- `src/ariadne/pipeline/`
- Manifest、Artifact、Result projection関連実装
- Alembic全revision
- `experiments/004_discovery_inference_integration/run.py`

### 2.3 テスト

- MLflow関連test
- Worker test
- Execution test
- CLI test
- migration test
- Artifact／Manifest test
- retry／cancel test
- secret redaction test
- PostgreSQL integration test

### 2.4 最初に提出する調査結果

コード変更前に次を整理してください。

1. 現在の`Execution`列
2. MLflow依存packageとversion
3. 既存Tracker Port／Adapterの有無
4. CLI、Worker、Stage実装内のMLflow SDK直接呼出し
5. 現在のCLI ID生成箇所
6. Worker開始、成功、失敗、cancelの状態遷移
7. retry時のExecution／Attempt semantics
8. Artifact／Manifest生成箇所
9. loggingとsecret redactionの実装
10. migration revision graph
11. 要件と実装のGap

---

## 3. DomainおよびDB model

### 3.1 `execution`へ追加する列

現行modelに存在しない場合、`Execution`へ次を追加してください。

| 列 | 型 | NULL | 既定値 | 役割 |
|---|---|---:|---|---|
| `mlflow_experiment_id` | `varchar(255)` | Yes | null | MLflow Experiment ID |
| `mlflow_run_id` | `varchar(255)` | Yes | null | MLflow Run ID |
| `mlflow_tracking_status` | `varchar(32)` | No | `PENDING`またはmode依存 | Tracking状態 |
| `mlflow_tracking_error` | `text` | Yes | null | redacted済み障害概要 |

必要なら次も追加してよいですが、汎用化を目的に不要な抽象化を導入しないでください。

- `mlflow_started_at`
- `mlflow_finished_at`

追加する場合は、要件上の必要性、使用箇所、状態との整合性を明示してください。

### 3.2 Tracking状態

最低限、以下を扱ってください。

- `NOT_REQUIRED`
- `PENDING`
- `ACTIVE`
- `FINISHED`
- `ERROR`

推奨意味:

| 状態 | 意味 |
|---|---|
| `NOT_REQUIRED` | `DRY_RUN`、`VALIDATE_ONLY`、または明示的にtracking不要 |
| `PENDING` | Web Execution受付済み、MLflow Run未作成 |
| `ACTIVE` | MLflow Runを作成または回収し、実行中 |
| `FINISHED` | MLflow Runがterminal状態へ終了し、対応付け完了 |
| `ERROR` | MLflow操作に失敗し、障害情報を記録 |

状態遷移はApplication Serviceで一元管理し、各Stageが任意文字列を直接設定しないようにしてください。

### 3.3 一意制約

`mlflow_run_id`には、非NULL値に対する一意性を付与してください。

PostgreSQLおよびSQLite test環境で、複数NULLを許容しつつ、同じ非NULL Run IDを複数Executionへ関連付けられないことを検証してください。

既存DBに重複値が存在し得る場合は、constraint追加前に検査し、推測で片方を削除しないでください。重複が見つかった場合のmigration方針を明示してください。

### 3.4 DB制約

可能な範囲でDB制約を追加してください。

- `mlflow_tracking_status`のCHECK
- `mlflow_run_id`のunique
- `ACTIVE`または`FINISHED`で`mlflow_run_id`を要求する整合性
- `NOT_REQUIRED`では原則として`mlflow_run_id IS NULL`

ただし、障害復旧の中間状態を不可能にする過剰なCHECKは避けてください。DB制約とApplication invariantの分担を文書化してください。

### 3.5 Migration

- Alembic revisionを追加する
- 既存データを保持する
- 既存Executionのtracking statusを安全にbackfillする
- `DRY_RUN`／`VALIDATE_ONLY`は`NOT_REQUIRED`
- tracking対象の過去Executionについて、事実が分からなければRun IDを捏造しない
- 不明な過去状態は、要件で許容される安全な状態へ明示的に分類する
- migration内で現在のORM metadataを参照しない
- upgrade／downgradeを明示的Alembic operationで記述する
- fresh DBとupgraded DBのschema同一性testを追加する

---

## 4. Tracking Port

### 4.1 Application Port

MLflow SDKをApplication、Worker、CLI、Stage処理へ直接分散させないでください。

`application/ports/experiment_tracker.py`またはrepository規約に沿う場所へ、MLflow非依存のPortを定義してください。

最低限、次と同等の能力を持たせてください。

```python
class ExperimentTracker(Protocol):
    def create_or_resume_run(...): ...
    def find_run_by_execution_id(...): ...
    def log_params(...): ...
    def log_metrics(...): ...
    def set_tags(...): ...
    def log_artifact(...): ...
    def terminate_run(...): ...
```

命名は既存規約に適合させてよいですが、次を満たしてください。

- Application層がMLflow SDK型へ依存しない
- server Workerで暗黙のactive runへ依存しない
- `mlflow_run_id`を明示的に渡す
- operationがretry可能か、冪等かをinterfaceまたは文書で明示する
- params、metrics、tagsの型変換をAdapterへ集約する
- secret redactionを共通化する

### 4.2 戻り値

Run参照は最低限以下を含む明示型としてください。

```python
@dataclass(frozen=True)
class TrackingRunReference:
    experiment_id: str
    run_id: str
    lifecycle_status: str | None = None
```

MLflow SDK objectをDomain／Applicationへ漏らさないでください。

### 4.3 例外

Tracker固有例外をApplicationが扱える分類へ変換してください。

例:

- connection／timeout
- authentication／authorization
- invalid request
- not found
- conflict／duplicate
- artifact upload failure
- terminal transition failure

生の接続文字列、token、credentialを例外messageへ含めないでください。

---

## 5. MLflow Adapter

### 5.1 実装方針

`infrastructure/tracking/mlflow_tracker.py`または既存規約に従う場所へ実装してください。

- `mlflow-skinny`を使用する
- server Workerでは`MlflowClient`中心に実装する
- active run global stateへの依存を避ける
- explicit `run_id`でlog／terminateする
- timeoutを設定可能にする
- tracking URIを設定可能にする
- retry対象と非retry対象を区別する
- retryはboundedにし、無限retryしない
- duplicate作成をretryで増幅しない

### 5.2 Null Adapter

`null_tracker.py`を実装してください。

- MLflow SDKを呼ばない
- 擬似Run IDを生成しない
- CLIの`--disable-mlflow`で使用可能
- Webの`DRY_RUN`／`VALIDATE_ONLY`でtracking不要処理に使用可能
- 呼出し側がtracking無効を明確に認識できる

### 5.3 設定

最低限、次と同等の設定を一元解決してください。

- `MLFLOW_TRACKING_URI`
- `MLFLOW_EXPERIMENT_NAME`
- `MLFLOW_ENABLED`
- `MLFLOW_TIMEOUT_SECONDS`
- `MLFLOW_TAG_PREFIX`

優先順位を統一してください。

```text
CLI引数 > 環境変数 > 設定ファイル > default
```

設定値、tracking URI、credentialをManifest、tag、logへ無条件に出力しないでください。

### 5.4 依存version

- API、Worker、CLIは`mlflow-skinny`を使用する
- versionを再現可能な形で固定する
- optional MLflow Server containerを追加する場合、完全版`mlflow`を別containerで使用する
- clientとserverは少なくとも同一major／minorへ整合させる
- `latest` tagを使用しない

MLflow Server containerの追加は、repositoryのscopeと要件を確認した上で行ってください。不要なら文書だけで起動方法を示し、無関係なdeployment拡張をしないでください。

---

## 6. Web／Worker連携

### 6.1 API受付

`POST /executions`では次を守ってください。

1. 冪等性検査
2. Ariadne Execution作成
3. `execution_id`採番
4. Execution Plan固定
5. Stage Execution作成
6. Outboxへ`EXECUTE_EXECUTION`
7. responseとして`execution_id`を返す

この時点では原則としてMLflow Runを作成しないでください。

初期tracking status:

- `RUN`: `PENDING`
- `DRY_RUN`: `NOT_REQUIRED`
- `VALIDATE_ONLY`: `NOT_REQUIRED`

### 6.2 Worker開始時のMLflow Run ensure

Workerは、実処理開始直前に次の順序でMLflow Runをensureしてください。

1. `Execution.mlflow_run_id`が存在する
   - 既存Runを使用する
2. DBにRun IDがない
   - MLflowからtag `ariadne.execution_id`で検索する
3. 一致するRunが1件ある
   - そのRun IDをExecutionへ保存する
4. 一致するRunがない
   - 新しいMLflow Runを作成する
5. 複数一致する
   - 自動選択せず、tracking errorとして扱い、診断可能な情報を記録する

新規Runには最低限次のtagを設定してください。

```text
ariadne.execution_origin = WEB
ariadne.execution_id
ariadne.project_id
ariadne.pipeline_definition_version_id
ariadne.execution_mode
ariadne.code_commit
```

値がnullの場合の送信規則を一貫させてください。文字列`"None"`を安易に記録しないでください。

### 6.3 作成成功後、DB保存前に障害が起きるケース

この障害窓を必ず扱ってください。

- MLflow Run作成成功
- DBへの`mlflow_run_id`保存前にprocess crash
- Worker再実行
- `ariadne.execution_id` tag検索で既存Runを回収
- 新しいRunを重複作成しない

この経路を自動testで検証してください。

### 6.4 Tracking status更新

代表的な更新:

```text
PENDING -> ACTIVE
ACTIVE -> FINISHED
PENDING -> ERROR
ACTIVE -> ERROR
```

- MLflow Run作成／回収後に`ACTIVE`
- 成功時にMLflow Runを`FINISHED`へ終了し、DBを`FINISHED`
- Execution失敗時にMLflow Runを`FAILED`へ終了
- cancel時にMLflow Runを`KILLED`へ終了
- MLflow操作失敗時に`ERROR`とredacted errorを保存

Ariadne Execution statusとMLflow tracking statusを同一enumへ統合しないでください。両者は別の状態機械です。

### 6.5 MLflow障害時のExecution扱い

要件と既存方針を調査し、以下を明示してください。

- Run作成不能時に計算を停止するか
- metrics記録失敗時に計算結果を成功扱いできるか
- Artifact upload失敗時の扱い
- terminate失敗時の扱い

推測で決めないでください。規範要件が不足する場合は、最小限安全なpolicyを文書化し、Requirement Gapとして報告してください。

少なくとも、MLflow障害を握り潰して`FINISHED`と記録してはなりません。`mlflow_tracking_error`にはcredentialを含まないredacted概要を保存してください。

### 6.6 Retry

- retryが新しいAriadne Executionを作る場合、新Executionは原則として新しいMLflow Runを持つ
- 同じExecutionのWorker再実行は既存MLflow Runを再利用する
- Stage Attempt retryだけを理由に新しいtop-level MLflow Runを無条件作成しない
- 初期実装では1 Execution = 1 MLflow Runを維持する
- retry元との関係はAriadne DBで管理し、MLflow tagへ必要な参照を追加してよい

### 6.7 Cancel

- cancel要求時点でRun未作成なら、擬似Runを作成しない
- active MLflow Runがある場合は`KILLED`へ終了する
- terminate失敗時はtracking errorを記録する
- Ariadne cancel処理とMLflow terminateの競合をtestする

---

## 7. Scientific metadataの記録

### 7.1 Params

少なくとも次を記録可能にしてください。

- algorithm
- estimator
- hyperparameter
- random seed
- analysis mode
- input mode

MLflow paramの型制約へ合わせる正規化をAdapterへ集約してください。巨大JSONをparamへ直接押し込まず、必要ならArtifactとhashへ分離してください。

### 7.2 Tags

Webでは最低限:

```text
ariadne.execution_origin = WEB
ariadne.execution_id
ariadne.project_id
ariadne.pipeline_definition_version_id
ariadne.execution_mode
ariadne.code_commit
```

CLIでは最低限:

```text
ariadne.execution_origin = CLI
ariadne.pipeline
ariadne.code_commit
```

必要に応じてDataset／Configuration hashをtagではなくparamまたはArtifactへ記録してください。秘密情報をtagへ入れないでください。

### 7.3 Metrics

Stageごとにnamespaceを分離してください。

例:

```text
discovery.edge_count
discovery.runtime_seconds
inference.ate
inference.standard_error
```

NaN、Infinity、非数値、巨大値の扱いを明示し、testしてください。

### 7.4 Artifacts

Stageごとにpathを分離してください。

例:

```text
discovery/graph.json
discovery/manifest.json
inference/estimate.json
inference/report.html
```

Ariadne Artifact Storeを正本とするArtifactと、MLflowへ複製するArtifactの責務を明示してください。MLflow upload成功だけでAriadne ArtifactをAVAILABLEにしないでください。

### 7.5 共通metadata

可能な範囲で次を記録してください。

- Dataset Version ID／content hash
- Configuration Version ID／content hash
- Causal Graph Version ID／content hash
- Causal Design Version ID／content hash
- Git commit
- package version
- dependency lock hash
- container image digest
- execution environmentの安全な要約

credential、connection string、SAS、token、passwordは記録してはなりません。

---

## 8. CLI連携

### 8.1 CLI option

既存CLIを調査し、必要なら次と同等のoptionを追加してください。

```text
--mlflow-tracking-uri
--mlflow-experiment
--mlflow-run-name
--resume-mlflow-run-id
--disable-mlflow
```

- 曖昧な`--run-id`は意味を分類する
- MLflow IDなら`--resume-mlflow-run-id`へ移行
- 人間向け名称なら`--mlflow-run-name`
- Ariadne Execution IDならCLI方針との整合を確認
- deprecated aliasを残す場合はwarningと廃止方針を文書化

### 8.2 CLI bootstrap

- tracking有効時、CLI bootstrapがMLflow Runを開始または再開する
- 取得した`mlflow_run_id`をApplication層へ明示注入する
- Planner／RunnerはUUIDを生成しない
- CLIはAriadne Execution rowを作成しない
- CLIは原則としてAriadne Metadata DBを必要としない
- 実験entry pointはCLIと同じtracking bootstrapを再利用する

### 8.3 CLI終了状態

- 正常終了: `FINISHED`
- 例外: `FAILED`
- user cancellation: 要件に従い`KILLED`
- `--disable-mlflow`: Null Tracker、Run IDなし

context managerを使用してよいですが、共通命名規則とredactionは同じAdapter／serviceを使用してください。

---

## 9. Transaction境界と整合性

MLflowとPostgreSQLを分散transactionで原子的にcommitできるとは仮定しないでください。

次の障害窓を列挙し、回復処理を実装・testしてください。

1. DB Execution作成後、Worker開始前
2. MLflow Run作成前
3. MLflow Run作成後、DB Run ID保存前
4. DB Run ID保存後、計算開始前
5. 計算成功後、metrics記録前
6. metrics記録後、Artifact upload前
7. Artifact upload後、MLflow terminate前
8. MLflow terminate後、Ariadne status確定前
9. cancelとterminateの競合
10. Worker lease失効と再実行

各窓で、二重Run、孤児Run、誤ったFINISHED、失われたerrorを防ぐ方針を明示してください。

必要に応じて、MLflow操作をStage AttemptまたはExecution Eventへ記録してよいですが、過剰な汎用Outboxを新設する前に既存構造との整合を評価してください。

---

## 10. Secret redaction

最低限、次をredact対象として扱ってください。

- password
- token
- secret
- credential
- connection string
- authorization header
- SAS query
- account key

対象:

- `mlflow_tracking_error`
- application log
- Execution Event payload
- Audit Event
- Manifest
- MLflow tag
- MLflow param
- exception chainのserialization

redaction後のmessageは診断可能性を残しつつ、秘密値を含めないようにしてください。

---

## 11. 必須テスト

### 11.1 Domain／DB

- MLflow列のdefaultとnullable
- tracking statusの許可値
- 非NULL`mlflow_run_id`の一意制約
- 複数NULLが許可される
- modeごとの初期status
- invalid invariantの拒否
- migration upgrade／downgrade
- fresh DBとupgraded DBのschema一致
- 既存Execution保持

### 11.2 Adapter unit test

MLflow SDKをmockまたはfakeし、次を検証してください。

- experimentのresolve／create方針
- Run作成
- Run再開
- execution ID tag検索
- 0件、1件、複数件
- params型変換
- metrics数値検証
- tags文字列化
- Artifact path
- terminate status
- timeout
- bounded retry
- non-retryable error
- secret redaction
- active run global stateへ依存しない

### 11.3 Null Tracker

- SDKを呼ばない
- 擬似IDを返さない
- log operationが安全にno-opになる
- tracking無効状態を呼出し側が識別できる

### 11.4 API test

- `POST /executions`でMLflow SDKを呼ばない
- `RUN`は`PENDING`
- `DRY_RUN`は`NOT_REQUIRED`
- `VALIDATE_ONLY`は`NOT_REQUIRED`
- responseにtracking情報を公開する場合の契約
- RBAC、idempotencyへの影響がない

### 11.5 Worker integration test

- Execution開始時にMLflow Runを作成
- 必須tagが付く
- `mlflow_experiment_id`と`mlflow_run_id`をDBへ保存
- tracking statusが`ACTIVE`
- Worker再実行時に重複Runを作らない
- DB保存前crash後にtag検索でRunを回収
- 複数一致時に自動選択しない
- 成功時`FINISHED`
- Execution失敗時MLflow `FAILED`
- cancel時`KILLED`
- Run作成失敗時`ERROR`
- params記録失敗
- metrics記録失敗
- Artifact upload失敗
- terminate失敗
- redacted error保存
- lease失効後再実行

### 11.6 MLflow integration test

可能な限り、実MLflow Tracking Serverまたはlocal file／SQLite backendを使用したintegration testを追加してください。

検証:

- Runの実作成
- tag検索
- params、metrics、artifacts
- terminate状態
- Run回収

mock testだけで完了扱いにしないでください。中央環境credentialは使用せず、隔離されたtest backendを使用してください。

### 11.7 CLI integration test

- CLIがAriadne Executionを作成しない
- tracking有効時にMLflowがRun IDを採番
- Application層へID注入
- Planner／RunnerがUUIDを生成しない
- `--resume-mlflow-run-id`
- `--disable-mlflow`
- 旧`--run-id`のdeprecatedまたは削除
- 実験entry pointが同じbootstrapを使用
- success／failure／cancelのterminal status

### 11.8 Scientific metadata test

- algorithm、estimator、seed、analysis mode
- Dataset／Configuration IDとhash
- code commit、package version、lock hash
- namespaced metrics
- namespaced Artifact path
- NaN／Infinityの扱い
- secretが記録されない

### 11.9 Concurrency test

実PostgreSQLと複数Workerを用いて、同一Executionに対する同時ensureでMLflow Runが重複しないことを検証してください。

完全な分散lockがない場合でも、tag検索、DB unique constraint、再確認を組み合わせ、最終的に複数Executionへ同じRun IDを割り当てず、同一Executionで複数Runを恒常的に作らない設計にしてください。

競合により孤児MLflow Runが生じ得る場合は、検出・診断・cleanup方針を明示してください。

---

## 12. CIおよびtest環境

testを次のsuiteへ分類してください。

```text
unit
postgres
worker
mlflow
cli
e2e
```

CIで最低限:

1. Adapter／Domain unit test
2. PostgreSQL migration＋constraint test
3. Worker integration test
4. local MLflow integration test
5. CLI test
6. failure injection test

中央MLflow Server、実credential、実Artifact containerへ依存しないようにしてください。

---

## 13. 文書更新

最低限、次を更新してください。

- 要件定義書
- データモデル定義書
- API仕様
- CLI利用方法
- Webサービス運用ガイド
- `.env.example`
- Compose利用方法
- local MLflow Trackingの設定
- 中央Tracking Server接続方法
- ExecutionとMLflow Runの責務分担
- ID体系
- failure semantics
- migration手順
- deprecated option／API

文書では、実装済みと将来要件を区別してください。

---

## 14. Traceability Matrix

次の形式で作成してください。

| Requirement ID | 規範要件 | 実装file | Test file | Status | Evidence / Gap |
|---|---|---|---|---|---|

Status:

- `Implemented`
- `Partially Implemented`
- `Not Implemented`
- `Blocked by Requirement Conflict`
- `Not Applicable`

根拠なしにImplementedとしないでください。

---

## 15. 禁止事項

- MLflow SDK呼出しをCLI、Worker、各Stageへコピーする
- server Workerで暗黙のactive runに依存する
- Worker再実行ごとに無条件で新Runを作成する
- `mlflow_run_id`の代わりに独自UUIDを生成する
- Ariadne `execution_id`とMLflow `run_id`を同じfieldへ格納する
- MLflowをQueue、RBAC、lease、Heartbeatの正本にする
- MLflow障害を握り潰す
- credentialをDB、log、tag、param、Manifestへ保存する
- migrationで既存Executionを削除する
- duplicate Run IDを推測で片方へ統合する
- testをskip／xfailして完了扱いにする
- mock testだけで連携完了とする
- `latest` image tagを使用する
- 不要な汎用`ExternalRunBinding`を導入する
- 1 Execution = 1 MLflow Runの初期方針を無断でnested runへ変更する

---

## 16. 期待する成果物

1. `Execution`のMLflow関連列
2. Alembic migration
3. DB constraint
4. Experiment Tracker Port
5. MLflow Adapter
6. Null Tracker
7. 設定resolver
8. Worker ensure処理
9. Web／Worker状態連携
10. CLI bootstrap連携
11. params／metrics／tags／artifacts記録
12. failure statusとredaction
13. unit、PostgreSQL、Worker、MLflow、CLI、concurrency test
14. CI更新
15. 文書更新
16. Traceability Matrix
17. 実行したtest commandと結果
18. 未解決Gap一覧

---

## 17. 完了条件

次をすべて満たした場合のみ完了としてください。

- `execution`に必要なMLflow列が存在する
- 非NULL`mlflow_run_id`が一意で、複数NULLを許容する
- tracking statusと障害概要を永続化できる
- API受付時にMLflow Runを作成しない
- Worker開始時にRunを冪等にensureする
- Run作成後DB保存前crashから回復できる
- Worker再実行でRunを重複作成しない
- 成功、失敗、cancelがMLflow terminal statusへ反映される
- Ariadne Execution statusとMLflow tracking statusが分離される
- `DRY_RUN`／`VALIDATE_ONLY`でRunを作成しない
- CLIがAriadne Executionを作成しない
- CLIのIDをMLflowが採番する
- Planner／Runnerが擬似IDを生成しない
- MLflow SDKがAdapterへ隔離される
- server Workerがexplicit `run_id`を使用する
- params、metrics、tags、artifactsが規約どおり記録される
- secretがDB、log、tag、param、Manifestへ漏れない
- PostgreSQL、Worker、MLflow integration、CLI、concurrency、failure injection testが成功する
- 文書とTraceability Matrixが更新される

全項目を満たせない場合は、結果を偽らず、未実装、失敗、要件矛盾を明示してください。

---

## 18. 最終報告形式

最終回答は次の順で出力してください。

1. 調査結果と既存Gap
2. 採用したArchitecture
3. DB modelとmigration
4. Port／Adapter
5. Web／Worker連携
6. CLI連携
7. failure semantics
8. secret redaction
9. 変更file一覧
10. test command、終了code、結果
11. Traceability Matrix集計
12. 未解決事項と残存リスク

数値、件数、test結果は実際の実行結果から記載し、推測で補完しないでください。
