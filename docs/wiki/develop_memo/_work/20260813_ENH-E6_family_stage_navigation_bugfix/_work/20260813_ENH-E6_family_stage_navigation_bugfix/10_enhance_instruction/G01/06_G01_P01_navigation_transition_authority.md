# ENH-E6 G01 P01 — Navigation Transition Authority

**Document class:** Primary Execution Contract — Work Package  
**Self-containment:** MUST — assigned Coding Agentは本P01だけでrequired behavior / constraints / verification / completion / stopを一意に判断できること。

- Enhancement: `ENH-E6`
- Gate: `G01`
- Package: `P01`
- Trial: operator-supplied (`Trial01` at first execution)
- Status: `APPROVED / READY_TO_EXECUTE`
- Target branch: `bugfix/ariadne_mvp_e6`
- Canonical product requirements/design: READ ONLY

## 1. Purpose

Analysis Family/Stage `NavigationContext`をapplication state、browser history、Family/Stage Navigation Shellへ適用するlifecycleを一つのtransition authorityへ収束させる。

P01は「Family tabを表示するために特定pathへrender callを足す」だけのsymptom patchではない。各entryがstate/history/renderを独立操作する構造を解消し、P02がstage-aware presentation/legacy mappingを一つのexplicit presentation seamへ接続できる状態を作る。

## 2. Effective Gate constraints applicable to this package

P01が守るeffective constraints:

- Family values: `EXPLORATORY / PREDICTIVE / CAUSAL`。
- backend navigation catalog is authority for Family order/label/default/stages。
- canonical route: `/projects/{project_id}/analysis/{family_slug}/{stage_slug}`。
- `Navigation Stage != Execution Stage`。
- Navigation ContextをDomain Resource/Executionへpersistしない。
- user navigation historyはpush、legacy normalizationはreplace、initial canonical restore/popstateはnew history entryを作らない。
- unknown/invalid navigation contextはexplicit error semanticsを維持し、別Family/Stageへsilent fallbackしない。
- ENH-E5 historical evidenceと`docs/wiki/requirement_definition/**`は変更禁止。
- P01 completion != G01 PASS。

Known pre-fix runtime fact for implementation orientation: API READY / selected Project / canonical exploratory profile routeでもFamily buttons=0, Stage buttons=0。これはP01のrequired behaviorを外部文書から補完するための参照ではなく、本契約に埋め込まれたbaseline factである。

## 3. In scope

- navigation context application/coordinator seam in frontend code
- Family click -> NavigationContext application convergence
- Stage click -> NavigationContext application convergence
- canonical initial route restore/reload -> same application path
- browser popstate -> same application path without creating new history entry
- analysis shell rendering/selected lifecycle within transition authority
- explicit presentation activation hook/boundary that P02 can implement/use
- minimal pure helper changes needed for parse/default/validation integration
- focused unit/DOM/static tests required below

Likely change surfaces may include `frontend/app.js`, `frontend/navigation_state.js`, minimal related frontend helper/test files. File names are not authority; inspect repository implementation substrate and choose minimal package-consistent changes.

## 4. Explicitly out of scope

P01 must not:

- finalize or newly redesign the full stage-aware presentation mapping; P02 owns exact presentation/legacy compatibility integration.
- implement ENH-E6 dedicated browser E2E runner or Docker inclusion; P03 owns it.
- change canonical requirement/design documents.
- modify backend catalog/API/schema/persistence.
- fully remove/redesign legacy left navigation.
- add fallback mapping such as `causal -> discovery` as the new canonical presentation authority.
- perform unrelated refactor/cleanup/visual redesign.
- weaken/delete/skip tests.

P01 may create an explicit presentation resolver/activation seam, but must keep its mapping behavior compatible with current behavior until P02 changes the exact approved mapping.

## 5. Entry criteria / required evidence

Coding Agent must perform repository preflight per canonical operator prompt:

- current branch is `bugfix/ariadne_mvp_e6`
- working tree clean
- record runtime `START_SHA`
- assigned P01 file is resolved exactly once
- no current-Trial formal remediation route conflict

No specific historical SHA is required to equal the planning baseline because Human may commit governance/template-compliance documents before execution. Do not block merely because `START_SHA != 5a5ced9...`; instead inspect current source diff/history as implementation substrate only. If production code already contains unexplained ENH-E6 implementation changes that make this package contract ambiguous, stop `BLOCKED_CONTRACT_AMBIGUITY` or `BLOCKED_REPOSITORY_STATE` as appropriate.

## 6. Required implementation

### 6.1 Single context-application authority

Implement one effective orchestration path, conceptually:

```text
applyAnalysisNavigation(context, historyMode, source)
  -> validate context against loaded/current backend catalog
  -> commit state.navigationContext
  -> synchronize URL/history according to explicit mode
  -> render/update Family tabs and selected Family
  -> render/update current-Family Stage sidebar and selected Stage
  -> call one explicit presentation activation boundary
  -> refresh route-dependent availability/state required by current navigation
  -> apply deterministic focus/error semantics where existing UI requires it
```

Exact function/module name is implementation choice. Required invariant: entry handlers must not each duplicate the full state/history/shell mutation sequence.

### 6.2 Entry convergence required in P01

The following existing/implemented paths must delegate to the same context-application authority for the P01-owned parts:

- Family tab click
- Stage sidebar click
- canonical Analysis route initial restore/reload
- browser `popstate`

Legacy analytical left-nav exact target mapping is P02, but P01 must expose/use a seam allowing an already-resolved canonical NavigationContext to enter the same authority. Do not hard-code P02's full mapping into P01 merely to make legacy buttons pass.

### 6.3 Shell lifecycle

When a valid Analysis NavigationContext is applied and catalog is available:

- Family buttons are rendered from catalog and selected Family is unambiguous.
- Stage buttons are rendered from current Family catalog stages and selected Stage is unambiguous.
- this happens as part of the same transition, including normal non-reload navigation once P02/legacy entry supplies context.

When leaving Analysis for a non-analysis workspace, shell must not remain as misleading current navigation. Hide/clear/disable strategy is implementation choice, but stale selected analysis shell must not represent non-analysis state.

### 6.4 History behavior

The transition authority must support at least:

- `PUSH` for new user Family/Stage action
- `REPLACE` for one-way route normalization callers
- `NONE` for initial canonical route application and popstate/reload restore

Avoid duplicate same-target entries. P01 need not invent legacy normalization targets; it must provide correct mode semantics for callers.

### 6.5 Failure semantics

- validation failure: no silent context substitution
- catalog unavailable/invariant failure: explicit current error handling; do not fabricate frontend catalog
- presentation seam cannot resolve/activate: propagate explicit configuration/error signal rather than silently jumping to another stage/workspace
- route-dependent refresh failure: do not mutate navigation identity to a fallback route to hide error

## 7. Focused verification

Run all applicable current tests plus add/adjust focused tests proving P01 behavior. Exact filenames may follow repository conventions.

| Verification | Required proof |
|---|---|
| pure/unit | context parse/default/history mode helpers continue to behave; no Navigation->Execution persistence/coupling |
| DOM/integration | applying valid context renders/selects Family and current-Family Stage controls through shared authority |
| integration | Family and Stage click delegate to shared application flow; direct canonical restore/popstate do not create duplicate history |
| static/inspection | no multiple full state+history+shell mutation implementations remain among P01-owned entry paths |
| regression | affected existing navigation_state / frontend contract tests remain green |

Focused verification must not use direct test-only DOM injection/render invocation as the sole proof if it bypasses the application transition under test. P01 does not need to run the future ENH-E6 blocking browser runner owned by P03.

Record exact commands and results in package report.

## 8. Protected contract / Transition Debt constraints

- preserve backend catalog authority; no full Family/Stage catalog duplicate constants.
- preserve canonical route semantics.
- preserve Navigation Stage vs Execution Stage separation.
- preserve non-persistence.
- preserve ENH-E5 historical evidence.
- `ANOM-E5-001` remains OPEN after P01.
- legacy IA full removal remains out-of-scope debt/future work.

## 9. Checkpoint / reporting rule

After implementation + focused verification succeed:

1. review changed files/diff; only P01 scope.
2. create Package checkpoint commit per canonical operator workflow.
3. create/update `20_implementation_reports/G01/Trial01/packages/` P01 status/checkpoint evidence as directed by operator prompt.
4. report `START_SHA`, `PACKAGE_CHECKPOINT_SHA`, evidence commit identity, exact verification summary.

Do not write Gate Decision, Fixed Candidate, P02/P03 report, or G01 PASS.

## 10. Package completion criteria

P01 is `PACKAGE_READY` only when:

- one context-application authority exists for P01-owned entry paths;
- Family/Stage render/selection lifecycle is owned by that authority;
- history push/replace/none semantics are explicit and focused-tested;
- canonical restore/popstate/Family click/Stage click converge appropriately;
- a presentation activation seam exists for P02 without P01 over-owning exact mapping;
- focused verification passes;
- changes are committed as package checkpoint and evidence/report is recorded;
- no protected/out-of-scope changes are included.

## 11. External reference policy

**Normative source isolation is mandatory.** For specification completion, Coding Agent must NOT read:

- Gate-level `06`
- Gate `07`
- `P00`
- other Pxx
- any `00`-`30` planning/analysis/report documents
- ADR
- prior enhancements
- issues
- external Web

Current repository source/test/config/migration may be inspected to understand implementation substrate, but not as required-behavior authority. This P01 is the complete normative package contract. If it is insufficient/ambiguous, stop `BLOCKED_CONTRACT_AMBIGUITY`; do not search forbidden documents to fill gaps.

## 12. Stop rule

Stop without scope expansion if:

- canonical requirement/design revision appears necessary;
- backend API/catalog/schema/domain change appears necessary;
- P01 requires exact P02 mapping to finish its own required seam and cannot remain compatible;
- existing architecture cannot support a bounded transition seam without broad migration not specified here;
- repository state is dirty/wrong branch/contract match ambiguous;
- focused verification cannot pass within P01 scope;
- any contract ambiguity requires forbidden reference exploration.

Return one canonical status from operator prompt, normally `PACKAGE_READY` or explicit `BLOCKED_*`.
