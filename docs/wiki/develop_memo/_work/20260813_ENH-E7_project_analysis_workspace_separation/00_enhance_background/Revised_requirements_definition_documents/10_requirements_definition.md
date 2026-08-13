# Requirement定義 — ENH-E7 effective delta

| Requirement ID | Requirement | Gate |
|---|---|---|
| E7-REQ-001 | `/projects`をProject Listのcanonical surfaceとする。 | G01 |
| E7-REQ-002 | `/projects/new`をProject Registerのcanonical surfaceとする。 | G01 |
| E7-REQ-003 | `/projects/<project_id>/overview`をselected Projectのdefault canonical surfaceとする。 | G01 |
| E7-REQ-004 | Overview / Research Context / Data / ResultsをProject Management local navigationとする。 | G01 |
| E7-REQ-005 | Project metadataとDataset / Analysis View lifecycle managementを別responsibilityにする。 | G01 |
| E7-REQ-006 | Project Archiveをselected Project lifecycle operationとしてOverviewに置く。 | G01 |
| E7-REQ-007 | Analysis View lifecycle managementをDataが所有し、Analysis Family横断で利用可能にする。 | G01 |
| E7-REQ-008 | Analysis WorkspaceをProject Managementとは別surfaceとする。 | G02 |
| E7-REQ-009 | Analysis ContextにCurrent Project / Active Research Context / Dataset Version / Analysis Viewを表示する。 | G02 |
| E7-REQ-010 | Analysis Workspace内のCurrent Projectはread-onlyとする。 | G02 |
| E7-REQ-011 | Family / Stage navigationはAnalysis Workspace内だけに表示する。 | G02 |
| E7-REQ-012 | canonical Analysis routeの意味論を維持する。 | G02 |
| E7-REQ-013 | Family切替時のdefault Stageはexisting catalog authorityで解決する。 | G02 |
| E7-REQ-014 | 既存Causal surfaceを定義Stage Contentsから操作可能にする。 | G02 |
| E7-REQ-015 | 既存Exploratory surfaceを定義Stage Contentsから操作可能にする。 | G02 |
| E7-REQ-016 | 既存Predictive surfaceを定義Stage Contentsから操作可能にする。 | G02 |
| E7-REQ-017 | Predictive Stage navigationで新Predictive Execution modelを作らない。 | G02 |
| E7-REQ-018 | legacy analytical URLをcanonical Analysis routeへnormalizeする。 | G02 |
| E7-REQ-019 | direct-link / reload / Back / ForwardをProject/Analysis双方で成立させる。 | G01/G02 |
| E7-REQ-020 | Results / Lineageがpersisted cross-analysis aggregation等を所有する。 | G01 |
| E7-REQ-021 | UI再編だけを理由にbackend analysis/domain semanticsを変更しない。 | G01/G02 |

Workflow execution-control Requirementは `../03_requirements_revision.md` に定義する。
