# 239 — G01/P04 AMD-E11-G01-P04-003 formal 09 Owner approval

**Date:** 2026-11-23 JST  
**Decision ID:** `DEC-G01-P04-003-09-APPROVE-01`  
**Status:** `FORMAL_09_OWNER_APPROVED / S10_REFREEZE_PENDING / S11_REAUTH_PENDING`  
**Repo:** `kousuke-ota-datascience/causal-atelier`  
**Branch:** `feature/ariadne_mvp_e11`

## 1. Owner authorization and immutable approval target

Owner explicitly authorized:

> AMD-E11-G01-P04-003の正式09改訂案を承認する。DEC-G01-P04-FISHERZ-NUMERIC-01=Aに基づくFisher-Zのfloat64数値適格性基準と、詳細設計30_63・P04 Coding Instruction 06・G01 Test Instruction 07の改訂を正式契約として承認せよ。P01/P03チェックポイント、公開E11 Schema Version、既承認の科学的意味、独立科学検証・G01_999受入条件を維持する。

**Exact pre-approval-record content SHA:** `c664829c7cbc5ae6f43c74c3c649db28be2425d2`  
**Amendment:** `10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P04-003_Gate_Contract_Amendment.md`  
**Owner numerical policy:** `DEC-G01-P04-FISHERZ-NUMERIC-01=A_ADOPTED` (record `combined_review/238_20261123_g01_p04_fisherz_numeric_A_owner_adopted.md`, supported by docket `237`).  
**Previous frozen S10:** `3a63caa2d58c76c7f4289593713ee5c437e4ec91`.

## 2. Approved numerical WHAT (P1-M06 / Fisher-Z only)

Retain the previously approved pre-FCI enumeration of every unordered observed pair `X,Y` and every conditioning subset `S`. For each float64 empirical correlation principal submatrix `R`, with full-correlation construction compatible with the effective causal-learn Fisher-Z Backend, require:

1. Complete finite continuous observations, `n > |S|+3`, finite `R` and strict positive definiteness (Cholesky succeeds).
2. Finite `kappa2(R)`, `kappa2(R) * np.finfo(np.float64).eps <= 1e-6`, inclusive. The epsilon is NumPy float64 machine epsilon, not half epsilon.
3. Finite inverse `W=inv(R)` and both residual products finite; `max(||R@W-I||_inf, ||W@R-I||_inf) <= 1e-8`, inclusive. These norms mean maximum absolute row sum, not largest entry.
4. Finite intermediate quantities, finite positive denominator, partial `r=-W[0,1]/sqrt(W[0,0]*W[1,1])` with `|r|<1` strictly; no accepting invalid results via Backend clipping.
5. Any failed/undefined/unreliable computation or incomplete screening blocks *before* FCI; no fabricated PAG/Graph, Marker or `SCI_NO_ADMISSIBLE_PAG` and no unapproved new public wire/exit code.

The adopted bounds are conservative **eligibility screening thresholds**, not certified partial-correlation/inverse forward accuracy or p-value accuracy, and not causal validity proofs.

## 3. Exact approved diff and invariants

Compared at approval against last blocked Coding Agent START_SHA `b9910c9a382241a9a850fc57579badb9ccfa8b11`, HEAD `c664829c7cbc5ae6f43c74c3c649db28be2425d2` differed in precisely these 6 files:

- `00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md` (modified).
- `10_enhance_instruction/G01/06_G01_P04_fci_backend_oracle.md` (modified).
- `10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md` (modified).
- `10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P04-003_Gate_Contract_Amendment.md` (added).
- `00_enhance_background/Revised_requirements_definition_documents/combined_review/237_20261123_g01_p04_fisherz_numerical_reliability_owner_decision_docket.md` (added).
- `00_enhance_background/Revised_requirements_definition_documents/combined_review/238_20261123_g01_p04_fisherz_numeric_A_owner_adopted.md` (added).

All of the following commits were ancestors with `behind_by=0`: prior S10 `3a63caa2d58c76c7f4289593713ee5c437e4ec91`, protected P01 `9bff61f0eae25236f95f31f2cd3e7c81291f0167`, protected P03 `858c9f73366036a2d1445e558135cd521f611462`.

This formal 09 approval does **not** change completed P01/P03 implementation, their 06/07 or checkpoint; does not change public E11 Schema Version, Product v2, `uv.lock`, P1-M06 categorical `category_codes` semantics, `chisq/gsq` expected-count policy or the existing PAG/Graph/BK scientific meaning. It does not relieve the future Agent of actual Python3.12/Backend numerical verification or independent MAG/PAG/BK Oracle, T2/T3, regression and G01_999 obligations.

## 4. Distinct pending approvals

**Formal 09 only** is approved. A **separate Owner S10 refreeze** on a new exact Git SHA **including this approval record**, then a distinct **Owner S11 limited Coding Authorization** for `G01/P04/Trial01` at that frozen SHA remain mandatory. This approval-record commit is administrative and does not retroactively modify the content SHA approved here.

No P04 code, focused-test results, FCI fit, checkpoint, science PASS or downstream Gate unlock is asserted.
