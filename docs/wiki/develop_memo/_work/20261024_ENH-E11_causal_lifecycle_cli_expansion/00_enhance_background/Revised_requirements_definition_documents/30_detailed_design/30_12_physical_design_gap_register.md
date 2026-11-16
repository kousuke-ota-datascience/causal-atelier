# 30.12 — Physical Detailed Design Template & Coverage Gap Register

**Status:** `DRAFT / PHYSICAL_DESIGN_PARTIAL / ADR_NOT_REVIEWED`

## 1. Per-class physical design checklist (mandatory)

| Dimension | Exact fields to record |
|---|---|
| Identity | Fully qualified Python symbol, package/module path, author/owner, document ID, source commit/blob, implementation status |
| Role | Responsibility/anti-responsibility, caller/callee, dependency direction, Port/Adapter relationship |
| Data | Each constructor/instance/class field, Python annotation, default, null, immutability, provenance, validation, privacy |
| Constructor | Exact signature, factory options, init ordering, resource ownership and lifecycle |
| Method | Visibility, signature with annotations, return type, pre/postcondition, mutating side effect, exceptions/error codes |
| Algorithm | Steps/pseudocode, branch conditions, numerical tolerances, precision, reproducibility/seed and complexity/cost |
| Concurrency/I-O | Thread/process assumptions, transaction/atomic boundary, retry/idempotency/rollback, paths and filesystem security |
| Serialization | Schema field names, version, canonicalization, reader/writer roundtrip, backward compatibility, checksum |
| Dependency | External methods, installed version/API, optional fallback policy, licensing boundary, environment profile |
| Verification | Test file/test ID, unit/contract/negative/integration/science, FR/NFR/AR & Gate trace, evidence SHA |

## 2. Split baseline document versus complete physical design

`30_01`〜`30_09` contain **lossless, reorganized existing 30_detailed_design.md text**. They are not all full class-level physical specifications. Only 30_10 source-reviewed representative classes have extracted field/method contracts; 30_11 is a candidate E11 class design. These statuses must remain separate until source audit and ADR approve each entry.

| Baseline topic | Split document | Remaining physical details / status |
|---|---|---|
| Domain / Resource / Navigation / Schema | 30_01 | Exact Python class signatures, value constructors, schema sources and tests; `SOURCE_AUDIT_REQUIRED` |
| Planning / Validation / Execution | 30_02 | Full Executor / StageExecution / Planner / bindings lifecycle, class test trace; **partial source examples in 30_10** |
| Project Management / Workspace | 30_03 | Concrete controller/state/store/react component contracts, errors, source; `SOURCE_AUDIT_REQUIRED` |
| Exploratory / Causal | 30_04 | Capability per-method classes, Graph/Result adapters, typed IO, science test traces; `SOURCE_AUDIT_REQUIRED` |
| Predictive workflows | 30_05 | Model registry, fitting, scikit/LightGBM adapters, coercion/validation classes; `SOURCE_AUDIT_REQUIRED` |
| Predictive advanced/XAI | 30_06 | SHAP/LIME exact provider symbols, method signatures, artifacts; `SOURCE_AUDIT_REQUIRED` |
| Result / Frontend | 30_07 | Comparators, lineage, routing and async presentation concrete symbols; `SOURCE_AUDIT_REQUIRED` |
| Persistence / Security / Failure | 30_08 | Atomic transaction/authorization/exception mapper and concrete negative tests; `SOURCE_AUDIT_REQUIRED` |
| Verification / history | 30_09 | Test locations and evidence mapping, not code class declarations; `TRACE_REVIEW_REQUIRED` |
| E11 new local classes and adapters | 30_11 | Exact module namespace, finalized class signatures, method algorithms, physical schemas, independent ADR; `NOT_IMPLEMENTED` |

## 3. No invented implementation evidence

- A class not found in checked source must be explicitly `PROPOSED`, not represented as an actual class.
- Source-confirmed fields and signatures are distinct from planned E11 class candidates.
- Rewriting this documentation cannot substitute for a code review, runtime environment test, coverage demonstration, legal approval or permission to begin Coding.

## 4. Exit criteria for a complete DD rewrite

1. Class inventory complete across selected scope; every new/modified class has the checklist and code/ADR mapping.
2. No unreviewed overlapping layer authorities; no spurious Product/CLI dependency introduced.
3. Versioned result/schema, error taxonomy and optional runtime capability accepted by independent reviewer.
4. Method-specific mathematics/CI and Known Truth validation plan linked, without claiming Science PASS.
5. Explicit Owner acceptance SHA for exact physical design; current `PHYSICAL_DESIGN_PARTIAL` changes only with evidence.
