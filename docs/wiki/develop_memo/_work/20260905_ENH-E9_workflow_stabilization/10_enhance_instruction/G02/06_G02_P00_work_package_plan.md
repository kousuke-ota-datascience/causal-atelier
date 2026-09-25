# G02 P00 Work Package Plan

- Status: `FROZEN`
- Gate authority: G02 06/07
- Execution role: `PLANNING_ONLY / NON_EXECUTABLE`

P00 は Work Package plan であり、Coding Agent に assigned Package として渡してはならない。Human / Orchestrator は `PACKAGE_ID=P00` で normal Work Package Coding Agent を起動しない。

| Package | Scope | Dependency | Completion boundary | Execution contract |
|---|---|---|---|---|
| P01 | Discovery operation title, Objective/Rationale help, Graph Candidates overflow | G01 PASS | focused tests + checkpoint | `06_G02_P01_discovery_copy_help_overflow.md` |
| P02 | Select All/Clear, current comparison highlight, algorithm/parameter summary | P01 | interaction/API regression + checkpoint | `06_G02_P02_selection_comparison_clarity.md` |
| P03 | modal-local adoption feedback, Mermaid source export | P02 | interaction/export regression + checkpoint | `06_G02_P03_adoption_feedback_export.md` |

Browser E2EはP01〜P03のfocused verificationでは実行しない。必要なBrowser E2EはGate 07 Independent Verificationの最後のverification itemとしてのみ実行する。

Pxx completion is not Gate PASS. P03後にCandidate Assemblyを行い、G02 07に対するFixed Trial Candidateを作る。Gate semantic claimまたはAC変更が必要ならPxx内で変更せず09 amendmentへ戻す。
