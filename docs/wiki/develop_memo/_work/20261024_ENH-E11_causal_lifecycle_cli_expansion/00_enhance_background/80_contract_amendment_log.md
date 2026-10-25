# ENH-E11 — 契約変更履歴（追記専用）

**文書区分:** 計画・証跡・ガバナンス資料  
**状態:** 承認済み契約の変更なし

## 1. 目的

正式承認後、またはGate 06/07のfreeze後に発生した契約変更を追記する。従前のBLOCKED/FAILと検証証拠を保持し、変更理由、影響するFR/NFR/AR・設計・Gate、変更前後の意味、SHA、再基準化、次Trialを記録する。

## 2. 現在の記録

**該当なし。** 2026年9月のNotion `HANDOFF_DRAFT`と2026年10月24日のオーナー方針におけるPhase 1〜3 CLI-firstへの対象拡大は、**承認前の計画変更**である。凍結済みGate契約の修正として遡及記録しない。事前調査`00_foundation_gap_reconciliation.md`、構想`01`、承認記録`02`、要件改定案`03`、三資料照合`06`、Issue #13で扱う。

## 3. 今後の記録必須項目

Amendment ID、状態、発生要因・証跡、影響Gate/Trial、変更種別（`REQUIREMENT_CHANGE / DESIGN_CHANGE / CONTRACT_DEFECT / OTHER`）、適用するGate 09、オーナー承認、変更前後の正規意味、影響06/07/Pxx/Rxx、再基準SHA、旧テスト証跡の保存状況。

**テストをPASSさせるためだけに科学的受入条件を緩めない。**
