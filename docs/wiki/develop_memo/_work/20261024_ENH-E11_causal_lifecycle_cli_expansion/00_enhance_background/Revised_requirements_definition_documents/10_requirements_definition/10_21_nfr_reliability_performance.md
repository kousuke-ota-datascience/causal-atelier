# 10_21_nfr_reliability_performance


---

## NFR original requirement rows

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| NFR-004 | 応答性能 | 通常一覧・詳細APIの95 percentile 2秒等のgeneral performance SLOとregression gateを定義する | — | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| NFR-005 | 拡張性 | 新しい分析領域を既存分析の挙動を壊さず追加できる | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-006a | 信頼性 | 中断・再送時にExecutionを安全に再開・再試行できる | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-006b | 信頼性 | 再試行・再起動で成功済み成果物の重複作成を防止する | — | ACTIVE | PARTIAL | ENH-E5 |
| NFR-007 | 整合性 | 成果物と管理情報の不整合が発生した場合、安全に回復・検知できる | — | DEFERRED | PARTIAL | FUTURE |
| NFR-010a | 可用性 | 分析実行の負荷がAPIの応答性・稼働に不必要な影響を与えない | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-010b | 可用性 | 実行基盤の再起動後に処理状態を復元・回復できる | — | DEFERRED | PARTIAL | FUTURE |
| NFR-011a | 観測性 | Request・実行・処理単位をまたいで障害を追跡できる | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-011b | 観測性 | comprehensive structured logging、metrics、operational telemetryを提供する | — | DEFERRED | PARTIAL | FUTURE |
| NFR-015 | Testability | Domain・実行・API・UI・科学計算を個別に検証できる | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-017 | Resource control | upload size、row/column count、memory、timeout等にexplicit operational hard limitを定義する | — | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| NFR-020a | 移植性 | 成果物保存先を交換しても分析の振る舞いが維持される | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-020b | 移植性 | Local filesystemに加えobject storage adapterを提供し、Port越しに切替可能にする | — | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| NFR-021 | Navigation separation | 画面ナビゲーションの変更が分析実行ライフサイクルに影響しない | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-023 | Maintainability | Familyごとの画面構成を他Familyへの影響を抑えて変更できる | — | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| NFR-024 | Testability | 画面構成・URL復元・表示・分析実行独立性を個別に検証できる | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-025 | Portability | CLIやライブラリ実行を画面状態なしで行える | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-027 | Performance | 画面構成情報の取得・表示によって分析処理の性能を不要に低下させない | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-030 | Reliability | ローカル成果物の保存に失敗した場合、部分的な書込みや不完全な成果物を正常な正本として公開しない | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| NFR-035 | Scientific Acceptance | 採用Methodの科学的受入を独立した既知真値・負例・再現性・推論品質の検証で実施し、事前登録した比較と多重性を考慮する | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| NFR-036 | Backward Compatibility | 新Local CLI機能が既存Scientific CLI、Product API／UI／Worker／DBおよび因果分析仕様・結果の互換性を損なわない | MUST | ACTIVE | UNVERIFIED | ENH-E11 |


### Local publish authorization freshness (NFR-030 / G01)

For a local run, a previously issued allow decision cannot itself prove that the actual staged files still satisfy the approved output policy. Revalidate the current staged Study, run/request identity, effective trusted root/actor, and complete artifact inventory **before** sealing the manifest/commit marker and atomically publishing. A missing, denied, inconsistent, or stale privacy authorization must not lead to a published COMPLETE result; later uncertainty after rename follows the existing indeterminate/readback requirements. This is an elaboration of NFR-030, not a new public authorization token or a relaxation of atomicity.
