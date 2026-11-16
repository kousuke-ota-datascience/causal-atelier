# 22_08_validation_architecture

**Status:** `BD01_E11_BASIC_DESIGN_REVISED / OWNER_POLICY_APPROVED / INDEPENDENT_REVIEW_PENDING`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `87196f2f03a7f3367724bc05fb254d1a4d98109e`.

---

## 11. Validation Architecture

### 11.1 Generic Validation

Validation責務は、現行実装の`PlanValidator`が直接行う検証と、それ以外のapplication/domain validationを分離する。

#### 11.1.1 PlanValidatorが行う検証

`PlanValidator`は現在、次を検証する。

1. `plan_schema_version == execution-plan/1`。
2. `project_id`と`analysis_specification_id`が空でない。
3. `stage_key`が一意で、Planに少なくとも1 Stageが存在する。
4. enabled Stageの`StageType`にRunnerが登録済みである。
5. `resource_policy.timeout_seconds`が指定される場合、整数かつ1..86400以内である。
6. dependencyのsource/target Stageが存在する。
7. enabled Stageがdisabled Stageへ依存しない。
8. dependencyが参照するsource output / target input名が各contractに存在する。
9. source output schemaとtarget input schemaが一致する。
10. 同じtarget Stage inputへ複数upstream bindingを作らない。
11. topological sortが成立し、cycleがない。

`StageType.namespace/name/version`のsyntax validationは`StageType`生成時のdomain invariantであり、PlanValidatorの独立stepとして重複実装しない。

#### 11.1.2 PlanValidator外のvalidation

次は別のdomain/application boundaryで扱う。

- Project / Resource boundary・ownership
- Analysis Specification schema/lifecycle validation
- Family固有scientific validation
- supported endpointにおけるidempotency
- Dataset/Artifact size等、個別use caseのresource policy
- Navigation catalogのFamily/Stage ID、slug、order、default Stage、renderer binding整合性

Navigation catalog validationをruntime Plan dependency validationへ混入しない。

#### 11.1.3 AnalysisView typed filter validation

AnalysisView create/update/validate/fixは同じDataset logical-type compatibility validatorを利用する。

| Logical Type | Operator |
| --- | --- |
| BOOLEAN | `EQ, NE, IN, NOT_IN, IS_NULL, NOT_NULL` |
| INTEGER / REAL / DATETIME | `EQ, NE, LT, LTE, GT, GTE, IN, NOT_IN, IS_NULL, NOT_NULL` |
| TEXT | `EQ, NE, IN, NOT_IN, IS_NULL, NOT_NULL` |
| OTHER | `IS_NULL, NOT_NULL` |

`IS_NULL/NOT_NULL`はvalueなし、`IN/NOT_IN`はnon-empty list。DATETIME valueはISO-8601、REALはfinite numeric、INTEGERはbooleanを許容しない。`time_cutoff`はDATETIME + `LT/LTE`。logical type unknownをsuccess扱いしない。Mismatch codeは`FILTER_TYPE_MISMATCH`。

### 11.2 Exploratory Validation

- column typeとchart encoding
- aggregation compatibility
- empty population
- sampling disclosure
- exploratory findingをcausal claimへ変換しない

### 11.3 Causal Validation

- Graph semantics
- Causal Question completeness
- identification strategy
- adjustment set
- inferred type
- eligibility
- estimator compatibility
- post-discovery warning

### 11.4 Predictive Validation

- target existence / type
- feature availability
- target / future / group leakage
- split overlap
- preprocessing fit boundary
- metric / task compatibility
- test isolation
- existing setting/spec parity

### 11.5 Navigation Validation

- supported Familyのみ。
- Stage ID / slugはFamily内一意。
- default Stageはcatalog内に存在する。
- Family / Stage orderingはdeterministic。
- renderer binding欠落を検出する。
- Navigation descriptorにruntime input/output、status、retry semanticsを持たせない。



### 11.6. Local Causalの科学的状態・推論のValidation

1. Technical execution outcome, identification state, point availability, uncertainty availability, scientific acceptance are **orthogonal axes**。Science不適格をI/O errorやゼロ値で置き換えない。
2. Weak-IVのAnderson–Rubin反転Confidence Setは`bounded`／`unbounded`／`disconnected`／`all real`を区別。承認済み正常なB0/B1のAR反転で`EMPTY`を通常形として出さない。Finite intervalへ丸めない。
3. CATE/DRIVはMethod・backend version・inference implementation・final model・nuisance・fold/seed/Bootstrapにより区間推論の妥当性が異なる。Backend標準出力を無条件に科学的受入しない。
4. Pointwise CIをsimultaneous confidence bandと呼ばない。推論無しならnull+typed reasonを保持。Exploratory point-onlyをConfirmatoryとして提供しない。
5. 研究者のoverrideは科学的な未識別を自動で打消さない。再識別・新GraphVersion・代替識別根拠が必要な場合はその手続き・provenanceを残す。

- 必須入力の`schema/version`、Path、Graph/Design/Estimand、データidentity、Method/Backend capabilityを識別・推定前に検査する。
- 非識別・要Review・Estimator不適格を数値推定成功へ自動昇格しない。
- Science negative、technical execution failure、inference unsupported、manifest publish failureを別状態として扱う。
- Confidence Set topology・CI availability・Method適格性を結果保存前後に検証する。

## 98. RD-04：要件由来の基本設計制約

**Status:** `RD04_DESIGN_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。要件文の抽象化・設計移管で失われてはならない元の実現方式・責務境界を保持する。旧Requirement IDとStatusを維持する。コード検証やArchitecture GateのPASSを意味しない。

### 98.1. FR-015（SPLIT）

- 既存要件の設計情報を含む原文：AnalysisViewのsource Dataset logical type × operator × value compatibilityをdomain/application validationで検証し、type mismatchを`FILTER_TYPE_MISMATCH`として返す
- RDに残る能力／Legacy Trace：データ型と演算子・値が適合しない分析条件は拒否され、理由を確認できる
- Original Requirement：`FR-015`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.2. FR-085（SPLIT）

- 既存要件の設計情報を含む原文：未登録Runner、cycle、missing output、schema mismatchをPlan受付時に拒否する
- RDに残る能力／Legacy Trace：計画の依存関係や必要な入力が不整合なら実行前に拒否する
- Original Requirement：`FR-085`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.3. FR-089（MOVE_BD）

- 既存要件の設計情報を含む原文：Generic validationとFamily-specific validationを分離して実行する
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】FR-085の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-089`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.4. AR-009（MOVE_BD）

- 既存要件の設計情報を含む原文：外部libraryのdtype objectまたはmodel objectをJSON正本へ保存しない
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】対応する既存上位要件に係る既存設計制約。具体的な実装契約は下位設計へ移し、元ID・Status・科学的制約の追跡を維持する
- Original Requirement：`AR-009`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../96_rd04_nfr_ar_application_review.md)
