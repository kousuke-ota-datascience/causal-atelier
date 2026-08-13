# ENH-E5 要件・設計整合性およびトレーサビリティ確認

- 状態: `APPROVED`
- Remediation decision: D1=31 / D2=35 / D3=28
- D2 planning freeze: 11 packages / unresolved=0
- NFR-019 current verdict: `PARTIAL_MATCH / FAIL`

## 0. Review conclusion

Phase H時点のplanning layerは、D1/D2/D3およびPhase G freezeをPhase I canonical documentsへ収束させるためのtrace planとして整合した。

ただし`10/21/22/23/30`自体はまだPhase I未改訂であるため、NFR-019はPASSではない。

現在のauthority flow:

```text
Requirement / decision
    ↓
03 / 04 planning revision
    ↓
10
    ↓
21 / 22 / 23 / 30
    ↓
cross-document review
    ↓
NFR-019 re-audit
    ↓ PASS
06 / assigned Pxx
07
```

D3:

```text
10: DEFERRED / FUTURE
    ↓
90 technical debt ledger
```

## 1. Traceability rule

### 1.1 D1

D1はcurrent implementation correction。

- `10`: current Requirement本文へ訂正。
- `21/22/23/30`: source-aligned current contractへ訂正。
- `06/Pxx/07`: ENH-E5新実装targetとして扱わない。regression/compatibility protectionにのみ反映。

### 1.2 D2

D2はENH-E5 target。

- `10`: ACTIVE + ENH-E5。
- `21/22/23/30`: Phase G frozen contractを具体化。
- NFR-019 PASS後に`06/Pxx/07`へ完全転写。

### 1.3 D3

D3はENH-E5非実装。

- `10`: DEFERRED + FUTURE。
- `21/22/23/30`: current implementation factのみ記載し、future targetをcurrent E5 targetとして記載しない。
- `90`: defer理由 / impact / future design / revisit trigger。
- `06/Pxx/07`: ENH-E5 acceptanceへ含めない。

## 2. Family / Navigation traceability

| Requirement group | 21 Logical Data | 22 Basic Design | 23 API | 30 Detailed | Future 06/Pxx | Future 07 |
|---|---|---|---|---|---|---|
| FR-129〜139 Family/Stage navigation | navigation non-resource concept | Workspace/Presentation/Application | catalog + route | descriptor/aggregator/frontend binding | G00/G01/G05 | route/UI/architecture tests |
| FR-140〜143 Nav/Execution separation | no nav persistence | runtime boundary | no nav required input | dependency prohibition | G00/G05 | architecture/static |
| FR-144〜145 capability ownership | descriptor ownership | capability responsibility | aggregated read API | catalog providers | G00 | unit/API/static |
| FR-146〜148 Exploratory | existing resources + nav | exploratory capability/UI | exploration/handoff APIs | exploratory binding | G04/G05 | browser/API/scientific |
| FR-149〜152 Predictive | AnalysisSpecification etc. | predictive capability/UI | predictive APIs | predictive binding | G02/G05 | regression/browser/scientific |
| FR-153〜156 Causal | GraphVersion/Result etc. | causal capability/UI | causal APIs | causal binding | G03/G05 | regression/browser/scientific |
| FR-157〜162 compatibility/state | no nav persistence | compatibility boundary | canonical/legacy route | normalization/rendering | G01/G05 | deep-link/regression |

## 3. D2 package traceability

Phase GのAffected Documentsを維持する。

| Package | 10 | 21 | 22 | 23 | 30 | 06/Pxx | 07 |
|---|---:|---:|---:|---:|---:|---:|---:|
| PF-D2-01 Typed Filter | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ |
| PF-D2-02 Exploratory Handoff | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PF-D2-03 Subgroup Evaluation | ✓ | — | ✓ | ✓ | ✓ | ✓ | ✓ |
| PF-D2-04 Comparability/Reuse | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PF-D2-05 Idempotency/Artifact | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PF-D2-06 Authorization/Sensitive | ✓ | — | ✓ | ✓ | ✓ | ✓ | ✓ |
| PF-D2-07 Lineage Completion | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PF-D2-08 Reproducibility | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PF-D2-09 Frontend Navigation/A11y | ✓ | — | ✓ | ✓ | ✓ | ✓ | ✓ |
| PF-D2-10 Test Architecture | — | — | ✓ | — | ✓ | ✓ | ✓ |
| PF-D2-11 Documentation/Nav Freeze | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

`—`はそのdocumentに独立normative deltaを要求しないことを意味し、他documentのcontractを無視してよいことを意味しない。

## 4. D1 correction traceability

D1 31 Decision Item:

```text
FR-002
FR-090
FR-092
NFR-013
FR-110a
FR-114a
FR-127a
FR-128a
NFR-020a
D10-004
D10-005a
D22-001
D22-002
FR-007
FR-011
FR-025a
FR-026a
FR-048
FR-068
FR-087a
FR-120a
FR-124a
NFR-001a
NFR-006a
NFR-008a
NFR-009a
NFR-010a
NFR-011a
D22-003a
D22-013a
D30-018a
```

Consistency rule:

- source factをENH-E5 targetと誤認しない。
- current sourceにないfield/API/Port/moduleを補完しない。
- D1修正をcurrent canonical snapshotへ反映し、Change Logへ由来を残す。

## 5. D2 target traceability

D2 35 Decision Item:

```text
FR-015
D21-005
FR-020
FR-032
FR-067
AR-016
FR-108
FR-114b
AR-017
D10-005b
FR-008
FR-034
FR-051
FR-054
FR-072
FR-082
FR-086a
FR-087b
FR-095
FR-107
FR-109
FR-111
FR-121
FR-123a
FR-124b
NFR-001b
NFR-002
NFR-006b
NFR-008b
NFR-012
AR-004
AR-020
D22-013b
D30-018b
NFR-019
```

全件がPhase G freeze packageへ割当済みである。Phase Iでcontract値を変更しない。

## 6. D3 future traceability

D3 28 Decision Item:

```text
FR-021
FR-028
FR-062
FR-110b
FR-118
FR-122
FR-126
FR-127b
FR-128b
NFR-004
NFR-017
NFR-020b
D10-005c
D10-006a
D10-006b
FR-025b
FR-026b
FR-086b
FR-120b
FR-123b
NFR-007
NFR-008c
NFR-009b
NFR-010b
NFR-011b
D22-003b
D22-013c
D30-018c
```

Trace rule:

- Requirement D3 → `10` + `90`
- Design D3 → current E5 targetから除外 + `90`
- D3 test surfaces → `D22-013c / D30-018c`としてE5 acceptanceから除外

## 7. Key consistency checks

### 7.1 Family identity

- `AnalysisSpecification.analysis_family`を維持。
- duplicate family discriminatorなし。

### 7.2 Navigation vs Runtime

- Navigation StageはExecution Stageではない。
- Navigation StageをDB/AnalysisSpecification/Executionへpersistしない。
- Navigation catalogはruntime plan authorityではない。
- scientific CLI/libraryはNavigation Stage independent。

### 7.3 Navigation exact contract

- endpoint: `GET /api/v1/navigation/analysis`
- schema: `analysis-navigation/1`
- canonical route: `/projects/{project_id}/analysis/{family_slug}/{stage_slug}`
- default: exploratory/profile, causal/setup, predictive/setup

これらはopen decisionではない。

### 7.4 Predictive preservation

- existing settings 100% preservation。
- existing field削除/rename/default semantics変更なし。
- LightGBM等のfuture engine追加なし。

### 7.5 Reproducibility migration

`StageAttempt.effective_random_seed`はENH-E5 migration対象。

従来の`DB migration: NONE`記述を残さない。

### 7.6 Authorization

current role taxonomyはOWNER/EDITOR/VIEWER。

E5でProject-scoped authorization coverageを完成させるがsystem-level Operator roleはD3。

### 7.7 Sensitive output

prediction/local explanation rowはpotentially sensitive。

configurable sensitive-column metadata/policyはD3。

### 7.8 Idempotency

「全create API」をheader対象にしない。

duplicate durable side effect riskで対象Commandを決定する。

### 7.9 Lineage

structural relationはcanonical identity/read modelで投影し、semantic relationだけgeneric LineageEdgeへ保存する。

### 7.10 D3 isolation

D3を10から消さず、06/Pxx/07のE5 acceptanceへ混ぜない。

## 8. NFR-019 documentation gate

Current:

`PARTIAL_MATCH / FAIL`

Phase I後に次を確認する。

- `DOC-019-01〜DOC-019-08` all PASS。
- `10/21/22/23/30`だけでcurrent + E5 targetが理解可能。
- G00/G01/Architecture Review/preflightへnormative specificationを委譲していない。
- exact route/schema/error/persistence decisionがcanonical docs内に存在。
- cross-document contradictionがない。

all PASSまで`06/Pxx/07`をfinal freezeしない。

## 9. Open approval items

Phase H planning decisionとしてのopen approval itemは **0件**。

ただし次は未完了作業でありapproval issueではない。

- Phase I canonical document revision
- cross-document consistency audit
- Phase J NFR-019 re-audit
- Phase K 06/Pxx/07 convergence

## 10. Review verdict

**PHASE_H TRACEABILITY PLAN: PASS**

意味:

- planning layer内でD1/D2/D3・Phase G freezeのtrace方針は一貫した。
- canonical document self-containmentは未達であり、NFR-019はまだFAIL。
