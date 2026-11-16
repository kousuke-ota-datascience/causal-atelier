# DOC-01 — 全設計書のストック適合性監査台帳

**種別:** FLOW / AUDIT（将来の正本には昇格しない）  
**監査開始時点:** 2026-11-16、`prototype/ariadne_mvp` / `db47b8694ce315b4e8dbe3ab18d1c125f2c71205`  
**判定:** `STOCK_FLOW_DRAFT_COMPLETE / STATIC_CHECK_PASS / OWNER_SEMANTIC_AND_COMBINED_REVIEW_PENDING / CODING_NOT_AUTHORIZED`

## 1. 目的と判定範囲

`Revised_requirements_definition_documents/`の10／21／22／23／30系を、将来`docs/wiki/requirement_definition/`へ反映可能な**ストック型**の文書として整える。改訂工程・承認経緯・レビュー・旧版草案・移管ログは本`doc01_review/`や各工程レビューへ分離する。

ストックに保持すべきものは、要件・データ／設計／Interface／物理設計の**継続的に有効な規範、契約、制約、受入条件**である。工程の状態、個別レビュー結果、追跡のためだけのプレースホルダーを本文の代わりにしない。

この監査は文書の正本昇格、Coding Authorization、独立Architecture/Science/Legalレビュー、Gate06/07 freezeや実装・テストPASSを代替しない。元正本`docs/wiki/requirement_definition/`はENH-E11対象テスト全件PASSまで変更禁止。

## 2. 対象および作業済みの分離

| 正本候補の文書群 | 直下の番号付きMarkdown件数 | 分離した主なフロー／監査資料 |
|---|---:|---|
| `10_requirements_definition/` | 23 | `rd04_migration/10_requirements_definition.md`、`metadata_snapshots/10_*.md`、要件発行draft |
| `21_logical_data_design/` | 18 | `rd04_migration/21_logical_data_design.md`、`metadata_snapshots/21_*.md`、local logical model draft |
| `22_product_basic_design/` | 19 | `rd04_migration/22_product_basic_design_part1.md`／`part2.md`、`metadata_snapshots/22_*.md`、BD草案とE8履歴 |
| `23_api_interface_design/` | 20 | `rd04_migration/23_api_interface_design.md`、`metadata_snapshots/23_*.md`、CLI/Port草案 |
| `30_detailed_design/` | 25 | `rd04_migration/30_detailed_design.md`、`metadata_snapshots/30_*.md`、class草案と物理設計gap記録 |
| **合計** | **105** | |

実体は次を参照する。

- [RD-04移管履歴](rd04_migration/)：Stockへ残す規範と移管元の工程記録を区別。
- [原メタデータ断片](metadata_snapshots/)：5文書群のレビュー状態、provenance等を保持。
- [旧草案の保全台帳](prior_drafts/README.md)：5群のdraftとDD gap等を分離。
- [MOVE_BD要件正文の回復](rd_move_bd_requirement_recovery.md)：19件の設計移管プレースホルダーを元要件本文へ戻し、元ID／状態を維持するという処置を記録。
- [BD-01監査](../bd01_review/README.md)：独立Architectureレビュー未完、未閉鎖11 findingは別管理する。

## 3. 検証結果

### 3.1. 実施した機械的確認

1. 基準SHAのGit treeで、5文書群直下の番号付きMarkdownは計105件（23/18/19/20/25）を確認。
2. 5文書群の内部に`_drafts/`、`_review/`という工程専用ディレクトリが残存しないことを確認。
3. [全体索引](../README_00_Revised_requirements_definition_documents.md)の相対Markdownリンク141件をGit treeと照合。基準SHAでの**唯一の未解決リンク**が、本監査台帳`doc01_review/README.md`だった。**本ファイル作成によって当該リンク先を設ける**。新コミットでの再照合は別途行う。
4. `MOVE_BD`由来の原文回復19件は[対照表](rd_move_bd_requirement_recovery.md)に記録されていることを確認。

### 3.2. 未検証・未閉鎖事項

| ID | 対象 | 未完事項 | DOC-01判定への影響 |
|---|---|---|---|
| DOC01-F01 | 105設計書すべて | 本文全体のフロー文言残存、歴史的レビュー結果の仕様誤混入、仕様本文の欠落を逐条検査していない | **BLOCKED** |
| DOC01-F02 | 10系の要件台帳 | 既存258＋新規44の計302条文は抽出しID重複0を確認。ただし旧条文122件の全文意味比較・Owner最終確認は未完 | PARTIAL / OWNER_REVIEW |
| DOC01-F03 | 5群の参照リンク | 元105設計書の本文内Markdown相対Fileリンクは破損0、索引141件も破損0。Anchor・外部URL・非Markdown参照までの完備性は未検証 | PARTIAL / ANCHOR_CHECK_PENDING |
| DOC01-F04 | 要件意味保存 | MOVE_BD 19件は旧退避要件とRequirement/Level/Status等が全件一致。RD-04全122改定条文の独立意味監査とOwner確認は未完 | PARTIAL / OWNER_REVIEW |
| DOC01-F05 | ENH-E11全体のWorkflow索引 | 上位`20261024_ENH-E11_causal_lifecycle_cli_expansion/README.md`には2026-10-25時点の`未作成`等の古い状態表示が残る。今回の5文書群の規範性判断とは別途修正する | **FOLLOW-UP** |

ここでの`BLOCKED`は**監査未完**を意味し、実装・科学的正しさがFAILと判定されたことを意味しない。

## 4. DOC-01完了条件

DOC-01の`PASS`は以下をすべて満たした時にのみ記録する。

1. 105設計書を逐条分類し、Stockに残す規範とFlowに移す監査・作業情報を区別。仕様欠落・重複して有効な対立条文を残さない。
2. 既存258件と新44件の正式要件ID／正文／Status／Traceを元資料と突合し、設計移管およびMOVE_BD 19件の意味保存を確認する。
3. 全設計書・索引のリンクおよび番号付けを機械的に再検査し、破損リンク・重複番号を解消する。
4. 未閉鎖findingsを別工程に移管する場合も、Stockへの混入がないこと、追跡先と判定根拠を台帳に明示する。
5. 元正本の不変性を確認し、基準Commit SHA・監査方法・結果をこの台帳に記録する。

**次工程:** Ownerの指示によりDOC-01／IF-01／DD-01の3工程Draftを連続作成し統合レビューへ提出する。これはDOC-01の独立PASSを先取りしない。Codingは別途禁止。

## 5. DOC-01追加監査結果と統合レビュー提出（2026-11-16）

- Stock型元105件を全件Readし、Markdown相対Fileリンクのファイル実在性を照合。**Broken file links 0**（anchor、外部URL内容の検証は範囲外）。文書内工程専用`_drafts/`、`_review/`は0件。
- 10系のRequirement表は**302行／ユニーク302 ID**。内訳は既存258件（FR195/NFR36/AR27）＋E11新44件（FR19/NFR8/AR17）。`FR-128a`等のsuffix付きIDも対象に含める。
- `MOVE_BD`19件を[退避10要件定義](../_source_snapshots/10_requirements_definition.md)の原表と比較し、Requirement、Level、Requirement Status、Implementation Status、Deliveryが**19/19完全一致**（グループ名を除く）。従来の置換placeholderはStock本文に見当たらない。
- IF-01で23系に2件、DD-01で30系に3件の新仕様を追加し、Stock候補は**110件**（23/18/19/22/28）。追加5ファイルの相対Markdownリンクは破損0。Source/Traceを参照して詳細は各reviewに記録。
- 完了判定は**STATIC STRUCTURE/ID/LINK CHECK PASS；Owner/independent semantic review pending**。RD-04の122改定条文や既存Productの全物理Classの意味同一性を機械監査だけで保証したとは主張しない。詳細は[DOC-01 Verification](90_doc01_stock_flow_verification.md)。
