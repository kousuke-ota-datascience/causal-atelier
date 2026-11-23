# 202 — ENH-E11 G01 five-layer source concordance for Gate 06/07

**Date:** 2026-11-23 JST  
**Authority class:** Author cross-document audit and future change-control instruction; not 09 approval, S10 amendment or S11 authorization.  
**Relative path base:** `docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/`  
**Current frozen G01-S10 immutable SHA:** `6df4b94de72a6ec8619f315e55ba7821e1eb157c`  
**Branch:** `feature/ariadne_mvp_e11`  
**P01 completed dependency checkpoint:** `9bff61f0eae25236f95f31f2cd3e7c81291f0167`  
**Existing formal 09 / S10 records:** 198 / 199. **New G01-S11 remains PENDING (200).**

## 1. Owner scope and direction

Owner explicitly requires the Coding Agent implementation WHAT (06_*.md) and independent test WHAT (07_*.md) to be modified **only after checking consistency** against these five stock document groups beneath the stated base:

1. `00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/`
2. `00_enhance_background/Revised_requirements_definition_documents/21_logical_data_design/`
3. `00_enhance_background/Revised_requirements_definition_documents/22_product_basic_design/`
4. `00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/`
5. `00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/`

Target implementation/verification instruction path: `10_enhance_instruction/{GATE_ID}/06_*.md` and `10_enhance_instruction/{GATE_ID}/07_*.md`.

The rule is **semantic responsibility/AC/ABI alignment**, not duplicating every stock paragraph. The package document must remain self-contained. Neither the text at a historic frozen SHA nor a later audit authorizes altering normative frozen 06/07 without formal 09 → new S10 → separate S11.

## 2. Audit scope at frozen `6df4b94de72a6ec8619f315e55ba7821e1eb157c`

| Package / instruction | Requirement layer | LDD | BD | Interface | Detailed Design | Tests and disposition |
| --- | --- | --- | --- | --- | --- | --- |
| G01 gate-wide 06 and P00 planning | FR-185–203, NFR-029–036 and current 10_91 AC | 21_25/21_40 | 22_06/22_09/22_12/22_15 | 23_41/23_42 | 30_60–30_63 | G01 07-01–12; Scope P01–P05 only, P00 plan |
| P01 strict Study / ContentRef / JCS / Manifest | FR-201/203; NFR-029 and 10_91 | 21_25/21_40 | 22_06/22_09/22_15 | 23_41/23_42 | 30_60 §9/11/12, 30_62 §4 | 07-01/02/04/07/12; **197** records exceptional already-implemented P01 upstream reverse alignment |
| P02 FD/root/Publisher/Reader | NFR-030/031 and 10_91 | 21_23/21_40 | 22_09/22_12 | 23_41/23_42 | 30_60 §10, 30_62 §3/5/8 | 07-02/05/06/11; **195/196** align PrivacyDecision and validate signature across all five layers |
| P03 Graph/PAG identity | FR-186, FR-201; NFR-029 | 21_25/21_40 | 22_06/22_09 | 23_41/23_42 | 30_61 §1/6/7 | 07-03/04/07; endpoint fidelity not identification or real FCI science |
| P04 FCI/CI/Backend semantics | FR-185/186/201, NFR-032/035; 10_32 Method Scope | 21_40 | 22_06/22_15 | 23_41/23_42 | 30_61 §5.3/5.5, 30_62 §2/7, 30_63 §1.3/4.4 | 07-08/09/10; non-null BK denied before FCI pending independent proof, no invented scientific negative |
| P05 CLI integration/Privacy/Product v2 | FR-201/203, NFR-030/031/036 | 21_23/21_40 | 22_09/22_12/22_15 | 23_41/23_42 | 30_60/30_62 | 07-07/11/12, protected Product regressions; authorized P02 decision passed unchanged to seal |
| G01 07 test WHAT | 10_91 + each applicable FR/NFR/AR | corresponding P01–P05 logical constraints | BD independent acceptance axes | IF strict positive/negative cases | DD REF/SPEC/MAN/GRAPH/PUB/READ/CAP/RUN/METH IDs | Preserve 07-01–12 and independent Linux/Backend/Science; no fake PASS |

The 06 files and 07 were inspected at the **immutable frozen source** and mapped to their existing DD/IF and AC responsibilities. This is **a targeted Author semantic/trace audit**, not a complete line-by-line independent S09 adjudication of every cross-gate source. No additional concrete inconsistency beyond the already closed P01/P02 defects has been established by this audit.

## 3. Change-resolution protocol

For each newly observed difference:

1. Record the exact **requirement ID**, LDD invariant, BD responsibility, IF signature/wire, DD class fields/methods, named 06 package section, 07 case and actual Git blob/SHA.
2. Decide whether the discrepancy is (A) editorial/trace only, (B) a binding CONTRACT_DEFECT affecting implementation WHAT or acceptance, or (C) an actual tested code/contract mismatch. Do not promote a user or agent hypothesis directly to fact.
3. For new not-yet-implemented packages, follow **RD → LDD / BD → IF → DD → 06 package → 07 verification** and keep all levels semantically equivalent. Do not copy enhancement-specific control-plane records into durable stock documents.
4. The **P01 reverse-alignment exception** is bounded to the already implemented P01 with Owner's explicit instruction and audit 197. It does not authorize weakening FR/NFR/MUST/AC or rewriting implementation to match a document. Existing P01 06, 30_60/30_62, source/tests and `9bff61f0eae25236f95f31f2cd3e7c81291f0167` remain intact.
5. If the difference affects any file at existing frozen `6df4b94de72a6ec8619f315e55ba7821e1eb157c`, prepare a new 09 amendment and cross-layer impact review, obtain separate Owner formal 09 approval and **new immutable S10 full SHA**, then **separate new S11**. No implementation or 06/07 contract editing on the currently authorized freeze by inference.
6. If no new semantic discrepancy is found, **do not churn the frozen 06/07**. Supply a trace audit and preserve their frozen hashes; a status header such as `DRAFT/NOT_FROZEN` is an issuance-time snapshot and later signed Owner 198/199/S11 records establish current authority, not arbitrary content substitution.
7. Confirm unchanged public wire/legacy v2, source/tests/lock where required, P01 checkpoint ancestry, real Trial state, distinct technical/scientific/authorization axes. Independent G01-999 acceptance remains unavailable without corresponding real evidence.

## 4. Documentation done versus executable evidence

Existing records 195–197 and actual frozen contents provide P01 and P02 reconciliation; P03/04/05/07 were mapped to their upstream headings, but no new line-level fix has been justified. No 06/07 revisions are made **after** frozen S10 as part of this protocol. This record is permitted as a *post-freeze control-plane document*, not permission to expand coding WHAT.

**Next authorization barrier:** separate Owner `DEC-G01-P02-S11-REAUTH-01` (docket 200). An earlier S11 record 193 applies to previous frozen SHA. P02 remains `BLOCKED_CODING_AUTHORIZATION` until a distinct new S11 is recorded.
