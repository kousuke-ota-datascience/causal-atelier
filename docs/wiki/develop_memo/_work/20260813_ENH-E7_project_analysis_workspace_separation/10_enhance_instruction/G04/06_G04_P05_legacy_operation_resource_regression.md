# ENH-E7 G04 P05 — Legacy / Operation / Resource Regression

**文書種別:** Primary Execution Contract
**Self-containment:** MUST  
**Information isolation:** MUST  
**Reporting contract:** SELF_CONTAINED
**Gate:** G04
**初回発行Trial:** 01
**Package:** P05
**Depends on:** P04
**Status at issuance:** FROZEN

## 1. 目的

legacy analytical URL、resource route、existing Causal/Exploratory/Predictive operation semanticsをG03/G04後も維持する。

## 2. このpackageに適用するconstraint

- G03 final PASS surface architectureをblocking protected contractとする。
- G01/G02 canonical route/domain/analysis semanticsを保護する。
- backend/API/persistence semanticsを変更しない。
- package completionはGate PASSではない。
- 本PxxだけがCoding Agentのnormative workflow implementation contractである。
- Gate 06 / 07 / P00 / other Pxxを仕様補完目的で読まない。
- source / tests / config / migrationsはimplementation substrateとして調査可能。
- source factと本Pxxが矛盾し、contractをsilent reinterpretしなければ実装できない場合は停止する。
- 未承認backend/API/persistence semantic changeが必要なら停止する。

## 3. In scope

- legacy analytical URL normalization
- resource route compatibility
- Causal mapped Stage operability
- Exploratory fixed mapping/semantics
- Predictive presentation/execution semantics

## 4. Required invariants

以下は実装方法の例ではなく、このpackageが成立させるProduct / architecture invariantである。

- legacy analytical URLはcanonical Analysis routeへnormalizeする。
- existing resource route semanticsを削除しない。
- Causal execution semanticsを変更しない。
- Exploratory Data Qualityはread-only availabilityであり`DATA_QUALITY` executionを作らない。
- `TIME_TREND`はvalid groupingと互換なaggregationを要求するexisting operationであり、`GROUP_SUMMARY_RESULT`を返す。時刻型、時間順序、トレンドモデルを追加しない。
- `CHART`は`CHART_RESULT`と永続`CHART_SPECIFICATION`（Vega-Lite JSON）artifactを生成するexisting operationであり、表示専用stateへ置換しない。
- Predictive Stageはpresentation/navigation viewであり新execution stepを作らない。

## 5. Explicitly out of scope

- backend semantic redesign。
- new taxonomy。
- unrelated operation bugfix。
- Acceptance Criteria変更。
- next package実装。

## 6. Entry criteria

- current checkoutが`feature/ariadne_mvp_e7`。
- dependency `P04` が満たされている。
- `G04/P05/Trial<TRIAL_NO>` Agent Execution ReadinessがPASS。
- preflightがArchitecture / Gate contract readinessをPASSしている。
- in-scope behaviorを曖昧にする未解決source factがない。

確認不能なら`PACKAGE_BLOCKED`として停止する。

## 7. Required implementation

1. existing operation mapping testsをG03/G04 DOMに合わせて更新する。
2. legacy/resource route behaviorを直接検証する。
3. UI移設を理由にoperation semanticsをsubstituteしない。
4. Data Qualityがexecution/previewを発行せず既存Profile resultだけをread-only表示すること、TIME_TRENDとCHARTが上記の既存result/artifact semanticsを保つことを確認する。

## 8. Required verification predicates

focused testは単なるelement ID / label文字列の存在確認だけで完了としてはならない。以下のpredicateを直接検査する。

- legacy URL fixtureがcanonical routeへ正規化。
- resource route fixtureが既存resource semanticsを維持。
- Causal/Exploratory/Predictive protected tests PASS。
- Data Qualityに`DATA_QUALITY` operation/API executionがなく、TIME_TRENDは`GROUP_SUMMARY_RESULT`、CHARTは`CHART_RESULT`と`CHART_SPECIFICATION` artifactを維持。
- 新backend/API/persistence diffなし。

## 9. Focused verification

| Check | Command / method | Required result |
|---|---|---|
| focused product test | `uv run pytest -q tests/product/test_enh_e7_g04_p05_legacy_operation_resource_regression.py` | PASS |
| nearby regression | touched responsibilityをcoverするrepository test | PASS |
| source/diff audit | DOM ownership / visibility / event binding / dead codeを含むdiff確認 | out-of-scope semantic changeなし |

## 10. Protected contract

- G03 Projects / Project Management / Analysis surface separation。
- G03 Family horizontal / Stage vertical / obsolete shell absence。
- existing Project/domain/analysis operation semantics。
- G01/G02のrequirements / acceptance semanticsを満たしていないcurrent presentation implementation自体はprotected implementationではない。
- current non-conforming global shellを互換性維持の名目で残してはならない。

## 11. Package handoff artifact contract

本packageのCoding Agentは、他のworkflow artifactを読まずに以下1ファイルを作成する。

### 11.1 Canonical保存先 / filename

`20_implementation_reports/G04/Trial<TRIAL_NO>/packages/ENH-E7_G04_P05_Trial<TRIAL_NO>_package_execution_status.md`

directoryが存在しない場合は作成してよい。

### 11.2 必須内容

```text
# ENH-E7 G04 P05 Package Execution Status

- Enhancement: ENH-E7
- Gate: G04
- Trial: <TRIAL_NO>
- Package: P05
- State: PACKAGE_COMPLETE | PACKAGE_BLOCKED
- Branch: feature/ariadne_mvp_e7
- Implementation HEAD full SHA: <40-hex SHA or NOT_RECORDED>

## 実施したscope
## Changed files / responsibility
## Required invariant conclusion
## Focused verification
  - exact command / method
  - exit code / result
## Remaining / blocker
## Scope guard確認
```

## 12. Stop condition

`PACKAGE_COMPLETE`または明示的`PACKAGE_BLOCKED`で停止する。Gate PASS/FAILを宣言しない。
