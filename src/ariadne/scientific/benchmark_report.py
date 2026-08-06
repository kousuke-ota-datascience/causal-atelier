"""Structured ENH-E1a scientific benchmark artifact and acceptance gate."""

from __future__ import annotations

import json
import os
import platform
import subprocess
from importlib import metadata
from pathlib import Path
from typing import Any


BENCHMARK_ID = "ariadne_ENH-E1a"
SCENARIO_MANIFEST = {
    "SB-E1A-001": "Randomized ATE",
    "SB-E1A-002": "Observed Confounding",
    "SB-E1A-003": "Missing Confounder",
    "SB-E1A-004": "Collider Adjustment",
    "SB-E1A-005": "Post-treatment Adjustment",
    "SB-E1A-006": "Poor Overlap",
    "SB-E1A-007": "Placebo",
    "SB-E1A-008": "Adjustment Variation",
    "SB-E1A-009": "Propensity Clipping",
    "SB-E1A-010": "Unresolved CPDAG/PAG",
    "SB-E1A-011": "Semi-synthetic ATE/ATT",
}
REQUIRED_SCENARIO_FIELDS = {
    "scenario_id", "scenario", "dgp_version", "seed", "ground_truth",
    "estimate", "bias", "rmse", "ci_coverage", "expected_status",
    "actual_status", "runtime_seconds", "package_versions",
}


def package_versions() -> dict[str, str]:
    names = ["ariadne", "numpy", "pandas", "scipy", "statsmodels", "scikit-learn"]
    versions: dict[str, str] = {}
    for name in names:
        try:
            versions[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            versions[name] = "NOT_INSTALLED"
    return versions


def evaluate_gate(scenarios: list[dict[str, Any]]) -> dict[str, Any]:
    by_id = {item["scenario_id"]: item for item in scenarios}
    manifest_complete = set(by_id) == set(SCENARIO_MANIFEST) and len(by_id) == len(scenarios)
    fields_complete = all(REQUIRED_SCENARIO_FIELDS <= set(item) for item in scenarios)
    deterministic = [item for item in scenarios if item["expected_status"] is not None]
    deterministic_rate = (
        sum(item["actual_status"] == item["expected_status"] for item in deterministic)
        / len(deterministic)
        if deterministic else 0.0
    )
    post_treatment_rate = float(
        by_id.get("SB-E1A-005", {}).get("actual_status") == "NOT_IDENTIFIED"
    )
    nonidentification_ids = {"SB-E1A-003", "SB-E1A-004", "SB-E1A-005"}
    nonidentification_rate = (
        sum(by_id.get(value, {}).get("actual_status") == "NOT_IDENTIFIED"
            for value in nonidentification_ids) / len(nonidentification_ids)
    )
    overlap_rate = float(
        by_id.get("SB-E1A-006", {}).get("actual_status") in {"WARN", "FAIL"}
    )
    quantitative = [by_id.get("SB-E1A-001", {}), by_id.get("SB-E1A-011", {})]
    max_standardized_bias = max(
        float(item.get("metrics", {}).get("standardized_absolute_bias", float("inf")))
        for item in quantitative
    )
    coverages = [float(item.get("ci_coverage", -1.0)) for item in quantitative]
    checks = {
        "manifest_complete": manifest_complete,
        "required_fields_complete": fields_complete,
        "deterministic_status_match_rate": deterministic_rate,
        "post_treatment_rejection_rate": post_treatment_rate,
        "nonidentification_detection_rate": nonidentification_rate,
        "poor_overlap_detection_rate": overlap_rate,
        "maximum_standardized_absolute_bias": max_standardized_bias,
        "ci_coverages": coverages,
        "multiple_seed_quantitative_scenarios": all(
            len(item.get("seeds", [])) > 1 for item in quantitative
        ),
    }
    passed = (
        manifest_complete
        and fields_complete
        and deterministic_rate == 1.0
        and post_treatment_rate == 1.0
        and nonidentification_rate == 1.0
        and overlap_rate == 1.0
        and max_standardized_bias <= 0.10
        and all(0.90 <= value <= 0.98 for value in coverages)
        and checks["multiple_seed_quantitative_scenarios"]
    )
    return {"gate_result": "PASS" if passed else "FAIL", "checks": checks}


def write_report(scenarios: list[dict[str, Any]], destination: Path) -> dict[str, Any]:
    gate = evaluate_gate(scenarios)
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        commit = "UNKNOWN"
    report = {
        "benchmark_id": BENCHMARK_ID,
        "code_commit": commit,
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "ci": os.getenv("CI", "false"),
        },
        "scenarios": sorted(scenarios, key=lambda item: item["scenario_id"]),
        **gate,
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report
