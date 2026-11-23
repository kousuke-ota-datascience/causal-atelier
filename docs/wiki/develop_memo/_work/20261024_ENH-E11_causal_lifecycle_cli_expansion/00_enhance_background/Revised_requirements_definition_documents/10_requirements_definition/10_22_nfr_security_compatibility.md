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
| NFR-034 | License Compliance — future customer delivery | 顧客向け納入が正式に決定された場合、審査対象の外部ライブラリを含む顧客納入について、適用ライセンスと配布条件を審査する。提供形態・対象Package・審査手順はその時点で別途確定する | MUST | DEFERRED | UNVERIFIED | FUTURE |

### External customer delivery (non-current requirement)

`NFR-034`は外販・顧客納入の実施自体が未確定であるため、現行ENH-E11の必須実装・受入から除外し、`DEFERRED / FUTURE`として将来検討対象に保持する。`DEFERRED`は外販を約束するものではない。将来顧客納入が正式にスコープ採用された場合、その時点の提供形態・配布Library・適用OSS License・組織ポリシーに基づき具体的な手順と受入条件を再審議する。**社内利用に適用されるOSSライセンス義務は免除されない。** 既存の社内コンプライアンス制度は遵守するが、その管理機能を今回のAriadneへ追加しない。今回のStatus訂正根拠は`combined_review/134_20261122_dec_nfr034_deferred_correction.md`。

### NFR-031 local output boundary

非root EUID・所有者一致のprivate ext4/XFS TrustedRoot（owner-only mode、safe dirfd/path/symlink）、Method別列・row/byte/memory制限、Study上の明示単独opt-inをPositive/Negativeで検証する。不許可時は個票生成に先立ちfail-closedし、個票値をログ/集計/Manifestへ含めない。同一UID別processや特権管理者に対する隔離を保証しない。未実装の署名Policy／二重CLI flagは初期提供外。


### Local per-run privacy authorization invariant (NFR-031)

Local scientific output requires an effective privacy decision tied to the **same validated Study/run ID and JCS-derived request hash, same live verified TrustedRoot FD identity, current principal EUID, permitted output classification and actual staged artifacts**. A permit for a different run, request, root, principal, or artifact classification must be rejected before publication even when the supplied decision says allowed. The staged files are checked again by the publisher's policy evaluator; denied or stale decisions fail closed, and aggregate-only G01 never authorizes row/Parquet output. This extends the existing NFR-031 security meaning, not Product RBAC, an independently signed policy, or a new wire field.


### G01 Local privacy decision equality and independently effective authorization (NFR-031)

An ephemeral `PrivacyDecision` is a **value-bearing constraint**, not an issuer-authenticated or unforgeable authorization credential. Acceptance MUST depend on the trusted Publisher's independent re-evaluation against actual staged Study, run/hash, verified root FD/EUID and artifact inventory, plus **structural value equality** to the supplied decision. Two valid decisions of the same type with equal values are equivalent and are accepted if the independently evaluated policy allows; issuance provenance, object identity, nonce, MAC or digital signature is NOT required. An allow boolean alone, a stale/mismatched decision or a policy denial MUST fail closed. Previously described 'forged' negative means **detectable field/invariant/policy mismatch**, not a byte-for-byte equivalent reconstruction. No relaxation of the privacy boundary or root/row restrictions is implied.
