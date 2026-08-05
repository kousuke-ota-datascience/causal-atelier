# SPEC-001 Execution Identity

## 0. 文書情報

- 文書種別: 正本仕様候補
- 対象: Ariadne Execution および `execution_id`
- 状態: Draft
- 目的:
  - Ariadne における Execution の意味を定義する
  - `execution_id` が識別する対象を定義する
  - Research Context、Analysis Specification、Execution Plan、Result、Claim との関係を整理する
  - Ariadne Execution と MLflow Run の Identity を区別する
  - 因果分析、機械学習、説明可能 AI へ拡張可能な共通概念として定義する

---

# 1. 背景

Ariadne は、因果探索および因果推論だけを実行するツールではなく、将来的には次の分析を扱うことを想定する。

- 因果探索
- 因果効果推定
- 機械学習モデルの学習
- 機械学習モデルの評価
- 説明可能 AI によるモデル説明
- 感度分析
- モデルまたは分析手法の比較
- その他、Research Question に対する証拠を生成する分析処理

したがって、Execution および `execution_id` を、Causal Design、因果推論、特定のアルゴリズム、または特定の分析ドメインに依存させない。

Ariadne では、Web/API 経由の処理について、Ariadne 固有の実行管理を行う。

Ariadne 固有の実行管理には、少なくとも次を含む。

- Project との関連
- User、Role および認可
- 実行要求の受付
- 冪等性
- Execution Plan
- Queue および Transactional Outbox
- Worker の割当て
- Lease および Heartbeat
- cancel
- retry
- Stage Execution
- Stage Attempt
- 状態遷移
- Event
- Artifact および Result との関連
- Audit
- MLflow Run との対応

一方、MLflow は、アルゴリズム、推定器、parameter、random seed、Dataset hash、Configuration hash、metrics、推定値、診断、Artifact 等の科学的・分析的な実行記録を扱う。

MLflow を、Queue、RBAC、冪等性、Worker Lease、Heartbeat 等の Ariadne 固有の実行管理の正本として使用しない。

---

# 2. 基本原則

## 2.1 Project

Project は、1つの Research Topic を管理する、Ariadne における最上位の業務、権限および分析来歴の境界である。

例:

```text
Project:
小売売上に関連または影響する要因の解明
```

1つの Project は、複数の Research Question、Hypothesis、Analysis Specification、Execution、Result および Claim を含むことができる。

```text
Project 1 : N Research Question
Project 1 : N Execution
Project 1 : N Result
Project 1 : N Claim
```

## 2.2 Research Context

Research Context は、分析を行う理由、問いおよび暫定的な考えを表す。

```text
Research Context
= Problem Statement
+ Research Question
+ Significance
+ Hypothesis
```

ただし、これらを Project 作成時または分析開始時の一律な必須入力とはしない。

分析者は、十分に言語化されていない問題意識から分析を開始する場合がある。また、Research Question や Hypothesis は、Dataset の確認、探索的分析、既存知識との比較等を通じて形成または精緻化される場合がある。

したがって、Research Context の構成要素は、分析の成熟度に応じて次の状態を取り得る。

- 未定義
- Draft
- Proposed
- Accepted
- Superseded
- Archived

Ariadne は、曖昧な Research Context から分析を開始することを許容する。

一方、Result を根拠として Claim を確定する段階では、Research Question、Significance、適用範囲、根拠および限界を明示する。

設計原則は次のとおりとする。

```text
Start loose.
Formalize progressively.
Conclude strictly.
```

---

# 3. Research Context を構成する概念

## 3.1 Problem Statement

Problem Statement は、分析者または関係者が認識している問題、違和感、関心または未解決事項を表す。

Problem Statement は、明確な疑問文になっていなくてもよい。

例:

```text
最近、店舗別売上の差が拡大している。
```

```text
ID-POS データを用いて、顧客へ提案可能な分析事例を整理したい。
```

Problem Statement は、Project 作成時における最小限の Research Context として使用できる。

## 3.2 Research Topic

Research Topic は、Project が扱う焦点化された研究対象または問題領域である。

1つの Project は、原則として1つの Research Topic に対応する。

```text
Project 1 : 1 Research Topic
```

例:

```text
ID-POS データを用いた小売売上の変動要因
```

Research Topic は、単なる広い分野名ではなく、Project の分析範囲を判断できる程度に焦点化されることが望ましい。

## 3.3 Research Question

Research Question は、Research Topic について、現時点では答えが確定しておらず、分析によって回答しようとする問いである。

例:

```text
顧客の購買履歴は、翌月売上の予測にどの程度有用か？
```

```text
売上予測モデルが利用する特徴は、店舗セグメント間でどのように異なるか？
```

```text
クーポン利用は、売上にどの程度の因果効果を持つか？
```

同じ Research Topic に対して、異なる分析ドメインの Research Question が存在してよい。

同一の Research Question に対して、複数の Execution を実行できる。

```text
Research Question 1 : N Execution
```

## 3.4 Significance

Significance は、Research Question に答えることで、誰が、何を新たに理解または判断できるようになるのかを表す。

または、その問いに答えられない場合に、何が理解または判断できないままになるのかを表す。

Significance は、少なくとも次の観点を含むことが望ましい。

- Audience
- Knowledge Contribution
- Decision Contribution
- Unresolved Consequence
- Scope

例:

```text
Research Question:
購買履歴は翌月売上の予測に有用か？

Significance:
この問いに答えることで、分析担当者は、
顧客属性だけを用いる場合と比較して、
購買履歴を取得、保持、加工する追加コストが
予測性能の改善に見合うかを判断できる。
```

Significance は、分析開始時には Draft または未定義でもよい。

ただし、Result から Claim を確定する段階では、原則として明示する。

## 3.5 Hypothesis

Hypothesis は、Research Question に対する、評価可能な暫定回答である。

Hypothesis は因果仮説に限定しない。

少なくとも次の claim type を区別する。

- `PREDICTIVE`
- `ASSOCIATIONAL`
- `MODEL_BEHAVIOR`
- `CAUSAL`

すべての Execution に、実行前の Hypothesis を必須とはしない。

探索的 Execution では、Research Question または Problem Statement を入力とし、Hypothesis 候補を出力してよい。

Execution と Hypothesis の関係を表す role として、次を検討対象とする。

- `GENERATE`
- `TEST`
- `COMPARE`
- `REFINE`
- `REPLICATE`

---

# 4. Analysis Specification

Analysis Specification は、何を、どの方法、仮定および評価基準で分析するかを定義する、ドメイン固有の分析仕様である。

例:

- Discovery Configuration
- Causal Design
- ML Training Specification
- Model Evaluation Specification
- Explainability Specification
- Sensitivity Analysis Specification
- Model Comparison Specification

Analysis Specification は、Execution Identity の構成要素ではない。

Execution は、Analysis Domain および Operation に応じて、必要な Analysis Specification を参照する。

```text
CAUSAL / DISCOVERY
→ Discovery Configuration を参照
```

```text
CAUSAL / ESTIMATION
→ Causal Design Version を参照
```

```text
MACHINE_LEARNING / TRAINING
→ ML Training Specification を参照
```

```text
MACHINE_LEARNING / EVALUATION
→ Model Version および Evaluation Specification を参照
```

```text
EXPLAINABILITY / EXPLANATION
→ Model Version および Explainability Specification を参照
```

Causal Design を Execution または `execution_id` の定義へ含めない。

---

# 5. Execution Plan

## 5.1 定義

Execution Plan は、1回の処理で使用する入力、仕様、method、runtime 条件、Stage 構成および出力契約を固定した、不変の計画である。

```text
Execution Plan
├── Project reference
├── Research Context Version または snapshot
├── Input Version bindings
├── Analysis Specification Version bindings
├── Analysis Domain
├── Operation
├── Algorithm / Method
├── Parameter
├── Random seed policy
├── Runtime specification
├── Stage definitions
├── Stage dependencies
├── Input contract
├── Output contract
└── Reproducibility metadata
```

Research Context が未成熟である場合、Execution Plan は、実行時点で定義済みの最も具体的な Research Context を固定する。

Execution Plan は、Research Context の現在値を単に可変参照するのではなく、実行時点の Version または snapshot を保持する。

## 5.2 Execution Plan と Execution の区別

```text
Execution Plan
= 何を、どの入力、条件および手順で実行するか
```

```text
Execution
= その Execution Plan を遂行する一回の処理要求と、
  その実行ライフサイクル
```

したがって、`execution_id` は Execution Plan そのものの ID ではない。

Execution Plan に独立した `execution_plan_id` を付与するか、Execution と1対1の不変 document として保持するかは、データモデル設計における別論点とする。

候補となる多重度は次である。

```text
候補A:
Execution Plan 1 : 1 Execution
```

```text
候補B:
Execution Plan 1 : N Execution
```

この多重度は SPEC-001 では確定しない。

---

# 6. Execution

## 6.1 定義

Execution は、Project 内で、受付時に固定された Execution Plan に基づいて、Ariadne が受け付け、管理する一回の非同期処理要求と、そのライフサイクルである。

Execution には、少なくとも次の責務を含む。

- 実行要求の受付
- Project との関連
- 要求者との関連
- 認可
- 冪等性
- Execution Plan との関連
- Queue への投入
- Transactional Outbox
- Worker の割当て
- Lease
- Heartbeat
- 状態遷移
- Stage Execution
- Stage Attempt
- Event
- cancel
- retry
- Artifact との関連
- Result との関連
- Audit
- 外部 Experiment Tracking ID との対応

Execution は、特定の Analysis Domain に依存しない。

## 6.2 Execution が対応しない概念

Execution は、次の概念そのものではない。

- Project
- Research Topic
- Problem Statement
- Research Question
- Significance
- Hypothesis
- Analysis Specification
- Causal Design
- ML Training Specification
- Model
- Result
- Artifact
- Claim
- MLflow Run

これらは、Execution の文脈、入力、仕様、出力、根拠または外部追跡対象として参照される。

---

# 7. execution_id

## 7.1 定義

`execution_id` は、Ariadne が受け付け、管理する一回の Execution を一意に識別する Ariadne 固有 ID である。

`execution_id` は、次を同一 Execution の情報として関連付ける。

- Project
- 要求者
- 受付時刻
- 認可結果
- 冪等性キー
- Execution Plan
- Queue message
- Stage Execution
- Stage Attempt
- Execution Event
- 実行状態
- cancel 要求
- retry
- Artifact
- Result
- Audit
- MLflow Run との対応

`execution_id` は、Execution Plan そのものを識別する ID ではない。

また、Research Question、Hypothesis、Result、Artifact、Claim または MLflow Run を識別する ID でもない。

## 7.2 execution_id の生成条件

原則として、次の条件を満たす処理について Execution を作成し、`execution_id` を採番する。

- Ariadne Control Plane が処理要求を受け付ける
- Ariadne が要求者および Project 権限を管理する
- Ariadne が Execution Plan を固定する
- Ariadne が処理状態を管理する
- Queue または Worker による非同期処理を行う
- Stage Execution または Attempt を管理する
- cancel、retry、Event または Audit を管理する
- Result または Artifact を Execution へ関連付ける

次の操作は、原則として新しい Execution を作成しない。

- Resource の一覧取得
- Resource の詳細参照
- Draft Resource の軽量な同期編集
- 既存 Result の閲覧
- 複数 Result の比較表示
- 既存 Graph の選択
- lineage の参照
- Artifact の参照
- 単なる画面遷移
- Notebook 内の任意のセル実行
- Ariadne Control Plane を通らない Local CLI 実行

ただし、同期操作に見える場合でも、重い validation、profile 生成または外部処理を Worker で実行する場合には、Execution とすることができる。

## 7.3 Execution の同一性

次の変更を伴う利用者の新しい処理要求は、原則として別 Execution とする。

- Input Dataset Version の変更
- Analysis Specification Version の変更
- Algorithm または Method の変更
- Parameter の変更
- 評価期間の変更
- データ分割の変更
- 対象 Model Version の変更
- Graph Version の変更
- Causal Design Version の変更
- Random seed policy の変更
- Runtime specification の変更
- Stage 構成の変更
- Output contract の変更
- 利用者による明示的な再実行要求

同一条件による再現確認であっても、利用者が新しい処理要求として実行した場合は、新しい `execution_id` を採番する。

元の Execution との関係は、`reproduces`、`derived_from` または同等の relation で表現する。

## 7.4 技術的 retry

Worker 障害または一時的な外部障害による技術的 retry では、新しい `execution_id` を採番しない。

```text
execution_id:
同一

stage_execution_id:
同一

stage_attempt_id:
新規
```

既存の Stage Attempt を上書きしない。

利用者が入力、設定または実行条件を変更して再実行する場合は、技術的 retry ではなく新しい Execution とする。

---

# 8. Result、Artifact および Claim

## 8.1 Result

Result は、Execution によって得られた、分析上の検索、表示または解釈の単位である。

例:

- Discovery Result
- Causal Effect Estimate
- Model Training Result
- Model Evaluation Result
- Feature Importance Result
- Local Explanation Result
- Diagnostic Result

```text
Execution 1 : N Result
```

## 8.2 Artifact

Artifact は、Execution によって生成、使用または登録された物理的な生成物である。

例:

- Parquet
- CSV
- Graph JSON
- model binary
- prediction values
- SHAP values
- diagnostics JSON
- Markdown report
- image
- configuration snapshot
- Manifest

```text
Result
= 分析上の意味を持つ結果

Artifact
= Result を構成または裏付ける物理的生成物
```

## 8.3 Claim

Claim は、Result を根拠として人間が構成する、Research Question への限定付き回答である。

Claim は自動計算結果そのものではない。

```text
Hypothesis
= 分析前または分析途中の暫定回答

Result
= Execution によって得られた計算上の事実

Claim
= Result を根拠として人間が提示する回答
```

Claim は、少なくとも次を含むことが望ましい。

- claim statement
- claim type
- 根拠となる Result
- 対象範囲
- 前提および仮定
- 不確実性
- qualification
- limitation

Claim type の例:

- `PREDICTIVE`
- `ASSOCIATIONAL`
- `MODEL_BEHAVIOR`
- `CAUSAL`

次のような意味の飛躍を行ってはならない。

```text
予測モデルの feature importance が高い
    ↓
その feature は outcome へ因果効果を持つ
```

```text
SHAP attribution が大きい
    ↓
その変数へ介入すれば outcome が変化する
```

```text
Discovery Graph に edge がある
    ↓
真の因果関係が証明された
```

---

# 9. MLflow Run との関係

## 9.1 責務の違い

```text
Ariadne Execution
= Web アプリケーション固有の処理要求と
  オーケストレーションの管理単位
```

```text
MLflow Run
= 科学的、分析的な計算実行の追跡単位
```

MLflow を Ariadne Execution 管理の正本として使用しない。

## 9.2 ID 名前空間

`execution_id` と `mlflow_run_id` は、異なる名前空間に属する。

```text
execution_id
- 採番者: Ariadne
- 対象: Ariadne Execution
- 主な使用場面: Web/API 受付
```

```text
mlflow_run_id
- 採番者: MLflow
- 対象: MLflow Run
- 主な使用場面:
  - Local CLI の科学計算
  - Web Worker が実処理を開始する時点
```

名前空間不明の `run_id` を、共通モデル、Manifest、Execution Plan またはログへ新規追加しない。

## 9.3 Web 実行

```text
origin = WEB
execution_id = Ariadne が採番
primary_namespace = ARIADNE
primary_id = execution_id
```

実処理を行う Execution Mode では、Worker が処理開始時に MLflow Run を作成または ensure し、`mlflow_run_id` を Execution へ関連付ける。

API 受付時点では、原則として MLflow Run を作成しない。

## 9.4 DRY_RUN および VALIDATE_ONLY

Web/API 経由では Ariadne Execution として記録してよいが、原則として MLflow Run を作成しない。

```text
execution_id:
作成する

mlflow_run_id:
None

mlflow_tracking_status:
NOT_REQUIRED
```

## 9.5 Local CLI

Local CLI は、Ariadne Control Plane による Execution 管理を行わない限り、Ariadne Execution を作成しない。

```text
origin = CLI
execution_id = None
```

MLflow が有効な場合:

```text
mlflow_run_id = MLflow が採番
primary_namespace = MLFLOW
primary_id = mlflow_run_id
```

MLflow が無効な場合:

```text
mlflow_run_id = None
primary_namespace = NONE
primary_id = None
```

Local CLI において、擬似的な Ariadne `execution_id` または擬似的な `mlflow_run_id` を生成してはならない。

CLI に `execution_id` が存在しないこと自体は、Ariadne の破綻を意味しない。

---

# 10. Execution Identity

Execution Identity は、Web 実行と CLI 実行の識別 context を、名前空間とともに保持する共通概念である。

```text
ExecutionIdentity
├── origin
├── execution_id
├── mlflow_run_id
├── primary_namespace
└── primary_id
```

Web 実行:

```text
origin = WEB
execution_id = required
primary_namespace = ARIADNE
primary_id = execution_id
```

CLI 実行:

```text
origin = CLI
execution_id = None
```

Execution Identity は、Web と CLI へ同じ ID を強制するための型ではない。

異なる実行 context の Identity 名前空間を明示し、名前空間不明の ID を共通処理へ持ち込まないための型である。

---

# 11. 概念モデル

```text
Project
  │
  ├── Research Topic
  │
  ├── Research Context
  │     ├── Problem Statement
  │     ├── Research Question
  │     ├── Significance
  │     └── Hypothesis
  │
  ├── Analysis Specifications
  │     ├── Discovery Configuration
  │     ├── Causal Design
  │     ├── ML Training Specification
  │     ├── Evaluation Specification
  │     └── Explainability Specification
  │
  ├── Execution Plans
  │     │
  │     └── Executions
  │           ├── Stage Executions
  │           │     └── Stage Attempts
  │           ├── Events
  │           ├── Artifacts
  │           ├── Results
  │           └── MLflow Run binding
  │
  └── Claims
        └── supported or challenged by Results
```

---

# 12. SPEC-001 の正本仕様候補

## 12.1 Execution

> Execution は、Project 内で、受付時に固定された Execution Plan に基づいて Ariadne が受け付け、管理する、一回の非同期処理要求とそのライフサイクルを表す。

## 12.2 execution_id

> `execution_id` は、Execution を一意に識別する Ariadne 固有 ID である。

> `execution_id` は、Project、要求者、認可、冪等性、Execution Plan、Queue、Stage Execution、Stage Attempt、Event、状態、cancel、retry、Artifact、Result、Audit および MLflow Run との対応を、同一 Execution の情報として関連付ける。

> `execution_id` は、Execution Plan そのもの、Research Question、Hypothesis、Analysis Specification、Result、Artifact、Claim または MLflow Run を識別する ID ではない。

## 12.3 Execution Plan

> Execution Plan は、1回の処理で使用する Research Context、Input Version、Analysis Specification、Algorithm、Parameter、Runtime 条件、Stage 構成および Input/Output contract を固定した不変の計画である。

## 12.4 Research Context

> Research Context は、Problem Statement、Research Question、Significance および Hypothesis から構成される。

> Research Context の構成要素は、分析の成熟度に応じて未定義または Draft でよい。

> Ariadne は、曖昧な Research Context から分析を開始することを許容する。ただし、Result を根拠として Claim を確定する段階では、Research Question、Significance、適用範囲、根拠および限界を明示する。

## 12.5 Analysis Domain からの独立

> Execution および `execution_id` は、因果分析、機械学習、説明可能 AI 等の特定の Analysis Domain へ依存しない。

> Causal Design、ML Training Specification、Evaluation Specification および Explainability Specification は、各 Execution が必要に応じて参照するドメイン固有の Analysis Specification であり、Execution Identity の構成要素ではない。

## 12.6 MLflow Run との分離

> Ariadne Execution は、Ariadne 固有の処理要求およびオーケストレーションを管理する。

> MLflow Run は、科学的・分析的な計算実行を追跡する。

> `execution_id` と `mlflow_run_id` は異なる名前空間に属し、相互に代用しない。

## 12.7 CLI

> Local CLI は、Ariadne Control Plane による Execution 管理を行わない限り、Ariadne Execution を作成せず、`execution_id` を持たない。

> MLflow 有効時の CLI では、科学計算の主 ID として `mlflow_run_id` を使用する。

> MLflow 無効時は、擬似的な `execution_id` または `mlflow_run_id` を生成しない。

---

# 13. 未決事項

1. Execution Plan に独立した `execution_plan_id` を付与するか
2. Execution Plan と Execution を1対1とするか、1対多とするか
3. Research Context を独立 Resource および Version として管理するか
4. Research Question、Significance、Hypothesis の状態遷移
5. Hypothesis role の正式な値
6. Analysis Domain と Operation の分類
7. 同一条件の再実行を表す relation
8. 技術的 retry と科学的 replication の relation 名称
9. Result と Artifact の多重度
10. Claim の作成、review、accept、supersede の状態遷移
11. Claim を人間のみが確定できるか
12. Local CLI の Research Context binding 方式
13. `experiments/` および `notebooks/` 配下の Experiment Definition 仕様
14. MLflow 無効時における CLI 実行の検索可能性
15. Web Execution と CLI Run を同一 Research Context へ関連付ける方法

---

# 14. 要約

```text
Project
= 1つの Research Topic を管理する境界
```

```text
Research Context
= なぜ、何を明らかにしようとしているか

Problem Statement
+ Research Question
+ Significance
+ Hypothesis
```

```text
Analysis Specification
= 何を、どの方法、仮定および評価基準で分析するか
```

```text
Execution Plan
= 今回の処理で使用する入力、仕様、method、
  runtime、Stage および出力契約を固定した不変の計画
```

```text
Execution
= Execution Plan を遂行する、
  Ariadne 上の一回の処理要求とそのライフサイクル
```

```text
execution_id
= Execution を一意に識別する Ariadne 固有 ID
```

```text
Result
= Execution によって得られた分析上の結果
```

```text
Artifact
= Result を構成または裏付ける物理的生成物
```

```text
Claim
= Result を根拠として人間が提示する、
  Research Question への範囲、仮定および限界付きの回答
```

Ariadne における `execution_id` は、分析の意味、Research Question または Execution Plan そのものを表す ID ではない。

`execution_id` は、固定された Execution Plan を Ariadne の管理下で遂行する、一回の処理要求とそのライフサイクルを識別する ID である。
