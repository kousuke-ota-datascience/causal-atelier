# ENH-E5 Current State Control Sheet（現状態管理表）

> Document class: Planning / Evidence / State Artifact
> State self-containment: このControl Sheetだけでverified current state、protected contracts、OPEN Transition Debt、active orchestration pointerを理解できること。

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Branch: `feature/ariadne_mvp_e5`
- Verified through Gate: `NONE`
- Current Active Gate: `G00`（未開始。draft contractのみ）
- Last updated: `2026-08-11T16:21:58+09:00`
- 更新権限: final Gate Decision後のHuman ownerのみ

## 1. Purpose and authority

final PASS済みGate evidenceだけをverified stateへpromotionする。Draft design、package completion、READY_FOR_TEST、FAIL/BLOCKED candidateをcurrent truthへ昇格しない。

## 2. Verified baseline

- Baseline commit: `46122c68333df03680b97c253a7b5d32bf9393e7`
- Verified implementation commit: `NONE`
- Migration / schema head: `UNKNOWN`
- Runtime / deployment baseline: `UNKNOWN`

Planning baseline SHAはremote branch HEADから確定済み。G00契約freeze前にlocal checkout一致とtest baselineをpreflightで確認する。

## 3. Verified current architecture / behavior

Planning discoveryで観測したが、Gate PASSによるverified stateにはまだ昇格していない事項:

- Product domainに`AnalysisFamily = EXPLORATORY | CAUSAL | PREDICTIVE`が存在する。
- Execution workflow側にgeneric `StageType`, `StageDefinition`, `StageExecution`が存在する。
- current frontendはProject/Data, Explore, Causal Discovery, Causal Inference, Predictive, Results/Lineage等をsingle sidebarで混在表示する。
- current predictive UIはPrediction Task / Split / Training / Evaluation / Explanation / Model Card等の設定・結果surfaceを保持する。
- current `AnalysisSpecification`は既に`analysis_family: AnalysisFamily`を保持する。
- current `ExecutionPlan` / `Execution`も`analysis_family`を持ち、runtime Stageは`StageType / StageDefinition / StageExecution`として別に表現される。
- Existing implementation alignment reviewにより、current canonical Resource field、planner shape、Worker lease、CLI/API、Lineage authority、package mapをRevised designと再突合し、設計側の乖離を修正した。Review verdictは`PASS_WITH_CORRECTIONS_APPLIED`。

これらはarchitecture discoveryのsource factであり、G00 PASS前はprotected contractではない。

## 4. Authority map

| Domain | Authority |
|---|---|
| Enhancement目的/scope | approved `00_enhance_background/02_enhancement_concept_approval_record.md` |
| target architecture | approved architecture decision record + `04_design_revision.md` |
| Gate implementation semantics | Gate-local `06_*_implementation_instruction.md` |
| Gate acceptance criteria | Gate-local `07_*_test_instruction.md` |
| Work Package planning / decomposition | P00（Operator / Planning用） |
| Work Package execution | assigned freeze済みPxxのみ |
| Fixed Trial Candidate identity | implementation completion report |
| Gate PASS/FAIL/BLOCKED | Test Item 999 Gate Decision |

## 5. Protected contracts

`NONE` — まだENH-E5でPASSしたGateはない。

## 6. OPEN Transition Debt

planning baselineでは`NONE`。後続へ延期したfeatureは明示的なout-of-scopeであり、Transition Debtではない。

## 7. Preflight state

- branch identity: `NOT_RUN`
- full baseline SHA / local一致確認: `NOT_RUN`（期待値 `46122c68333df03680b97c253a7b5d32bf9393e7`）
- clean/expected repository state: `NOT_RUN`
- test baseline: `NOT_RUN`
- DB/migration head: `NOT_RUN`

## 8. Active orchestration pointer

1. Humanが00層のscopeとarchitecture decisionをreview/approveする。
2. `40_operator_workflows/preflight/ENH-E5_preflight_instruction.md`を実行する。
3. local HEADがpin済みbaseline SHAと一致することを確認し、test baselineを記録する。
4. Freeze G00 06/07.
5. Start G00 Trial01.

## 9. Evidence index

`NONE` — implementation/test evidenceはまだ生成されていない。

## 10. Update log

- 2026-08-11T16:21:58+09:00: 既存実装整合性監査を完了。Resource field、canonicalization/schema registry、auth/role、Worker lease、planner shape、API route semantics、Research Context relation/usage、Lineage authority、CLI/package boundaryをPlanning baseline sourceへ突合し、設計側の乖離を修正。監査判定は`PASS_WITH_CORRECTIONS_APPLIED`。
- 2026-08-11T16:10:52+09:00: 既存実装・設計整合性レビューを実施。unchanged contractのsource-of-truthをPlanning baseline current codeへ戻し、Resource field、planner、Worker lease、CLI/API、Lineage、package map等の設計乖離を修正。Gate PASS promotionはまだない。
- 2026-08-11T15:17:11+09:00: API/詳細設計の自己完結性レビューを反映。AnalysisFamily、Result/Annotation/Artifact、Worker lease、StageExecution、Predictive contract等を本文内へ展開し、存在しないpublic claim/event contract前提を除去。Gate PASS promotionはまだない。
- 2026-08-11T14:39:45+09:00: review feedbackを反映した次版planning stateへ更新。Gate PASS promotionはまだない。

## Execution Agentへの参照禁止

Current State Control Sheetはoperator/state control artifactであり、通常のCoding/Test Agentへnormative inputとして読ませない。

protected Gate identityが必要な場合、freeze担当者が06/07/Pxx本文へ具体値を転記する。

