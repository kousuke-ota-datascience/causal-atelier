# Browser E2E Gate Policy — ENH-E7 instance

Browser E2E proves a small number of real cross-layer critical user journeys. It is not the primary proof for detailed route taxonomy, DOM ownership, validation or domain rules.

## Canonical suite budget

ENH-E7 plans three blocking journeys across the enhancement:

1. G01 Project Management journey.
2. G02 Analysis main journey.
3. G02 Analysis history / legacy compatibility journey.

Detailed correctness belongs in lower-level tests.

## Environment

- use the repository's established browser E2E harness.
- bootstrap from current source, not a stale image.
- record relevant service/build identity when a runtime mismatch is suspected.
- wait on semantic UI/network conditions, not arbitrary sleeps where avoidable.

## Evidence

For failure capture:

- actual page/URL/state.
- expected state.
- screenshot/trace/video when available.
- browser console/page errors.
- relevant network request/response.
- API/service logs when relevant.
- exact failing synchronization/assertion.

## Classification

- PRODUCT_INTEGRATION_DEFECT -> may support FAIL.
- TEST_IMPLEMENTATION_DEFECT -> BLOCKED until test is corrected.
- TEST_ORCHESTRATION_DEFECT -> BLOCKED.
- TEST_ENVIRONMENT_DEFECT -> BLOCKED.
- UNKNOWN -> BLOCKED unless product violation is independently verified.
