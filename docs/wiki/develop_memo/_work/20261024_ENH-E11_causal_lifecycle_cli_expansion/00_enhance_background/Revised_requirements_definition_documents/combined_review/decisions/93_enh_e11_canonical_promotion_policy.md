# ENH-E11 — 作業文書の格納・Canonical昇格方針（Owner決定）
 
**Owner決定日:** 2026-11-16 JST  
**状態:** `OWNER_APPROVED_DOCUMENT_LOCATION_AND_PROMOTION_CRITERION / FULL_TEST_PASS_PENDING / NOT_PROMOTED`
 
## 1. 本エンハンス内の文書配置
 
ENH-E11の要件定義・論理データ設計・基本設計・インターフェース設計・詳細設計、およびその変更記録・監査台帳の管理先は、実装と検証の期間を通して次のディレクトリとする。
 
```text
docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/00_enhance_background/Revised_requirements_definition_documents/
```
 
- 上記ディレクトリ内の`10_*`／`21_*`／`22_*`／`23_*`／`30_*`を、ENH-E11で編集・レビュー・検証する文書群とする。
- 元の`docs/wiki/requirement_definition/`は現時点で**変更しない**。上記作業コピーで発行した条文・設計を、この時点で元正本に反映したと見なさない。
- ENH-E11の`_drafts/`や`_review/`の資料は正式な有効設計と区別し、文書の状態を引き続き明示する。
 
## 2. 元正本への昇格条件
 
**ENH-E11の対象となるテストが全件PASSしたことを確認した後に、元正本への昇格を実施する。**
 
- 1件でも未実施・FAIL・BLOCKED・未判定の対象テストが残る状態では昇格しない。
- 全件PASSを判定する対象範囲は、ENH-E11の承認済みRequirements、Scope／Method／UC、回帰保護、科学的受入およびGate計画に対応する検証項目とし、対象と除外を検証台帳で区別する。**Methodが承認済みであること／試験計画を作成したことはテストPASSではない。**
- 全件PASS後、作業文書のRevisionと証拠を照合して`docs/wiki/requirement_definition/`へ昇格する。具体的な昇格差分・最終レビュー・履歴・版管理はその際に記録する。
- 配布ライセンス審査・顧客納入可否は、テストPASSとは別の既存Legal Gateとして管理する。
 
## 3. 現時点の状態
 
| 対象 | 状態 |
|---|---|
| ENH-E11作業ディレクトリ | ACTIVE WORKING DOCUMENT SET |
| RD-01分類／RD-02再編／RD-03 E11新条文・Trace | GitHubへ記録済み（未承認Dispositionなど各文書の個別状態は維持） |
| 全件テストPASS | 未確認・未達 |
| 元正本への昇格 | NOT_STARTED / BLOCKED_UNTIL_ALL_APPLICABLE_TESTS_PASS |
| 顧客配布ライセンス承認 | 別途審査、未完了 |
 
**この決定は、要件の内容や実装範囲の追加承認、Gate PASS、Coding開始許可を意味しない。**
