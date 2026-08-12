# ENH-E5 G01 Trial 01 P02 — Package status

- PROJECT_NAME: Ariadne
- ENHANCE_ID: ENH-E5
- GATE_ID: G01
- PACKAGE_ID: P02
- TRIAL_NO: 01
- Normative Pxx contract: `docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/10_enhance_instruction/G01/06_G01_P02_navigation_shell_ui.md`
- START_SHA: `4800fabd1ab9d44ab6e64797a51278d38fb97564`
- Package status: BLOCKED_CONTRACT_AMBIGUITY
- PACKAGE_CHECKPOINT_SHA: none
- Changed / uncommitted files: none

## Blocker

P02 requires `GET /projects/{project_id}/operation-availability` and that its result be presented by the frontend. The contract specifies the query parameter names and response envelope, but does not specify:

- the required operation names for the `operations` map;
- the resource-type-specific availability predicates;
- the authorization input, authority, or decision boundary; or
- the behavior when no resource query is provided.

These omissions prevent the required behavior and error semantics from being determined uniquely. Deriving them from current routers, existing `allowed_actions` fields, or a different Package/Gate document would treat the repository or prohibited material as specification authority, contrary to P02 section 0.

## Execution performed

- Repository preflight passed: branch `feature/ariadne_mvp_e5`, clean working tree, START_SHA recorded.
- Identified exactly one assigned P02 contract.
- Inspected current source only to establish that no existing `operation-availability` endpoint was available for direct UI binding.
- No production, test, schema, or migration change was made.
- No focused verification was run because implementation cannot begin without inventing the missing contract.

## Required clarification to resume

Define the operation key set and each resource-type predicate (including authorization authority and no-resource behavior) for the `operation-availability` response, or explicitly authorize a named existing availability authority as the normative source.
