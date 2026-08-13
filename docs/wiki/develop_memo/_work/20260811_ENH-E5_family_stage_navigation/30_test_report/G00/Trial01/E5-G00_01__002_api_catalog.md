# ENH-E5 G00 Trial 01 — Test Item 002: API and canonical catalog

## Purpose

Independently verify AC-G00-001 through AC-G00-005: the read-only endpoint and exact navigation catalog / response field contract.

## Command and target

```text
TEST_TARGET=61e5749387a152a793c1dddaf6fd6cf2c49751aa
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 \\
uv run pytest -q tests/product/test_enh_e5_g00_navigation.py tests/product/test_architecture.py
```

## Raw evidence

```text
..........                                                               [100%]
10 passed in 3.16s
```

The API assertion invoked `GET /api/v1/navigation/analysis` and asserted HTTP 200 plus complete JSON equality. The asserted response has only top-level `schema_version` and `families`, uses `schema_version: analysis-navigation/1`, and contains the exact three ordered Families, slugs, defaults, stage IDs/slugs/labels/orders stipulated by Gate 07. It thereby also detects forbidden `schema` or generic `id` field drift.

An independent catalog import observation produced:

```text
EXPLORATORY/exploratory/profile: profile, data-quality, distribution, relationships, comparison, findings
PREDICTIVE/predictive/setup: setup, train, predict, metrics, explainability, model-management
CAUSAL/causal/setup: setup, discovery, identification, estimation, effects, diagnostics, sensitivity
```

## Result

**PASS.** AC-G00-001, AC-G00-002, AC-G00-003, AC-G00-004, and AC-G00-005 satisfy the exact Gate 07 values.
