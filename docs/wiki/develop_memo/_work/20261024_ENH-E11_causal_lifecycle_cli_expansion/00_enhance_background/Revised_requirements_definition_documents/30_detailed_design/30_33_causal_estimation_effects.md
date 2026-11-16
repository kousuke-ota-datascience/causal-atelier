# 30_33_causal_estimation_effects

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `04d83541e55ab0364500afb4b92ef55c10785a0c`.

---

### 14.5 Estimation

目的は、identified estimandを有限標本データから推定することである。

primary surface:

- selected Identification Resultのcompact prerequisite/reference
- estimator selection
- nuisance model configuration
- bootstrap / uncertainty configuration
- revision / override where supported
- execution submission/status
- estimation result linkage

Identification assumptionをestimator parameterへ埋没させない。Identification/Data Eligibilityの全文説明をEstimationのpage purposeとして再掲しない。

### 14.6 Effects

目的は、保存済みTreatment Effect Resultを読み、effect量とuncertaintyを解釈・比較することである。

primary surface:

- `TREATMENT_EFFECT_RESULT`
- ATE / ATT / CATE等、result schemaが持つeffect payload
- uncertainty / interval
- subgroup / heterogeneity projection
- supported comparison/reference

Diagnosticsと同一primary card/headingを共有しない。
