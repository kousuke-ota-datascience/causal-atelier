# 30_52_failure_handling

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `04d83541e55ab0364500afb4b92ef55c10785a0c`.

---

## 22. Failure / error handling

### 22.1 Route failure

invalid routeはexplicit navigation errorとして扱い、無関係なdefaultへsilent redirectしない。

### 22.2 Context failure

selection restore失敗はunselected stateへ落とし、架空defaultを作らない。

### 22.3 API failure

loading/error stateとlast known current routeを分離する。API failureだけを理由にrouteを別Family/Stageへ書き換えない。

### 22.4 Runtime failure

runtime failureはExecution/StageExecution/Result scientific status contractで表現し、Navigation Stage自体をruntime statusとして更新しない。

### 22.5 Feature selector failure

Predictive feature selectorでDataset Version/schemaを取得できない場合はselectorをunavailable/errorとして表示し、架空column optionやstale selectionをscientific inputとして確定しない。

Dataset Version変更によりselected featureが無効になった場合は、無効featureをsilent保持しない。clearまたはvalid intersectionへのreconcileを行う場合、利用者に変更を示す。

---

**当該構成要素の詳細設計制約（関連Requirement）**

- **`NFR-011a`**：current request/execution/stage correlation identifiersをlogへ出力する
