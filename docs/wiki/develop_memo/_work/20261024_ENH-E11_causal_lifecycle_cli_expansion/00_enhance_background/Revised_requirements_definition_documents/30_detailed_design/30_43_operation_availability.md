# 30_43_operation_availability


---

## 19. Operation Availability

### 19.1 Purpose

Operation Availabilityは現在のProject/resource/route contextにおいて、どのcommand/controlを実行可能かをread-only projectionする。

Frontend route parser、Navigation catalog、Stage visibilityはscientific truthを所有しない。

### 19.2 Authority

```text
availability projection
  ≠ command authorization/validation
```

actual commandがdenyした場合、そのdenyをauthoritativeとする。

### 19.3 Representative reason codes

```text
PROJECT_ACCESS_DENIED
UNSUPPORTED_OPERATION
RESOURCE_REQUIRED
ROUTE_REQUIRED
RESOURCE_IMMUTABLE
SPEC_NOT_FIXED
GRAPH_NOT_FIXED
IDENTIFICATION_REQUIRED
INPUT_GRAPH_REQUIRED
INPUT_RESULT_REQUIRED
EXECUTION_STATE_NOT_RUNNABLE
RESULT_NOT_EXPORTABLE
DOMAIN_PREREQUISITE_NOT_SATISFIED
```

request-level error例:

```text
INVALID_OPERATION_AVAILABILITY_QUERY
UNSUPPORTED_RESOURCE_TYPE
ENTITY_NOT_FOUND
PROJECT_ACCESS_DENIED
INVALID_NAVIGATION_ROUTE
ROUTE_RESOURCE_FAMILY_MISMATCH
```

closed vocabularyをimplementation都合で無秩序に拡張しない。

### 19.4 Data Quality availability

Data Quality Stageは専用operationを持たないため、Profile result availabilityをprojectionする。

```text
PROFILE result present → read-only READY
PROFILE result absent  → unavailable(NO_PROFILE_RESULT) + Profile link
```

このreasonはUI-local presentation contractとして扱う場合でも、backend runtime operation/stateを作成しない。

---
