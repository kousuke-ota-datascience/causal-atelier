# 258 — G01/P05 abort session binding: Owner decision docket

**Date:** 2026-11-24 JST  
**State:** BLOCKED_CONTRACT_AMBIGUITY / ADDITIONAL_P02_EXCEPTION_OWNER_DECISION_PENDING  
**Decision ID proposed:** DEC-G01-P05-ABORT-SESSION-BINDING-01  
**START_SHA and verified remote HEAD:** 9420734f7968bfe85d72c535dd670ed85f753874  
**Active S10:** ef8e67ffa795e4ab00a4f86b600dac046548f5b4  
**S11:** DEC-G01-P05-002-S11-REAUTH-01 (combined_review/257)

## 1. Evidence and defect

At START_SHA, src/ariadne/interfaces/cli/local_causal/publication.py lines 84–89, 103–126 and 316–334 show that each _Sink holds its Publisher, and Publisher holds root, run_id, request_hash and policy, but neither holds its issuing Adapter nor an independently supplied session identity. Adapter.begin creates a new Publisher and returns its sink. Adapter.seal checks exact sink identity within its own Publisher and policy identity; neither establishes identity relative to the calling run. src/ariadne/capabilities/causal/ports/local_io.py lines 60–65 confirms existing begin/seal/publish signatures. AMD-002 §§2–3 requires abort(sink,reason) to reject cross-run/session substitution but provides no independent expected session input or issuer binding. IF 23_41 §4.1b, DD 30_62 §8.2a, P05 06 §6.4/6.6a, G01 07 abort matrix inherit that defect.

Two legitimate STAGING sinks from separate runs/adapters with the same policy pass the proposed nominal type, self-identity, policy and state checks. Even adding run_id/hash/root alone cannot distinguish concurrent attempts of the same run on the same root. Agent's reported ext4 experiment confirms the predicate collision; abort was not invoked and 207 existing tests do not prove new behavior. This is a contract defect in AMD-002, not a reason to relax cross-session rejection. No source change observed/reported. No exhaustive requirement or architecture review is justified.

## 2. Proposed A — explicit caller-owned session token with issuance binding

For Owner consideration, add internal nominal, opaque, process-local PublicationSessionToken (identity equality; fresh object per attempt, no public serialization; not an authentication credential). P05 creates one token before begin and retains it independently of the sink; also retains the validated run_id, request_hash and TrustedLocalRoot. Extend existing begin with a backward-compatible optional keyword session: PublicationSessionToken | None = None; new P05 always supplies non-null session. Preserve existing begin positional/keyword calling behavior and return type, scientific sink and concrete publication algorithm. At issuance, bind issuing Adapter object and the exact token to the run-scoped Publisher, e.g. immutable binding record installed before sink is returned. The new binding requires a minimal Publisher constructor/internal field addition or equivalent one-time issuance initialization, explicitly outside prior exception. No global registry, no filesystem/session persistence. Existing legacy begin with no session remains functional for begin/seal/publish but is ineligible for new abort facade. Define exact field placement and failure handling in AMD-003 after Owner approval, without changing concrete begin/abort/commit algorithms.

New abort signature proposal:
```python
def abort(self, *, sink: StagingArtifactSink, session: PublicationSessionToken,
          run_id: str, request_hash: str, root: TrustedLocalRoot,
          reason: str) -> None: ...
```

Require exact _Sink and publisher._sink identity, publisher's issuer is self, token identity is independently retained session, run_id/hash equality and exact root object identity, existing policy identity, and STAGING or VALIDATING only. All mismatches fail before delegation, no mutation of either session. No token extracted from candidate sink as expected input; do not accept null, forge by value or reuse a token across attempts (caller must create fresh identity; no global uniqueness registry). Scope is accidental/contract-level substitution in trusted in-process Python, not protection against arbitrary malicious code with access to private fields or the ability to replace ALL trusted caller inputs. Such a stronger security requirement would need separate Owner decision. Existing seal and publish retain their signatures and validation. Abort once on pre-publish failure, never after invoking publish; primary typed failure preserved, secondary cleanup diagnostic, quarantine and FD closure, not secure erasure.

## 3. Alternatives

B: additive begin_session method returns an opaque per-attempt receipt plus sink, with a one-time binding in the Publisher and independent receipt passed to abort. Existing begin signature untouched, but introduces another entrypoint and result type plus similar binding state; viable if exact old begin signature is inviolable. C: merely compare run/hash/root or policy with the sink; insufficient for same-run concurrent attempts and same-policy separate Adapters. D: remove independent cross-session rejection and treat sink as sole capability; weakens approved AMD-002, not recommended.

Recommend A because one optional keyword retains legacy callers and avoids a second lifecycle entrypoint; the trade-off is explicit additional P02 changes to begin signature/body and binding field/initialization. None is permitted by current S11. Both A and B require Owner approval. Do not change LocalArtifactPublisher.abort, concrete begin/validate/commit algorithms, seal/publish, scientific sink, prior tests or checkpoint history.

## 4. Narrow impact and validation

If A approved, amend IF 23_41 §4.1b, DD 30_62 §8.2/8.2a, P05 06 §6.4/6.6a, and G01 07 abort acceptance with AMD-E11-G01-P05-003; explicitly supersede only AMD-002 identity/signature and limited exception clauses. Prior historical 09 and completed P02 06/07 stay unchanged. Potential source paths remain src/ariadne/capabilities/causal/ports/local_io.py (token, begin optional keyword, abort signature) and src/ariadne/interfaces/cli/local_causal/publication.py (issuer/token binding, minimal initialization, Adapter.begin and abort). Exact constructor signature/field placement must be defined and audited before formal approval. No source edits now.

Require tests: same Adapter/different run; different Adapter/same policy; same Adapter/same run/hash/root concurrent distinct tokens; wrong root/hash; missing/foreign token; wrong sink; valid original pairing; repeated abort and PUBLISHING/COMMITTED/INDETERMINATE rejection; no mutation/FD closure of other session; original error preservation; legacy begin/seal/publish regression; existing P02/P01/P03/P04 and Product regression. Where seal may already have created staging marker, assert no FINAL committed marker or new final run (do not assert private quarantined marker absence after seal). The pre-existing final run must remain untouched. Prior 207 PASS not a new test result.

Retain P01 9bff61f0eae25236f95f31f2cd3e7c81291f0167, P02 3a76a0aa1698037354b284ba7b5a875300473ce6, P03 858c9f73366036a2d1445e558135cd521f611462, P04 7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6. No public E11 Schema, scientific semantics, independent G01_999 requirements, DEFERRED_PRODUCT_POLICY_BRIDGE unfulfilled dependency or uv.lock changes.

## 5. Decision required

Owner must approve additional bounded P02 exception before contract changes are finalized. Then prepare AMD-003 and static audit, obtain separate formal 09 approval, exact SHA S10 refreeze, distinct S11 limited authorization. No coding, test execution, formal 09, refreeze or authorization by this docket. Current P05 remains blocked.
