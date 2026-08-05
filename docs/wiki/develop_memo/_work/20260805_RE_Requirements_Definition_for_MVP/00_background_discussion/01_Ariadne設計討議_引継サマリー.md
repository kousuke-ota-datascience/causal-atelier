# Ariadne設計討議 引き継ぎサマリー

## 0. 対象コードベースと参照資料

対象は `ariadne_20260804_100233.zip`。

主な参照資料:

- `ariadne/docs/wiki/develop_memo/_work`
  - 過去の修正タスク
  - 一部タスクには実行結果、回答、検証記録を含む
- `ariadne/docs/wiki/requirement_definition/00_glossary.md`
- `ariadne/docs/wiki/requirement_definition/01_web_service_requirements_v1.3.md`
- `ariadne/docs/wiki/requirement_definition/01_web_service_requirements_v1.4.md`
- `ariadne/docs/wiki/requirement_definition/02_data_model_definition_v1.4.md`
- `ariadne/docs/wiki/requirement_definition/traceability_matrix.md`

現行データモデルは、Resource、Version、Execution、Fact / Artifact、Projectionを区別し、Metadata DBには識別子、hash、所在、来歴、状態、検索・権限制御用projectionを保存する方針を持つ。

Execution周辺には、`execution`、`execution_plan`、`stage_execution`、`stage_attempt`、各種入力binding、input preparation、event、manifest、outbox、audit等、多数のテーブルが存在する。

---

# 1. 現在のプロジェクト状態に関する評価

## 1.1 稼働・検証状況

- 本番または実業務での稼働実績はない。
- 主としてCLIで計算経路を動かした段階。
- 開発者以外の分析者がWeb上の一連の導線を検証した実績はない。
- したがって、現状は「MVP」と断定するより、**Engineering PrototypeまたはTechnical Vertical Slice**と位置付ける方が正確。
- ユーザビリティ、業務価値、継続利用意向、既存Notebook/CLIに対する優位性は未評価。

## 1.2 辛口評価

- 技術構想は一貫している。
- 論理モデルは体系的。
- しかし、実利用前にエンタープライズ級のメタデータ・実行管理モデルを先行実装しており、**過剰設計リスクが高い**。
- 「実装済み」は必要性の証明ではない。
- 現行ERは完成仕様ではなく、**最大構成の設計仮説**として扱うべき。
- 現在の状態は「畳水練」に近い。泳法、記録方式、障害管理を精緻化している一方、利用者が実際の分析業務で価値を得られるかは未検証。

---

# 2. Ariadneの意味論的な背骨

Ariadneの本質は、単なる因果分析アルゴリズム実行基盤、Pipeline Runner、またはMLflow UIの代替ではない。

## 2.1 本質の一文定義

> **Ariadneは、分析上の問いや目的から、使用したデータ、分析仕様、プログラム、パラメータ、実行履歴、生成物および限定付きの解釈までを、再現・比較・監査可能な来歴として結び付ける分析ワークスペースである。**

短く表現するなら:

> **問いから分析結果までの「なぜ・何を・どう実行し・何が得られたか」を、一つの来歴として管理する。**

## 2.2 意味論上必要な概念

```text
Project
= 1つのResearch Topicを扱う業務、権限、来歴の境界

Research Context
= 分析を行う理由と問いの文脈

  Problem Statement
  + Research Question
  + Significance
  + Hypothesis

  ※成熟度に応じて一部は未定義またはDraftでよい

Analysis Specification
= 何を、どの方法、仮定、評価基準で分析するかを表す
  ドメイン固有の分析仕様

例:
- Discovery Configuration
- Causal Design
- ML Training Specification
- Model Evaluation Specification
- Explainability Specification

Execution Plan
= 今回の処理で使用するResearch Context、入力Version、
  Analysis Specification、Algorithm、Parameter、Runtime、
  Stage構成、出力契約を固定した不変の計画

Execution
= Execution PlanをAriadne管理下で遂行する、
  一回の処理要求とそのライフサイクル

Result
= Executionによって得られた分析上の結果

Artifact
= Resultを構成または裏付ける物理的生成物

Claim / Interpretation
= Resultを根拠として人間が提示する、
  Research Questionへの範囲、仮定、限界付きの回答
```

## 2.3 重要な設計原則

```text
Start loose.
Formalize progressively.
Conclude strictly.
```

意味:

- 分析者は曖昧なProblem Statementから開始してよい。
- Research Question、Significance、Hypothesisを開始時の一律必須入力にはしない。
- 分析の進行に応じてResearch Contextを精緻化する。
- ResultからClaimを確定する段階では、問い、根拠、範囲、仮定、限界を明示する。
- 曖昧な問いから始めることは許すが、曖昧なまま強い結論を確定することは許さない。

## 2.4 『リサーチの技法』との関係

ウェイン・C・ブースらの枠組みにある、

```text
Focused Topic
→ Research Question
→ Significance / So what?
→ Answer / Claim
→ Reasons and Evidence
```

を下敷きにする。

ただし、この枠組みを必須入力フォームとして直訳しない。

Research Topic、Research Question、Significance、Hypothesisは、分析来歴を説明する概念として必要だが、すべてをProject作成時に完成させることは要求しない。

過去の `20250603_ID-POSを用いたデータ分析事例のリサーチ.docx` では、初版から第二版にかけてTopicとQuestionが変化し、未解決時の不利益も作業上の困難に寄っており、未完成箇所が残る。これは、問いや意義の言語化が一回の入力で完成するものではないことを示す一事例として扱う。

---

# 3. 因果分析に限定しない将来像

Ariadneは将来的に次を扱う想定。

- 因果探索
- 因果効果推定
- 機械学習モデルの学習
- 機械学習モデルの評価
- 説明可能AI
- 感度分析
- モデル比較
- 仮説生成・検証・再現

したがって、Executionや`execution_id`をCausal Designに依存させない。

Causal Designは、`CAUSAL / ESTIMATION`に必要なAnalysis Specificationの一種とする。

同様に:

```text
CAUSAL / DISCOVERY
→ Discovery Configuration

CAUSAL / ESTIMATION
→ Causal Design

MACHINE_LEARNING / TRAINING
→ ML Training Specification

MACHINE_LEARNING / EVALUATION
→ Model Version + Evaluation Specification

EXPLAINABILITY / EXPLANATION
→ Model Version + Explainability Specification
```

また、以下を混同しない。

- 関連が強い変数
- 予測性能に寄与する変数
- モデルが利用する変数
- SHAP等でattributionが大きい変数
- 介入によりoutcomeを変える因果変数

Claimには、少なくとも次のclaim typeを想定する。

- `PREDICTIVE`
- `ASSOCIATIONAL`
- `MODEL_BEHAVIOR`
- `CAUSAL`

---

# 4. SPEC-001 Execution Identityの議論

## 4.1 Executionの正本候補

> **Executionは、Project内で、受付時に固定されたExecution Planに基づいてAriadneが受け付け、管理する、一回の非同期処理要求とそのライフサイクルを表す。**

Executionは、特定の分析ドメインには依存しない。

## 4.2 execution_idの正本候補

> **`execution_id`は、Ariadneが管理する一回のExecutionを一意に識別するAriadne固有IDである。**

`execution_id`は、次を同一Executionへ関連付ける。

- Project
- 要求者、認可
- 冪等性
- Execution Plan
- Queue / Outbox
- 状態遷移
- Stage Execution
- Stage Attempt
- Event
- cancel、retry
- Artifact
- Result
- Audit
- MLflow Runとの対応

`execution_id`は次のIDではない。

- Research Topic
- Research Question
- Hypothesis
- Analysis Specification
- Execution Plan
- Result
- Artifact
- Claim
- MLflow Run

重要な表現:

> **`execution_id`は一回の実行計画のIDではなく、その計画を遂行する一回のExecutionのIDである。**

## 4.3 Execution Planとの関係

Execution Planは概念として必須。

ただし、独立テーブルや独立IDが必須とは限らない。

現行スキーマでは`execution_plan`が`execution_id`をPK兼FKとして持つ完全な1対1で、canonical JSONとhashを保持する。

そのため、物理的には次のどちらでも意味論を維持できる。

```text
案A:
execution_planを1対1の独立テーブルとして維持

案B:
executionへplan_json、plan_hashを統合
```

本質は、実行時の計画が不変snapshotとして残ることであり、独立テーブルの有無ではない。

## 4.4 retryと再実行

- Worker障害等の技術的retry:
  - 同じ`execution_id`
  - 同じ`stage_execution_id`
  - 新しい`stage_attempt_id`
- 利用者による再実行:
  - 新しい`execution_id`
  - 同一条件の再現確認でも、新しい処理要求なら別Execution
- 元Executionとの関係は、`reproduces`、`derived_from`等のrelationで表現する。正式名称は未決。

## 4.5 CLIとWeb

### Web/API

- Ariadne Executionを作成する。
- `execution_id`をAriadneが採番する。
- Queue、RBAC、冪等性、Lease、Heartbeat、cancel、retry等をAriadneが管理する。
- 実計算開始時にWorkerがMLflow Runを作成またはensureし、`mlflow_run_id`をExecutionへ関連付ける。

### Local CLI

- Ariadne Executionを作成しない。
- `execution_id`を持たない。
- MLflow有効時は`mlflow_run_id`を科学計算の主IDとする。
- MLflow無効時は擬似IDを生成しない。
- Manifest、Artifact、設定hash、code version等で再現性を保持する。

CLIに`execution_id`がないこと自体は破綻ではない。

問題になるのは、CLI Runから次へ戻れない場合。

- Research Context
- Dataset
- Analysis Specification
- code version
- parameter
- Artifact
- Result

---

# 5. Execution Identityの議論から見えた過剰設計

## 5.1 本当の問題

`execution_id`の定義に時間が掛かった理由は、IDが特殊だったからではない。

> **Executionが何のために存在するかを説明する上位モデルが未整理だったため。**

Executionを説明する過程で、Project、Research Context、Analysis Specification、Execution Plan、Result、Artifact、Claimまで議論が広がった。

この広がり自体は、Ariadneの意味論的な背骨を発見するうえで有益だった。

一方、その概念をすべて独立テーブルや独立Resourceにすると、過剰設計になる。

## 5.2 重要な区別

```text
概念として必要
≠ 独立エンティティとして必要
≠ 独立テーブルとして必要
≠ 利用者への必須入力項目として必要
```

## 5.3 当面、独立エンティティ化を避ける候補

- Research Topic
- Research Question
- Significance
- Hypothesis
- Claim
- Execution Plan

これらは概念として保持するが、当初はVersioned JSON、canonical document、または親Resourceのsnapshotとして扱える。

独立Resourceへ昇格するのは、次の要件が実際に現れた場合。

- 独立したライフサイクル
- N:M関係
- 独立検索
- review / approval
- Version差分監査
- 複数Project間での再利用
- 業務上の状態遷移

## 5.4 最小集約候補

```text
Project
Analysis Definition Version
Execution
Result / Artifact
```

### Project

1つの分析テーマと権限・来歴の境界。

### Analysis Definition Version

以下をVersioned Documentとして内包する。

- `objective`
- optional Research Context
- analysis domain / operation
- domain-specific Analysis Specification

### Execution

以下を持つ。

- `execution_id`
- Project
- Analysis Definition Version
- input bindings
- immutable plan snapshot
- status
- Stage / Attempt / Event
- MLflow binding

### Result / Artifact

- Resultは検索・比較・解釈単位
- Artifactは物理生成物
- Manifestは実行実績のcanonical記録

---

# 6. 現行ERに対する暫定評価

## 6.1 現行ERを凍結しない

稼働実績がないため、現行ERを完成仕様として固定しない。

現行ERは、Resource、Version、Execution、Fact / Artifact、Projectionの更新規則が明確であり、設計思想には価値がある。

一方、以下の必要性は未実証。

- 各概念の独立テーブル化
- 全projectionの永続化
- input bindingの型別テーブル分割
- planning時とattempt時のinput preparation分割
- Supporting領域の全Resource
- 全監査・可視化機能

## 6.2 比較的維持理由が強いもの

- `project`
- `dataset`
- `dataset_version`
- `configuration`
- `configuration_version`
- `execution`
- `stage_execution`
- `stage_attempt`
- `artifact`
- `execution_event`
- `outbox_event`
- `audit_event`
- `causal_graph`
- `causal_graph_version`

特にStage Attemptは、Worker、Lease、Heartbeat、error、resource usage、retry履歴を保持し、Stage Executionとは異なるライフサイクルを持つため、分離理由が強い。

## 6.3 統合・再評価候補

- `execution_plan`
- stage input系テーブル
- stage parameter
- planning時 / attempt時のinput preparation
- 低利用または未使用projection
- `execution_result_summary`
- Supporting領域の一部

---

# 7. 必要となる最小の検証シナリオ

まず、利用者が実際に必要とする分析ユースケースを定義し、それを成立させる最小構成を逆算する。

既存テーブルからユースケースを作ってはいけない。

```text
利用者の判断
→ 必要な証拠
→ 証拠を生成する分析
→ 保持すべき来歴
→ 最小論理構造
→ 現行ERとの差分
```

## UC-01 探索的分析から候補仮説を得る

### 状況

具体的な仮説はまだない。

### 例

```text
売上差を説明する候補要因や候補構造を見つけたい。
```

### 最小導線

1. Projectを作成
2. Datasetを登録
3. 対象列・意味を設定
4. 分析方法とparameterを設定
5. 実行
6. 複数結果を比較
7. 候補仮説または候補Graphを保存

### 検証する価値

- 曖昧な問題意識から開始できるか
- 分析設定を理解できるか
- 複数結果比較が判断に役立つか
- 候補仮説へ接続できるか
- 何を来歴として後で見たいか

## UC-02 明示した仮説または分析目的を評価する

### 例A: 因果推論

```text
クーポン施策は売上へ正の効果を持つか。
```

### 例B: 機械学習

```text
購買履歴を追加したモデルは、
顧客属性だけのモデルより予測誤差が小さいか。
```

### 最小導線

1. ProjectとDatasetを選択
2. Questionまたはobjectiveを記録
3. Hypothesisまたは評価目的を記録
4. Analysis Specificationを設定
5. 実行
6. Resultとdiagnosticsを確認
7. 限定付きの解釈を記録
8. 使用データ、code、parameter、Artifactへ遡る

### 検証する価値

- Question / Hypothesisの入力コストは許容可能か
- Analysis Specificationの表現は理解できるか
- Resultから妥当なClaimを作れるか
- 来歴を辿ることに価値があるか
- NotebookやMLflow単体より有用か

## UC-03 同じ問いを別条件・別手法で再評価する

### 目的

Ariadne固有の比較・来歴価値を検証する。

### 最小導線

1. 過去Executionを選択
2. Dataset、method、parameterのいずれかを変更
3. 新しいExecutionとして実行
4. 差分を比較
5. 元Executionとのrelationを確認

### 検証する価値

- Execution Plan snapshotが必要か
- どの差分を比較したいか
- `execution_id`が比較の起点として有用か
- Analysis Definitionを再利用する価値があるか

## UC-04 結果の説明可能性・追跡可能性を確認する

### 目的

第三者が結果の根拠を確認できるか検証する。

### 最小導線

1. Resultを開く
2. 使用Dataset Versionを確認
3. 分析仕様、parameter、code versionを確認
4. Artifactとdiagnosticsを確認
5. Interpretation / limitationを確認

### 検証する価値

- 利用者が実際に必要とする来歴粒度
- 不要なメタデータ
- Result、Artifact、Manifestの区別が必要か
- Claim管理が独立Resourceとして必要か

---

# 8. 利用者検証で観察すべき事項

- どの画面・用語で止まるか
- 何を入力できないか
- Research QuestionやSignificanceはいつなら書けるか
- Notebookへ戻りたくなる箇所はどこか
- Dataset Versionを理解できるか
- Discovery ResultとSaved Graphの違いを理解できるか
- ResultとArtifactの違いを理解できるか
- Graph比較が意思決定に使えるか
- どの来歴を後で見たいか
- retry、cancel、Event履歴が本当に必要か
- どの情報は自動取得すべきか
- どの概念は内部に隠すべきか
- Ariadneがない場合と比べ、作業時間・再現性・説明性が改善するか

---

# 9. 次のチャットで行うべき作業

## 優先1: 意味論的な背骨を短い正本候補として固定

対象:

- Project
- Research Context
- Analysis Specification
- Execution Plan
- Execution
- Result
- Artifact
- Interpretation / Claim

ここでは概念定義だけを行う。テーブル化は決めない。

## 優先2: 最小検証シナリオを確定

まずは次の2ケースを優先する。

1. 探索的分析から候補仮説を得る
2. 明示した仮説または分析目的を評価する

必要であれば、比較再実行と第三者説明を追加する。

## 優先3: シナリオごとの最小情報構造を導出

各シナリオについて整理する。

- 入力
- ユーザー操作
- 実行
- 出力
- 判断
- 必要な来歴
- 必須概念
- 任意概念
- 不要な概念

## 優先4: 最小論理モデルを既存ERへ写像

既存テーブルを次へ分類する。

- 必須
- 内部実装として維持
- JSON / canonical documentへ統合可能
- Projectionとして再生成可能
- 未使用
- 将来要件のみ
- 削除候補

## 優先5: SPEC-001比較表を作る

比較表の列:

- 論点ID
- 論点
- 旧記述の仕様
- 旧記述のドキュメント
- 新記述の仕様
- 新記述のドキュメント
- 実装状況
- 実装状況の根拠
- 正本仕様
- 正本仕様選出の根拠
- 影響範囲
- 未解決事項
- 決定状態

---

# 10. 次チャットで避けるべきこと

- `execution_id`だけを再度深掘りし続ける
- 重要な概念をすぐ独立テーブルへする
- 現行ERを前提にユースケースを作る
- 実装済みであることを必要性の根拠にする
- 全要件を最初の検証対象にする
- Research Question、Significance、Hypothesisを一律必須入力にする
- Web/CLI共通バックエンドの話をExecution Identityへ混ぜる
- MLflow RunとAriadne Executionを同一視する
- テーブル数を減らすこと自体を目的にする
- 利用者検証前に正本スキーマを凍結する

---

# 11. 現時点の主要結論

1. **Ariadneの意味論的な背骨は維持する。**
2. **豊かな概念モデルを、そのまま豊かな物理ERへ展開しない。**
3. **`execution_id`はExecution Planではなく、一回のAriadne Executionを識別する。**
4. **Execution Planは概念として必要だが、独立テーブルである必然性は未確定。**
5. **CLIに`execution_id`がないこと自体は破綻ではない。**
6. **MLflow Runは科学計算、Ariadne ExecutionはControl Plane実行管理を担う。**
7. **現行ERは完成仕様ではなく最大構成の設計仮説。**
8. **本番・利用者検証がないため、MVP適合性とプロダクト価値は未評価。**
9. **今後は代表ユースケースから最小構成を逆算する。**
10. **概念を削るのではなく、独立エンティティ化・必須入力化を抑制する。**
