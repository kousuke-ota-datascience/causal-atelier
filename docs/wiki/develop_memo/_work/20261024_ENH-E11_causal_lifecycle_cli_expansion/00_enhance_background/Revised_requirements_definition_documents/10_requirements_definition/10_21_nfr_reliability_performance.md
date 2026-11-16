# 10_21_nfr_reliability_performance

**Status:** `RD03_FORMAL_E11_ISSUED / OWNER_SHA_REVIEW_PENDING`; original ID, level and state retained.  
**Source blob:** `40b83f29c67b4a39f6db5393be7534c5e892d656`.

---

## NFR original requirement rows

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| NFR-004 | 応答性能 | 通常一覧・詳細APIの95 percentile 2秒等のgeneral performance SLOとregression gateを定義する | — | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| NFR-005 | 拡張性 | 新Analysis Familyを既存Executor変更なしにRegistry追加できる | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-006a | 信頼性 | current claim/lease/retry mechanicsでExecution/Stage lifecycleを安全に再試行できる | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-006b | 信頼性 | retry/restartでsuccessful Stage outputのduplicate durable Artifact materializationを防止する。exactly-once executionは保証しない | — | ACTIVE | PARTIAL | ENH-E5 |
| NFR-007 | 整合性 | Metadata transactionとArtifact writeのcross-store failure compensationを定義する | — | DEFERRED | PARTIAL | FUTURE |
| NFR-010a | 可用性 | API processとWorker processを分離するcurrent deployment boundaryを維持する | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-010b | 可用性 | Worker restart後の明示的resume/recovery semanticsを定義する | — | DEFERRED | PARTIAL | FUTURE |
| NFR-011a | 観測性 | current request/execution/stage correlation identifiersをlogへ出力する | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-011b | 観測性 | comprehensive structured logging、metrics、operational telemetryを提供する | — | DEFERRED | PARTIAL | FUTURE |
| NFR-015 | Testability | Domain、Planner、Runner、API、Worker、UI、scientific benchmarkを分離testできる | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-017 | Resource control | upload size、row/column count、memory、timeout等にexplicit operational hard limitを定義する | — | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| NFR-020a | 移植性 | Artifact storageを`ArtifactStore` Port abstraction越しに利用する | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-020b | 移植性 | Local filesystemに加えobject storage adapterを提供し、Port越しに切替可能にする | — | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| NFR-021 | Navigation separation | Navigation concernの変更がruntime execution lifecycleへ不要に伝播しない | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-023 | Maintainability | Family-specific Navigation Stage catalogをCapability ownershipで局所化する | — | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| NFR-024 | Testability | Navigation descriptor、route、renderer binding、runtime independenceをunit/integration/E2Eで分離検証できる | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-025 | Portability | CLI / library executionがWeb UI route、tab/sidebar state、NavigationStageDescriptorへ依存しない | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-027 | Performance | navigation metadata取得・renderingがanalysis executionのcritical pathへ不要なI/Oまたはblocking dependencyを追加しない | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-030 | Reliability | ローカル成果物の保存に失敗した場合、部分的な書込みや不完全な成果物を正常な正本として公開しない | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| NFR-035 | Scientific Acceptance | 採用Methodの科学的受入を独立した既知真値・負例・再現性・推論品質の検証で実施し、事前登録した比較と多重性を考慮する | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| NFR-036 | Backward Compatibility | 新Local CLI機能が既存Scientific CLI、Product API／UI／Worker／DBおよび因果分析仕様・結果の互換性を損なわない | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
