#!/usr/bin/env python3
"""Local *non-production* capability probe. Run separately in each frozen E11 ENV, never as a product import.

Does not prove causal correctness or valid inference. Nonzero exit for missing dependency/API.
"""
import argparse
import importlib
import importlib.metadata as md
import inspect
import json
import platform
import sys
from pathlib import Path

CONTRACT = {
    "ENV-BASE": [
        ("causal-learn", "causallearn.search.ConstraintBased.FCI", "fci"),
        ("statsmodels", "statsmodels.api", "OLS"),
    ],
    "ENV-DOWHY": [("dowhy", "dowhy", "CausalModel")],
    "ENV-ECONML": [
        ("econml", "econml.dml", "LinearDML"),
        ("econml", "econml.dml", "CausalForestDML"),
        ("econml", "econml.dr", "DRLearner"),
        ("econml", "econml.dr", "ForestDRLearner"),
        ("econml", "econml.metalearners", "SLearner"),
        ("econml", "econml.metalearners", "TLearner"),
        ("econml", "econml.metalearners", "XLearner"),
        ("econml", "econml.iv.dr", "DRIV"),
    ],
    "ENV-TIGRAMITE": [
        ("tigramite", "tigramite.pcmci", "PCMCI"),
        ("tigramite", "tigramite.lpcmci", "LPCMCI"),
    ],
}
METHODS = {
    ("tigramite.pcmci", "PCMCI"): ("run_pcmci", "run_pcmciplus"),
    ("tigramite.lpcmci", "LPCMCI"): ("run_lpcmci",),
    ("dowhy", "CausalModel"): ("identify_effect",),
}
for module, name in [("econml.dml", "LinearDML"), ("econml.dml", "CausalForestDML"),
    ("econml.dr", "DRLearner"), ("econml.dr", "ForestDRLearner"),
    ("econml.metalearners", "SLearner"), ("econml.metalearners", "TLearner"),
    ("econml.metalearners", "XLearner"), ("econml.iv.dr", "DRIV")]:
    METHODS[(module, name)] = ("fit", "effect")

def inspect_env(profile):
    result = {
        "profile": profile, "python": platform.python_version(), "executable": sys.executable,
        "python_target_ok": sys.version_info[:2] == (3, 12), "checks": [],
    }
    for distribution, module_name, symbol_name in CONTRACT[profile]:
        row = {"package": distribution, "module": module_name, "symbol": symbol_name}
        try:
            row["version"] = md.version(distribution)
            obj = getattr(importlib.import_module(module_name), symbol_name)
            row["signature"] = str(inspect.signature(obj))
            row["method_signatures"] = {}
            for method in METHODS.get((module_name, symbol_name), ()):
                fun = getattr(obj, method)
                row["method_signatures"][method] = str(inspect.signature(fun))
            row["status"] = "API_PRESENT_UNVALIDATED"
        except Exception as exc:
            row["status"] = "BLOCKED"
            row["error"] = type(exc).__name__ + ": " + str(exc)
        result["checks"].append(row)
    result["status"] = "API_PROBED_NOT_SCIENCE_VALIDATED" if result["python_target_ok"] and all(x["status"] == "API_PRESENT_UNVALIDATED" for x in result["checks"]) else "BLOCKED"
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", required=True, choices=tuple(CONTRACT))
    parser.add_argument("--output", required=True, help="Path under safe review-only area; never include secrets.")
    args = parser.parse_args()
    out = inspect_env(args.profile)
    Path(args.output).write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    print(out["status"])
    sys.exit(0 if out["status"] == "API_PROBED_NOT_SCIENCE_VALIDATED" else 3)
