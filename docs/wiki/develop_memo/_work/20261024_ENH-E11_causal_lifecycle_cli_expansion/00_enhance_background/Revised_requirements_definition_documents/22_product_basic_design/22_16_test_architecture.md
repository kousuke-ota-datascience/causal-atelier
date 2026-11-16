# 22_16_test_architecture

**Status:** `BD01_E11_BASIC_DESIGN_REVISED / OWNER_POLICY_APPROVED / INDEPENDENT_REVIEW_PENDING`. Original chapter and source provenance retained; DD physical coverage remains partial.  
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



### 19.1. Local Scientific CLIの検証境界

| Layer | E11 added tests / gate |
|---|---|
| Static architecture | Local CLI→Web/API/DB/Worker逆依存禁止、Domain→optional backend逆依存禁止、old v2 schema reader保護 |
| Unit/contract | Graph endpoint fidelity、Estimand差、nonidentification fail closed、backend unavailable、Result state axes、confidence set topology |
| Local artifact integration | traversal/symlink、publish partial failure、readback/checksum、crash-recovery、row-level privacy、old Run compatibility |
| Environment | 5 isolated profiles＋conditional RD、lock/extra/API/version、core startup、old E9/v2 regression |
| Independent science | 41 Method/68 Scope/10 UC、DGP/NEG/REF/AC/ENV-AC、FWER=.05、K/R/MC／Coverage／Monte Carlo error |
| Delivery / legal | Artifact・Recipient・License/SBOMの実名審査。Science/Env PASSとは別 |

`PLAN:G01〜G10`は開発Workstreamであり正式Gate06/07ではない。**本BDの文書監査PASSが実行テストPASSを意味しない**。[Review](../bd01_review/90_architecture_consistency_review.md)。

実装が継続的に充足すべき検証契約として、Local CLIとProductの依存方向、入力版Dispatch、Method適格性、typed inference、成果物の部分公開拒否、環境・Privacy回帰を含む。Method固有のScience受入は設計検証とは独立する。

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
