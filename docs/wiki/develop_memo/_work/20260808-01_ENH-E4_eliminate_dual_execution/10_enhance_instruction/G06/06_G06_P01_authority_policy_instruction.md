# ENH-E4 E4-G06 P01 Authority Policy Instruction

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Branch: `refactor/ariadne_mvp_e4`
- Gate: `E4-G06`
- Gate Name: Lineage authority consolidation
- Trial: `01`
- Work Package: `P01`
- Package Name: Lineage authority policy / semantic allowlist / generic-only admission guard
- Document Type: Coding Agent Work Package Instruction
- File:
  `10_enhance_instruction/G06/06_G06_P01_authority_policy_instruction.md`
- Governing Control Document:
  `10_enhance_instruction/G06/06_G06_P00_work_package_plan.md`
- Fixed G06 Architecture Baseline:
  `aae491519472f87bfbda88069eb1e65a858a9fcc`
- Previous Gate Fixed Implementation/Test Candidate:
  `ad3e3e124ee47f9cbaa2470b25263b7289795262`
- Product Migration Head at G06 Entry:
  `20260809_product_0010`
- Transition Debt:
  `E4-TD-004 OPEN -> G06`

---

# 1. Instruction Status

本書は E4-G06 Trial01 の Coding Agent execution package `P01` を実行するための指示書である。

本書は単独で解釈してはならない。

必ず先に以下を読むこと。

```text
10_enhance_instruction/G06/
06_G06_P00_work_package_plan.md
```

P00はG06全体のgoverning control documentであり、本書より上位のGate-local execution ruleである。

本書とP00が矛盾する場合:

```text
P01 implementationを開始しない
    ->
矛盾箇所を明示する
    ->
PACKAGE_BLOCKED
```

とする。

上位architecture contractを推測で変更してはならない。

---

# 2. P01 Purpose

P01の目的は、Product lineageについて、

```text
source semantic type
+
relation semantic
+
target semantic type
    ->
lineage authority class
```

を一元判定できるdomain/application policyを確立し、

```text
GENERIC_ONLY
```

と判定されたsemantic relationだけがgeneric persisted lineage authorityへ進める状態を作ることである。

特に、current manual lineage writer:

```text
ProductClosureService.create_lineage_link()
```

が、

```text
relation nameがrecognizedである
    ->
generic persist可能
```

という状態から、

```text
source / relation / target semantic tuple
    ->
authority classification
    ->
GENERIC_ONLY only
        -> generic persist可能
```

という状態へ移ることをP01の中心成果とする。

---

# 3. P01 Is Not the Whole G06

P01はE4-G06全体を完了させるpackageではない。

P01終了時:

```text
E4-G06:
NOT_COMPLETE

Trial:
01

TD-004:
OPEN
```

でなければならない。

P01では以下を完了させない。

```text
P02:
structural workflow writer cutover

P03:
all generic-only production writer convergence

P04:
typed lineage read reconstruction

P05:
closure / export projection convergence

P06:
retry / rerun / revise lineage audit
negative authority audit

P07:
Gate-wide completion / fixed candidate / READY_FOR_TEST
```

---

# 4. P01 Entry Preconditions

P01 Coding Agentは実装開始前に以下を確認する。

## 4.1 Branch / HEAD

```bash
git branch --show-current
git rev-parse HEAD
git status --short
git log --oneline -15
```

Expected branch:

```text
refactor/ariadne_mvp_e4
```

## 4.2 G06 architecture baseline ancestry

```bash
git merge-base --is-ancestor \
  aae491519472f87bfbda88069eb1e65a858a9fcc \
  HEAD
echo $?
```

Expected:

```text
0
```

## 4.3 P00 presence

```bash
test -f \
  docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/10_enhance_instruction/G06/06_G06_P00_work_package_plan.md
echo $?
```

Expected:

```text
0
```

## 4.4 P01 entry SHA

P01の実際のentry SHAは、

```text
P00がrepositoryへ配置・commitされた後の
P01開始時HEAD
```

である。

本書作成時点ではP00 commit SHAを固定しない。

Coding Agentは開始時に:

```bash
git rev-parse HEAD
```

で得たSHAを、

```text
P01 Entry SHA
```

としてPackage Checkpoint Reportへ記録する。

重要:

```text
Fixed G06 Architecture Baseline
    = aae4915...

P01 Entry SHA
    = P00 commitを含む実際のpackage開始HEAD
```

であり、同一とは限らない。

report-only/docs-only commitを無視して古いSHAへcheckoutしてはならない。

---

# 5. Dirty Working Tree Rule

`git status --short` が空でない場合:

1. 変更fileを列挙する。
2. P01と関係するproduction/test変更か確認する。
3. user/operatorが作った変更をsilentに破棄しない。
4. untracked evidence/reportだけか、production conflictかを区別する。

以下の場合は開始しない。

```text
P01 scopeと競合する
未説明production source変更が存在する
```

その場合:

```text
PACKAGE_BLOCKED
```

として報告する。

---

# 6. Source of Truth / Precedence

P01でsemantic判断を行う場合、以下のprecedenceを使用する。

```text
1. Passed Gate-local contract + final Gate Decision
2. ENH-E4 approved ADR / INV / REQ / CON
3. G06 P00 + formal G06 Gate decomposition
4. approved lineage allowlist correction
5. verified current source at P01 Entry SHA
6. existing tests as regression evidence
```

既存testがtarget contractと衝突する場合、

```text
existing test
    != architecture authority
```

である。

ただし、testを変更する前に何のcontractを検証しているかを確認する。

---

# 7. Mandatory Architecture References

最低限以下を確認する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
10_enhance_instruction/G06/
06_G06_P00_work_package_plan.md
```

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/architecture_review/
06_target_architecture_decision_record_result.md
```

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/architecture_review/
07_gate_decomposition_result.md
```

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/architecture_review/
08c_lineage_allowlist_contract_correction_result.md
```

必要に応じてformal snapshot:

```text
00_enhance_background/Revised_requirements_definition_documents/
21_論理データ設計.md

00_enhance_background/Revised_requirements_definition_documents/
30_詳細設計.md
```

を確認する。

---

# 8. Verified Baseline Facts

Fixed G06 architecture baseline
`aae491519472f87bfbda88069eb1e65a858a9fcc`
では、少なくとも以下が成立している。

## 8.1 Domain lineage model

```text
src/ariadne/product/domain/lineage.py
```

にはbaseline時点で:

```text
ResourceRef
LineageEdge
```

が存在する。

しかし、

```text
LineageAuthority
authority classifier
generic admission policy
```

は存在しない。

## 8.2 Current relation vocabulary

```text
src/ariadne/product/application/product_closure_service.py
```

にはflat relation vocabulary:

```text
USED_INPUT
GENERATED
DERIVED_FROM
REVISED_FROM
SUPPORTED_BY
MOTIVATED
SELECTED
REJECTED
```

が存在する。

このsetは現在:

```text
relation name recognized?
```

を判定している。

## 8.3 Current manual generic writer

baselineの:

```text
ProductClosureService.create_lineage_link()
```

は概ね以下の順序で処理する。

```text
relation name validation
    ->
source/target reference validation
    ->
same-project validation
    ->
LineageEdgeOrm creation
    ->
commit
```

つまりbaselineでは、

```text
source semantic type
+
relation semantic
+
target semantic type
```

に基づくauthority classificationがgeneric persistenceの前提になっていない。

## 8.4 Current direct generic writer outside create_lineage_link

baselineではworkspace annotation decision pathが:

```text
SELECTED / REJECTED
```

を直接 `LineageEdgeOrm` へwriteする箇所を持つ。

これはP03でgeneric-only writer全体をconvergeする際のinventory対象である。

P01ではこのwriterの全面refactorへ越境しない。

ただしP01のcentral policyを将来P03から再利用できる形にする。

---

# 9. G06 Authority Model

P01はP00で固定された以下のmodelを変更しない。

```text
Lineage Authority
│
├── TYPED_STRUCTURAL
│
├── GENERIC_ONLY
│
├── PROJECTION_ONLY
│
└── OUT_OF_SCOPE
```

Unknown / unapproved semantic tupleはformal authority classではない。

Unknownを便利なfallback classとしてpersist可能にしてはならない。

Expected:

```text
unknown / unapproved
    ->
generic write rejected
```

---

# 10. TYPED_STRUCTURAL Contract

以下はapproved typed structural semantic relationsである。

## 10.1 Execution owns Result

```text
Source:
Execution

Semantic:
owns / generates

Target:
Result

Representative relation vocabulary:
GENERATED

Authority:
TYPED_STRUCTURAL

Generic authoritative edge:
FORBIDDEN
```

## 10.2 Result owns Artifact

```text
Source:
Result

Semantic:
owns / generates

Target:
Artifact

Representative relation vocabulary:
GENERATED

Authority:
TYPED_STRUCTURAL

Generic authoritative edge:
FORBIDDEN
```

## 10.3 DatasetVersion is Execution input

```text
Source:
DatasetVersion

Relation:
USED_INPUT

Target:
Execution

Authority:
TYPED_STRUCTURAL

Generic authoritative edge:
FORBIDDEN
```

## 10.4 AnalysisView is Execution input

```text
Source:
AnalysisView

Relation:
USED_INPUT

Target:
Execution

Authority:
TYPED_STRUCTURAL

Generic authoritative edge:
FORBIDDEN
```

## 10.5 Result is Execution input

```text
Source:
Result

Relation:
USED_INPUT

Target:
Execution

Authority:
TYPED_STRUCTURAL

Generic authoritative edge:
FORBIDDEN
```

## 10.6 Result produces GraphVersion

```text
Source:
Result

Target:
GraphVersion

Authority:
TYPED_STRUCTURAL

Generic authoritative edge:
FORBIDDEN
```

relation vocabularyはcurrent formal designとverified code semanticsを確認してclassifierへ固定すること。

名前を推測で追加しない。

## 10.7 Artifact derives DatasetVersion

```text
Source:
Artifact

Target:
DatasetVersion

Authority:
TYPED_STRUCTURAL

Generic authoritative edge:
FORBIDDEN
```

relation vocabularyはformal contractを確認して固定する。

## 10.8 Execution base/revision relation

```text
Source:
Execution

Target:
Execution

Representative relation vocabulary:
DERIVED_FROM
REVISED_FROM
or approved typed mutation relation

Authority:
TYPED_STRUCTURAL

Generic authoritative edge:
FORBIDDEN
```

---

# 11. GENERIC_ONLY Contract

以下はapproved generic-only semantic relationsである。

## 11.1 Artifact stage/process derivation

```text
Source:
Artifact

Relation:
DERIVED_FROM

Target:
Artifact

Authority:
GENERIC_ONLY

Generic authoritative edge:
ALLOWED
```

## 11.2 Result summarizes Result

```text
Source:
Result

Relation:
SUMMARIZES

Target:
Result

Authority:
GENERIC_ONLY

Generic authoritative edge:
ALLOWED
```

## 11.3 Result summarizes Artifact

approved formal relation contractが存在する場合:

```text
Source:
Result

Relation:
SUMMARIZES

Target:
Artifact

Authority:
GENERIC_ONLY

Generic authoritative edge:
ALLOWED
```

formal snapshot / allowlist correctionとの整合を確認すること。

## 11.4 Documents relation

typed structural equivalentを持たない場合のみ:

```text
Source:
Result or Artifact

Relation:
DOCUMENTS

Target:
approved Product resource

Authority:
GENERIC_ONLY
```

以下のようなtargetがformal contractで承認対象になっている。

```text
AnalysisSpecification
DatasetVersion
AnalysisView
related Product resource
```

ただし、

```text
DOCUMENTSというrelation名
```

だけを理由にuniversal allowしない。

source/target semantic tupleがapprovedである必要がある。

## 11.5 Evidence relation

typed structural equivalentを持たない場合のみ:

```text
SUPPORTED_BY
EVIDENCE_FOR
```

等のapproved evidence relationをGENERIC_ONLYとして扱う。

relation nameだけでuniversal allowしない。

## 11.6 MOTIVATED

formal contractでapprovedされたmanual/semantic relation:

```text
Result
    ->
AnalysisSpecification
```

等をGENERIC_ONLYとして扱う。

current API regressionで利用されている既存approved manual semantic linkとの互換性を確認する。

## 11.7 SELECTED / REJECTED

approved user-authored semantic relationはGENERIC_ONLY。

ただしP01でannotation direct writer全体をrefactorしない。

central classifierがP03から利用可能であることを優先する。

---

# 12. PROJECTION_ONLY Contract

以下はauthority persistence対象ではない。

```text
closure
traversal
synthetic lineage
export lineage representation
```

P01でclosure/export implementationを変更しない。

P01 classifierへprojection-only概念を表現可能にしてもよいが、

```text
manual generic writerから
PROJECTION_ONLY relationをpersist可能にする
```

ことは禁止する。

---

# 13. OUT_OF_SCOPE Contract

以下はP01 Product target authorityへ取り込まない。

```text
legacy ArtifactLineage
legacy-only family lineage authority
```

legacy retirementはG07 boundary。

P01を理由にlegacy source削除を行わない。

---

# 14. Critical Semantic Rule

以下を絶対条件とする。

```text
relation name
    !=
authority
```

例えば:

```text
Execution --DERIVED_FROM--> Execution
    = TYPED_STRUCTURAL
```

に対し、

```text
Artifact --DERIVED_FROM--> Artifact
    = GENERIC_ONLY
```

である。

したがって:

```python
if relation == "DERIVED_FROM":
    allow_generic = True
```

のような実装は禁止する。

同様に:

```python
GENERIC_RELATIONS = {
    "DERIVED_FROM",
    ...
}
```

だけでauthority admissionを決定してはならない。

---

# 15. P01 Required Design Outcome

P01ではcentral Product lineage authority policyを実装する。

第一候補:

```text
src/ariadne/product/domain/lineage.py
```

または同じProduct domain配下の小さなdedicated module。

重要なのはfile名ではなく、

```text
single semantic policy
```

である。

以下をserviceごとに複製しない。

---

# 16. Required Authority Type

最低限、以下相当を型として表現する。

```text
TYPED_STRUCTURAL
GENERIC_ONLY
PROJECTION_ONLY
OUT_OF_SCOPE
```

実装形式はcurrent code styleに合わせてよい。

候補:

```text
Enum
Literal
frozen dataclass + enum
```

ただし:

```text
raw string scattered across services
```

は避ける。

Unknown / unapproved tupleを上記classへ無理に分類しない。

---

# 17. Required Classifier

以下相当のsingle entry pointを実装する。

```text
classify_lineage_authority(
    source_type,
    relation_type,
    target_type,
)
```

または同等の明確なAPI。

入力:

```text
semantic resource type
relation type
semantic resource type
```

出力:

```text
approved LineageAuthority
```

または:

```text
unapproved / unsupported indication
```

を一意に返す。

classifierはDB accessを必要としないpure policyであることを推奨する。

---

# 18. Required Generic Admission Guard

以下相当を実装する。

```text
assert_generic_lineage_allowed(
    source_type,
    relation_type,
    target_type,
)
```

または同等のAPI。

Expected:

```text
GENERIC_ONLY
    -> pass

TYPED_STRUCTURAL
    -> reject

PROJECTION_ONLY
    -> reject

OUT_OF_SCOPE
    -> reject

unknown / unapproved
    -> reject
```

errorはexisting domain/application error taxonomyへ合わせる。

P01だけのために新しいHTTP error architectureを作らない。

---

# 19. Relation Vocabulary Reconciliation

current baseline relation vocabularyとformal approved relation vocabularyに差がある。

baseline current vocabulary:

```text
USED_INPUT
GENERATED
DERIVED_FROM
REVISED_FROM
SUPPORTED_BY
MOTIVATED
SELECTED
REJECTED
```

formal approved generic-only semanticsには追加で:

```text
EVIDENCE_FOR
DOCUMENTS
SUMMARIZES
```

が存在する。

P01ではこの差を無視してはならない。

対応方針:

```text
syntactic recognized vocabulary
    !=
generic authority allowlist
```

として分離する。

formal contractで必要なrelation nameがcurrent syntactic vocabularyに欠ける場合:

```text
recognized vocabularyへ追加してよい
```

ただしそのrelation nameを:

```text
all source/targetでgeneric allowed
```

にしてはならない。

---

# 20. Resource Type Vocabulary Rule

authority policyでは:

```text
Execution
Result
Artifact
DatasetVersion
AnalysisView
AnalysisSpecification
GraphVersion
...
```

等のsemantic Product resource typeを使用する。

ORM class名:

```text
FamilyResultOrm
FamilyArtifactOrm
```

をauthority semantic typeとして採用しない。

legacy/family storage representationとProduct semantic resource typeを混同しない。

P01で新しいresource type taxonomyを大規模設計しない。

---

# 21. create_lineage_link Integration

P01では:

```text
ProductClosureService.create_lineage_link()
```

をcentral admission policyへ接続する。

Current ordering:

```text
relation vocabulary validation
source/target parsing
self-edge validation
role/project checks
resource existence/project validation
persist
```

を大きく崩す必要はない。

ただしgeneric persist前に必ず:

```text
semantic authority admission
```

が実行されること。

Recommended logical order:

```text
parse source/relation/target
    ->
syntactic vocabulary validation
    ->
semantic authority classification/admission
    ->
self-edge validation
    ->
role validation
    ->
resource existence/project validation
    ->
LineageEdgeOrm persistence
```

またはsecurity/error behaviorを保つためにrole/resource validationを先に行ってもよい。

重要なのは:

```text
LineageEdgeOrm creation / flush / commit
```

より前にsemantic admissionが完了すること。

---

# 22. Structural Generic Write Rejection

以下のようなmanual requestをgeneric persistenceしてはならない。

```text
Execution
GENERATED
Result
```

```text
Result
GENERATED
Artifact
```

```text
DatasetVersion
USED_INPUT
Execution
```

```text
AnalysisView
USED_INPUT
Execution
```

```text
Result
USED_INPUT
Execution
```

```text
Execution
REVISED_FROM
Execution
```

Expected:

```text
validation rejection

LineageEdgeOrm:
corresponding row = 0
```

typed canonical stateを変更してはならない。

---

# 23. Generic-only Positive Admission

最低限、以下の明白なGENERIC_ONLY relationでpositive pathを証明する。

```text
Artifact
DERIVED_FROM
Artifact
```

および:

```text
Result
SUMMARIZES
Result
```

formal/current resource fixtureの都合で一方が実現困難な場合でも、pure policy testでは両方を固定する。

PostgreSQL/service positive testは少なくとも1つ実行する。

---

# 24. Unknown Combination Rejection

recognized relation nameであっても、approved semantic tupleでなければrejectする。

例はformal contractを侵害しない組み合わせをtest fixtureとして選ぶこと。

重要:

```text
recognized relation
+
unknown tuple
    != allowed generic edge
```

を証明する。

---

# 25. Same Relation / Different Authority Test

P01の最重要pure policy test。

必ず:

```text
DERIVED_FROM
```

について:

```text
Execution -> Execution
    = TYPED_STRUCTURAL
```

と:

```text
Artifact -> Artifact
    = GENERIC_ONLY
```

を同一test module内で証明する。

これがP01のarchitecture intentを最も直接的に検証する。

---

# 26. Existing Endpoint / Project Validation Preservation

P01はcurrent `create_lineage_link()` の以下を壊してはならない。

```text
source exists
target exists
source in requested project
target in requested project
cross-project rejected
self-edge rejected
write role required
duplicate/idempotent behavior preserved
```

P01のauthority policy追加を理由に:

```text
project boundary validation削除
resource existence validation削除
duplicate handling redesign
```

を行わない。

---

# 27. Duplicate Behavior

baseline `create_lineage_link()` はDB uniqueness conflict時にexisting rowを再取得するbehaviorを持つ。

P01ではこのsemanticsを原則変更しない。

authority consolidationとduplicate/idempotency redesignは別問題である。

P03または別approved packageで必要にならない限り変更しない。

---

# 28. Annotation Writer Boundary

baselineではannotation decision:

```text
SELECTED
REJECTED
```

がdirect `LineageEdgeOrm` writerを持つ。

P01では:

```text
create_annotation()
update_annotation()
```

等を全面的にauthority-policyへ切り替えることを必須にしない。

理由:

```text
P01:
policy foundation + manual admission proof

P03:
generic-only authority convergence across writers
```

というpackage boundaryを守るため。

ただしP01で実装するpolicyはP03がreuseできるpublic/internal Product APIとして設計する。

---

# 29. Workflow Writer Boundary

以下はP01で変更しない。

```text
Causal workflow structural lineage writers
Exploratory workflow structural lineage writers
Predictive workflow structural lineage writers
```

P02の責務である。

P01のtestを通すためにworkflow writerを先に削除してはならない。

---

# 30. Read Reconstruction Boundary

P01では以下を変更しない。

```text
project_lineage()
result_lineage()
Predictive list_lineage()
typed reconstruction
```

P04/P05の責務である。

P01のauthority classifierをread projectionへ無理に接続しない。

---

# 31. Closure / Export Boundary

P01では:

```text
closure source_class
export source_class
synthetic edge representation
```

を変更しない。

P05の責務である。

---

# 32. Mutation Boundary

P01では:

```text
retry
rerun
revise
```

のlineage behaviorを変更しない。

P06の責務である。

ただしExecution->Execution relationがTYPED_STRUCTURALであることはclassifierで表現する。

---

# 33. Database / Migration Boundary

P01では原則:

```text
Migration:
NONE
```

とする。

理由:

```text
central authority policy
+
application admission guard
```

はexisting `product_lineage_edge` schema変更なしで成立できると想定されるため。

DB migrationが必要と判断した場合:

1. なぜapplication/domain policyでは不十分か。
2. どのformal requirementがschema enforcementを要求するか。
3. P02/P03/P05へ送るべきではないか。

を確認する。

便利さだけでmigrationを追加しない。

必要性がcontract上不明なら:

```text
PACKAGE_BLOCKED
```

ではなく、まず:

```text
UNKNOWN / UNCONFIRMED
```

としてlocal alternativeを検討する。

---

# 34. Expected Production Change Area

Primary candidate:

```text
src/ariadne/product/domain/lineage.py
```

Expected:

```text
LineageAuthority type
semantic authority mapping/classifier
generic admission policy
```

Secondary candidate:

```text
src/ariadne/product/application/product_closure_service.py
```

Expected:

```text
create_lineage_link()
    -> central policy enforcement
```

必要に応じて:

```text
small dedicated Product lineage policy module
```

を追加してよい。

禁止:

```text
policy copy in multiple workflow services
```

---

# 35. Existing Code Style Rule

current repositoryのstyleに従う。

不要なframework導入をしない。

P01だけのために:

```text
new dependency
new DI framework
new registry framework
new plugin mechanism
```

を追加しない。

simple explicit data structureでcontractを表現できるならそれを優先する。

---

# 36. Policy Representation Guidance

relation matrixは明示的であること。

例:

```text
(source_type, relation_type, target_type)
    ->
LineageAuthority
```

のtable / mapping。

ただし一つのsemantic relationが複数target kindを持つ場合、可読性を損なう巨大if-chainは避ける。

以下を満たすこと。

```text
auditable
testable
closed by default
relation-name-onlyではない
```

---

# 37. Closed-by-default Rule

allowlistにないsemantic tupleはrejectする。

つまりpolicyは:

```text
default allow
```

ではなく:

```text
default deny
```

である。

禁止:

```python
return LineageAuthority.GENERIC_ONLY
```

をunknown fallbackにすること。

---

# 38. Evidence / Payload Rule

P01はgeneric edge `evidence_json` schemaを全面再設計しない。

既存payload:

```text
evidence
```

をpreserveする。

authority classifierがevidence内容によってauthorityを変える設計は原則禁止。

authorityは:

```text
source semantic type
relation semantic
target semantic type
```

で決定する。

evidenceはauthority classificationの代用品ではない。

---

# 39. Required New Tests

P01 focused testsを新規作成する。

推奨file:

```text
tests/product/
test_enh_e4_g06_p01_lineage_authority_policy.py
```

```text
tests/product/
test_enh_e4_g06_p01_authority_policy_postgres.py
```

既存test naming conventionにより微調整してよい。

ただしP01 testであることがfilenameから識別できること。

---

# 40. Pure Policy Test Matrix

最低限以下をtestする。

## Structural

```text
Execution + GENERATED + Result
    -> TYPED_STRUCTURAL
```

```text
Result + GENERATED + Artifact
    -> TYPED_STRUCTURAL
```

```text
DatasetVersion + USED_INPUT + Execution
    -> TYPED_STRUCTURAL
```

```text
AnalysisView + USED_INPUT + Execution
    -> TYPED_STRUCTURAL
```

```text
Result + USED_INPUT + Execution
    -> TYPED_STRUCTURAL
```

```text
Execution + REVISED_FROM + Execution
    -> TYPED_STRUCTURAL
```

formal contractで`DERIVED_FROM`もExecution mutation relationとして承認される場合:

```text
Execution + DERIVED_FROM + Execution
    -> TYPED_STRUCTURAL
```

## Generic-only

```text
Artifact + DERIVED_FROM + Artifact
    -> GENERIC_ONLY
```

```text
Result + SUMMARIZES + Result
    -> GENERIC_ONLY
```

```text
Result + DOCUMENTS + AnalysisSpecification
    -> GENERIC_ONLY
```

またはformal allowlist上のapproved DOCUMENTS tuple。

```text
Result + EVIDENCE_FOR + approved target
    -> GENERIC_ONLY
```

またはformal/current vocabularyでapproved evidence tuple。

```text
Result + MOTIVATED + AnalysisSpecification
    -> GENERIC_ONLY
```

```text
approved resource + SELECTED/REJECTED + approved semantic target
    -> GENERIC_ONLY
```

current annotation direction / formal contractと一致するexact tupleを使用する。

## Deny

```text
unknown relation
    -> rejected
```

```text
recognized relation + unapproved tuple
    -> rejected
```

---

# 41. Mandatory Relation-name Ambiguity Test

必須:

```text
DERIVED_FROM
```

のauthorityがrelation名だけで決まらないことをtestする。

Expected:

```text
Execution -> Execution
    TYPED_STRUCTURAL

Artifact -> Artifact
    GENERIC_ONLY
```

このtestが存在しない場合、P01 completeとしない。

---

# 42. PostgreSQL / Service Test — Structural Negative

real PostgreSQL上でmanual generic writerへstructural relationを渡す。

推奨例:

```text
Execution
GENERATED
Result
```

またはfixture作成が容易な別の明白なTYPED_STRUCTURAL tuple。

Expected:

```text
request/service call:
rejected

product_lineage_edge:
matching row count = 0

typed canonical relationship:
unchanged
```

DB row absenceを明示的にquery/assertする。

HTTP responseのみで合格としない。

---

# 43. PostgreSQL / Service Test — Generic Positive

real PostgreSQL上でGENERIC_ONLY relationを作成する。

推奨:

```text
Artifact
DERIVED_FROM
Artifact
```

Expected:

```text
accepted

product_lineage_edge:
exactly one matching authoritative row

evidence:
preserved
```

duplicate behaviorを同じtestで確認してもよいが、P01の主目的をぼかさない。

---

# 44. PostgreSQL / Service Test — Unknown Tuple Negative

real PostgreSQL上で:

```text
recognized relation name
+
unapproved source/target tuple
```

を送る。

Expected:

```text
rejected

product_lineage_edge:
matching row count = 0
```

これによりrelation-name-only allowlistが残っていないことを証明する。

---

# 45. Project Boundary Regression

P01はexisting project-boundary behaviorを保全する。

少なくとも以下existing regressionを確認する。

```text
tests/product/test_cross_analysis_lineage_e3.py::
test_explicit_lineage_link_rejects_cross_project_resources
```

Expected:

```text
cross-project explicit lineage:
rejected
```

existing error code/HTTP semanticsを不必要に変更しない。

---

# 46. Existing Manual Semantic Link Regression

baseline existing regression:

```text
tests/product/test_cross_analysis_lineage_e3.py::
test_project_lineage_combines_families_and_explicit_relations
```

はmanual:

```text
Result --MOTIVATED--> Execution
Result --MOTIVATED--> AnalysisSpecification
```

を使用している。

P01では、このexisting usageがapproved `user-authored/manual semantic link` contractに該当するかをformal allowlistと照合する。

該当する場合:

```text
regressionを維持する
```

該当しない場合:

```text
testを力任せに通すためallowlistを広げない
```

Facts / Interpretation / Required Decisionを明示する。

formal contractから一意に判断できない場合:

```text
PACKAGE_BLOCKED
```

を使用できる。

---

# 47. Standard Verification Commands

新規pure policy test:

```bash
uv run pytest -q \
  tests/product/test_enh_e4_g06_p01_lineage_authority_policy.py
```

real PostgreSQL:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g06_p01_authority_policy_postgres.py \
  -q
```

existing project-boundary regression:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_cross_analysis_lineage_e3.py::test_explicit_lineage_link_rejects_cross_project_resources \
  -q
```

existing manual semantic-link regression:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_cross_analysis_lineage_e3.py::test_project_lineage_combines_families_and_explicit_relations \
  -q
```

test file/function名を実装時に変更した場合は、actual exact commandをreportへ記録する。

---

# 48. Standard PostgreSQL Rule

real PostgreSQL acceptance evidenceは:

```text
scripts/test/run_product_postgres_tests.sh
```

を標準entry pointとして使用する。

以下をacceptance evidenceの主経路にしない。

```text
manual docker run
manual network/IP
manual DSN
manual psql bootstrap
manual Alembic
manual external pytest
```

runner evidenceには:

```text
exact command
exit code
passed
failed
skipped
evidence directory
tested SHA/state
```

を記録する。

---

# 49. Test Partition Rule

G05で確認されたstate contaminationを考慮し、focused PostgreSQL testとexisting regressionは必要に応じて別runner invocationで実行する。

```text
one giant pytest invocation
```

を成功条件にしない。

ただしcombined failureが発生した場合:

```text
isolated PASS
    ->
fixture defect確定
```

とはしない。

root causeを確認する。

再現不能の場合:

```text
NOT_REPRODUCED
ROOT_CAUSE_UNCONFIRMED
```

を使用する。

---

# 50. Required Negative Static Audit

P01終了時に、authority policyがmanual writerだけのlocal special-caseになっていないか確認する。

最低限:

```bash
rg -n \
  "LINEAGE_RELATIONS|LineageEdgeOrm|create_lineage_link|DERIVED_FROM|GENERATED|USED_INPUT|REVISED_FROM|SUMMARIZES|DOCUMENTS|EVIDENCE_FOR|MOTIVATED|SELECTED|REJECTED" \
  src/ariadne/product
```

目的:

```text
current writer inventoryを確認
P02/P03へ残るwriterを把握
P01がscope越境していないことを確認
```

このauditで見つかったwriterをP01で全部修正しない。

P02/P03 residual workとしてreportへ列挙する。

---

# 51. P01 Explicitly Forbidden Changes

P01では以下を行わない。

```text
Causal structural writer cutover
Exploratory structural writer cutover
Predictive structural writer cutover

all annotation lineage writer convergence
all generic-only writer convergence

project_lineage typed reconstruction
result_lineage typed reconstruction
Predictive list_lineage convergence

closure source_class implementation
export source_class implementation
synthetic projection redesign

retry lineage cleanup
rerun lineage cleanup
revise lineage cleanup

legacy ArtifactLineage deletion
legacy Family source deletion
CLI retirement
migration chain cleanup
bootstrap cleanup

Execution authority redesign
StageExecution authority redesign
Result authority redesign
Artifact ownership redesign

Control Sheet promotion
TD-004 CLOSED declaration
E4-G06 PASS declaration
READY_FOR_TEST declaration
```

---

# 52. No Test-fitting

以下は禁止。

```text
特定test IDだけallow
fixture resource IDだけallow
MOTIVATEDをtestのためuniversal allow
DERIVED_FROMをuniversal generic allow
structural tupleだけspecial-caseでDB write後に削除
validation errorを隠すためHTTP layerで握り潰す
```

architecture semanticsを先に固定する。

---

# 53. Error Semantics

P01 authority rejectionはexisting application/domain error taxonomyに合わせる。

候補:

```text
InvalidSchema
```

等。

新しいerror typeが明らかに必要で、既存taxonomyではsemanticを正しく表せない場合のみ追加を検討する。

その場合でも:

```text
new external API error contract
```

まで拡張しない。

HTTP error responseの形は既存web layer contractを維持する。

---

# 54. Security / Information Disclosure

validation orderingを変更する際、unauthorized userへresource existenceを過剰に漏らさないこと。

current role/project validation semanticsを確認する。

P01のauthority classifier自体はpure semantic policyであるため、DB existenceをclassifierへ組み込まない。

---

# 55. P01 Package Completion Conditions

以下を全て満たした場合のみ:

```text
G06-P01_COMPLETE
```

とする。

```text
1. central lineage authority type exists

2. central semantic classifier exists

3. classifier is source/relation/target tuple based

4. relation-name-only authority admission is eliminated

5. formal structural relations are classified TYPED_STRUCTURAL

6. formal generic-only relations are classified GENERIC_ONLY

7. unknown/unapproved tuple is denied by default

8. current syntactic relation vocabulary and formal vocabulary are reconciled

9. create_lineage_link uses central generic admission policy

10. structural manual generic write is rejected

11. rejected structural write creates zero matching LineageEdgeOrm rows

12. generic-only positive write persists

13. project-boundary behavior remains valid

14. mandatory same-relation/different-authority test exists and passes

15. focused pure tests PASS

16. focused real PostgreSQL tests PASS

17. relevant existing regressions PASS or are formally classified

18. no migration unless explicitly justified

19. implementation checkpoint commit created

20. P01 Package Checkpoint Report created
```

---

# 56. Implementation Checkpoint Commit

production + test implementationがcompleteし、focused verificationがPASSしたらcheckpoint commitを作成する。

禁止:

```bash
git add .
```

明示的にfileをstageする。

例:

```bash
git add \
  src/ariadne/product/domain/lineage.py \
  src/ariadne/product/application/product_closure_service.py \
  tests/product/test_enh_e4_g06_p01_lineage_authority_policy.py \
  tests/product/test_enh_e4_g06_p01_authority_policy_postgres.py
```

actual changed filesに合わせること。

commit message例:

```text
E4-G06 P01 establish lineage authority policy
```

commit後:

```bash
git rev-parse HEAD
```

を取得する。

このSHAを:

```text
P01 Implementation Checkpoint SHA
```

とする。

---

# 57. Package Checkpoint Report

P01完了時に以下を作成する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G06/Trial01/packages/
E4-G06_01_P01_implementation_checkpoint_report.md
```

P00で定義したPackage Checkpoint Report contractに従う。

---

# 58. Required Package Report Fields

最低限:

```text
Gate:
E4-G06

Trial:
01

Package:
P01

Package Status:
COMPLETE / BLOCKED

G06 Architecture Baseline:
aae491519472f87bfbda88069eb1e65a858a9fcc

P01 Entry SHA:
<actual>

P01 Implementation Checkpoint SHA:
<actual>

Product Migration Head:
<actual>

Changed Production Files:
<exact paths>

Changed Test Files:
<exact paths>

Migration:
NONE / exact migration

Authority Policy:
<summary>

Formal Relation Vocabulary Reconciliation:
<summary>

Structural Generic Negative Write:
PASS / FAIL / NOT_RUN

Generic-only Positive Write:
PASS / FAIL / NOT_RUN

Unknown Tuple Negative Write:
PASS / FAIL / NOT_RUN

Project Boundary Regression:
PASS / FAIL / NOT_RUN

Existing Manual Semantic Link Regression:
PASS / FAIL / BLOCKED / NOT_RUN

Tests:
<exact commands/results>

PostgreSQL Evidence:
<exact commands/results/evidence directories>

Residual P02 Writers:
<inventory>

Residual P03 Generic-only Writers:
<inventory>

Facts:
...

Interpretation:
...

Unknown / Unconfirmed:
...

TD-004:
OPEN

Gate Status:
E4-G06 NOT_COMPLETE

Next Package:
P02

git status --short:
<exact output>
```

---

# 59. Report Commit

Package Checkpoint Report作成後、reportのみのcommitを作成してよい。

ただし:

```text
report commit SHA
    !=
P01 Implementation Checkpoint SHA
```

とする。

P02がproduction baselineとして参照すべきSHAは:

```text
P01 Implementation Checkpoint SHA
```

である。

docs commitがHEADに存在する場合、P02はactual HEADから開始してよいが、tested implementation identityをreport commitへ置き換えてはならない。

---

# 60. P01 Final Agent Output

Coding Agentは終了時に以下をexactに報告する。

```text
Package status:
G06-P01_COMPLETE
or
G06-P01_BLOCKED

Gate status:
E4-G06 NOT_COMPLETE

Trial:
01

G06 architecture baseline:
aae491519472f87bfbda88069eb1e65a858a9fcc

P01 entry SHA:
<sha>

P01 implementation checkpoint SHA:
<sha>

Product migration head:
<value>

Changed production files:
<exact paths>

Changed/new test files:
<exact paths>

Migration:
NONE
or exact migration

Pure policy tests:
<exact command>
exit code
passed
failed
skipped

PostgreSQL tests:
<exact command>
exit code
passed
failed
skipped
evidence directory

Existing regressions:
<exact commands/results>

Authority classifier:
<summary>

Structural generic negative write:
PASS / FAIL / NOT_RUN

Generic-only positive write:
PASS / FAIL / NOT_RUN

Unknown tuple rejection:
PASS / FAIL / NOT_RUN

Residual writer inventory for P02/P03:
<summary>

TD-004:
OPEN

Package report:
<exact path>

git status --short:
<exact output>
```

---

# 61. P01 Must Not Declare

P01終了時に以下を宣言してはならない。

```text
E4-G06 PASS

READY_FOR_TEST

TD-004 CLOSED

all lineage authority converged

closure/export converged

structural duplicate writers globally removed
```

これらはP02-P07およびIndependent Test Agentの責務である。

---

# 62. Stop / Escalation Conditions

以下の場合は推測で実装しない。

## 62.1 Formal allowlist contradiction

同じ:

```text
source type
relation
target type
```

について上位formal contractが:

```text
TYPED_STRUCTURAL
```

と:

```text
GENERIC_ONLY
```

の両方を要求する場合。

## 62.2 Existing approved API vs formal contract conflict

current documented/required Product APIがgeneric relationを必須とする一方、formal allowlistが同tupleをTYPED_STRUCTURALとして禁止する場合。

## 62.3 Protected Gate regression required by policy

P01 policyを実装するために:

```text
G02-G05 authority semantics
```

を壊す必要がある場合。

その場合:

```text
G06-P01_BLOCKED
```

として:

```text
Facts
Contradiction
Affected contract
Observed code/test
Why local implementation cannot resolve it
Required decision
```

を報告する。

単なる実装量、test failure、fixture failureはDESIGN_BLOCKED理由ではない。

---

# 63. Facts / Interpretation / Unknown Rule

Coding Agentは調査結果・reportで:

```text
Facts
Interpretation
Unknown / Unconfirmed
```

を分離する。

例:

```text
Fact:
existing test uses Result MOTIVATED Execution.

Fact:
formal allowlist explicitly names Result MOTIVATED AnalysisSpecification and
approved user-authored/manual links.

Interpretation:
Result MOTIVATED Execution may be intended as an approved manual link.

Unknown:
whether Execution is explicitly approved as MOTIVATED target if formal
documents do not make that target set unambiguous.
```

Unknownを勝手にFactsへ昇格しない。

---

# 64. Root Cause Rule

test failureが発生しても再現証拠なしにroot causeを断定しない。

許容:

```text
NOT_REPRODUCED
ROOT_CAUSE_UNCONFIRMED
```

禁止:

```text
probably fixture issue
```

だけでtestを変更すること。

---

# 65. P01 Exit State

P01 successful completion時:

```text
Package:
P01 COMPLETE

Central authority policy:
ESTABLISHED

Manual generic admission:
POLICY-GUARDED

Global structural writer cutover:
NOT YET COMPLETE

Global generic-only writer convergence:
NOT YET COMPLETE

Typed read reconstruction:
NOT YET COMPLETE

Closure/export projection:
NOT YET COMPLETE

Mutation lineage audit:
NOT YET COMPLETE

E4-G06:
NOT_COMPLETE

TD-004:
OPEN
```

---

# 66. Immediate Next Package

P01がCOMPLETEしたら停止する。

次に実行するpackage:

```text
G06-P02
Structural writer cutover
```

planned instruction:

```text
10_enhance_instruction/G06/
06_G06_P02_structural_writer_cutover_instruction.md
```

P01 Coding AgentがP02を自動継続してはならない。
