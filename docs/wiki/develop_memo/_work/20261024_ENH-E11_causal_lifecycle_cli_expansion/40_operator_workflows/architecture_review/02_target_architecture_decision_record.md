# ENH-E11 Target Architecture Decision Record

**Document class:** Planning / Operator Artifact  
**Decision status:** PROPOSED / **NOT APPROVED**  
**Decision authority:** Human architecture owner (pending)  
**Timestamp:** Not issued

## 1. Context

8/4 historical Phase1–3 methods were reduced by the 9月ENH-E11
Foundation-only HANDOFF_DRAFT, and later re-adopted for CLI-only implementation.
The Product has existing current semantics for ATE/ATT, Graph and basic causal
stages. New heterogeneous/time-series/quasi-experimental methods require a
separate, validated portable interface.

## 2. Current architecture facts

Refer to direct source evidence listed in `01_architecture_discovery.md`.
Current ScientificCoreAdapter emits typed result descriptors, CLI has strict
config schema/manifest paths, and E9 scientific diagnostics have defined
weighting applicability. These observed facts do not resolve source-of-truth
ownership for new local design types.

## 3. Proposed decision

- Domain defines library-independent Question/Design/Graph/Estimand/Result
  semantics; Scientific Core adapters own library method execution and method
  validation; local CLI owns paths/manifests. Confirm actual import directions.
- Phase1/2/3 capability families share typed envelopes but retain method-specific
  design schema and scientific statuses: no fake universal `ATE` for CATE/RD/LATE.
- Optional backend imports and package versions are isolated per method.
- New E11 outputs persist as local versioned files only; no server DB migration.
- Full test source/candidate/evidence identities are protected by Workflow,
  not by GitHub Issue checkboxes.

## 4. Proposed canonical authorities

| Concern | Proposed authority after CLI-only ENH-E11 |
|---|---|
| Local Question/Design/Graph specification | Versioned validated local spec + content hash, mapped to current canonical semantics |
| External engine objects | Ephemeral Scientific Core adapter memory, not canonical payload |
| Scientific estimates and negatives | Ariadne result schema with method-specific estimand/status/warnings |
| Large CATE / temporal / donor data | Durable local Parquet/JSON artifact with schema version, manifest checksum |
| Backend versions, seeds/splits, inputs | Local run manifest, reproducible at fixed SHA |
| Existing Product DB resources | Unchanged existing Product authority; future integration separate |
| Gate accepted state | Independent canonical 999 Gate Decision |

## 5. Proposed invariants and verification

| ID | Invariant | Primary verification |
|---|---|---|
| ADR-I01 | Domain does not import DoWhy/EconML/Tigramite types | Import/architecture contract |
| ADR-I02 | PAG circles and temporal lag semantics never silently become DAG | Graph round-trip/negative test |
| ADR-I03 | Identification and eligibility are distinct from estimation | Known-truth/nonidentified test |
| ADR-I04 | IPTW weights, DR propensity components and synthetic donor weights are not conflated | Estimator/diagnostics contract |
| ADR-I05 | CATE, LATE, RD local effects are not relabeled ATE without proof | Design/estimand schema contract |
| ADR-I06 | Missing optional backend does not kill unrelated CLI methods | Dependency-unavailable integration test |
| ADR-I07 | File outputs are replayable by version/input/split/seed/artifact hashes | Fixed-SHA reproducibility benchmark |
| ADR-I08 | No new E11 API, Worker, DB or UI runtime dependency | Architecture contract test |

## 6. Constraints

- Preserve current `causal-analysis-spec/2` and standalone CLI configs or an
  approved explicit version migration.
- No arbitrary import path/pickle upload and no unrestricted per-unit CATE
  exposure by default.
- Method-specific assumptions and negative statuses must be human-readable.

## 7. Removed / deprecated paths

None approved. Do not remove existing Product runtime paths or rewrite E9/E10
stable components for convenience.

## 8. Transition debt and closure

New local method results do not become Product persisted DB resources in E11;
explicit future API/Worker/DB mapping and migration will be a follow-on project.
Avoid a hidden unbounded compatibility promise.

## 9. Alternatives considered

- Full simultaneous Web API/Worker/DB/UI integration: intentionally excluded by
  owner due to development and Browser E2E cost.
- DoWhy/EconML types as canonical Result: rejected candidate because it couples
  domain contracts to external libraries and serialization versions.
- All methods forced into ATE/ATT `EstimationInput`: rejected candidate because
  the causal estimands and design validation differ scientifically.
- Implement Phase 1 only as the 9月 draft: superseded in planned scope by later
  owner direction but preserved as historical provenance.

## 10. Consequences / risks

New versioned file schema, scientific validation benchmarks and optional
dependency support matrix are required. Full cross-layer Product integration
will be separate and cannot be claimed complete by E11.

## 11. Approval

- Status: **PENDING**
- Authority: human owner / architecture owner
- Evidence: not yet provided
- No Gate 06/07 freeze or implementation start is authorized by this proposal.
