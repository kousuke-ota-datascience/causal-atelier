# 10_22_nfr_security_compatibility

**Status:** `RD03_FORMAL_E11_ISSUED / OWNER_SHA_REVIEW_PENDING`; original ID, level and state retained.  
**Source blob:** `40b83f29c67b4a39f6db5393be7534c5e892d656`.

---

## NFR original requirement rows

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| NFR-008a | 安全性 | current input validation、path traversal防止、secret非露出等のsafeguardを維持する | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-008b | 安全性 | 全project-scoped routeへProjectMembership authorizationを一貫適用する | — | ACTIVE | PARTIAL | ENH-E5 |
| NFR-008c | 安全性 | production-grade authentication/security hardeningを完成させる | — | DEFERRED | PARTIAL | FUTURE |
| NFR-009a | Privacy | current sensitive Result suppressionを維持する | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-009b | Privacy | prediction/local explanation/exportのconfigurable minimization policyを提供する | — | DEFERRED | PARTIAL | FUTURE |
| NFR-012 | Accessibility | current surfaceの主要操作をkeyboardで実行でき、focus/name/error/non-color/contrast semanticsを満たす | — | ACTIVE | PARTIAL | ENH-E5 |
| NFR-014 | 互換性 | `causal-analysis-spec/2`の正規contractおよび保存済みCausal Resultをschema versionに従って読取可能に保つ | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-018 | Dependency direction | Product DomainからWeb Framework、ORMおよびlegacy packageへ依存しない | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-022 | Navigation determinism | 同一Project / Family / Stage routeは同一navigation stateへdeterministicに復元される | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-026 | Accessibility | Current Family / Stageを色だけでなくsemantic active state、label、focus等でも識別できる | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-028 | Dependency isolation | optional analytical engineのimport/availability failureをcore process startup failureへ伝播させず、capability discovery/selection時に局所化してstable unavailable state/errorとして報告する | — | ACTIVE | IMPLEMENTED | ENH-E10 |
| NFR-031 | Security and Privacy | ローカル分析で不正なPath／Symlink／任意実行Objectを拒否し、個票出力を権限・最小化条件に従い管理する | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| NFR-032 | Dependency Isolation | 任意導入の科学Backendの不在・不適合が既存Coreや別Methodの稼働を妨げず、当該能力のUnavailable状態と理由を明示できる | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| NFR-034 | License Compliance | 配布先ごとのライセンス審査が完了しない限り、審査対象の外部ライブラリを含む顧客納入を許可しない | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
