# ENH-E6 Design Revision

- Status: `READY_FOR_OWNER_REVIEW`

## 1. Design claim

Family/Stage navigation は `NavigationContext` を唯一のcanonical presentation stateとして扱い、Navigation Contextを適用する単一 coordinator を設ける。

概念interface:

```text
applyAnalysisNavigation(context, historyMode, source)
  1. validate context against backend catalog
  2. commit state.navigationContext
  3. synchronize browser history / canonical URL
  4. render Family tabs / Stage sidebar selected state
  5. resolve (family, stage) -> presentation binding
  6. activate presentation surface
  7. refresh route-dependent operation availability
  8. apply deterministic focus policy
```

`historyMode` は少なくとも `push / replace / none(popstate restore)` を区別する。

## 2. Entry-path convergence

次のentryは直接state/history/renderを個別操作せず、contextを構築・parseした後 `applyAnalysisNavigation` へ委譲する。

- Family tab click
- Stage sidebar click
- canonical URL direct open
- reload
- `popstate`
- legacy analysis route normalization
- legacy analytical left-nav compatibility shortcut

## 3. Separation of concerns

### Pure navigation model

`frontend/navigation_state.js` は可能な限り以下のpure function責務を持つ。

- parse / serialize
- defaultContext
- navigationContext validation
- legacy route -> canonical context normalization

DOM activation、workspace visibility、focus、API refreshをpure navigation modelへ混入しない。

### Coordinator / presentation layer

`frontend/app.js` または専用frontend moduleが次を所有する。

- transition orchestration
- render lifecycle
- presentation binding
- history side effect
- operation availability refresh
- focus

## 4. Stage-aware presentation binding

canonical binding keyは `(familySlug, stageSlug)`。

E6 minimal mapping:

```text
exploratory/* -> explore
predictive/*  -> predictive
causal/setup -> discovery
causal/discovery -> discovery
causal/identification -> inference
causal/estimation -> inference
causal/effects -> inference
causal/diagnostics -> inference
causal/sensitivity -> inference
```

未知のsupported catalog stageにbindingが無い場合は configuration defect。`discovery` 等へsilent fallbackしない。

## 5. Legacy responsibility boundary

legacy left navigationは non-analysis workspaces と analysis compatibility shortcuts を同じvisual navに置いていてもよいが、analysis shortcutはcanonical route contextを生成するだけとする。

禁止:

```text
legacy button
  -> independently select workspace
  -> independently push legacy URL
  -> independently mutate navigationContext
```

要求:

```text
legacy button
  -> resolve compatibility NavigationContext
  -> applyAnalysisNavigation(...)
```

## 6. Observable shell lifecycle

analysis shellは `NavigationContext != null` のanalysis contextでobservableとなる。

non-analysis workspaceでは以下のどちらかを明示実装する。

- shellをhiddenにする、または
- disabled/non-current stateを表示する

常時空DOMを画面上に置き、rendererが偶然呼ばれた時だけ内容が入る設計は禁止する。

E6では既存レイアウトへの影響を最小化するため、analysis contextでshow / non-analysis contextでhideを推奨する。

## 7. Failure semantics

- navigation catalog unavailable: navigation actionを開始せず explicit error
- unknown Family/Stage: canonical route error
- missing presentation binding: configuration error
- transition中API refresh failure: context/URLをsilent rollbackして別Stageへ移さない。error stateを表示し、selected route identityを保持する

## 8. Alternatives rejected

### A. `activateWorkspace()` に `renderAnalysisNavigation()` を1行追加

Rejected as root fix。通常導線の症状は改善しても、複数のstate/history/render authorityとFamily-only presentation bindingを残す。

### B. legacy left navを即時全削除

E6 bugfixとしてscopeが過大。compatibility shortcutへ降格し、primary authorityのみ除去する。

### C. `Causal Inference` を `causal/estimation` に直結

Inference画面はIdentification/Eligibilityを先行前提としており、canonical causal stage orderもidentificationが先。compatibility入口は `causal/identification` が一貫する。
