# ENH-E6 Requirements Revision

- Status: `APPROVED / FROZEN FOR ENH-E6 G01`
- Scope: ENH-E5 Family/Stage navigation contract の observable integration bugfix

## Requirement delta

ENH-E6 は E5 canonical Family/Stage catalog自体を変更しない。E5要件が real user journey で観測可能かつ一貫して成立するためのintegration requirementを追加・明確化する。

| ID | Requirement | Level | Delivery |
|---|---|---|---|
| E6-FR-001 | Project選択後、supported analysis entryから遷移した時点で、reloadを要求せず3 Family tabsがobservableでなければならない | MUST | ENH-E6 |
| E6-FR-002 | Family tab click は target Family の backend-catalog default Stageへ遷移し、URL / application state / selected tab / Stage list / presentationを同期しなければならない | MUST | ENH-E6 |
| E6-FR-003 | Stage click は current Familyを保持し、selected Stage route/state/presentationを同期しなければならない | MUST | ENH-E6 |
| E6-FR-004 | canonical deep link / reload / browser back-forward は同じ Navigation Context とobservable UIを復元しなければならない | MUST | ENH-E6 |
| E6-FR-005 | Navigation Contextの変更は単一のtransition authorityを通り、各entry handlerがstate/history/renderを独立に再実装してはならない | MUST | ENH-E6 |
| E6-FR-006 | presentation binding は最低限 `(AnalysisFamily, navigation_stage_id)` を入力として決定でき、Family単位だけでCausal presentationを固定してはならない | MUST | ENH-E6 |
| E6-FR-007 | legacy analytical left navigationを残す場合、それはcanonical Family/Stage routeへのcompatibility entryであり、parallel navigation authorityになってはならない | MUST | ENH-E6 |
| E6-FR-008 | Causal Discovery legacy entryは `causal/discovery`、Causal Inference legacy entryは `causal/identification` をcompatibility entry pointとする | MUST | ENH-E6 |
| E6-FR-009 | renderer missing / invalid catalog / unsupported presentation binding は明示errorとし、別Family/Stageへのsilent fallbackを禁止する | MUST | ENH-E6 |
| E6-NFR-001 | Gate blocking verification はFamily tabをreal browserで実際にclickし、DOM text existenceだけではPASSできない | MUST | ENH-E6 |
| E6-NFR-002 | E5 protected route/history/catalog semanticsをregressionさせない | MUST | ENH-E6 |

## Non-requirements

- Navigation StageをExecution Stageへ変換・persistすること
- Family tabごとに別backend endpointを新設すること
- current analysis algorithmsを変更すること
