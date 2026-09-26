# ENH-E10 G02 P01 — Explanation Capability / Canonical Contract

**Document class:** Work Package Execution Contract  
**Status:** `MATERIALIZED_DRAFT / NOT_EXECUTABLE`  
**Gate:** `G02`  
**Package:** `P01`  
**Depends on:** `G01 PASS`  
**Self-containment:** MUST when FROZEN  
**Information isolation:** MUST  
**Execution eligibility:** `BLOCKED_CONTRACT_NOT_FROZEN`

## 1. Package objective

method capability registry、model-method compatibility、global/local contract、canonical result/provenance、optional dependency semantics、coefficient compatibilityを成立させ、P02へ引き渡す。

## 2. Architecture values required before freeze

method IDs、compatibility matrix、canonical result schema、optional dependency/version metadata、failure taxonomyを06/07と一致させる。

## 3. Required behavior

- explanation method capability registryを定義し、method identity/version、global/local support、dependency availability、required model interfaceを表現する。
- G01 model capabilityとmodel-method compatibilityをbackend authorityで照合する。
- canonical explanation result/provenance contractを定義し、provider raw objectをpublic canonical truthにしない。
- existing LINEAR_COEFFICIENT_CONTRIBUTION behavior、feature-order rejection、predictive-not-causal boundaryを保護する。
- unavailable/unsupported/incompatibleをsilent fallbackせず区別する。

## 4. Focused verification

coefficient global/local regression、compatibility matrix、negative cases、dependency availability semantics、canonical result/provenance contract。

## 5. Completion boundary

focused verification PASS、package report、exact checkpoint SHA、blocker NONE。terminal stateは `PACKAGE_READY` または `BLOCKED_*`。
