# ENH-E7 G03 — UI Surface Architecture Correction Contract

Status: FROZEN  
Execution Mode: WORK_PACKAGE

## Gate claim

G01/G02で成立したrouting/domain/application semanticsを保護しながら、
current non-conforming global shellをtarget IAに合わせて置換し、
Projects Surface / Project Management Shell / Analysis Workspace Shellが
DOM ownership・runtime visibility・navigation hierarchy・layout topologyの各観点で分離される。

## Work Package一覧

- P01 — Top-level Surface Activation Authority — dependency: G02 PASS
- P02 — Projects Surface Separation — dependency: P01
- P03 — Project Management Shell — dependency: P02
- P04 — Analysis Workspace Shell — dependency: P03
- P05 — Obsolete Global Shell Cleanup — dependency: P04
- P06 — Surface Architecture Integration — dependency: P05

## Active contract rule

- G01/G02のPASS artifactsは履歴として保持する。
- G01/G02 normative requirementsに反するcurrent presentation implementationはprotected implementationではない。
- G03はCSS微調整Gateではなくpresentation architecture correction Gateである。
- PxxはdependencyとpreflightがPASSした場合だけexecution eligible。
- 08はformal FAILまでinactive。
- 09はsemantic Gate contract amendmentが明示的に承認された場合だけactive。
