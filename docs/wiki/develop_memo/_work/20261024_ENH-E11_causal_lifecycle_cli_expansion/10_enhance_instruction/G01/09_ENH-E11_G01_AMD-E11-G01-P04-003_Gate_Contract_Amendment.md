# AMD-E11-G01-P04-003 — P1-M06 Fisher-Z float64 numerical eligibility contract

**Date:** 2026-11-23 JST  
**Gate / Package / Trial:** `G01/P04/Trial01`  
**Classification:** `METHOD_NUMERICAL_ELIGIBILITY_CONTRACT_GAP`  
**Owner decision:** `DEC-G01-P04-FISHERZ-NUMERIC-01=A_ADOPTED`  
**State:** `AUTHOR_PREPARED_FORMAL_09_CANDIDATE / FORMAL_09_OWNER_APPROVAL_PENDING / S10_REFREEZE_PENDING / S11_REAUTH_PENDING`  
**Last stopped Agent START_SHA:** `b9910c9a382241a9a850fc57579badb9ccfa8b11`  
**Prior frozen G01 S10:** `3a63caa2d58c76c7f4289593713ee5c437e4ec91`  
**Prior S11:** `DEC-G01-P04-002-S11-REAUTH-01` (does not cover this new numerical acceptance boundary)  
**Protected P01:** `9bff61f0eae25236f95f31f2cd3e7c81291f0167`  
**Protected P03:** `858c9f73366036a2d1445e558135cd521f611462`  
**P04 checkpoint:** none

## 1. Root cause, higher-level authority and bounded change

Existing `AMD-E11-G01-P04-001`, DD `30_63` §4.4, P04 `06` §6.4 and G01 `07` require finite, positive-definite and **reliably invertible** Fisher-Z correlation submatrices in an exhaustive pre-FCI screen. They do not prescribe a quantitative acceptance criterion when Cholesky and inversion both succeed for an ill-conditioned matrix. Backend's `causal-learn 0.1.4.8` `FisherZ.__call__` uses `np.linalg.inv` and may clip computed `|r|>=1`, neither of which guarantees numerical reliability. The root defect is the missing **Method-specific numerical policy**, not a fault in completed P01/P03 or permission to water down independent test expectations.

Owner adopted precisely A in `DEC-G01-P04-FISHERZ-NUMERIC-01`; see `combined_review/237_20261123_g01_p04_fisherz_numerical_reliability_owner_decision_docket.md` for evidence and alternatives and `combined_review/238_20261123_g01_p04_fisherz_numeric_A_owner_adopted.md` for the explicit decision.

## 2. Normative Fisher-Z acceptance contract

For `P1-M06/fisherz` only and **every** unordered distinct observed pair `(X,Y)` and every conditioning subset `S` of all other observed columns (including `S=empty` and `|S|=p-2`, independent of configured depth), before any FCI call:

1. Require declared CONTINUOUS, complete, finite, nonconstant numerical observations and `n>|S|+3`. The numeric reference is `float64` using the verified ordered Dataset, with the **full-sample** correlation `R_full` produced compatibly with the selected effective `causal-learn` Fisher-Z `np.corrcoef(data.T)`. `R` is the corresponding full-correlation principal submatrix ordered `[X,Y,*ordered(S)]` with no different subset-wise re-estimation.
2. All `R` entries must be finite and `R` must be strictly positive-definite (successful Cholesky). Establish a finite 2-norm condition number `kappa2(R)` and require **`kappa2(R)*np.finfo(np.float64).eps <= 1e-6`**, inclusive. `np.finfo(np.float64).eps` is machine epsilon `2.220446049250313e-16`, not half that number.
3. Compute the float64 inverse `W=inv(R)`; require finite entries and both finite matrix-products `R@W`, `W@R`. Both absolute matrix residual infinity norms must satisfy **`max(||R@W-I||_inf, ||W@R-I||_inf) <= 1e-8`**, inclusive; matrix infinity norm is **maximum row sum of absolute residuals**, not maximum individual element.
4. Derive `r=-W[0,1]/sqrt(W[0,0]*W[1,1])` for `X,Y` first in the ordered submatrix. Require a finite **strictly positive** denominator, finite `r`, **`abs(r)<1`**, and finite derived Fisher-Z transform, statistic and p-value if evaluated. Never convert a numerically invalid value to accepted input by relying on the Backend's `abs(r)>=1` clipping.
5. Failed algebraic or numerical tests, a numerical calculation that cannot be completed reliably, NaN/Inf/overflow, an incomplete exhaustive scan, and resource exhaustion are **pre-FCI typed reject/unresolved** with no Backend invocation, Graph, success Marker or relabeling to `SCI_NO_ADMISSIBLE_PAG`. Reuse already-approved typed technical/eligibility families, no newly invented public exit code.

These numerical thresholds are **Owner-authorized conservative screening heuristics**, not guaranteed inverse forward-error or Fisher-Z p-value accuracy bounds and not proof of independent sampling, Gaussianity, Markov or faithfulness. If a user requires certified p-value accuracy or additional precision, that is a separate scientific approval, not inferred from this contract.

## 3. Required independent checks

G01-07-08 must independently reproduce all pair/subset screening results and the exact two finite-precision inequalities, including inclusive boundary comparisons, well-conditioned positive data and real effective Backend fit separately. Negative cases: `n=|S|+3`, rank deficient, nonfinite, Cholesky-failure, Cholesky/inversion-success but condition-budget failure, inverse-residual-only failure, `abs(r)>=1`/nonfinite partial r, incomplete enumeration, and a failed candidate even when FAS `depth=0`. Check `np.linalg.norm(..., ord=np.inf)` row-sum semantics rather than an entrywise maximum. Agent's two-column synthetic near-collinear examples give a useful **condition-budget diagnostic** (roughly `4.58e-7, 4.60e-3, 4.80e-1`), not a claim of full dataset or fitted-FCI acceptance. Tests may use separately constructed small matrix fixtures for exact comparator behavior, but integration cases must verify **actual** float64 Dataset-to-R-to-full-FCI path. Every rejected input must call FCI zero times. G01-07-09/10 and independent G01_999 remain unchanged.

## 4. Exact document scope and compatibility

**Changed normative documents:**
- `00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md`
- `10_enhance_instruction/G01/06_G01_P04_fci_backend_oracle.md`
- `10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md`

**New control-plane evidence:** `combined_review/237_20261123_g01_p04_fisherz_numerical_reliability_owner_decision_docket.md`, `combined_review/238_20261123_g01_p04_fisherz_numeric_A_owner_adopted.md`, and this AMD-003 formal 09 candidate.

**Intentionally unchanged:** RD `10`, LDD `21`, BD `22`, IF `23` public and internal schemas, `e11-local-*/1` wire versions, `uv.lock`, P1-M06 `category_codes` contract, `chisq/gsq` CI and category expected-count policy, P01/P02/P03/P05 implementation and instructions, Product v2, other Methods/Gates, independent MAG/PAG/BK oracle, T2/T3, real Python3.12/backend, regression and G01_999. The only compatibility effect is a stricter **Method-specific numerical eligibility** outcome for some continuous data; the request/output wire shapes are unaltered.

P01/P03 protected checkpoint commits remain fixed and must not be edited or reinterpreted as evidence that a P04 numerical screening implementation is present. The currently blocked Trial01 has no P04 checkpoint or implementation changes. Fixed computational-enumeration resource bounds remain unspecified under the earlier fail-closed policy; this AMD resolves only the numerical reliability decision.

## 5. Explicit release control

**Formal 09 is NOT granted merely by this document or Owner A scientific selection.** Require distinct Owner formal `AMD-E11-G01-P04-003` 09 approval. Then prepare the exact complete Git SHA **including the future 09 approval record**, obtain separately approved revised G01 S10, and separately issue limited G01/P04/Trial01 S11 reauthorization at that immutable SHA. The existing S10 `3a63caa2d58c76c7f4289593713ee5c437e4ec91` and S11 `DEC-G01-P04-002-S11-REAUTH-01` do not permit implementation of revised numerical acceptance.

This document does not assert FCI fit, test PASS, source checkpoint, independent science acceptance or Gate999 PASS.
