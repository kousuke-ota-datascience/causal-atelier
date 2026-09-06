# ENH-E9 G02 Trial 01 Test Item 006 — Reverification Browser cross-layer connectivity

> **Document class:** Evidence Artifact

- Status: PASS (BROWSER_E2E)
- Fixed Trial Candidate SHA: `8cf70523093efa53b59a7de2c655f9755dbceb8d`
- Tested Repository State: `7a142e306bc3c921e1b6be81e6f20e58ac223d80`
- 07 Contract: `10_enhance_instruction/G02/07_Ariadne_ENH-E9_G02_test_instruction.md` (FROZEN)
- M02 repair record: `00_enhance_background/08_test_architecture_migration/05_execution_record.md`
- Timestamp: 2026-09-06T05:14:21Z

## Purpose / command

Mandatory final Browser verification: Project List → New Project → current Analysis/Discovery route → Discovery → candidate comparison → adopted FIXED Graph. Items 004–005 passed first.

```bash
docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e9-g02-verify --profile e2e run --build --rm --no-deps --entrypoint python browser-e2e tests/enhancement/enh_e9/g02/browser_e2e/run_discovery_candidate_adoption.py
```

Exit code: `0`.

```text
{"evidence": "/evidence/enh-e9-g02-discovery-candidate-adoption-evidence.json", "status": "PASS"}
checkpoints: project-list, project-created, dataset-registered, current-analysis-discovery-route,
discovery-results-and-candidates, graph-comparison, adopted-fixed-graph
Discovery executions: 2; comparison candidates: 2
adopted FIXED Graph Version: 11900828-a74d-4479-9cd7-e75954ceb9f8
console: []
```

## Diagnostics / evaluation

- JSON: `test-results/browser_e2e/enh-e9-g02-discovery-candidate-adoption-evidence.json`
- Trace: `test-results/browser_e2e/enh-e9-g02-discovery-candidate-adoption-trace.zip`
- Screenshot/video: `test-results/browser_e2e/enh-e9-g02-discovery-candidate-adoption.png`, `...-video/`
- Failure classification: N/A (PASS).

The repaired runner reached all required current-UI checkpoints and modal-local adoption feedback identified a returned FIXED Graph. This proves cross-layer connectivity; detailed graph/scientific semantics remain item 005's contract-test responsibility.

| Criterion | Result |
|---|---|
| Mandatory Browser journey | PASS |
| Candidate comparison | PASS (2 candidates) |
| Adoption result | PASS (returned FIXED Graph identified) |

Production, migration, dependency changes by Test Agent: NONE.
