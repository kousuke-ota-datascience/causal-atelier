# 30_34_causal_diagnostics_sensitivity

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `04d83541e55ab0364500afb4b92ef55c10785a0c`.

---

### 14.7 Diagnostics

目的は、推定の支持条件・安定性・diagnostic warningを確認することである。

primary surface:

- `DIAGNOSTICS_RESULT`
- balance
- overlap
- effective sample size
- weight diagnostics
- scientific warning

Effects Resultをprerequisite/referenceとして参照してよいが、Effect comparisonをDiagnosticsのpage purposeにしない。

### 14.8 Sensitivity

目的は、推定結果が仮定・仕様変更に対してどの程度頑健かを確認することである。

primary surface:

- target Treatment Effect Result reference
- `REFUTATION_RESULT`
- `SENSITIVITY_RESULT`
- Refutation control/result
- Sensitivity control/result
- alternate assumption/specification依存性
- robustness interpretation

Refutation/Sensitivity operation controlはSensitivity Stageのみが所有する。Identification / Estimation / Effects / Diagnosticsではこれらをeditable controlとして表示しない。

### 14.9 Causal visibility matrix

| Surface | identification | estimation | effects | diagnostics | sensitivity |
| --- | ---: | ---: | ---: | ---: | ---: |
| Identification purpose/input/action | ON | OFF | OFF | OFF | OFF |
| Identification / Eligibility / Gate result | ON | compact prerequisite/reference | OFF | OFF | OFF |
| Estimation config/action | OFF | ON | OFF | OFF | OFF |
| Treatment effect primary result/comparison | OFF | compact completion/reference | ON | optional reference | prerequisite reference |
| Diagnostics result/warnings | OFF | OFF | OFF | ON | optional prerequisite/reference |
| Refutation controls/results | OFF | OFF | OFF | OFF | ON |
| Sensitivity controls/results | OFF | OFF | OFF | OFF | ON |

### 14.10 Causal presentation guidance

Causal Stageのprimary purpose summaryは日本語を基本とする。ATE、ATT、CATE、estimand、overlap、ESS等、実装・分析概念との対応上英語が明確な専門語は英語を維持してよい。

説明文から、少なくとも次を理解できること。

- このStageで何を判断・閲覧するか
- 前後Stageと何が異なるか
- current operationがscientific executionかsaved Result readか

---
