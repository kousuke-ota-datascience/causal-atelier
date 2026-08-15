# ENH-E7 G03 P00 Work Package Plan

文書種別: Planning / Operator Artifact  
Status: DRAFT_NOT_FROZEN  
P00はimplementation Work Packageではない。

## 1. Work Package Modeが必要な理由

同一frontend内でtop-level shell、Projects、Project Management、Analysis、cleanupが相互に影響する。
bounded executionとdependency controlにより、旧shellへのincremental patchではなく段階的なreplacementを行う。

## 2. Effective Gate semantic boundary

Gate claim:
Projects Surface / Project Management Shell / Analysis Workspace Shellをtop-level ownershipとして分離し、
old global shellを削除する。

共通constraint:

- G01/G02 normative semanticsを保護する。
- current non-conforming presentation implementationは保護しない。
- package completionをGate PASSと扱わない。
- Pxxをself-containedにする。
- obsolete shellのCSS-only hidingを最終状態に残さない。

## 3. Package map

| Package | Purpose | Depends on | Exit criterion |
|---|---|---|---|
| P01 | route/stateからtop-level surfaceを一意にactivateするauthorityを作る | G02 PASS | incompatible surfacesの同時activeを防止 |
| P02 | Project List / New ProjectをProjects Surfaceへ分離 | P01 | project未選択surfaceにproject/analysis固有chromeなし |
| P03 | selected ProjectのProject Management Shellとlocal vertical navを構築 | P02 | PM ownershipがDOM/runtimeで独立 |
| P04 | Analysis Context / Family / Stage / ContentsをAnalysis Workspace Shellへ構築 | P03 | Family横・Stage縦・PMとは別surface |
| P05 | old global sidebar / common header / dead presentation codeを削除 | P04 | duplicate/obsolete shellなし |
| P06 | 全surface topologyを統合しstructural regressionを閉じる | P05 | G03 candidate assembly可能 |

## 4. Dependency policy

P01→P02→P03→P04→P05→P06の順に実行する。
同一DOM/CSS/JS責務への競合patchを避けるため、G03は意図的に直列dependencyとする。
