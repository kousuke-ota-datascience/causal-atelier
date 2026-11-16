# 30_31_causal_setup_discovery

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `04d83541e55ab0364500afb4b92ef55c10785a0c`.

---

## 14. Causal Capability / Stage Contents

### 14.1 Runtime discriminator / mapping

Causal family spec schema versionは`causal-analysis-spec/2`。runtime operationは次のdiscriminatorを使用する。

```text
DISCOVERY
IDENTIFICATION
ESTIMATION
REFUTATION
SENSITIVITY
```

Representative mapping:

| ExecutionOperation | stage_key | StageType |
| --- | --- | --- |
| `DISCOVERY` | `discovery` | `causal.discovery.v1` |
| `IDENTIFICATION` | `identification` | `causal.identification.v1` |
| `ESTIMATION` | `estimation` | `causal.estimation.v2` |
| `REFUTATION` | `refutation` | `causal.refutation.v1` |
| `SENSITIVITY` | `sensitivity` | `causal.sensitivity.v1` |

runtime input matrix:

| ExecutionOperation | input_graph_version_id | input_result_id |
| --- | ---: | ---: |
| DISCOVERY | なし | なし |
| IDENTIFICATION | 必須 | なし |
| ESTIMATION | 必須 | 必須 |
| REFUTATION | 必須 | 必須 |
| SENSITIVITY | 必須 | 必須 |

`Effects` / `Diagnostics`等のNavigation Stageはsaved Result readで成立し得るため、同名ExecutionOperation/StageTypeを追加しない。

### 14.2 Setup

primary responsibility:

- causal question / design preparation
- direct graph registration where supported
- Research Context / Dataset / Analysis View確認

Identification/Estimation/Sensitivityのmain operationをSetupへ複製しない。

### 14.3 Discovery

primary responsibility:

- discovery specification
- PC / GES等のcurrent discovery operation
- graph candidate
- candidate comparison/edit/adopt/fix
- confounder / mediator / collider / temporal ordering / domain assumption検討

Discoveryのnavigation placementはruntime graph/discovery semanticsを変更しない。
