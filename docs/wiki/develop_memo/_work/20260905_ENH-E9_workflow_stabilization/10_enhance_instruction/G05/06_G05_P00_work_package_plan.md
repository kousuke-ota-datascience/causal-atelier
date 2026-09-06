# G05 P00 Work Package Plan

- Status: `FROZEN`
- Gate authority: G05 06/07
- Execution role: `PLANNING_ONLY / NON_EXECUTABLE`

G05はP01のみを実行Packageとする。

| Package | Scope | Dependency | Completion boundary | Execution contract |
|---|---|---|---|---|
| P01 | integrated regression preparation, critical journey fixture/orchestration wiring, protected regression self-check, candidate finalization input | G01–G04 PASS | non-browser regression/self-check + checkpoint | `06_G05_P01_integrated_regression_acceptance.md` |

P01 focused verificationではBrowser E2Eを実行しない。Browser E2EはIndependent Verificationで、すべてのnon-browser blocking verificationを完了・評価した後の最後のverification itemとしてのみ実行する。

P01 completion is not Gate PASS. P01後にCandidate Assemblyを行い、G05 07に対するFixed Trial Candidateを作る。
