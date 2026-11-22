# S05 B04 — versioned optional Backend candidates (2026-11-22)

Status: OFFICIAL_RELEASE_CANDIDATES_ONLY / NOT_RESOLVED / NOT_RUNTIME_PROBED / SCIENCE_BLOCKED.

| Isolated profile | Candidate package(s) | Release evidence | Missing proof |
|---|---|---|---|
| ENV-BASE | causal-learn==0.1.4.8; statsmodels==0.14.6 | Current existing uv.lock | Python 3.12 actual FCI/IV and native source tests |
| ENV-DOWHY | dowhy==0.14 | PyPI release with Python >=3.9,<3.14 | Separate compatible resolution; CausalModel graph/identification; binary-IV conditional complier LATE mapping |
| ENV-ECONML | econml==0.17.1 | PyPI Nov 18 2026 CPython3.12 Linux wheels | Tagged dependency resolution, eight Method fit/CI probe; public docs currently 0.16.0 |
| ENV-TIGRAMITE | tigramite==5.2.10.1 | PyPI Jan 14 2026 py3 wheel, GPLv3+ | CPython3.12 import/PCMCI+/LPCMCI graph output and licensing obligations; no explicit PyPI Requires-Python |

Targets: ENV-BASE, ENV-DOWHY, ENV-ECONML, ENV-TIGRAMITE isolated and independent; not ENV-COMBINED. A wheel existing is not successful dependency resolution, a symbol existing is not a fitted target's API, and a fitted estimator existing is not scientific effect/CI validity. Do not mark any effective Backend as supported from this evidence.

Project target Python >=3.12,<3.13. Current review runtime Python3.13.5, numpy2.3.5, scipy1.17, sklearn1.8, pandas2.2.3; optional imports absent and network package fetch unavailable. The target Python3.12 isolated environments and actual dependency resolution are inaccessible here. No pyproject/uv.lock/source/test changes are authorized before Coding Authorization.

Execution contract: use review-only combined_review/tools/e11_backend_probe.py separately in exact pinned environments; require version match from distribution metadata plus actual symbols/signatures and Method-specific fit/inference positive+negative fixtures, record source/fixture+lock hashes. A pure API probe is not science acceptance.

Sources: https://pypi.org/project/dowhy/0.14/ ; https://pypi.org/project/econml/0.17.1/ ; https://pypi.org/project/tigramite/5.2.10.1/ ; https://www.pywhy.org/EconML/reference.html ; https://jakobrunge.github.io/tigramite/ .

DEC-02 remains conditional: if solver or actual inference fails, offer evidence-based options without silently dropping a Method.
