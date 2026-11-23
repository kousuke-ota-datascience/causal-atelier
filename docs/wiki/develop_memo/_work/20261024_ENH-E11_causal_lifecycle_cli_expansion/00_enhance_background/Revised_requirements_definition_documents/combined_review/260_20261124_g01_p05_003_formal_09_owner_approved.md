# 260 — G01/P05 AMD-E11-G01-P05-003 formal 09 Owner approval

**Date:** 2026-11-24 JST
**Decision ID:** DEC-G01-P05-003-FORMAL09-APPROVAL
**State:** FORMAL_09_OWNER_APPROVED / S10_REFREEZE_PENDING / S11_REAUTH_PENDING / P05_BLOCKED_UNDER_AMD003
**Branch:** feature/ariadne_mvp_e11
**Approved amendment:** AMD-E11-G01-P05-003
**Adopted static audit:** combined_review/259
**Underlying design decision:** DEC-G01-P05-ABORT-SESSION-BINDING-01=A (combined_review/258)
**Pre-record HEAD:** 8560c8e18f583b2c6a9081c85e76fb24a1279224
**Current frozen S10 (unchanged by this decision):** ef8e67ffa795e4ab00a4f86b600dac046548f5b4

## 1. Owner decision

> DEC-G01-P05-003-FORMAL09-APPROVALを承認する。AMD-E11-G01-P05-003を正式09として承認し、combined_review/259の静的整合性・実装可能性監査結果を採用する。P02への限定例外はPublicationSessionToken、LocalPublicationPortおよびLocalPublicationAdapterのbeginへの後方互換なオプション引数追加、abort操作、Publisherの発行元・セッション情報の保持とConstructor初期化に限る。既存LocalArtifactPublisher.begin/validate/commit/abortアルゴリズム、Adapterのseal/publish、P01〜P04チェックポイント履歴、公開E11 Schema Version、既承認の科学的意味、独立G01_999受入条件、DEFERRED_PRODUCT_POLICY_BRIDGE未完了依存を維持する。正式09承認記録をGitHubへ反映し、S10再凍結用の完全Git SHAを提示せよ。S10再凍結とS11再認可は別決裁とする。

AMD-003 is formally approved as an internal, bounded amendment to AMD-002's session identity, issuance, signatures and P02 exception envelope. AMD-001 and other AMD-002 invariants remain effective. Audit 259 is adopted as an Author static contract and implementability audit conditional on fresh per-attempt tokens and sequential lifecycle operations per session, not executable or independent verification.

## 2. Verified approval input

Before recording this decision, remote HEAD was 8560c8e18f583b2c6a9081c85e76fb24a1279224. AMD-003 and audit 259 were read from the branch. Comparison to previous S11 record 9420734f7968bfe85d72c535dd670ed85f753874 returned ahead 10, behind 0, with exactly seven changed document paths: IF 23_41, DD 30_62, P05 06, G01 07, AMD-003 formal 09 candidate, and combined_review/258 and 259. No source/test/lockfile change was present.

## 3. Approved bounded P02 exception

Only later S11 may authorize changes to src/ariadne/capabilities/causal/ports/local_io.py (nominal PublicationSessionToken, optional session=None keyword on LocalPublicationPort.begin, abort signature) and src/ariadne/interfaces/cli/local_causal/publication.py (necessary imports, optional keyword-only issuer/session arguments and private _issuer/_session initialization in LocalArtifactPublisher constructor, Adapter.begin optional session and issuance binding, Adapter.abort). Existing four-argument constructor and legacy begin calls remain call-compatible. Legacy tokenless sessions remain ineligible for facade abort. No registry, setter, new Application collaborator or scientific sink change.

P05 retains independently generated fresh token, validated run_id/request_hash and exact root before begin. Adapter verifies exact nominal sink, original publisher sink, issuer identity, token identity, run/hash/root/policy and STAGING or VALIDATING before delegation to unchanged concrete abort. Refuse mismatches without mutation. Application abort once after successful begin and before invoking publish; never after publish invocation. Original typed error preserved; secondary nonsecret cleanup error separately. Preserve existing final run; private quarantine is not secure erasure. Existing concrete begin/stage_bytes/validate/commit/abort algorithms and Adapter seal/publish unchanged. No protected P02 test or completed Package changes outside the stated exception. Any further exception requires separate Owner disposition.

## 4. Protected conditions

P01 9bff61f0eae25236f95f31f2cd3e7c81291f0167
P02 3a76a0aa1698037354b284ba7b5a875300473ce6
P03 858c9f73366036a2d1445e558135cd521f611462
P04 7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6

Maintain public E11 Schema Versions, existing scientific meaning, privacy, no-clobber, independent Reader, Product v2 compatibility, uv.lock, independent science and G01_999 acceptance. DEFERRED_PRODUCT_POLICY_BRIDGE remains UNFULFILLED. Historical 207 tests do not establish new behavior. New focused, physical FS and regression verification remain required.

## 5. Separate control-plane decisions

This is formal 09 approval only. The commit recording this approval is the candidate for separate exact SHA S10 refreeze; it does not itself change the active S10. Prior DEC-G01-P05-002-S11-REAUTH-01 does not authorize AMD-003 implementation. New S10 refreeze followed by distinct G01/P05/Trial01 limited S11 authorization and Agent preflight checks are required before coding. No source implementation, test execution, checkpoint or independent PASS asserted.
