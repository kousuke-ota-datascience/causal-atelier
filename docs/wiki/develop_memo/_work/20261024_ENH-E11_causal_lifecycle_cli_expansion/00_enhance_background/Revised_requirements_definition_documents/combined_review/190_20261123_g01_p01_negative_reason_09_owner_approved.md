# 190 — ENH-E11 G01 P01: AMD-E11-G01-P01-002 Formal 09 Owner Approval

**Decision ID:** `DEC-G01-P01-REBASELINE-02 / FORMAL_09_AMENDMENT_APPROVAL`  
**Owner decision:** `APPROVED`  
**Decision date:** 2026-11-23 JST  
**Provenance:** Owner explicitly responded `DEC-G01-P01-REBASELINE-02を承認する` to a proposal that specifically defined **formal 09 approval of AMD-E11-G01-P01-002 and provisional G01-S10 re-freeze at bcc1d797e1406e8816d12b725eeace07a181c702**.  
**Approved amendment:** `AMD-E11-G01-P01-002` / `CONTRACT_DEFECT`  
**Approved exact immutable full Git SHA:** `bcc1d797e1406e8816d12b725eeace07a181c702`  
**Frozen lock Git blob:** `2b83110e86b26b7969fbddf8f98a727370ae19f7`  
**Repository/branch:** `kousuke-ota-datascience/causal-atelier` / `feature/ariadne_mvp_e11`

## 1. Formal contract-change approval

The Owner formally approved the **specific** amended contract identified above, as proposed in:

- `10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P01-002_Gate_Contract_Amendment.md`
- `00_enhance_background/Revised_requirements_definition_documents/combined_review/189_20261123_g01_p01_negative_reason_contract_defect_impact.md`
- The amended `G01/06_G01_P01_local_contract_codec.md`, `06_G01_P04_fci_backend_oracle.md`, `06_G01_P05_cli_use_case_privacy.md`, G01 `07`, stock `23_42` and `30_62` at frozen-source SHA `bcc1d797e1406e8816d12b725eeace07a181c702`.

This approval replaces the **proposal/approval status** of 09 AMD-002 at that historical commit; its substantive text remains immutable. Do not edit the source SHA's 09 merely to revise its prior `PROPOSED` status. The earlier AMD-001 and approvals 185/186/187 remain historical for their former frozen contract.

The amendment mandates a **closed G01 science-negative lexical discriminator**: `SCI_NO_ADMISSIBLE_PAG` is the only possible negative code and must be a singleton in both `ValidatedRunEvidence.graph_negative_reason_codes` and `Status.reason_codes`; technical-error strings are rejected even if identical across both fields. For Graph-positive, both lists are empty. P01's pure check does **not** establish that scientific-negative is a real FCI result. P04 and P05 may issue/publish such a negative only if method-specific scientific justification actually exists, otherwise fail closed. No current verified FCI producer or independent proof was asserted.

## 2. Impact disposition and protected constraints

Author-level affected-contract reconciliation is documented in 189 and formal 09. The preceding S10 `707f6aaac1df5393dbf762448c41db2f1c9dbf35` to approved source commit has only documentation edits, including P01/P04/P05, 07, stock IF/DD, formal 09, audit/ledger/handoff. Source `src/`, `tests/`, `pyproject.toml`, public E11 JSON schemas and `uv.lock` were not modified in this amendment.

The `uv.lock` **Git blob** remains `2b83110e86b26b7969fbddf8f98a727370ae19f7`. A separate real runtime must verify lock bytes SHA-256, branch, clean worktree, effective contract drift, environment and Trial state.

No independent S09, B02/B03/B04/B05, independent MAG/PAG/BK science, T2/T3, real FS/Reader, Product v2 regression, independent 07, or G01_999 PASS is claimed or waived. `DEC-G01-EXEC-01` G01-only coding-before-external-evidence timing remains; non-null BK including empty object remains typed denied until proven safe. No changes to G02–G10.

## 3. Authority ordering and limits

1. **Formal AMD-002 09 Owner approval: APPROVED** in this record 190.
2. **New provisional G01-S10 re-Freeze:** explicitly authorized by the same Owner decision but must be recorded in a **separate subsequent record 191**, pinning the exact full Git SHA above.
3. **New limited G01-S11 Coding Authorization:** **NOT GRANTED** by `DEC-G01-P01-REBASELINE-02`; a later distinct Owner decision is mandatory before Coding Agent can resume.

Old 187 is **not** reusable for the changed contract. Historical G01/P01/Trial01 pre-coding BLOCKED results remain preserved, not formal FAIL and not a Package checkpoint. This record alone does not grant coding or scientific acceptance.
