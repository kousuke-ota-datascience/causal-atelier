# G01 Gate-local Instruction Set — Observable Family / Stage Navigation Integration

**Document class:** Authoring Guide  
**Self-containment:** MUST.

- Enhancement: `ENH-E6`
- Execution Mode: `WORK_PACKAGE`
- Gate contract: `APPROVED / FROZEN`
- Trial planned: `Trial01`

## 1. Required artifacts

- `06_Ariadne_ENH-E6_G01_implementation_instruction.md` — Gate-wide implementation semantic contract.
- `07_Ariadne_ENH-E6_G01_test_instruction.md` — Independent Verification acceptance contract. **Coding Agent must not read it.**

## 2. Conditional artifacts

- `06_G01_P00_work_package_plan.md` — applicable; Human/operator orchestration only.
- `06_G01_P01_navigation_transition_authority.md` — assigned P01 Coding Agent primary contract.
- `06_G01_P02_stage_presentation_and_legacy_compatibility.md` — assigned P02 primary contract after dependency checkpoint.
- `06_G01_P03_browser_regression_and_test_strengthening.md` — assigned P03 primary contract after dependency checkpoint.
- `08_*` / `08_G01_Rxx_*` — not instantiated unless formal FAIL/remediation.
- `09_*` — not instantiated unless semantic contract defect is Human-approved.

## 3. Freeze / Trial rule

- 06/07 frozen before Coding execution.
- Pxx execution interruptions/corrections stay in Trial01 until Fixed Candidate is independently judged.
- formal FAIL creates next Trial; do not silent rewrite 06/07.
- package complete != candidate complete != Gate PASS.

## 4. Reference rule

Gate06/07/Pxx are self-contained for their authority domain. Work Package Coding Agent is routed through canonical template operator prompt and receives assigned Pxx only as normative implementation contract. It must not read G01 06/07/P00/other Pxx/00-30/ADR/past ENH/issues/Web to discover required behavior.

## 5. Amendment ledger rule

Any Human-approved semantic amendment must use G01 09 and append an entry to `00_enhance_background/80_contract_amendment_log.md`. Semantic Gate amendment count: `0`. Documentation/governance re-baseline: `DOC-REBASELINE-001` in the 80 ledger.
