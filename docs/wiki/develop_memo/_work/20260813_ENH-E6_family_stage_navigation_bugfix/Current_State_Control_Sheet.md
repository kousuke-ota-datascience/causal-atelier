# ENH-E6 Current State Control Sheet

- Enhancement: `ENH-E6`
- Baseline branch: `bugfix/ariadne_mvp_e6`
- Baseline SHA: `5a5ced9bd6a0e62027c4058eb66ec487719bde23`
- State: `INITIALIZED`
- Rule: final PASS 済み evidence のみ verified current state へ promotion する。

## Verified inherited state

| ID | State | Authority / evidence | ENH-E6 handling |
|---|---|---|---|
| E6-CS-001 | ENH-E5 G01 は historical Gate Decision 上 PASS 済みであり、その evidence chain は immutable | ENH-E5 G01 frozen 06/07 + final Gate Decision | 遡及修正しない |
| E6-CS-002 | ENH-E5 closeout ledger に `ANOM-E5-001` が `OPEN_FOLLOW_UP / FUTURE / BUGFIX_ENHANCEMENT` として記録されている | `20260811_ENH-E5_family_stage_navigation/00_enhance_background/90_technical_debt_and_future_enhancements.md` | ENH-E6 source anomaly として継承 |
| E6-CS-003 | baseline source には Family tab / Stage sidebar の DOM と renderer code が存在する | `frontend/index.html`, `frontend/app.js` | 「未実装」ではなく integration anomaly として扱う |
| E6-CS-004 | baseline source の canonical route restore path は `renderAnalysisNavigation()` を呼ぶ | `frontend/app.js` | regression protected fact |
| E6-CS-005 | baseline source の normal `activateWorkspace()` path は Navigation Context / history を変更し得るが `renderAnalysisNavigation()` を呼ばない | `frontend/app.js` | E6 direct defect target |
| E6-CS-006 | baseline source は `ANALYSIS_WORKSPACES.causal = discovery` の Family 単位 mapping を持つ | `frontend/app.js` | E6 design defect target |

> 注: `E6-CS-005/006` は source inspection により確認した implementation fact。fresh runtime/browser reproduction は ENH-E6 ではまだ verified ではない。

## Not yet verified / prohibited promotion

- fresh environment の observable UI reproduction
- Browser DOM / computed visibility / selected state
- user click 後の URL / history / active presentation の同期
- ENH-E6 implementation candidate
- ENH-E6 tests

これらを Gate PASS 前に verified current state へ記載してはならない。
