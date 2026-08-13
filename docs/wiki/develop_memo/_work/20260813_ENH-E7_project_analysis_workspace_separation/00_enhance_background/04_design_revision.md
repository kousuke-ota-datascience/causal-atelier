# ENH-E7 Design改定

**文書種別:** Planning / Decision Artifact  
**Status:** PROPOSED_PENDING_ARCHITECTURE_REVIEW

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
PROFILE → Profile、DISTRIBUTION → Distribution、ASSOCIATION → Relationships、
GROUP_SUMMARY → Comparison、Saved Exploratory Results → Findings。

`Data Quality / TIME_TREND / CHART`はG02 freeze前にsource factで確定する。

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
