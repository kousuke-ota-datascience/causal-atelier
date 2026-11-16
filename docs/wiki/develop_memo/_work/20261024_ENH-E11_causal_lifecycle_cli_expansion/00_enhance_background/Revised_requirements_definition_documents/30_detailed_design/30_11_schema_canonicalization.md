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


## 98. RD-04：詳細設計へ引き継ぐ要求起源の具体制約

**Status:** `RD04_DETAILED_CONSTRAINT_TRACE / OWNER_CONTENT_REVIEW_PENDING`。RD-04で抽象化した原文から、モジュール・Class・Method・I/O・失敗処理へ落とすべき実現制約を保持する。実装されていると確認した記録ではない。クラスレベル仕様は[共通テンプレート](30_01_class_design_template.md)に従い別途DD設計確認する。

### 98.1. NFR-003（SPLIT）

- 移管する原条項の具体内容：Canonical JSONとhash生成はfield順やprocessに依存しない
- 上位Requirementと整合する要求核：同一内容から環境に依存しない同一性識別値を生成できる
- `NFR-003`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../96_rd04_nfr_ar_application_review.md)
