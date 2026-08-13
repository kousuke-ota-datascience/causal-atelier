# Ariadne ENH-E6 G01 実装指示書 — Gate Coding Contract

**Document class:** Primary Execution Contract (Gate-wide semantic authority)  
**Self-containment:** MUST for Gate implementation semantics.  
**Contract state:** `APPROVED / FROZEN`

- Project: `Ariadne`
- Enhancement: `ENH-E6`
- Gate: `G01`
- Branch: `bugfix/ariadne_mvp_e6`
- Production baseline: `5a5ced9bd6a0e62027c4058eb66ec487719bde23`
- Execution Mode: `WORK_PACKAGE`

## 1. Gate definition / acceptance claim

### Gate objective

ENH-E5 intended Family/Family-local Stage navigationをnormal user entryを含むsupported navigation pathsへ統合し、Navigation Context、URL/history、Family/Stage shell、presentation surfaceを一貫して適用する。

### Contract claim established by PASS

G01 PASS後、後続は次へ依存できる:

- Analysis context entry直後に3 Family tabsがobservable/operable。
- Stage sidebarはcurrent Family固有。
- Family/Stage user action、canonical route、reload、Back/Forward、legacy analytical shortcutが一つのnavigation application authorityへ収束。
- `(family, stage)` presentation bindingがCausal Discovery/Inference surface boundaryをdeterministically表現。
- invalid catalog/context/bindingはsilent fallbackしない。

### Why this is one Gate

transition authority、shell observability、presentation binding、history/legacy behaviorは一つのFamily/Stage navigation semantic claimを共同で成立させる。作業量はP01-P03へ分解するがGateは分けない。

## 2. Effective implementation context

Protected inherited semantics:

- Families: `EXPLORATORY / PREDICTIVE / CAUSAL`
- backend navigation catalog is authority for Family order/label/default/stage list
- canonical route: `/projects/{project_id}/analysis/{family_slug}/{stage_slug}`
- `Navigation Stage != Execution Stage`
- Navigation Context is not persisted to Domain Resource/Execution
- affected ENH-E5 route/operation-availability semantics remain compatible

Frozen negative control:

```text
API READY
Project selected
normal Explore -> /projects/<id>/analysis/exploratory/profile
Family tab container=1
Family buttons=0
Stage buttons=0
```

## 3. Execution Mode decision

`WORK_PACKAGE`:

- P01: navigation transition authority/lifecycle convergence
- P02: stage-aware presentation + legacy analytical compatibility
- P03: browser regression/test strengthening

P01/P02/P03 checkpoints require Candidate Assembly before Independent Verification.

## 4. Required implementation semantics

1. Implement one effective Navigation Context application authority owning validation, state commit, history synchronization, Family/Stage rendering/selection, presentation activation boundary, route-dependent refresh/focus/error ordering.
2. Family click, Stage click, canonical initial restore, reload, popstate, legacy normalization, analytical legacy shortcut converge on that authority.
3. Analysis shell becomes observable on analysis context entry without reload; non-analysis context does not show misleading empty active shell.
4. Legacy analytical targets:
   - Explore -> `exploratory/profile`
   - Predictive -> `predictive/setup`
   - Causal Discovery -> `causal/discovery`
   - Causal Inference -> `causal/identification`
5. Required presentation mapping:
   - `exploratory/* -> explore`
   - `predictive/* -> predictive`
   - `causal/setup -> discovery`
   - `causal/discovery -> discovery`
   - `causal/identification -> inference`
   - `causal/estimation -> inference`
   - `causal/effects -> inference`
   - `causal/diagnostics -> inference`
   - `causal/sensitivity -> inference`
6. History policy:
   - user navigation = push
   - legacy normalization = replace
   - initial canonical restore/popstate = no new entry
   - avoid duplicate same-target entries
7. Fail closed on unknown/missing supported Family/Stage/catalog/presentation binding. No silent `discovery` fallback.

## 5. Allowed scope

- frontend navigation/presentation code: `frontend/app.js`, `frontend/navigation_state.js`, minimal related helper modules
- minimal `frontend/index.html` / `frontend/styles.css` changes needed for shell lifecycle/semantics
- affected product/frontend tests
- browser harness/test integration in P03
- `Dockerfile.browser-e2e` / `.dockerignore` only as required by P03 runner inclusion

Backend production code is not allowed absent new proof that the frozen catalog/route contract itself is defective; such proof requires stop/escalation, not opportunistic edit.

## 6. Explicitly prohibited scope

- `docs/wiki/requirement_definition/**` modification
- ENH-E5 historical frozen evidence modification
- backend catalog redesign/full frontend catalog duplication
- Navigation Stage runtime persistence or Execution Stage coupling
- broad left-nav/UI redesign
- unrelated refactor/cleanup
- reload-based workaround that hides initial render defect
- test deletion/assertion weakening/skip/xfail/error suppression to obtain green

## 7. Protected passed-Gate contracts

ENH-E5 PASS evidence remains immutable. G01 implementation must retain affected parse/serialize, legacy normalization compatibility, catalog authority, canonical route behavior, operation availability, and browser history semantics unless the frozen ENH-E6 contract explicitly refines the implementation path above.

## 8. Transition Debt

- `ANOM-E5-001` remains OPEN until G01 final PASS.
- visual removal/redesign of legacy analytical left nav is future scope; ENH-E6 only removes its parallel state authority.
- no new temporary fallback architecture may be introduced without explicit stop/escalation.

## 9. Schema / migration / API / runtime policy

- DB/schema migration: none expected/allowed in normal package scope.
- API schema/catalog change: none expected/allowed in normal package scope.
- Navigation Context persistence: prohibited.
- Browser history/client navigation state changes are frontend runtime changes only.
- If implementation requires migration/API/domain contract change, package must block/escalate.

## 10. Automated test obligations

Coding-side packages must run their Pxx-defined focused verification. Across G01 candidate, affected unit/DOM/static/regression tests and a real Chromium runner operating actual Family/Stage controls must exist. Static source-existence checks are supplemental only.

## 11. Candidate Assembly requirement

After all P01-P03 required checkpoints/evidence are ready, a separate Candidate Assembly Agent/process fixes one Trial01 Candidate SHA. No individual Coding Agent may claim its package checkpoint is the Fixed Trial Candidate unless explicitly assigned Candidate Assembly responsibility.

## 12. Coding Agent prohibited work

Package Coding Agent must not:

- read G01 07/P00/other Pxx/Gate06/00-30/ADR/past ENH/issues/Web to discover required behavior;
- execute another package;
- assemble Fixed Candidate;
- make Gate PASS/FAIL decision;
- modify protected/canonical documents;
- expand package scope to solve unrelated findings.

Each assigned Pxx must be sufficient on its own; ambiguity causes `BLOCKED_CONTRACT_AMBIGUITY`.

## 13. Required outputs

### SINGLE_EXECUTION

N/A — G01 does not use single-execution mode.

### WORK_PACKAGE

Per Pxx:

- package implementation changes
- exact focused verification commands/results
- package checkpoint commit identity
- package status/checkpoint report under Trial01 `20_implementation_reports`
- evidence commit/push per operator workflow
- final `PACKAGE_READY` or explicit `BLOCKED_*`

Gate-wide outputs after packages: Fixed Trial Candidate + Candidate Assembly completion record, then Independent Verification evidence/decision.

## 14. External reference policy

This Gate06 is self-contained for Gate-wide semantics. It may cite source/evidence as provenance. It is not the Coding Agent direct entry source in Work Package Mode; operator prompt resolves assigned Pxx.

## 15. Stop condition

Stop/escalate rather than broaden if:

- canonical requirement/design appears to require revision;
- backend catalog/API/schema must change;
- approved legacy/presentation mapping conflicts with a higher-authority canonical product requirement;
- package cannot meet its contract without another package/unrelated refactor;
- repository preflight is dirty/wrong branch/ambiguous;
- assigned Pxx is insufficient or contradictory.
