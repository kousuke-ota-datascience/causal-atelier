# ENH-E11 — Owner-authorized execution-branch reassignment (2026-11-23)

**Decision:** `DEC-E11-EXEC-BRANCH-01=OWNER_DIRECTED`.
**Owner instruction:** 「作業ブランチを以下に変更した」「これ以外にもリポジトリ名をハードコード（プレイスホルダーのインスタンス化）しているドキュメントがあれば修正せよ」 with destination https://github.com/kousuke-ota-datascience/causal-atelier/tree/feature/ariadne_mvp_e11 .
**Classification:** Operational branch retarget / instantiated execution identity correction; **not** new implementation WHAT, Method semantics, S09/07 scientific approval, Gate999 PASS or Coding Agent execution.
**Actual repository (unchanged):** `kousuke-ota-datascience/causal-atelier`.
**Previous execution branch:** `prototype/ariadne_mvp` (preserve historical provenance, not current push destination).
**New exclusive execution/write/push branch:** `feature/ariadne_mvp_e11`.
**Branch-point verification before edits:** GitHub returned both refs pointing to the **same full commit** `82ea702021ce453a4e3f32bf4c5a8a6f36621daa`; GitHub commit comparison returned `status=identical`, ahead=0, behind=0. This is a branch re-target, **not** a repository rename or a source reset.
**S10 full immutable frozen commit (unchanged):** `a05fd072cbb82a7c6e43f45e7208e078f0784a2b`.
**Frozen `uv.lock` Git blob (unchanged):** `2b83110e86b26b7969fbddf8f98a727370ae19f7`.
**Owner S10 and S11:** [179](179_20261123_g01_provisional_s10_owner_approved.md) and [180](180_20261123_g01_limited_s11_owner_coding_authorization.md), respectively. Their original approvals still authorize only G01/P01–P05 implementation and developer tests; no science PASS or other Gates. The operational handoff is [181](181_20261123_g01_coding_agent_entry_handoff.md).

## 1. Necessary correction and authority boundaries

The prior `BRANCH_NAME=prototype/ariadne_mvp` and hard-coded `git push -u causal-atelier prototype/ariadne_mvp` in ENH-E11 instantiated 40 Agent entry prompts would direct an external Coding/Test Agent to the **wrong branch**. Owner explicitly ordered a branch change; these exact operation-routing literals must now use `feature/ariadne_mvp_e11`. The remote alias `REMOTE_NAME=causal-atelier` was not changed by the Owner; actual runtime must verify that alias points to the unchanged repository before pushing.

This correction does **not** rewrite frozen S10 commit contents, alter `src/`, `tests/`, `pyproject.toml` or `uv.lock`, or authorize changing scientific Method, Graph/PAG, Privacy, Product v2, status/Reader semantics, schema or Acceptance Criteria. Post-freeze **administrative/routing changes** are explicitly recorded by this Owner instruction, but any substantive new normative WHAT still requires the formal 09/impact/re-freeze and Owner reapproval prescribed by the frozen S10/S11 contracts.

Do not treat unchanged SHA indices (e.g., `s09_post_reconciliation_document_snapshot_draft14.json` and `s09_g01_scoped_review_inventory_draft8.json`) as an audit of edited branch files. Their historical 402/source blob identity remains the immutable S10 authority; re-evaluate *actual code-time* changed files by both semantic diff and exact commit SHA, and record that 182 permits only the explicitly listed branch-routing changes.

## 2. Modified current-use documentation

- `40_operator_workflows/agent_entry_prompts/00_variable_conventions.md`: instantiated branch variable.
- `40_operator_workflows/agent_entry_prompts/10_normal_execution_01_single_execution_coding_agent_prompt.md`: branch variable, clean preflight check, `git push` destination and managed fixed identity.
- `40_operator_workflows/agent_entry_prompts/10_normal_execution_02_work_package_coding_agent_prompt.md`: same four branch references.
- `40_operator_workflows/agent_entry_prompts/20_candidate_assembly_01_work_package_candidate_assembly_agent_prompt.md`: managed fixed identity.
- `40_operator_workflows/agent_entry_prompts/30_independent_verification_01_test_agent_prompt.md`: branch variable, preflight, push and managed identity.
- `40_operator_workflows/agent_entry_prompts/40_fail_remediation_01_fail_rework_coding_agent_prompt.md`: branch variable and managed identity.
- `40_operator_workflows/agent_entry_prompts/50_orchestration_01_gate_orchestrator_prompt.md`: managed fixed identity.
- `10_enhance_instruction/G01/06_Ariadne_ENH-E11_G01_implementation_instruction.md`: branch-labeled prospective execution baseline only, no Method/AC change.
- `00_enhance_background/Revised_requirements_definition_documents/combined_review/158_20261122_s05_independent_science_reviewer_prompt.md`: branch target and clarification that its review prompt does not grant Coding Authorization (actual G01 S11 exists in 180).
- `00_enhance_background/Revised_requirements_definition_documents/combined_review/165_20261122_s09_independent_document_audit_instruction.md`: instantiated reviewer `BRANCH` value.
- `00_enhance_background/Revised_requirements_definition_documents/combined_review/180_20261123_g01_limited_s11_owner_coding_authorization.md`: operative branch and migration addendum; historical S10 identity unchanged.
- `00_enhance_background/Revised_requirements_definition_documents/combined_review/181_20261123_g01_coding_agent_entry_handoff.md`: branch invocation/check and migration addendum.

Two 40-layer human README documents may also point to this record for the current effective execution target even though they had no old hard-coded literal.

## 3. Intentionally untouched source provenance

Historical design decisions, investigation notes, past reviews and SHA/source inventories retain their *original* `prototype/ariadne_mvp` references when these describe where a historical snapshot was taken. Examples: S10 freeze record 179, approval docket 178's original frozen branch, PREP03 audit, `working_notes` with pinned old HEAD, `_source_snapshots`, previous `s09_post_reconciliation_document_snapshot_draft*.json` (whose `branch` field is a historical inventory identity). Replacing those strings would falsify provenance and would **not** retarget the active Agent. The old Git ref has not been deleted or mutated by this operation.

## 4. Coding Agent execution preflight for new branch

```text
REPOSITORY=kousuke-ota-datascience/causal-atelier
REMOTE_NAME=causal-atelier
BRANCH_NAME=feature/ariadne_mvp_e11
GATE_ID=G01
TRIAL_NO=01
PACKAGE_ID=P01
EXECUTION_MODE=WORK_PACKAGE
FROZEN_G01_SOURCE_FULL_SHA=a05fd072cbb82a7c6e43f45e7208e078f0784a2b
FROZEN_UV_LOCK_BLOB_SHA=2b83110e86b26b7969fbddf8f98a727370ae19f7
```

Before Coding Agent work starts: inspect actual remote with `git remote -v`, branch with `git branch --show-current`, cleanliness with `git status --porcelain`, actual HEAD with `git rev-parse HEAD`, frozen S10 commit/lock existence, and meaningful diff of current execution HEAD against the frozen S10 source. **Do not reset, checkout, cherry-pick, change the old branch, or write to another branch to bypass an unsuccessful preflight.** A mismatch beyond this bounded routing/admin change is `BLOCKED_CODING_AUTHORIZATION` pending impact and Owner decision.

**At time of this planning update:** no external Linux VM/Codex CLI agent or independent Reviewer has been run from this conversation. Coding entry remains limited Owner-authorized but actual runtime execution is unobserved; `G01_999=BLOCKED`; G02–G10 are not authorized.
