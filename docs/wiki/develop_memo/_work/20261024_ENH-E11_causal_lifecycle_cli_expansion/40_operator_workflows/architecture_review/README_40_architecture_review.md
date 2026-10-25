# ENH-E11 — Architecture Review資料一覧

**状態:** 調査ドラフト／目標ArchitectureのHuman判断待ち

本Enhancementは新たなScientific runtime入口、第一級Design/Result契約、optional backend、永続ローカルArtifact、version・provenanceの所有権を伴うため、Workflowに従いArchitecture Reviewが必要となる。

**作業順序:** まず`../../00_enhance_background/00_foundation_gap_reconciliation.md`を確認する。9月末Foundation Gapの現状を把握せず、歴史資料の全項目をそのまま新実装対象にしてはならない。

1. `01_architecture_discovery.md` — コード上の事実、推論、未確認事項、ソース。
2. `02_target_architecture_decision_record.md` — 所有権、不変条件、目標案。**未承認**。
3. `03_gate_decomposition.md` — 意味上の受入境界と依存関係の案。**Gate 06/07未固定**。

正式な決定は00層の要件・設計へ反映して初めて有効となる。適用するWorkflow原則は`agentic_enhancement_workflow_template/40_operator_workflows/architecture_review/README_40_architecture_review.md`を参照する。
