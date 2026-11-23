# 237 — ENH-E11 G01/P04/Trial01 Fisher-Z numerical reliability ambiguity — Owner decision docket

**Date:** 2026-11-23 JST  
**Decision requested:** `DEC-G01-P04-FISHERZ-NUMERIC-01`  
**Status:** `OWNER_SCIENTIFIC_NUMERICAL_ACCEPTANCE_DECISION_PENDING / NON_NORMATIVE_DOCKET`  
**Classification:** `CONTRACT_AMBIGUITY / FISHERZ_NUMERICAL_RELIABILITY_UNDEFINED`  
**Agent START_SHA:** `b9910c9a382241a9a850fc57579badb9ccfa8b11`  
**Frozen G01-S10:** `3a63caa2d58c76c7f4289593713ee5c437e4ec91`  
**Approved prior S11:** `DEC-G01-P04-002-S11-REAUTH-01`  
**Completed P01:** `9bff61f0eae25236f95f31f2cd3e7c81291f0167`  
**Completed P03:** `858c9f73366036a2d1445e558135cd521f611462`  
**P04 checkpoint:** none (Agent reports no files changed).

> Non-normative technical assessment and Owner decision options. This document changes no existing frozen DD, 06, 07, 09 or published Schema. It is **not** new authorization to resume Coding. A new numerical acceptance boundary requires explicit Owner adoption, formal 09, a separate revised S10 and S11.

## 1. Verified source authority and root cause

The approved `AMD-E11-G01-P04-001` and `30_63_causal_method_adapters.md` §4.4 require, for every unordered observed pair `X,Y` and every conditioning subset `S` of remaining variables, a finite positive-definite empirical correlation submatrix `R_{X,Y,S}`, `n>|S|+3`, and **reliably invertible** numerical conditioning before *any* FCI call. The strict preflight must fail closed if reliability cannot be verified; an arbitrary unapproved conditioning cutoff is explicitly prohibited. P04 `06` repeats these rules; G01 `07` demands singular/near-singular boundary negatives.

Neither the frozen Method contract nor its scientific requirements fix a quantitative reliability target, error bound, condition-number criterion or reference implementation for the challenging case in which Cholesky and `np.linalg.inv` both succeed. This is a missing Method numerical acceptance policy, not a P01/P03 implementation mismatch. Modifying the 07 expected result to match current numerical behavior would be improper.

Primary Backend evidence: `py-why/causal-learn` tag `0.1.4.8`, `causallearn/utils/cit.py`, `FisherZ.__call__` computes `np.linalg.inv(sub_corr_matrix)`, derives a partial correlation from inverse entries and, when `|r|>=1`, clips it to `(1-eps)*sign(r)`. It catches `LinAlgError` for singular matrices but does not establish a numerical forward-error bound. The clipping route illustrates that successful Backend completion is **not** proof that the underlying partial correlation and resulting p-value are reliable. The Agent independently confirmed actual Python 3.12.16, causal-learn 0.1.4.8 and FCI node_names signature, but **did not fit FCI**.

## 2. Independent numerical evidence and interpretation

Given the Agent's two columns `x=[-3,-2,-1,1,2,3]` and `x+eps*z` with `z=[1,-1,1,-1,1,-1]`, their 2-by-2 sample correlation matrices produce approximately:

| eps | cond2(R) | cond2(R) × u (u=2.220446049250313e-16) |
| --- | ---: | ---: |
| 1e-4 | 2.06e9 | 4.58e-7 |
| 1e-6 | 2.07e13 | 4.60e-3 |
| 1e-7 | 2.16e15 | 4.80e-1 |

These are independent **local numpy calculations on the synthetic example**, not FCI tests or measured forward errors. The condition-times-epsilon heuristic is a sensitivity/risk indicator under finite-precision backward-stability assumptions, not by itself a certified bound on Fisher-Z p-value error, accuracy of underlying input covariance, statistical power, or causal validity. A small computed inverse residual can coexist with a huge condition number and does not establish an accurate computed inverse or accurate p-value.

## 3. Owner decision options

### A — Recommended for consideration: explicit conservative double-precision condition budget

Adopt a numerical screening contract in addition to existing complete/finite/variance and `n>|S|+3` rules:

1. Verify correlation construction using the **same data dtype/order and `np.corrcoef`-compatible semantics** as the selected effective Backend; reject nonfinite, non-symmetric (beyond the approved floating-point comparison policy), and any non-positive-definite submatrix. A successful Cholesky factorization is necessary but not sufficient.
2. Compute a *finite, nonnegative, independently checked* 2-norm condition number `kappa2(R)` using singular values or a stable condition estimator; reject failure, NaN/Inf or rank-deficient input. Do not infer accuracy just from successful `inv`.
3. Define `u = np.finfo(np.float64).eps` (machine epsilon, **not** unit roundoff 0.5*eps), and **accept the conditioning-budget portion only if `kappa2(R) * u <= 1e-6`** for **every** enumerated triple. The numeric budget `1e-6` is a **proposed**, previously unapproved engineering/scientific screening threshold. It indicates a conservative approximate six-decimal-digit inverse sensitivity budget under standard assumptions; it is *not* an absolute/relative forward-error certification or guarantee of accurate Fisher-Z p-values.
4. Require finite inverse and partial-correlation intermediate values, independently verify `R @ inv(R)` and `inv(R) @ R` residual consistency with a **separately approved numerical residual rule** (a candidate is `max(||R I_R-I||inf,||I_R R-I||inf) <= 1e-8`; also **not yet approved**). Ensure `|partial_r|<1` without relying on the Backend's `|r|>=1` clipping to turn a near-singular case into a false positive. The inverse residual is only a supplemental necessary diagnostic, not a substitute for conditioning.
5. If the declared numeric check cannot be computed reliably, return typed pre-FCI **eligibility-unresolved** fail-closed with no FCI invocation, no false Graph/Marker, no `SCI_NO_ADMISSIBLE_PAG`, no new public error code.

A true forward-error guarantee for partial correlations/p-values would require independent precision/error analysis and potentially a different Backend algorithm; **A is a conservative eligibility heuristic, not a certified numerical accuracy guarantee**. If Owner desires strict error certification, choose B. Fixed compute-budget/cap remains separate and is not silently resolved by A.

Implication for the Agent's three examples: every one of `eps=1e-4/1e-6/1e-7` breaches the candidate `kappa2*u<=1e-6`? **No:** `1e-4` yields `4.58e-7`, which *passes* that **one numerical threshold**; `1e-6` and `1e-7` fail. This does not imply that a full Dataset is globally eligible: all X/Y/S matrices and other checks must pass. Independent fixture tests must include correctly constructed condition-budget pass/fail cases and values directly on both sides of the explicit boundary, plus singular, nonfinite, invalid n, and `|partial_r|>=1` cases.

### B — precision-certified acceptance (more rigorous, larger scope)

Require a computed, independent high-precision/reference partial correlation/p-value and independently bounded error, with explicit maximum accepted error in p-value or partial correlation (and a documented precision-escalation algorithm), in addition to all-subsets preflight and effective Backend compatibility. Would require independent choice of precision, absolute vs relative p-value tolerance, cross-library equivalence, and usually a larger implementation/test scope; no such threshold/reference is currently authorized. This is scientifically stronger when a real accuracy guarantee is essential but not a minimal P04 contract correction.

### C — algebraic decomposition only (not recommended without material contract relaxation)

Treat finite strict positive-definiteness, Cholesky and successful `np.linalg.inv` as sufficient. This produces an implementable algorithm without introducing a numerical cutoff but does **not** establish the already-required numerical reliability. It can pass very ill-conditioned cases and risks erroneous partial correlations and p-values. It would require an explicit **relaxation** of the current scientific/Method acceptance meaning and is **not** a valid automatic editorial correction.

## 4. Precision and residual choices still requiring exact approval

If A is chosen, the Owner must approve **both** the conditioning budget (candidate `kappa2*np.finfo(np.float64).eps<=1e-6`) and the supplemental inverse-residual check (candidate absolute infinity-norm tolerance `<=1e-8`), or direct a different explicit quantitative rule; do not treat suggested values as inherited scientific requirements. Decide whether eigenvalue/partial-correlation roundoff checks should be strict and fail-closed (recommended) and confirm `float64` as the effective numerical dtype (candidate). Do not confuse machine epsilon with unit roundoff or assert p-value precision from matrix residual alone. The full-sample `np.corrcoef` and conditioned submatrix checks must agree with effective pinned Backend; exact algorithm is implementation-level after acceptance rules are approved.

## 5. Exact minimal amendment footprint after Owner decision

Expected normative change **only**:
- `00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md` §4.4: method-specific numeric eligibility acceptance authority and limitation, without changing higher RD/BD/IF public semantics.
- `10_enhance_instruction/G01/06_G01_P04_fci_backend_oracle.md` §6.4: deterministic numerical preflight algorithm aligned to DD.
- `10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md` G01-07-08: independent boundary cases/negative reference, no mock-based scientific PASS.
- `10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P04-003_Gate_Contract_Amendment.md`: formal 09 **candidate**.
- This `combined_review/237` decision evidence and a later explicit Owner adoption record.

Expected **unchanged**: existing FR/AR, LDD, BD, IF, versioned public Study/Graph/Manifest schemas, category-domain contract `AMD-002`, all `chisq/gsq` eligibility, Product v2, `uv.lock`, completed P01/P03 code/06/07/tests/checkpoint, P02/P05 code, other Methods/Gates, independent MAG/PAG/BK science and G01_999 obligations.

## 6. Control-plane release sequence

Request explicit `DEC-G01-P04-FISHERZ-NUMERIC-01` Owner decision on A with actual numeric values or a different option. Author can then prepare the bounded DD→06→07→AMD-003 candidate. Require **separate formal 09 Owner approval** of the final new normative delta, **separate S10 Owner refreeze** on the new complete immutable Git SHA including 09 approval record, then **separate S11 Owner coding reauthorization**. The current S10 `3a63caa2d58c76c7f4289593713ee5c437e4ec91` and S11 `DEC-G01-P04-002-S11-REAUTH-01` do not authorize changed numeric-eligibility behavior.

The current Agent reported no P04 code or checkpoints and did not run full FCI. A docket-only commit is not a test or an independent science PASS.
