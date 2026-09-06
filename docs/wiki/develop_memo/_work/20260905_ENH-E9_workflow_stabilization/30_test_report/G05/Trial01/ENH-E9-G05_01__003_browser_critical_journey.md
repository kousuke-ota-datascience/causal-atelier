# ENH-E9 G05 Trial 01 Test Item 003 — Browser critical causal journey

> **Document class:** Evidence Artifact

- Status: BLOCKED / BROWSER_E2E
- Fixed Candidate: `2959afcf03261cba50edf13bf334038519b6c476`
- Tested state: `7c6a97953615c98c36d3bf1d5afa1af005771437`
- 07: `10_enhance_instruction/G05/07_Ariadne_ENH-E9_G05_test_instruction.md` (FROZEN)
- Timestamp: 2026-09-06T09:40:48Z

## Command and raw evidence

```bash
docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e9-g02-verify --profile e2e run --build --rm --no-deps --entrypoint python browser-e2e tests/enhancement/enh_e9/g05/browser_e2e/run_critical_causal_journey.py
```

Runner exit: `1`.

```text
last checkpoint: discovery-candidate-adopted-fixed
route: /projects/64fb3485-9727-4264-85d4-f58b7452558a/analysis/causal/identification
failure: #refresh-inference resolved but was not visible after 30 seconds
```

## Browser diagnostic classification

- JSON: `test-results/browser_e2e/enh-e9-g05-critical-causal-journey-evidence.json`
- Trace: `test-results/browser_e2e/enh-e9-g05-critical-causal-journey-trace.zip`
- Screenshot: `test-results/browser_e2e/enh-e9-g05-critical-causal-journey-failure.png`
- Video: `test-results/browser_e2e/enh-e9-g05-critical-causal-journey-video/`
- Console: `[]`
- Classification: `TEST_IMPLEMENTATION_DEFECT`

The runner correctly reached Project, Dataset, Discovery, and adopted FIXED Graph. It then submits Identification and confirms its execution/results through the API, but clicks `#refresh-inference` before navigating to Estimation. Current `index.html` places that control inside `data-causal-stage-surface="estimation"`; screenshot shows Identification is active and the control is hidden. This is stale runner sequencing before the required selected-Identification→Estimation and Effects/Diagnostics assertions. It is not a verified product violation, but it prevents product correctness determination for the mandatory cross-layer journey.

Test Agent production/migration/dependency changes: NONE.
