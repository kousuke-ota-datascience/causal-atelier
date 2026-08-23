# ENH-E8 Contract Amendment Log

freeze / retrospective-freeze後のGate contract amendmentをappend-onlyで記録する。

2026-08-20のPredictive feature-selector追加は、ENH-E8のcontractがまだ `DRAFT_FOR_REVIEW` の段階で取り込まれたため、pre-freezeのscope/design revisionである。`09` Gate Contract Amendmentではなく、Trialも増加させない。

| Amendment | Gate | Status | 理由 | Effective contracts |
|---|---|---|---|---|
| `G03-A01` | `G03` | `APPROVED/APPLIED` | G03初回retrospective reconstruction後の追加bugfixにより、Estimation handler bootstrap中のinteraction race、canonical frontend asset delivery、およびhistorical regression testのstalenessがblocking verification conditionとして判明した。original G03 claimは維持し、AC/implementation constraintsを強化した。 | `10_enhance_instruction/G03/06_Ariadne_ENH-E8_G03_implementation_instruction.md`, `10_enhance_instruction/G03/07_Ariadne_ENH-E8_G03_test_instruction.md` |

## G03-A01 traceability

- Amendment record: `../10_enhance_instruction/G03/09_ENH-E8_G03_A01_Gate_Contract_Amendment.md`
- Re-baseline status: `RETROSPECTIVE_FROZEN / A01_APPLIED`
- Trial impact: none. G03はformal Independent Verification前であり、Trial01 Fixed Verification Candidateは未確定。
- Semantic impact: Gate claimの緩和・変更ではなく、runtime bootstrap / static asset delivery / verification coverageのcompletion conditionを追加。
- Protected Gate impact: G01/G02 semantics、API、DB/persistence、backend causal estimation semanticsは変更しない。
- Git traceability: A01 record作成 commit `1c4d583de258161a36ff9f2da24170a34f258e15`。re-baselined primary contractsは後続commitsで適用。

scope revision記録は `../90_change_history/20260820_predictive_feature_selector_scope_revision.md` を参照する。

freeze後に06/07のsemantic claim / Acceptance Criteriaを変更する必要が生じた場合は`09_*_Gate_Contract_Amendment.md`を使用する。`08` remediationで06/07の欠陥をsilentに書き換えてはならない。
