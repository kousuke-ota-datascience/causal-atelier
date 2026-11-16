# DOC-01 — Stock/Flow分離・Requirement Integrity・Link検証結果

**Document type:** FLOW / AUDIT、正本化対象外  
**Baseline commits:** 作業コピー開始時`db47b8694ce315b4e8dbe3ab18d1c125f2c71205`、初期台帳`f5ccbac5adabbe932e79686a1e81502883610d49`。  
**Inspection date:** 2026-11-16  
**Internal assessment:** `STATIC_CHECK_PASS / STOCK_FLOW_RESTRUCTURE_PREPARED / OWNER_CONTENT_REVIEW_PENDING / CODING_NOT_AUTHORIZED`。

## 1. ScopeとMethod

- 対象：`Revised_requirements_definition_documents/`のStock系Markdown、初期105件（10=23、21=18、22=19、23=20、30=25）。
- 分類軸：User/Operator期待と科学的条件は10、論理値・関係は21、責務・System architectureは22、Observable Interface/wireは23、Class/Process/Algorithmは30。Enhancement固有のReview/移管ログ/草案/Source snapshotは`doc01_review/`等に分離。
- 初期105件のblobをGitHub commit/treeで読取、relative Markdown file linkをtree pathへ解決、工程専用Placeholder語と残存階層を確認。元正本`docs/wiki/requirement_definition/`を編集していない。
- Requirement rowsの集計は10系の原表 `| FR-... | / | NFR-... | / | AR-... |`を対象に抽出。変更履歴（10_99等）の再掲を正式台帳行として二重計上しない。数字だけでなく`FR-128a`等suffix付きIDを抽出。
- 元の退避10要件定義と各10系Stockの `MOVE_BD` 19件を行の原文・Level・Status・Implementation Status・Deliveryで直接比較した。

## 2. 数値結果

| Check | Result | 観測上の限界 |
|---|---|---|
| 初期Stock 5群 | 105 files、23/18/19/20/25 | フォルダー粒度の構造と本文検査 |
| Stock内の`_drafts/` / `_review/` | 0 | File tree上 |
| 元105ファイルのMarkdown relative file links | Broken 0 | HTML-anchor見出しID、外部URL・非Markdown参照は含まず |
| Root index relative links（台帳新設後） | 141件、Broken 0 | 参照先file存在の確認 |
| Requirements original baseline | FR 195／NFR 36／Scientific AR 27 = 258 | Statusの個別実装判定は別 |
| ENH-E11 newly issued | FR 19／NFR 8／Scientific AR 17 = 44 | 全件未検証／実装完了ではない |
| Requirement active table rows | 302件、重複ID 0 | 10系原表の整合；科学的正しさとは別 |
| MOVE_BD全文復元 | 19/19、旧snapshotと一致 | 原文・Level/Status/Implementation/Delivery比較。122条文すべての意味検証ではない |
| IF-01／DD-01追加後のStock | 110件、23/18/19/22/28 | 新規5 fileのMarkdown relative linkに破損0。統合索引へ追加 |
| Code/Science/Legal/Independent Review | NOT_RUN / NOT_APPROVED | DOC文書監査から推定しない |

## 3. Flowへ分離した資料の分類

| Flow / audit location | 分離した内容 | Stockへ保持する情報 |
|---|---|---|
| `doc01_review/rd04_migration/` | RD-04原文/移管理由、工程状態、source SHA | 現行の永続要件・科学的制約、設計下位Contract |
| `doc01_review/metadata_snapshots/` | 各5群の歴史的review/publication stateとprovenance（各a/b） | Contractに必要な実効schema/versionと設計制約のみ |
| `doc01_review/prior_drafts/` | 旧E11 draft5件、E8 Stage旧稿、DD gap snapshot | 採用された規範だけを10/21/22/23/30系へ反映 |
| `doc01_review/rd_move_bd_requirement_recovery.md` | MOVE_BD 19件の復元根拠・対照 | 原文Requirement ID/Level/Status/Meaningを10系へ戻す |
| `bd01_review/` | Architectureの13 Findings/2修正/11 open | Owner採用ARC09原則の永続的責務を22系に保持 |
| `if01_review/`、`dd01_review/` | IF/DD内部Review・未閉鎖 | 23/30系の候補Interface/Physical contracts |
| `combined_review/` | 3工程一括Owner review/意思決定依頼 | Owner承認後に規範だけをStockへ反映 |

## 4. 内容監査の残余（合算レビュー対象）

| DOC Finding | Evidence | 未閉鎖 |
|---|---|---|
| DOC01-F01 | 105件の相対File link／工程用directoryの構造点検により、代表的な混入は除去。汎用の全文意味的レビューは未完 | Owner/independent逐条レビュー |
| DOC01-F02 | 302正式要件ID抽出・重複0。既存258+新44件 | 旧122改訂条文の意味保存/実装Status最終確認 |
| DOC01-F03 | 原105件のMarkdown fileリンクBroken0＋Root索引141件Broken0。新5件Broken0 | Anchor/画像/外部/既存コード参照の完全検証 |
| DOC01-F04 | MOVE_BD原文19/19一致 | RD-04全部のTrace/Meaning/Owner closure |
| DOC01-F05 | Root ENH-E11 workflow READMEには2026-10-25の古い計画状態あり | 別途Flow索引更新；Stock契約と区別 |

未閉鎖事項は**Contract未承認／文書完全性審査の残余**であり、観測していないMethod Science FAILという意味ではない。

## 5. DOC-01判定の限界

- 「Stock配置の修復と機械的Check」について内部PASSを記録するが、**Ownerまたは独立Reviewerによる全文の逐条意味監査のPASSではない**。
- Userの指示でDOC-01の作業版完成後、IF-01とDD-01を続行し、その3件を同時にレビューする。従ってReview Ownerが採否を返すまで `DOC01_READY_FOR_COMBINED_REVIEW` とする。
- 既存 `Product GAP-C01〜04` はDOC cleanupにより閉鎖しない。Schema/Backend/Legal/Science/Gate06/07/Implementationは独立状態。
- 元正本への昇格はENH-E11対象テスト**全件PASS後のみ**。CICD testを実行したという証拠は存在しない。

## 6. 一括レビューの照合順

1. DOC-01：ストック／フローの分類・302条文と旧19全文比較・残存意味監査を検討。
2. IF-01：新E11 CLI/Portの具体Schema・Output/Graph/AR/Privacy/Atomicとlegacy互換を検討。
3. DD-01：各Class責務、41 Method adapterの型と科学的限定、Fault Injection/Privacy/Backendを検討。
4. 例外・修正要求を一つのレビュー記録で判定し、承認済み変更だけをStockに反映。全テストPASSまでcanonicalへpromoteしない。
