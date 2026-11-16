# 10_00_overall_RD

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`; original ID, level and state retained.  
**Source blob:** `40b83f29c67b4a39f6db5393be7534c5e892d656`.

---

## 0. INTRODUCTION

### 0.1. プロダクトコンセプトから導かれる要件上の課題

Ariadneのプロダクトコンセプトを、次のとおり定義する。

> **Ariadneは、Projectを問い・データ・分析・結果・判断の来歴境界とし、Project ManagementでResearch Contextおよびversioned analysis inputを管理し、Analysis WorkspaceでExploratory / Predictive / Causalの分析を行い、その条件、結果、判断理由および相互関係を追跡可能にする分析プロダクトである。**

このプロダクトコンセプトに基づき、Ariadneでは、探索的分析、予測分析、因果分析という、目的・判断基準・成果物の意味が異なる分析活動を、一つのProjectの中で継続的に扱う必要がある。

これらの分析活動を適切に扱うため、ユーザーは少なくとも次の二つの情報を明確に把握できなければならない。

* **どのAnalysis Familyで分析しているか**
  探索、予測、因果のいずれの分析目的・分析観点に基づいて作業しているか。

* **そのAnalysis Familyの中で、現在どの分析作業を行っているか**
  データ確認、分析条件の定義、モデルまたは推定方法の構築、評価、診断、結果確認など、分析ワークフロー上の現在位置。

この二つが明確に区別されない場合、ユーザーは現在の分析目的と作業位置を把握しづらくなり、異なるAnalysis Familyに属する操作、結果および判断を混同する可能性がある。

特に、予測分析における予測性能や特徴量寄与と、因果分析における因果効果や識別結果は、意味および判断基準が異なる。したがって、異なるAnalysis FamilyのResultを同一の意味を持つ結果として扱ってはならない。

また、探索から予測分析または因果分析へ進む場合、あるいは複数の分析結果を比較、再利用または改訂する場合には、少なくとも次の情報を追跡できなければならない。

* Research TopicおよびResearch Context
* DatasetおよびDataset Version
* Analysis Viewその他の分析対象データの導出条件
* Analysis Specification
* ExecutionおよびExecution Plan
* ResultおよびArtifact
* 分析時の判断、AnnotationおよびWarning
* これらの間のLineage

これらの情報が失われた場合、分析結果の再現、比較、根拠確認、改訂、および後続分析への適切な引継ぎが困難になる。

したがってAriadneは、異なるAnalysis Familyの意味論を明確に分離しながら、一つのProject内で分析ワークフローを継続的に扱うことができ、各分析の問い、入力データ、分析条件、実行、結果、判断およびLineageを一貫して追跡可能な分析環境を提供しなければならない。

### 0.2. Legends

#### 0.2.1. Requirement levels

- `MUST`: acceptanceに必須。
- `MUST NOT`: 実装してはならない。
- `SHOULD`: 強い推奨。逸脱には明示理由が必要。
- `MAY`: 任意。必須acceptanceには含めない。

#### 0.2.2. Requirement lifecycle

各Requirementは、Requirementそのものの有効性、現在の実装充足状態、およびdelivery origin/scopeを独立した属性として管理する。

##### Requirement Status

Requirementがproduct requirementとして現在どの状態にあるかを表す。

| Value | Meaning |
| --- | --- |
| `ACTIVE` | 現在有効なRequirement。現在実装済みか、将来実装予定かには依存しない。 |
| `DEFERRED` | Requirementとしての必要性は維持するが、current mandatory delivery/acceptanceから除外され、将来の実装対象として延期されている。 |
| `RETIRED` | Requirementとして廃止され、current product contractとして維持しない。 |

##### Implementation Status

Requirementに対する現在の実装充足状態を表す。

| Value | Meaning |
| --- | --- |
| `IMPLEMENTED` | Requirementを満たす実装が存在し、当該snapshotでcurrent implementationとして確認されている。 |
| `PARTIAL` | Requirementの一部は実装されているが、Requirement全体を満たしていない。 |
| `NOT_IMPLEMENTED` | Requirementを満たす実装が確認されていない。 |
| `UNVERIFIED` | 実装有無またはRequirement充足状態を利用可能なevidenceから確定できていない。 |

##### Delivery

Requirementの実装・主要改訂がどのdelivery scopeに属するかを表す。

| Value | Meaning |
| --- | --- |
| `BASELINE` | ENH-E5開始時点までにcurrent implementationへ含まれていた既存contract。 |
| `ENH-E5` | ENH-E5で実装または不足部分の完成をdelivery対象としたRequirement。 |
| `ENH-E7` | ENH-E7で追加、責務改訂、または実装充足したRequirement。 |
| `ENH-E10` | ENH-E10 Predictive Advanced Modeling / XAIで追加または主要改訂したRequirement。 |
| `FUTURE` | current snapshot時点では実装完了対象外で、将来Enhancementで扱うRequirement。 |

三つの属性は独立した軸として扱う。`Delivery`はRequirementの由来・主要delivery段階を示し、`Requirement Status`や`Implementation Status`の代替ではない。

#### 0.2.3. 用語

- `Family`: Exploratory / Predictive / Causalのanalytical capability context。
- `Navigation Stage`: Family内でユーザーが選択するwork/view context。
- `Execution Stage`: ExecutionPlan / StageExecutionに属するruntime execution unit。
- `Stage`を単独で用いる場合、UI/application文脈ではNavigation Stageを指す。

## 1. 適用範囲

AriadneはProject / Research Topicを境界として、Research Context、Dataset Version、Analysis View、Exploratory / Predictive / Causalの三つのAnalysis Family、Execution、Result、Artifact、AnnotationおよびLineageを管理する。

Application surfaceは`Project Management`と`Analysis Workspace`へ責務分離する。Project ManagementはProject resource / versioned analysis inputのlifecycleを管理し、Analysis WorkspaceはCurrent Project / Active Research Context / Dataset Version / Analysis ViewからなるAnalysis Contextの下でanalysis execution / presentationを行う。

Analysis WorkspaceではAnalysis Familyをanalytical context、Navigation StageをFamily-local work/view contextとして扱う。Navigation Stageはruntime Execution Stageではない。

対象データは前処理可能な表形式データとし、予測分析の対象TaskはBinary ClassificationとRegressionとする。因果分析はGraph Discovery、Identification、Data Eligibility、ATE / ATT Estimation、Diagnostics、RefutationおよびSensitivityを対象とする。

## 2. Actor

| Actor | 責務 | 権限上の位置づけ |
| --- | --- | :--- |
| Analyst | Context、Data、Analysis Specification、Execution、比較、Annotationを作成・操作する | ProjectMembership roleに従う。WRITE / MUTATEおよびExecution mutationはOWNER / EDITOR |
| Reviewer / Viewer | Result、warning、diagnostics、Lineage、Annotationを確認する | ProjectMembership roleに従う。VIEWERを含むOWNER / EDITOR / VIEWERがread可能 |
| Infrastructure Operator | 実行基盤、保存領域、認証、監視等のinfrastructureを運用する | ProjectMembership roleではない運用persona。system-level authorization policyはDEFERRED / FUTURE |

## 90. この文書種別の目的・責務・規範性

- **目的:** User/OperatorがAriadneに期待してよい機能、科学的許容条件、状態、セキュリティ、再現性および検証可能な受入条件を定める。
- **含む:** MUST/SHOULD/MUST NOT、FR/NFR/AR ID、Requirement Status/Implementation Status/Delivery、Actor/UC/Scope、科学的反例、Test/Acceptance Sourceへのリンク。
- **含まない:** Python classの命名やprivate field、REST/CLIのwire format詳細、推定アルゴリズムの実装手続。
- **優先順位:** 現行正本の規範性は`docs/wiki/requirement_definition/10_requirements_definition.md`に残る。DEC09で採用された意味差分は別途この作業コピーで改訂草案を作り、Owner批准・SHA・Status確定後にControlled Publicationする。
- **E11特則:** 旧§11のDoWhy/EconML除外は、DEC09採用のE11機能別optional外部engineに限定して改訂予定。旧FR-161（E10 optional predictive engine）はこの許可の根拠として転用しない。
- **受入:** Scope68行ごとのR/Q/N/D、E11-REQ仮ID→新正式ID、Method/UC/Issue/Architecture/Gate、旧条文との逐条diffを監査する。既存ProductのPARTIALを黙ってIMPLEMENTEDにしない。

**E11追加草案:** [10_14_enh_e11_formal_requirement_publication_draft.md](10_14_enh_e11_formal_requirement_publication_draft.md)
