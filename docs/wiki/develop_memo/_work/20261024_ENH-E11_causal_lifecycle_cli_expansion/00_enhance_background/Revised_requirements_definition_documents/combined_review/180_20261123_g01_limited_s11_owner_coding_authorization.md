# G01 — Limited S11 Coding Authorization: separate Owner approval record

**Decision ID:** `G01-S11-LIMITED`
**Decision:** `OWNER_APPROVED_LIMITED_CODING_AUTHORIZATION`
**Decision date:** 2026-11-23 JST
**Authorization provenance:** The Owner, in the new thread continuing `00_計画⑮`, explicitly replied: 「以下の判断について、推奨案を採用する」 to the distinct question 「次のOwner判断：限定G01-S11」, whose proposed approval was expressly limited to G01 P01–P05 implementation and developer testing, without science PASS, G01_999, other Gates or production. This is a human textual approval, **not** a cryptographic signature, independent verification, or proof that any Agent has run.
**Separate prerequisite S10 evidence:** [179 — G01 provisional S10 Owner approval](179_20261123_g01_provisional_s10_owner_approved.md); [178 — exception docket](178_20261123_g01_provisional_s10_limited_s11_owner_approval_docket.md); [177 — DEC-G01-EXEC-01](177_20261123_dec_g01_exec01_owner_adopted_evidence_rephasing.md).

## 1. Exact authorized identity

| Field | Binding |
| --- | --- |
| `PROJECT_NAME` / `ENHANCE_ID` | `Ariadne` / `ENH-E11` |
| `GATE_ID` | `G01` only |
| `EXECUTION_MODE` | `WORK_PACKAGE` |
| `AUTHORIZED_PACKAGE_IDS` | `P01,P02,P03,P04,P05` |
| `P00` | planning/traceability only, **not** Coding Package |
| Authorized actions | Implement only assigned G01 package source and enhancement-local developer/focused tests; package checkpoint/report/push; when all packages are ready, Candidate Assembly. Do not equate package completion to Gate acceptance |
| Repository | `kousuke-ota-datascience/causal-atelier` |
| Required execution branch | `prototype/ariadne_mvp` under the existing ENH-E11 40 Operator preflight |
| **G01_S10_FROZEN_SOURCE_FULL_SHA** | **`a05fd072cbb82a7c6e43f45e7208e078f0784a2b`** (immutable normative source identity; do not substitute moving branch HEAD) |
| **Frozen `uv.lock` Git blob SHA** | **`2b83110e86b26b7969fbddf8f98a727370ae19f7`** |
| First normal execution | `GATE_ID=G01`, `TRIAL_NO=01`, `PACKAGE_ID=P01`, provided no actual prior G01 trial/remediation artifacts change the runtime-derived trial identity |
| Dependency order | `P01 → P02 and P03 → P04 → P05 → Candidate Assembly`; the 40 Orchestrator may run ready packages sequentially while respecting dependencies |

**Binding contracts at frozen commit:** `10_enhance_instruction/G01/06_Ariadne_ENH-E11_G01_implementation_instruction.md`, `06_G01_P00_work_package_plan.md`, `06_G01_P01_local_contract_codec.md`, `06_G01_P02_atomic_publication_reader.md`, `06_G01_P03_pag_graph_version.md`, `06_G01_P04_fci_backend_oracle.md`, `06_G01_P05_cli_use_case_privacy.md`, `07_Ariadne_ENH-E11_G01_test_instruction.md`; relevant common E11 v1/Method Profile/source contracts and ENH-E11 `40_operator_workflows/agent_entry_prompts/` at the **same frozen full commit**. G01 common/source candidate inventory `s09_g01_scoped_review_inventory_draft8.json` (11 OWN_GATE, 69 COMMON_SHARED, 5 IMPACT_SAMPLE, 317 DEFERRED_OTHER_GATE) and all-source `s09_post_reconciliation_document_snapshot_draft14.json` (402 paths) are author integrity indices, not an independent PASS.

**Frozen-header precedence:** A frozen 06/Pxx/07/40 header saying `S10/S11 NOT_AUTHORIZED` is historical at its document issuance, and is superseded **for authorization state only** by S10 record 179 plus this S11 record 180. The normative scientific/technical WHAT in those frozen documents is unchanged. Do not rewrite the frozen contracts to change a historical status field.

## 2. Executable entry guard (Orchestrator / Human operator)

1. Read **both** distinct positive Owner records 179 and 180; confirm G01 only, allowed P01–P05, G01 S10 freeze full 40-hex SHA, `uv.lock` Git blob and continuing post-S11 exception ledger. Policy adoption 177 or docket 178 alone is insufficient.
2. On the **actual coding machine**, check `git branch --show-current`, `git status --porcelain`, `git rev-parse HEAD`, `git rev-parse a05fd072cbb82a7c6e43f45e7208e078f0784a2b^{commit}`, and `git rev-parse a05fd072cbb82a7c6e43f45e7208e078f0784a2b:uv.lock`. Current branch must be `prototype/ariadne_mvp`, working tree clean, frozen commit reachable, and frozen lock blob matching the value above. Also record `sha256sum uv.lock` for the **actual** checkout; Git blob SHA is not SHA-256.
3. Branch HEAD need **not** equal frozen source full SHA solely because subsequent **administrative evidence** commits exist. Verify actual effective 06/Pxx/07/40/common normative contracts and lock against the frozen full SHA before running; require no unapproved normative drift. At S11 approval, GitHub commit comparison from `a05fd072...` to branch showed only review/readiness/docket additions/edits, not normative source or `uv.lock`; **re-verify at execution time**. Dirty worktree, missing authorization, changed effective normative contract/lock, unsupported branch or non-G01 scope: fail closed as `BLOCKED_CODING_AUTHORIZATION` or `BLOCKED_REPOSITORY_STATE`, with exact evidence.
4. Orchestrator resolves G01 `WORK_PACKAGE` and its dependency DAG. Launch `50_orchestration_01_gate_orchestrator_prompt.md` with `GATE_ID=G01`, `TRIAL_NO=01` only after runtime identity and Trial state are confirmed. Assigned Work Package Agent uses `10_normal_execution_02_work_package_coding_agent_prompt.md` with `GATE_ID=G01`, `PACKAGE_ID=Pxx`, `TRIAL_NO=01`. The Coding Agent's **sole implementation WHAT authority** is its assigned Pxx; 40 owns WHERE/HOW. Gate 06/P00/07 are Orchestrator, planning and independent-verification authorities, **not** a license for the assigned coder to supplement an ambiguous Pxx with other plans.
5. Each Pxx records actual START_SHA, focused commands/results, checkpoint SHA, package report and any `BLOCKED_*`; no fake run evidence. Once all required packages are `PACKAGE_READY`, use the separate Candidate Assembly Prompt, fix the **actual** Trial Candidate full SHA and hand it to genuinely independent 07 Test Agent. Never infer a candidate SHA from this administrative record.

## 3. Hard limits of authorization

**Not authorized:** P00 coding; any G02–G10 Method/gate coding; Product v2 ABI/CLI migration or uncontrolled change; Web/API/Worker/DB expansion; public/production scientific use; upstream contract/algorithm/threshold alterations; acceptance-criterion dilution; unapproved `uv.lock` drift; an invented Backend correction, PAG scientific truth or imputed causal Effect; automatic downstream Gate launch; `S09_PASS`, `B02_PASS`, `B04_PASS`, `B05_PASS`, `G01_999_PASS` or `SCIENCE_PASS`.

**Hard science safety:** Tagged `causal-learn==0.1.4.8` FCI accepts no non-null BackgroundKnowledge in G01 pre-remedy execution: even structurally empty non-null BK must yield typed `BACKEND_SEMANTICS_UNVERIFIED` / exit 4 **before backend FCI invocation**. This is a fail-closed interim implementation, **not** BK-positive scientific acceptance. Preserve `fisherz/chisq/gsq` eligibility, PAG endpoint uncertainty, independent MAG/PAG/BK reference, no fake Effect, no row output, strict Privacy, Linux private atomic Reader/Publisher, and legacy Product v2 regression.

**Test placement:** New tests start under `tests/enhancement/enh_e11/g01/<layer>/`, where layer is appropriate `unit/contract/integration`; no mandatory Browser E2E for this G01 CLI-only scope. Discover existing Product suite paths from actual checkout; do not auto-promote to `tests/regression/`, relocate legacy suites, or silently skip missing mandatory evidence.

## 4. Unwaived acceptance obligation ledger

| Obligation | At approval | Required before `G01_999=PASS` |
| --- | --- | --- |
| Independent common+G01 S09/B06 | `EXTERNAL_PENDING / NOT_RUN` | Separate actual Reviewer; fix material contract defects through formal 09 and reauthorization |
| B02 | `EXTERNAL_PENDING / NOT_RUN` | Real Python3.12 standard Draft202012 validation of six public + three active G01 P1-M06 Schema; positive/negative/cross-wire |
| B03 | `NOT_IMPLEMENTED / NOT_RUN` | Real private Linux FS, same-UID/no-clobber atomic Publisher, Marker/Manifest, independent Reader/readback and Privacy |
| B04 | `EXTERNAL_PENDING / NOT_RUN` | Real Python3.12 ENV-BASE fitted FCI `fisherz/chisq/gsq`, APIs/console/node/Lock checks |
| B05 / T2 / T3 | `EXTERNAL_PENDING / NOT_ACCEPTED` | Independent MAG/PAG/BK Oracle, sound remedy + console safety, real Pilot → preregistered confirmatory science evidence |
| Independent 07 / 999 | `NOT_RUN / BLOCKED` | Same fixed Trial Candidate full SHA, all mandatory 07 items, Product v2 regression and independent Gate judgment |

Under `DEC-G01-EXEC-01` these items **do not block G01 coding solely because external reviewer/Linux is unavailable**, but they all remain binding acceptance obligations. Any missing evidence keeps `G01_999=BLOCKED`; actual disproving results may be `FAIL`. The G01 exception does **not** change G02–G10 S09→S10→S11 or their upstream 999 requirements.

## 5. Execution and escalation status

- `G01_PROVISIONAL_S10=APPROVED`
- `G01_LIMITED_S11=OWNER_APPROVED`
- `CODING_AUTHORIZED_SCOPE=G01_P01_TO_P05_DEVELOPER_TESTS`
- `CODING_AGENT_EXECUTION=NOT_OBSERVED_IN_THIS_CHAT`
- `IMPLEMENTATION_REPORTS/CANDIDATE_SHA=NOT_OBSERVED`
- `INDEPENDENT_S09_B02_B04_B05=EXTERNAL_PENDING`
- `G01_999=BLOCKED`
- `G02_TO_G10=NOT_AUTHORIZED`

The Owner's coding approval is final **within this limited scope**; no new Owner vote is necessary just to start P01 when a compliant execution environment is available. A material contract defect, changed scientific meaning, uncontrolled Product v2/Privacy/ABI impact, or required departure from frozen source triggers formal 09/change impact and a **new** Owner decision, not unilateral coding-side amendment. Current chat has not connected to the existing Owner Linux VM, started Codex CLI, executed P01 tests, or appointed a genuinely independent reviewer. Refer to the separate operational handoff `181_20261123_g01_coding_agent_entry_handoff.md`.
