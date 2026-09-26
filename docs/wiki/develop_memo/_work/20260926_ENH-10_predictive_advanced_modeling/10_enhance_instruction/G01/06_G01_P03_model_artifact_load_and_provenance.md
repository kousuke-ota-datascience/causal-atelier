# ENH-E10 G01 P03 — Model Artifact / Load / Provenance Integration

**Document class:** Work Package Execution Contract  
**Status:** `MATERIALIZED_DRAFT / NOT_EXECUTABLE`  
**Gate:** `G01`  
**Package:** `P03`  
**Depends on:** `G01 P02 canonical package report = PACKAGE_COMPLETE`  
**Self-containment:** MUST when FROZEN  
**Information isolation:** MUST  
**Execution eligibility:** `BLOCKED_CONTRACT_NOT_FROZEN`

## 1. Package objective

durable serialization/load、feature/preprocessor identity、runner integration、provenance、existing linear protected regressionを成立させ、Candidate Assembly可能なG01 implementation stateへ到達する。

## 2. Architecture values required before freeze

artifact schema/version、provider serialization format、loader dispatch、feature/preprocessor identity contract、provenance fields、predictive spec revision decisionを06/07と一致させる。

## 3. Required behavior

- provider modelをdurable artifactへserializeし、fresh-process相当のloader dispatchからpredict可能にする。
- feature order/name、preprocessor identity、model/task identity、provider/library version、parameters、seedをartifact/provenanceへ結び付ける。
- serialize/load前後prediction parityを検証する。
- existing linear fitted-model read/use behaviorを保護する。
- runner/result/model-card integrationをGate-wide contractへ接続する。

## 4. Focused verification

- binary/regression serialize → load → predict parity
- feature/preprocessor mismatch rejection
- provenance/artifact/model-card audit
- existing logistic/linear protected integration regression
- optional dependency absence regression

## 5. Protected invariants

P01/P02 semantics、TEST isolation、existing fitted model compatibility、no mandatory LightGBM、no silent fallback。

## 6. Completion boundary

focused verification PASS、G01-wide integration self-check可能、package report + exact checkpoint SHA。terminal stateは `PACKAGE_READY` または `BLOCKED_*`。P03 completion後はCandidate Assemblyへ進む。
