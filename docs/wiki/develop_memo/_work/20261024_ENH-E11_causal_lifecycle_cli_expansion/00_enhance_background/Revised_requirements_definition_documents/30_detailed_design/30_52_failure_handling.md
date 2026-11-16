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


## 98. RD-04：詳細設計へ引き継ぐ要求起源の具体制約

**Status:** `RD04_DETAILED_CONSTRAINT_TRACE / OWNER_CONTENT_REVIEW_PENDING`。RD-04で抽象化した原文から、モジュール・Class・Method・I/O・失敗処理へ落とすべき実現制約を保持する。実装されていると確認した記録ではない。クラスレベル仕様は[共通テンプレート](30_01_class_design_template.md)に従い別途DD設計確認する。

### 98.1. NFR-011a（SPLIT）

- 移管する原条項の具体内容：current request/execution/stage correlation identifiersをlogへ出力する
- 上位Requirementと整合する要求核：Request・実行・処理単位をまたいで障害を追跡できる
- `NFR-011a`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../96_rd04_nfr_ar_application_review.md)
