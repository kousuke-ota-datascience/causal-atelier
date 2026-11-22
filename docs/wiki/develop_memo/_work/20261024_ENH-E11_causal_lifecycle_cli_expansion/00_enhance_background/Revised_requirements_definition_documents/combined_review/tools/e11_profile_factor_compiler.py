#!/usr/bin/env python3
"""Enhancement-only profile factor compiler and structural parity checker.

No implementation, backend import or science test. Run from a checkout in a Python 3.12
environment with jsonschema. Fails closed if any original draft cannot be regenerated
bit-for-bit as a JSON structural object or its schema is invalid.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
from jsonschema import Draft202012Validator

KINDS = ("method_config", "question_profile", "design_profile", "output_profile", "inference_profile")
ROOT = Path(__file__).resolve().parents[2] / "23_api_interface_design" / "schema_drafts" / "method_profiles"

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def factor(payloads):
    """Exact reversible factoring of *top-level* metadata/properties; all remaining
    JSON Schema semantics (if/then/else, dependentSchemas, definitions, etc.) are
    preserved verbatim in each overlay. Do not use allOf with conflicting
    additionalProperties=false: reconstruct the original schema before validation."""
    shared = {}
    keys = set.intersection(*(set(p) for p in payloads.values()))
    for key in sorted(keys):
        if key == "properties":
            pkeys = set.intersection(*(set(p["properties"]) for p in payloads.values()))
            common = {name: next(iter(payloads.values()))["properties"][name]
                      for name in sorted(pkeys)
                      if all(canonical(p["properties"][name]) ==
                             canonical(next(iter(payloads.values()))["properties"][name])
                             for p in payloads.values())}
            if common:
                shared["properties"] = common
        elif all(canonical(p[key]) == canonical(next(iter(payloads.values()))[key])
                 for p in payloads.values()):
            shared[key] = next(iter(payloads.values()))[key]
    overlays = {}
    for id_, original in payloads.items():
        overlay = copy.deepcopy(original)
        for k, v in shared.items():
            if k == "properties":
                for name in v:
                    overlay["properties"].pop(name)
                if not overlay["properties"]:
                    del overlay["properties"]
            else:
                del overlay[k]
        overlays[id_] = overlay
    return shared, overlays

def reassemble(shared, overlay):
    result = copy.deepcopy(shared)
    for k, v in overlay.items():
        if k == "properties":
            result.setdefault("properties", {}).update(copy.deepcopy(v))
        else:
            result[k] = copy.deepcopy(v)
    return result

def validate(inputs, outfile):
    failures = []
    full = {}
    for id_ in inputs["method_ids"]:
        for kind in KINDS:
            name = "e11_" + id_.lower().replace("-", "_") + "_" + kind + "_v1.schema.json"
            src = ROOT / name
            if not src.is_file():
                failures.append("MISSING:" + name)
                continue
            raw = json.loads(src.read_text(encoding="utf-8"))
            try:
                Draft202012Validator.check_schema(raw)
            except Exception as exc:
                failures.append("INVALID_META:" + name + ":" + repr(exc))
                continue
            full[(id_, kind)] = raw
    result = {"status": "BLOCKED", "originals_seen": len(full), "expected": 200,
              "kinds": {}, "failures": failures}
    if len(full) != 200:
        outfile.write_text(json.dumps(result, indent=2) + "\n")
        return result
    for kind in KINDS:
        group = {id_: full[(id_, kind)] for id_ in inputs["method_ids"]}
        shared, overlays = factor(group)
        checked = {}
        for id_, old in group.items():
            new = reassemble(shared, overlays[id_])
            try:
                Draft202012Validator.check_schema(new)
            except Exception as exc:
                failures.append("REBUILD_META:" + id_ + ":" + kind + ":" + str(exc))
            if canonical(new) != canonical(old):
                failures.append("NOT_IDENTICAL:" + id_ + ":" + kind)
            checked[id_] = hashlib.sha256(canonical(old).encode("utf-8")).hexdigest()
        result["kinds"][kind] = {
            "shared": shared, "overlays": overlays, "source_semantic_json_sha256": checked,
            "identity_proof": "EXACT_JSON_AST_REASSEMBLY_EQUALITY",
            "jsonschema_acceptance_equivalence":
                "Logically exact if reconstructed schema is identical to original",
        }
    result["failures"] = failures
    result["status"] = "STRUCTURAL_IDENTITY_VERIFIED" if not failures else "BLOCKED"
    outfile.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    return result

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True)
    args = p.parse_args()
    ids = (["P1-M%02d" % i for i in range(1, 21) if i != 6] +
           ["P2-M%02d" % i for i in range(1, 9)] +
           ["P3-M%02d" % i for i in range(1, 14)])
    report = validate({"method_ids": ids}, Path(args.out))
    print(report["status"], report["originals_seen"], "/200")
    raise SystemExit(0 if report["status"] == "STRUCTURAL_IDENTITY_VERIFIED" else 3)
