# ENH-E6 G01 P02 — Stage-aware Presentation and Legacy Compatibility

**Document class:** Primary Execution Contract — Work Package  
**Self-containment:** MUST.

- Enhancement: `ENH-E6`
- Gate: `G01`
- Package: `P02`
- Status: `APPROVED / WAITING_FOR_P01_CHECKPOINT`
- Target branch: `bugfix/ariadne_mvp_e6`

## 1. Purpose

Use the NavigationContext application seam established by P01 to make presentation activation deterministic by `(family, stage)` and convert analytical legacy left-nav entries into canonical Family/Stage compatibility shortcuts. This package resolves the Causal Discovery/Inference presentation boundary without redesigning underlying scientific screens.

## 2. Effective Gate constraints applicable to this package

- backend catalog remains Family/Stage authority.
- canonical route remains `/projects/{project_id}/analysis/{family_slug}/{stage_slug}`.
- Navigation Stage is UI/navigation state, not Execution Stage/persistent domain state.
- P02 must use the P01 shared transition/application seam rather than create a parallel history/state/render path.
- missing supported presentation binding fails explicitly; no silent default.
- exact mappings below are normative P02 behavior.
- canonical docs and ENH-E5 historical evidence are protected.

## 3. In scope

- stage-aware presentation resolver/binding integrated with P01 transition seam
- activation of existing `explore`, `predictive`, `discovery`, `inference` surfaces from canonical `(family, stage)`
- legacy analytical left-nav click resolution to exact canonical contexts
- removal/deprecation of Family-only mapping as canonical presentation authority
- fail-closed missing binding behavior
- focused DOM/integration/static/regression tests
- minimal shell/workspace activation changes necessary to keep selected navigation and visible presentation coherent

## 4. Explicitly out of scope

- redesign/replace existing analysis forms/screens
- remove entire legacy left navigation
- change backend catalog or canonical Family/stage definitions
- change canonical requirement/design docs
- implement browser runner/Docker harness owned by P03
- scientific workflow/algorithm changes
- persist Navigation Stage
- refactor unrelated workspace routing

## 5. Entry criteria / required evidence

- operator preflight clean branch/tree and runtime `START_SHA`
- P01 required package checkpoint exists and implementation seam is present in current repository
- assigned P02 resolves exactly once
- no formal remediation route for current Trial

If P01 seam is absent/incompatible and cannot be used without modifying P01 scope, stop `BLOCKED_IMPLEMENTATION`/`BLOCKED_CONTRACT_AMBIGUITY`; do not reimplement P01 inside P02.

## 6. Required implementation

### 6.1 Normative presentation mapping

```text
exploratory/* -> explore
predictive/* -> predictive

causal/setup -> discovery
causal/discovery -> discovery

causal/identification -> inference
causal/estimation -> inference
causal/effects -> inference
causal/diagnostics -> inference
causal/sensitivity -> inference
```

Here `*` means any stage actually present in the backend-authoritative current Family catalog for the existing surface class; do not create a full duplicated frontend catalog. Causal mapping is explicit because it distinguishes two existing surfaces.

A supported catalog stage without a valid presentation mapping is a configuration defect/error. Do not default it to `discovery`, `explore`, or another surface.

### 6.2 Normative legacy analytical shortcut targets

```text
Explore            -> exploratory/profile
Predictive         -> predictive/setup
Causal Discovery   -> causal/discovery
Causal Inference   -> causal/identification
```

Legacy button handler must resolve the target NavigationContext and submit it to P01 transition authority. It must not independently activate workspace, push a parallel legacy route, and later mutate NavigationContext.

`Causal Inference -> causal/identification` is a compatibility entry point, not a scientific statement that inference equals identification. User can navigate subsequent estimation/effects/diagnostics/sensitivity stages through Stage navigation.

### 6.3 Presentation state coherence

For any applied valid context:

- exactly the required existing analysis presentation surface is active for the mapping above;
- obsolete previous analysis presentation is inactive;
- Family/Stage selected UI stays aligned with current context;
- legacy shortcut does not leave a split-brain workspace vs canonical route state;
- switching Causal discovery -> identification changes presentation from Discovery to Inference without changing selected Family.

### 6.4 Failure behavior

- missing mapping for supported stage -> explicit configuration/user-visible/logged error according to existing frontend error convention; no fallback.
- invalid Family/Stage -> existing canonical route validation error; do not normalize to unrelated valid state.
- no duplicate full backend catalog ownership in frontend.

## 7. Focused verification

| Verification | Required proof |
|---|---|
| unit/pure | presentation resolver returns exact mapping above and rejects missing binding |
| DOM/integration | `causal/discovery` activates Discovery only; `causal/identification` and `causal/estimation` activate Inference only |
| integration | four legacy shortcuts resolve exact canonical contexts via shared transition path |
| history/state | legacy shortcut uses canonical transition semantics and does not create split-brain legacy state |
| static | Family-only `causal -> discovery` is not retained as canonical presentation authority; no duplicate catalog |
| regression | affected Explore/Predictive/Causal existing frontend tests remain green |

P02 may use existing DOM integration tests. P03 owns blocking real Chromium journeys; do not expand P02 to build browser harness.

## 8. Protected contract / Transition Debt constraints

- P01 shared transition seam is protected dependency for P02; do not fork it.
- Navigation Stage/Execution Stage separation and non-persistence remain protected.
- legacy visual IA remains temporarily; only authority is reduced to compatibility shortcut.
- ANOM-E5-001 remains OPEN after P02.

## 9. Checkpoint / reporting rule

After focused verification succeeds, create P02 package checkpoint/evidence/report per canonical operator workflow. Report exact changed files, mapping implementation, shortcut convergence, commands/results, `START_SHA`, checkpoint/evidence identities, remaining P03 scope. Do not claim Gate PASS.

## 10. Package completion criteria

`PACKAGE_READY` only if:

- all normative presentation mappings above are implemented and focused-tested;
- all four legacy analytical targets are implemented through P01 seam;
- missing mapping fails closed;
- no parallel Family-only canonical presentation authority remains;
- affected regressions pass;
- checkpoint/report/evidence are recorded;
- no P03/browser-harness or protected out-of-scope work is included.

## 11. External reference policy

Assigned P02 is the only normative implementation contract. Coding Agent must not read Gate06, Gate07, P00, other Pxx, 00-30 planning/report documents, ADR, prior enhancements, issues, or Web to discover requirements. Inspect current source/test/config only as implementation substrate. Ambiguity -> `BLOCKED_CONTRACT_AMBIGUITY`.

## 12. Stop rule

Stop if P01 seam is missing/incompatible, backend/canonical design change is required, exact mappings conflict with higher-authority product behavior discovered in allowed substrate but cannot be resolved from this contract, browser harness work becomes necessary for package completion, or focused verification cannot succeed within P02 scope.
