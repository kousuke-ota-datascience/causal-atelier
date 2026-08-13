# ENH-E6 設計書改定

> **Document class:** Planning / Decision Artifact  
> **Self-containment:** MUST for own subject.

**重要:** canonical design documents are not revised. 本書はENH-E6 bugfixのeffective implementation design deltaを記録する。

## 1. Source design documents

- `docs/wiki/requirement_definition/**` — canonical design provenance, READ ONLY
- ENH-E5 Family/Stage navigation background/G01 contracts
- current frontend source: `frontend/app.js`, `frontend/navigation_state.js`, `frontend/index.html`, `frontend/styles.css`
- existing frontend/product/browser tests
- ENH-E6 Architecture Review artifacts

## 2. Design delta

Current fragmented flowをsingle Navigation Transition Authorityへ収束する。

Conceptual flow:

```text
entry intent / parsed canonical URL
  -> resolve + validate NavigationContext against catalog
  -> applyAnalysisNavigation(context, historyMode, source)
       -> commit state.navigationContext
       -> synchronize history according to mode
       -> render/select Family tabs
       -> render/select current Family Stage sidebar
       -> resolve stage-aware presentation binding
       -> activate presentation surface
       -> refresh route-dependent availability
       -> deterministic focus/error state
```

Function/module nameはimplementation detail。重要なのはside-effect ownershipとentry convergence。

## 3. Authority / ownership changes

| Concern | Before problem | ENH-E6 target authority |
|---|---|---|
| navigation intent parse/default | mixed entry logic | pure navigation-state model/catalog validation |
| application of NavigationContext | distributed among activation/restore/handlers | one transition coordinator |
| browser history | multiple entry-specific updates | transition coordinator with explicit `push/replace/none` mode |
| Family/Stage shell | renderer invoked only on some paths | coordinator-owned render lifecycle |
| presentation activation | Family-only/legacy workspace selection | stage-aware presentation binding called by coordinator |
| legacy analysis left nav | workspace + route authority | compatibility context resolver only |

## 4. Runtime / data-flow changes

Entry convergence includes:

- Family tab click
- Stage click
- canonical URL initial restore
- reload
- browser `popstate`
- legacy route normalization
- legacy analytical left-nav shortcut

History policy:

- user navigation -> `pushState`
- one-way legacy normalization -> `replaceState`
- initial canonical restore / `popstate` -> no new history entry
- same target -> avoid unnecessary duplicate history

Presentation binding minimum:

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

Legacy shortcut targets:

```text
Explore -> exploratory/profile
Predictive -> predictive/setup
Causal Discovery -> causal/discovery
Causal Inference -> causal/identification
```

## 5. Persistence / migration changes

`NONE` expected.

- no DB migration
- no new Domain Resource field
- no Execution Stage mapping/persistence
- no Navigation Context persistence beyond existing client/browser state semantics
- no backend catalog schema change

If implementation proves persistence/API schema change necessary, current contract is insufficient and work must stop/escalate rather than silently expand scope.

## 6. Compatibility / rollout strategy

- existing legacy analytical buttons remain visible for E6 compatibility but become canonical shortcuts.
- existing canonical/legacy route normalization remains supported.
- existing Explore/Predictive/Discovery/Inference surfaces are reused; E6 does not redesign them.
- non-analysis workspace navigation remains unaffected except shell visibility lifecycle.
- fail closed on missing supported stage presentation binding.

## 7. Temporary architecture / Transition Debt candidates

- complete removal/redesign of legacy left navigation remains future work.
- all exploratory/predictive stages sharing one existing surface is accepted for E6; stage-specific screen redesign is out of scope.
- `ANOM-E5-001` remains OPEN until G01 final PASS.

## 8. Gate implications

One Gate G01 because transition authority, observable shell, presentation binding, legacy compatibility, history behavior, and real-browser proof jointly establish one user-visible navigation contract.

Work Packages:

- P01: transition authority/lifecycle convergence
- P02: stage-aware presentation + legacy compatibility
- P03: regression/browser harness strengthening

P01/P02 completion alone cannot establish G01 PASS.
