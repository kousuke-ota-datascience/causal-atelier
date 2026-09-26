# ENH-E10 G01 P01 — Model Capability / Optional Dependency

**Document class:** Work Package Execution Contract  
**Status:** `MATERIALIZED_DRAFT / NOT_EXECUTABLE`  
**Gate:** `G01`  
**Package:** `P01`  
**Depends on:** `ENH-E9 final PASS / accepted pre-E10 baseline`  
**Self-containment:** MUST when FROZEN  
**Information isolation:** MUST — after freeze, Coding Agent uses this assigned Pxx as normative implementation authority.  
**Execution eligibility:** `BLOCKED_CONTRACT_NOT_FROZEN`

## 1. Package objective

model capability registry、task compatibility、parameter metadata、optional dependency availability/version/error taxonomyをbounded execution unitとして成立させ、P02へ引き渡せるcheckpointを作る。

## 2. Architecture values required before freeze

model IDs/parameter schema、optional dependency group/version bounds、deterministic metadata、failure taxonomyを06/07と矛盾なく具体化する。Coding Agentに設計判断を委譲しない。

## 3. Required behavior

- provider-neutral model capability descriptorを定義し、task compatibility、parameter schema/default metadata、dependency requirement、availability/version、determinism metadataを機械可読にする。
- existing logistic/linear registry behaviorを保護する。
- LightGBM optional dependencyのavailability discoveryをcore import/startから分離する。
- unavailable model selection、task mismatch、invalid parameterを区別可能なerror taxonomyへ接続する。
- silent fallbackは禁止する。

## 4. Focused verification

- existing logistic/linear registry regression
- task compatibility matrix
- optional dependency absent/import isolation
- parameter validation/error taxonomy

## 5. Protected invariants

- Gate 06/07のsemantic claim / Acceptance Criteriaを変更しない。
- TEST isolation / TRAIN-only preprocessing fitを変更しない。
- unrelated workflowへ変更を広げない。
- test expectationを弱めない。

## 6. Completion boundary

scope内implementation complete、focused verification PASS、package-local blocker NONE、package report作成、exact `PACKAGE_CHECKPOINT_SHA` 固定。terminal stateは `PACKAGE_READY` または明示的 `BLOCKED_*`。PACKAGE_READYはGate PASSではない。
