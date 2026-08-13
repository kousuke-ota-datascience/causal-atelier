# ENH-E6 Architecture Discovery Result

> **Document class:** Planning / Operator Artifact  
> **Product code changes:** NONE.

- Target: `ENH-E6`
- Source baseline: `5a5ced9bd6a0e62027c4058eb66ec487719bde23`
- Discovery status: `COMPLETE_FOR_PLANNING`

## Fact / Inference / Unknown

| Category | Classification | Observation |
|---|---|---|
| 1. runtime entrypoints | Fact | left navigation workspace buttons, Family/Stage buttons, canonical route restore, popstate/reload are analysis navigation entry classes |
| 2. request/navigation lifecycle | Fact | normal workspace activation and canonical route restore have different side-effect paths; canonical restore invokes navigation renderer |
| 3. canonical write paths | Fact | client NavigationContext/history are mutated in frontend; no evidence of domain persistence requirement |
| 4. canonical read paths | Fact | backend navigation catalog supplies Family/Stage structure; URL/context are used for route restore |
| 5. ownership/authority | Fact | state/history/render/presentation responsibilities are distributed across frontend functions |
| 6. persistence/schema | Fact | no ENH-E6 need/evidence for new DB model/migration; Navigation Context is non-persistent UI state |
| 7. lineage/artifact relation | N/A | Family/Stage navigation is not a scientific result lineage resource |
| 8. legacy/duplicate paths | Fact | legacy analytical left-nav and canonical Family/Stage routing coexist; Causal Discovery/Inference are separate workspaces under broad causal route semantics |
| 9. UI/API/job divergence | Fact | UI catalog depends on backend authority; clean preflight showed API READY/canonical route while shell children remained zero, isolating frontend integration gap |
| 10. tests encoding behavior | Fact | static/source contract tests exist; Playwright browser harness exists; observable Family tab normal-entry proof was missing |

Additional facts:

- DOM containers and renderer code exist; defect is not simply missing markup.
- Family-only presentation mapping includes `causal -> discovery`.
- existing inference surface starts at Identification semantics before estimation.

Inferences supported by facts:

- direct defect is missing lifecycle convergence, not only CSS/DOM creation.
- root architecture issue is fragmented NavigationContext application authority.
- stage-aware presentation binding is required to represent existing Causal surfaces.

Unknowns resolved before freeze:

- Whether defect reproduces under API READY Project context: resolved YES by clean preflight.
- Existing browser harness/canonical invocation: resolved Playwright/Chromium compose pattern.

Remaining runtime-derived unknowns are implementation/candidate identities, not target architecture ambiguity.

## Target decision topics

1. single Navigation Context application authority
2. pure navigation model vs side-effect coordinator boundary
3. exact stage-aware presentation mapping
4. legacy analytical shortcut targets/responsibility
5. shell lifecycle in analysis/non-analysis context
6. history push/replace/none semantics
7. fail-closed missing binding
8. one Gate vs multiple execution packages
