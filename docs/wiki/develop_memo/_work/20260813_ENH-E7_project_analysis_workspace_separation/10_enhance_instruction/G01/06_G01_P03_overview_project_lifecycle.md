# ENH-E7 G01 P03 — Overview / Project Lifecycle

**文書種別:** Primary Execution Contract  
**Self-containment:** MUST
**Information isolation:** MUST
**Reporting contract:** SELF_CONTAINED  
**Gate:** G01  
**初回発行Trial:** 01  
**Package:** P03  
**Depends on:** P01,P02  

## 1. 目的

selected Projectのmetadata / lifecycle responsibilityをOverviewへ移設する。

## 2. このpackageに適用するconstraint

- Project ManagementとAnalysis Workspaceは異なるnavigation scopeである。
- existing domain/execution semanticsを保護する。
- ENH-E6 canonical Analysis route / Family / Stage semanticsをregressionさせない。
- package completionはGate PASSではない。
- **本PxxだけがこのCoding executionのnormative workflow implementation contractである。**
- parent 06 / 07 / P00 / other PxxはHuman traceability用であり、仕様補完目的で読まない。
- source / tests / config / migrationsはimplementation substrateとして調査可能。
- 未承認backend/API/persistence semantic changeが必要なら停止する。

## 3. In scope

- Project metadata / identity / status
- Project Archive
- Overviewをselected Project default surfaceとする

## 4. Explicitly out of scope

- Dataset registration / Analysis View lifecycleをOverviewへ混在させない。

加えて以下はout of scope。
- Acceptance Criteria変更
- unrelated cleanup / refactoring
- next package実装

## 5. Entry criteria

- current checkoutが`feature/ariadne_mvp_e7`。
- `G01/P03/Trial01`のAgent Execution ReadinessがPASS。
- dependency `P01,P02` が満たされている。
- preflightがArchitecture / Gate contract readinessをPASSしている。
- in-scope behaviorを曖昧にする未解決source factがない。

確認不能なら`PACKAGE_BLOCKED`として停止する。

## 6. Required implementation

1. §3 responsibilityを特定する範囲でcurrent source/testsを調査する。
2. §2/§4を維持して§3 behaviorを実装する。
3. repository conventionに従ってfocused testを追加・更新する。
4. substitute backend semanticsを作らない。
5. source factとcontractが矛盾する場合はsilent reinterpretせず停止する。

## 7. Focused verification

| Check | Command / method | Required result |
|---|---|---|
| focused product test | `uv run pytest -q tests/product/test_enh_e7_g01_p03_overview_project_lifecycle.py` | PASS |
| nearby regression | touched responsibilityをcoverするrepository test | PASS |
| source/diff audit | ownership/navigationを含むdiff確認 | out-of-scope semantic changeなし |

## 8. Protected contract

- Protected upstream: ENH-E6 G01 PASS candidate `575cdd139aea09d4f19b46ab6a6d38545f645c71` が確立したcanonical Analysis Family/Stage navigation / transition semantics。
- intentional open Transition Debtは導入しない。
- legacy URL compatibilityを削除しない。

## 9. Package handoff artifact contract

本packageのCoding Agentは、**他のworkflow artifactを読まずに**以下1ファイルを作成する。

`<TRIAL_NO>` はoperator promptから渡されたruntime値である。

### 9.1 Canonical保存先 / filename

```text
20_implementation_reports/G01/Trial<TRIAL_NO>/packages/
ENH-E7_G01_P03_Trial<TRIAL_NO>_package_execution_status.md
```

directoryが存在しない場合は作成してよい。

### 9.2 必須内容

最低限、以下を本文内に持つ。

```text
# ENH-E7 G01 P03 Package Execution Status

- Enhancement: ENH-E7
- Gate: G01
- Trial: <TRIAL_NO>
- Package: P03
- State: PACKAGE_COMPLETE | PACKAGE_BLOCKED
- Branch: feature/ariadne_mvp_e7
- Implementation HEAD full SHA: <40-hex SHA or NOT_RECORDED>

## 実施したscope
## Changed files / responsibility
## Focused verification
  - exact command / method
  - exit code / result
## Remaining / blocker
## Scope guard確認
  - next package workなし
  - Gate acceptance decisionなし
  - prohibited workflow-document dependencyなし
## Facts
## Interpretation
```

`Implementation HEAD full SHA` はtraceability用であり、package completionを成立させるSHA lockではない。

### 9.3 Package handoff semantics

`PACKAGE_COMPLETE` は、assigned scope実装、required focused verification PASS、unresolved blockerなし、本status report作成済みを意味する。

Work PackageはGate-level quality boundaryではないため、package単位のFixed Candidate SHA、implementation checkpoint report、Gate級acceptanceは要求しない。

Gate-level candidate identityは全required package完了後のCandidate Assemblyで固定する。

## 10. Package completion criteria

Overview ownership/lifecycle regressionがPASSする。

加えてfocused verification完了、unresolved blockerなし、package execution status report作成済みであること。

## 11. External reference policy

Coding Agentはsource/test/runtime factを調査してよい。
Gate 06 / Gate 07 / P00 / other Pxx / 00 / 20 / 30をpackage specification補完目的で読まない。

本Pxxが不十分またはverified source factと矛盾する場合は
`PACKAGE_BLOCKED_CONTRACT_AMBIGUITY`として停止する。

## 12. Stop rule

- scope完了 → `PACKAGE_COMPLETE`
- 安全に継続不能 → `PACKAGE_BLOCKED`
- Gate PASS/FAILを宣言しない
- 別packageへ自動継続しない
