# Test Item 007 — Protected regression

- Result: **PASS**
- Candidate: `575cdd139aea09d4f19b46ab6a6d38545f645c71`
- AC: 011

## Command and observed output

```text
.venv/bin/pytest -q tests/product/test_enh_e5_g00_navigation.py tests/product/test_enh_e5_g01_trial04_route_validation.py tests/product/test_enh_e5_g01_navigation_state.py tests/product/test_enh_e5_g01_navigation_shell.py
16 passed in 10.12s
```

These affected E5 tests cover canonical route parse/serialize, legacy normalization, catalog-driven shell/current stage behavior, and route validation. Test Item 002 additionally ran the existing E5 shell test alongside E6 tests. Test Items 004–006 independently exercised protected route/history behavior in Chromium.

Candidate diff inventory contains no `docs/wiki/requirement_definition/**` or ENH-E5 frozen evidence/contracts/reports modifications. Static audit found no Navigation Stage persistence.
