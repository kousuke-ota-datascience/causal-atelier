# ENH-E7 Target Architecture Decision Record

**Status:** PROPOSED_PENDING_LOCAL_SOURCE_CONFIRMATION

| Decision | Proposed target | Status |
|---|---|---|
| AR-E7-01 Application route authority | separate Project route authority from existing Analysis route authority | PROPOSED |
| AR-E7-02 Project/Analysis boundary | Project Management owns resources; Analysis Workspace consumes analysis context | PROPOSED |
| AR-E7-03 Shell ownership | Projects / Project Management / Analysis Workspace are separate presentation scopes | PROPOSED |
| AR-E7-04 Analysis Context | Project URL-derived/read-only; Context/Dataset/View selectable existing resources | PROPOSED |
| AR-E7-05 Analysis View ownership | lifecycle management in Data; selection in Analysis Workspace | PROPOSED |
| AR-E7-06 Results boundary | persisted cross-analysis aggregation in Results/Lineage; stage-local presentation in Analysis | PROPOSED |
| AR-E7-07 Legacy policy | remove duplicate legacy UI shortcuts; retain/normalize legacy URLs | PROPOSED |
| AR-E7-08 Causal mapping | Setup/Discovery/Identification/Estimation/Effects/Diagnostics/Sensitivity mapping in plan | PROPOSED |
| AR-E7-09 Exploratory ambiguous items | freeze Data Quality/TIME_TREND/CHART from source facts; do not invent operations | OPEN_LOCAL_CONFIRMATION |
| AR-E7-10 API/persistence | no changes expected; confirm sufficiency from source | OPEN_LOCAL_CONFIRMATION |
| AR-E7-11 local Git identity | remote alias and E7 baseline full SHA | OPEN_LOCAL_CONFIRMATION |

## Approval condition

Architecture Review becomes APPROVED only when all OPEN_LOCAL_CONFIRMATION items are resolved with source evidence and no decision conflicts with verified upstream contracts.
