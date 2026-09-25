# ENH-E9 Residual Scope Matrix

- Status: `INITIAL_CLASSIFICATION / MUST_REVERIFY_AT_E9_BASELINE`
- Historical inventory authority: observation only, not implementation backlog
- Reverification baseline: `UNSET` until E8 G03 formal PASS

| Historical observation | Initial disposition | E9 Gate candidate | Baseline evidence |
|---|---|---|---|
| Saved Analysis Viewに`[表示]`がない | `RESIDUAL_CANDIDATE` | G01 | pending |
| Active Research Context tooltipがない | `RESIDUAL_CANDIDATE` | G01 | pending |
| SetupでDiscovery Graphを要求 | `RESOLVED / E8` | OUT | pending confirmation |
| Setup Stage自体の存在意義 | `ARCHITECTURE_QUESTION / OUT` | OUT | n/a for E9 |
| Discovery operation領域にtitleがない | `RESIDUAL_CANDIDATE` | G02 | pending |
| Discovery Objective tooltipがない | `RESIDUAL_CANDIDATE` | G02 | pending |
| Discovery Rationale tooltipがない | `RESIDUAL_CANDIDATE` | G02 | pending |
| Discovery submit後feedbackがない | `RESOLVED` | OUT | pending confirmation |
| Graph Candidates overflow | `RESIDUAL_CANDIDATE / runtime verify` | G02 | pending |
| Graph Candidate一括選択/解除 | `RESIDUAL_CANDIDATE` | G02 | pending |
| Graph Comparison current selection highlight | `RESIDUAL_CANDIDATE` | G02 | pending |
| Graph Comparison説明にalgorithm/parameter不足 | `RESIDUAL_CANDIDATE` | G02 | pending |
| Graph採用結果がmodal外notice | `RESIDUAL_CANDIDATE` | G02 | pending |
| Graph Mermaid export | `RESIDUAL_CANDIDATE` | G02 | pending |
| Population tooltip | `RESIDUAL_CANDIDATE` | G03 | pending |
| Comparator tooltip | `RESIDUAL_CANDIDATE` | G03 | pending |
| Treatment schema-backed selector | `RESIDUAL_CANDIDATE` | G03 | pending |
| Outcome手入力 | `RESOLVED` | protected regression | pending confirmation |
| Estimation横方向layout | `RESOLVED / E8` | OUT | pending confirmation |

## Classification rule

E8 G03 PASS SHA固定後、各rowについてcurrent frontend/source/runtime/test evidenceを記録し、最終的に次のいずれかへ確定する。

- `RESOLVED`
- `RESIDUAL`
- `OUT`
- `ARCHITECTURE_QUESTION`

`RESIDUAL_CANDIDATE`をそのままimplementation scopeへ昇格させてはならない。
