# ENH-E6 Existing Implementation / Design Alignment Review

**Document class:** Planning / Evidence Artifact  
**Self-containment:** MUST for source-alignment conclusion.

- Status: `COMPLETE_SOURCE_INSPECTION / RUNTIME_REPRODUCED`
- Production baseline: `5a5ced9bd6a0e62027c4058eb66ec487719bde23`

## 1. Purpose

ENH-E5 intended Family/Stage navigation semanticsとproduction implementationを照合し、missing componentではなくlifecycle/integration anomalyであること、target change boundaryを特定する。

## 2. Evidence inventory

| Evidence | Observed fact |
|---|---|
| `frontend/index.html` | `analysis-family-tabs`, `analysis-stage-sidebar` containers exist |
| `frontend/index.html` | legacy `Causal Discovery` and `Causal Inference` coexist |
| `frontend/app.js` | Family-only analysis workspace mapping includes `causal:'discovery'` |
| `frontend/app.js` | normal workspace activation mutates active state/history/navigation context |
| `frontend/app.js` | canonical route restore invokes analysis navigation rendering |
| `frontend/app.js` | Family/Stage handlers route through restore path |
| `tests/product/test_enh_e5_g01_navigation_shell.py` | static/source-string contract checks exist |
| ENH-E5 P02/07 | Family tabs, Family-local sidebar, `(family, stage)` binding and browser-layer behavior were intended |
| ENH-E5 debt ledger | `ANOM-E5-001` requires fresh observable UI/real tab operation follow-up |

## 3. Alignment classification

### MATCH

- Family/Stage catalog model
- canonical route parse/serialize concept
- DOM shell existence
- catalog-driven Family/Stage renderer existence
- Family/Stage event handling primitives

### PARTIAL / DEFECT

- A-001: normal transition does not guarantee shell render lifecycle.
- A-002: Family-only presentation selection does not express Causal Discovery/Inference stage boundary.
- A-003: legacy analytical nav retains dual workspace/route responsibility.
- A-004: source contract inspection does not prove normal-entry observability.

## 4. Root cause

- Direct: normal entry does not converge on canonical analysis navigation application/render lifecycle.
- Structural: NavigationContext apply is not a first-class single authority; state/history/render/presentation responsibilities are distributed.
- Structural: stage-aware presentation binding is incomplete.
- Process: observable real-browser journey was not a blocking proof despite source elements existing.

## 5. Runtime reproduction

2026-08-13 Human owner executed existing Playwright/Chromium harness against pre-fix baseline:

```text
HEALTH: API READY
AFTER_PROJECT_SELECT_URL: http://frontend/projects/<project_id>/data
AFTER_EXPLORE_URL: http://frontend/projects/<project_id>/analysis/exploratory/profile
FAMILY_TAB_CONTAINER_COUNT: 1
FAMILY_BUTTON_COUNT: 0
STAGE_BUTTON_COUNT: 0
```

This establishes a clean runtime negative control: API availability and canonical Project Analysis route are established, yet Family/Stage buttons remain unrendered. It does not prove the future fix.

## 6. Alignment conclusion

ENH-E6 is not a missing-HTML/CSS-only repair. The required fix is lifecycle/authority integration plus stage-aware presentation/legacy compatibility, followed by real-browser regression proof. Backend catalog/schema changes are not supported by current evidence and remain outside allowed production scope unless a new blocking fact is established and escalated.
