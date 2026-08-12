# ENH-E5 Enhancement 構想・要件改定計画

- 状態: `APPROVED`
- 対象branch: `feature/ariadne_mvp_e5`
- Planning pin: `46122c68333df03680b97c253a7b5d32bf9393e7`
- ENH-E4 alignment baseline: `a770cc4f38137063cd5f22d8035e91e3c63b7502`
- Phase H basis:
  - `40_operator_workflows/preflight_analysis/remediation_decision_log.md`
  - `40_operator_workflows/preflight_analysis/remediation_decision_matrix.csv`
  - `40_operator_workflows/preflight_analysis/remediation_decision_freeze_audit.md`
  - `40_operator_workflows/preflight_analysis/d2_planning_decision_freeze.md`
  - `40_operator_workflows/preflight_analysis/d2_planning_decision_matrix.csv`
  - `90_technical_debt_and_future_enhancements.md`

## 0. Phase Hの結論

ENH-E5の改定scopeは、Family × Family-local Navigation StageのUI/Navigation再構成だけではない。

ENH-E4完了実装とのalignment auditにより検出した非MATCH項目を、次の3分類でplanningへ取り込む。

- `D1 CURRENT_IMPLEMENTATION`: current implementationをcurrent contractとして正本文書へ訂正する。
- `D2 E5_TARGET_CHANGE`: current implementationでは不足するがENH-E5で実装する。
- `D3 DEFER`: Requirement方向は維持するがENH-E5では実装せず、`DEFERRED / FUTURE`として正本へ残す。

remediation decision baselineは次のとおり。

| Decision | Decision Item |
|---|---:|
| D1 | 31 |
| D2 | 35 |
| D3 | 28 |
| Total | 94 |

D2の未確定planning decisionはPhase Gで11 packageへ収束済みであり、未割当・重複・未freezeはない。Phase H以降、下流文書でこれらを再解釈しない。

## 1. 課題認識

### 1.1 Family / Navigation Stageの責務分離

Ariadneは`EXPLORATORY / PREDICTIVE / CAUSAL`の3 Familyを扱うが、application navigation上のFamilyとFamily内work/view contextはruntime execution lifecycleと分離されなければならない。

Critical invariant:

> `Navigation Stage != Execution Stage`

Navigation StageはFamily-local UI/Application contextであり、`StageType / StageDefinition / ExecutionPlan / StageExecution`のruntime contractではない。

### 1.2 planning文書とcurrent implementationの乖離

ENH-E5 revised documentsの非変更部分をENH-E4完了実装baselineへ照合した結果、旧資料由来のoverstatement、未実装targetのcurrent fact化、current実装の責務境界と異なる記述が検出された。

したがってPhase Iでは、Family/Navigationの新規targetだけでなくD1によるcurrent contract訂正を同時に行う。

### 1.3 ENH-E5 scopeの拡張

alignment auditでD2と裁定された35 Decision Itemは、Family/Navigation Stageそのもの以外にも次を含む。

- AnalysisView typed filter validation
- Exploratory handoff / provenance
- Predictive subgroup evaluation
- scientific comparability / exploratory-reuse guard
- command idempotency / retry-safe Artifact commit
- Project authorization / sensitive output boundary
- canonical lineage completion
- reproducibility metadata completion
- frontend deep navigation / action state / accessibility
- D2-derived test architecture
- documentation self-containment / Navigation architecture freeze

これらはENH-E5 target contractへ含める。

## 2. 改定目的

1. Application model上のFamilyを`EXPLORATORY / PREDICTIVE / CAUSAL`として維持し、既存`AnalysisSpecification.analysis_family`をdiscriminatorとして再利用する。
2. `Family -> Navigation Stage*`をapplication/navigation modelとして成立させる。
3. Navigation StageとExecution Stageを分離し、Navigation stateをruntime/CLI/library/persistenceへ漏らさない。
4. Predictive既存設定・Specification semanticsを100%保持した上で再配置・拡張する。
5. D1をcurrent contract訂正として`10/21/22/23/30`へ反映する。
6. D2をENH-E5 targetとしてPhase G freezeどおり`10/21/22/23/30`へ具体化する。
7. D3をRequirement正本から削除せず`DEFERRED / FUTURE`として残し、詳細を90 ledgerへtraceする。
8. `10/21/22/23/30`だけでcurrent + E5 targetを理解できるself-contained normative snapshotを成立させる。
9. NFR-019再監査PASS後にのみ`06/Pxx/07`をfinal freezeする。

## 3. Requirement / Design snapshot改定方針

Revised documentsは差分要約ではなく、その時点で有効なnormative snapshotとして作成する。

### 3.1 Requirement table

`10_requirements_definition.md` のRequirement一覧は最低限次の列を持つ。

```text
ID
Area
Requirement
Level
Requirement Status
Implementation Status
Delivery
```

`Area`を採用し、`Domain`へ名称変更しない。

Status vocabulary:

- Requirement Status: `ACTIVE / DEFERRED / RETIRED`
- Implementation Status: `IMPLEMENTED / PARTIAL / NOT_IMPLEMENTED / UNVERIFIED`
- Delivery: `BASELINE / ENH-E5 / FUTURE`

Requirement本文には「ENH-E4では」「今回は」等のtiming-dependent wordingを置かない。時系列差分はplanning/change log/Deliveryへ分離する。

### 3.2 D1 / D2 / D3の正本反映

- D1: `ACTIVE / IMPLEMENTED / BASELINE`
- D2 MISMATCH: `ACTIVE / NOT_IMPLEMENTED / ENH-E5`
- D2 PARTIAL_MATCH: `ACTIVE / PARTIAL / ENH-E5`
- D3 MISMATCH: `DEFERRED / NOT_IMPLEMENTED / FUTURE`
- D3 PARTIAL_MATCH: `DEFERRED / PARTIAL / FUTURE`
- NFR-019: documentation-only D2として別途verification statusを管理する。

### 3.3 Planning evidenceとnormative authority

`preflight_analysis`はnon-normativeである。

```text
source/audit evidence
    ↓
preflight_analysis
    ↓
01〜06 planning documents
    ↓
10 / 21 / 22 / 23 / 30 canonical documents
    ↓
NFR-019 re-audit PASS
    ↓
06 / Pxx
07
```

Coding/Test Agentがpreflightから不足仕様を補完する運用は禁止する。

## 4. ENH-E5 In Scope

### 4.1 Family / Navigation

- Family tabs
- Family-local Navigation Stage sidebar
- URL-driven current Family/Stage state
- browser history / deep link
- legacy analytical route normalization
- backend-authoritative Navigation catalog
- capability-owned Stage catalog
- resource deep navigation
- backend-authoritative action availability
- async presentation state
- E5変更surfaceのaccessibility

### 4.2 Family catalog

Exploratory:

`profile / data-quality / distribution / relationships / comparison / findings`

Predictive:

`setup / train / predict / metrics / explainability / model-management`

Causal:

`setup / discovery / identification / estimation / effects / diagnostics / sensitivity`

Default:

| Family | slug | default_stage_id |
|---|---|---|
| EXPLORATORY | `exploratory` | `profile` |
| CAUSAL | `causal` | `setup` |
| PREDICTIVE | `predictive` | `setup` |

Canonical route:

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}
```

Navigation catalog:

```text
GET /api/v1/navigation/analysis
schema = analysis-navigation/1
```

### 4.3 D2 package scope

| Package | Scope |
|---|---|
| PF-D2-01 | AnalysisView Typed Filter Validation |
| PF-D2-02 | Exploratory Handoff & Provenance |
| PF-D2-03 | Predictive Subgroup Evaluation |
| PF-D2-04 | Scientific Comparability & Exploratory-Reuse Guard |
| PF-D2-05 | Command Idempotency & Retry-safe Artifact Commit |
| PF-D2-06 | Project Authorization & Sensitive Output Boundary |
| PF-D2-07 | Canonical Lineage Completion |
| PF-D2-08 | Reproducibility Metadata Completion |
| PF-D2-09 | Frontend Deep Navigation, Action State & Accessibility |
| PF-D2-10 | Derived E5 Test Architecture |
| PF-D2-11 | Documentation Self-containment & Navigation Architecture Freeze |

### 4.4 Compatibility

- Predictive existing controls/settingsを削除・rename・semantic changeしない。
- `AnalysisSpecification.analysis_family`を維持する。
- Navigation Stageを`AnalysisSpecification / ExecutionPlan / Execution / StageExecution`へpersistしない。
- Navigation catalogからruntime Stageを生成しない。
- CLI/library direct scientific executionをNavigation Stage必須入力にしない。
- current Result / Artifact / Lineage responsibilityをD1に従い訂正・維持する。

## 5. ENH-E5 Out of Scope / D3

以下はENH-E5 acceptanceへ含めない。

- LightGBM / DoWhy / EconML
- general operational AuditLog
- configurable retention/deletion policy
- distinct system/operator authorization
- sensitive/use-restriction column metadataとconfigurable sensitive-output policy
- automated hyperparameter selection
- additional Exploratory matrix/missing-pattern/visualization surfaces
- dataset/context/date filter expansion
- generic Product orchestration CLI
- DB/Worker/ArtifactStore component readiness
- operational hard limits / resource policy
- general p95 API SLO/performance gate
- object-storage adapter
- cross-store compensation
- production-grade authentication/security hardening
- explicit Worker restart/resume semantics
- comprehensive structured logging/metrics
- systematic schema-example synchronization

D3 Requirementは正本から削除せず、`DEFERRED / FUTURE`として保持する。

## 6. DB migration方針

従来の「DB migration: NONE」は撤回する。

ENH-E5で明示的に必要なmigration:

```text
StageAttempt.effective_random_seed: int | null
```

- stochastic Stageのactual effective seedをattempt単位で保存する。
- retryされた同一logical Stageは同じeffective seedを再利用する。
- deterministic Stageは`null`。

PF-D2-05のArtifact retry-safe materializationは、現時点では新規uniqueness columnを必須化しない。既存schemaで保証不能とPhase I詳細設計時に判明した場合、`30`を先にamendし、`06`でmigrationを発明しない。

## 7. Gate mapの扱い

既存G00〜G05はFamily/Navigation改修のsemantic acceptance boundaryとして維持する。

| Gate | Acceptance boundary |
|---|---|
| G00 | Family / Navigation Stage contractとruntime independence |
| G01 | URL-driven Family/Stage navigation shell、route/history、legacy compatibility |
| G02 | Predictive recomposition + existing setting/semantics compatibility |
| G03 | Causal recomposition |
| G04 | Exploratory recomposition |
| G05 | Cross-family convergence / product regression |

ただしD2 packageは複数Gateへcross-cutするため、Phase I/J完了前にGate別`06/Pxx/07`へ直接割り付けて仕様を補完しない。

## 8. Phase H以降の実行順序

```text
Phase H: 01〜06 planning update
    ↓
Phase I: 10 / 21 / 22 / 23 / 30 revision
    ↓
cross-document consistency / traceability audit
    ↓
Phase J: NFR-019 DOC-019-01〜08 re-audit
    ↓ all PASS
Phase K: 06 / Pxx / 07 convergence and freeze
    ↓
Phase L: ③-1 ↔ ① final re-audit
```

## 9. Freeze条件

Phase Iへ進む条件:

- D1/D2/D3 94 Decision Itemの裁定がfreeze済み。
- Phase G D2 35 Decision Item / 11 packageがFROZEN。
- `FR-122 / FR-126 / D10-006a / D10-006b` のD3 human approvalが明示済み。
- planning文書01〜06が上記裁定と矛盾しない。

Coding contract final freeze条件:

- `10/21/22/23/30`がself-contained。
- D1/D2/D3がcanonical documentsへ完全反映済み。
- NFR-019 `DOC-019-01〜08`がall PASS。
- その後にのみ`06/Pxx/07`をfinal freezeする。
