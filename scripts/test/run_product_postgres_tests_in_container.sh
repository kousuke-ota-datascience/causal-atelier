#!/usr/bin/env bash
set -uo pipefail

cd /app
evidence_dir="${ARIADNE_TEST_EVIDENCE_DIR:-/evidence}"
mkdir -p "$evidence_dir"

python scripts/test/reset_product_test_db.py
reset_code=$?
printf 'reset_exit_code=%s\n' "$reset_code"
if [ "$reset_code" -ne 0 ]; then exit "$reset_code"; fi

alembic -c alembic_product.ini upgrade head
migration_code=$?
printf 'migration_exit_code=%s\n' "$migration_code"
if [ "$migration_code" -ne 0 ]; then exit "$migration_code"; fi

alembic -c alembic_product.ini current
current_code=$?
printf 'migration_current_exit_code=%s\n' "$current_code"
if [ "$current_code" -ne 0 ]; then exit "$current_code"; fi

pytest "$@"
pytest_code=$?
printf 'pytest_exit_code=%s\n' "$pytest_code"
exit "$pytest_code"
