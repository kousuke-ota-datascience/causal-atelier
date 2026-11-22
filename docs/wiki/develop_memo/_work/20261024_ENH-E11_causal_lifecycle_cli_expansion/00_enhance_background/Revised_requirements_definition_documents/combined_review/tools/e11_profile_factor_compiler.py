#!/usr/bin/env python3
"""Independent review-only Draft 2020-12 parity verification for all 200 E11 Method Profiles.

Must run from a full checkout of the approved GitHub commit. Requires jsonschema>=4
only in the review environment; never imported by production Ariadne code.
The baseline 200 source drafts remain unchanged. Factored drafts are NOT automatically
registered into the runtime until Contract Freeze/Coding Authorization.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2] / "23_api_interface_design" / "schema_drafts" / "method_profiles"
KINDS = ("method_config", "question_profile", "design_profile", "output_profile", "inference_profile")
IDS = (
    [f"P1-M{i:02d}" for i in range(1, 21) if i != 6]
    + [f"P2-M{i:02d}" for i in range(1, 9)]
    + [f"P3-M{i:02d}" for i in range(1, 14)]
)

def normalized(x: Any) -> str:
    return json.dumps(x, sort_keys=True, ensure_ascii=False, separators=(",", ":"))

def git_blob_sha(path: Path) -> str:
    payload = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(payload)).encode() + b"\x00" + payload).hexdigest()

def materialize(shared: dict, overlay: dict) -> dict:
    result = copy.deepcopy(shared)
    for key, value in overlay.items():
        if key == "properties":
            result.setdefault("properties", {}).update(copy.deepcopy(value))
        else:
            result[key] = copy.deepcopy(value)
    return result

def exemplar(schema: dict) -> Any:
    if "const" in schema:
        return copy.deepcopy(schema["const"])
    if "enum" in schema:
        return copy.deepcopy(schema["enum"][0])
    if "oneOf" in schema:
        return exemplar(schema["oneOf"][0])
    kind = schema.get("type", "object" if "properties" in schema else "string")
    if isinstance(kind, list):
        kind = kind[0]
    if kind == "null":
        return None
    if kind == "boolean":
        return False
    if kind == "integer":
        return schema.get("minimum", 0)
    if kind == "number":
        low = schema.get("exclusiveMinimum", schema.get("minimum", 0))
        high = schema.get("exclusiveMaximum", schema.get("maximum"))
        if high is not None and high > low:
            return (high + low) / 2
        return low + 1 if "exclusiveMinimum" in schema else low
    if kind == "string":
        if schema.get("pattern") == "^[a-f0-9]{64}$":
            return "0" * 64
        return "x" * max(schema.get("minLength", 1), 1)
    if kind == "array":
        value = [exemplar(schema.get("items", {"type": "string"}))
                 for _ in range(schema.get("minItems", 0))]
        if schema.get("uniqueItems"):
            value = [(v + str(i) if isinstance(v, str) else v)
                     for i, v in enumerate(value)]
        return value
    if kind == "object":
        value = {k: exemplar(schema.get("properties", {}).get(k, {"type": "string"}))
                 for k in schema.get("required", [])}
        for clause in schema.get("allOf", []):
            if "if" not in clause:
                continue
            branch = "then" if Draft202012Validator(clause["if"]).is_valid(value) else "else"
            for k, definition in clause.get(branch, {}).get("properties", {}).items():
                if k in value:
                    value[k] = exemplar(definition)
        return value
    raise ValueError(f"unsupported example generator kind: {kind}")

def assert_equivalent_instance(original: dict, rebuilt: dict, instance: Any,
                               should_accept: bool, label: str, failures: list[str]) -> None:
    left = Draft202012Validator(original).is_valid(instance)
    right = Draft202012Validator(rebuilt).is_valid(instance)
    if left != right or left != should_accept:
        failures.append(f"{label}: expected={should_accept}, original={left}, factored={right}")

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--report", type=Path, required=True)
    args = p.parse_args()
    errors: list[str] = []
    counts = {"methods": len(IDS), "schema_count": 0, "positive": 0,
              "missing_required_negative": 0, "unknown_field_negative": 0,
              "const_negative": 0, "conditional_inference_negative": 0}
    observed_ids = set()
    for kind in KINDS:
        factored_path = ROOT / "factored" / f"e11_{kind}_factored_v1.json"
        factored = json.loads(factored_path.read_text(encoding="utf-8"))
        if set(factored["profiles"]) != set(IDS):
            errors.append(f"{kind}: missing or excess method")
            continue
        for method in IDS:
            item = factored["profiles"][method]
            expected_name = f"e11_{method.lower().replace('-', '_')}_{kind}_v1.schema.json"
            if item["source_file"] != expected_name:
                errors.append(f"{kind}/{method}: wrong source file name")
                continue
            src = ROOT / expected_name
            if not src.is_file() or git_blob_sha(src) != item["source_blob_sha"]:
                errors.append(f"{kind}/{method}: source Git blob SHA mismatch")
                continue
            original = json.loads(src.read_text(encoding="utf-8"))
            rebuilt = materialize(factored["shared_schema"], item["overlay"])
            if normalized(original) != normalized(rebuilt):
                errors.append(f"{kind}/{method}: JSON AST is not identical")
                continue
            try:
                Draft202012Validator.check_schema(original)
                Draft202012Validator.check_schema(rebuilt)
            except Exception as exc:
                errors.append(f"{kind}/{method}: invalid meta-schema: {type(exc).__name__}: {exc}")
                continue
            observed_ids.add((method, kind))
            counts["schema_count"] += 1
            example = exemplar(original)
            label = f"{kind}/{method}"
            assert_equivalent_instance(original, rebuilt, example, True, label + "/positive", errors)
            counts["positive"] += 1
            if original.get("required"):
                miss = copy.deepcopy(example)
                del miss[original["required"][0]]
                assert_equivalent_instance(original, rebuilt, miss, False, label + "/missing-required", errors)
                counts["missing_required_negative"] += 1
            unknown = {**example, "__unrecognized_property__": True}
            assert_equivalent_instance(original, rebuilt, unknown, False, label + "/unknown-property", errors)
            counts["unknown_field_negative"] += 1
            for prop, sch in original.get("properties", {}).items():
                if prop in example and "const" in sch:
                    bad = copy.deepcopy(example)
                    if isinstance(bad[prop], bool):
                        bad[prop] = not bad[prop]
                    elif isinstance(bad[prop], str):
                        bad[prop] = "__WRONG_CONST__"
                    else:
                        bad[prop] = "__wrong_type__"
                    assert_equivalent_instance(original, rebuilt, bad, False, label + "/const", errors)
                    counts["const_negative"] += 1
                    break
            if kind == "inference_profile" and original.get("allOf"):
                bad = {**example, "requested": False, "confidence_level": 0.95}
                assert_equivalent_instance(original, rebuilt, bad, False, label + "/conditional-inference", errors)
                counts["conditional_inference_negative"] += 1

    status = "PASS_SCHEMA_STRUCTURAL_AND_VALIDATOR_PARITY" if not errors and len(observed_ids) == 200 else "BLOCKED"
    report = {"status": status, "counts": counts, "failures": errors,
              "scope": "Draft 2020-12 schema AST, metaschema and generated fixture acceptance",
              "science_backend_privacy_cross_artifact_evidence": "NOT_EVALUATED",
              "code_authorization": "NOT_GRANTED"}
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(status, counts, "errors", len(errors))
    return 0 if status.startswith("PASS") else 3

if __name__ == "__main__":
    raise SystemExit(main())
