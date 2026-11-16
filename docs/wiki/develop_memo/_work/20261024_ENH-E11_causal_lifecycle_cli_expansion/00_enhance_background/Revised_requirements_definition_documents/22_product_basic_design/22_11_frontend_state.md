# 22_11_frontend_state


---

## 14. Frontend State Design

Frontend stateは次の責務へ分離する。

- server state: API query cache
- Project route state: Project list/registerまたはProject / Project section
- Analysis route state: Project / Family / Navigation Stage / optional resource identity
- Analysis Context selection: Research Context / Dataset Version / Analysis View
- draft state: unsaved form
- authoritative resource state: backend Resource status
- async presentation state: `IDLE / LOADING / READY / EMPTY / PARTIAL / ERROR / CANCELLED`

Authority rule:

1. Analysis WorkspaceのCurrent ProjectはURL `project_id`をauthorityとしread-only。
2. Current Family / Navigation Stageはcanonical Analysis route / application navigation stateをauthorityとする。
3. Research Context / Dataset Version / Analysis Viewはcurrent Projectと整合するexisting resource/stateだけを復元する。
4. Dataset Version変更でAnalysis Viewが互換でなくなればAnalysis View selectionを解除する。
5. context selection不足だけを理由にFamily / Stage routeを書き換えない。
6. Family / Navigation StageをDB/workspace persistent stateへ昇格させない。
7. Predictive等のdraft inputをStage切替で不必要に破棄しない。
8. Button enablementはclient local stateだけで決定せず、backend validation / operation availabilityを利用する。

Backend action availabilityは最低限`{allowed, reason_code?, message?}`を返し、action visibilityとaction allowedを別conceptとして扱う。
