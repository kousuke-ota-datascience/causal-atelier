# G03 P01 — Identification Input Ergonomics

**Status:** `FROZEN`  
**Gate authority:** G03 06/07  
**Depends on:** G02 canonical `999_gate_decision = PASS`

## Scope

Implement only the G03 residual interaction improvements:

- Population help/tooltip explaining target population meaning.
- Comparator help/tooltip explaining counterfactual/reference condition meaning.
- Treatment selector whose candidate authority is the selected Dataset Version schema.
- Clear or invalidate stale Treatment when Dataset Version/schema changes remove the selected candidate; do not silently retain it.
- Preserve Identification Outcome as automatic/read-only projection from the selected FIXED Graph designated Outcome.

Baseline-satisfied behavior may be evidence-only; do not reimplement without need.

## Protected semantics

Preserve existing causal-question serialization/backend validation, FIXED Graph prerequisite, Population/Treatment/Comparator/Outcome/Time/Estimand/Decision Use semantics, identification strategy, adjustment set, assumptions, designated Outcome lineage, and selected Identification Result → Estimation lineage.

## Forbidden

- independent editable Outcome selector/free text
- selector-local scientific validation that replaces backend authority
- new Dataset schema API
- Estimation submission architecture change
- unrelated Graph/Estimation refactoring

## Focused verification

Use static/syntax plus focused frontend interaction/unit and integration/contract/regression tests sufficient to prove:

1. help text is present and semantically correct;
2. Treatment candidates come from selected Dataset Version schema;
3. stale Treatment is not silently retained;
4. serialization/backend validation remains compatible;
5. FIXED Graph Outcome remains automatic/read-only;
6. Graph → Identification → Estimation protected lineage is unchanged.

**Do not run Browser E2E in this Package.** Browser E2E is deferred to G05 final Gate-level verification.

## Completion boundary

Package is complete only when scope implementation/evidence and focused non-browser verification pass, no protected invariant changes are introduced, no unresolved blocker remains, and the package checkpoint/report are produced. Package completion is not G03 PASS.
