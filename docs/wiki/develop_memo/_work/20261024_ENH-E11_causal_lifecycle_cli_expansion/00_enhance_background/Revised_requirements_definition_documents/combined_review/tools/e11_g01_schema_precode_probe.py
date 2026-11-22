#!/usr/bin/env python3
"""Read-only 6-public/3-active-FCI Draft202012 G01 diagnostic; historical profile is non-dispatch."""
from __future__ import annotations
import argparse
from copy import deepcopy
import importlib.metadata
from hashlib import sha256
import re
import json
from pathlib import Path
import subprocess
import sys

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "23_api_interface_design" / "schema_drafts"
PUBLIC = (
    "e11_local_study_v1.schema.json",
    "e11_local_graph_v1.schema.json",
    "e11_local_status_v1.schema.json",
    "e11_local_effect_result_v1.schema.json",
    "e11_local_manifest_v1.schema.json",
    "e11_local_commit_marker_v1.schema.json",
)
FCI_ACTIVE = (
    "e11_p1_m06_fci_method_config_v1.schema.json",
    "e11_p1_m06_fci_question_profile_v1.schema.json",
    "e11_p1_m06_fci_design_profile_v1.schema.json",
)
FCI_HISTORICAL_NONDISPATCH = "e11_g01_fci_method_config_v1.schema.json"

def git(root: Path, *args: str) -> str:
    p = subprocess.run(["git", *args], cwd=root, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return p.stdout.strip()

def load_schema(path: Path) -> dict:
    # JSON Schema is source-of-truth; reject duplicate keys instead of last-wins.
    def reject_duplicate_keys(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj:
                raise ValueError(f"Duplicate JSON Schema key {key!r} in {path}")
            obj[key] = value
        return obj
    data = json.loads(path.read_text(encoding="utf-8"),
                      object_pairs_hook=reject_duplicate_keys)
    if not isinstance(data, dict):
        raise ValueError(f"Not a JSON Schema object: {path}")
    Draft202012Validator.check_schema(data)
    if data.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise ValueError(f"Wrong $schema: {path}")
    return data

def config() -> dict:
    return {"indep_test": "fisherz", "alpha": 0.05, "depth": -1,
            "max_path_length": -1, "background_knowledge": None}

def question() -> dict:
    return {"question_id": "q01", "research_question": "What is the graph?",
            "population": "observations", "analysis_goal": "GRAPH_STRUCTURE"}

def design() -> dict:
    return {"design_id": "d01", "question_id": "q01",
            "design_kind": "OBSERVATIONAL_GRAPH_DISCOVERY",
            "variables": [{"name": "X", "measurement_scale": "CONTINUOUS"},
                          {"name": "Y", "measurement_scale": "CONTINUOUS"}],
            "assumptions": {"causal_markov_declared": True,
                            "faithfulness_declared": True,
                            "acyclicity_declared": True,
                            "latent_confounding_possible": True,
                            "sampling_unit": "person"},
            "background_knowledge": None}

def cases(name: str) -> list[tuple[str, bool, dict]]:
    if name == FCI_ACTIVE[0]:
        ok = config()
        bk = deepcopy(ok)
        bk["background_knowledge"] = {"required_edges": [["X", "Y"]],
                                      "forbidden_edges": []}
        r = [("valid_config", True, ok), ("valid_explicit_bk", True, bk)]
        for key, value in (("alpha", 0), ("alpha", 1), ("depth", -2),
                           ("max_path_length", -2), ("indep_test", "invalid")):
            bad = deepcopy(ok)
            bad[key] = value
            r.append((f"reject_{key}_{value}", False, bad))
        for key in ("alpha", "background_knowledge"):
            bad = deepcopy(ok)
            del bad[key]
            r.append((f"reject_missing_{key}", False, bad))
        bad = deepcopy(ok)
        bad["unknown_backend_default"] = 1
        r.append(("reject_additional_field", False, bad))
        bad = deepcopy(bk)
        bad["background_knowledge"]["required_edges"] = [["X"]]
        r.append(("reject_invalid_pair", False, bad))
        bad = deepcopy(bk)
        bad["background_knowledge"]["unknown"] = 1
        r.append(("reject_additional_bk", False, bad))
        bad = deepcopy(bk)
        bad["background_knowledge"]["required_edges"] = [["X", "Y"], ["X", "Y"]]
        r.append(("reject_duplicate_bk", False, bad))
        return r
    if name == FCI_ACTIVE[1]:
        ok = question()
        r = [("valid_question", True, ok)]
        for key, value in (("question_id", ""), ("analysis_goal", "ATE")):
            bad = deepcopy(ok)
            bad[key] = value
            r.append((f"reject_{key}", False, bad))
        bad = deepcopy(ok)
        bad["unknown"] = "extra"
        r.append(("reject_extra", False, bad))
        bad = deepcopy(ok)
        del bad["population"]
        r.append(("reject_missing_population", False, bad))
        return r
    if name == FCI_ACTIVE[2]:
        ok = design()
        bk = deepcopy(ok)
        bk["background_knowledge"] = {"required_edges": [],
                                      "forbidden_edges": [["X", "Y"]]}
        r = [("valid_design", True, ok), ("valid_design_bk", True, bk)]
        bad = deepcopy(ok)
        bad["variables"] = bad["variables"][:1]
        r.append(("reject_one_variable", False, bad))
        bad = deepcopy(ok)
        bad["assumptions"]["faithfulness_declared"] = "yes"
        r.append(("reject_nonboolean_assumption", False, bad))
        bad = deepcopy(ok)
        bad["variables"][0]["measurement_scale"] = "UNKNOWN"
        r.append(("reject_scale", False, bad))
        bad = deepcopy(ok)
        bad["variables"][0]["extra"] = "x"
        r.append(("reject_extra_variable_field", False, bad))
        bad = deepcopy(ok)
        bad["design_kind"] = "RANDOMIZED_TRIAL"
        r.append(("reject_design_kind", False, bad))
        bad = deepcopy(ok)
        bad["background_knowledge"] = {"required_edges": [["X"]],
                                       "forbidden_edges": []}
        r.append(("reject_wrong_bk_pair", False, bad))
        return r
    raise ValueError(f"No fixture set: {name}")

def cross(schemas: dict[str, dict]) -> dict[str, bool]:
    study, graph, status, manifest = (schemas[x] for x in
                                     (PUBLIC[0], PUBLIC[1], PUBLIC[2], PUBLIC[4]))
    privacy = study["properties"]["privacy"]
    return {
        "discover_is_study_operation": (
            "DISCOVER" in study["properties"]["operation"]["enum"]),
        "method_config_is_required": (
            "config" in study["properties"]["method"]["required"]),
        "privacy_row_optin_required_boolean": (
            "row_export_requested" in privacy["required"]
            and privacy["properties"]["row_export_requested"].get("type") == "boolean"),
        "local_graph_product_ids_const_null": (
            graph["properties"]["version_id"].get("const", "__MISSING__") is None
            and graph["properties"]["parent_version_id"].get("const", "__MISSING__") is None),
        "technical_status_enums_equal": (
            manifest["properties"]["execution"]["properties"]["technical_status"]["enum"]
            == status["properties"]["technical_status"]["enum"]),
        "manifest_graph_dispatch_declared": (
            "graph" in manifest["properties"]["schema_dispatch"]["properties"]),
    }

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report", type=Path, required=True)
    ap.add_argument("--expected-head", required=True, help="Exact 40-hex checkout SHA")
    args = ap.parse_args()
    repo = ROOT
    while repo != repo.parent and not (repo / ".git").exists():
        repo = repo.parent
    if not (repo / ".git").exists():
        raise RuntimeError("Not a real Git checkout")
    if not re.fullmatch(r"[0-9a-f]{40}", args.expected_head):
        raise ValueError("--expected-head must be the independently pinned 40-hex SHA")
    head = git(repo, "rev-parse", "HEAD")
    dirty = bool(git(repo, "status", "--porcelain=v1"))
    lock_path = repo / "uv.lock"
    if not lock_path.is_file():
        raise RuntimeError("Target uv.lock missing at pinned checkout")
    lock_sha256 = sha256(lock_path.read_bytes()).hexdigest()
    lock_blob_sha = git(repo, "hash-object", str(lock_path))
    script_blob_sha = git(repo, "hash-object", str(Path(__file__).resolve()))
    target_python = sys.version_info[:2] == (3, 12)
    # Exactly 6 public + 3 active P1-M06 schemas are normative for G01.
    schemas = {name: load_schema(SCHEMAS / name) for name in PUBLIC + FCI_ACTIVE}
    blobs = {name: git(repo, "hash-object", str(SCHEMAS / name))
             for name in schemas}
    # Legacy e11_g01_* is historical documentation, never a Method dispatch target.
    # Validate it best-effort for drift visibility; do NOT gate active G01 readiness on it.
    historic = {"path": FCI_HISTORICAL_NONDISPATCH,
                "authority": "HISTORICAL_NONDISPATCH",
                "diagnostic_only": True}
    historic_path = SCHEMAS / FCI_HISTORICAL_NONDISPATCH
    if historic_path.exists():
        historic["git_blob_sha"] = git(repo, "hash-object", str(historic_path))
        try:
            old_schema = load_schema(historic_path)
            active_schema = deepcopy(schemas[FCI_ACTIVE[0]])
            for value in (old_schema, active_schema):
                value.pop("$id", None)
                value.pop("title", None)
            historic["valid_metaschema"] = True
            historic["same_constraints_as_active"] = old_schema == active_schema
        except Exception as exc:
            historic["valid_metaschema"] = False
            historic["diagnostic_error"] = type(exc).__name__ + ": " + str(exc)
    else:
        historic["valid_metaschema"] = False
        historic["diagnostic_error"] = "HISTORICAL_FILE_ABSENT"
    fixtures = []
    for name in FCI_ACTIVE:
        v = Draft202012Validator(schemas[name])
        for label, expected, instance in cases(name):
            actual = v.is_valid(instance)
            fixtures.append({"schema": name, "case": label,
                             "expected_valid": expected, "actual_valid": actual,
                             "matched": expected == actual})
    relations = cross(schemas)
    passed = (target_python and head == args.expected_head and not dirty
              and len(schemas) == 9
              and all(x["matched"] for x in fixtures)
              and all(relations.values()))
    report = {
        "verdict": ("PASS_AUTHOR_STRUCTURAL_PRECODE_DIAGNOSTIC"
                    if passed else "BLOCKED_OR_FAILED_AUTHOR_DIAGNOSTIC"),
        "warning": ("This is author-provided structural evidence only, NOT independent S09,"
                    " G01 S10/S11, FCI Science/Backend, Reader/OS or Gate999 PASS."),
        "python": sys.version.split()[0],
        "jsonschema": importlib.metadata.version("jsonschema"),
        "approved_python_312": target_python,
        "git_head": head, "expected_head": args.expected_head,
        "git_head_matches": head == args.expected_head,
        "git_worktree_dirty": dirty,
        "uv_lock_sha256": lock_sha256,
        "uv_lock_git_blob_sha": lock_blob_sha,
        "probe_source_blob_sha": script_blob_sha,
        "source_blob_sha": blobs,
        "active_fci_profile_count": len(FCI_ACTIVE),
        "historic_g01_schema_diagnostic_nonblocking": historic,
        "metaschema_valid_count": len(schemas),
        "fci_fixture_count": len(fixtures),
        "fci_fixture_mismatches": [x for x in fixtures if not x["matched"]],
        "cross_checks": relations,
        "semantic_obligations_unverified": [
            "G01 Study / Question / Design / Dataset / method / BK equality",
            "BK required-forbidden overlap, cycles, node existence and variable uniqueness",
            "Effective Python3.12 causal-learn FCI fitted API and CI assumptions",
            "Independent MAG/PAG scientific Oracle and T2/T3",
            "Actual atomic E11 Publisher/Reader, private FS and byte/hash readback",
            "Full positive/negative public E11 Study/Graph/Status/Manifest/Marker instances",
        ],
    }
    out = args.report.resolve()
    if out == repo.resolve() or repo.resolve() in out.parents:
        raise ValueError("Review report path must be outside the repository")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": report["verdict"], "report": str(out),
                      "schema_count": len(schemas), "fixture_count": len(fixtures),
                      "mismatches": len(report["fci_fixture_mismatches"])}))
    return 0 if passed else 2

if __name__ == "__main__":
    raise SystemExit(main())
