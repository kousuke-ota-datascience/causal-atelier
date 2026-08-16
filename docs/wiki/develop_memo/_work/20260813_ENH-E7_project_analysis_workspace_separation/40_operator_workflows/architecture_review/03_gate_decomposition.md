# ENH-E7 Gate Decomposition Decision

**Status:** PROPOSED

## G01 — Project Management Surface Contract

PASS establishes Project creation/selection/management as an independent URL-authoritative resource-management surface.

Why one Gate: route authority, ownership and Project-local resource surfaces must work together before Analysis Workspace can safely depend on them.

Execution decomposition: P01-P07.

## G02 — Analysis Workspace Contract

PASS establishes Analysis Context, Family/Stage workspace, existing Causal/Exploratory/Predictive operability, legacy compatibility and cross-surface browser semantics.

Why one Gate: a shell without existing functional operability is not a downstream-usable Analysis contract.

Execution decomposition: P01-P06.

## Dependency

```text
G01 PASS -> G02
```

Implementation volume is handled by Work Packages, not extra Gates.
