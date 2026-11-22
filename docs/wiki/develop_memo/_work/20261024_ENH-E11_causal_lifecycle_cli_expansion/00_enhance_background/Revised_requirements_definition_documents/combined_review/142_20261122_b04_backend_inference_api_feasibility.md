# B04 — Effective Backend/API/Inference feasibility assessment (2026-11-22)

**Status: PUBLIC_OFFICIAL_DOCUMENTATION_REVIEWED / TARGET_RUNTIME_NOT_PROBED / B04_BLOCKED_FOR_CONTRACT_FREEZE.**

## Baseline source
- Repo `pyproject.toml` requires Python >=3.12,<3.13; locked `causal-learn==0.1.4.8` and `statsmodels==0.14.6`, plus numpy=2.2.6, scipy=1.13.1, pyarrow=24.0.0. `dowhy`, `econml`, `tigramite` are **absent from both pyproject optional deps and uv.lock**. Under S02, four future isolated profiles ENV-BASE/DOWHY/ECONML/TIGRAMITE remain required, not ENV-COMBINED.
- The assistant runtime is Python 3.13.5, **not** project supported Python 3.12, and lacks dowhy/econml/tigramite/causallearn. Do not call this an actual target-env API probe. No source/test/dependency edits authorized.

## Primary upstream public API and limitations
| Backend | Official upstream documentation examined | Feasibility | Remaining hard stop |
| --- | --- | --- | --- |
| DoWhy | https://www.pywhy.org/dowhy/v0.14/dowhy.html | CausalModel / identify_effect; identification APIs exist | No lock/version/API run; nonparametric ATE display is not proof of B0 LATE. The separate conditional IV identification is Method-specific. |
| EconML | https://www.pywhy.org/EconML/reference.html ; https://www.pywhy.org/EconML/spec/inference.html ; https://www.pywhy.org/EconML/_autosummary/econml.iv.dr.DRIV.html | LinearDML/CausalForestDML, DR/ForestDR, SLearner/TLearner/XLearner, DRIV have documented classes | Must bind explicit class paths and inference per Method; fit() and effect_interval() being exposed does not imply valid inferential CI for the configured nuisance/final model. |
| Tigramite | https://jakobrunge.github.io/tigramite/ ; https://jakobrunge.github.io/tigramite/_modules/tigramite/lpcmci.html | PCMCI.run_pcmci/run_pcmciplus and LPCMCI.run_lpcmci are documented | Live API/version absent; graph orientation/lag semantics and CI test assumptions must be validated. |
| causal-learn | https://causal-learn.readthedocs.io/en/latest/search_methods_index/Constraint-based%20causal%20discovery%20methods/FCI.html | FCI public import documented, locked 0.1.4.8 | Backend version specific signature/return marks and CI tests have not been probed. |

## Method inference rules (normative draft)
- P2-M01..04 and P2-M08: `inference.requested=true` may be accepted only for an *actually fitted* library/API/configuration where effect interval matches the selected method/estimand and the independent scientific inference acceptance is specified. Otherwise typed `UNSUPPORTED`/no CI; never silently point-only yet claim confirmatory success.
- P2-M05..07: separate meta-learner API probing; inherited methods or advertised `effect_interval` are **not sufficient evidence** of calibrated CI; point-only is allowed only when the approved Method capability explicitly permits it.
- P1-M05 DoWhy IV: `identify_effect` is not a numerical estimator; B0 LATE conditional proof needs explicit Z/A/assumption validators and source refs.
- P3-M01..03: graph discovery return matrix and endpoint invariants from actual version required; do not auto-orient ambiguous PAG/CPDAG.
- P3-M12 SCM remains point-only; P3-M10/P3-M11 AR confidence sets cannot be converted to a single finite interval based solely on generic library API.
- Local native quasi/IV/SCM methods require **Ariadne algorithms**, not simply statsmodels version availability; no evidence of actual method implementation is implied.

## Probe contract
`combined_review/tools/e11_backend_probe.py` is a **review-only runnable probe** to execute under each pinned Python3.12 environment after the optional dependency profiles have been resolved. It reports installed distribution/version, import path, constructor signature, method signatures and explicit BLOCKED; a successful probe is still **API_PROBED_NOT_SCIENCE_VALIDATED**. This script has not been executed in the target environments. Exact optional package pins, compatibility testing and actual B04 resolution remain REQUIRED before Freeze. Do not update pyproject/uv.lock or run Coding Agent during this review.
