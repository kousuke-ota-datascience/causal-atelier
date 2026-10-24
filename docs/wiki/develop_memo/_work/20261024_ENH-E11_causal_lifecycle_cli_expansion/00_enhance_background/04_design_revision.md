# ENH-E11 — 設計書改定案

**Document class:** Planning / Decision Artifact  
**Status:** DRAFT TARGET DESIGN / ARCHITECTURE REVIEW PENDING

## 1. Source design documents

- `docs/wiki/requirement_definition/21_logical_data_design.md`
- `docs/wiki/requirement_definition/22_product_basic_design.md`
- `docs/wiki/requirement_definition/23_api_interface_design.md`
- `docs/wiki/requirement_definition/30_detailed_design.md`
- Existing standalone CLI: `src/ariadne/interfaces/cli/`, Scientific Core:
  `src/ariadne/scientific/`, inference engine: `src/ariadne/causal/inference/`.
- Product domain current `analysis_spec.py` and scientific core ports.

## 2. Proposed design delta

### Scientific Core boundaries

- **Causal context:** reuse current Causal Question/Design/Graph schemas where
  compatible; add a local versioned identity/provenance document when Product DB
  owner cannot be reused without Worker/DB integration.
- **Identification:** normalize native/DoWhy backend result to Ariadne-native
  identified/requires-review/not-identified/unsupported taxonomy; assumptions
  and source graph must be attached. No library objects in canonical payload.
- **Graph discovery:** FCI, PCMCI families register algorithm ID, CI test,
  parameters and backend metadata; ensure typed edge endpoints, lag metadata and
  exact round-trip serialization. No forced DAG conversion.
- **Estimation:** preserve existing `ipw` / `aipw`; introduce capability-oriented
  estimator interface for CATE and design-specific estimators without forcing
  all results into binary-treatment ATE/ATT fields.
- **Refutation/sensitivity:** method-specific, provenance-rich scientific result
  with upstream effect identity. Keep existing baseline method codes.
- **Temporal/quasi-experimental:** distinct validated design contract for panel,
  time, running variable, instrument and donor pool instead of extending all
  cross-sectional estimator input fields indiscriminately.

### Local output model

- Validated CLI config → scientific method adapter → result/diagnostics →
  durable local files → manifest (inputs, hashes, parameters, versions, seed,
  split identity, statuses, artifact hashes). No DB identity requirement.
- Use existing CLI adapter/manifest helpers where suitable. New schema versions
  must preserve legacy `config_version=2.0` readers; version-bump semantics
  subject to Architecture Review.
- Large per-unit CATE results as Parquet, concise summary as JSON, readable
  design-specific scientific audit as Markdown/JSON; do not expose all rows in
  a single control-plane response.

## 3. Authority / ownership changes

**Proposed, not frozen:**

- Domain owns portable scientific question/design/estimand/invariant types;
  Scientific Core adapters own optional backend calls, validation and numeric
  method results; CLI owns local path resolution and file writing.
- Library objects/pickles are not domain/result authority; baseline current
  Product Graph/Result resources remain authoritative for existing Web path.
- Method-specific design identities must be capable of being recreated from
  local spec+manifest without relying on Product DB.

## 4. Runtime / data-flow changes

- **Added:** local CLI method selections and validated operation spec for
  DoWhy/FCI/EconML/Tigramite and quasi-experimental estimators.
- **Preserved:** current Product API → Worker → DB orchestration for existing
  functionality; no addition to these paths during ENH-E11.
- **Preserved:** navigation state is independent from CLI/runtime execution;
  Navigation Stages are not 1:1 with scientific execution stages.
- **Error taxonomy:** `NOT_IDENTIFIED`, `REQUIRES_REVIEW`, poor support and
  violated eligibility produce scientific results; missing dependency/invalid
  config remains a typed technical/configuration error.

## 5. Persistence / migration changes

- No new E11 database migrations or new server-side persisted resources.
- Introduce/add versioned **local** file schemas and checksums with atomic
  write expectations. Before approval decide handling partial write/retry and
  confidentiality of row-level CATE artifacts.
- Existing `ArtifactStore` abstractions and persisted Product reads remain
  unchanged; portable mapping into future API/DB is a subsequent Enhancement.

## 6. Compatibility / rollout strategy

- Retain `ipw`, `aipw`, existing `GraphType` semantics, and existing CLI
  config contracts; use explicit new option names to prevent ambiguous
  stabilized/normalized weight interpretation.
- Backend imports are lazy/optional, with named extras and precise unavailable
  messages. Record effective package/python versions in the manifest.
- Deterministic lower-layer scientific validation is the primary test proof;
  don't add Browser E2E for standalone CLI functions.
- If existing E9/E10 test behavior is altered intentionally, record exact
  semantic change and preserve current invariant coverage (do not simply skip).

## 7. Temporary architecture / Transition Debt candidates

| Debt candidate | Why acceptable for CLI-first E11 | Closure condition |
|---|---|---|
| No API/Worker/DB integration for new methods | Explicit owner scope boundary | Follow-on enhancement defines Product authority, design and integration tests |
| Local-file identity vs Product version resources | No new DB migration permitted | Approved mapping/linkage policy before future persistence integration |
| Method-specific artifact schemas | Heterogeneous design outputs differ scientifically | Stable versioned schema and future adapters, not a fictitious universal scalar estimate |
| Full library backend portability | Engine versions/platform constraints | Optional dependency/support matrix and reproducible benchmark evidence |

## 8. Gate implications

The draft G01–G10 semantic claims in `01` and the Issue→Gate matrix in `05`
require Architecture Review to decide stable source-of-truth, graph ownership,
estimator result typing, local artifact identity, privacy and dependency order.
No Gate contracts are currently frozen.

## 9. Mandatory Architecture Review decisions

1. Graph/Question/Design ownership and versions in a DB-free local run.
2. Scientific result vs diagnostic vs artifact boundaries.
3. Identification gating and nonidentifiable-result semantics.
4. `TIME_SERIES_GRAPH` / endpoint/lag compatibility.
5. CATE and local design-specific estimand representations.
6. Method-specific inference and benchmark contract selection.
7. Dependency version matrix and installation isolation.
8. CLI versioning, filename/path safety, artifact atomicity and privacy.
9. Future API/Worker/DB migration path with no premature implementation.
