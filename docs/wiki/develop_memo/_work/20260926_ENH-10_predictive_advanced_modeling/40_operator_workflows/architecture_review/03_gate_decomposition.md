# ENH-E10 Gate Decomposition — Post Architecture Review

> **Document class:** Architecture Review / Gate Decomposition  
> **Status:** `REVIEW_COMPLETE / PENDING_HUMAN_APPROVAL`  
> **Enhancement:** `ENH-E10`

## 1. Decomposition principle

GateはdownstreamがPASS済みsemantic contractへ依存できる境界で分ける。implementation sizeだけの分割はWork Packageで行う。

Architecture Reviewの結果、G01/G02/G03のsemantic boundariesは維持する。各Gateはexecution-size/failure-localizationのためWork Packageを使用する。

## 2. Gates

| Gate | Objective | Entry prerequisites | Contract established on PASS | Transition Debt | Regression dependencies |
|---|---|---|---|---|---|
| G01 | Predictive Model Backend Contract | ENH-E9 accepted baseline | model capability、LightGBM binary/regression、optional dependency、fitted-model/2 load/predict、provenance | NONE | existing logistic/linear、TRAIN-only preprocessing、TEST isolation |
| G02 | Predictive Explanation Backend Contract | G01 PASS | method capability、SHAP_TREE、LIME_TABULAR、coefficient compatibility、global/local/provenance | NONE | all G01 contracts + coefficient explanation |
| G03 | Predictive Product Integration Contract | G01 PASS + G02 PASS | capability-driven Train/Explainability/Model Management + 2 blocking Browser journeys | NONE | all G01/G02 contracts + ENH-E8 stage responsibility + ENH-E9 unrelated flows |

## 3. Work Package decomposition

### G01 — WORK_PACKAGE

```text
P01 Model Capability / Optional Dependency
  -> P02 LightGBM Model Adapters
  -> P03 Artifact / Load / Provenance Integration
  -> Candidate Assembly
```

Reason: dependency contract, provider execution, durable artifact integration have ordered implementation dependencies and distinct failure modes.

### G02 — WORK_PACKAGE

```text
P01 Explanation Capability / Canonical Contract
  -> P02 SHAP Backend
  -> P03 LIME Backend / Explanation Integration
  -> Candidate Assembly
```

Reason: common compatibility/canonical contract must exist before method adapters; SHAP and LIME have independent scientific/runtime failure modes.

### G03 — WORK_PACKAGE

```text
P01 Capabilities / Train Integration
  -> P02 Explainability / Model Management Integration
  -> P03 Browser E2E / Product Regression
  -> Candidate Assembly
```

Reason: Browser journey is only meaningful after API/frontend integration is complete.

## 4. Ordering rationale

```text
G01 PASS
  ↓
G02 PASS
  ↓
G03 PASS
```

G02 consumes model identity, loader/predict behavior and optional dependency semantics established by G01.

G03 consumes both model and explanation capability contracts and MUST NOT redefine their scientific semantics.

## 5. Final convergence condition

ENH-E10 completes only when:

- G01 canonical 999 = PASS
- G02 canonical 999 = PASS
- G03 canonical 999 = PASS
- no unapproved Transition Debt
- advanced dependencies remain optional
- existing linear predictive behavior remains supported
- Predictive Explanation remains explicitly non-causal

## 6. Forbidden parallelization

- G02 coding before G01 PASS
- G03 coding before G01 + G02 PASS
- G03 Browser contract used to redefine G01/G02 numeric/scientific acceptance
- P02 before same-Gate P01 PACKAGE_COMPLETE
- P03 before same-Gate P02 PACKAGE_COMPLETE
- package completion treated as Gate PASS

## 7. Gate vs Work Package boundary check

All three Gate splits create downstream-relyable semantic contracts; no Gate exists solely due to implementation size.

The three-Package decomposition inside each Gate is execution decomposition only and does not create new acceptance boundaries.

## 8. Freeze readiness

Architecture decisions required by 06/07/Pxx are technically resolved by `02_target_architecture_decision_record.md`.

Remaining pre-freeze work:

1. Human architecture approval
2. reflect decisions into 04/05 and all G01-G03 06/07/Pxx
3. apply approved requirement delta to canonical requirement/design documents as required
4. freeze 06/07/Pxx in one consistent batch
