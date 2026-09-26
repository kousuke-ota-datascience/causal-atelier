# ENH-E10 G03 P00 — Work Package Plan

**Document class:** Work Package Planning Contract  
**Status:** `MATERIALIZED_DRAFT / PLANNING_ONLY / NON_EXECUTABLE`  
**Gate:** `G03`  
**Execution mode:** `WORK_PACKAGE`  
**Gate dependency:** `G01 PASS + G02 PASS`  
**Authority:** Gate 06/07 define semantics and acceptance; P00 only defines execution decomposition.

## 1. WP adoption decision

API/capability-driven Train、Explainability/Model Management presentation、real-browser cross-layer proofは別subsystem boundaryであり、P03はP01/P02のproduct wiring完成後でなければ有効なE2Eを構築できないため、G03はWork Package modeを採用する。

## 2. Package map

| Package | Scope | Dependency |
|---|---|---|
| P01 | Capabilities / Train Integration | G01 PASS + G02 PASS |
| P02 | Explainability / Model Management Integration | P01 PACKAGE_COMPLETE |
| P03 | Browser E2E / Product Regression | P02 PACKAGE_COMPLETE |

## 3. Freeze blockers

capabilities API schema、parameter rendering/default selection、unavailable/incompatible UX、Model Management provenance set、Browser canonical command/environment/fixture/synchronization/assertions。

## 4. Package execution rule

P01 → P02 → P03。各PxxはFROZEN後にassigned Coding Agentへ渡す。P03 completion後にCandidate Assemblyを行う。Pxx completionはGate PASSではない。

## 5. Current state

`MATERIALIZED_DRAFT`。06/07/P01-P03と同一batchでfreezeする。
