# 259 — AMD-E11-G01-P05-003 static contract and implementability audit

**Date:** 2026-11-24 JST
**Owner design decision:** DEC-G01-P05-ABORT-SESSION-BINDING-01=A (docket 258)
**State:** AUTHOR_STATIC_AUDIT_PREPARED / FORMAL_09_PENDING / S10_REFREEZE_PENDING / S11_REAUTH_PENDING / P05_BLOCKED
**Current immutable S10:** ef8e67ffa795e4ab00a4f86b600dac046548f5b4
**Last blocked START_SHA:** 9420734f7968bfe85d72c535dd670ed85f753874

## 1. Scope and evidence
Read actual source at START_SHA: src/ariadne/interfaces/cli/local_causal/publication.py lines 84–89, 103–126, 247–334; src/ariadne/capabilities/causal/ports/local_io.py lines 60–70. Review only directly related IF 23_41 §4.1b, DD 30_62 §3.2/3.3/8.2/8.2a, P05 06 §6.4/6.6a and G01 07 abort cases, plus AMD-002/003. The issue is missing independent expected session and issuer data, not a scientific or public wire defect. The reported 207 historical test passes and ext4 predicate observation do not constitute new abort tests.

## 2. Static realizability
| Predicate | Expected independently retained | Candidate existing/new data |
| --- | --- | --- |
| nominal sink | _Sink class | type(sink) |
| original sink | original Publisher sink | sink is p._sink |
| issuer | Adapter self | new p._issuer |
| attempt | fresh PublicationSessionToken before begin | new p._session |
| run | validated run_id | existing p.run_id |
| hash | validated request_hash | existing p.request_hash |
| root | context.root exact object | existing p.root |
| policy | Adapter injected policy | existing p.permission_policy |
| lifecycle | STAGING or VALIDATING | existing p.state |

Both missing fields can be initialized in existing Publisher constructor before creation of its _sink. Optional keyword-only issuer/session defaults preserve existing four-argument constructor calls. Adapter.begin receives token before allocation, validates nominal type, passes self and token into constructor, invokes unchanged concrete begin. No registry, setter, second publication engine, or modification of concrete abort/validate/commit/begin algorithm required. Existing policy and root objects are available without CLI imports in Application. Source uses postponed annotations; no import cycle is needed by defining token in existing local_io and importing it into CLI publication. Existing seal/publish unchanged.

Counterexamples: wrong Adapter with same policy fails issuer; same Adapter different run fails run/token; identical run/hash/root with distinct fresh attempts fails token identity; distinct root object fails root identity even if its verified identity is equal; legacy session=None cannot match exact nominal token; invalid state fails before delegation. This is a logical proof conditional on fresh tokens and sequential lifecycle calls within one session. No runtime execution or test PASS. Arbitrary private-field tampering, deliberate token reuse and substitution of every trusted input are outside the approved caller contract. Distinct sessions may interleave. Same-session concurrent calls would require separate synchronization and are not promised by this internal contract.

## 3. Contract concordance
IF: canonical token and begin/abort signature, independent expected values and complete predicate.
DD: constructor/field table and §8.2a exact storage, type guards, issuance and state predicate.
P05 06: fresh token, independent run/hash/root, begin eligibility and disabling before publish invocation, single abort attempt.
G01 07: independent substitution matrix, valid STAGING/VALIDATING, legacy begin regression, no mutation of either session on rejection, original failure preservation, real FS.
AMD-003: supersedes AMD-002 only in identity/signature/issuance and exception envelope; historical AMDs remain untouched. AMD-001 Factory remains binding.
No final committed marker/new final run on pre-publish failure; a private staged marker after seal may exist. Existing final run preserved. No secure-erasure guarantee. No Application abort after publish invocation. Original Publisher owns internal failures and indeterminate outcomes.

## 4. Bounded implementation exception
Later S11 alone may permit token and begin/abort in local_io.py, necessary imports, private issuance fields and optional constructor args in LocalArtifactPublisher, Adapter.begin/abort in publication.py. No other completed P02 code/instruction/test changes; existing concrete begin/stage_bytes/validate/commit/abort and Adapter seal/publish unchanged. Existing callers compatible at call level; actual behavioral compatibility and structural test-double compatibility must be demonstrated by focused and Product regression. If a protected caller/test modification proves necessary, stop for separate Owner disposition. No requirement, logical data, basic design, public E11 schema, science or uv.lock change.

Protected checkpoints: P01 9bff61f0eae25236f95f31f2cd3e7c81291f0167; P02 3a76a0aa1698037354b284ba7b5a875300473ce6; P03 858c9f73366036a2d1445e558135cd521f611462; P04 7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6. Independent G01_999, actual FS/Reader/science, Product regression and DEFERRED_PRODUCT_POLICY_BRIDGE UNFULFILLED dependency remain unchanged.

## 5. Verdict and release controls
Specific identity predicate is constructible from existing fields plus authorized new issuer/session fields under the stated caller assumptions. Author static contract audit only; no source implementation, executable proof, or independent PASS. Require formal 09 Owner approval, separate exact SHA S10 refreeze and distinct S11 authorization before coding. No broader claim that every P05 contract is free of blockers.
