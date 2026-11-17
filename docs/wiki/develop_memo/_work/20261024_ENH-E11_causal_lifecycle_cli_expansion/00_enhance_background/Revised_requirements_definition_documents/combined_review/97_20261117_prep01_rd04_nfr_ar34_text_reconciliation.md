# PREP-01 RD04 NFR/AR34 — Revised Requirement Text and Metadata Reconciliation

- Date: 2026-11-17 JST
- Source branch/commit: `prototype/ariadne_mvp` / `ba7a608e3459542a2de58da203c8298ec4d75888`
- Ledger: `doc01_review/rd04_review/96_rd04_nfr_ar_application_review.md` (blob `0ffd4a693b6b6d1b18b290f146ceef771a088378`)
- Type: FLOW / STATIC RECONCILIATION, not semantic/independent approval
- Scope: 34 changed original NFR/Scientific AR clauses; 29 KEEP_RD are not changed here

## 1. Procedure

Resolve each ID once among the 5 revised NFR/AR stock files, compare RD04 ledger revised requirement text literally, and compare Requirement Status / Implementation Status. Any mismatch is a true ledger-vs-working-copy discrepancy, not implicitly a semantic regression; report without auto-overwriting accepted normative language.

## 2. Per-clause comparison

| ID | Disposition | Stock file | Text | Req status | Impl status |
|---|---|---|---|---|---|
| NFR-001b | SPLIT | `10_20_nfr_reproducibility.md` | MATCH | MATCH | MATCH |
| NFR-002 | SPLIT | `10_20_nfr_reproducibility.md` | MATCH | MATCH | MATCH |
| NFR-003 | SPLIT | `10_20_nfr_reproducibility.md` | MATCH | MATCH | MATCH |
| NFR-013 | SPLIT | `10_20_nfr_reproducibility.md` | MATCH | MATCH | MATCH |
| NFR-019 | REWRITE_RD | `10_20_nfr_reproducibility.md` | MATCH | MATCH | MATCH |
| NFR-005 | SPLIT | `10_21_nfr_reliability_performance.md` | MATCH | MATCH | MATCH |
| NFR-006a | SPLIT | `10_21_nfr_reliability_performance.md` | MATCH | MATCH | MATCH |
| NFR-006b | SPLIT | `10_21_nfr_reliability_performance.md` | MATCH | MATCH | MATCH |
| NFR-007 | SPLIT | `10_21_nfr_reliability_performance.md` | MATCH | MATCH | MATCH |
| NFR-010a | SPLIT | `10_21_nfr_reliability_performance.md` | MATCH | MATCH | MATCH |
| NFR-010b | SPLIT | `10_21_nfr_reliability_performance.md` | MATCH | MATCH | MATCH |
| NFR-011a | SPLIT | `10_21_nfr_reliability_performance.md` | MATCH | MATCH | MATCH |
| NFR-015 | SPLIT | `10_21_nfr_reliability_performance.md` | MATCH | MATCH | MATCH |
| NFR-020a | SPLIT | `10_21_nfr_reliability_performance.md` | MATCH | MATCH | MATCH |
| NFR-021 | SPLIT | `10_21_nfr_reliability_performance.md` | MATCH | MATCH | MATCH |
| NFR-023 | SPLIT | `10_21_nfr_reliability_performance.md` | MATCH | MATCH | MATCH |
| NFR-024 | SPLIT | `10_21_nfr_reliability_performance.md` | MATCH | MATCH | MATCH |
| NFR-025 | SPLIT | `10_21_nfr_reliability_performance.md` | MATCH | MATCH | MATCH |
| NFR-027 | REWRITE_RD | `10_21_nfr_reliability_performance.md` | MATCH | MATCH | MATCH |
| NFR-008a | SPLIT | `10_22_nfr_security_compatibility.md` | MATCH | MATCH | MATCH |
| NFR-014 | SPLIT | `10_22_nfr_security_compatibility.md` | MATCH | MATCH | MATCH |
| NFR-018 | MOVE_BD | `10_22_nfr_security_compatibility.md` | **MISMATCH** | MATCH | MATCH |
| NFR-028 | SPLIT | `10_22_nfr_security_compatibility.md` | MATCH | MATCH | MATCH |
| AR-004 | SPLIT | `10_30_ar_scientific_integrity.md` | MATCH | MATCH | MATCH |
| AR-016 | SPLIT | `10_30_ar_scientific_integrity.md` | MATCH | MATCH | MATCH |
| AR-019 | SPLIT | `10_30_ar_scientific_integrity.md` | MATCH | MATCH | MATCH |
| AR-020 | SPLIT | `10_30_ar_scientific_integrity.md` | MATCH | MATCH | MATCH |
| AR-021 | SPLIT | `10_30_ar_scientific_integrity.md` | MATCH | MATCH | MATCH |
| AR-022 | MOVE_BD | `10_30_ar_scientific_integrity.md` | **MISMATCH** | MATCH | MATCH |
| AR-027 | REWRITE_RD | `10_30_ar_scientific_integrity.md` | MATCH | MATCH | MATCH |
| AR-006 | REWRITE_RD | `10_31_ar_estimand_inference.md` | MATCH | MATCH | MATCH |
| AR-008 | SPLIT | `10_31_ar_estimand_inference.md` | MATCH | MATCH | MATCH |
| AR-009 | MOVE_BD | `10_31_ar_estimand_inference.md` | **MISMATCH** | MATCH | MATCH |
| AR-024 | SPLIT | `10_31_ar_estimand_inference.md` | MATCH | MATCH | MATCH |

## 3. Aggregate and disposition

- IDs: 34 / 34. Unique: 34. Missing/duplicate ID: 0.
- Exact revised text: 31 / 34.
- Requirement Status: 34 / 34. Implementation Status: 34 / 34.
- Static transcription: FAIL. Scientific semantic preservation and design-destination transfer **NOT_REVIEWED**.
- Source blob IDs: `10_20_nfr_reproducibility.md`=`4079ad4365150d7f4894fe88fe75a233da77eb0d`; `10_21_nfr_reliability_performance.md`=`95aacf593e823acf8f4bac803baf5082b13a00a6`; `10_22_nfr_security_compatibility.md`=`5a029d9ff0e86995745fa62fe677fdc543f8eb00`; `10_30_ar_scientific_integrity.md`=`59c0561de41a0b6f9a0c1080403da848ed3210c4`; `10_31_ar_estimand_inference.md`=`17dcec4af47440a0260b15fe603724d9ae6a9e91`.

## 4. Mismatches, if any

- **NFR-018 (MOVE_BD):** ledger revised = "【設計制約移管・Legacy Trace】NFR-005に係る既存設計制約。具体的な実装契約は下位設計へ移し、元ID・Status・科学的制約の追跡を維持する"; current stock = "Product DomainからWeb Framework、ORMおよびlegacy packageへ依存しない"; file `10_22_nfr_security_compatibility.md`
- **AR-022 (MOVE_BD):** ledger revised = "【設計制約移管・Legacy Trace】対応する既存上位要件に係る既存設計制約。具体的な実装契約は下位設計へ移し、元ID・Status・科学的制約の追跡を維持する"; current stock = "Family間でStage数・名称を揃えることを科学的workflow要件としない"; file `10_30_ar_scientific_integrity.md`
- **AR-009 (MOVE_BD):** ledger revised = "【設計制約移管・Legacy Trace】対応する既存上位要件に係る既存設計制約。具体的な実装契約は下位設計へ移し、元ID・Status・科学的制約の追跡を維持する"; current stock = "外部libraryのdtype objectまたはmodel objectをJSON正本へ保存しない"; file `10_31_ar_estimand_inference.md`

**Next:** 34 scientific/operational constraints must still be checked for loss, status changes, test acceptance, and transfer to 21/22/23/30. Document-level literal match cannot replace independent scientific/Architecture review.
