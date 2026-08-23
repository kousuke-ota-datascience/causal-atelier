# 0. Ariadne Product Concept

## 0.1. Product Concept

> **分析の目的・前提・手法・実行・結果・解釈を一連の構造として保持し、「何を根拠に、どこまで主張できるか」を追跡可能にする分析基盤**

Ariadneでは、分析結果だけでなく、その前後にある判断・前提・実行・解釈までを一体として扱う。

> **分析を「結果」ではなく「検証可能なプロセス」として扱う**

---

## 0.2. 現行プロダクト構成

> **Ariadneの本質は分析プロセスの構造化であり、Exploratory / Predictive / Causalはその価値を具体化する現在の分析ファミリである**

| Analysis Family | 主な問い |
|---|---|
| **Exploratory** | 何が起きているのか？ |
| **Predictive** | 何が起こりそうか？ |
| **Causal** | 何をすると何が変わるか？ |

3つは共通の `Planning → Execution` モデル上で扱う。

> **一つのビジネス課題 / 問いを、探索・予測・因果という複数の観点から扱える**

---

# 1. Ariadneが解決する課題

## 1.1. 分析プロセスの分断

> **分析業務の本質は「計算」だけではなく、その前後にある多数の判断にある**

実務では、分析を構成する情報が複数の場所や人に分散しやすい。

| 情報 | 存在する場所の例 |
|---|---|
| 分析コード | Notebook / Source Code |
| 前提・条件 | 文書 / PowerPoint |
| 議論・判断理由 | Slack / Email / Meeting |
| 結果・解釈 | Report / Presentation |
| 暗黙知 | 分析者の頭の中 |

その結果、後から以下を追跡しにくくなる。

- なぜその分析をしたのか
- どの前提に依存した結果か
- なぜその手法を選んだのか
- 他の分析者が再現・比較・再利用できるか
- どこまでを根拠として説明できるか

> **Ariadneでは、分析結果ではなく「分析プロセス」を管理単位とする**

---

# 2. Product Principles

## 2.1. 主張と前提

> **あらゆる分析結果から導かれる主張には、前提が伴う。強い主張には強い前提が伴う**

高い精度や強い結論だけをもって良い分析とは判断しない。

> **「この結果が正しい」ではなく、「この前提のもとでは、ここまで主張できる」と扱う**

---

## 2.2. Ariadneが価値を置く領域

> **分析アルゴリズム単体の性能競争を、Ariadneの主戦場にはしない**

scikit-learn、DoWhy、EconML等の成熟した既存技術を活用しつつ、Ariadneは以下に価値を置く。

| 既存技術を活用する領域 | Ariadneが価値を置く領域 |
|---|---|
| 統計・機械学習・因果推論アルゴリズム | ビジネス課題 / 問い、分析設計、前提管理 |
| 推定・予測・数値計算 | 比較・診断、結果解釈、根拠追跡 |

> **良いアルゴリズムをすべて自ら作るのではなく、適切に選び、検証し、解釈できる仕組みに価値を置く**

---

# 3. Analysis Workflow

## 3.1. Planning → Execution

> **Ariadneでは、分析を `Planning → Execution` の二段階で構造化する**

| Planning | Execution |
|---|---|
| ビジネス課題 / 問い | 分析処理の実行 |
| 分析上の問い | 実行結果 |
| 前提条件 | 診断結果 |
| 手法・実行計画 | 実行履歴 / Error / Metadata |

> **「何をする予定だったか」と「実際に何をしたか」を分離しつつ、相互に追跡する**

---

## 3.2. Workflowの拡張性

> **AriadneのWorkflowは、Exploratory / Predictive / Causalの3種類に限定されない**

中核は特定の統計手法ではなく `Planning → Execution` という実行モデルにある。

Planningで実行内容を記述し、Execution側の実装層を追加できれば、他の分析・計算処理もWorkflowへ組み込める。

> **Ariadneは「3種類の分析ツール」ではなく、Planning → Executionに適合する処理を拡張可能な分析Workflow基盤として設計されている**

---

# 4. System Positioning

## 4.1. Analysis ContextとExecutionの分離

> **Ariadne自身が、すべての分析計算を実行する必要はない**

既存のData Lake / Lakehouse / Analytics Platform / Databricks等でData・Code・Computeを保持・実行し、Ariadneはその上位でAnalysis Contextを管理できる。

| Ariadneが担う領域 | 既存基盤でも担える領域 |
|---|---|
| ビジネス課題 / 問い | データ処理 |
| 前提・分析設計 | SQL / Python / Spark実行 |
| Analysis Workflow | 統計・機械学習処理 |
| 実行履歴・結果との対応 | 計算資源 / Job Execution |
| 結果の解釈 | Data / Artifact保持 |

> **既存のData / Compute基盤と競合するのではなく、その上位で分析を構造化する**

---

## 4.2. Analysis Context / History

> **究極的には、Ariadne自身が分析を実行しなくても、分析の目的と履歴を保持できればよい**

Ariadneが保持するのは、

- なぜ分析したか
- 何を分析したか
- どの前提で実行したか
- 何を実行したか
- 何が得られたか
- 何を主張したか

というAnalysis Contextである。

> **Ariadneを「独自のAnalysis Engine」ではなく、Analysis Contextと履歴を管理するレイヤーとして位置づける**

---

# 5. Interfaces

## 5.1. Interface構成

> **同じAriadne Coreを、利用者・利用形態に応じて異なるInterfaceから利用する**

| Interface | 主な利用者 / 利用主体 | 主な用途 |
|---|---|---|
| **WebUI** | Analyst / Data Scientist / Reviewer / Consultant | 対話的分析、確認、PoC |
| **CLI / Codebase** | Engineer / SI担当者 | Script、Batch、SI組み込み |
| **Web API** | Application / Workflow Engine / AI Agent | Analysis Capabilityの呼び出し |

WebUIは人がAriadneを操作する入口であり、CLI / Web APIは他のSystem / SolutionへAriadneを組み込む入口となる。

> **Ariadneの価値はWebUIそのものではなく、その背後にあるAnalysis Model / Capabilityにある**

---

# 6. Productization

## 6.0. 商品化方針サマリ

> **既存の「再利用可能なSI Componentを商品化する」取り組みに合流しながら、WebUI / Web API / CLI・Codebaseの3方向で商品価値を検証・形成する**

Ariadneは既存の商品化活動とは別系統で立ち上がったため、社内で検討済みの商品化プロセスとの接続を重視する。

| 機能開発優先順位 | 外販商品化優先順位 | 対象 | 主な位置づけ |
|---:|---:|---|---|
| 1 | N/A (*1) | **WebUI** | 商談Demo / PoC / 社内利用 |
| 2 | 1 | **CLI / Codebase** | SI向け再利用可能Component |
| 3 (*2) | 2 | **Web API** | 外部System向けAnalysis Service |

(*1) WebUI単独での外販優先度は低いが、商談・PoC・社内Consultant利用による売上貢献とProduct Discoveryのため機能開発優先度は高い。

(*2) WebUI自体がWeb APIを利用するためAPI機能も並行して成熟する。優先度3は、Databricks等の外部Platformからの直接利用に向けた標準化・接続検証を指す。

---

## 6.1. Productization First Step

> **Planning → Executionモデルに基づき、予測・最適化などの分析処理を再利用可能なWorkflowとして実行・管理できるComponentを構築する**

First Stepとしてこれを選ぶ理由：

- 既存のSI Component商品化プロセスに合流しやすい
- チームのPredictive / Optimization Skillを直接活用できる
- 性質の異なる処理を同じFrameworkで扱うことで拡張性を検証できる
- 実案件で「本当に再利用されるか」を確認できる

| 処理 | Planning | Execution |
|---|---|---|
| **Predictive** | Target / Features / Model / Metrics | Train / Evaluate / Predict |
| **Optimization** | Objective / Variables / Constraints / Solver | Build / Solve / Evaluate |

> **「分析機能を増やす」のではなく、「次の案件でも再利用できるAriadne Component」を作る**

---

## 6.2. 3つの商品化対象

### WebUI

> **商談・PoC・社内Consultant利用を通じて、人が使うAriadneとしての価値を作り込む**

主な狙い：

- 顧客関心の喚起
- PoC実施の効率化
- PoC品質の平準化
- Consultant FeedbackによるUI / 分析支援機能の改善

主要Userは、専門Engineer / Data Scientistほどプログラミングに特化していない一方、仮説立案・顧客課題整理に長けたConsultantを想定する。

### CLI / Codebase

> **既存の商品化プロセスに最も直接的に合流するSI組み込み用Componentとして育てる**

共通化可能な分析処理・Planning / Execution構造・履歴管理をAriadne Componentとして再利用し、顧客固有部分のみ個別SIとする。

### Web API

> **既存Web APIを、顧客System / Application / 外部Platformから安定利用できるAnalysis Serviceへ成熟させる**

APIそのものは既にWebUIから利用している。今後はInput / Output、認証、Error Handling、外部接続、運用等を標準化・検証する。

---

## 6.3. Productization Path

> **SIでReusable Componentを育て、WebUIでUser-facingな価値を磨き、Web APIを外部利用可能なServiceへ成熟させる**

```text
                         ┌→ WebUI
                         │  商談 / PoC / 社内利用
                         │  ↓
                         │  UX / Analysis Support改善
                         │
SI Project ─→ Reusable Component
                         │
                         ├→ CLI / Codebase
                         │  他SI案件へ再利用
                         │
                         └→ Standardized Capability
                                    ↓
                               Web API
```

---

# 7. Go-To-Market

## 7.1. Product Core ValueとMarket Entry Point

> **Ariadneの本質的価値と、顧客が最初に購入する理由は一致しなくてよい**

| Product Core Value | 顧客が認識しやすい初期課題 |
|---|---|
| Analysis Processの構造化 | 分析工数が大きい |
| 前提の明示 | 品質が人に依存する |
| 根拠の追跡性 | レビューが難しい |
| 再現性 | 説明責任が重い |
| Analysis Contextの蓄積 | 同じ分析を何度も実装している |

> **Productとして目指す価値は維持しつつ、市場には具体的な業務課題から入る**

---

## 7.2. SIを活用したProduct Discovery

> **既存SI案件を、顧客価値と商品化可能性を検証する場として利用する**

```text
SI Project
    ↓
効果を測定
    ↓
Reusable Patternを抽出
    ↓
Component化
    ↓
Standardize
    ↓
Productize
```

> **SIそのものをゴールとせず、商品化できる共通部分を発見するために利用する**

---

## 7.3. 商品形態とCustomer Value

> **「何を売るか」と「なぜ顧客がお金を払うか」は分けて検証する**

| 商品として提供するもの | 顧客価値の仮説 |
|---|---|
| Web API | 分析工数削減 |
| SI組み込みComponent | 開発工数削減 |
| Analysis Capability | 高度分析の再利用 |
| Analysis Model / Workflow | 分析方法の標準化・レビュー容易性 |
| Analysis History | Governance / 説明責任 |

また、User / Integrator / Buyerを分けて検証する。

| Role | 想定例 | 主な関心 |
|---|---|---|
| User | Analyst / Data Scientist | 分析しやすいか |
| Integrator | SI Engineer / Developer | 組み込みやすいか |
| Buyer | Project Owner / Manager | 投資対効果があるか |

> **Pricingの前に、誰が・何に価値を感じるのかを検証する**

---

# Demonstration

## WebUI Demonstration

> **WebUIの見た目ではなく、背後にあるAriadneのAnalysis Modelを確認する**

確認ポイント：

- ビジネス課題 / 問いから分析が構造化されている
- Planning → ExecutionとしてWorkflowが表現される
- 結果だけでなく、目的・条件・前提を追える
- 同じAnalysis CapabilityをWeb API / CLIから利用できる
- Execution先をAriadne自身に限定しない

---

# Appendix A. Agent / MCP Integration

## A.1. Agent / Web API

> **Ariadneは既にWeb APIで主要機能を提供しているため、HTTP APIを呼び出せるAgentから現状でも利用可能な構成となっている**

Web APIはFastAPIベースで、Analysis Workflow / Execution / Result等を `/api/v1` 以下に提供する。

ただし現状はAgent専用Interfaceではなく、API選択、Input構築、認証、Execution状態確認等はAgent側で扱う必要がある。

> **現状でもAgentから呼び出し可能だが、Agent-nativeなTool Interfaceは今後の拡張領域**

---

## A.2. MCP Serverとの接続

> **AriadneはAnalysis CapabilityをWeb APIとして分離しているため、MCP Server追加との親和性が高い**

```text
AI Agent
   ↓
MCP Client / Server
   ↓
Ariadne Web API
   ↓
Planning → Execution
```

MCP対応ではCore Analysis機能を再実装せず、主に以下を追加する。

- MCP Tool Definition
- Tool InputとAPI InputのSchema Mapping
- Authentication伝播
- 非同期Execution / Result取得
- Error Mapping / Observability

> **MCP対応はCore機能の再実装ではなく薄いInterface Adapter追加が中心となるため、相対的に低工数で実現できると見込む**

---

# Appendix B. Ariadne開発で得られたもの

## B.1. 3つの成果

> **Ariadne開発では、「Product」「Productを動かすFramework」「Productを作るProcess」の3つの資産が得られた**

| Layer | 得られたもの | 再利用先 |
|---|---|---|
| **Product** | Ariadne Product | Ariadneの商品化 |
| **Framework** | Planning → Execution基盤 | 他の分析・計算Workflow |
| **Development Process** | Agentic Enhancement Workflow Template | 他Project / Product開発 |

### Ariadne Product

分析の目的・前提・手法・実行・結果・解釈を一体として管理するProduct本体。

### Planning → Execution基盤

PlanningとExecutionを分離し、異なる分析・計算処理を同じ上位構造で実行・管理するFramework。

現時点で完全な汎用Workflow Engineとしての商品化が完了しているわけではなく、Predictive / Optimization等の実案件適用を通じて再利用範囲を検証する。

### Agentic Enhancement Workflow Template

AI Agentによる設計・実装・独立検証を管理する開発Workflow。

```text
Enhancement Background
        ↓
Gate / Implementation Contract
        ↓
Coding Agent
        ↓
Implementation Evidence
        ↓
Independent Verification
        ↓
Gate Decision
```

> **Ariadne開発の成果はProduct本体に閉じず、今後の分析Solution開発・Software開発へ再利用可能な技術資産・開発資産を含んでいる**
