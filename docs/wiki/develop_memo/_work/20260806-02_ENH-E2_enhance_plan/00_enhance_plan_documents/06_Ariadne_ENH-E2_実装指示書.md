# Ariadne ENH-E2 実装指示書

- 作成日: 2026-08-06
- 対象ブランチ: `prototype/ariadne_mvp`
- 基準コミット: `538daebcee888722b245cb887bdfc8ec86d827c6`
- 改定識別子: `ENH-E2`
- 実装状態: 未着手

## 1. 実装開始条件

次の改訂版文書を正本として使用すること。

- `00_プロダクトコンセプトメモ.md`
- `10_要件定義.md`
- `21_論理データ設計.md`
- `22_プロダクト基本設計.md`
- `23_API・インターフェース設計.md`
- `30_詳細設計.md`

`31_ENH-E1a_設計追補.md`を別途参照して実装してはならない。内容は改訂版`30_詳細設計.md`へ統合済みとする。

## 2. Coding Agentへの最上位指示

1. 実装から要件を変更しない
2. 画面だけで不変条件を実装しない
3. Projectを物理削除しない
4. Discovery Resultを直接編集しない
5. FIXED Graph Versionを更新しない
6. Graph Candidate用の新しい正本Tableを作らない
7. Inference画面でOutcomeを再入力させない
8. CPDAG / PAGをDAGとして描画しない
9. 既存ENH-E1 / E1a科学機能を退行させない
10. 未決事項を発見した場合は実装を独自補完せず、要件・設計変更提案として報告する

## 3. 現行コード上の主な変更対象

### 3.1. Frontend

- `frontend/index.html`
- `frontend/app.js`
- `frontend/styles.css`

現行のProject作成フォーム、Graph Version editor、Discovery comparisonのJSON表示およびInference Outcome入力を置換する。

### 3.2. Domain / Application

- `src/ariadne/product/domain/project.py`
- `src/ariadne/product/domain/graph_version.py`
- `src/ariadne/product/domain/analysis_spec.py`
- `src/ariadne/product/application/project_data_service.py`
- `src/ariadne/product/application/graph_version_service.py`
- `src/ariadne/product/application/query_service.py`
- 必要に応じて`graph_candidate_query_service.py`

### 3.3. API

- `src/ariadne/interfaces/web_api/routers/projects.py`
- `src/ariadne/interfaces/web_api/routers/graph_versions.py`
- `src/ariadne/interfaces/web_api/routers/results.py`
- `src/ariadne/interfaces/web_api/schemas/__init__.py`
- router registrationおよびerror handler

### 3.4. Persistence

- `src/ariadne/product/persistence/orm_models.py`
- repository mapper / repository implementation
- `product_migrations/versions/`

## 4. Work Package依存順序

```text
WP-0 Requirements Gate
→ WP-1 Project Archive Contract
→ WP-2 Outcome / Discovery Contract
→ WP-3 Graph Candidate Query
→ WP-4 Graph Edit Lifecycle
→ WP-5 Frontend Information Architecture
→ WP-6 Graph Comparison
→ WP-7 Inference Input Revision
→ WP-8 ENH-E1a Regression
→ WP-9 Final Verification
```

## 5. WP-0 Requirements Gate

### 5.1. 作業

- 基準コミットを記録する
- 改訂版6文書のhashを記録する
- 要件ID FR-068〜095、NFR-017〜021をTest計画へ写像する
- `31_ENH-E1a_設計追補.md`が改訂版成果物に含まれないことを確認する

### 5.2. 完了条件

- Coding Agentが旧文書を正本として使用していない
- 実装前差分と要件差分が区別されている

## 6. WP-1 Project Archive Contract

### 6.1. Domain

- `Project.archive()`をApplication Serviceから利用可能にする
- ARCHIVED Projectのmetadata更新を拒否する
- ARCHIVED ProjectへのDataset登録、Execution作成、Graph作成およびAnnotation writeを共通guardで拒否する

### 6.2. API

- `DELETE /api/v1/projects/{project_id}`を追加する
- 処理はidempotentな論理削除とする
- ACTIVE Project一覧を既定とする
- 状態不整合を`PROJECT_ARCHIVED`で返す

### 6.3. Frontend

- Project Register & Management画面を追加する
- Project registerとProject listを配置する
- 削除確認modalを実装する
- archive完了時に選択中Project contextを解除する

### 6.4. Test

- ACTIVE → ARCHIVED
- 二重DELETEのidempotency
- archived write rejection
- existing lineage retention
- hard delete未実行

## 7. WP-2 Outcome / Discovery Contract

### 7.1. Data Model

Graph Versionへ`designated_outcome_node`を追加する。既存行はnullable migrationとする。

### 7.2. Discovery Snapshot

- `operation_spec.designated_outcome_node`
- `operation_spec.feature_columns`
- Dataset schemaとの一致
- OutcomeがFeature columnsに含まれることを要求する

### 7.3. Result / Graph Version

- Discovery Result summary / payloadへOutcomeを保存する
- Graph Version作成時にOutcomeを継承する
- 子Versionは親から既定継承する
- Outcome変更時は新Versionと理由を要求する

### 7.4. Test

- unknown outcome rejection
- outcome not in features rejection
- result propagation
- parent inheritance
- fixed graph inference eligibility

## 8. WP-3 Graph Candidate Query

### 8.1. Query Model

Discovery Graph ResultとGraph Versionを`GraphCandidateView`へ変換する。

必須field:

- candidate kind / id
- source result
- graph version
- parent graph
- graph type / origin
- status / fixed flag
- designated outcome
- node / edge counts
- summary / warning
- allowed actions

### 8.2. API

- list endpoint
- detail endpoint
- comparison query
- Project境界検証

### 8.3. Test

- ResultとGraph Versionの統合順序
- parent / source表示
- archived Project read-only
- no GraphCandidate table

## 9. WP-4 Graph Edit Lifecycle

### 9.1. Domain規則

- Parent Graphは同一ProjectかつFIXED
- DRAFTのみ`apply_edit()`可能
- FIXEDへの直接PATCH拒否
- parent cycle拒否
- FIX前にGraph semanticsとOutcomeを検証

### 9.2. Modal操作

| Candidate | 操作 |
|---|---|
| Discovery Result | inspect、DISCOVERED root作成、edit-as-child |
| DRAFT Graph Version | inspect、edit、fix |
| FIXED Graph Version | inspect、create child draft |

Discovery Resultから編集を開始する場合、Algorithm Outputを保存するDISCOVERED rootを確保した後にUSER_EDITEDまたはCONSTRAINT_ADJUSTED child DRAFTを作成する。

### 9.3. Test

- result overwrite不可
- parent must be fixed
- draft update
- fixed update rejection
- child creation
- rationale requirement
- cycle detection

## 10. WP-5 Frontend Information Architecture

### 10.1. 共通

- ページ説明
- セクション説明
- glossary / tooltip
- placeholder
- status badge
- disabled reason

### 10.2. Project / Data

- Project編集のみ
- Dataset Register
- Registered Datasets

### 10.3. Discovery

- Feature selector modal
- Outcome dropdown
- Graph Candidate table
- Graph inspect/edit modal
- standalone Graph Version editor削除

## 11. WP-6 Graph Comparison

- 2件以上で起動
- modal表示
- candidateごとのtab
- Graph Type表示
- node / edge summary
- compatibleな場合のedge add / remove / orientation diff
- incompatibleな場合の理由表示
- raw JSONは補助的downloadまたはdebugに限定

## 12. WP-7 Inference Input Revision

- Outcome inputを削除
- FIXED Graph選択時にOutcomeをread-only表示
- graph outcome未指定時はIdentification buttonを無効化
- APIでOutcome一致を再検証
- Identification、Data Eligibility、各入力項目のhelpを表示

## 13. WP-8 ENH-E1a Regression

改訂版30へ統合された次のcontractを維持する。

- inferred types
- prerequisite skip statuses
- Identification status precedence
- revision_context
- post-selection inference warnings
- v2 strict allow-list

既存ENH-E1 / E1a Testを削除または弱化してはならない。

## 14. WP-9 Final Verification

### 14.1. 必須検証

- unit test
- API contract test
- repository integration test
- frontend contract test
- E2E-01〜E2E-10
- scientific benchmark regression
- migration up / downまたはforward-only方針確認
- document traceability

### 14.2. 完了定義

- FR-068〜095およびNFR-017〜021がTest証跡を持つ
- archived Projectが物理削除されない
- Graph Candidate用Tableがない
- FIXED Graphの直接更新経路がない
- Inference Outcome tamperingを拒否する
- Graph比較が2件から使用可能である
- Graph Version editorの独立セクションがない
- 31追補内容のregression testが成功する

## 15. 完了報告形式

```markdown
## ENH-E2 Completion Report

### Baseline
- Branch:
- Start commit:
- End commit:

### Requirements
- Implemented IDs:
- Deferred IDs:

### Changed Files
- ...

### State Transition Compliance
- Project:
- Graph Version:
- Execution / Result:

### Tests
- Unit:
- Integration:
- API:
- Frontend:
- E2E:
- Benchmark:

### Deviations
- None / details

### Unresolved Issues
- None / details
```
