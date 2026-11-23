# 241 — G01/P04 AMD-E11-G01-P04-003 limited S11 Owner Coding Authorization

**Date:** 2026-11-23 JST  
**Decision ID:** `DEC-G01-P04-003-S11-REAUTH-01`  
**State:** `S11_OWNER_APPROVED / G01_P04_TRIAL01_LIMITED_CODING_AUTHORIZED / G01_999_NOT_PASSED`  
**Repository:** `kousuke-ota-datascience/causal-atelier`  
**Working branch:** `feature/ariadne_mvp_e11`

## 1. Explicit Owner authorization and immutable contract

Owner's instruction:

> DEC-G01-P04-003-S11-REAUTH-01を承認する。AMD-E11-G01-P04-003に基づくG01-S10凍結SHA cbfdbdd6b91f3a2f889fe9b62c2a4ab286da6132 を対象に、G01/P04/Trial01の限定Coding Authorizationを再発行せよ。P01チェックポイント9bff61f0eae25236f95f31f2cd3e7c81291f0167、P03チェックポイント858c9f73366036a2d1445e558135cd521f611462、公開E11 Schema Version、既承認の科学的意味、独立科学検証・G01_999受入条件を維持する。

**Frozen normative G01-S10 SHA:** `cbfdbdd6b91f3a2f889fe9b62c2a4ab286da6132`.

**Strict execution scope:** `GATE_ID=G01`, `PACKAGE_ID=P04`, `TRIAL_NO=01` only. This is a distinct S11 approval following `AMD-E11-G01-P04-003` formal09 and the new S10. Earlier S11 authorization `DEC-G01-P04-002-S11-REAUTH-01` applies to an older S10 and is not the current normative coding authority.

## 2. Verified entry control-plane facts

Prior to this record's creation, branch HEAD was `65afd9b21d05cbf5c9a79229cbca4db1014f2022`. GitHub compare found:
- Frozen S10 `cbfdbdd6b91f3a2f889fe9b62c2a4ab286da6132` is ancestor, ahead 1, behind 0; the sole post-freeze change was `combined_review/240_20261123_g01_p04_003_s10_owner_refreeze.md`.
- Protected P01 `9bff61f0eae25236f95f31f2cd3e7c81291f0167` is ancestor, ahead 64, behind 0.
- Protected P03 `858c9f73366036a2d1445e558135cd521f611462` is ancestor, ahead 29, behind 0.
- Previous S10 `3a63caa2d58c76c7f4289593713ee5c437e4ec91` is ancestor, ahead 10, behind 0.
- Owner formal09 `DEC-G01-P04-003-09-APPROVE-01` is recorded in `combined_review/239_20261123_g01_p04_003_formal_09_owner_approved.md` and Owner S10 `DEC-G01-P04-003-S10-REFREEZE-01` in `combined_review/240_20261123_g01_p04_003_s10_owner_refreeze.md`.

The eventual commit creating this S11 record is administrative and not itself a new S10 frozen SHA; no branch HEAD movement automatically alters the frozen normative contract.

## 3. Limited implementation and test authorization

Authorize only G01/P04/Trial01 coding and developer verification against all applicable frozen RD/BD/IF/DD plus `10_enhance_instruction/G01/06_G01_P04_fci_backend_oracle.md`, `10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md`, `30_detailed_design/30_63_causal_method_adapters.md`, and `09_ENH-E11_G01_AMD-E11_G01_P04-001`, `002`, `003`.

Specifically:
- Preserve AMD-001 exhaustive pre-FCI screening of every unordered pair (X,Y) and every subset S without trimming by configured `depth` or `max_path_length`. Incomplete enumeration, unavailable resources or otherwise undecidable eligibility must fail closed, without invoking FCI or issuing a false scientific-negative.
- Preserve AMD-002 strict internal categorical `Design.variables[].category_codes` universe and exact integer-coded observed Dataset membership; unobserved declared levels and absent full-Cartesian conditioned strata remain in screen; `chisq/gsq` expected count floor >=5 retains its original meaning.
- Apply AMD-003 Fisher-Z float64 full-sample correlation and principal-submatrix construction compatible with the installed effective Backend for every X/Y/S: finite complete continuous observations; `n>|S|+3`; finite positive definite submatrices; `kappa2(R)*np.finfo(np.float64).eps <= 1e-6`; `max(||R inv(R)-I||_inf,||inv(R)R-I||_inf) <= 1e-8` using maximum absolute row-sum matrix norms; finite intermediate values and strict `abs(partial_r)<1`. Failed/undecidable checks deny before Backend call; Backend `abs(r)>=1` clipping cannot be treated as scientific admissibility. These are conservative eligibility checks, not a guarantee of p-value or inverse forward accuracy.
- Preserve verified effective Python3.12 / causal-learn signature and FCI behavior, true `node_names` and node ordering, PAG circle/arrow/tail endpoint fidelity and latent uncertainty, Graph source ContentRef and dual hashes, non-null BK fail closed, strict error/status routing and no private stdout leakage.
- Implement focused tests at the approved lifecycle/layer locations and report actual results: numeric near-singular matrices with successful inversion but unacceptable conditioning, independent residual checks, threshold-boundary comparators, full all-subsets coverage, categorical positive and negative, preflight non-invocation, actual Backend fit and scientific Oracle evidence as applicable. Mechanical success does not grant independent science approval.
- **Do not change** completed P01/P03 code, tests, instructions or checkpoints; P02/P05 scope, public E11 `e11-local-*/1` wire version, Product v2, `uv.lock`, other Methods/Gates or previously approved scientific target without separate change authorization. Previous bounded P02 Reader compatibility decisions do not create a blanket change exception.

## 4. Trial restart, evidence and stop discipline

The same `Trial01` restarts after previous `BLOCKED_CONTRACT_AMBIGUITY`, with **no P04 checkpoint**. The prior reported stop `START_SHA=b9910c9a382241a9a850fc57579badb9ccfa8b11` and actual Python3.12.16 / causal-learn 0.1.4.8 imported signatures are evidence about a previous run, not substitutes for fresh checks.

At restart the Coding Agent must independently verify checked-out remote/branch, clean tree, fresh `START_SHA`, ancestor relationships and administrative-only post-freeze differences, both `uv.lock` Git blob and physical file SHA256, effective Python/Backend APIs, actual P01/P03 checkpoints and P04 checkpoint/remediation state. Do not assume the working environment is unchanged.

If a new material contract ambiguity, unsupported Backend behavior, scientific oracle inadequacy, completed-package conflict or unapproved numerical cutoff is encountered, stop without altering frozen WHAT; provide exact reproducible blocker evidence and bounded change-control proposal.

On successful legitimate package completion, report code/test changes, exact commands and results, new checkpoint commit SHA, working tree and push facts. No unexecuted test, independent MAG/PAG review, real FCI proof, `G01_999 PASS`, downstream Gate unlock or public publication authorization is implied by S11.

## 5. Explicit separation from G01 scientific acceptance

`S11_OWNER_APPROVED` allows scoped coding, not formal independent 07/999 science approval. Preserve independent MAG/PAG Oracle, non-null BK fail closed, T2/T3, Product v2 regression and G01_999 requirements. The fixed exhaustive-enumeration compute-resource budget remains unspecified; the Coding Agent must not invent it, and failure to finish required evaluation is a typed technical stop before FCI.
