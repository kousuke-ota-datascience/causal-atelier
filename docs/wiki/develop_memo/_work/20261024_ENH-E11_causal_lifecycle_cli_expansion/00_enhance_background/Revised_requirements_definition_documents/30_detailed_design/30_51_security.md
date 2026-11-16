# 30_51_security

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `04d83541e55ab0364500afb4b92ef55c10785a0c`.

---

## 21. Security / authorization

### 21.1 Project boundary

すべてのProject-scoped resource read/writeはactorのProject accessを検証する。

URLの`project_id`だけを信頼せず、resourceが同じProjectに所属することを検証する。

### 21.2 Navigation and authorization

route visibilityやdisabled controlをauthorization enforcementの代替にしない。

Project/Context/Data/Result/Analysis API commandはserver-side authorizationを実施する。

### 21.3 Cross-project prohibition

- Research Context restore
- Dataset Version restore
- Analysis View restore
- deep-linked resource resolve
- Result / Lineage traversal

でProject境界外resourceを採用しない。

---
