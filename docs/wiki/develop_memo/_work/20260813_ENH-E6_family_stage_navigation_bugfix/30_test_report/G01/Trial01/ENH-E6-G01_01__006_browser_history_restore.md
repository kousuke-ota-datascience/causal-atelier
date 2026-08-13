# Test Item 006 — B03 history and reload restore

- Result: **PASS**
- Candidate: `575cdd139aea09d4f19b46ab6a6d38545f645c71`
- AC: 003, 004, 010

## Command and raw evidence

Executed the canonical Docker/Chromium command recorded in Test Item 004. The JSON evidence records `B03-direct-reload-history-restore: PASS` and no console errors.

The runner uses actual Explore, Family, and Stage controls, then `page.go_back`, `page.go_forward`, and `page.reload`, each followed by assertions of canonical URL, selected Family, selected Stage, and active presentation. Recorded route sequence:

```text
/analysis/exploratory/profile
/analysis/predictive/setup
/analysis/predictive/train
```

Final snapshot preserved `/analysis/predictive/train`, Predictive as the sole selected Family, Train as current Stage, active `predictive` presentation, 3 Family controls, and 6 Predictive-local Stage controls. Evidence/artifacts are under `test-results/browser_e2e/enh-e6-family-stage-navigation-*`.
