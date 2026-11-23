# ENH-E11 / G01 — Coding Agent entry handoff after limited S11

**Handoff date:** 2026-11-23 JST.
**Status:** `HANDOFF_READY / OWNER_S11_AUTHORIZED / CODING_EXECUTION_NOT_OBSERVED`.
**Source of authority:** [G01 S10 Owner record 179](179_20261123_g01_provisional_s10_owner_approved.md) + **[G01 limited S11 Owner record 180](180_20261123_g01_limited_s11_owner_coding_authorization.md)**; timing exception [177](177_20261123_dec_g01_exec01_owner_adopted_evidence_rephasing.md). This handoff is **not** a new scientific contract, implementation approval for another Gate, or confirmation of a running Agent.

## 1. Operator's task

Start **G01 / Trial01 / P01**, then only after actual `PACKAGE_READY` checkpoints continue the approved dependency sequence `P01 → P02 → P03 → P04 → P05` (P02/P03 can be dependency-independent after P01; sequential order is acceptable to the 40 Orchestrator). Following five packages, run **Candidate Assembly**, then hand the actual fixed Candidate SHA to genuinely independent 07 and required S09/B02/B03/B04/B05/T2/T3/999 verification. **Stop at G01, do not auto-start G02.**

Run-time identity:

```text
PROJECT_NAME=Ariadne
ENHANCE_ID=ENH-E11
ENHANCE_SHORT_ID=E11
GATE_ID=G01
EXECUTION_MODE=WORK_PACKAGE
TRIAL_NO=01
PACKAGE_ID=P01
BRANCH_NAME=feature/ariadne_mvp_e11
WORK_ROOT=docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion
G01_S10_FROZEN_SOURCE_FULL_SHA=a05fd072cbb82a7c6e43f45e7208e078f0784a2b
FROZEN_UV_LOCK_BLOB_SHA=2b83110e86b26b7969fbddf8f98a727370ae19f7
OWNER_S10_RECORD=combined_review/179_20261123_g01_provisional_s10_owner_approved.md
OWNER_S11_RECORD=combined_review/180_20261123_g01_limited_s11_owner_coding_authorization.md
```

`START_SHA`, `PACKAGE_CHECKPOINT_SHA`, `FIXED_TRIAL_CANDIDATE_SHA` and `TEST_START_SHA` **must be derived from the actual runtime**, not populated from the approval SHA or an administrative commit. Trial01 is the intended initial Trial **only if no prior actual Gate/Trial/remediation evidence changes that premise**.

## 2. Normative entry resources

All paths below are within `WORK_ROOT` and normative WHAT/WHERE/HOW is frozen to full commit `a05fd072cbb82a7c6e43f45e7208e078f0784a2b`:

- **Orchestrator (control plane):** `40_operator_workflows/agent_entry_prompts/50_orchestration_01_gate_orchestrator_prompt.md` with `GATE_ID=G01`, `TRIAL_NO=01`.
- **Assigned coding agent:** `40_operator_workflows/agent_entry_prompts/10_normal_execution_02_work_package_coding_agent_prompt.md` with `GATE_ID=G01`, `PACKAGE_ID=P01`, `TRIAL_NO=01`.
- **40 conventions:** `40_operator_workflows/agent_entry_prompts/00_variable_conventions.md`; use the Enhancement-specific prompt, **not** a template-side prompt.
- **P01 sole assigned coding WHAT:** `10_enhance_instruction/G01/06_G01_P01_local_contract_codec.md`.
- **P02:** `10_enhance_instruction/G01/06_G01_P02_atomic_publication_reader.md` after P01 checkpoint.
- **P03:** `10_enhance_instruction/G01/06_G01_P03_pag_graph_version.md` after P01 checkpoint.
- **P04:** `10_enhance_instruction/G01/06_G01_P04_fci_backend_oracle.md` after P01 and P03 checkpoints.
- **P05:** `10_enhance_instruction/G01/06_G01_P05_cli_use_case_privacy.md` after P02/P03/P04 checkpoints.
- **Gate WHAT and test authority for orchestration/assembly/test:** `10_enhance_instruction/G01/06_Ariadne_ENH-E11_G01_implementation_instruction.md`, `06_G01_P00_work_package_plan.md` (plan only), `07_Ariadne_ENH-E11_G01_test_instruction.md`.
- **Candidate Assembly:** `40_operator_workflows/agent_entry_prompts/20_candidate_assembly_01_work_package_candidate_assembly_agent_prompt.md`.
- **Independent verification:** `40_operator_workflows/agent_entry_prompts/30_independent_verification_01_test_agent_prompt.md` after actual Candidate Assembly, with separately assigned genuinely independent agent.

The **individual coding agent reads only its assigned Pxx as implementation requirement authority**, as the existing 40 Work Package prompt explicitly instructs. Orchestrator/Assembly/Independent Test roles may consult other specified authorities for their distinct responsibilities. This handoff provides invocation identity only; it is **not** an additional Pxx implementation specification.

## 3. Preflight on the real approved coding environment

From an existing local checkout (do **not** reset/stash/overwrite dirty work):

```bash
git branch --show-current
git status --porcelain
git rev-parse HEAD
git rev-parse a05fd072cbb82a7c6e43f45e7208e078f0784a2b^{commit}
git rev-parse a05fd072cbb82a7c6e43f45e7208e078f0784a2b:uv.lock
git hash-object uv.lock
sha256sum uv.lock
git diff --name-status a05fd072cbb82a7c6e43f45e7208e078f0784a2b HEAD
```

**Required checks:**
- Branch is exactly `feature/ariadne_mvp_e11`, working tree clean, frozen commit available, and frozen `uv.lock` blob is `2b83110e86b26b7969fbddf8f98a727370ae19f7`.
- For the actual checkout, `git hash-object uv.lock` matches the frozen blob (unless a properly escalated and newly authorized dependency contract exists); record the actual SHA256 separately.
- Inspect the entire diff, not just file counts. Only administrative authorization/readiness files may be newer; any effective 06/Pxx/07/40/Common contract or scientific/Privacy/v2/lock drift requires contract-diff analysis and appropriate Owner authorization **before** implementing.
- Verify 179 and 180 are available to the Orchestrator and denote distinct S10/S11 human decisions. Do **not** treat historical `NOT_AUTHORIZED` headers in frozen Pxx/40 as current status; these are overridden solely in control-plane state by 179+180. Preserve frozen WHAT.
- Verify actual Trial evidence locations and no formal FAIL remediation route; if the Trial is not normal initial Trial01, do not invent a new Trial or run the normal Agent.
- No Linux/Python3.12/Backend fitting has been witnessed in the current ChatGPT session. If these cannot be executed there, preserve **actual** failure evidence. The absence of independent scientific tests alone does **not** revoke S11, but may block a specific package focused verification and **always blocks G01_999 until satisfied**.

If any preflight requirement is unmet, report exact `BLOCKED_REPOSITORY_STATE`, `BLOCKED_CODING_AUTHORIZATION`, `BLOCKED_EXECUTION_UNRESOLVABLE`, or `BLOCKED_CONTRACT_AMBIGUITY` as appropriate; do not silently switch branches, weaken acceptance or repair contracts outside the assigned package.

## 4. Minimal P01 handoff contract and evidence

**Purpose:** pure strict Local Study/ContentRef/Question–Design/Method Profile + RFC8785 JCS + pure Local Manifest DTO. Physical TrustedRoot, FCI oracle and Graph evidence belong to later packages. Start with `G01` / `P01` and only the frozen `06_G01_P01_local_contract_codec.md`.

**What P01 must report:** actual `START_SHA`, exact assigned Pxx source identity, scoped changed files and focused test discovery/collection/commands/results, actual checkpoint SHA, Report status `PACKAGE_READY` or reasoned `BLOCKED_*`, and evidence commit SHA. The normal Work Package Agent is responsible for its own package checkpoint and reports under `20_implementation_reports/G01/Trial01/packages/` according to the 40 conventions; the Orchestrator, not the coding agent, picks the next package.

**Test placement:** enhancement-local G01 tests start at `tests/enhancement/enh_e11/g01/<layer>/` with `unit/contract/integration`; use the actual source checkout to discover Product v2 regressions. No automatic migration to `tests/regression/` and no mandatory Browser E2E for G01 CLI-only.

**Non-null BK** (even empty) must fail pre-FCI with `BACKEND_SEMANTICS_UNVERIFIED` / exit 4 until actual independent safe remedy; do not delete BK-positive future scientific acceptance, invent a PAG oracle, weaken independent Graph/T2/T3 targets, export rows, or synthesize Effect.

## 5. Handoff vs acceptance

`OWNER_S11_APPROVED` permits development **now** in a suitable independently observed coding runtime. It does **not** imply `CODING_STARTED`, `P01_READY`, `S09_PASS`, any B02–B05 run, a Fixed Trial Candidate, science PASS or `G01_999_PASS`.

Before `G01_999 PASS`, the independent Reviewer/Test Agent and approved Python3.12 environment must provide real B02 six-public/three-G01-Schema, B03 OS/FS/Reader/privacy, B04 fitted `fisherz/chisq/gsq`, B05 independent MAG/PAG/BK and accepted correction, T2 pilot and preregistered T3, all G01 07 mandatory items against the same fixed candidate SHA, and legacy Product v2 regression. The G01-only evidence rephasing in 177 permits coding **before** these are proven, not acceptance without them.

**Current evidence at handoff:** GitHub S10/S11 records created; coding machine/Codex CLI not invoked from this conversation; G01 Pxx reports and candidate SHA not observed; scientific/technical independent checks pending; downstream Gates still closed.

## 6. Owner-approved execution branch migration (2026-11-23 JST)

This handoff has been retargeted to `feature/ariadne_mvp_e11`. The GitHub repository `kousuke-ota-datascience/causal-atelier` and `REMOTE_NAME=causal-atelier` are unchanged; verify that this local remote alias really exists and resolves to that repository, and do not substitute an unknown remote silently. The branch migration was authorized by the Owner and documented in [182](182_20261123_e11_execution_branch_retargeting.md). Both branch refs originally pointed to `82ea702021ce453a4e3f32bf4c5a8a6f36621daa` before this retargeting; G01 S10's immutable frozen contract commit `a05fd072cbb82a7c6e43f45e7208e078f0784a2b` still identifies the scientific/technical WHAT. Operational 40 prompts and the G01 06 branch label may differ only in specifically documented invocation/routing fields. The Coding Agent must honor **the feature branch as its sole write/push target**, preserve prior branch history, and stop for unexpected non-administrative contract drift.
