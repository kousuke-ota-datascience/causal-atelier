# 21_20_value_domain_identifiers

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`; original ID, level and state retained.  
**Source blob:** `72903b9ad48b5b7edabaa7bb1c2cace42aa46ce7`.

---

## 4. 非Entityのデータモデル

本章は独立identity/lifecycleを持たないvalue object、projection、query model、navigation metadata、embedded schemaを定義する。これらをUI上に存在するという理由だけでpersistent Entityへ昇格させない。

### 4.1 AnalysisFamily

`AnalysisFamily`はEntityではなくdomain discriminatorであり、許容値は次の3つとする。

- `EXPLORATORY`
- `CAUSAL`
- `PREDICTIVE`

この値は`AnalysisSpecification.analysis_family`、`ExecutionPlan.analysis_family`、`Execution.analysis_family`で共通利用する。同義のduplicate enum/fieldを増設しない。

### 4.4 Runtime Stage value model

ExecutionPlan内のruntime Stageは次のvalue objectで表現する。

```json
{
  "stage_key": "train",
  "stage_type": {
    "namespace": "predictive",
    "name": "train",
    "version": "1"
  },
  "input_contract": {},
  "output_contract": {},
  "parameters": {},
  "resource_policy": {},
  "enabled": true
}
```

- `StageType`: namespace / name / versionでruntime Stage種別を識別
- `StageDefinition`: input/output/parameter/resource policy
- `StageBinding`: Stage間dependency / input-output binding

これらはNavigation Stageと同一型にしない。
