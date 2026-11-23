# AMD-E11-G01-P04-001 — FCI exhaustive CI eligibility preflight (Owner-selected A; formal 09 candidate)

**Date:** 2026-11-23 JST  
**Gate/Package/Trial:** G01/P04/Trial01  
**Owner design decision:** DEC-G01-P04-CI-ELIG-01 = A_ADOPTED (2026-11-23)  
**Status:** AUTHOR_NORMATIVE_CORRECTION_PREPARED / FORMAL_09_OWNER_APPROVAL_PENDING / S10_REFREEZE_PENDING / S11_REAUTH_PENDING  
**Stopped Coding Agent START_SHA:** 748deb4ba6287bbd1b71e233504c36c6f430e5b7; BLOCKED_CONTRACT_AMBIGUITY; no P04 checkpoint  
**Preexisting frozen S10:** 52e5c60176d6b72c91f839ef267f46657bd380b5  
**Protected P01 checkpoint:** 9bff61f0eae25236f95f31f2cd3e7c81291f0167  
**Protected P03 checkpoint:** 858c9f73366036a2d1445e558135cd521f611462

## 1. Defect and adopted decision

The existing P04 06 §6.4 and G01 07-08 require pre-FCI rejection of insufficient sample/category support but have no exact CI-family-specific predicate or scope of conditioning sets. This is an implementation-observable scientific contract defect originating in the Method detailed design, not a P01/P03 code discrepancy. The Owner adopted A: conservative exhaustive candidate preflight before FCI, rather than instrumenting each actually reached CI call. See combined_review/228_20261123_g01_p04_ci_eligibility_owner_decision_docket.md. The alternative B (lazy CI-call guard) and C (reduce published CI Method scope) are not authorized.

## 2. New bounded normative WHAT

For each distinct unordered observed X/Y variable pair and every conditioning subset of other p-2 variables, including empty and full subset, check before FCI call. The candidate count is C(p,2) * 2^(p-2); do not use depth/max_path_length as a preflight exclusion because the pinned FCI Possible-D-Sep may call beyond FAS depth.

- FisherZ: declared continuous complete finite nonconstant values, n>|S|+3, and finite, positive-definite, reliably invertible sample correlation submatrix on X/Y/S. No Gaussianity/faithfulness/independent rows assertion as fact.
- Chisq/Gsq: exactly declared integer-coded categorical domain values, per each declared S=s combination a supported, nondegenerate X-by-Y contingency table with positive degrees of freedom and independence-null expected count >=5 for each declared X/Y cell; reject absent strata, inadequate expected counts and coercion. Expected-count 5 is a conservative G01 screening floor, not a universally sufficient asymptotic validity proof.
- Unfinished/exhausted/numerically unverifiable preflight is typed unresolved/blocked, never eligible; no Backend FCI invocation, scientific-negative fabrication or publication. No unapproved new public error/exit version. No silent scan truncation. Non-null BK remains separately denied before FCI under existing Backend semantics control.
- The exact fixed computational cap and optional numerical conditioning tolerance are not assigned a made-up number. If positive deterministic admission requires them, flag a distinct limited specification decision; an incomplete or numerically uncertain input must remain blocked, not quietly accepted.

## 3. Cross-layer files and scope

Revised:
- 30_detailed_design/30_63_causal_method_adapters.md — Method-specific design authority with exhaustive preflight predicate, qualifications and independent science limitations.
- 10_enhance_instruction/G01/06_G01_P04_fci_backend_oracle.md — identical bounded execution responsibility.
- 10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md — independent n/|S|, E=5 boundary, sparse conditioned stratum, numerical singularity and no partial scan acceptance tests.

Reviewed for semantic invariance; unchanged: 10_13, 10_32, 10_91; 21_41; 22_06; 23_41; 30_61/30_62; P01/P02/P03/P05 06; public E11 versioned wire, legacy Product v2, optional Backend selection. This is an implementation-specific quantitative eligibility tightening, not a new generic LDD field, public request key, extra science-positive guarantee or Graph output type. The approved A policy is localized to P1-M06. Independent G01-07-09/10, G01_999, BK non-null guards, MAG/PAG oracle and Product regression remain mandatory.

## 4. Compatibility and accepted-risk boundary

FCI preflight may reject previously schema-valid sparse datasets; that is a behavioral eligibility restriction, not a public wire format change. All three permitted CI choices remain. The all-subsets count is exponential, so for high-p inputs successful admission cannot be promised at any implicit runtime or memory bound. The Owner selection A favors fail-closed conservative admission over an unbounded performance guarantee. No changes were made to completed P01/P03 code, tests, 06/07, or checkpoint commits; no existing Package modification is requested. P02 Reader's separately approved provenance compatibility correction is unaffected.

## 5. Verification and release control

Boundary cases: fisherz n=|S|+3 reject, n=|S|+4 only algebraic candidate; singular or numerically unstable correlation reject/block; expected discrete count E=5 candidate vs E<5 reject; marginally well-supported but conditional-sparse reject; balanced categorical full support positive; missing declared stratum reject; depth=0 does not reduce all-subsets screen; incomplete exhaustion must fail before Backend invocation; typed error routing and no scientific-negative translation. Runtime Python3.12 effective Backend fit and independent science Oracle are still not tested by this document update.

Formal Owner approval of this exact AMD-E11-G01-P04-001 proposal is required, followed by a separately recorded provisional S10 refreeze at the final full Git SHA and another separate limited S11 coding authorization. Neither the Owner's earlier selection of A nor this author document is itself formal 09, S10 or S11. Do not resume P04 Trial01 under the prior S10/S11.
