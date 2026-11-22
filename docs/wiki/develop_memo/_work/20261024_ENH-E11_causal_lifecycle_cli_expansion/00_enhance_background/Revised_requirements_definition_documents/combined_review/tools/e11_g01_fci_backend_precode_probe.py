#!/usr/bin/env python3
"""Read-only ENV-BASE FCI tagged-version tiny-fit/API probe; NOT scientific acceptance."""
from __future__ import annotations
import argparse
from contextlib import redirect_stdout, redirect_stderr
from hashlib import sha256
import importlib.metadata
import inspect
import io
import json
from pathlib import Path
import subprocess
import sys
import traceback

ROOT = Path(__file__).resolve().parents[2]

def git(root: Path, *args: str) -> str:
    p = subprocess.run(["git", *args], cwd=root, check=True,
                       capture_output=True, text=True)
    return p.stdout.strip()

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--expected-head", required=True, help="Pinned 40-character Git commit")
    ap.add_argument("--report", required=True, type=Path)
    args = ap.parse_args()

    repo = ROOT
    while repo != repo.parent and not (repo / ".git").exists():
        repo = repo.parent
    if not (repo / ".git").exists():
        raise RuntimeError("Expected a real pinned Git checkout")

    out = args.report.resolve()
    if out == repo.resolve() or repo.resolve() in out.parents:
        raise ValueError("Review report must be outside repository")

    head = git(repo, "rev-parse", "HEAD")
    dirty = bool(git(repo, "status", "--porcelain=v1"))
    py312 = sys.version_info[:2] == (3, 12)
    report = {
        "warning": "Author pre-code API/fit smoke only. NOT independently reviewed Graph oracle, T2/T3, G01 S09/S10/S11 or Gate999 PASS.",
        "python": sys.version.split()[0],
        "python312": py312,
        "git_head": head,
        "expected_head": args.expected_head,
        "sha_match": head == args.expected_head,
        "dirty": dirty,
        "target_distribution": "causal-learn==0.1.4.8",
        "source_tag_fci_blob_sha": "869b8de01ed495ce4738d3452e0217604dc31e9b",
        "bk_nonnull_runtime": "BLOCK_PRE_FCI_KNOWN_TAGGED_SOURCE_SCIENCE_AND_STDOUT_HAZARD",
        "bk_support_science_accepted": False,
        "fit_science_accepted": False,
    }
    fit_ok = False
    neg_ok = False
    try:
        import numpy as np
        from causallearn.search.ConstraintBased.FCI import fci

        dist = importlib.metadata.version("causal-learn")
        sig = inspect.signature(fci)
        params = list(sig.parameters)
        required = {
            "dataset", "independence_test_method", "alpha", "depth",
            "max_path_length", "verbose", "background_knowledge",
            "show_progress", "node_names",
        }
        signature_ok = required.issubset(params)
        rng = np.random.default_rng(271828)
        n = 512
        x = rng.normal(size=n)
        y = .75 * x + rng.normal(size=n)
        z = .55 * y + rng.normal(size=n)
        data = np.column_stack((x, y, z)).astype("float64")
        cols = ["X", "Y", "Z"]
        report.update({
            "distribution_version": dist,
            "numpy_version": np.__version__,
            "actual_signature": str(sig),
            "declared_columns": cols,
            "input_sha256": sha256(data.tobytes()).hexdigest(),
            "n": n,
            "signature_required_names_available": signature_ok,
        })
        if signature_ok and dist == "0.1.4.8":
            stdout, stderr = io.StringIO(), io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                graph, edges = fci(
                    data, independence_test_method="fisherz",
                    alpha=.05, depth=-1, max_path_length=-1,
                    verbose=False, background_knowledge=None,
                    show_progress=False, node_names=cols,
                )
            backend_names = [node.get_name() for node in graph.get_nodes()]
            edge_rows = [
                {
                    "node1": edge.get_node1().get_name(),
                    "endpoint1": str(edge.get_endpoint1()),
                    "node2": edge.get_node2().get_name(),
                    "endpoint2": str(edge.get_endpoint2()),
                }
                for edge in edges
            ]
            no_unknown = all(x["node1"] in cols and x["node2"] in cols
                             and x["node1"] != x["node2"] for x in edge_rows)
            fit_ok = (
                len(backend_names) == len(cols)
                and set(backend_names) == set(cols)
                and len(set(backend_names)) == len(cols)
                and no_unknown
                and stdout.getvalue() == ""
                and stderr.getvalue() == ""
            )
            report.update({
                "actual_backend_node_names": backend_names,
                "backend_edges": edge_rows,
                "backend_graph_name_and_edge_identity_valid": no_unknown,
                "unexpected_stdout": stdout.getvalue()[:5000],
                "unexpected_stderr": stderr.getvalue()[:5000],
                "fit_api_structural_ok": fit_ok,
            })
            neg_out, neg_err = io.StringIO(), io.StringIO()
            neg_exc = None
            with redirect_stdout(neg_out), redirect_stderr(neg_err):
                try:
                    fci(
                        data, independence_test_method="unsupported-not-a-test",
                        alpha=.05, depth=-1, max_path_length=-1,
                        verbose=False, background_knowledge=None,
                        show_progress=False, node_names=cols,
                    )
                except (ValueError, TypeError, KeyError) as e:
                    neg_exc = type(e).__name__
            neg_ok = bool(neg_exc) and neg_out.getvalue() == "" and neg_err.getvalue() == ""
            report.update({
                "invalid_ci_method_rejected": bool(neg_exc),
                "invalid_ci_exception_type": neg_exc,
                "negative_stdout": neg_out.getvalue()[:5000],
                "negative_stderr": neg_err.getvalue()[:5000],
            })
        else:
            report["blocked_reason"] = "VERSION_OR_SIGNATURE_MISMATCH"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback_tail"] = traceback.format_exc()[-3000:]

    passed = (py312 and head == args.expected_head and not dirty
              and report.get("distribution_version") == "0.1.4.8"
              and report.get("signature_required_names_available") is True
              and fit_ok and neg_ok)
    report["verdict"] = (
        "PASS_AUTHOR_FCI_TINY_FIT_DIAGNOSTIC" if passed
        else "BLOCKED_OR_FAILED_AUTHOR_FCI_DIAGNOSTIC"
    )
    report["unverified"] = [
        "Actual Ariadne E11 Adapter integration and strict typed input preflight",
        "Independently derived MAG/PAG graph truth/reference and forbidden BK motif",
        "Runtime scientific FCI soundness, stochastic T2/T3, error control and coverage",
        "Cross-process CLI stdout/log containment and atomic Publisher/Reader",
        "Any non-null BackgroundKnowledge execution (intentionally NOT called)",
    ]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": report["verdict"], "report": str(out),
                      "fit_api_structural_ok": fit_ok,
                      "invalid_ci_rejected": neg_ok}))
    return 0 if passed else 2

if __name__ == "__main__":
    raise SystemExit(main())
