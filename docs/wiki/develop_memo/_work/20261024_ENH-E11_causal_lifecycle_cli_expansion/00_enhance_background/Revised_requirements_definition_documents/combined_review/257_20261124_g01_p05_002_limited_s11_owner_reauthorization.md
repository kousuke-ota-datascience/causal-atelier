# 257 — G01/P05/Trial01 limited S11 Owner reauthorization against AMD-002 S10

**Date:** 2026-11-24 JST  
**Decision ID:** `DEC-G01-P05-002-S11-REAUTH-01`  
**State:** `S11_OWNER_APPROVED / G01_P05_TRIAL01_LIMITED_CODING_AUTHORIZED / BOUNDED_P02_ABORT_EXCEPTION_AUTHORIZED / DEFERRED_PRODUCT_POLICY_BRIDGE_UNFULFILLED / G01_999_NOT_PASSED`  
**Repository:** `kousuke-ota-datascience/causal-atelier`  
**Branch:** `feature/ariadne_mvp_e11`  
**Immutable active G01-S10:** `ef8e67ffa795e4ab00a4f86b600dac046548f5b4`  
**S10 decision:** `DEC-G01-P05-002-S10-REFREEZE-01`, combined_review/256  
**Formal 09 decision:** `DEC-G01-P05-002-FORMAL09-APPROVAL`, combined_review/255  
**Amendments:** `AMD-E11-G01-P05-001` and `AMD-E11-G01-P05-002` (002 supplements 001)  
**Superseded P05 S11:** `DEC-G01-P05-001-S11-REAUTH-02`, bound to earlier S10 `d5b7fab759b27ed8427a46256bac5ac8231e0c77`

## 1. Explicit Owner decision

> DEC-G01-P05-002-S11-REAUTH-01を承認する。AMD-E11-G01-P05-002に基づく新G01-S10凍結SHA ef8e67ffa795e4ab00a4f86b600dac046548f5b4 を対象に、G01/P05/Trial01限定Coding Authorizationを再発行せよ。完了済みP02への実装変更例外はLocalPublicationPortおよびLocalPublicationAdapterへのabort操作の限定追加のみとする。既存LocalArtifactPublisher.abort、begin/seal/publishを変更してはならない。P01チェックポイント9bff61f0eae25236f95f31f2cd3e7c81291f0167、P02チェックポイント3a76a0aa1698037354b284ba7b5a875300473ce6、P03チェックポイント858c9f73366036a2d1445e558135cd521f611462、P04チェックポイント7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6、公開E11 Schema Version、既承認の科学的意味、独立科学検証・G01_999受入条件、およびDEFERRED_PRODUCT_POLICY_BRIDGE未完了依存を維持する。

**Disposition:** New Owner S11 authorization is issued solely for `GATE_ID=G01 / PACKAGE_ID=P05 / TRIAL_NO=01` against the exact frozen S10 above. It includes implementation and focused developer verification under the approved amendments, and only the expressly bounded completed-P02 source exception specified below. It does not authorize an unrelated Package, Gate, or independent acceptance waiver.

## 2. Verified pre-record state

GitHub branch HEAD before issuing this record was `2b9ac5e7f071b4bf0f5ed4c25398a5291985ec0c`. The S10 approval record `combined_review/256_20261124_g01_p05_002_s10_owner_refreeze.md` was read and matched the exact frozen SHA and Owner scope. Comparison from S10 to that HEAD returned ahead 1 / behind 0, with only the S10 administrative record 256 added.

| Package | Protected checkpoint | Comparison to pre-record HEAD |
| --- | --- | --- |
| P01 | `9bff61f0eae25236f95f31f2cd3e7c81291f0167` | ancestor; ahead 100 / behind 0 |
| P02 | `3a76a0aa1698037354b284ba7b5a875300473ce6` | ancestor; ahead 75 / behind 0 |
| P03 | `858c9f73366036a2d1445e558135cd521f611462` | ancestor; ahead 65 / behind 0 |
| P04 | `7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6` | ancestor; ahead 23 / behind 0 |

Ancestry and diff checks are not runtime tests or evidence of unchanged scientific behavior by themselves. The Coding Agent must independently verify local worktree and prior package reports before editing.

## 3. Authorized implementation scope

Use the frozen Gate 06, P05 06, Gate 07, superior IF 23_41 and DD 30_62, and both formal 09 amendments. Preserve all unrelated contract provisions.

AMD-001: Application-owned `LocalManifestFactoryPort.build(*,evidence:ManifestBuildEvidence)->ManifestValue`, required twelfth UseCase collaborator, immutable evidence and CLI composition-root Adapter delegating to the original P01 `LocalRunManifest.from_run_evidence`. No Application import of CLI implementation or nominal CLI DTOs. No bypass of existing Factory validation.

AMD-002: add exactly the following internal operation to the existing P02 Port and matching facade:

~~~python
def abort(self, *, sink: StagingArtifactSink, reason: str) -> None: ...
~~~

The only permitted completed-P02 source edits are:
- `src/ariadne/capabilities/causal/ports/local_io.py`: additive `LocalPublicationPort.abort` declaration;
- `src/ariadne/interfaces/cli/local_causal/publication.py`: additive `LocalPublicationAdapter.abort` method.

The Adapter verifies exact begin-returned sink, owning Publisher, policy binding, and allowed pre-publication state before delegating to the original `LocalArtifactPublisher.abort(reason)`. Reject fake/substituted sink, wrong policy, repeated abort and unsafe states. No modification to `LocalArtifactPublisher.abort`, existing begin/seal/publish, any other P02 method, scientific sink, P02 instruction/test/checkpoint history, or other completed Package. If implementation cannot meet the approved contract within those two additive methods, stop and request another Owner decision; do not add ownership registries or modify begin implicitly.

P05 invokes abort once on the exact sink on a failure after successful begin and before invoking publish, including Discovery, staging, invalid evidence, Manifest Factory or seal failure. No abort before begin returns a sink. No Application abort once publish is invoked, including a raised publish exception; the original P02 transaction owns its internal abort and indeterminate handling. Never delete or overwrite a potentially committed run. Abort closes owned handles and quarantines residue, not guaranteed secure erasure. Preserve original typed failure and CLI exit classification; report cleanup failure separately without secret or row data.

## 4. Verification obligations and retained invariants

Implement focused tests within authorized P05 scope for AMD-001 Factory wiring and AMD-002 pre-publish failure path; verify original sink identity, safe lifecycle, repeated/invalid abort rejection, failure preservation, actual private FS/FD and quarantine behavior, no false committed marker/final run, no Application abort after publish invocation, and independent Reader. Rerun original P01–P04 focused tests and relevant Product v2 regressions; do not modify their historical expected results. The Coding Agent's earlier 207 PASS report is historical, not proof of the new implementation.

Preserve existing public E11 Schema Versions, six-field ArtifactDescriptor, public CLI/API, P1-M06 FCI/PAG/Graph science, authentic scientific negative vs technical failure, unsupported non-null BK fail-closed behavior, privacy/no-row, no-clobber, independent Reader, Product v2 compatibility and uv.lock. Real Python/Backend/FS evidence, independent scientific validation, T2/T3 and G01_999 acceptance remain mandatory.

`DEFERRED_PRODUCT_POLICY_BRIDGE` stays UNFULFILLED, not retired or waived; the corresponding G01_999 dependency remains unresolved absent separately approved completion or explicit acceptance rephasing. This S11 is not a P05 checkpoint or independent PASS.

## 5. Agent restart conditions

1. Use `40_operator_workflows/agent_entry_prompts/10_normal_execution_02_work_package_coding_agent_prompt.md` with G01/P05/01.
2. Fast-forward synchronize feature/ariadne_mvp_e11, confirm a clean worktree, record actual full START_SHA, and verify frozen S10 ancestry. Before coding, changes after S10 must be solely the S10/S11 administrative records 256/257; check exact paths, not ancestry alone.
3. Verify uv.lock Git blob and physical SHA-256 across S10/HEAD/worktree, and P01–P04 checkpoint ancestry and completed package evidence. Check actual package state and absence of an incompatible prior P05 checkpoint.
4. Read effective frozen IF/DD/06/07 and both approved amendments, implement only authorized scope and test as directed. Preserve the exact bounded P02 exception.
5. Record actual commands/results, changed paths, checkpoint SHA and push outcome or stop with exact blocker. No fabricated PASS, no weakening tests, and no unapproved contract amendment.

## 6. Control-plane conclusion

This is a distinct, limited S11 authorization against `ef8e67ffa795e4ab00a4f86b600dac046548f5b4`. This administrative record does not change that frozen SHA. Coding may resume only after Agent restart checks; no source implementation or tests are performed by this authorization record itself.
