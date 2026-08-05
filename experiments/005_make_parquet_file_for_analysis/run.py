#!/usr/bin/env python3

from pathlib import Path
import argparse
from typing import Mapping, Sequence
import json
from ariadne.application.pipeline.etl import execute_completejourney_etl

DEFAULT_TABLE_TYPES: dict[str, str] = {
    "campaign_descriptions": "rda",
    "campaigns": "rda",
    "coupon_redemptions": "rda",
    "coupons": "rda",
    "demographics": "rda",
    "products": "rda",
    "transactions": "rds",
    "promotions": "rds",
}

## run.py の実行時に引数を引き渡し、テーブルタイプを指定できるようにするためのCLIパーサーを構築します。
## 指定するのはテーブル名のみ。テーブルタイプは Default で指定されているものを使用する。
def build_parser() -> argparse.ArgumentParser:
    """Build the integrated pipeline parser."""

    parser = argparse.ArgumentParser(
        description="Run causal discovery and causal inference as one reproducible pipeline.",
    )
    parser.add_argument("--table-names", default=None)
    return parser

def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse integrated CLI arguments."""

    return build_parser().parse_args(argv)

def main(argv: Sequence[str] | None = None) -> None:
    """Run the selected pipeline command strategy."""

    args = parse_args(argv)
    if args.table_names is None: 
        table_types = DEFAULT_TABLE_TYPES
    else:
        table_types = {
            k: DEFAULT_TABLE_TYPES[k] for k in DEFAULT_TABLE_TYPES.keys()
            if k in (json.loads(args.table_names) 
                     if args.table_names.startswith("[") 
                     else json.loads(Path(args.table_names).read_text())
                     )
        }

    outputs = execute_completejourney_etl(Path.cwd(), table_types=table_types)
    for logical_name, path in sorted(outputs.items()):
        print(f"{logical_name}: {path}")

if __name__ == "__main__":
    main()
