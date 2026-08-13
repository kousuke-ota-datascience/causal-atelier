# ENH-E6 要件・設計整合性およびトレーサビリティ確認

> **Document class:** Planning / Decision Artifact  
> **Self-containment:** MUST for own subject.

- Review status: `PASS_FOR_FROZEN_G01_CONTRACT`
- Canonical requirement/design modification: `NONE`

## 1. Traceability matrix

| Requirement / Invariant | Design realization | Gate | Acceptance Criterion |
|---|---|---|---|
| E6-FR-001 observable shell | coordinator-owned shell lifecycle | G01 | AC-E6-G01-001 |
| E6-FR-002 Family default | Family intent -> catalog default -> coordinator | G01 | AC-E6-G01-002 |
| E6-FR-003 Stage click | Stage intent -> same Family context -> coordinator | G01 | AC-E6-G01-003 |
| E6-FR-004 route/history restore | parse/serialize + historyMode=none on restore/popstate | G01 | AC-E6-G01-004 |
| E6-FR-005 single authority | one context-application coordinator | G01 | AC-E6-G01-005 |
| E6-FR-006 stage-aware presentation | `(family, stage)` binding | G01 | AC-E6-G01-006 |
| E6-FR-007 legacy compatibility boundary | legacy shortcut -> canonical context resolver | G01 | AC-E6-G01-007 |
| E6-FR-008 exact Causal legacy targets | discovery/identification mappings | G01 | AC-E6-G01-008 |
| E6-FR-009 fail closed | validation/binding errors explicit | G01 | AC-E6-G01-009 |
| E6-NFR-001 real-browser proof | Playwright actual Family/Stage click | G01 | AC-E6-G01-010 |
| E6-NFR-002 protected regression | affected E5 route/catalog/history/availability suite | G01 | AC-E6-G01-011 |
| Navigation Stage != Execution Stage | no runtime persistence/mapping | G01 | AC-005/009/011 audit |
| backend catalog authority | no duplicated full catalog frontend ownership | G01 | AC-001/002/009/011 |

## 2. Consistency checks

- Requirement vs design: `PASS`
- Design vs Gate decomposition: `PASS`
- Gate boundaries mutually coherent: `PASS` — one semantic Gate, execution split by Work Package
- Transition Debt exits defined: `PASS`
- Canonical requirement/design immutability: `PASS` — no revision planned
- Coding/Test authority separation: `PASS after template-compliance correction` — Pxx no longer depends on/read-instructs G01 07

## 3. Unresolved issues

No semantic issue blocks G01 Trial01 execution after Human review/preflight/template-compliance correction.

Operational values that must be runtime-derived, not prefilled:

- P01 actual `START_SHA` after Human commits this compliance update
- package checkpoint/evidence SHA
- Fixed Trial Candidate SHA
- browser/test result identities

These are not contract ambiguities.

## 4. Conclusion

ENH-E6 realization requirements, target design, one-Gate decomposition, package DAG, and frozen Acceptance Criteria are coherent. `Causal Inference -> causal/identification` is an approved compatibility entry decision, not a domain equivalence. Coding Agent receives only assigned self-contained Pxx; Independent Test receives 07. Proceed to P01 only after Human applies this template-compliance artifact update to the branch.
