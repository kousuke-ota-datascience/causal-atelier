# ENH-E10 G01 P00 — Work Package Plan

**Document class:** Work Package Planning Contract  
**Status:** `FROZEN / PLANNING_ONLY / NON_EXECUTABLE`  
**Gate:** `G01`  
**Execution mode:** `WORK_PACKAGE`  
**Gate dependency:** `NONE`  
**Authority:** Gate 06/07 define semantics and acceptance; P00 only defines execution decomposition.

## 1. WP adoption decision

registry/dependency contract → provider adapter → durable artifact/load integration の順序依存があり、途中checkpointでfailure localizationできる。3領域は同一Gate claimを構成するが、1 execution unitへ潰すとoptional dependency・scientific adapter・artifact compatibilityの障害原因が混在するため、G01はWork Package modeを採用する。

WPはGate semantic boundaryを変更しない。Pxx completionはGate PASSを意味しない。

## 2. Package map

| Package | Scope | Dependency |
|---|---|---|
| P01 | Model Capability / Optional Dependency | ENH-E9 final PASS / accepted pre-E10 baseline |
| P02 | LightGBM Model Adapters | P01 PACKAGE_COMPLETE |
| P03 | Artifact / Load / Provenance Integration | P02 PACKAGE_COMPLETE |

## 3. Architecture Review resolution

Technical decisions are resolved in `40_operator_workflows/architecture_review/02_target_architecture_decision_record.md` and materialized into 06/07/P01-P03.

Human approval, canonical requirement/design application, and final traceability are complete. Canonical snapshot: `3e22d09e7e68e65aceb54d1a3a32cab697d7b480`. P01-P03 are frozen execution contracts.

## 4. Package execution rule

- P01 → P02 → P03 の順で実行する。
- 各PxxはFROZEN後、assigned Coding AgentがそのPxxのみをnormative implementation authorityとして読む。
- packageごとにfocused verificationとcheckpoint/reportを作成する。
- package interruption/restartだけでTrial番号を増やさない。
- P03 complete後にCandidate Assemblyを実行し、Gate-wide self-verification後にFixed Trial Candidateを固定する。
- PxxはGate PASSを宣言しない。

## 5. Current state

`FROZEN / PLANNING_ONLY / NON_EXECUTABLE`。P00 is planning authority only; execution starts from P01 after Agent Execution Readiness.
