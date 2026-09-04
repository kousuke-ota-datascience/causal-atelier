Document title: 分析実装の基本方針とAriadneの位置づけ

# 28. Slide 28｜分析実装の基本方針とAriadneの位置づけ

## 28.1. Message

**分析はデータサイエンティストがScratch＋成熟OSSで実装し、Ariadneは分析過程の構造化・追跡を補助する。**

## 28.2. Chart

**チャートタイトル:** 分析サービスを担う主体・実装手段・Ariadneの役割分担

Data Scientistを分析品質の主体、Scratch＋成熟OSSを案件固有の分析を実現する実装手段、Ariadneを必要に応じて分析過程を構造化・追跡する補助層として分離して示す。

### 28.2.1. Chart Structure

主チャートは、中央の「分析サービス本体」と、その下を支える「Ariadne（案件に応じて）」および「お客様のData / Compute環境」で構成する。

```text
Business / Analysis Question
            ↓
┌──────────────────────────────────────────────┐
│ 分析サービス本体                              │
│                                              │
│ Data Scientist                              │
│ 問い定義 → 分析設計 → 実装 → 検証 → 解釈      │
│                  ↓                           │
│          Scratch + 成熟OSS                   │
│      案件固有の要件に合わせて構成             │
└──────────────────────────────────────────────┘
            ↓
Evidence / Decisionへの接続

┌──────────────────────────────────────────────┐
│ Ariadne（案件に応じて利用）                   │
│ Context / Input・条件 / Execution / Result   │
│ 判断・Lineageの構造化・追跡を補助             │
└──────────────────────────────────────────────┘
            ↕
┌──────────────────────────────────────────────┐
│ お客様のData / Compute環境                    │
└──────────────────────────────────────────────┘
```

**PowerPoint上の配置・強調**

- 中央の「分析サービス本体」を最大の視覚ウェイトとし、Data Scientistを主語として見せる。
- Scratch＋成熟OSSはData Scientistが案件要件に応じて選択・構成する実装手段として、Data Scientistの下位に配置する。
- Ariadneは主フローへ直列に挿入せず、下段の補助レールとして配置する。`案件に応じて利用` を明示し、PoCの必須条件や分析Engineに見せない。
- 最下段にお客様のData / Compute環境を置き、既存環境と併存する位置づけを示す。
- Ariadneの機能名や対応Algorithmを多数列挙せず、何を構造化・追跡するかだけを表示する。

### 28.2.2. Chart内の最小表示テキスト

- Business / Analysis Question
- **Data Scientist**
- 問い定義・分析設計・実装・検証・解釈
- **Scratch + 成熟OSS**
- 案件固有の要件に合わせて構成
- Evidence / Decisionへの接続
- **Ariadne（案件に応じて利用）**
- Context / Input・条件 / Execution / Result / 判断 / Lineage
- 構造化・追跡を補助
- お客様のData / Compute環境

## 28.3. Supporting Logic

### 28.3.1. 分析品質を担う主体

- サービスの分析品質は、特定ProductやAlgorithmそのものではなく、Data ScientistがBusiness / Analysis Question、成立条件、検証方法、結果の解釈を一貫して設計できることによって担保する。
- PredictiveではPrediction Question、未知データでのValidation、Failure / Utilityを、CausalではEstimand、Assumptions、Identification、Diagnostics / Sensitivityを分析目的に応じて設計する。
- 分析結果はModel / Estimateで閉じず、前Sectionまでに整理したEvidenceをDecision / Actionへ接続する。

### 28.3.2. Scratch＋成熟OSSの位置づけ

- 案件固有のData Structure、Outcome / Treatment、Evaluation、運用制約等へ対応するため、Python等によるScratch Developmentを基本とする。
- 統計・機械学習・因果推論については、成熟したOSS / Libraryを目的と成立条件に応じて選択し、必要な実装を組み合わせる。
- 顧客課題を特定Product、単一Model Family、固定Workflowへ合わせるのではなく、Questionと成立条件から実装を決める。

### 28.3.3. Ariadneの位置づけ

- Ariadneの要件上の対象には、Research Context、versioned analysis input、Analysis Specification、Execution、Result / Artifact、分析時の判断・Annotation、これらのLineageが含まれる。
- したがって本資料では、Ariadneを**問い・入力・分析条件・実行・結果・判断の来歴を構造化し、追跡を補助する選択肢**として位置づける。
- 一方、現行要件には実装状態が `PARTIAL` の追跡・再現性項目もあるため、「分析プロセス全体の完全な再現性を保証する」等の表現は採用しない。
- AriadneはData ScientistによるQuestion Definition、Scientific Design、Validation、Interpretationを自動的に代替するものではない。

### 28.3.4. サービスScopeとの境界

- Ariadne利用はPoC成立の前提とせず、案件・お客様環境に応じて利用する。
- Ariadneの現時点の実装範囲と、Data ScientistがScratch＋成熟OSSで提供可能な分析サービスの範囲を同一視しない。
- AriadneのPredictive / Causal Capabilityに存在する手法数を、当チームのサービス対応範囲や差別化の根拠として扱わない。
- お客様の既存Data / Compute環境を置き換える前提ではなく、その環境と併存する補助手段として説明する。

## 28.4. Speaker Note

当チームのPoCは、Ariadneにお客様の課題を合わせる形ではありません。まず、何を知り、何を判断したいかを起点にData Scientistが分析を設計し、案件固有の要件に応じてScratch開発と成熟したOSSを組み合わせます。Ariadneは、案件によって必要な場合に、分析のContextや入力・条件、実行、結果、判断の来歴を整理し、後から追える形にするために利用します。そのため、Ariadneを利用しないPoCも成立しますし、現在Ariadneに実装されている分析手法の範囲が、当チームの分析サービス全体の対応範囲を決めるわけでもありません。

## 28.5. Slide 28からSlide 29への接続

> **実装手段はQuestionと成立条件に合わせて選ぶ。次に、この方針が実際のPoCでBusiness QuestionからAnalysis、Decision / Actionへどう落ちるかを、Predictiveの適用例で確認する。**
