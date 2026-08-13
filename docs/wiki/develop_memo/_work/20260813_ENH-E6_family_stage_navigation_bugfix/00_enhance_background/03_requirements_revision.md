# ENH-E6 要件定義書改定

> **Document class:** Planning / Decision Artifact  
> **Self-containment:** MUST for own subject.

**重要:** 本artifact名はworkflow templateに従うが、ENH-E6はcanonical `docs/wiki/requirement_definition/**`を改定しない。本書は既存正本要求をbugfixで実現・検証するためのENH-local realization requirement deltaを記録する。

## 1. Source documents

- canonical requirements/design: `docs/wiki/requirement_definition/**` — provenance only / READ ONLY
- ENH-E5 background and frozen G01 contracts — inherited intended Family/Stage semantics
- ENH-E5 `ANOM-E5-001` ledger — source anomaly
- ENH-E6 architecture/source/preflight evidence — realization gap facts

## 2. Requirement delta

| Requirement ID | Before | After | Reason |
|---|---|---|---|
| E6-FR-001 | Family/Stage shell implementation elements exist but normal-entry observability not guaranteed | Analysis context entry直後、reloadなしで3 Family tabsとcurrent Family Stage listがobservable/operable | source existenceとuser-observable behaviorのgapを閉じる |
| E6-FR-002 | Family click handler存在 | actual Family clickがcatalog default Stage canonical contextへatomicに遷移 | Family switching requirementをobservableに固定 |
| E6-FR-003 | Stage click handler存在 | actual Stage clickがFamily維持でURL/state/selected/presentationを同期 | Stage-local navigation consistency |
| E6-FR-004 | canonical parse/restore存在 | direct route/reload/Back/Forwardでsame Navigation Contextを復元 | history/deep-link contract |
| E6-FR-005 | multiple transition responsibilities | all analysis navigation entries converge on single application transition authority | structural root cause remediation |
| E6-FR-006 | Family-only presentation mapping may select Causal discovery | presentation is deterministically bound by `(family, stage)` | Discovery/Inference boundary correction |
| E6-FR-007 | legacy left nav can act as workspace/route authority | analytical legacy entries are canonical-context compatibility shortcuts only | parallel authority elimination |
| E6-FR-008 | Discovery/Inference both use broad causal route semantics | exact compatibility entry targets are fixed: discovery→`causal/discovery`, inference→`causal/identification` | deterministic legacy behavior |
| E6-FR-009 | missing/unknown binding may be vulnerable to fallback | invalid catalog/context/binding fails explicitly; no silent fallback | prevent split-brain/misrouting |
| E6-NFR-001 | source/static tests can pass without observable shell | real Chromium must click actual Family/Stage elements in blocking proof | prevent E5 false positive recurrence |
| E6-NFR-002 | protected E5 behavior can regress during fix | affected E5 route/catalog/history/availability behavior remains regression-protected | bugfix compatibility |

## 3. New invariants / constraints

- `Navigation Stage != Execution Stage`.
- backend catalog remains Family/order/label/default/stage authority.
- canonical route remains `/projects/{project_id}/analysis/{family_slug}/{stage_slug}`.
- Navigation Context is not persisted to Domain Resource/Execution.
- one transition application authority owns side-effect ordering; entry handlers do not duplicate full state/history/render logic.
- presentation mapping uses `(family, stage)` where stage distinguishes existing surfaces.
- legacy analysis navigation is compatibility entry, not parallel state authority.
- no silent fallback for missing presentation binding.
- real-browser actual-element operation is mandatory for observable acceptance.

## 4. Removed / deprecated requirements

Canonical requirement removal: `NONE`.

Deprecated implementation assumptions:

- Family-only `causal -> discovery` as canonical presentation authority.
- legacy analytical button independently activating workspace/history/navigation state.
- source-string existence as sufficient proof of observable Family navigation.

## 5. Acceptance implications

Requirements map to G01 ACs:

- E6-FR-001 -> AC-001
- E6-FR-002 -> AC-002
- E6-FR-003 -> AC-003
- E6-FR-004 -> AC-004
- E6-FR-005 -> AC-005
- E6-FR-006 -> AC-006
- E6-FR-007 -> AC-007
- E6-FR-008 -> AC-008
- E6-FR-009 -> AC-009
- E6-NFR-001 -> AC-010
- E6-NFR-002 -> AC-011

Independent Verification authority is frozen G01 07; Coding Agent does not receive 07.
