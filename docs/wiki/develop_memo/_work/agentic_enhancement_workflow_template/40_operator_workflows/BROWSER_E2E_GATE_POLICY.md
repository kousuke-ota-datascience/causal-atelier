# Browser E2E Gate Policy — critical journey / environment / evidence 共通方針

**Document class:** Authoring / Operational Policy  
**Self-containment:** MUST — Browser E2E を Gate blocking verification として設計・実行・診断する共通原則を本書だけで理解できること。

> **Authority boundary:** 本書は template authoring / operational policy であり、個別 Gate の Acceptance Criteria authority ではない。実行時の normative verification authority は freeze 済み `07` である。Browser E2E を採用する Gate では、本書の必要事項を Gate 固有の `06 / 07` へ具体化して freeze する。

## 1. Purpose

Browser E2E は廃止しない。ただし、Gate blocking Browser E2E の責務を次へ限定する。

> 少数の critical user journey が、real browser から frontend / API / persistence / worker 等の実システム境界を跨いで成立することを確認する。

Browser E2E を detailed specification correctness の一次証明にはしない。

## 2. Test layer responsibility

原則として requirement / Acceptance Criteria ごとに最も deterministic で failure localization しやすい test layer を割り当てる。

```text
Unit / domain tests
    = domain rule / validation / boundary behavior

API integration tests
    = request / response / persistence contract

Frontend contract tests
    = caller payload / rendering / state transition contract

Browser E2E
    = critical user journey の real cross-layer connectivity
```

詳細 correctness は lower-level deterministic tests で証明し、Browser E2E は real-system connectivity の最終確認に使う。

## 3. Gate blocking Browser E2E selection

Gate blocking として維持する canonical Browser E2E suite 全体は、**原則 3〜5 本程度**の critical journey に限定する。各 Gate の `07` は、その canonical suite から当該 Gate の Acceptance Criteria に relevant な subset だけを選択する。

Browser surface がない Gate は 0 本でよい。各 Gate に 3〜5 本ずつ Browser E2E を追加して suite を増殖させない。

各 Gate blocking Browser E2E item は `07` 内で最低限以下を明示する。

- journey name / Test Item ID
- covers Acceptance Criteria
- critical である理由
- cross-layer boundary
- canonical command / method
- environment bootstrap / teardown authority
- semantic synchronization point
- observable assertion
- failure evidence requirements
- PASS / FAIL / BLOCKED semantics

canonical Gate blocking suite 全体が5本を超える場合、lower-level testでは代替できない理由と、critical journeyとして残す理由をauthoring recordへ記載する。

## 4. Browser E2E から原則外す詳細検証

以下は原則として Browser E2E の主責務にしない。

- validation operator × type matrix
- boundary value validation
- error taxonomy 全件
- warning taxonomy 全件
- schema compatibility 詳細
- family / mode 全分岐
- navigation stage 全組合せ
- lineage metadata 全 field
- invalid query 全パターン
- serialization edge case
- scientific / domain prerequisite 全パターン

必要な correctness proof は unit / domain / API integration / frontend contract test 等へ配置する。

## 5. Hermetic environment requirement

Gate blocking Browser E2E は、過去の手動操作や残存 runtime state に依存してはならない。

canonical Browser E2E command / workflow は、必要に応じて次を自己完結的に成立させる。

```text
clean project namespace
↓
current-source image build / recreate
↓
database startup
↓
migration
↓
API startup
↓
worker startup
↓
frontend startup
↓
fixture setup
↓
Browser E2E
↓
evidence collection
↓
cleanup
```

以下を暗黙 prerequisite にしない。

- manual `docker compose up`
- previous worker state
- stale / previous image
- previous database fixture
- previous Browser E2E artifact

Browser E2E 実行前に必要な prerequisite / service identity / current-source build identity は `40_operator_workflows/preflight/` または canonical command 自身で観測可能にする。

## 6. Synchronization principle

Browser E2E の synchronization authority は semantic / observable state とする。

原則として以下だけに依存しない。

- `sleep()`
- fixed timeout only
- URL change only
- element が即時出現するという仮定

例:

```text
canonical URL reached
AND
workspace / data refresh completed
```

```text
execution submitted
AND
terminal execution status observed
```

async refresh / rerender により form state が再構築される場合、操作可能性だけでなく必要な ready state を確認する。

## 7. Assertion principle

Browser E2E は implementation detail ではなく observable behavior を assertion authority とする。

避けるもの:

- legacy URL alias の exact expectation
- internal DOM structure
- internal function name
- fixed timing

優先するもの:

- canonical route
- expected result visible
- execution terminal success
- draft / artifact creation observed
- persistence / lineage observable

## 8. Failure evidence standard

Browser E2E が FAIL / BLOCKED になった場合、利用可能な範囲で最低限以下を evidence として保存する。

- Playwright trace (`trace.zip` 等)
- failure screenshot
- video
- browser console
- page errors
- relevant network request / response
  - URL
  - method
  - request body
  - response status
  - response body
- API logs
- worker logs
- Compose / service state
- Fixed Trial Candidate SHA
- exact test command
- timestamp
- synchronization point / assertion that failed

credential / token / secret / sensitive fixture value は evidence 保存前に redact する。

HTTP status 単体を root cause と決めつけない。intentional negative test の response と actual failing assertion を区別する。

## 9. Failure classification

Browser E2E failure は、evidence に基づき可能な限り以下へ分類する。

```text
PRODUCT_INTEGRATION_DEFECT
TEST_IMPLEMENTATION_DEFECT
TEST_ORCHESTRATION_DEFECT
TEST_ENVIRONMENT_DEFECT
UNKNOWN
```

分類は diagnosis であり、それ自体が Gate Decision authority ではない。

- `PRODUCT_INTEGRATION_DEFECT` で有効な 07 Acceptance Criteria 違反が verified された場合: `FAIL` 候補
- `TEST_IMPLEMENTATION_DEFECT`: product correctness を判定できない場合は原則 `BLOCKED`
- `TEST_ORCHESTRATION_DEFECT`: product correctness を判定できない場合は原則 `BLOCKED`
- `TEST_ENVIRONMENT_DEFECT`: product correctness を判定できない場合は原則 `BLOCKED`
- `UNKNOWN`: product correctness を判定できない限り `BLOCKED`

harness / orchestration / environment defect を product implementation FAIL として扱わない。

## 10. Coding-side self-verification rule

Coding Agent / Work Package Coding Agent が Browser E2E failure を観測した場合、未検証仮説を root cause として即修正しない。

修正前に最低限以下を確定する。

```text
failure point
actual observable state
expected state
candidate cause
supporting evidence
```

current coding contract scope 外の test implementation / orchestration / environment defect が原因で verification を完遂できない場合、scope 外修正で回避せず適切な `BLOCKED_*` として停止する。

## 11. Candidate Assembly rule

Candidate Assembly が Gate-wide coding-side verification として Browser E2E を実行する場合も、本 policy の critical-journey / hermetic-environment / evidence-first 原則を適用する。

Candidate Assembly Agent は Browser E2E failure をその場で production / automated test / orchestration 修正してはならない。必要な verification が成立しない場合は evidence を残して `BLOCKED_INTEGRATION_VERIFICATION` 等の適切な blocker で停止する。

## 12. Independent Test Agent rule

Independent Test Agent は frozen `07` に定義された Browser E2E Test Item だけを Gate blocking test として実行する。Test Agent 自身が詳細仕様証明のために Browser E2E scope を拡張しない。

Browser E2E failure 時は failure evidence と classification を Test Item Report に記録する。production code / automated test code / Browser test implementation / orchestration を Test Agent 自身で修正しない。

## 13. formal FAIL remediation rule

Browser E2E を trigger とした formal FAIL remediation は、evidence が product / contract behavior の違反を支持する場合のみ開始する。

failure evidence が `TEST_IMPLEMENTATION_DEFECT` / `TEST_ORCHESTRATION_DEFECT` / `TEST_ENVIRONMENT_DEFECT` / `UNKNOWN` のままで product violation が verified されていない場合、production remediation へ進めない。

FAIL Rework Coding Agent は、Browser E2E failure の未検証仮説を根拠に speculative fix を繰り返さない。

## 14. Frozen contract / non-retroactive rule

本 policy の追加・更新は、**適用時点ですでに freeze 済み、execution 開始済み、または完了済みの contract / Trial / enhancement** を silent rewrite する根拠にならない。

既に成立している Browser E2E requirement を execution 途中または事後に削除・緩和し、PASS 条件を変更してはならない。

本 policy は原則として、**本 policy を取り込んだうえで新規 authoring / re-authoring され、その後 freeze される contract** から適用する。適用開始前に成立済みの frozen contract へは遡及適用しない。

既存 frozen contract 自体に defect がある場合のみ、既存 workflow の explicit amendment / re-baseline rule に従う。これは本 policy の遡及適用ではなく、明示的な contract amendment として扱う。

## 15. Authoring checklist

- [ ] requirement / AC ごとに primary proof layer を選んだ
- [ ] Browser E2E を detailed correctness の一次証明にしていない
- [ ] Gate blocking Browser E2E は critical journey に限定した
- [ ] canonical Gate blocking Browser E2E suite 全体を原則3〜5本程度に収め、各Gateはrelevant subsetだけを選択した
- [ ] canonical command が stale service / image / DB state に依存しない
- [ ] synchronization が semantic / observable state に基づく
- [ ] assertion が observable behavior に基づく
- [ ] failure evidence collection を 07 に具体化した
- [ ] failure classification と FAIL / BLOCKED の境界を 07 に具体化した
- [ ] 適用開始前に成立済みの frozen contract へ本 policy を遡及適用していない
