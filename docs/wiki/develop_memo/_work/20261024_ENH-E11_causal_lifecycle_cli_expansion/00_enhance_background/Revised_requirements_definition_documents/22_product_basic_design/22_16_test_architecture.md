# 22_16_test_architecture


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
| Delivery / legal | 実際の顧客配布前に対象Dependency/配布方式をOwner・法務が手動審査。内部科学CLIのGate実行にはSBOM生成／受領者別認可管理を追加しない |

`PLAN:G01〜G10`は暫定的な計画Workstream名であり、そのままではEnhancement Workflowの正式受入Gateではない。正式Gateはsemantic Acceptance Contractとして境界を確定し、各Gateの`06` Coding Contract・`07` Verification Contract・`999` Decisionで管理する。**本BDの文書監査PASSが実行テストPASSを意味しない**。[Review](../bd01_review/90_architecture_consistency_review.md)。

実装が継続的に充足すべき検証契約として、Local CLIとProductの依存方向、入力版Dispatch、Method適格性、typed inference、成果物の部分公開拒否、環境・Privacy回帰を含む。Method固有のScience受入は設計検証とは独立する。

**当該機能に適用する設計制約（関連Requirement）**

- **`NFR-015`**：Domain、Planner、Runner、API、Worker、UI、scientific benchmarkを分離testできる
- **`NFR-024`**：Navigation descriptor、route、renderer binding、runtime independenceをunit/integration/E2Eで分離検証できる
