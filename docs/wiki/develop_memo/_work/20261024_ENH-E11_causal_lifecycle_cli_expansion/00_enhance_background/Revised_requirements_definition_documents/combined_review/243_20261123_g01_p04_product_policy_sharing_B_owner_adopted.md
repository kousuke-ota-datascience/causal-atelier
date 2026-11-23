# 243 — G01/P04 Product v2 shared policy staged migration — Owner B adopted

**Date:** 2026-11-23 JST  
**Decision:** `DEC-G01-P04-PRODUCT-POLICY-SHARING-01=B_ADOPTED`  
**State:** `OWNER_ARCHITECTURE_DECISION_ADOPTED / AMD004_09_PENDING / S10_S11_PENDING`  
**Prior stopped Agent START_SHA:** `99c33a661272d45bf72c8dee61ce1eb129a337dd`  
**Prior G01 S10:** `cbfdbdd6b91f3a2f889fe9b62c2a4ab286da6132`

## Owner's explicit decision

> DEC-G01-P04-PRODUCT-POLICY-SHARING-01はB案を採用する。G01/P04では新Local Methodの共通pure policy基盤とP1-M06適格性検証を実装し、既存Product v2 ScientificValidationServiceへの接続はDEFERREDとして別途Owner承認を要する工程に分離せよ。Architecture全体の単一Authority・共通化要求は維持し、G01_999の受入条件に関する依存関係も明示すること。Product v2コード、完了済みP01/P03、公開E11 Schema Version、既承認の科学的・独立検証条件を変更せず、上位設計・06・07の最小改訂とAMD-E11-G01-P04-004正式09案を作成せよ。

## Approved design and temporal scope

**G01/P04 now:** One Local P1-M06 Method metadata/eligibility pure policy authority; actual Local DISCOVER validation through the Method Registry and effective Backend capability path. No patch to Product v2 `ScientificValidationService.validate_submission`, its existing legacy `ESTIMATOR_CAPABILITIES`, Product v2 CLI/DB/Worker, or completed P01/P03 implementation. The legacy table remains a **legacy-only compatibility baseline** during this intermediate stage, not an additional owner of P1-M06 or new Method eligibility. No duplicative, independently mutable copies of legacy estimator rules in new Method Registry and no claim of completed Product policy delegation.

**Deferred work:** `DEFERRED_PRODUCT_POLICY_BRIDGE` requires a distinct Owner-approved integration effort to migrate Product v2 validation to the shared pure policy/metadata Authority while preserving Product v2 Discovery/Identification early return, Estimation aliases/estimands/error classifications, upstream lineage, and all Product regressions. `DEFERRED` does not mean `RETIRED` or fulfilled.

**Acceptance discipline:** G01_999 continues to require all independent FCI/PAG/BK/FS/Privacy/Regression/T2/T3 evidence. The shared-policy bridge is an explicitly tracked **unfulfilled architecture dependency**: no `G01_999 PASS` by claiming the shared Product connection is present, and absent a separate formal Owner acceptance rephasing decision, the relevant shared-policy completion requirement remains blocking until actual authorized bridge and verification are complete. Do not silently assign its completion to an unspecified later Gate or waive it.

## Change management

Bounded Author drafting changes: DD `30_61`, DD `30_62`, IF `23_41`, G01/P04 `06`, G01 `07`, new `AMD-E11-G01-P04-004` formal 09 candidate. Decision dossier `242` is supporting non-normative evidence.

The Owner adopted the design/timing choice and contract-drafting authority; this is **not** formal AMD-004 09 approval, S10 immutable refreeze, or revised G01/P04/Trial01 S11 reauthorization. Existing S10/S11 remain historical authority for old WHAT. Coding stays blocked until renewed 09→S10→S11.

Protected SHA P01 `9bff61f0eae25236f95f31f2cd3e7c81291f0167`, P03 `858c9f73366036a2d1445e558135cd521f611462`; retain AMD-001 exhaustive CI coverage, AMD-002 categorical category_codes, AMD-003 Fisher-Z numeric acceptance, public E11 versions, and independent G01_999 acceptance.
