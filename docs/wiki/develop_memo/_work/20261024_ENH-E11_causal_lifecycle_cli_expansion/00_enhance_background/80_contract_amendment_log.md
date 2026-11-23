# ENH-E11 — 契約変更履歴（追記専用）

**文書区分:** 計画・証跡・ガバナンス資料  
**状態:** G01/P01凍結後契約欠陥の改訂案あり／Owner A案採用、改訂後のS10/S11再承認待ち

## 1. 目的

正式承認後、またはGate 06/07のfreeze後に発生した契約変更を追記する。従前のBLOCKED/FAILと検証証拠を保持し、変更理由、影響するFR/NFR/AR・設計・Gate、変更前後の意味、SHA、再基準化、次Trialを記録する。

## 2. 現在の記録

**初回凍結後契約変更より前は該当なし。** 2026年9月のNotion `HANDOFF_DRAFT`と2026年10月24日のオーナー方針におけるPhase 1〜3 CLI-firstへの対象拡大は、**承認前の計画変更**である。凍結済みGate契約の修正として遡及記録しない。事前調査`00_01_foundation_gap_reconciliation.md`、構想`01`、承認記録`02`、要件改定案`03`、三資料照合`00_03`、Issue #13で扱う。

### AMD-E11-G01-P01-001 — `CONTRACT_DEFECT`（2026-11-23）

- **発端:** G01/P01 Trial01 Coding Agentが`BLOCKED_CONTRACT_AMBIGUITY`で実装前停止。`from_run_evidence(evidence:ValidatedRunEvidence)`の必須構造とArtifact別upstream-ref joinが06/P01単独で未確定。観測開始SHA `6ec2f59fa71b85aeff46daf0e6740b04281e8436`、Package checkpointなし、変更なし。停止報告はユーザー提供の外部Agent記録で、独立検証済みTest報告ではない。
- **Owner方針:** 同日の会話で **A案（既存責務を維持した最小契約補完）採用**、続けて「早急に…ドキュメント修正」を指示。これは修正の承認であり、**変更後のS10 Freeze/S11 Coding Authorizationの再発行ではない**。
- **変更前Freeze / Authorization:** S10 `a05fd072cbb82a7c6e43f45e7208e078f0784a2b`／`uv.lock` Git blob `2b83110e86b26b7969fbddf8f98a727370ae19f7`、Owner記録179/180。両記録を不変の履歴として保持。
- **変更後の設計意味:** P01はtyped Study/Status/Runtime/Stochastic/Artifact/Graph-or-negative evidenceをpureに投影し、各Refの値・Inventory・Method/Statusの照合を拒否条件まで定義。P02は実bytes/hash/FS/Reader、P03はGraph意味、P05は実行・Inputとcross-file validation。出力Graph Refと入力Graph nullを区別。公開E11 JSON version/schemaへの新フィールド追加なし、P1-M06 Science/BK/Privacy/旧v2/07/999要件に変更なし。
- **影響範囲:** G01/P01 §3,§6.5,§7,§10、stock 30_62 §4、IF 23_42 §2、G01/P02・P05 handoff、G01 07検証の明確化。G01/P03・P04本体、G02以降Method契約、code/uv.lockは変更不要。FR-201/202/203・NFR-029/030/032・AR-040の**既存受入意味は不変**。
- **変更管理記録:** `combined_review/183_20261123_g01_p01_manifest_evidence_contract_defect_amendment.md`。本更新を反映するGit commit full SHAは当該commit作成後に操作記録から取得し、正式なOwner再Freeze記録に固定する（自己参照SHAをこのファイル内に捏造しない）。
- **再開条件:** 改訂文書のcross-contract監査→契約変更として09/影響評価→Owner新暫定G01-S10 Freeze→**別個**の限定G01-S11再Authorization→実行環境の最新SHA/lock/クリーンtree再Preflight。Trial01の停止記録を保存し、formal FAILではないためTrialを自動増番しない。**現時点で実装再開許可は未成立**。

## 3. 今後の記録必須項目

Amendment ID、状態、発生要因・証跡、影響Gate/Trial、変更種別（`REQUIREMENT_CHANGE / DESIGN_CHANGE / CONTRACT_DEFECT / OTHER`）、適用するGate 09、オーナー承認、変更前後の正規意味、影響06/07/Pxx/Rxx、再基準SHA、旧テスト証跡の保存状況。

**テストをPASSさせるためだけに科学的受入条件を緩めない。**
