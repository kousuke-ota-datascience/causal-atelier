# ENH-E6 Preflight / Prerequisite Workflow

**Document class:** Authoring Guide  
**Status:** `COMPLETED FOR G01 START`

## 1. Purpose

Verify environment/tooling/browser/runtime prerequisites and obtain a clean pre-fix negative control independently of product implementation acceptance.

## 2. Semantics

Preflight PASS means G01 execution/verification prerequisites are available and defect negative control is reproducible. It does not mean product Gate PASS or FAIL of a future candidate.

## 3. Instruction authoring

`ENH-E6_G01_preflight_instruction.md` records purpose, baseline, non-destructive checks/methods, expected results, abort conditions, result schema.

## 4. Result authoring

`ENH-E6_G01_preflight_result.md` records observed branch/commit context, Playwright harness facts, API READY, Project/canonical route, Family/Stage child counts, environment mutations, eligibility.

## 5. Typical checks

Repository identity, existing browser framework, compose browser service, current-source Docker build, API/frontend/worker readiness, Project fixture, canonical Analysis route, observable shell negative control.

## 6. Gate blocking Browser E2E prerequisite — conditional

Applicable. Existing Playwright/Chromium `browser-e2e` compose path was confirmed. Future candidate canonical command must build current source, include ENH-E6 runner, wait API READY, own its Project/browser context/evidence path, and not depend on stale manual services/images.
