# ENH-E6 G01 Preflight Instruction

**Document class:** Operator Artifact / Execution Instruction  
**Self-containment:** MUST.

- Purpose: confirm existing browser E2E harness and reproduce ANOM-E5-001 under API READY + valid Project/canonical Analysis context before coding.
- Target Gate: `G01`
- Expected branch: `bugfix/ariadne_mvp_e6`
- Production behavior baseline of interest: `5a5ced9bd6a0e62027c4058eb66ec487719bde23` plus planning-only commits allowed; record actual observed HEAD.
- Destructive operations allowed: `NO` for source/history; Docker build/start and creation of disposable E2E Project fixture allowed.
- Result file: `40_operator_workflows/preflight/ENH-E6_G01_preflight_result.md`

## Checks

| Check ID | Check | Exact command / method | Expected |
|---|---|---|---|
| PF-001 | repository identity | `git branch --show-current; git rev-parse HEAD; git status --short` | target branch, recorded HEAD, no unexplained product edits |
| PF-002 | browser framework discovery | grep/find Playwright/Selenium/Cypress dependencies and browser_e2e files | existing Playwright Python/Chromium harness identified |
| PF-003 | compose/Docker invocation | inspect `compose.e1a.yaml`, `Dockerfile.browser-e2e`, existing runner documented command | current browser-e2e service and canonical command pattern resolved |
| PF-004 | clean runtime health | run browser-e2e current-source build and wait `#health` = `API READY` | API READY |
| PF-005 | valid Project context | create/select Project through supported UI and assert `/projects/<id>/data` | Project context established |
| PF-006 | normal Analysis entry negative control | click actual Explore entry without reload, record URL and Family/Stage button counts | canonical exploratory/profile route; pre-fix Family/Stage buttons absent reproducing anomaly |

## Abort conditions

- cannot establish API READY/current-source stack
- cannot create/select Project context
- observed source behavior differs materially such that intended anomaly is not reproduced
- repository has unexplained product implementation changes making baseline identity ambiguous

Do not modify product code during preflight.

## Required result schema

Record status, timestamp, observed branch/commit, check methods/exit or success, observed facts, PASS/FAIL/BLOCKED, environment mutations, conclusion, Gate execution eligibility. Preserve command output/screenshot paths where available.
