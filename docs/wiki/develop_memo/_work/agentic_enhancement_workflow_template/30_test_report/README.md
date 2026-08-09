# 30_test_report — Gate-local Test / Audit Evidence Specification v2

## 0. Purpose

Test / Audit Agentが実際に行った検証とGate判定を、後から独立に追跡・追試・監査できる粒度で保存する。

```text
test item report
  = 1 test itemの実行事実・結果・再現手順

gate decision report
  = 当該Gate / Trialのtest item evidenceを集約した最終判定
```

## 1. Directory and naming

```text
30_test_report/{{GATE_ID}}/
{{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_ID}}_{{TEST_ITEM_ID}}_<name>.md
{{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_ID}}_999_gate_decision.md
```

## 2. Common evidence rules

- tested commit full SHA — MUST
- exact copy-paste executable command — MUST
- exit code — MUST when command executed
- raw relevant output — MUST
- Facts / Interpretation separation — MUST
- AC mapping — MUST
- Test Agent source mutation = `NONE` — MUST for normal PASS evidence
- timestamp = timezone付きISO 8601 — MUST

## 3. PASS / FAIL / BLOCKED

### PASS
Required AC / regression / TD auditが必要evidence付きで成立。

### FAIL
test実行可能でproduct / implementationがMUST contractを満たさない。

### BLOCKED
prerequisite、environment、contract ambiguity等で妥当なproduct判定不能。

## 4. Protected passed-Gate regression

後続Gateが以前のprotected semanticsへ触れる場合、該当regression itemをMUSTとする。
regression failureはactive GateをFAILにできる。

## 5. Transition Debt

TDが存在する場合、scope expansion / exit criterion / authority overlapを必要に応じてTest Itemとして監査する。

## 6. Gate Decision promotion semantics

final PASS Gate DecisionだけがCurrent State Control Sheetのverified-state promotion triggerとなる。
FAIL / BLOCKEDはpromotion triggerではない。
