# Enhance構想・要件改定計画

- 作成日: 2026-08-06
- 対象システム: Ariadne 初期価値検証版
- 対象リポジトリ: `kousuke-ota-datascience/causal-atelier`
- 対象ブランチ: `prototype/ariadne_mvp`
- 基準コミット: `538daebcee888722b245cb887bdfc8ec86d827c6`
- 改定識別子: `ENH-E2`
- 改定名称: 操作・状態連動型UIおよびGraph操作統合
- 改善要望正本: `docs/wiki/develop_memo/_work/20260806-02_bug_and_improvement/bug_and_improvement.md`
- 文書状態: 承認対象

> **要件定義書は常にシステムの正本である。**
>
> **実装、既存コード、DBスキーマ、API、UIまたはテスト結果から要件を逆生成・事後更新してはならない。**

## 1. 要件定義書正本原則

### 1.1. 正本の定義

ENH-E2では、次の順序を維持する。

```text
改善要望
→ Enhance構想
→ 要件定義
→ 論理データ設計
→ プロダクト基本設計
→ API・インターフェース設計
→ 詳細設計
→ 実装指示
→ 実装
→ 検証
```

既存コードはAs-Isの制約および変更対象を把握する資料であり、To-Be要件の根拠ではない。

### 1.2. 基準文書

ENH-E2の改定元は次の文書群とする。

- `00_プロダクトコンセプトメモ.md`
- `10_要件定義.md`
- `21_論理データ設計.md`
- `22_プロダクト基本設計.md`
- `23_API・インターフェース設計.md`
- `30_詳細設計.md`
- `31_ENH-E1a_設計追補.md`

`31_ENH-E1a_設計追補.md`はENH-E2改訂時に`30_詳細設計.md`へ統合し、改訂後の正本文書群では独立文書として残さない。

## 2. 改定の背景

### 2.1. 現状

現行MVPは、Project、Dataset Version、Discovery、Graph Version、Inference、ResultおよびLineageを一続きに操作できる。一方、画面構造は実装機能を直接並べた状態に近く、利用者が次を判断しにくい。

- 各ページ・セクションで何を行うか
- 専門用語が何を意味するか
- どのデータ状態でどの操作が可能か
- Discovery ResultとGraph Versionの違い
- FIXED Graphを編集したときに何が生成されるか
- Outcomeがどの段階で決まり、下流へどう引き継がれるか
- Project削除が分析来歴へ与える影響

### 2.2. 構造上の問題

現行基本設計は、画面項目と一部制約を列挙しているが、次の対応が全画面で統一されていない。

```text
利用者操作
→ 操作可能な前提状態
→ 参照する正本Entity
→ 新規生成または更新するEntity
→ 操作後状態
→ 画面上の有効・無効・read-only表示
→ 拒否時の挙動
```

この不足はParent Graphに限らず、Project、Dataset、Execution、Graph Version、Identification、Data Eligibility、ResultおよびAnnotationの全操作に影響する。

## 3. ENH-E2の目的

ENH-E2は、既存の科学的妥当性基盤を維持したまま、利用者の操作と正本データの状態遷移を明示的に接続する。

目的は次の4点である。

1. 画面の目的、専門用語、入力例および操作結果を理解可能にする
2. Project管理を分析画面から分離し、登録・一覧・削除を一箇所に集約する
3. Discovery Resultと派生Graph Versionを一つのGraph Candidate操作面に統合する
4. 基本設計書へ操作・前提状態・Entity生成更新・状態遷移・UI Gateを記載する

## 4. 対象範囲

### 4.1. 全画面共通

- ページトップへ目的と作業概要を表示する
- 全セクションへタイトルと説明を表示する
- 専門用語へ補足説明を付与する
- 入力項目へツールチップまたは入力例を提供する
- 操作可否を正本Entityの状態から導出する

### 4.2. Project Register & Management

- 新規管理画面を追加する
- Project登録をProject / Data画面から移管する
- ACTIVE Project一覧を表示する
- Project削除操作を提供する
- 画面上の削除は`ACTIVE → ARCHIVED`の論理削除とする
- ARCHIVED Projectは通常選択および新規操作の対象外とし、既存Lineageは保持する

### 4.3. Project / Data

- 選択中Projectの情報編集に責務を限定する
- Dataset RegisterとRegistered Datasetsを明示的に分離する
- ページ文言を利用目的が分かる表現へ改める

### 4.4. Discovery

- Feature columnsをDataset schemaから選択できるモーダルを追加する
- テキスト入力と選択モーダルの同期規則を定義する
- OutcomeをDataset列から選択する
- OutcomeをDiscovery Execution SnapshotおよびGraph Versionへ引き継ぐ
- DAG表示ではdesignated outcome nodeを可能な限り右端に配置する

### 4.5. Graph Results

- Discovery Graph ResultとGraph Versionを統合表示する
- 子Graph Versionを含めたGraph Candidate一覧を提供する
- FIXEDフラグ、親情報、status、summaryを表示する
- DAG確認・編集をモーダルへ統合する
- 独立したGraph Version editorセクションを廃止する
- 2件以上のGraph Candidateを比較できるモーダルを提供する
- 比較結果を生JSONだけで表示しない

### 4.6. Inference

- IdentificationおよびData Eligibilityの説明を表示する
- 各入力項目へツールチップと入力例を付与する
- Outcome入力欄を廃止する
- FIXED Graph Versionのdesignated outcomeをread-onlyで継承する
- Graph VersionのOutcomeとInference SnapshotのOutcome不一致を拒否する

### 4.7. 文書改定

- `00`、`10`、`21`、`22`、`23`、`30`をENH-E2統合改定する
- `31_ENH-E1a_設計追補.md`の内容を`30_詳細設計.md`へ統合する
- `22_プロダクト基本設計.md`を操作・状態境界中心に再構成する

## 5. 主要設計判断

### 5.1. 主要Entityを増やさない

ENH-E2では既存7 Entityを維持する。

```text
Project
Dataset Version
Execution
Result
Artifact
Graph Version
Annotation
```

Graph Candidate一覧、Graph比較およびモーダル状態はQuery ModelまたはUI状態として扱い、正本Entityを追加しない。

### 5.2. Project削除は論理削除とする

Project、Dataset Version、Execution、ResultおよびGraph Versionは分析来歴の正本である。したがって、UI上の削除操作はProjectの`status`を`ARCHIVED`へ変更する。

- hard deleteは実施しない
- ARCHIVED Projectへの新規Dataset登録、Execution作成、Graph作成およびAnnotation更新を拒否する
- 既存ResultおよびLineageはread-onlyで参照可能とする
- ENH-E2では復元UIを対象外とする

### 5.3. OutcomeはGraph Versionへ継承する

Outcomeは単なる表示順序ではなく、Inferenceで使用するCausal Questionの必須要素である。Discovery画面で選択したOutcomeを次の経路で保持する。

```text
Discovery Analysis Spec
→ Discovery Graph Result
→ Graph Version.designated_outcome_node
→ Inference Causal Question Outcome
```

DRAFT Graph Versionでは未指定を許容できるが、Inference入力に使用するFIXED Graph Versionでは必須とする。

### 5.4. Graph ResultsはQuery Projectionとする

Discovery ResultとGraph Versionは異なる正本Entityであるため、同一テーブルへ物理統合しない。`GraphCandidateView`として要求時に統合する。

### 5.5. Algorithm Outputを上書きしない

Discovery ResultのGraphを直接編集してAlgorithm Outputとして保存してはならない。

- Discovery Resultはread-only
- 未編集採用は`DISCOVERED` Graph Versionを生成する
- 編集は固定済みGraph Versionを親とする新しいDRAFTを生成する
- FIX操作はDRAFTをFIXEDへ遷移させる操作であり、新Version生成操作ではない

### 5.6. 操作・状態境界を基本設計へ記載する

各主要操作について次を必須記載項目とする。

| 項目 | 定義内容 |
|---|---|
| 操作 | 利用者が要求する処理 |
| 前提状態 | 操作可能なEntity statusおよび参照条件 |
| 読取対象 | 操作判断に使用する正本情報 |
| 生成対象 | 新規作成するEntity |
| 更新対象 | 更新可能なEntityと属性 |
| 操作後状態 | 正常完了後の状態 |
| UI Gate | enabled / disabled / read-only / hidden |
| 拒否結果 | 状態不整合時の表示とerror |

## 6. 非対象

- Projectの物理削除
- ARCHIVED Projectの復元UI
- 複数Outcomeを同時に管理するGraph Version
- 新しい主要EntityまたはGraph Candidate Table
- 汎用Workflow Designer
- Graph layout engineの製品固定
- 詳細RBACおよび承認Workflow
- Algorithm Outputの直接編集
- CPDAG / PAGの暗黙DAG変換
- Inference画面でのOutcome上書き

## 7. 成果物

### 7.1. Enhance計画文書

1. `01_Enhance構想・要件改定計画.md`
2. `02_Enhance構想承認記録.md`
3. `03_要件定義書改定.md`
4. `04_設計書改定.md`
5. `05_要件・設計整合性およびトレーサビリティ確認.md`
6. `06_Ariadne_ENH-E2_実装指示書.md`

### 7.2. 改訂版要件・設計文書

1. `00_プロダクトコンセプトメモ.md`
2. `10_要件定義.md`
3. `21_論理データ設計.md`
4. `22_プロダクト基本設計.md`
5. `23_API・インターフェース設計.md`
6. `30_詳細設計.md`

`31_ENH-E1a_設計追補.md`は出力しない。内容は`30_詳細設計.md`へ統合する。

既存の`07_ariadne_ENH-E1_実施状況監査報告書.md`および`08_ariadne_ENH-E1a_再実装ならびに再テスト指示書.md`に相当する文書は、実装後の監査または是正が発生した場合に作成する後続成果物であり、ENH-E2計画策定時点の成果物には含めない。

## 8. 実施順序

```text
WP-DOC-1 改善要望の要求化
→ WP-DOC-2 概念・要件改定
→ WP-DOC-3 論理データ設計改定
→ WP-DOC-4 基本設計の操作・状態境界化
→ WP-DOC-5 API・詳細設計改定
→ WP-DOC-6 31設計追補の30への統合
→ WP-DOC-7 トレーサビリティ確認
→ WP-DOC-8 実装指示書確定
```

## 9. リスクと対策

| リスク | 影響 | 対策 |
|---|---|---|
| Project削除をhard deleteとして実装する | Lineage破壊 | `ARCHIVED`への状態遷移としてAPI・Domain・UIを統一する |
| OutcomeをUI状態だけで保持する | 再読込時に消失、Inference不整合 | Discovery SnapshotとGraph Versionへ永続化する |
| ResultとGraph Versionを同一Entity扱いする | Provenance破壊 | Query Projectionのみ統合する |
| FIXED Graphを直接更新する | 再現性破壊 | DRAFT / FIXED Gateと子Version生成をDomainで強制する |
| UIだけで操作を禁止する | API直接利用で不変条件を破る | Application ServiceおよびDomainでも検証する |
| Graph比較をJSON表示で済ませる | 利用者が差分を解釈できない | DAG表示、タブ、構造差分summaryを提供する |

## 10. 完了条件

- 改善要望の全項目が要件IDへ対応している
- Project削除、Outcome継承、Graph Candidate統合およびGraph編集の意味論が一意である
- 全主要画面に操作・状態対応表がある
- `31_ENH-E1a_設計追補.md`の全内容が`30_詳細設計.md`へ統合されている
- 7 Entity原則と不変性原則を維持している
- API、データ、基本設計および詳細設計に矛盾がない
- 実装指示書が改訂後正本のみから導出されている
