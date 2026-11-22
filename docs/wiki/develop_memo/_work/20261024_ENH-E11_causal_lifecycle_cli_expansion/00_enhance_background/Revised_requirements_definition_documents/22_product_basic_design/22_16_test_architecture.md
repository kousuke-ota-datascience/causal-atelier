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
| Environment | 4必須isolated profiles（BASE/DOWHY/ECONML/TIGRAMITE）＋Method別conditional RD、lock/extra/API/version、core startup、関連E9/v2 regression |
| Independent science | 41 Method/68 Scope/10 UC、DGP/NEG/REF/AC/ENV-AC、FWER=.05、K/R/MC／Coverage／Monte Carlo error |

`PLAN:G01〜G10`は暫定的な計画Workstream名であり、そのままではEnhancement Workflowの正式受入Gateではない。正式Gateはsemantic Acceptance Contractとして境界を確定し、各Gateの`06` Coding Contract・`07` Verification Contract・`999` Decisionで管理する。**本BDの文書監査PASSが実行テストPASSを意味しない**。[Review](../bd01_review/90_architecture_consistency_review.md)。

実装が継続的に充足すべき検証契約として、Local CLIとProductの依存方向、入力版Dispatch、Method適格性、typed inference、成果物の部分公開拒否、環境・Privacy回帰を含む。Method固有のScience受入は設計検証とは独立する。

**当該機能に適用する設計制約（関連Requirement）**

- **`NFR-015`**：Domain、Planner、Runner、API、Worker、UI、scientific benchmarkを分離testできる
- **`NFR-024`**：Navigation descriptor、route、renderer binding、runtime independenceをunit/integration/E2Eで分離検証できる

## S02 Owner-adopted current Local CLI contract (2026-11-22)

The 2026-11-22 Owner decision (combined_review/137) **supersedes only contradictory E11 draft implementation mechanisms** in preceding sections: a single versioned Study `privacy.row_export_requested=true` is the explicit row-export opt-in, with no additional CLI flag or `cli_row_flag` argument. The unpublished `e11-local-study/1` has **no `privacy.policy_ref` field**; the withdrawn signed-policy Schema is historical/non-dispatched. Permission is rechecked for each run and before row iteration using source/Method identity, verified private nonroot same-UID local ext4/XFS TrustedRoot and strict Method-specific output shape/limits. Unregistered or ineligible output is denied, not silently downgraded. No new Product GraphVersion import/mutation: standalone Local Graph refs must be null; Product GraphVersion remains Product-owned. Shared Schema/RowSchema/Port shapes and targeted regressions may replace duplicate implementation **only after strict per-Method Positive/Negative parity, dependency/ABI and old Product v2 compatibility are established**. G10 checks independently accepted evidence for **all 41 Methods** and reruns changed/affected Method science; upstream evidence reuse needs a proven transitive behavior-affecting dependency closure, else rerun/BLOCK. G01 invariant-based real-FS failure tests remain obligatory for NFR-030 no-false-success; no untested power-loss certification. This is a normative design revision, not scientific/OS/backend PASS or Coding Authorization.
