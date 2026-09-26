# ENH-E10 Enhance構想承認記録 — Predictive Advanced Modeling / XAI

> **Document class:** Planning / Decision Artifact  
> **Status:** `MATERIALIZED / PENDING_HUMAN_APPROVAL`  
> **Self-containment:** MUST for own subject

- Decision: **PENDING**
- Decision timestamp: **N/A — formal concept approval has not been recorded**
- Decision authority: **Human enhancement owner / architecture owner**
- Reviewed proposal: `00_enhance_background/01_enhancement_concept_and_requirement_revision_plan.md`
- Primary handoff: `00_enhance_background/_handoff/ENH-E10 Handoff — Predictive Advanced Modeling - XAI.md`
- Implementation authorization: **NO**

## 1. Approval state

本artifactの目的は、未承認状態を曖昧にしないことである。

ENH-E10 working directoryのmaterializationとGate draft作成は進行しているが、それ自体をconcept / requirement / architectureのHuman approvalとして扱わない。

現時点では次のproposalがreview対象である。

- LightGBM Binary Classification / Regression
- SHAP
- LIME
- optional predictive-advanced dependency model
- provider-neutral model capability / artifact-load contract
- explanation compatibility/global-local contract
- capability-driven Predictive UI integration
- G01 / G02 / G03 decomposition

## 2. Proposed scope awaiting approval

### Proposed in-scope

- LightGBM classifier/regressor
- model registry/capability generalization
- fitted-model serialization/load/prediction
- optional dependency handling
- model/runtime/package provenance
- SHAP global/local Predictive Explanation
- LIME local Predictive Explanation
- model × explanation compatibility
- Train / Explainability / Model Management integration
- ENH-E10 scoped deterministic tests and final critical Browser E2E

### Proposed protected scope

- ENH-E8 Predictive six-stage navigation
- Setup-owned feature editing
- Train/Predict read-only feature context
- TRAIN-only preprocessing
- untouched TEST isolation
- existing logistic/linear behavior
- predictive-not-causal terminology
- ENH-E9 stabilized Project/Causal/Graph workflows

## 3. Conditions required for APPROVED

Formal `APPROVED` へ変更する前に、少なくとも以下をreviewする。

1. `03_requirements_revision.md` のrequirement delta
2. `04_design_revision.md` のarchitecture decisions / unresolved decisions
3. `05_requirements_design_consistency_and_traceability_review.md`
4. external enginesがmandatory core dependencyにならないこと
5. artifact/schema backward compatibility strategy
6. SHAP/LIME semanticsをmethod-specificに扱うこと
7. G01/G02/G03のacceptance boundary
8. E10 non-goalsがupstream scopeを侵食しないこと

## 4. Explicit non-approval

Architecture Review technical decision record now proposes exact values for the items below, but **technical selection is not Human approval**. 現時点で以下は承認済みとみなしてはならない。

- exact LightGBM / SHAP / LIME package version bounds
- exact optional dependency group composition
- final model IDs
- final model parameter defaults
- categorical/native missing-value support
- early stopping
- final fitted-model artifact schema/version
- SHAP output scale/background/additivity semantics
- LIME perturbation/discretization/sample defaults
- final capabilities API schema
- predictive spec version revision
- Browser E2E canonical environment/command
- G01/G02/G03 Coding execution

## 5. Required follow-up

Human enhancement owner / architecture ownerは、01/03/04/05をreviewし、次のいずれかを明示する。

- `APPROVED`
- `CONDITIONAL` with concrete conditions
- `REJECTED`

Architecture Reviewのtechnical decisionsはreview用draftとして04/05およびGate 06/07/Pxxへmaterializeしてよい。ただし、Humanが`APPROVED`または条件を満たした`CONDITIONAL`を明示するまで、canonical requirement/designへのapproved applicationおよびGate 06/07/Pxxの`FROZEN`化を行ってはならない。

本書が `PENDING` の間は、G01/G02/G03 implementationを開始しない。
