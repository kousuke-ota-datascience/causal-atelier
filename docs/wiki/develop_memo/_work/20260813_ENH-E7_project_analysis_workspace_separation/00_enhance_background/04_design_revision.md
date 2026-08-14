# ENH-E7 Design改定

**文書種別:** Planning / Decision Artifact  
**Status:** APPROVED_FOR_G01_AND_FROZEN_FOR_G02

## 1. Navigation authority

```text
Application Navigation
├─ Project Navigation
│  ├─ /projects
│  ├─ /projects/new
│  └─ /projects/<id>/<section>
└─ Analysis Navigation
   └─ /projects/<id>/analysis/<family>/<stage>[/resource/...]
```

Project route authorityをAnalysis-specific navigation stateへ混在させない。
ENH-E6のAnalysis navigation / transition authorityをprotected upstream semanticsとして維持する。

## 2. UI ownership

- Projects Surface: Project List / New Project entry
- Project Management Shell: header / local navigation / Overview / Context / Data / Results
- Analysis Workspace Shell: Analysis Context / Family tabs / Stage sidebar / Stage Contents

## 3. Analysis Context

- Current Project: URL由来、read-only
- Research Context: existing Project resourceから選択
- Dataset Version: existing Project resourceから選択
- Analysis View: selected Dataset Versionと整合するexisting viewから選択

Project変更はProjects / Project Management経由で行う。

## 4. Resource ownership

- Project metadata / archive → Overview
- Research Context lifecycle/history → Context
- Dataset / Dataset Version / Schema / Preview / Analysis View lifecycle → Data
- persisted cross-analysis result / comparison / artifacts / lineage / annotation → Results / Lineage
- Stage-local execution/result presentation → Analysis Workspace

## 5. Surface migration

### Causal
Setup / Discovery / Identification / Estimation / Effects / Diagnostics / Sensitivityへexisting surfaceを移設する。

### Exploratory
| Stage | Existing operation / availability | Final placement behavior |
| --- | --- | --- |
| Profile | `PROFILE` | operation controlとProfile resultを配置する。 |
| Data Quality | operationなし | read-only availability stage。existing `PROFILE` resultを表示し、存在しない場合は`NO_PROFILE_RESULT`とProfileへの導線だけを表示する。execution、resource、backend stateを作らない。 |
| Distribution | `DISTRIBUTION` | operation controlとresultを配置する。 |
| Relationships | `ASSOCIATION` | operation controlとresultを配置する。 |
| Comparison | `GROUP_SUMMARY`, `TIME_TREND` | 両operationのcontrolとresultを配置する。`TIME_TREND`は既存grouping/aggregationであり、時系列モデルや時刻型validationを追加しない。 |
| Findings | `CHART`およびsaved Exploratory Results | `CHART` control、Chart artifact/result、既存saved resultを配置する。`CHART`は既存の永続operationであり、表示専用mechanismへ置換しない。 |

`DATA_QUALITY` operationは作らない。Stage placementはpresentation/navigation decisionであり、Exploratory planner、runner、Result type、artifact type、API/persistenceを変更しない。

### Predictive
existing `Prediction Task → Split → Training → Evaluation → Explanation → Model Card` semanticsを保護する。
Stageはpresentation/navigation viewであり、新backend execution modelではない。

## 6. Legacy compatibility

replacement Analysis Workspace成立後に旧analytical UI shortcutを削除する。
legacy URLはcanonical Analysis routeへnormalizeする。

## 7. API / persistence方針

```text
Persistence migration: NONE EXPECTED
API contract change: NONE EXPECTED
Backend domain semantic change: NOT AUTHORIZED
```

## 8. Coding Agent information isolation

```text
Human operator
  -> Enhancement-specific prompt
  -> assigned Pxx
  -> source / tests / config / migrations
```

Coding AgentはGate 06 / 07 / P00 / other Pxx / 00 / 20 / 30を仕様補完目的で読まない。

## 9. Rollback

- G01 rollbackでENH-E6 protected Analysis semanticsを変更しない。
- G02 rollbackでG01 PASS contractを保護する。
