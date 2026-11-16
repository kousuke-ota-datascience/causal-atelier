# 10_18_fr_security_operations


---

## FR original requirement rows

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| FR-121 | Security / Ops | Project内操作を所属Roleに応じて認可し権限外の処理を防止する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-122 | Security / Ops | 作成、更新、archive、execution、cancel、retry、export等をgeneral operational audit trailへ記録する | MUST | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| FR-123a | Security / Ops | Project authorizationに基づきexplicit sensitive outputをOWNER/EDITORへ制限し、VIEWERにはaggregate/suppressed viewのみ許可する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-123b | Security / Ops | sensitive-column metadata等に基づくconfigurable exposure/minimization policyを提供する | MUST | DEFERRED | PARTIAL | FUTURE |
| FR-124a | Security / Ops | 成果物の情報・取得をProject境界内で安全に利用できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-124b | Security / Ops | 旧経路を含む成果物取得に同じProject権限を適用する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-125 | Security / Ops | Project archive後も監査・Lineageを保持する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-126 | Security / Ops | Metadata、Artifact、logのconfigurable retention/deletion policyを提供する | SHOULD | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| FR-127a | Security / Ops | current basic health endpointを提供する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-127b | Security / Ops | API、DB、Worker、ArtifactStoreのcomponent readinessを提供する | MUST | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| FR-128a | Security / Ops | 【設計制約移管・Legacy Trace】FR-035／NFR-005の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-128b | Security / Ops | 運用上の処理規模と実行時間の上限を設定・適用できる | MUST | DEFERRED | NOT_IMPLEMENTED | FUTURE |
