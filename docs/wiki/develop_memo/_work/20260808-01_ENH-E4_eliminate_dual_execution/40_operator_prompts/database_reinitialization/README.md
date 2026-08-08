# Database Reinitialization Operator Runbook

## 1. Purpose

このディレクトリは、`ENH-E4 eliminate dual execution` の一環として実施する **開発環境データベース完全初期化**について、以下をGit管理下に記録するためのものである。

1. 人間がAgentへ渡した実行指示
2. 実際に実行されたコマンド
3. 各コマンドの exit code
4. 各コマンドの stdout / stderr
5. 前段階の結果を根拠として確定した次段階の操作

この作業は通常の Coding Agent / Test Agent による実装作業とは異なり、**人間主導の逐次オペレーション**として扱う。

---

## 2. Positioning

親ディレクトリ `40_operator_prompts/` は、通常、Agentへ渡す最小入口プロンプトを管理する。

本ディレクトリはその通常用途とは分離し、DB初期化のような破壊的オペレーションについて、

> prompt → execution → result → human review → next prompt

の対応関係を明示的に残すための専用領域とする。

ここに通常のCoding Agent向け作業契約を複製しない。

---

## 3. Operating Principle

この作業では、Agentによる推論・探索・判断を可能な限り行わせない。

目的は以下。

* AIクレジット消費を抑える
* 実際に実行された操作を人間が後から追跡可能にする
* 破壊的操作の判断主体を人間側に置く
* 実環境で確認済みのコマンド列を最終的なrunbookとして残す

Agentの役割は原則として、

> **指定されたコマンドを、そのまま実行し、その結果を指定されたファイルへ記録すること**

だけとする。

---

## 4. Prohibited Agent Behavior

各promptに明示的な指示がない限り、Agentは以下を行ってはならない。

* 独自の追加調査
* コードベース全体の探索
* 実行方法の選択
* 代替コマンドの選択
* エラー原因の推論
* エラー回避策の自動実行
* retry
* migration
* database reset
* container / volume の削除
* ファイル変更
* ソースコード変更
* 設定変更
* promptに存在しないコマンドの実行

コマンドが失敗した場合も、Agent自身で修正操作を行わない。

**exit code と出力を記録し、そのphaseを終了する。**

---

## 5. Human / Agent Responsibility Boundary

### Human / ChatGPT

以下を担当する。

1. 前phaseのresultを確認する
2. 事実と未確定事項を整理する
3. 次に必要な操作を決定する
4. 実行コマンドを固定する
5. 次phaseのpromptを作成する
6. 破壊的操作の対象を確定する

### Agent

以下だけを担当する。

1. 指定されたpromptを読む
2. 指定されたコマンドブロックを実行する
3. 指定されたresultファイルを生成する
4. 実行終了後に停止する

---

## 6. Prompt / Result Pair

各phaseは、原則として以下の2ファイルで構成する。

```text
NN_<phase>_prompt.md
NN_<phase>_result.md
```

例:

```text
01_environment_inventory_prompt.md
01_environment_inventory_result.md
```

### `*_prompt.md`

実行前に人間側で確定した作業指示。

以下を含む。

* phaseの目的
* 実行可能な操作
* 禁止操作
* 実行する固定コマンド
* resultファイルの出力先
* Agentの終了条件

### `*_result.md`

実際の実行記録。

以下を含む。

* promptファイル
* 実行日時
* 各コマンド
* 各exit code
* stdout / stderr

resultには原則としてAgentによる考察・解釈・提案を書かない。

---

## 7. Phase Model

DB完全初期化は以下のphaseに分割する。

```text
01_environment_inventory
        |
        v
02_database_configuration
        |
        v
03_pre_reset_state
        |
        v
04_reset
        |
        v
05_rebuild
        |
        v
06_post_reset_verification
```

---

## 8. Phase Definitions

### 01_environment_inventory

**read-only**

repositoryとDB関連構成物の所在を確認する。

主な確認対象:

* repository root
* branch
* working tree
* Docker / Compose関連ファイル
* environment fileの所在
* dependency / migration設定ファイル
* migration directory
* DB関連設定を含むファイルの所在

DBには接続しない。

---

### 02_database_configuration

**read-only**

Phase 01で特定されたファイルのうち、必要なものだけを確認する。

目的:

* DB種別
* DB接続方式
* container / service
* database name
* volume
* ORM
* migration framework
* migration command

を確定する。

Phase 01の結果を確認するまでコマンドは確定しない。

---

### 03_pre_reset_state

**read-only**

実DBの削除前状態を確認する。

目的:

* 実際の接続対象
* migration state
* schema / table
* record state
* 永続volume

を確認し、Phase 04で削除する対象を確定する。

---

### 04_reset

**destructive**

既存データを削除する。

このphaseでは、Phase 01〜03の結果から人間側で完全に確定した破壊的コマンドのみを実行する。

Agent自身にreset方法を選択させない。

---

### 05_rebuild

DBを現在のコードベースが期待する初期状態へ再構築する。

必要に応じて以下を実施する。

* DB起動
* schema再構築
* migration
* 必須seed

具体的操作は前phaseの結果を確認してから固定する。

---

### 06_post_reset_verification

原則 **read-only**。

以下を確認する。

* migration state
* schema / table
* record state
* application DB connection
* 必要なread/write
* 必要なtest

この結果をもってDB初期化作業の完了可否を人間が判断する。

---

## 9. Sequential Gate

次phaseのpromptを事前に推測して作成しない。

必ず、

```text
Phase N prompt
    |
    v
Agent execution
    |
    v
Phase N result
    |
    v
Human review
    |
    v
Phase N+1 prompt
```

の順序で進める。

前phaseのresultが確認されていない状態で、次の破壊的操作へ進まない。

---

## 10. Result as Primary Record

チャットログではなく、このディレクトリ内の `*_prompt.md` / `*_result.md` を作業記録の一次資料とする。

チャットへresultを貼り付けて検討する場合も、Git管理下のresultファイルを正とする。

---

## 11. Secret Handling

resultファイルへ秘密情報を記録しない。

特に以下を直接出力しない。

* passwords
* API keys
* access tokens
* complete connection strings containing credentials
* `.env` の全面表示

必要な場合は、秘密値そのものではなく、

* 設定ファイルのpath
* variable name
* service name
* database name
* host category

など、操作確定に必要な最小情報だけを取得する。

---

## 12. Current Files

開始時点では以下を作成する。

```text
database_reinitialization/
├── README.md
└── 01_environment_inventory_prompt.md
```

Phase 01実行時に以下が生成される。

```text
01_environment_inventory_result.md
```

以降のpromptは、直前のresultを人間が確認した後に追加する。

---

## 13. Final Deliverable

全phase完了後、この一連のprompt / resultから、

> 実環境で実際に使用し、成功したDB完全初期化コマンド列

を抽出できる状態を完成条件とする。

推測に基づく手順ではなく、実行記録に基づく再現可能なrunbookを残す。
