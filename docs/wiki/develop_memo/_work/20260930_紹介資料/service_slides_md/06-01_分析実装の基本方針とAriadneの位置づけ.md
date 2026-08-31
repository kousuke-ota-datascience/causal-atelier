Document title: 分析実装の基本方針とAriadneの位置づけ

# 27. Slide 27｜分析実装の基本方針とAriadneの位置づけ

## 27.1. Message

**分析はデータサイエンティストのスクラッチ開発を基本とし、成熟OSSを適切に組み合わせ、Ariadneは分析プロセスの構造化・追跡を補助する。**

## 27.2. Chart

**チャートタイトル:** サービス実装の3層構造

Messageを説明・論証するための主たる視覚表現として、以下の構造を採用する。

### 27.2.1. Chart Structure

- 既存の論理フロー／概念図を主チャートとして用い、要素間の関係・順序が一目で追える構造にする。

```text
┌────────────────────────────┐
│ Data Scientist              │
│ 問い定義・分析設計・検証・解釈 │
├────────────────────────────┤
│ Scratch + OSS               │
│ Python / ML / Statistical / Causal libraries │
├────────────────────────────┤
│ Ariadne（案件に応じて）      │
│ Context / Workflow / Result / Lineage支援     │
└────────────────────────────┘
        ↕
お客様のData / Compute環境
```

**PowerPoint上の配置・強調**

- 3層スタック図を中央に置き、最上段のData Scientistを最も強調する。
- Ariadneは補助層として表現し、製品がサービスそのものに見えないようにする。
- 下部にCustomer Data / Computeを置く。

### 27.2.2. Chart内の最小表示テキスト

実際のPowerPoint上では、以下のラベル・短文を中心に表示する。Supporting Logicの全文をスライド上へ掲載しない。

- Data Scientist
- 問い定義・分析設計・検証・解釈
- Scratch + OSS
- Python / ML / Statistical / Causal libraries
- Ariadne（案件に応じて）
- Context / Workflow / Result / Lineage支援
- お客様のData / Compute環境

## 27.3. Supporting Logic

- スクラッチ実装：案件固有のデータ構造・要件・検証設計へ柔軟に対応する。
- OSS活用：統計・機械学習・因果推論の成熟ライブラリを目的に応じて選択する。
- Ariadne：Research Context、versioned input、Predictive / Causal workflow、結果・lineage等の追跡を支援する。
- Ariadne利用をPoC成立の前提にはせず、お客様の既存データ・計算基盤と併存可能な位置づけとする。

- 補足論点：**差別化の中心は独自アルゴリズム数ではなく、問い・前提・手法・検証・解釈を一貫して設計できるデータサイエンス能力に置く。**

## 27.4. Speaker Note

現状のAriadne実装範囲と、サービスとしてスクラッチで対応可能な分析範囲を混同しない。Ariadneは分析Workflow支援の選択肢として説明する。

## 27.5. Slide 27からSlide 28への接続

> **次に、予測PoCが業務課題からActionへどのようにつながるかを一つの適用例で示す。**
