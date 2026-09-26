# ENH-E10 G02 P03 — LIME Backend / Explanation Integration

**Document class:** Work Package Execution Contract  
**Status:** `MATERIALIZED_DRAFT / NOT_EXECUTABLE`  
**Gate:** `G02`  
**Package:** `P03`  
**Depends on:** `G02 P02 canonical package report = PACKAGE_COMPLETE`  
**Self-containment:** MUST when FROZEN  
**Information isolation:** MUST  
**Execution eligibility:** `BLOCKED_CONTRACT_NOT_FROZEN`

## 1. Package objective

LIME local adapter、sampling/seed/feature representation、unsupported global behavior、artifact/model-card provenance、G01/coefficient protected regressionを統合し、Candidate Assembly可能なG02 stateへ到達する。

## 2. Architecture values required before freeze

LIME local/global policy、discretization/kernel/sample size/features、classification target、feature representation、seed/reproducibility、dependency versionを06/07と一致させる。

## 3. Required behavior

- frozen contractに従いLIME local explanationを実装する。
- instance identity、feature representation、effective seed、sampling/method parametersを保持する。
- global非対応ならexplicit unsupported/not-applicableとしpseudo-globalを生成しない。
- explanation artifact/result/model-card provenanceへSHAP/LIME/coefficientを共通contractで統合する。
- G01 protected model contractとTEST isolationを維持する。

## 4. Focused verification

binary/regression LIME local fixed-seed behavior、global unsupported contract、dependency unavailable、artifact/model-card provenance、G01/coefficient/TEST-isolation regressions。

## 5. Completion boundary

focused verification PASS、G02-wide compatibility self-check可能、package report、exact checkpoint SHA。terminal stateは `PACKAGE_READY` または `BLOCKED_*`。P03 completion後はCandidate Assemblyへ進む。
