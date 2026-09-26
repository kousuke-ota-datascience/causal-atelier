# ENH-E10 G02 P00 — Work Package Plan

**Document class:** Work Package Planning Contract  
**Status:** `MATERIALIZED_DRAFT / PLANNING_ONLY / NON_EXECUTABLE`  
**Gate:** `G02`  
**Execution mode:** `WORK_PACKAGE`  
**Gate dependency:** `G01 PASS`  
**Authority:** Gate 06/07 define semantics and acceptance; P00 only defines execution decomposition.

## 1. WP adoption decision

共通Explanation contractを先に固定し、その上へSHAPとLIMEを載せる依存DAGがある。SHAPとLIMEはfailure mode・scientific semantics・optional dependencyが異なり、個別focused verificationが必要なため、G02はWork Package modeを採用する。

## 2. Package map

| Package | Scope | Dependency |
|---|---|---|
| P01 | Explanation Capability / Canonical Contract | G01 PASS |
| P02 | SHAP Backend | P01 PACKAGE_COMPLETE |
| P03 | LIME Backend / Explanation Integration | P02 PACKAGE_COMPLETE |

## 3. Architecture Review resolution

Technical decisions are resolved and materialized into 06/07/P01-P03: method IDs/compatibility, SHAP raw-output semantics and additivity, LIME local-only defaults/reference strategy, optional dependency bounds, v1 additive explanation schemas, and failure taxonomy.

Remaining freeze blocker: **Human Architecture Review approval** plus required requirement/design application.

## 4. Package execution rule

P01 → P02 → P03。各PxxはFROZEN後にassigned Coding Agentへ渡す。Pxx completionはGate PASSではない。P03 complete後にCandidate Assemblyを行う。

## 5. Current state

`MATERIALIZED_DRAFT`。06/07/P01-P03と同一batchでfreezeする。
