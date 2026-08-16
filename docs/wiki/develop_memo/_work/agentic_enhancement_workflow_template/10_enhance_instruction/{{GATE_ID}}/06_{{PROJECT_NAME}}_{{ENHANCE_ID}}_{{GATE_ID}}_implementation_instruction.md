# {{PROJECT_NAME}} {{ENHANCE_ID}} {{GATE_ID}} 実装指示書 — Gate Coding Contract

**Document class:** Primary Execution Contract  
**Self-containment:** MUST — Coding AgentがGate implementation semanticsを理解するためのnormative rulesを本書内に保持する。

- Project: {{PROJECT_NAME}}
- Enhancement: {{ENHANCE_ID}}
- Active Gate: {{GATE_ID}}
- Branch: {{BRANCH}}
- Baseline: {{BASELINE_FULL_SHA}}
- Contract status: FROZEN
- Execution Mode: SINGLE_EXECUTION / WORK_PACKAGE
- canonical evidence-derived state model: {{CONTROL_SHEET_PATH}}

## 1. Gate definition / acceptance claim

### Gate objective
{{GATE_OBJECTIVE}}

### Contract claim established by PASS
このGateがfinal PASSしたとき、後続工程は以下を成立済みcontractとして依存してよい。

{{DOWNSTREAM_USABLE_RESULT_AFTER_PASS}}

### Why this is one Gate
{{WHY_THIS_IS_ONE_ACCEPTANCE_BOUNDARY}}

実装難易度やAgent execution sizeをGate境界理由として使用しない。

## 2. Effective implementation context

本Gateの実装判断に必要なcurrent semantics / assumptionsを、外部文書を読まなくても理解できる粒度で記載する。

{{EFFECTIVE_CURRENT_CONTEXT}}

外部requirement / design / Control Sheetはfact source / provenanceとして参照してよいが、本Gateのimplementation ruleを外部へ委譲しない。

## 3. Execution Mode decision

- Selected: SINGLE_EXECUTION / WORK_PACKAGE
- Reason: {{EXECUTION_MODE_REASON}}
- P00 Plan (traceability / orchestration): {{P00_PATH_OR_NA}}

Work Package ModeであってもGate semantic contractは分割されない。

## 4. Required implementation semantics
{{REQUIRED_IMPLEMENTATION_SEMANTICS}}

## 5. Allowed scope
{{ALLOWED_SCOPE}}

## 6. Explicitly prohibited scope
{{PROHIBITED_SCOPE}}

## 7. Protected passed-Gate contracts

| Gate | Protected semantic | Allowed interaction | Mandatory regression |
|---|---|---|---|
| {{PREVIOUS_GATE_OR_NONE}} | {{SEMANTIC}} | {{INTERACTION}} | {{REGRESSION}} |

## 8. Transition Debt

| TD ID | Required action in this Gate | Exit criterion / scope guard |
|---|---|---|
| {{TD_ID_OR_NONE}} | introduce / preserve / close / NONE | {{CRITERION}} |

## 9. Schema / migration / API / runtime policy
{{POLICY_OR_NA}}

## 10. Automated test obligations
{{TEST_OBLIGATIONS}}

Test obligationを設計する際は、requirementごとに最もdeterministicでfailure localizationしやすいtest layerを割り当てる。Browser E2Eをdetailed correctnessの一次証明にしない。Browser E2Eが必要な場合は、real browserからsystem boundaryを跨ぐcritical user journeyに限定し、詳細validation / boundary / taxonomy / schema分岐等は原則lower-level testへ配置する。

Coding-side Browser E2Eを要求する場合、canonical command、hermetic environment prerequisite、semantic synchronization point、observable assertionを本書またはassigned Pxxへ具体化する。Browser E2E failureを観測した場合は、未検証仮説をroot causeとして即修正せず、failure point / actual observable state / expected state / supporting evidenceを確定してからscope内修正の可否を判断する。

## 11. Candidate Assembly requirement

Before READY_FOR_TEST:

- all required execution units complete
- integration / Gate-wide self-check complete
- protected passed-Gate coding-side regression complete
- unresolved candidate-affecting change = NONE
- Fixed Trial Candidate SHA fixed
- Implementation Completion Report created

Package checkpoint aloneをFixed Trial Candidateと扱わない。

## 12. Coding Agent prohibited work

- Gate Decision
- Acceptance Criteria変更
- test回避のための07変更
- passed-Gate semanticの無断変更
- next Gate先行実装
- package scope外の便乗変更

## 13. Required outputs

### SINGLE_EXECUTION
- implementation status report
- implementation completion report
- Gate-local implementation detail update

### WORK_PACKAGE
各package:
- package execution status report
- implementation checkpoint report
- checkpoint SHA

Trial completion時:
- Fixed Trial Candidate SHA
- implementation completion report
- Gate-local implementation detail update

## 14. External reference policy

以下は参照してよい。

- source / test / migration / runtime target
- previous PASS evidence
- approved requirement / design provenance
- canonical evidence-derived state modelのverified fact

参照先は本書のnormative implementation semanticsを変更・補完するauthorityとして扱わない。本書とverified factが衝突し実装判断不能な場合は推測せず`BLOCKED_CONTRACT_AMBIGUITY`として停止する。

## 15. Stop condition

Coding sideは`READY_FOR_TEST`または明示的`BLOCKED_*`で停止する。Gate PASSを宣言しない。
