# 22_16_test_architecture

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `87196f2f03a7f3367724bc05fb254d1a4d98109e`.

---

## 19. Test Architecture

Current design concernを次のtest layerへtraceする。

- domain invariant / typed filter / scientific guard → unit/domain test
- persistence / StageAttempt seed / concurrency / idempotency / authorization / lineage → integration test
- route/header/error/response/authorization → API contract test
- Navigation/deep link/history/async state/accessibility → frontend/browser test
- Navigation→runtime import prohibition / optional future dependency prohibition → architecture/static test
- Planner golden / Plan DAG / Runner contract / worker lifecycle → workflow regression
- CLI / library direct execution → headless regression
- Predictive existing setting/spec parity → compatibility regression
- Causal scientific benchmark / Predictive leakage/split/subgroup → scientific test
- Family横断browser E2E

`DEFERRED` concern（general AuditLog、retention、object storage、hard limits、production auth hardening、cross-store compensation等）のtest targetをcurrent mandatory acceptanceへ混ぜない。


## 98. RD-04：要件由来の基本設計制約

**Status:** `RD04_DESIGN_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。旧要件の具体設計制約を担当領域へ移管。実装検証・ADR承認済みを意味しない。

### 98.1. NFR-015（SPLIT）

- 元の設計情報を含む要件：Domain、Planner、Runner、API、Worker、UI、scientific benchmarkを分離testできる
- 改訂後RD／Legacy Trace：Domain・実行・API・UI・科学計算を個別に検証できる
- ID：`NFR-015`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [逐条記録](../96_rd04_nfr_ar_application_review.md)

### 98.2. NFR-024（SPLIT）

- 元の設計情報を含む要件：Navigation descriptor、route、renderer binding、runtime independenceをunit/integration/E2Eで分離検証できる
- 改訂後RD／Legacy Trace：画面構成・URL復元・表示・分析実行独立性を個別に検証できる
- ID：`NFR-024`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [逐条記録](../96_rd04_nfr_ar_application_review.md)
