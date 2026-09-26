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

## 2. Effective architecture values

- method = `LIME_TABULAR`; local-only.
- supported models = existing logistic/linear and new LightGBM classifier/regressor.
- representation = preprocessed feature space matching model `feature_order`.
- binary explains positive-class probability; regression explains numeric prediction.
- TRAIN-derived `predictive-explanation-reference/1`: deterministic sample without replacement, max 500 rows, seed = explanation sampling seed.
- persist reference hash/count/seed/provenance only; raw reference rows remain runtime bindings.
- defaults: num_samples=2000, num_features=min(10,n_features), feature_selection=auto, discretize_continuous=false, distance_metric=euclidean, kernel_width=0.75*sqrt(n_features), sample_around_instance=false.
- one-hot outputs are categorical binary features; record perturbation-validity limitation.
- derive independent deterministic effective seed per explained row from sampling seed + row identity.
- global request or local_explanations=false => `EXPLANATION_SCOPE_NOT_SUPPORTED`.
- LIME version = `0.2.0.1`.

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
