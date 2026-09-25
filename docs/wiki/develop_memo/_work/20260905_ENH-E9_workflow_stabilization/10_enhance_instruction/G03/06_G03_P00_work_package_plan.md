# G03 P00 Work Package Plan

- Status: `FROZEN`
- Gate authority: G03 06/07
- Execution role: `PLANNING_ONLY / NON_EXECUTABLE`

P00はWork Package planでありCoding Agentへassigned Packageとして渡してはならない。G03はP01のみを実行Packageとする。

| Package | Scope | Dependency | Completion boundary | Execution contract |
|---|---|---|---|---|
| P01 | Population/Comparator help, Dataset-backed Treatment selector, stale Treatment clearing, FIXED Graph Outcome read-only inheritance regression | G02 PASS | focused frontend/integration/regression tests + checkpoint | `06_G03_P01_identification_input_ergonomics.md` |

Package focused verificationではBrowser E2Eを実行しない。G03ではBrowser E2E自体を必須とせず、cross-layer browser journeyはG05の最終verification itemへ委譲する。

P01 completion is not Gate PASS. P01後にCandidate Assemblyを行い、G03 07に対するFixed Trial Candidateを作る。
