# ENH-E5 Current State Control Sheet（現状態管理表）

> Document class: Planning / Evidence / State Artifact  
> State self-containment: このControl Sheetだけでverified current state、protected contracts、OPEN Transition Debt、active orchestration pointerを理解できること。

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Branch: `feature/ariadne_mvp_e5`
- Enhancement State: `CLOSED`
- Verified through Gate: `G05`
- Current Active Gate: `NONE`
- Final Verified Implementation Candidate: `5cf0caf515b8e57fc114eabea0efd9acffe23e62`
- Final Gate: `G05 / Trial01`
- Final Gate Decision: `PASS`
- Final Promotion Eligibility: `PROMOTION_ALLOWED`
- Last updated: `2026-08-13T14:24:45+09:00`
- 更新権限: final Gate Decision後のHuman ownerのみ

## 1. Purpose and authority

本書は、ENH-E5のverified current stateをHuman ownerがpromotionし、Enhancement全体のcloseout状態を管理するstate-control artifactである。

verified stateへpromotionできるのは、Independent Test Agentによるfinal Gate Decisionが`PASS`かつ`PROMOTION_ALLOWED`となったFixed Trial Candidateのみとする。

以下をverified current truthへ昇格してはならない。

- Draft design
- Package completion / `PACKAGE_READY`
- Coding Agentのself-verification
- `READY_FOR_TEST`
- `FAIL` / `BLOCKED_*` candidate
- evidence-only commitをsemantic implementation candidateとみなした状態

ENH-E5はG00からG05までの全Gateがfinal `PASS / PROMOTION_ALLOWED`となったため、Human owner authorityにより`CLOSED`へpromotionする。

---

## 2. Verified baseline / final implementation identity

- Planning baseline commit: `46122c68333df03680b97c253a7b5d32bf9393e7`
- Verified implementation commit: `5cf0caf515b8e57fc114eabea0efd9acffe23e62`
- Verified implementation source: `G05 / Trial01 FIXED_TRIAL_CANDIDATE_SHA`
- Final G05 Test Evidence commit: `3f7da9d87acdf24fe4b5ba8b81671c0c1eaec21f`
- Enhancement state: `CLOSED`
- Migration / schema state: G05 Fixed Trial Candidateに含まれるverified semantic implementation stateをauthorityとする
- Runtime / deployment state: separate deployment baselineとしてはpromotionせず、Gate evidenceで検証されたcandidate-bound stateをauthorityとする

### 2.1 Commit identity rule

以下は別identityである。

```text
FIXED_TRIAL_CANDIDATE_SHA
!= implementation evidence commit
!= TEST_EVIDENCE_COMMIT_SHA
!= closeout documentation commit
```

ENH-E5のverified implementation commitは、最終semantic candidateである次のSHAに固定する。

```text
5cf0caf515b8e57fc114eabea0efd9acffe23e62
```

G05 Independent Test evidence commit `3f7da9d...` および本closeout後に作成されるdocumentation-only commitは、verified implementation commitを置換しない。

---

## 3. Verified current architecture / behavior

G00からG05までのfinal PASSにより、少なくとも以下のENH-E5 contract群はverified stateへpromotionされた。

### 3.1 Family / Navigation domain

- `AnalysisFamily = EXPLORATORY | CAUSAL | PREDICTIVE` をFamily authorityとして扱う。
- Navigation Stageとruntime Execution Stageを別概念として扱う。
- Family / Navigation Stage catalogとcanonical route contractをG00/G01のprotected contractとして扱う。
- canonical deep-link / route validation / operation-availability semanticsをG01のprotected contractとして扱う。

### 3.2 Predictive Family

- Predictiveを6つのNavigation Stageへ再構成した状態をG02のprotected contractとして扱う。
- Navigation Stageの再構成によって既存Predictive execution semantics、設定項目、scientific protectionを破壊しない。
- subgroup evaluation、saved Result read surface、draft preservation等のG02 acceptanceをprotected contractとして扱う。

### 3.3 Causal Family

- Causalを7つのNavigation Stageへ再構成した状態をG03のprotected contractとして扱う。
- IdentificationとEstimationの責務分離、および既存Causal execution semanticsをG03のprotected contractとして扱う。

### 3.4 Exploratory Family

- Exploratoryを6つのNavigation Stageへ再構成した状態をG04のprotected contractとして扱う。
- AnalysisView、typed filter、Exploratory execution、Result保存、Causal/Predictive handoff等のG04 acceptanceをprotected contractとして扱う。
- G04最終Trialではcanonical Chromium regressionがPASSしている。

### 3.5 Cross-family / product-wide contract

G05 final PASSにより、以下をENH-E5最終cross-cutting protected contractとして扱う。

- cross-family comparison compatibility
- side-effecting command idempotency
- explicit lineage-linkのscope boundary
- canonical typed lineage projection
- reproducibility / effective random seed
- runtime manifest
- G00-G04 protected regression preservation

### 3.6 Closeout時にverified behaviorへ昇格しない観測事項

closeout時の追加観測として、3 Family tabが実画面上で期待どおり表示されていない可能性がある。

この観測はENH-E5の既PASS Gateを遡及変更せず、別bugfix enhancementで再現・原因確定・修正するfollow-up itemとする。

ENH-E5 closeout時点では、この観測を理由にproduction code、test code、06/Pxx/07、既存Gate evidenceを変更しない。

---

## 4. Authority map

| Domain | Authority |
|---|---|
| Enhancement目的/scope | approved `00_enhance_background/02_enhancement_concept_approval_record.md` |
| target architecture | approved architecture decision record + `04_design_revision.md` |
| Gate implementation semantics | Gate-local freeze済み`06_*_implementation_instruction.md` |
| Gate acceptance criteria | Gate-local freeze済み`07_*_test_instruction.md` |
| Work Package planning / decomposition | P00（Operator / Planning用） |
| Work Package execution | assigned freeze済みPxxのみ |
| Fixed Trial Candidate identity | current Trialのimplementation completion report |
| Gate PASS/FAIL/BLOCKED | current TrialのTest Item 999 Gate Decision |
| verified state promotion | final Gate Decision後のHuman owner |
| deferred D3 ledger | `00_enhance_background/90_technical_debt_and_future_enhancements.md` |

---

## 5. Protected contracts / final Gate promotion record

ENH-E5のG00-G05はすべてfinal `PASS / PROMOTION_ALLOWED`。

| Gate | Final Trial | FIXED_TRIAL_CANDIDATE_SHA | Final Gate Decision |
|---|---:|---|---|
| G00 | Trial01 | `6e8eb6736a0d72403f5c6ca1a019e8f562d4533c` | `30_test_report/G00/Trial01/E5-G00_01__999_gate_decision.md` |
| G01 | Trial04 | `1fb9e0f3bd8850782433a2475900fce45d420cd4` | `30_test_report/G01/Trial04/E5-G01_04__999_gate_decision.md` |
| G02 | Trial01 | `b5fe825c046714c1865c0e6cc1733851aaca8ae2` | `30_test_report/G02/Trial01/E5-G02_01__999_gate_decision.md` |
| G03 | Trial01 | `bb4afd2b94e724e64d60945bc961cea044acacef` | `30_test_report/G03/Trial01/E5-G03_01__999_gate_decision.md` |
| G04 | Trial02 | `564df2da67efa43c4455718b9b3d81f6d3e98c61` | `30_test_report/G04/Trial02/E5-G04_02__999_gate_decision.md` |
| G05 | Trial01 | `5cf0caf515b8e57fc114eabea0efd9acffe23e62` | `30_test_report/G05/Trial01/E5-G05_01__999_gate_decision.md` |

### 5.1 Test evidence commit identity

`TEST_EVIDENCE_COMMIT_SHA`はTest evidence/reportをcommitした後に確定するため、同一commit内の`999_gate_decision.md`へ自己参照値として必ずしも記録されない。

exact Test Evidence commitが必要な場合は、対象999 reportに対してGit historyをauthorityとして解決する。

例:

```bash
git log -1 --format='%H' -- \
  docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/30_test_report/G05/Trial01/E5-G05_01__999_gate_decision.md
```

G05 final Test Evidence commitは以下で確定済み。

```text
3f7da9d87acdf24fe4b5ba8b81671c0c1eaec21f
```

---

## 6. OPEN Transition Debt / deferred scope

### 6.1 Gate-derived Transition Debt

ENH-E5 closeoutを阻害するOPEN Transition Debt:

```text
NONE
```

G00-G05の全Gateはfinal `PASS / PROMOTION_ALLOWED`である。

### 6.2 Preflight D3 / FUTURE items

preflightでD3 / FUTUREへ送った未実装・部分実装Requirement/Designは、Gate failure由来のTransition Debtではない。

これらは次をauthorityとして継続管理する。

```text
00_enhance_background/90_technical_debt_and_future_enhancements.md
```

D3/FUTURE itemが残っていることを理由にENH-E5をreopenしない。

### 6.3 Closeout follow-up

ENH-E5 closeoutで認識した以下の事項は、ENH-E5のGate acceptance blockerではなく、後続enhancement / maintenanceで扱う。

1. 3 Family tab observable UIの再現・原因確定・bugfix
2. G05 full-suite observationに残る5 failuresの整理
3. Agentic Workflow Template v3_1の次回enhancementでのeffectiveness validation
4. Browser E2E policyを具体runnerへinstantiationした際のeffectiveness validation

詳細は`00_enhance_background/90_technical_debt_and_future_enhancements.md`を参照する。

---

## 7. Preflight / execution lifecycle state

ENH-E5のpreflightおよびGate execution lifecycleは完了している。

- planning baseline established: `COMPLETE`
- requirements/design convergence: `COMPLETE`
- preflight / contract freeze: `COMPLETE`
- G00 execution / verification: `PASS / PROMOTION_ALLOWED`
- G01 execution / verification: `PASS / PROMOTION_ALLOWED`
- G02 execution / verification: `PASS / PROMOTION_ALLOWED`
- G03 execution / verification: `PASS / PROMOTION_ALLOWED`
- G04 execution / verification: `PASS / PROMOTION_ALLOWED`
- G05 execution / verification: `PASS / PROMOTION_ALLOWED`
- enhancement-level state promotion: `CLOSED`

個別preflight commandのhistorical evidenceは既存preflight / Gate evidenceをauthorityとし、本Control Sheetへ再構成しない。

---

## 8. Active orchestration pointer

```text
NONE — ENH-E5 CLOSED
```

ENH-E5に対する通常Coding Agent、Work Package Agent、Candidate Assembly Agent、FAIL Rework Agent、Independent Test Agentの追加実行は予定しない。

後続事項を扱う場合は、ENH-E5を再開せず、別enhancement / maintenance workflowとして新しいscope、baseline、contract、evidence chainを開始する。

---

## 9. Evidence index

### 9.1 G00

- Final Trial: `Trial01`
- Fixed Candidate: `6e8eb6736a0d72403f5c6ca1a019e8f562d4533c`
- Gate Decision: `30_test_report/G00/Trial01/E5-G00_01__999_gate_decision.md`
- Decision: `PASS`
- Promotion: `PROMOTION_ALLOWED`

### 9.2 G01

- Final Trial: `Trial04`
- Fixed Candidate: `1fb9e0f3bd8850782433a2475900fce45d420cd4`
- Gate Decision: `30_test_report/G01/Trial04/E5-G01_04__999_gate_decision.md`
- Decision: `PASS`
- Promotion: `PROMOTION_ALLOWED`

### 9.3 G02

- Final Trial: `Trial01`
- Fixed Candidate: `b5fe825c046714c1865c0e6cc1733851aaca8ae2`
- Gate Decision: `30_test_report/G02/Trial01/E5-G02_01__999_gate_decision.md`
- Decision: `PASS`
- Promotion: `PROMOTION_ALLOWED`

### 9.4 G03

- Final Trial: `Trial01`
- Fixed Candidate: `bb4afd2b94e724e64d60945bc961cea044acacef`
- Gate Decision: `30_test_report/G03/Trial01/E5-G03_01__999_gate_decision.md`
- Decision: `PASS`
- Promotion: `PROMOTION_ALLOWED`

### 9.5 G04

- Final Trial: `Trial02`
- Fixed Candidate: `564df2da67efa43c4455718b9b3d81f6d3e98c61`
- Test Evidence Commit: `92afd1802e52db813b4fc4c7d6e1c7d2280b6a7`
- Gate Decision: `30_test_report/G04/Trial02/E5-G04_02__999_gate_decision.md`
- Decision: `PASS`
- Promotion: `PROMOTION_ALLOWED`
- canonical Chromium regression: `PASS`

### 9.6 G05

- Final Trial: `Trial01`
- Fixed Candidate: `5cf0caf515b8e57fc114eabea0efd9acffe23e62`
- Test Evidence Commit: `3f7da9d87acdf24fe4b5ba8b81671c0c1eaec21f`
- Gate Decision: `30_test_report/G05/Trial01/E5-G05_01__999_gate_decision.md`
- Decision: `PASS`
- Promotion: `PROMOTION_ALLOWED`

### 9.7 G05 full-suite observation boundary

G05 Independent Testでrepository-wide pytestは次を観測した。

```text
5 failed, 314 passed, 33 skipped
```

Gate Decisionでは以下のように分類された。

- 4件: G05で必須化された`Idempotency-Key`を送らない旧test/caller
- 1件: frozen G05 scope外の`ScientificStatus` contract

詳細:

```text
30_test_report/G05/Trial01/E5-G05_01__004_full_suite_observation.md
```

これらはfrozen G05 mandatory AC / protected regression違反とは判定されず、G05は`PASS / PROMOTION_ALLOWED`である。

本観測は後続maintenance itemとして保持し、ENH-E5をreopenしない。

---

## 10. Closeout decision

Human ownerは、G00-G05のfinal Gate Decisionとpromotion eligibilityに基づき、ENH-E5を以下の状態へpromotionする。

```text
ENH-E5
  G00 PASS
  G01 PASS
  G02 PASS
  G03 PASS
  G04 PASS
  G05 PASS
      ↓
  VERIFIED THROUGH G05
      ↓
  FOLLOW-UP ITEMS SEPARATED
      ↓
  CLOSED
```

Closeout時の更新はdocumentation-onlyとする。

closeoutのために以下を変更してはならない。

- production source
- frontend source
- automated test implementation
- migration
- dependency
- freeze済み06/Pxx/07
- historical implementation report
- historical independent test evidence

---

## 11. Update log

- 2026-08-13T14:24:45+09:00: G05 / Trial01 final `PASS / PROMOTION_ALLOWED`を受け、G00-G05全Gateのverified stateをpromotion。Final Verified Implementation Candidateを`5cf0caf515b8e57fc114eabea0efd9acffe23e62`へ固定し、ENH-E5を`CLOSED`へ移行。closeout follow-upはENH-E5をreopenせず別enhancement / maintenanceへ分離。
- 2026-08-11T16:21:58+09:00: 既存実装整合性監査を完了。Resource field、canonicalization/schema registry、auth/role、Worker lease、planner shape、API route semantics、Research Context relation/usage、Lineage authority、CLI/package boundaryをPlanning baseline sourceへ突合し、設計側の乖離を修正。監査判定は`PASS_WITH_CORRECTIONS_APPLIED`。
- 2026-08-11T16:10:52+09:00: 既存実装・設計整合性レビューを実施。unchanged contractのsource-of-truthをPlanning baseline current codeへ戻し、Resource field、planner、Worker lease、CLI/API、Lineage、package map等の設計乖離を修正。Gate PASS promotionはまだない。
- 2026-08-11T15:17:11+09:00: API/詳細設計の自己完結性レビューを反映。AnalysisFamily、Result/Annotation/Artifact、Worker lease、StageExecution、Predictive contract等を本文内へ展開し、存在しないpublic claim/event contract前提を除去。Gate PASS promotionはまだない。
- 2026-08-11T14:39:45+09:00: review feedbackを反映した次版planning stateへ更新。Gate PASS promotionはまだない。

---

## Execution Agentへの参照禁止

Current State Control Sheetはoperator/state control artifactであり、通常のCoding/Test Agentへnormative inputとして読ませない。

protected Gate identityが必要な場合、freeze担当者が06/07/Pxx本文へ具体値を転記する。

ENH-E5は`CLOSED`であるため、本書のcloseout follow-up記述を既存ENH-E5 Gate contractの追加normative requirementとして解釈してはならない。
