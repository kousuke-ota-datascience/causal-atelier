# ENH-E7 Target Architecture Decision Record

**Status:** APPROVED

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
| AR-E7-09 Exploratory ambiguous items | Data Quality/TIME_TREND/CHARTはG02 freeze前にsource factで確定し、operationを捏造しない | APPROVED_WITH_G02_DEFERRED_CONFIRMATION |
| AR-E7-10 API/persistence | G01/P01開始時点では変更不要をapproved baselineとする。反証時はaffected packageをBLOCKEDしamendmentへ移行 | APPROVED |
| AR-E7-11 local Git identity | remote=`causal-atelier` / branch=`feature/ariadne_mvp_e7` / baseline=`1beea1c9eb3ffa5d01f7c266b826e52136d01e8f` | APPROVED |

## Approval condition

HumanはArchitecture Reviewを承認した。

G01/P01開始に必要なarchitecture decisionはAPPROVEDとする。
G02-specificなExploratory詳細配置はG02 06/07 freeze前のsource confirmationへdeferする。
deferred itemを理由にG01 contractを拡張・推測してはならない。
