# ENH-E11 — 承認済み要件・設計のSnapshot格納場所

**状態:** **承認待ち。ENH-E11で承認済みの改定Snapshotは存在しない。**

このディレクトリは、ENH-E11の要件・設計改定が正式承認された後に、正本の有効版を保存するための場所である。

格納候補：`00_product_concept_memo.md`、`10_requirements_definition.md`、`21_logical_data_design.md`、`22_product_basic_design.md`、`23_api_interface_design.md`、`30_detailed_design.md`。

承認前の草案や歴史資料をここへ置き、承認済みと表示してはならない。

現行正本の計画参照点は`84c5a624389b233fcb97c656f1c94d177f459c5a`。先行する事前調査は`../00_foundation_gap_reconciliation.md`。正式承認時には、その時点の受入基準SHAを再取得し、承認済み正本をchecksumとともに保存する。

適用Workflow：`agentic_enhancement_workflow_template/00_enhance_background/README_00.md`。
