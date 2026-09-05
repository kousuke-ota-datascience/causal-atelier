# ENH-E9 Design Revision

- Status: `DRAFT_NOT_FROZEN`
- Authority: current `21/22/23/30` requirement/design snapshot + E8 protected contract

## 1. Design intent

E9はE8で確立したInformation Architecture、Stage responsibility、navigation/runtime separation、Result/Execution lineageを維持し、residual usabilityとdiagnostics backend conformanceのみを修正する。

## 2. Invariants

- `Navigation Stage != Execution Stage`。
- Project ManagementとAnalysis Workspaceのownershipを混在させない。
- Analysis View lifecycleはProject Management / Dataが所有し、Analysis Workspaceはexisting viewをcontextとして利用する。
- Discovery Result / DRAFT Graph Version / FIXED Graph Versionのmutability semanticsを維持する。
- FIXED Graphを直接更新しない。
- Identification / Estimation / Effects / DiagnosticsのStage responsibilityを維持する。
- UI/IA都合だけでnew API / persistence / runtime lifecycleを追加しない。
- Frontend presentationはpersisted Resultをauthorityとし、新しいcausal estimate/diagnosticを推測生成しない。

## 3. Outcome ownership

E9 protected design:

```text
Discovery designated Outcome
  -> GraphVersion designated_outcome_node
  -> Identification read-only Outcome
  -> Estimation
```

TreatmentをDataset-schema-backed selectorへ改善してもOutcome ownershipは変更しない。

## 4. Diagnostics contract direction

G04 authoring時に少なくとも次をstable structured contractとしてfreezeする候補とする。

```text
diagnostics.weighting.effective_sample_size

diagnostics.weighting.weights
  count
  min
  mean
  median | p50
  p95
  p99
  max
  extreme_weight_count
  extreme_weight_rule
  scale_or_normalization_semantics

balance.before
balance.after
```

これは**draft design direction**であり、current baseline/sourceとscientific semanticsを確認する前にfield名をimplementation authorityとして使用してはならない。

Estimator applicability:

- difference-in-means: weighting diagnosticsを機械的に要求しない
- OLS: IPW相当weight diagnosticsを機械的に要求しない
- IPW: actual analysis weightsに基づくweight/ESS/balance diagnosticsを検討
- AIPW: propensity-derived weighting componentのdiagnosticを提示し得るが、AIPW全体の単一final weightとして表現しない

## 5. UI residual design direction

- G01: existing resourceのvisibility/meaningを改善し、resource ownershipを変更しない。
- G02: Discovery/Graph comparison/adoptionのinteraction clarityを改善し、scientific execution/adoption semanticsを変更しない。
- G03: Population/Comparatorの意味説明とTreatment candidate selectionを改善し、causal question semanticsを変更しない。
- G05: critical journey proofに限定し、Browser E2Eをdetailed scientific correctnessの一次証明にしない。
