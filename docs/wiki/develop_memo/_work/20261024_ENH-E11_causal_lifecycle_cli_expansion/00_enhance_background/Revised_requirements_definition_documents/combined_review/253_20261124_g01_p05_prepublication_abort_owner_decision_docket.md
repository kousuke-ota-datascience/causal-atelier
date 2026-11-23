# 253 — G01/P05 pre-publication staging abort boundary: Owner decision docket

**Date:** 2026-11-24 JST  
**State:** `CONTRACT_BOUNDARY_DEFECT_CONFIRMED / P02_COMPLETED_PACKAGE_EXCEPTION_OWNER_DECISION_PENDING / P05_TRIAL01_BLOCKED`  
**Proposed Owner decision ID:** `DEC-G01-P05-P02-ABORT-BOUNDARY-01`  
**Current immutable S10:** `d5b7fab759b27ed8427a46256bac5ac8231e0c77`  
**Current P05 S11:** `DEC-G01-P05-001-S11-REAUTH-02` (`combined_review/252_20261124_g01_p05_001_limited_s11_owner_reauthorization_02.md`)  
**Coding Agent reported START_SHA:** `b64bb385cca120dd7af6154ea3cb87ae3b2b0ac3`  
**Completed P02 checkpoint:** `3a76a0aa1698037354b284ba7b5a875300473ce6`  
**Branch:** `feature/ariadne_mvp_e11`

## 1. Verifiable root cause

P05 `10_enhance_instruction/G01/06_G01_P05_cli_use_case_privacy.md` §6.4, step 9 directs Application `LocalCausalUseCase.run` to abort scoped staging if failure occurs before rename. Superior DD `30_62_local_execution_publication.md` §§1.6/3.4/3.5/8.3 and IF `23_42_local_result_manifest_artifact.md` §7 require pre-publication staging to be aborted/quarantined and distinguish `ABORTED` from post-rename `PUBLICATION_INDETERMINATE`. Completed P02 `06_G01_P02_atomic_publication_reader.md` §§6.3/6.4 already owns a concrete `LocalArtifactPublisher.abort(reason)` method. The implementation `src/ariadne/interfaces/cli/local_causal/publication.py` confirms that it releases handles, moves to `ABORTED`, and forbids `COMMITTED` or `INDETERMINATE` abort. It does not claim secure deletion of staged bytes (random private staging token quarantines residue).

But the Application-facing `ariadne.capabilities.causal.ports.local_io.LocalPublicationPort` in `src/ariadne/capabilities/causal/ports/local_io.py` exposes only `begin(*,run_id,request_hash,root)`, `seal(*,sink,manifest,privacy)`, `publish(*,bundle,root)`. `ariadne.scientific.ports.artifacts.StagingArtifactSink` exposes only `stage_bytes`. The completed `LocalPublicationAdapter` implements no `abort` facade operation. It maps the sink to its original Publisher by a private `_Sink._publisher` field, which Application is forbidden to access directly.

Therefore P05 cannot call a normative public Application Port method to terminate a live pre-rename staging session on failure in Discovery, staged validation or AMD-001 Manifest Factory. No existing contract-consistent call path can be identified; an Application import/cast of CLI `_Sink` or direct access to `_publisher` would violate approved dependency direction. The 207 previously reported existing focused + Product regression PASS and a partial ext4 experiment do not verify this not-yet-implemented P05 error path.

## 2. Owner options and recommended bounded completed-P02 exception

**A — RECOMMENDED: scoped additive Application Port `abort` and P02 concrete facade delegation.** Amend the *internal* Application `LocalPublicationPort` signature to add:

~~~python
def abort(self, *, sink: StagingArtifactSink, reason: str) -> None: ...
~~~

The CLI `LocalPublicationAdapter.abort` must validate the sink is the exact live `_Sink` owned by this facade's policy-bound `LocalArtifactPublisher` and invoke its already implemented `abort(reason)`. Do not accept an arbitrary/adversarial sink by structural similarity or an external publisher instance with incompatible policy. Retain the P02 concrete state machine: pre-rename only (including before commit's actual no-clobber rename), handle release and quarantine; no destructive cleanup of potentially committed/indeterminate run. Crucially: the Agent must not assume `PUBLISHING` always means that rename has not occurred. Because the existing concrete `abort` blocks only `COMMITTED/INDETERMINATE`, facade and P05 must avoid calling abort after `publish` begins or when rename outcome could be uncertain; never turn a post-rename failure into deletion/abort. Any evidence that concrete Publisher's abort-state constraints are insufficient must be escalated before modifying P02 concrete behavior. Distinguish original failure classification from best-effort cleanup failure, and never fabricate successful rollback.

The new operation is an internal Port contract addition, not a change to P02 `begin/seal/publish` method signatures, published E11 wire, privacy authority, scientific meaning or external CLI API. **Nevertheless it explicitly modifies a completed P02 Port and concrete Adapter**; Owner's A approval must name this bounded P02 exception, with proof of backward compatibility and appropriate focused regression. P01/P03/P04 remain immutable.

**B — relocate abort ownership into a new P05-specific control Port.** This avoids modifying the existing `LocalPublicationPort` Protocol declaration but still requires new CLI-side access to the completed P02 Publisher via a dedicated lifecycle capability, adds dependency injection and has a greater risk of duplicating publication lifecycle authority. Avoid unless A has an evidenced incompatibility.

**C — allow leave-in-place private staging after pre-rename failure with no explicit abort.** Existing Publisher instances can be abandoned at the end of scope, but this does not establish a deterministic explicit `ABORTED` state or handle-release contract. It weakens P05 and DD/IF pre-publication failure contracts. **Not recommended** absent an explicit Owner waiver of the cleanup-state semantics.

## 3. Contract, code and test impact if A is approved

Normative documents to amend minimally via `AMD-E11-G01-P05-002`:
1. `00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md`: internal `LocalPublicationPort.abort(*,sink,reason)` with same-run/policy exact sink, no public wire changes.
2. `00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md`: lifecycle call on exception from `run` after begin; pre-rename-only vs indeterminate/committed boundary.
3. `10_enhance_instruction/G01/06_G01_P05_cli_use_case_privacy.md`: call Port abort in pre-rename exception path; no CLI concrete import, no committed cleanup, typed failure preservation.
4. `10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md`: independent positive and negative cleanup tests, same sink run/policy, no double abort, state/FD/Marker/final-run, post-rename indeterminate protection and pre-existing P02 regression.
5. An explicit **bounded exception** to protected completed P02 `src/ariadne/capabilities/causal/ports/local_io.py` and `src/ariadne/interfaces/cli/local_causal/publication.py` for additive Port/facade method only, as part of later authorized coding or an approved remediation step; preserve completed P02 instructions, checkpoint and previous source-history immutability. Existing P02 `LocalArtifactPublisher.abort(reason)` is to be reused without modification unless a new separate defect/Owner decision establishes necessity. The P02 ownership of publication remains exclusive.

Potential independent regression set: existing P02 begin/seal/publish, privacy re-evaluation, FD/root identity, no-clobber, interleaved runs, strict Reader and legacy Product suite; new abort-before-seal, abort-after-validation-before-publish, Factory failure, wrong sink and policy, repeated abort, attempts on COMMITTED/INDETERMINATE and exception-in-cleanup; no Marker/final-run for pre-rename failure, and no deletion/false success if rename potentially occurred. Physical ext4 test is required where specified. Do not weaken expected results to match existing implementation limitations.

Requirement definition (10), logical data design (21), Product basic design (22), published E11 Schema Version, scientific contracts, Product v2, `uv.lock` and G01_999 acceptance need no change. The P01-specific prior exception does not authorize this P02 exception.

## 4. Release controls and limits

This docket is **not** Owner adoption of A, **not** a formal 09 contract amendment or approval, and **not** S10 refreeze or S11 reauthorization. No normative document, test or code was changed by the decision docket.

Owner is requested to decide `DEC-G01-P05-P02-ABORT-BOUNDARY-01=A` **with explicit permission for the narrowly scoped completed P02 additive Port/Adapter extension**, while preserving the original concrete `abort` semantics and all P01–P04 protected source/checkpoints except the specifically approved P02 change. After decision, prepare and audit `AMD-E11-G01-P05-002` coherently across IF/DD/P05 06/G01 07, obtain separate formal 09 Owner approval, separate exact SHA S10 refreeze and separate G01/P05/Trial01 S11 reauthorization **before any changed-source coding**. If additional concrete Publisher changes are discovered necessary, stop for an additional Owner disposition.

Until such reauthorization P05 remains `BLOCKED_CONTRACT_AMBIGUITY`. `DEFERRED_PRODUCT_POLICY_BRIDGE` remains `UNFULFILLED` and independent `G01_999` requirements remain unchanged.
