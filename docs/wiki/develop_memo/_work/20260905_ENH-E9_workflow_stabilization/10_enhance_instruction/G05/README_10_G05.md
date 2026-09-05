# ENH-E9 Gate G05 — Integrated Regression Acceptance

- Contract status: `DRAFT_NOT_FROZEN`
- Execution mode: `SINGLE_EXECUTION`
- Dependency: G04 final PASS

## Semantic claim

E9 residual fixesを統合した後も、E8で確立したCausal workflowが1つのbrowser journeyとして成立する。

## Draft critical journey

```text
Analysis Context
 -> Discovery
 -> Graph review / comparison
 -> FIXED Graph
 -> Identification
 -> Estimation
 -> Effects
 -> Diagnostics
```

## Protected regression

- ENH-E8 G01/G02/G03 final protected contracts
- Result / Execution lineage
- Navigation Stage / Execution operation separation
- existing API route grammar
- Outcome one-way ownership
- G01-G04 final PASS contracts

G05は新機能実装Gateではなくintegrated acceptance boundary。G05で新しいsemantic defectが見つかった場合、owner Gate/contractへtraceして扱う。
