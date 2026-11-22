#!/usr/bin/env python3
"""Read-only ENV-BASE FCI tagged-version tiny-fit/API probe; NOT scientific acceptance."""
from __future__ import annotations
import argparse
from contextlib import redirect_stdout, redirect_stderr
from hashlib import sha256
import re
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
    py312 = sys.version_info[:2] == (3, 12)
    report = {
        "warning": "Author pre-code API/fit smoke only. NOT independently reviewed Graph oracle, T2/T3, G01 S09/S10/S11 or Gate999 PASS.",
        "python": sys.version.split()[0],
        "python312": py312,
        "git_head": head,
        "expected_head": args.expected_head,
        "sha_match": head == args.expected_head,
        "dirty": dirty,
        "uv_lock_sha256": lock_sha256,
        "uv_lock_git_blob_sha": lock_blob_sha,
        "probe_source_blob_sha": script_blob_sha,
        "target_distribution": "causal-learn==0.1.4.8",
        "source_tag_fci_blob_sha": "869b8de01ed495ce4738d3452e0217604dc31e9b",
        "bk_nonnull_runtime": "BLOCK_PRE_FCI_KNOWN_TAGGED_SOURCE_SCIENCE_AND_STDOUT_HAZARD",
        "bk_support_science_accepted": False,
        "fit_science_accepted": False,
        "execution_scope": "AUTHOR_ONLY_FCI_API_SHAPE_SMOKE_NO_MAG_PAG_SCIENCE",
    }
    # Never import or fit a backend on a different/unapproved review target.
    # Keep a separate structured refusal artifact outside the checkout.
    if not (py312 and head == args.expected_head and not dirty):
        report["verdict"] = "BLOCKED_PRECONDITION_NO_BACKEND_EXECUTION"
        report["blocked_reasons"] = [
            name for name, failure in (
                ("PYTHON_NOT_3_12", not py312),
                ("HEAD_MISMATCH", head != args.expected_head),
                ("DIRTY_WORKTREE", dirty),
            ) if failure
        ]
        report["backend_invoked"] = False
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\\n", encoding="utf-8")
        print(json.dumps({"verdict": report["verdict"], "report": str(out)}))
        return 2

    def probe_fci_mode(fci_func, data, cols, ci_method):
        """Return independent structural evidence for one CI, even if it fails."""
        captured_stdout, captured_stderr = io.StringIO(), io.StringIO()
        result = {
            "independence_test_method": ci_method,
            "data_sha256": sha256(data.tobytes()).hexdigest(),
            "n": int(data.shape[0]),
            "n_variables": int(data.shape[1]),
            "fit_api_structural_ok": False,
        }
        try:
            with redirect_stdout(captured_stdout), redirect_stderr(captured_stderr):
                graph, edges = fci_func(
                    data, independence_test_method=ci_method, alpha=.05,
                    depth=-1, max_path_length=-1, verbose=False,
                    background_knowledge=None, show_progress=False,
                    node_names=cols,
                )
            names = [node.get_name() for node in graph.get_nodes()]
            edge_rows = [
                {"node1": edge.get_node1().get_name(),
                 "endpoint1": str(edge.get_endpoint1()),
                 "node2": edge.get_node2().get_name(),
                 "endpoint2": str(edge.get_endpoint2())}
                for edge in edges
            ]
            pairs = [tuple(sorted((e["node1"], e["node2"]))) for e in edge_rows]
            no_unknown = all(
                e["node1"] in cols and e["node2"] in cols
                and e["node1"] != e["node2"] for e in edge_rows
            )
            nodes_in_original_order = names == cols
            no_duplicate_pairs = len(pairs) == len(set(pairs))
            result.update({
                "backend_node_names": names,
                "backend_edges": edge_rows,
                "node_order_matches_dataset": nodes_in_original_order,
                "edge_nodes_match_dataset": no_unknown,
                "duplicate_edge_pairs_absent": no_duplicate_pairs,
                "fit_api_structural_ok": (
                    nodes_in_original_order and no_unknown and no_duplicate_pairs
                    and captured_stdout.getvalue() == ""
                    and captured_stderr.getvalue() == ""
                ),
            })
        except Exception as exc:
            result["error"] = type(exc).__name__ + ": " + str(exc)
            result["traceback_tail"] = traceback.format_exc()[-3000:]
        finally:
            result["unexpected_stdout"] = captured_stdout.getvalue()[:5000]
            result["unexpected_stderr"] = captured_stderr.getvalue()[:5000]
        return result

    fit_ok = False
    categorical_fit_ok = False
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
            fisherz = probe_fci_mode(fci, data, cols, "fisherz")
            report["actual_backend_node_names"] = fisherz.get("backend_node_names")
            report["backend_edges"] = fisherz.get("backend_edges")
            report["backend_graph_name_and_edge_identity_valid"] = (
                fisherz.get("node_order_matches_dataset", False)
                and fisherz.get("edge_nodes_match_dataset", False)
                and fisherz.get("duplicate_edge_pairs_absent", False)
            )
            report["unexpected_stdout"] = fisherz["unexpected_stdout"]
            report["unexpected_stderr"] = fisherz["unexpected_stderr"]
            report["fisherz_fit"] = fisherz
            fit_ok = fisherz["fit_api_structural_ok"]
            report["fit_api_structural_ok"] = fit_ok

            # Two categorical methods must be independently evaluated.
            # Already declared integer categories only: this is NOT
            # Ariadne's input eligibility or MAG/PAG science verification.
            rng_cat = np.random.default_rng(271829)
            n_cat = 2048
            cat_x = rng_cat.binomial(1, 0.5, size=n_cat)
            cat_y = np.bitwise_xor(cat_x, rng_cat.binomial(1, 0.20, size=n_cat))
            cat_z = np.bitwise_xor(cat_y, rng_cat.binomial(1, 0.20, size=n_cat))
            categorical_data = np.column_stack(
                (cat_x, cat_y, cat_z)).astype(np.int64)
            categorical_reports = []
            for ci_method in ("chisq", "gsq"):
                outcome = probe_fci_mode(fci, categorical_data, cols, ci_method)
                outcome["integer_coded_categories"] = True
                categorical_reports.append(outcome)
            report["categorical_ci_fits"] = categorical_reports
            categorical_fit_ok = (
                len(categorical_reports) == 2
                and all(x["fit_api_structural_ok"] for x in categorical_reports)
            )
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
              and fit_ok and categorical_fit_ok and neg_ok)
    report["verdict"] = (
        "PASS_AUTHOR_FCI_TINY_FIT_DIAGNOSTIC" if passed
        else "BLOCKED_OR_FAILED_AUTHOR_FCI_DIAGNOSTIC"
    )
    report["unverified"] = [
        "Actual Ariadne E11 Adapter integration and strict typed input preflight",
        "Categorical CI scientific validity, support thresholds, and all typed data negatives",
        "In-process redirect_stdout/stderr cannot establish subprocess/OS-level console containment",
        "Independently derived MAG/PAG graph truth/reference and forbidden BK motif",
        "Runtime scientific FCI soundness, stochastic T2/T3, error control and coverage",
        "Cross-process CLI stdout/log containment and atomic Publisher/Reader",
        "Any non-null BackgroundKnowledge execution (intentionally NOT called)",
    ]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": report["verdict"], "report": str(out),
                      "fit_api_structural_ok": fit_ok,
                      "categorical_fit_api_structural_ok": categorical_fit_ok,
                      "invalid_ci_rejected": neg_ok}))
    return 0 if passed else 2

if __name__ == "__main__":
    raise SystemExit(main())
