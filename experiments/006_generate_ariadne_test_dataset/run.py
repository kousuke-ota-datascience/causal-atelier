"""Generate a deterministic Ariadne registration dataset via the real preprocessor.

The synthetic source tables mimic the four Complete Journey tables consumed by
``ariadne.preprocessing.inference.FeatureBuilder``.  The file intended for Web
App registration is the builder's unmodified ``inference_frame`` output.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Sequence

import numpy as np
import pandas as pd

from ariadne.preprocessing.inference.builder import FeatureBuilder
from ariadne.preprocessing.inference.config import load_feature_config


DEFAULT_SEED = 20260805
DEFAULT_HOUSEHOLDS = 500
DEFAULT_CAMPAIGN_ID = "18"
DEFAULT_PRE_WEEKS = 8
DEFAULT_OUTPUT_DIR = Path("artifacts/experiments/006_generate_ariadne_test_dataset")
FEATURE_CONFIG = Path("configs/preprocessing/inference_features.yaml")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a synthetic Complete Journey dataset for Ariadne registration.",
    )
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--households", type=int, default=DEFAULT_HOUSEHOLDS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _days_since_epoch(value: datetime) -> int:
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    return (value - epoch).days


def _build_source_tables(
    *,
    seed: int,
    household_count: int,
) -> tuple[dict[str, pd.DataFrame], dict[str, Any]]:
    if household_count < 100:
        raise ValueError("households must be at least 100 for stable test diagnostics")

    rng = np.random.default_rng(seed)
    household_ids = np.arange(1, household_count + 1)
    age_labels = np.array(["19-24", "25-34", "35-44", "45-54", "55-64", "65+"])
    income_labels = np.array(
        ["Under 15K", "15-24K", "25-34K", "35-49K", "50-74K", "75-99K", "100-124K"]
    )
    age_index = rng.integers(0, len(age_labels), household_count)
    income_index = np.clip(age_index + rng.integers(-2, 3, household_count), 0, len(income_labels) - 1)
    home_owner = rng.random(household_count) < (0.25 + 0.09 * age_index)
    married = rng.random(household_count) < (0.30 + 0.07 * age_index)
    household_size = rng.integers(1, 6, household_count)
    kids_count = np.minimum(rng.poisson(0.9, household_count), household_size - 1)
    shopping_affinity = rng.normal(0, 1, household_count)

    age_values = age_labels[age_index].astype(object)
    income_values = income_labels[income_index].astype(object)
    home_ownership_values = np.where(home_owner, "Homeowner", "Renter").astype(object)
    marital_status_values = np.where(married, "Married", "Single").astype(object)
    age_values[rng.random(household_count) < 0.025] = "Unknown"
    income_values[rng.random(household_count) < 0.025] = "Unknown"
    home_ownership_values[rng.random(household_count) < 0.025] = "Unknown"
    marital_status_values[rng.random(household_count) < 0.025] = "Unknown"
    demographics = pd.DataFrame(
        {
            "household_id": household_ids,
            "age": age_values,
            "income": income_values,
            "home_ownership": home_ownership_values,
            "marital_status": marital_status_values,
            "household_size": household_size.astype(str),
            "household_comp": np.where(kids_count > 0, "Family", "Adult only"),
            "kids_count": kids_count.astype(str),
        }
    )

    centered_age = (age_index - age_index.mean()) / age_index.std()
    centered_income = (income_index - income_index.mean()) / income_index.std()
    treatment_logit = (
        -0.10
        + 0.35 * centered_age
        + 0.45 * centered_income
        + 0.25 * home_owner.astype(float)
        + 0.35 * shopping_affinity
    )
    treatment_probability = 1.0 / (1.0 + np.exp(-np.clip(treatment_logit, -2.0, 2.0)))
    treated = rng.binomial(1, treatment_probability)
    campaigns = pd.DataFrame(
        {
            "household_id": household_ids[treated == 1],
            "campaign_id": DEFAULT_CAMPAIGN_ID,
        }
    )

    first_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    campaign_start = first_date + timedelta(weeks=DEFAULT_PRE_WEEKS)
    campaign_end = first_date + timedelta(weeks=11, days=6)
    campaign_descriptions = pd.DataFrame(
        {
            "campaign_id": [DEFAULT_CAMPAIGN_ID],
            "start_date": [_days_since_epoch(campaign_start)],
            "end_date": [_days_since_epoch(campaign_end)],
        }
    )

    transaction_rows: list[dict[str, Any]] = []
    basket_number = 1
    for position, household_id in enumerate(household_ids):
        baseline_signal = (
            3.0 * centered_income[position]
            + 1.5 * centered_age[position]
            + 2.5 * shopping_affinity[position]
            + 0.8 * household_size[position]
        )
        for week in range(1, 13):
            basket_probability = float(
                np.clip(0.45 + 0.10 * shopping_affinity[position] + 0.02 * week, 0.15, 0.85)
            )
            basket_count = 1 + int(rng.random() < basket_probability) + int(rng.random() < 0.12)
            period_effect = 3.0 * treated[position] if week > DEFAULT_PRE_WEEKS else 0.0
            weekly_total = 24.0 + baseline_signal + 0.35 * week + period_effect + rng.normal(0, 2.0)
            weekly_total = max(5.0, weekly_total)
            proportions = rng.dirichlet(np.ones(basket_count))
            for basket_offset in range(basket_count):
                sales_value = weekly_total * proportions[basket_offset]
                if week <= DEFAULT_PRE_WEEKS:
                    pre_coupon_probability = float(
                        np.clip(0.12 + 0.05 * shopping_affinity[position], 0.03, 0.30)
                    )
                    coupon_used = rng.random() < pre_coupon_probability
                else:
                    coupon_used = bool(treated[position])
                coupon_discount = -float(coupon_used) * (0.20 + 0.03 * sales_value)
                coupon_match_discount = coupon_discount * float(rng.uniform(0.25, 0.75))
                transaction_time = first_date + timedelta(
                    weeks=week - 1,
                    days=basket_offset,
                    hours=int(rng.integers(8, 21)),
                )
                transaction_rows.append(
                    {
                        "household_id": int(household_id),
                        "basket_id": f"B{basket_number:07d}",
                        "week": week,
                        "transaction_timestamp": int(transaction_time.timestamp()),
                        "sales_value": round(float(sales_value), 6),
                        "quantity": int(rng.integers(1, 6)),
                        "retail_disc": round(-float(rng.uniform(0, 0.08) * sales_value), 6),
                        "coupon_disc": round(coupon_discount, 6),
                        "coupon_match_disc": round(coupon_match_discount, 6),
                    }
                )
                basket_number += 1

    transactions = pd.DataFrame(transaction_rows)
    metadata = {
        "data_generating_process": {
            "analysis_unit": "household",
            "pre_window_weeks": [1, 8],
            "outcome_window_weeks": [9, 12],
            "treatment": "campaign 18 membership",
            "treatment_assignment": "Bernoulli(logistic(baseline demographics, shopping affinity))",
            "outcome_treatment_increment_per_week": 3.0,
            "outcome_treatment_increment_over_four_weeks": 12.0,
            "note": "The increment is the structural simulation parameter, not an estimated effect.",
        },
        "treatment_counts": {
            "control": int((treated == 0).sum()),
            "treated": int((treated == 1).sum()),
        },
    }
    return {
        "transactions": transactions,
        "demographics": demographics,
        "campaigns": campaigns,
        "campaign_descriptions": campaign_descriptions,
    }, metadata


def _write_frame(frame: pd.DataFrame, path: Path) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".parquet":
        frame.to_parquet(path, index=False)
    else:
        frame.to_csv(path, index=False)
    return {
        "path": str(path),
        "rows": len(frame),
        "columns": len(frame.columns),
        "column_names": list(frame.columns),
        "sha256": _sha256(path),
    }


def generate(*, seed: int, household_count: int, output_dir: Path) -> dict[str, Any]:
    source_tables, generation_metadata = _build_source_tables(
        seed=seed,
        household_count=household_count,
    )
    config = load_feature_config(FEATURE_CONFIG)
    result = FeatureBuilder(config).build(
        source_tables,
        campaign_id=DEFAULT_CAMPAIGN_ID,
        pre_weeks=DEFAULT_PRE_WEEKS,
        collinearity_threshold=0.995,
    )

    raw_dir = output_dir / "source_tables"
    source_outputs = {
        name: _write_frame(frame, raw_dir / f"{name}.csv")
        for name, frame in source_tables.items()
    }
    registration_csv = _write_frame(
        result.inference_frame,
        output_dir / "ariadne_completejourney_household_test.csv",
    )
    registration_parquet = _write_frame(
        result.inference_frame,
        output_dir / "ariadne_completejourney_household_test.parquet",
    )
    standardized = _write_frame(
        result.standardized,
        output_dir / "diagnostics" / "standardized_frame.parquet",
    )
    dropped = _write_frame(
        result.dropped_columns,
        output_dir / "diagnostics" / "dropped_columns.csv",
    )

    manifest = {
        "manifest_version": "1.0",
        "generated_at": "deterministic; timestamp intentionally omitted",
        "seed": seed,
        "household_count": household_count,
        "campaign_id": DEFAULT_CAMPAIGN_ID,
        "pre_weeks": DEFAULT_PRE_WEEKS,
        "preprocessor": "ariadne.preprocessing.inference.builder.FeatureBuilder",
        "preprocessor_output": "FeatureBuildResult.inference_frame",
        "feature_config": {
            "path": str(FEATURE_CONFIG),
            "sha256": _sha256(FEATURE_CONFIG),
        },
        **generation_metadata,
        "source_tables": source_outputs,
        "registration_outputs": {
            "csv": registration_csv,
            "parquet": registration_parquet,
        },
        "diagnostics": {
            "standardized": standardized,
            "dropped_columns": dropped,
        },
    }
    manifest_path = output_dir / "generation_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    manifest["manifest_path"] = str(manifest_path)
    return manifest


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    manifest = generate(
        seed=args.seed,
        household_count=args.households,
        output_dir=args.output_dir,
    )
    print(json.dumps({
        "registration_outputs": manifest["registration_outputs"],
        "treatment_counts": manifest["treatment_counts"],
        "manifest_path": manifest["manifest_path"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
