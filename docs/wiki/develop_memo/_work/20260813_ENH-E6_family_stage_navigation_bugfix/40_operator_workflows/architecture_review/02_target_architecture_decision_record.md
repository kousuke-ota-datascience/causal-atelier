# ENH-E6 Target Architecture Decision Record

> **Document class:** Planning / Operator Artifact

## 1. Context

Family/Stage UI components exist but normal entry can establish canonical Analysis URL without observable Family/Stage buttons. Multiple frontend paths own portions of state/history/render/presentation and Causal presentation uses Family-only mapping. ENH-E6 must repair implementation without changing canonical requirements/design/backend catalog.

## 2. Current architecture facts

- backend catalog is authoritative for Family/Stage structure.
- `frontend/app.js` has legacy workspace activation, route restore, shell rendering, presentation activation responsibilities distributed.
- canonical route restore renders navigation; normal activation is asymmetric.
- legacy Causal Discovery/Inference exist as separate workspaces.
- browser harness can reproduce defect with API READY.

## 3. Decision

Adopt a single frontend NavigationContext application authority. Entry paths resolve/parse an intended context, then delegate side effects to that authority. Separate pure parse/default/validation logic from coordinator DOM/history/presentation side effects. Presentation resolver uses `(family, stage)` for Causal surface boundary. Legacy analytical nav becomes compatibility context resolver, not parallel state authority.

## 4. Canonical authorities

| Concern | Canonical authority after completion |
|---|---|
| Family/stage labels/order/default/list | backend navigation catalog |
| URL representation | canonical `/projects/{id}/analysis/{family}/{stage}` serializer/parser |
| applied client navigation state | single NavigationContext application coordinator |
| browser history side effects | same coordinator with push/replace/none mode |
| shell selected/render state | coordinator based on catalog + current context |
| presentation surface | `(family, stage)` presentation resolver invoked by coordinator |
| legacy analysis entry | compatibility context mapping -> coordinator |

## 5. Invariants

| ID | Invariant | Verification implication |
|---|---|---|
| E6-INV-01 | Navigation Stage != Execution Stage | no runtime persistence/coupling in code/static audit |
| E6-INV-02 | backend catalog remains structural authority | no duplicated full catalog; browser order/labels match catalog |
| E6-INV-03 | one applied-navigation side-effect authority | entry path code/integration audit |
| E6-INV-04 | history semantics explicit | Back/Forward/reload browser + lower-layer tests |
| E6-INV-05 | stage-aware Causal presentation | discovery vs identification/estimation tests |
| E6-INV-06 | legacy analysis nav is compatibility-only | exact routes and no split-brain state |
| E6-INV-07 | fail closed | missing/unknown binding tests |
| E6-INV-08 | canonical docs/historical evidence immutable | candidate diff audit |

## 6. Constraints

- no canonical requirement/design revision
- no DB/API/catalog schema change expected
- reuse existing presentation surfaces
- retain legacy visual entries for compatibility
- no assertion weakening/reload workaround

## 7. Explicitly removed / deprecated paths

Deprecated as canonical authority:

- Family-only `causal -> discovery` presentation selection.
- legacy analytical handler independently mutating workspace/history/navigation state.
- source-string existence as sufficient observable acceptance proof.

Legacy visual navigation itself is not removed.

## 8. Transition strategy and temporary debt

P01 introduces convergence seam; P02 binds exact presentation/legacy semantics; P03 fixes observable proof. Until G01 PASS, ANOM-E5-001 remains open. Full legacy IA removal stays future work.

## 9. Alternatives considered

- one-line `renderAnalysisNavigation()` addition: rejected; leaves fragmented authority.
- immediate full legacy nav removal: rejected; bugfix scope too broad.
- Causal Inference -> `causal/estimation`: rejected; compatibility entry should start at identification consistent with existing flow/stage order.

## 10. Consequences / risks

Positive: one navigation state authority, deterministic history/presentation, better testability. Risks: regression in workspace activation/history/focus; Causal mapping mismatch; browser harness inclusion. Mitigate via package boundaries and layered/real-browser verification.

## 11. Approval

- Status: `APPROVED`
- Authority: `Human owner`
- Timestamp: `2026-08-13`
