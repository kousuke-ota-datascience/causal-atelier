# ENH-E5 要件・設計整合性およびトレーサビリティ確認

- 状態: `DRAFT_FOR_REVIEW`

## 1. Review conclusion

Revised 00〜30は、Family / Navigation Stageをapplication concernとして追加し、existing execution/resource architectureを維持する方向で整合させる。

Human approval前のtarget decision（navigation metadata endpoint、exact route/default等）はDRAFTとして明示し、06/07 freeze前に確定する。

## 2. Traceability matrix

| Requirement | Logical Data | Basic Design | API/Interface | Detailed Design | Gate |
| --- | --- | --- | --- | --- | --- |
| FR-001〜128 existing product baseline | 3.1 / 4 / 5 / 6〜8 | 2〜15 existing architecture | 1〜17 existing interface taxonomy | 1〜21 existing implementation design | regression-protected across G00〜G05 |
| FR-104〜105 revised Workspace navigation baseline | 3.2 navigation state | 4 Workspace IA / 10 Frontend State | 13 Frontend Support / 15 CLI boundary | 18 Frontend / Navigation Components | G01/G05 |
| FR-129〜139 Family/Stage navigation | 3.2 / 4.2 | 4.3〜4.6 Workspace IA | 13.2〜13.3 Frontend Support, routeはFrontend contract | 18 Frontend / Navigation Components | G00/G01 |
| FR-140〜143 Nav/Execution separation | 3.2.2 / 4.2 | 3.3 / 5.5〜5.6 Generic Workflow Core | 6.2, 10.1, 14.2, 15.1 | 8.1, 11.1〜11.2, 19.1 | G00/G05 |
| FR-144〜145 Capability ownership | 3.2 / 4.2 | 3.2 / 6 Family別Workflow/Capability | 13.3 source of truth | 10.1 Capability-owned Navigation Catalog | G00 |
| FR-146〜148 Exploratory | existing Result/Annotation/Lineage + 3.2 | 4.5.1 / 6.1 / 7.2 | 7 Explore API | 12 Exploratory Capability | G04 |
| FR-149〜152 Predictive | 5.5 AnalysisSpecification等 | 4.5.2 / 6.3 / 7.4 | 6.3 / 9 Predictive API | 14 Predictive Capability | G02 |
| FR-153〜156 Causal | GraphVersion / Result + existing family discriminator | 4.5.3 / 6.2 / 7.3 | 8 Causal API | 13 Causal Capability | G03 |
| FR-157〜162 compatibility/persistence/scope | 3.2 / no persistent nav state | 4.2〜4.4 / 10 / 14 | 10〜17 existing contract + 13 frontend support | 18.6 / 19.1 / 21 | G01/G05 |

## 3. Consistency checks

### 3.1 Product Concept / Requirements

- Product Conceptはproduct visionから開始し、Enhancement履歴を本文冒頭に置かない。
- Requirementsはcurrent effective stateを本文、Change Logを末尾に置く。

### 3.2 Logical Data / Current Code

- `AnalysisSpecification.analysis_family`が既存であるためFamily field追加なし。
- Navigation StageはAnalysisSpecificationへ追加しない。
- runtime StageType/StageDefinition/StageExecutionをNavigation descriptorへ再利用しない。

### 3.3 Basic / API / Detailed Design

- UI navigationを文書トップレベルの唯一の主役にせず、Presentation責務配下へ配置する。
- backend/application/capability/executionの影響を同時に記述する。
- execution semanticsはnavigation taxonomyから独立する。

### 3.4 Predictive 100% preservation

G02 P01はcurrent Predictive設定項目をrepository factとして全量inventoryし、compatibility guardrailを成立させるPackageとする。P01完了前に、inventory結果へ依存するG02 P02/P03をFROZENにしない。P02/P03へ必要なfactはPlanning担当が各Pxx本文へ収束させる。

### 3.5 Deferred scope isolation

External engines、Flagship、新Finding domain等がGate scopeへ混入していないことを確認する。

## 4. Heading / document-role review

全文書について、同一heading levelに異なる抽象度の概念が混在しないことを確認する。

- abstract -> concrete
- Why -> What -> How
- current effective state -> change log
- major responsibility -> subsection detail

## 5. Open approval items

- navigation metadata deliveryをbackend APIとするか、そのexact contract
- canonical browser route exactness / legacy mapping
- Causal default Stage
- Overview/Flagship deferred positioning

これらはHuman approvalまたはArchitecture Reviewで確定後、06/07へ収束させる。
## 6. Existing implementation alignment

ENH-E5で変更しない領域について、Planning baseline sourceとRevised 21/22/23/30を追加突合した。結果は`06_existing_implementation_design_alignment_review.md`に記録し、検出した乖離は設計側へ反映済みである。

主な修正対象は、canonical Resource field、Result status matrix、Worker claim/lease、Causal/Exploratory/Predictive planner shape、PlanValidator/RunnerRegistry、CLI、API route、Lineage authority、current package/module mapである。

このreviewにより、target Navigation designとcurrent runtime factを明示的に分離した。current implementationに存在しないFamily/Navigation Stage targetそのものは乖離扱いせず、既存runtime contractを壊さないことをtraceability/Acceptance Criteriaで保護する。

