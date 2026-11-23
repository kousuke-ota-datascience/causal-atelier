# 231 — G01/P04 AMD-E11-G01-P04-001 limited S11 Owner Coding Authorization

**Date:** 2026-11-23 JST  
**Decision ID:** `DEC-G01-P04-001-S11-REAUTH-01`  
**Status:** `S11_OWNER_APPROVED / G01_P04_TRIAL01_LIMITED_CODING_AUTHORIZED / G01_999_NOT_PASSED`  
**Repository:** `kousuke-ota-datascience/causal-atelier`  
**Branch:** `feature/ariadne_mvp_e11`

## 1. Explicit Owner decision and frozen identity

Owner directive:

> DEC-G01-P04-001-S11-REAUTH-01を承認する。AMD-E11-G01-P04-001に基づくG01-S10凍結SHA a7003b359444af64cad0edbade0341243653a8bf を対象に、G01/P04/Trial01の限定Coding Authorizationを再発行せよ。P01チェックポイント9bff61f0eae25236f95f31f2cd3e7c81291f0167、P03チェックポイント858c9f73366036a2d1445e558135cd521f611462、既承認の科学的・独立検証・G01_999受入条件を維持する。

**Immutable S10 frozen normative commit:** `a7003b359444af64cad0edbade0341243653a8bf`.

Relevant prior decisions:
- Scientific eligibility choice: `DEC-G01-P04-CI-ELIG-01=A`.
- Formal 09 approval: `DEC-G01-P04-001-09-APPROVE-01`, `combined_review/229_20261123_g01_p04_001_formal_09_owner_approved.md`.
- S10 refreeze: `DEC-G01-P04-001-S10-REFREEZE-01`, `combined_review/230_20261123_g01_p04_001_s10_owner_refreeze.md`.
- New S11: this **separate explicit Owner instruction**.

## 2. Verified entry context (before writing this record)

- Branch HEAD: `82cef68d815abf8a82ed58bd168eaea640da6ff4`.
- Approved frozen S10 is ancestor (ahead 1, behind 0), sole later change is S10 approval record `230`; therefore **HEAD need not equal frozen S10** if subsequent changes are strictly authorized control-plane records and ancestry/content have been checked.
- Prior S10 `52e5c60176d6b72c91f839ef267f46657bd380b5` is ancestor.
- P01 checkpoint `9bff61f0eae25236f95f31f2cd3e7c81291f0167` is ancestor.
- P03 checkpoint `858c9f73366036a2d1445e558135cd521f611462` is ancestor.
- Actual Agent workstation clean tree, remotes, lock bytes, installed Python3.12 effective Backend API and future Trial runtime tests **must be rechecked by Coding Agent**; they are not established by GitHub history.

## 3. Strict authorized scope

**Authorized:** G01/P04/Trial01 only. Implement the previously scoped `P1-M06` FCI Backend and capability/Discovery adapter, exhaustive pre-call CI eligibility (every unordered observed pair and every subset of remaining columns; `C(p,2)*2^(p-2)`), exact `fisherz/chisq/gsq` predicates and typed fail-closed, FCI graph/provenance/endpoint fidelity, relevant focused developer verification and factual package reporting, using the frozen normative:
- `10_enhance_instruction/G01/06_G01_P04_fci_backend_oracle.md`
- `10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md`
- `00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md`
- `10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P04-001_Gate_Contract_Amendment.md`
- all other applicable frozen upstream RD/LDD/BD/IF/DD and Gate-level 06/07 contracts, as of exact S10.

**Protected dependencies:** P01 checkpoint `9bff61f0eae25236f95f31f2cd3e7c81291f0167`; P03 checkpoint `858c9f73366036a2d1445e558135cd521f611462`. Do not alter completed P01/P03 06/07, code/tests/checkpoint artifacts without new explicit authorization. Existing separate P02 Reader bounded compatibility authorization does not become P04 blanket permission. P05 implementation, other Gate work, Product v2 and public API/version modifications are out of scope.

**No scientific dilution:** preserve PAG circle/tail/arrow semantics, independent MAG→PAG oracle, BK non-null `BACKEND_SEMANTICS_UNVERIFIED` pre-call guard, JSON stdout privacy, real Backend/Python3.12 and Linux gates, independent testing and G01_999 acceptance. No graph negative `SCI_NO_ADMISSIBLE_PAG` without actual proof; no false PASS from mechanical tests.

**Unresolved quantitative parameters:** a fixed finite computation limit or numerical condition-number threshold has not been approved. Fail closed when exhaustive/finite/numerically reliable preflight cannot be established; do not invent a new public eligibility policy, silently truncate candidate S sets or claim an unexecuted science-positive result. Escalate if positive eligibility becomes impossible without a new scientific decision.

## 4. Trial01 restart and stop / completion discipline

- Coding Agent starts from actual checked-out branch and records a fresh `START_SHA`, tree cleanliness, Git ancestry, lock blob+bytes, effective Python/causal-learn distribution/API facts. Pin the **contract identity** to immutable S10 SHA above, not to the newer HEAD or the date.
- The earlier Agent stopped at `748deb4ba6287bbd1b71e233504c36c6f430e5b7` with `BLOCKED_CONTRACT_AMBIGUITY`, no P04 implementation or checkpoint. The restart keeps Trial01 numbering; it does not invent a prior P04 checkpoint.
- Discover code and test paths from repository and established operator workflow; use enhancement test-placement policy and maintain protected Product regressions. Do not fabricate tests or scientific results.
- If a new material CONTRACT_AMBIGUITY, unsupported Backend behavior, science oracle deficiency, completed-package incompatibility or absent authority arises, stop at that boundary, provide exact reproducible evidence and a scoped remediation request rather than silently changing frozen WHAT.
- Report actual code changes, focused test commands and results, independent evidence still pending, full commit/checkpoint SHA and push state. `PACKAGE_READY` only if the package's applicable objective DoD is supported; this does not issue `G01_999 PASS` or unlock downstream Gate.

## 5. Authorization semantics

**S11_APPROVED is a limited coding permission, not S09 independent verification, Gate 07/999 approval, scientific acceptance, publication authorization beyond G01's agreed test lane or a modification of frozen S10.** This record's Git commit is administrative and is not itself the S10 SHA.
