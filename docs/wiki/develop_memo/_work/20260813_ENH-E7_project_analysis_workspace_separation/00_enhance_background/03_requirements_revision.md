# ENH-E7 Requirement改定

**文書種別:** Planning / Decision Artifact  
**Status:** PROPOSED_PENDING_ARCHITECTURE_REVIEW

## 1. Product Requirement delta

ENH-E7以前はProject lifecycle navigationとanalytical navigationがapplication hierarchy上で混在していた。
ENH-E7ではProject ManagementとAnalysis Workspaceの責務を明示的に分離する。

| Requirement ID | 改定後Requirement | Gate |
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
| E7-REQ-022 | FR-104/105の6つの機能的destination（Research Context / Data / Explore / Causal / Predictive / Results）はroute-addressableであることを維持する。Project ManagementのResearch Context / Data / Results、およびcanonical Analysis route `/projects/<project_id>/analysis/<family>/<stage>` のEXPLORATORY / CAUSAL / PREDICTIVE Familyがそれぞれを所有する。これは6個のpeer tab、old global shell、または旧route tokenの存続を要求しない。direct-link / reload / Back / ForwardはE7-REQ-019に従う。 | G02/G04 |

## 2. Workflow execution Requirement

- Enhancement-specific Agent entry promptをwork root配下へinstance化する。
- template側Agent promptを直接executionに使用しない。
- Enhancement-fixed identityをAgent execution前に解決する。
- Human operatorはruntime execution identifierだけを指定する。
- Coding Agentのnormative workflow contextをassigned Pxxのみに限定する。
- Pxxをself-containedにする。
- Coding AgentへGate 07をacceptance answer keyとして露出させない。
- Document complianceとAgent Execution Readinessを別判定にする。
- Readinessを4軸で検証し、不成立時はBLOCKEDとする。

## 3. Deprecatedとする挙動

G02 PASS後、旧Global sidebarのanalytical shortcutと、Project metadata / Dataset managementの混在責務を廃止する。

legacy analytical URLは削除せず、canonical Analysis routeへのcompatibility entryとして維持する。

## 4. Invariant

- Project Management = Project resource management。
- Analysis Workspace = Project context下のanalysis execution / presentation。
- Family = analysis paradigm。
- Stage = Family内のworkflow / presentation view。
- Operation = Stage内の処理。
- existing analysis execution semanticsを保護する。
