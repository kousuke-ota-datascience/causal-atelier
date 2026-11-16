# 21_13_entity_execution

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`; original ID, level and state retained.  
**Source blob:** `72903b9ad48b5b7edabaa7bb1c2cace42aa46ce7`.

---

### 3.7 ExecutionPlan

定義: 固定されたAnalysisSpecificationからplannerが生成するruntime Stage DAGの不変plan。

| 属性 | PK | FK | データ型 | NOT NULL | その他制約 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| `execution_plan_id` | 1 |  | UUID / VARCHAR(36) | 1 | 不変 | Execution Plan識別子 |
| `project_id` |  | `Project.project_id` | UUID / VARCHAR(36) | 1 | INDEX, `ON DELETE RESTRICT` | 所属Project |
| `analysis_specification_id` |  | `AnalysisSpecification.analysis_specification_id` | UUID / VARCHAR(100) | 1 | INDEX; logical FK | 入力Specification。物理FK有無に依存しない論理参照 |
| `analysis_family` |  |  | VARCHAR(20) | 1 | `EXPLORATORY / CAUSAL / PREDICTIVE` | Family |
| `plan_schema_version` |  |  | VARCHAR(100) | 1 |  | Plan schema version |
| `planner_id` |  |  | VARCHAR(100) | 1 |  | Planner識別子 |
| `planner_version` |  |  | VARCHAR(40) | 1 |  | Planner version |
| `stages_json` |  |  | JSON | 1 |  | StageDefinition一覧 |
| `dependencies_json` |  |  | JSON | 1 |  | Stage dependency/binding DAG |
| `plan_hash` |  |  | VARCHAR(64) | 1 | UNIQUE | canonical Plan hash |
| `created_at` |  |  | TIMESTAMP WITH TIME ZONE | 1 |  | 生成日時 |

設計判断・制約:
- ExecutionPlanは生成後に上書きしない。
- `analysis_family`は入力AnalysisSpecificationのFamilyと一致しなければならない。
- Navigation Stage / browser routeをExecutionPlanへ保存しない。

### 3.8 Execution

定義: 一つのAnalysis Operationを、固定されたinputとsnapshotで実行するcanonical execution。

| 属性 | PK | FK | データ型 | NOT NULL | その他制約 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| `execution_id` | 1 |  | UUID / VARCHAR(36) | 1 | 不変 | Execution識別子 |
| `project_id` |  | `Project.project_id` | UUID / VARCHAR(36) | 1 | INDEX, `ON DELETE RESTRICT` | 所属Project |
| `analysis_family` |  |  | VARCHAR(20) | 1 | `CAUSAL / EXPLORATORY / PREDICTIVE` | Analysis Family |
| `dataset_version_id` |  | `DatasetVersion.dataset_version_id` | UUID / VARCHAR(36) | 1 | INDEX, `ON DELETE RESTRICT` | 入力Dataset Version |
| `input_graph_version_id` |  | `GraphVersion.graph_version_id` | UUID / VARCHAR(36) |  | INDEX, `ON DELETE RESTRICT` | 入力Graph Version |
| `input_result_id` |  | `Result.result_id` | UUID / VARCHAR(36) |  | INDEX, `ON DELETE RESTRICT` | 上流Result |
| `batch_key` |  |  | UUID / VARCHAR(36) | 1 | INDEX | batch / comparison単位 |
| `operation` |  |  | VARCHAR(20) | 1 | `DISCOVERY / IDENTIFICATION / ESTIMATION / REFUTATION / SENSITIVITY` | Operation |
| `objective_snapshot` |  |  | TEXT |  |  | 受付時objective snapshot |
| `rationale_snapshot` |  |  | TEXT |  |  | 受付時rationale snapshot |
| `analysis_spec_json` |  |  | JSON | 1 | canonical execution snapshot | 実行用Analysis Specification snapshot |
| `algorithm_or_estimator` |  |  | VARCHAR(100) | 1 |  | algorithm / estimator |
| `parameter_json` |  |  | JSON | 1 | default `{}` | parameter snapshot |
| `random_seed` |  |  | BIGINT |  |  | random seed |
| `code_version` |  |  | VARCHAR(200) | 1 |  | code version |
| `runtime_version_json` |  |  | JSON | 1 | default `{}` | runtime/library versions |
| `snapshot_hash` |  |  | VARCHAR(128) | 1 |  | canonical snapshot hash |
| `snapshot_schema_version` |  |  | VARCHAR(100) | 1 |  | snapshot schema version |
| `status` |  |  | VARCHAR(20) | 1 | `QUEUED / RUNNING / SUCCEEDED / FAILED / CANCELLED` | technical status |
| `retry_count` |  |  | INTEGER | 1 | default `0`, `>= 0` | retry回数 |
| `last_error_summary` |  |  | TEXT |  |  | 最終technical error |
| `requested_by` |  |  | VARCHAR(200) | 1 |  | 要求者 |
| `requested_at` |  |  | TIMESTAMP WITH TIME ZONE | 1 |  | 受付日時 |
| `started_at` |  |  | TIMESTAMP WITH TIME ZONE |  |  | 開始日時 |
| `finished_at` |  |  | TIMESTAMP WITH TIME ZONE |  |  | 終了日時 |
| `base_execution_id` |  | `Execution.execution_id` | UUID / VARCHAR(36) |  | INDEX, self reference | rerun/revision元Execution |
| `revision_kind` |  |  | VARCHAR(20) |  | NULL / `RERUN / REVISED` | revision種別 |
| `change_reason` |  |  | TEXT |  |  | 変更理由 |
| `lease_owner` |  |  | VARCHAR(200) |  | INDEX | worker lease owner |
| `lease_expires_at` |  |  | TIMESTAMP WITH TIME ZONE |  | INDEX | worker lease期限 |

設計判断・制約:
- Submit後のinput Dataset/Graph/Result、analysis snapshot、method、parameterを上書きしない。
- Operation別input制約は`6.4`で定義する。
- `base_execution_id`を使うrevisionも新しいExecution identityを持つ。
- worker token等の内部実装属性は論理Domain属性に含めない。


`runtime_version_json`は最低限、実際の実行環境を再構築するための次のmetadataを保持する。

```text
ariadne_code_version
python_version
platform_system
platform_release
machine
libraries
```

`libraries`には実際にregistered/used runner dependencyとして使用したscientific library versionを保存する。version取得だけを目的にfuture optional dependencyをimportしない。

Canonical `Execution`には`execution_plan_id`を独立属性として必須化しない。ExecutionPlan identityを保持するapplication pathでは`analysis_spec_json`内metadataとして扱い得るが、canonical Execution FKと同一視しない。

### 3.9 StageExecution

定義: ExecutionPlanで定義されたruntime Stageのcanonical実行状態。

| 属性 | PK | FK | データ型 | NOT NULL | その他制約 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| `stage_execution_id` | 1 |  | UUID / VARCHAR(36) | 1 | 不変 | StageExecution識別子 |
| `execution_id` |  | `Execution.execution_id` | UUID / VARCHAR(36) | 1 | INDEX, `ON DELETE RESTRICT` | 親Execution |
| `stage_key` |  |  | VARCHAR(100) | 1 | UNIQUE(`execution_id`,`stage_key`) | Execution内Stage key |
| `stage_type_json` |  |  | JSON | 1 |  | runtime StageType |
| `ordinal` |  |  | INTEGER | 1 | `>= 0` | 表示/plan順序 |
| `dependencies_json` |  |  | JSON | 1 | default `[]` | 依存Stage key |
| `status` |  |  | VARCHAR(40) | 1 | StageExecution状態allowlist | technical stage status |
| `input_binding_json` |  |  | JSON | 1 | default `{}` | resolved input binding |
| `output_binding_json` |  |  | JSON | 1 | default `{}` | produced output binding |
| `last_error_json` |  |  | JSON |  |  | 最終error detail |
| `started_at` |  |  | TIMESTAMP WITH TIME ZONE |  |  | 開始日時 |
| `finished_at` |  |  | TIMESTAMP WITH TIME ZONE |  |  | 終了日時 |
| `created_at` |  |  | TIMESTAMP WITH TIME ZONE | 1 |  | 生成日時 |

設計判断・制約:
- `stage_execution_id`と`execution_id`のidentity pairは一意である。
- Navigation Stageとは別概念であり、Family-local UI Stage IDをruntime lifecycleへ流用しない。

### 3.10 StageAttempt

定義: StageExecutionに対するappend-only retry/attempt history。

| 属性 | PK | FK | データ型 | NOT NULL | その他制約 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| `stage_attempt_id` | 1 |  | UUID / VARCHAR(36) | 1 | 不変 | StageAttempt識別子 |
| `stage_execution_id` |  | `StageExecution.stage_execution_id` | UUID / VARCHAR(36) | 1 | INDEX, `ON DELETE RESTRICT` | 対象StageExecution |
| `attempt_number` |  |  | INTEGER | 1 | `> 0`; UNIQUE(`stage_execution_id`,`attempt_number`) | attempt連番 |
| `worker_id` |  |  | VARCHAR(200) | 1 |  | worker識別子 |
| `started_at` |  |  | TIMESTAMP WITH TIME ZONE | 1 |  | 開始日時 |
| `finished_at` |  |  | TIMESTAMP WITH TIME ZONE |  |  | 終了日時 |
| `error_json` |  |  | JSON |  |  | 失敗detail |
| `effective_random_seed` |  |  | INTEGER |  |  | 実際に使用したseed |

設計判断・制約:
- StageAttemptはappend-onlyとし、過去attemptを上書きしない。


## 98. RD-04：要求の論理データ制約の受入・Trace

**Status:** `DESIGN_CONSTRAINT_MIGRATION / OWNER_CONTENT_REVIEW_PENDING`。以下はRD-04で抽象化した元要件のうち、データ定義・同一性・来歴・正本性に関係する条項を論理設計側に残したもの。原文は出典保証目的で保持する。現行コードで検証済みと主張しない。

### 98.1. FR-076（SPLIT）

- 元要件（設計上の拘束を含む）：Plannerはversionedで不変なExecution Planを生成する
- RD改訂後の要求：分析の実行計画を版管理し、実行時の条件を後から復元できる
- Trace：`FR-076`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../95_rd04_fr_application_review.md)

### 98.2. FR-077（MOVE_BD）

- 元要件（設計上の拘束を含む）：Stage Typeをnamespace、name、versionで識別する
- RD改訂後の要求：【設計制約移管・Legacy Trace】FR-076の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Trace：`FR-077`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../95_rd04_fr_application_review.md)

### 98.3. FR-078（SPLIT）

- 元要件（設計上の拘束を含む）：PlanはStage dependencyとinput/output bindingをDAGとして保持する
- RD改訂後の要求：分析処理の依存順序と処理間の入力・出力の対応を追跡できる
- Trace：`FR-078`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../95_rd04_fr_application_review.md)

### 98.4. FR-082（SPLIT）

- 元要件（設計上の拘束を含む）：idempotency対象Commandでは`(project_id, command_scope, idempotency_key)`をauthorityとし、同一semantic requestをreplay、異なるrequestを`IDEMPOTENCY_CONFLICT`で拒否する
- RD改訂後の要求：再送された同一依頼の重複処理を防止し、同じ識別子で異なる依頼が来た場合は拒否する
- Trace：`FR-082`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../95_rd04_fr_application_review.md)

### 98.5. FR-086a（SPLIT）

- 元要件（設計上の拘束を含む）：stochastic Stageのactual effective random seedを`StageAttempt.effective_random_seed`へ保存し、同一logical Stageのretryで同じseedを再利用する
- RD改訂後の要求：確率的処理を再試行しても同じ実効乱数条件を再現できる
- Trace：`FR-086a`; Status=`ACTIVE`; Implementation=`PARTIAL`; [逐条レビュー](../95_rd04_fr_application_review.md)

### 98.6. FR-087b（SPLIT）

- 元要件（設計上の拘束を含む）：Execution `runtime_version_json`にAriadne code、Python、platform、machineおよび実際に利用したscientific library versionを保持する
- RD改訂後の要求：分析の再現に必要な実行環境と科学ライブラリの版を確認できる
- Trace：`FR-087b`; Status=`ACTIVE`; Implementation=`PARTIAL`; [逐条レビュー](../95_rd04_fr_application_review.md)
