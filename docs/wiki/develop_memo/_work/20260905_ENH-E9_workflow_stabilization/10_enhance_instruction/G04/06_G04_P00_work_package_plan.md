# G04 P00 Work Package Plan

- Status: `FROZEN`
- Gate authority: G04 06/07
- Execution role: `PLANNING_ONLY / NON_EXECUTABLE`

| Package | Scope | Dependency | Completion boundary | Execution contract |
|---|---|---|---|---|
| P01 | estimator weight/component exposure, applicability enum/contract, frozen extreme-rule boundary | G03 PASS | scientific/unit contract tests | `06_G04_P01_contract_applicability_estimator_exposure.md` |
| P02 | IPW actual-weight stats + treated/control ESS structured persistence | P01 | IPW ATE/ATT independent numeric tests + integration | `06_G04_P02_ipw_weight_stats_ess_persistence.md` |
| P03 | `balance.before/after`, weighted balance wiring, AIPW PROPENSITY_COMPONENT / non-weighted NOT_APPLICABLE | P02 | estimator applicability + balance tests | `06_G04_P03_balance_applicability.md` |
| P04 | frontend structured consumption, legacy compatibility/regression wiring | P03 | frontend integration + Gate-wide regression | `06_G04_P04_frontend_structured_consumption.md` |

P00はCoding Agent実行対象ではない。Package focused verificationではBrowser E2Eを実行しない。G04ではBrowser E2Eをblocking numeric/scientific proofに使用せず、cross-layer Browser E2EはG05の最後に実行する。

Frozen extreme-weight rule:

```text
extreme_rule = "weight > 10.0"
extreme_count = count(actual arm weight > 10.0)
```

`weight == 10.0`はextremeに含めず、propensity clipping countを流用しない。

PxxはGate semantic claim/ACを変更できない。各Pxxはassigned Coding Agent向けself-contained normative contractであり、Gate 06/07/P00/other Pxxをsemantic補完目的で読ませない。全Pxx後にFixed Trial Candidateをassembleする。
