# 10_18_fr_security_operations

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`; original ID, level and state retained.  
**Source blob:** `40b83f29c67b4a39f6db5393be7534c5e892d656`.

---

## FR original requirement rows

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| FR-121 | Security / Ops | 全project-scoped routeでpersisted ProjectMembership role（OWNER/EDITOR/VIEWER）に基づくauthorizationをservice action前に検証する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-122 | Security / Ops | 作成、更新、archive、execution、cancel、retry、export等をgeneral operational audit trailへ記録する | MUST | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| FR-123a | Security / Ops | Project authorizationに基づきexplicit sensitive outputをOWNER/EDITORへ制限し、VIEWERにはaggregate/suppressed viewのみ許可する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-123b | Security / Ops | sensitive-column metadata等に基づくconfigurable exposure/minimization policyを提供する | MUST | DEFERRED | PARTIAL | FUTURE |
| FR-124a | Security / Ops | Artifact metadata/downloadでProject境界とsafe content dispositionを検証するcurrent contractを維持する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-124b | Security / Ops | legacy/generic routeを含むArtifact downloadでProjectMembership authorizationを一貫適用する | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-125 | Security / Ops | Project archive後も監査・Lineageを保持する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-126 | Security / Ops | Metadata、Artifact、logのconfigurable retention/deletion policyを提供する | SHOULD | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| FR-127a | Security / Ops | current basic health endpointを提供する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-127b | Security / Ops | API、DB、Worker、ArtifactStoreのcomponent readinessを提供する | MUST | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| FR-128a | Security / Ops | Algorithm/Runnerをregistry/capabilityから解決・管理するcurrent contractを維持する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-128b | Security / Ops | size limit、timeout等のoperational resource configurationを一元管理する | MUST | DEFERRED | NOT_IMPLEMENTED | FUTURE |
