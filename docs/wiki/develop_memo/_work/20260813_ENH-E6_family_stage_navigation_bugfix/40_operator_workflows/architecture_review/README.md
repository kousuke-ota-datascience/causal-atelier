# ENH-E6 Architecture Review Workflow

**Document class:** Authoring Guide  
**Applicability:** `REQUIRED / COMPLETED FOR PLANNING`

## 1. Purpose

Before implementation contract, identify current navigation architecture facts, decide target authority/lifecycle, and confirm Gate vs Work Package decomposition without changing product code.

## 2. 使用条件 — CONDITIONAL MUST

ENH-E6 meets:

- runtime/navigation lifecycle change
- authority/ownership consolidation
- legacy analytical path consolidation
- UI/history/presentation cross-boundary source-of-truth alignment

## 3. 実行順序

1. `01_architecture_discovery_result.md` — facts/inferences/unknowns.
2. `02_target_architecture_decision_record.md` — target authorities/invariants/transition decision.
3. `03_gate_decomposition.md` — one Gate / package boundary decision.

## 4. Output rule

Results are planning/operator evidence, not Coding Agent normative inputs. Approved decisions are reflected in 00 and self-contained Pxx/Gate contracts. Coding Agent is not instructed to read these artifacts.
