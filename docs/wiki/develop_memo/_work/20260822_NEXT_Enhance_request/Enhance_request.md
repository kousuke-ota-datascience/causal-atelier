# 0. INTRODUCTION

Information Architecture

```text
Ariadne
│
├─ Project Management
│
│   ├─ Project List
│   │
│   └─ Selected Project
│       ├─ Overview / Project Info
│       ├─ Research Context
│       ├─ Data
│       └─ Results / Lineage
│
└─ Analysis Workspace
    │
    ├─ Analysis Context
    │   ├─ Current Project
    │   ├─ Active Research Context
    │   ├─ Dataset Version
    │   └─ Analysis View
    │
    └─ Analysis
        ├─ Exploratory
        │   └─ Stage
        ├─ Causal
        │   └─ Stage
        └─ Predictive
            └─ Stage
```


# 1. Project Management
## 1.1. Project List
## 1.2. Selected Project
### 1.2.1. Overview / Project Info
### 1.2.2. Research Context
### 1.2.3. Data

- `Saved Analysis Views` に対して、設定した値を確認できるように [表示] ボタンがほしい 
    - 表示形式、挙動は下記画面と同様
        - `Research Context` > 'Version history' > [表示]

### 1.2.4. Results / Lineage

# 2. Analysis Workspace
## 2.1. Analysis Context
### 2.1.1. Current Project
### 2.1.2. Active Research Context

- ツールチップがない

### 2.1.3. Dataset Version
### 2.1.4. Analysis View



## 2.2. Analysis
### 2.2.1. Exploratory
#### 2.2.1.x. Exploratory-Stage
### 2.2.2. Causal

#### 2.2.2.1. setup

- `Setup` の段階で、 Discovery の結果のグラフを要求されるのは変。必須入力項目でないならば、その旨を記載する
- setupに入力項目を入れなくても、discoveryができるならば、その存在意義が疑問

#### 2.2.2.2. Discovery

- 名称未定領域（アルゴリズム設定→因果探索計算実行領域）
    - 本領域にタイトルをつけること
    - 入力用ツールチップがない
        - 'Objective'
            - ツールチップの文言例: 今回の因果探索で達成したい分析目的を書きます
            - 入力値の例: `coupon、visits、sales間の妥当な因果構造候補を探索する。`
        - 'Rationale'
            - ツールチップの文言例: なぜその探索条件を選んだのかを記載します
            - 入力値の例: `アルゴリズム依存性を確認するためPCとGESを比較する。また、条件付き独立性検定の閾値に対する感度を確認するため、PCはalpha=0.01と0.05で比較する。`
    - [複数Executionを受付]ボタンを押下した後の、画面上の変化がなく実行したかどうかの手応えがない。

- `Graph Candidates` 
    - 表示がはみ出る
    - 一括選択/選択解除のボタンがほしい

- 複数グラフの比較用モーダル画面: `Graph Comparison`
    - 現在選択している探索結果=グラフをハイライトする機能がほしい
    - 選択している探索結果=グラフの簡易な説明文を、[選択対象の探索結果リスト]と[DAG=グラフ]の間に入れてほしい。最大で3行程度の簡素なもので良いが、以下は含めてほしい
        - アルゴリズム
        - 設定パラメータ（現時点ではPCアルゴリズムのalpha）

- Graphを確認/編集するモーダル画面: `Graphを確認/編集する`
    - `Algorithm Outputを採用` を押下した際に以下のメセージが表示されるのがモーダル画面ではなく、本画面なので、ボタンを押した結果が分かりづらい
        - `Algorithm Outputを変更せずDISCOVERED FIXED Versionとして採用しました`
    - グラフのエクスポート機能がほしい。出力形式はマーメイド図の markdown source code 

#### 2.2.2.3. Identification

- `Causal Analysis`
    - Identification
        - `Population`, `Comparator`, にToolchipがない。何を入力したら良いのかがわからない。少なくとも表 2.2.2.3-01のような入力インストラクションがあると良い
        - 'Treatment' について、`Discovery` > `OUtcome` と同様にドロップダウンで選択可能にする。いちいち項目名を覚えている使用者はいない

表 2.2.2.3-01
| 項目                          | 必須か         | 入力する値                                        | 因果推論上の意味                                                    |
| --------------------------- | ----------- | -------------------------------------------- | ----------------------------------------------------------- |
| **Dataset**                 | **必須**      | 分析対象のDataset Version                         | 因果効果を識別・推定する観測データ。                                          |
| **FIXED Graph**             | **必須**      | 固定済み因果Graph                                  | 因果構造の仮定。調整変数や識別可能性を決める根拠。                                   |
| **Analysis mode**           | **必須※**     | `EXPLORATORY` / `CONFIRMATORY`               | 探索的分析か確認的分析かを区別する。※UIでは既定値あり。                               |
| **Population**              | **必須**      | 効果を知りたい対象集団。例: `2026年7月時点の会員顧客`              | **Target population**。誰に対する因果効果なのかを定義する。                    |
| **Comparator**              | **必須**      | Treatmentの比較対象。例: `クーポン非配布`                  | 反実仮想上の基準状態。通常 (A=0) に対応する。                                  |
| **Treatment**               | **必須**      | Treatment列名。例: `coupon_received`             | 介入・曝露 (A)。                                                  |
| **Outcome**                 | **必須・入力不要** | FIXED Graphから自動継承                            | 結果変数 (Y)。GraphにOutcomeがなければIdentificationを実行できない。           |
| **Analysis unit**           | **必須**      | `customer`, `household`, `store` など          | 因果効果を定義する単位。potential outcome (Y_i(a)) の (i)。               |
| **Treatment time**          | **必須**      | 介入時点。例: `coupon_issue_date`                  | **time zero**。Treatment前後を区別する基準。                           |
| **Outcome window**          | **必須**      | 例: `Treatment後30日`                           | どの期間のOutcomeに対する効果を評価するかを定義する。                              |
| **Estimand**                | **必須※**     | `ATE` / `ATT`                                | 求める因果効果の種類。※UIでは既定値あり。                                      |
| **Identification strategy** | **必須※**     | `BACKDOOR` / `RANDOMIZED`                    | 因果効果を観測データから識別する論理。※UIでは既定値あり。                              |
| **Adjustment set**          | 条件付き必須      | 交絡調整する列。例: `age,past_sales`                  | Backdoor経路を遮断するpre-treatment covariates。`RANDOMIZED`なら通常不要。 |
| **Assumptions**             | 任意※         | 例: `No unmeasured confounding`, `Positivity` | 識別を正当化する科学的仮定。※UI上は任意だが、**因果推論としては明示を強く推奨**。                |


#### 2.2.2.4. Estimation

- `Causal Analysis`
    - 全般
        - Estimation 他、このセクション内の項目が横方向に展開されるせいで非常に見づらくなっている。縦方向に項目を並べるというのがENH-E9での指示だったはずだが修正されていない


### 2.2.3. Predictive
#### 2.2.3.x. Predictive-Stage
