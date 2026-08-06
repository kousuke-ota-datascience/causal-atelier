# ariadne 用語集

- 文書版: 1.0
- 作成日: 2026-08-04
- 対象: ariadne Webサービス要件定義書 v1.4、データモデル定義書 v1.4 で使用する用語

## 用語一覧

| 用語 | 定義 |
|---|---|
| **Ariadne Execution** | Web実行要求、Queue、RBAC、idempotency、lease、heartbeat、cancel、retryの管理単位。CLIでは作成しない。物理テーブル `execution`、識別子 `execution_id`。 |
| **MLflow Run** | 科学的・分析的なparams、metrics、artifacts、診断、実験比較の追跡単位。MLflowが採番する。物理的には外部システムが管理する。 |
| **`execution_id`** | AriadneがWeb受付時に採番するExecution ID（UUID文字列）。CLIでは原則null。Ariadne APIの正式識別子。 |
| **`mlflow_run_id`** | MLflowが採番するRun ID。CLIのMLflow有効時に使用する科学実験の主ID。WebではWorker開始時にMLflow Runをensureして関連付ける（将来実装）。CLIでMLflow無効時はnull。 |
| **`run_label`** | CLI再現性マニフェストに記録する人間指定の識別ラベル。Ariadne execution_idではなく、MLflow run_idでもない。`--run-label` CLIオプションで指定する。未指定時はnull。 |
| **`run_name`** | 人間向けの表示名。一意識別子ではない。MLflowのrun名として使用する場合はMLflow語彙に従う。 |
| **Stage Execution** | Ariadne Execution内のstage単位の実行管理エンティティ。物理テーブル `stage_execution`、識別子 `stage_execution_id`。 |
| **Stage Attempt** | Stage Executionの試行履歴。Workerのlease、heartbeat、workspace、error、resource usageを保持する。再試行時は既存Attemptを上書きしない。 |
| **ExecutionIdentity** | CLIとWeb実行の識別contextを名前空間とともに保持する共通型。`origin`（CLI/WEB）、`execution_id`、`mlflow_run_id`、`primary_namespace`（ARIADNE/MLFLOW/NONE）、`primary_id`を持つ。 |
| **Execution Plan** | Execution受付時に確定したstage構成、入力Version、hash、input modeおよびparameterの不変canonical document。Web/APIのみ。 |
| **RunManifest** | CLI pipelineが各stageの完了時に書き出す再現性マニフェストYAML。`run_label`、設定ファイルhash、出力artifactパスを記録する。 |
| **Execution管理** | Ariadneが担う責務: Queue、RBAC、idempotency、lease、heartbeat、cancel、retry。MLflowはこれらの正本ではない。 |
| **実験追跡 (Experiment Tracking)** | MLflowが担う責務: params、metrics、artifacts、診断、実験比較。AriadneはMLflowを科学実験追跡として使用する（将来実装）。 |
| **`--run-id`** | CLIオプション。deprecated alias。`--run-label`の旧名称。将来廃止予定。 |
| **`--run-label`** | CLIオプション。マニフェストに書き込む人間指定ラベル。Ariadne execution_idではない。 |
| **`--execution-id`** | v1.4で削除されたCLIオプション。CLIはAriadne Executionを作成しないため不要。 |
| **DRY_RUN** | Execution modeの値。Planのシリアライズのみ行い、実処理もMLflow Runも作成しない。 |
| **VALIDATE_ONLY** | Execution modeの値。Planのvalidationのみ行い、Stage実行もMLflow Runも作成しない。 |
| **NullTracker** | MLflow無効時に使用するNo-op ExperimentTracker実装（将来実装）。擬似IDを生成しない。 |

## ID名前空間の対応

| ID | 採番者 | 使用場面 | 追加先 |
|---|---|---|---|
| `execution_id` | Ariadne (UUID) | Web受付時 | `execution` table |
| `mlflow_run_id` | MLflow | CLI有効時 / Web Worker開始時 | MLflow Tracking Server（将来: `execution` table） |
| `run_label` | 人間 | CLI manifest | manifest YAML |
| `stage_execution_id` | Ariadne (UUID) | Web Worker実行中 | `stage_execution` table |

## 禁止事項

- `run_id`という名前空間不明の識別子を共通モデル、Manifest、Execution Plan、ログへ新規追加しない
- CLIでAriadne `execution_id`を生成・保持しない
- WebのAriadne `execution_id`をMLflow `run_id`で代用しない
- PlannerおよびRunnerがUUIDフォールバックを生成しない
- tracking無効時に擬似IDを生成しない
- MLflowをQueue、RBAC、idempotency、lease、heartbeatの正本にしない
