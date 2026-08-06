# Enhance構想承認記録

- 記録日: 2026-08-06
- 承認対象: `ENH-E2`
- 策定根拠: 本チャット上のProject OwnerによるENH-E2文書策定指示および2026-08-06 23:40 JSTの承認
- 改善要望・文書策定方針: 承認済み
- ENH-E2計画・要件・設計内容: Project Owner承認済み
- 実装開始状態: 未承認
- 本番リリース状態: 未承認

> **本記録は、ENH-E2の改善要望、文書策定方針、計画、要件および設計内容に対するProject Owner承認を記録する。実装開始および本番投入は別の承認対象であり、本承認には含めない。**

## 1. 承認対象

### 1.1. 計画識別子

```text
ENH-E2
```

### 1.2. 計画名称

```text
操作・状態連動型UIおよびGraph操作統合
```

### 1.3. 対象範囲

- 改善要望の要求化
- Enhance構想と要件定義の改定
- 論理データ、基本設計、APIおよび詳細設計の改定
- 操作と状態遷移の境界定義
- `31_ENH-E1a_設計追補.md`の`30_詳細設計.md`への統合
- 要件・設計トレーサビリティ確認
- 実装指示書作成

## 2. 改善要望および策定方針として承認済みの事項

1. 4つの分析Workspaceを維持し、Project Register & Managementを管理画面として追加する
2. Project登録をProject / Dataから管理画面へ移管する
3. Project削除を`ACTIVE → ARCHIVED`の論理削除とする
4. ARCHIVED Projectの分析来歴を保持する
5. Feature columnsをDataset schemaから選択できるUIを追加する
6. OutcomeをDiscoveryで選択し、Graph VersionおよびInferenceへ継承する
7. InferenceのOutcome入力欄を廃止する
8. Discovery ResultとGraph VersionをGraph Candidate Query Projectionで統合表示する
9. Graph確認・編集機能をモーダルへ統合する
10. 独立Graph Version editorセクションを廃止する
11. 2件以上のGraph Candidate比較を視覚表示する
12. FIXED Graph Versionを直接更新しない
13. Parent Graphは版系譜上の派生元Graph Versionを意味する
14. 各画面の基本設計に操作、前提状態、Entity生成更新、操作後状態およびUI Gateを記載する
15. 主要Entityを7件のまま維持する
16. `31_ENH-E1a_設計追補.md`を`30_詳細設計.md`へ統合する

## 3. 承認済みの要件・設計判断

### 3.1. Project削除

画面文言は「削除」としてよいが、実装は論理削除とする。hard deleteを行う場合は別途要件変更承認を必要とする。

### 3.2. Outcome

- Graph Versionに指定されたOutcomeがGraph nodeおよびDataset columnとして存在すること
- Inference受付時にGraph VersionとCausal QuestionのOutcome一致を検証すること
- 既存Graph Versionはmigration後にOutcome未指定を許容するが、Inferenceへの新規使用は拒否すること

### 3.3. Graph編集

- Discovery Resultを直接上書きしないこと
- FIXED Graph Versionの編集は新しい子DRAFTを生成すること
- DRAFTのみ同一Version内で編集可能とすること
- Parent Graphは同一ProjectかつFIXEDであること
- Cycleを生成しないこと

### 3.4. Graph表示

DAG表示を要求する箇所でも、Graph TypeがCPDAG / PAGの場合はendpoint semanticsを保持し、DAGと誤表示しないこと。

### 3.5. 操作可否

Frontendの表示制御だけで不変条件を実装しない。Domain / Application Service / APIでも同一規則を検証すること。

## 4. 対象外または未承認事項

- Projectの物理削除
- ARCHIVED Project復元機能
- 複数Outcomeの同時指定
- Graph Candidate専用Tableまたは新しい主要Entity
- Graph Versionのmerge
- 複数Parent Graph
- 詳細RBAC
- 承認Workflow
- 本番リリース

## 5. 文書優先順位

```text
10_要件定義.md
→ 22_プロダクト基本設計.md
→ 21_論理データ設計.md
→ 23_API・インターフェース設計.md
→ 30_詳細設計.md
→ 06_Ariadne_ENH-E2_実装指示書.md
→ 実装
→ Test
```

データ設計と基本設計に矛盾がある場合は、要件に戻って意味論を確定してから両方を改定する。

## 6. 承認再審議条件

1. OutcomeをGraph Versionへ保持すると既存科学モデルと整合しないことが実証された場合
2. Project archiveでは改善要望の削除目的を満たせない場合
3. Graph Candidate Projectionで性能または整合性要件を満たせない場合
4. 既存7 Entityでは操作履歴またはProvenanceを保持できない場合
5. FIXED Graphの不変性とモーダル編集要件が両立しない場合
6. ENH-E1a追補を30へ統合した結果、上位要件と矛盾する場合

## 7. 承認結果

```text
判定: APPROVED
文書策定方針: APPROVED
Enhance計画: APPROVED
要件・設計文書: APPROVED
承認者: Project Owner
承認日時: 2026-08-06 23:40 JST
承認根拠: 本チャット上の「承認する」との明示回答
実装開始: NOT_APPROVED
本番リリース: NOT_APPROVED
```
