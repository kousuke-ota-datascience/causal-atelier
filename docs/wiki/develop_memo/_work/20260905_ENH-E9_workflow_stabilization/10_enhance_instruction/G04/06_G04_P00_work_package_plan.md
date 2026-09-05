# G04 P00 Work Package Plan

- Status: `FROZEN`
- Gate authority: G04 06/07

| Package | Scope | Dependency | Completion boundary |
|---|---|---|---|
| P01 | estimator weight/component exposure, applicability enum/contract, fixture design | G03 PASS | scientific/unit contract tests |
| P02 | IPW actual-weight stats + treated/control ESS structured persistence | P01 | IPW ATE/ATT independent numeric tests + integration |
| P03 | `balance.before/after`, weighted balance wiring, AIPW PROPENSITY_COMPONENT / non-weighted NOT_APPLICABLE | P02 | estimator applicability + balance tests |
| P04 | frontend structured consumption, legacy compatibility/regression wiring | P03 | frontend integration + Gate-wide regression |

PxxはGate semantic claim/ACを変更できない。Extreme-weight ruleはP01でscientific/configuration authorityとtest boundaryを同時に固定し、06の「rule+count pair」要件を満たす。全Pxx後にFixed Trial Candidateをassembleする。
