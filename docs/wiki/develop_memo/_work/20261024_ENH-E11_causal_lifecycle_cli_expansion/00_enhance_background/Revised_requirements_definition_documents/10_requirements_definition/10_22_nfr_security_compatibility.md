# 10_22_nfr_security_compatibility


---

## NFR original requirement rows

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| NFR-008a | 安全性 | 入力検証と危険なパス・秘密情報の保護を維持する | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-008b | 安全性 | 全project-scoped routeへProjectMembership authorizationを一貫適用する | — | ACTIVE | PARTIAL | ENH-E5 |
| NFR-008c | 安全性 | production-grade authentication/security hardeningを完成させる | — | DEFERRED | PARTIAL | FUTURE |
| NFR-009a | Privacy | current sensitive Result suppressionを維持する | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-009b | Privacy | prediction/local explanation/exportのconfigurable minimization policyを提供する | — | DEFERRED | PARTIAL | FUTURE |
| NFR-012 | Accessibility | current surfaceの主要操作をkeyboardで実行でき、focus/name/error/non-color/contrast semanticsを満たす | — | ACTIVE | PARTIAL | ENH-E5 |
| NFR-014 | 互換性 | 既存v2の因果分析仕様と保存済み結果を継続して読み取れる | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-018 | Dependency direction | 【設計制約移管・Legacy Trace】NFR-005に係る既存設計制約。具体的な実装契約は下位設計へ移し、元ID・Status・科学的制約の追跡を維持する | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-022 | Navigation determinism | 同一Project / Family / Stage routeは同一navigation stateへdeterministicに復元される | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-026 | Accessibility | Current Family / Stageを色だけでなくsemantic active state、label、focus等でも識別できる | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-028 | Dependency isolation | 任意の分析エンジンが利用不能でも基本機能を継続でき、利用不能理由を識別できる | — | ACTIVE | IMPLEMENTED | ENH-E10 |
| NFR-031 | Security and Privacy | ローカル分析で不正なPath／Symlink／任意実行Objectを拒否し、個票出力を権限・最小化条件に従い管理する | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| NFR-032 | Dependency Isolation | 任意導入の科学Backendの不在・不適合が既存Coreや別Methodの稼働を妨げず、当該能力のUnavailable状態と理由を明示できる | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| NFR-034 | License Compliance — historical, non-current | 配布先ごとのライセンス審査が完了しない限り、審査対象の外部ライブラリを含む顧客納入を許可しない【旧条文・現行E11では非適用。顧客納入は未確定】 | MUST | RETIRED | UNVERIFIED | ENH-E11 |

### ENH-E11 internal scientific CLI scope correction (Owner, 2026-11-22)

`NFR-034`は初期E11の正式なcurrent acceptanceから除外する。配布形態・受領者・外販方針が未確定であり、このE11でCustomer Deliveryの規範的要件・実装機能・Release Gateを作らない。元のID／旧MUST条文は歴史的追跡のため残し、`RETIRED`は現在の義務がないことを表す。外販決定時にはその時点の実配布形態・依存Library・適用OSS Licenseと組織ポリシーを元に別途正式要件を起案する。**これはOSSライセンスの遵守不要を意味しない。** 社内でのソフトウェア利用・複製・配布にも適用条件があり、既存組織の承認・コンプライアンス制度はE11の機能要件として新規実装せずに従う。
