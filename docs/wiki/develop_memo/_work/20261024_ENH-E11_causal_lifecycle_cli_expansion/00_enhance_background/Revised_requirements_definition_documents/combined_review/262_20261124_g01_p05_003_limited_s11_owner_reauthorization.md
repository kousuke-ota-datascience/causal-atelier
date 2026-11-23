# 262 — G01/P05/Trial01 limited S11 Owner reauthorization against AMD-003 S10

**Date:** 2026-11-24 JST  
**Decision ID:** `DEC-G01-P05-003-S11-REAUTH-01`  
**State:** `S11_OWNER_APPROVED / G01_P05_TRIAL01_LIMITED_CODING_AUTHORIZED / BOUNDED_P02_SESSION_BINDING_EXCEPTION_AUTHORIZED / G01_999_NOT_PASSED / DEFERRED_PRODUCT_POLICY_BRIDGE_UNFULFILLED`  
**Repository:** `kousuke-ota-datascience/causal-atelier`  
**Branch:** `feature/ariadne_mvp_e11`  
**Immutable active G01-S10:** `47ecfe33f3daf91da8c589db589b21f628e4e23b`  
**S10 decision:** `DEC-G01-P05-003-S10-REFREEZE-01`, combined_review/261  
**Formal 09 decision:** `DEC-G01-P05-003-FORMAL09-APPROVAL`, combined_review/260  
**Amendments:** AMD-E11-G01-P05-001, 002, 003 (003 supersedes only 002 identity/issuance/signature/exception provisions)  
**Superseded S11:** DEC-G01-P05-002-S11-REAUTH-01 against earlier S10 ef8e67ffa795e4ab00a4f86b600dac046548f5b4

## 1. Explicit Owner decision

> DEC-G01-P05-003-S11-REAUTH-01を承認する。AMD-E11-G01-P05-003に基づく新G01-S10凍結SHA 47ecfe33f3daf91da8c589db589b21f628e4e23b を対象に、G01/P05/Trial01限定Coding Authorizationを再発行せよ。完了済みP02への限定例外はPublicationSessionTokenの追加、LocalPublicationPortおよびLocalPublicationAdapterのbeginへの後方互換なオプション引数追加、abort操作、Publisherの発行元・セッション情報の保持とConstructor初期化に限る。既存LocalArtifactPublisher.begin/stage_bytes/validate/commit/abortアルゴリズム、Adapterのseal/publishを変更してはならない。P01チェックポイント9bff61f0eae25236f95f31f2cd3e7c81291f0167、P02チェックポイント3a76a0aa1698037354b284ba7b5a875300473ce6、P03チェックポイント858c9f73366036a2d1445e558135cd521f611462、P04チェックポイント7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6、公開E11 Schema Version、既承認の科学的意味、独立科学検証・G01_999受入条件、およびDEFERRED_PRODUCT_POLICY_BRIDGE未完了依存を維持する。

**Disposition:** Issue new limited Coding Authorization solely for GATE_ID=G01 / PACKAGE_ID=P05 / TRIAL_NO=01, against the exact immutable S10 above, including the expressly bounded completed-P02 exception and focused developer verification. No unrelated Package or Gate authorization or independent acceptance waiver.

## 2. Verified pre-record Git state

Remote branch HEAD before issuance was a18e717886acb9d3056f4792851a91e0a1a9a8fe. Read S10 record combined_review/261_20261124_g01_p05_003_s10_owner_refreeze.md and confirmed exact frozen SHA and scope. Comparison from S10 to that HEAD returned ahead 1 / behind 0; only the S10 administrative record 261 was added.

| Protected Package | Exact checkpoint | Comparison to pre-record HEAD |
| --- | --- | --- |
| P01 | 9bff61f0eae25236f95f31f2cd3e7c81291f0167 | ancestor; ahead 113 / behind 0 |
| P02 | 3a76a0aa1698037354b284ba7b5a875300473ce6 | ancestor; ahead 88 / behind 0 |
| P03 | 858c9f73366036a2d1445e558135cd521f611462 | ancestor; ahead 78 / behind 0 |
| P04 | 7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6 | ancestor; ahead 36 / behind 0 |

Git checks do not constitute runtime verification.

## 3. Authorized implementation scope

Use frozen Gate 06, P05 06, Gate 07, IF 23_41, DD 30_62 and formal AMD-001/002/003. Preserve AMD-001 Manifest Factory boundary, immutable observed evidence, twelfth required collaborator and unchanged P01 factory. Preserve AMD-002 pre-publish abort and post-publish protection as supplemented by AMD-003.

Only permitted completed-P02 changes:
- src/ariadne/capabilities/causal/ports/local_io.py: nominal identity-only PublicationSessionToken (__slots__ = ()), optional session=None on LocalPublicationPort.begin and session-bound abort declaration.
- src/ariadne/interfaces/cli/local_causal/publication.py: necessary token import, optional keyword-only issuer/session constructor parameters and private _issuer/_session initialization before creation of original _sink in LocalArtifactPublisher, optional session argument and issuance binding in LocalPublicationAdapter.begin, and new LocalPublicationAdapter.abort implementation.

Exact signature and predicate are frozen in AMD-003 and DD 30_62 §8.2a. P05 retains a fresh exact nominal token and expected run/hash/root before begin; Adapter binds issuer=self and token before calling unchanged concrete begin. Legacy begin and four-argument constructor calls remain compatible; legacy tokenless sessions cannot use facade abort. Abort checks exact nominal sink and Publisher, original sink identity, issuer, independent token, run/hash/root/policy and STAGING or VALIDATING before delegating to unchanged concrete abort exactly once. Mismatch fails PUBLICATION_FAILED before mutation. No registry, setter, new Application collaborator or scientific sink change. No private CLI access from Application. Fresh token per attempt; per-session lifecycle calls sequential; distinct sessions may interleave.

Application makes one eligible abort attempt after successful begin and before invoking publish on failure, closes eligibility immediately before publish invocation, and never invokes abort after publish starts. Preserve primary typed failure/exit and separately report nonsecret cleanup fault. Existing Publisher owns rename/indeterminate handling. Private residue quarantine is not secure erasure; preserve pre-existing final run and no newly committed final Marker/run on pre-publish failure.

Existing concrete LocalArtifactPublisher.begin/stage_bytes/validate/commit/abort algorithms, Adapter.seal/publish, completed P02 instructions/tests/checkpoint and P01/P03/P04 remain protected. Any necessary change beyond this envelope requires another explicit Owner decision before modification.

## 4. Verification and retained conditions

Run authorized P05 focused developer tests, including AMD-001 Factory wiring and AMD-003 original pairing, same-policy different Adapter, same Adapter/different run, identical run/hash/root with different fresh tokens, wrong hash/root/policy/token, fake sink, legacy tokenless rejection, invalid/repeated states, no mutation of either session on refusal, actual FS/FD/quarantine behavior, preservation of original failure and no Application abort after publish invocation. Regress original P01–P04 focused tests and relevant Product v2 tests without rewriting historical expectations. A private staging Marker after seal is not final committed evidence. Historical 207 passing tests and Author static audit 259 do not establish new behavior.

Preserve public E11 Schema Versions, existing scientific meaning, privacy, no-clobber, independent Reader, Product v2 compatibility, uv.lock, actual physical FS and independent science verification, T2/T3 and independent G01_999 acceptance. DEFERRED_PRODUCT_POLICY_BRIDGE stays UNFULFILLED and its acceptance dependency is neither waived nor retired. This is not a P05 checkpoint or independent PASS.

## 5. Coding Agent restart

Use 40_operator_workflows/agent_entry_prompts/10_normal_execution_02_work_package_coding_agent_prompt.md with G01/P05/01. Fast-forward synchronize designated branch, confirm clean worktree, record actual full START_SHA, verify frozen SHA ancestry and exact administrative-only post-freeze changes 261/262 before coding. Verify uv.lock Git blob and physical SHA-256 across S10/HEAD/worktree, checkpoint ancestry and completed Package evidence, actual package state and absence of incompatible P05 checkpoint. Read effective frozen contracts and approved amendments. Implement and test only authorized scope, record actual commands/outcomes, paths, checkpoint SHA and push outcome or stop with precise blocker. Do not weaken acceptance or fabricate PASS.

## 6. Control-plane conclusion

Distinct limited S11 issued against 47ecfe33f3daf91da8c589db589b21f628e4e23b. This administrative record does not alter that immutable S10. Coding may resume only after Agent restart checks. No implementation, executable tests, checkpoint or independent acceptance performed by this record.
