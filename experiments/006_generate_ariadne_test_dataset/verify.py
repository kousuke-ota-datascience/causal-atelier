"""Verify the generated registration dataset against Product scientific adapters."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from ariadne.product.domain.enums import ScientificStatus
from ariadne.product.ports.scientific_core import DiscoveryInput, EstimationInput
from ariadne.scientific.discovery.adapter import DiscoveryAdapter
from ariadne.scientific.inference.adapter import EstimationAdapter


OUTPUT_DIR = Path("artifacts/experiments/006_generate_ariadne_test_dataset")
DATASET = OUTPUT_DIR / "ariadne_completejourney_household_test.parquet"
CSV_DATASET = OUTPUT_DIR / "ariadne_completejourney_household_test.csv"
DISCOVERY_COLUMNS = [
    "age_midpoint",
    "income_midpoint_k",
    "household_size",
    "kids_count",
    "pre_sales_value",
    "pre_quantity",
    "treated",
    "outcome_sales_value",
]
ADJUSTMENT_SET = [
    "age_midpoint",
    "age_unknown",
    "income_midpoint_k",
    "income_unknown",
    "household_size",
    "kids_count",
    "pre_baskets",
    "pre_quantity",
    "pre_sales_value",
    "pre_coupon_disc",
    "pre_coupon_match_disc",
    "pre_retail_disc",
    "homeowner_yes",
    "homeowner_unknown",
    "married_yes",
    "married_unknown",
]


def main() -> int:
    parquet = pd.read_parquet(DATASET)
    csv = pd.read_csv(CSV_DATASET)
    pd.testing.assert_frame_equal(csv, parquet, check_dtype=False, rtol=1e-12, atol=1e-12)
    assert len(parquet) == 500
    assert parquet.isna().sum().sum() == 0
    assert set(parquet["treated"].unique()) == {0.0, 1.0}
    assert all(parquet[column].nunique() > 1 for column in ADJUSTMENT_SET)

    verification_dir = OUTPUT_DIR / "verification"
    discovery_summary = {}
    for algorithm in ("pc", "ges"):
        output = DiscoveryAdapter().run(
            DiscoveryInput(
                dataset_path=DATASET,
                algorithm=algorithm,
                parameters={"alpha": 0.05} if algorithm == "pc" else {},
                random_seed=42,
                analysis_spec={
                    "feature_columns": DISCOVERY_COLUMNS,
                    "constraints": {
                        "required_edges": [["treated", "outcome_sales_value"]],
                    },
                },
            ),
            verification_dir / "discovery" / algorithm,
        )
        assert output.scientific_status is ScientificStatus.VALID
        discovery_summary[algorithm] = output.summary

    graph = {
        "graph_type": "DAG",
        "nodes": [*ADJUSTMENT_SET, "treated", "outcome_sales_value"],
        "edges": [
            *[
                {
                    "source": column,
                    "target": target,
                    "endpoint_source": "TAIL",
                    "endpoint_target": "ARROW",
                }
                for column in ADJUSTMENT_SET
                for target in ("treated", "outcome_sales_value")
            ],
            {
                "source": "treated",
                "target": "outcome_sales_value",
                "endpoint_source": "TAIL",
                "endpoint_target": "ARROW",
            },
        ],
    }
    graph_path = verification_dir / "known_test_graph.json"
    graph_path.parent.mkdir(parents=True, exist_ok=True)
    graph_path.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")

    estimation_summary = {}
    for estimator in ("ols", "ipw", "aipw"):
        output = EstimationAdapter().run(
            EstimationInput(
                dataset_path=DATASET,
                graph_path=graph_path,
                estimator=estimator,
                parameters={},
                random_seed=42,
                analysis_spec={
                    "treatment": "treated",
                    "outcome": "outcome_sales_value",
                    "estimand": "ATE",
                    "target_population": None,
                    "adjustment_set": ADJUSTMENT_SET,
                    "assumptions": [
                        "consistency",
                        "conditional_exchangeability",
                        "positivity",
                        "no_interference",
                    ],
                    "inference_options": {},
                },
            ),
            verification_dir / "estimation" / estimator,
        )
        assert output.scientific_status is ScientificStatus.VALID
        estimation_summary[estimator] = output.summary

    summary = {
        "status": "PASS",
        "rows": len(parquet),
        "columns": len(parquet.columns),
        "missing_values": int(parquet.isna().sum().sum()),
        "treatment_counts": {
            str(int(key)): int(value)
            for key, value in parquet["treated"].value_counts().sort_index().items()
        },
        "discovery": discovery_summary,
        "estimation": estimation_summary,
    }
    summary_path = verification_dir / "verification_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
