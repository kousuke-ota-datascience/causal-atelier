# 30_11_schema_canonicalization

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `04d83541e55ab0364500afb4b92ef55c10785a0c`.

---

## 6. Schema registry / canonicalization

### 6.1 SchemaRegistry

Generic scientific/product payload schemaはversion stringをkeyとしてvalidatorを登録する。

```python
class SchemaRegistry:
    def register(self, schema_version, validator): ...
    def validate(self, schema_version, payload): ...
    def canonicalize(self, schema_version, payload) -> bytes: ...
    def hash(self, schema_version, payload) -> str: ...
```

Invariant:

- empty / duplicate schema version registrationを拒否する。
- unknown versionはunsupported version errorとする。
- payloadはMappingを要求する。
- canonicalization前にschema validationする。

Navigation metadata `analysis-navigation/1`はpresentation/application metadata contractであり、scientific generic SchemaRegistryへ登録しない。

### 6.2 Canonical JSON

canonicalizationは少なくとも次を満たす。

- dataclassはfield mappingへ変換する。
- Enumは`.value`へ変換する。
- UUID / datetimeはstable stringへ変換する。
- non-finite floatを拒否する。
- mapping keyはstringのみ。
- mapping key orderに依存しないcanonical serializationを行う。
- semantic payloadに含まれないbrowser navigation stateをhash inputへ混入しない。

### 6.3 Reproducibility metadata

Execution/Resultのreproducibility metadataには、実際に利用したlibrary version、input snapshot identifier、analysis specification/version、effective random seed等を必要に応じて記録する。

browser Navigation Stageはscientific reproducibility inputではない。

---
