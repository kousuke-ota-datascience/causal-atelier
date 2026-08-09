#!/usr/bin/env bash
set -uo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"
project_name="ariadne-test"
evidence_dir="${ARIADNE_TEST_EVIDENCE_DIR:-$repo_root/test-results/postgres}"
mkdir -p "$evidence_dir"
started_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
commit="$(git rev-parse HEAD 2>/dev/null || printf unknown)"
log_file="$evidence_dir/run-$(date -u +%Y%m%dT%H%M%SZ).txt"

set +e
docker compose -f compose.test.yaml -p "$project_name" up -d database_test
up_code=$?
if [ "$up_code" -eq 0 ]; then
  docker compose -f compose.test.yaml -p "$project_name" run --build --rm \
    -v "$evidence_dir:/evidence" test_runner \
    /app/scripts/test/run_product_postgres_tests_in_container.sh "$@" 2>&1 | tee "$log_file"
  run_code=${PIPESTATUS[0]}
else
  run_code="$up_code"
fi
set -e

finished_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
{
  printf 'implementation_commit=%s\nstarted_at=%s\nfinished_at=%s\n' "$commit" "$started_at" "$finished_at"
  printf 'database_service=database_test\ndatabase_image=postgres:17-alpine\n'
  printf 'compose_project=%s\nrun_exit_code=%s\npytest_command=' "$project_name" "$run_code"
  printf 'pytest %q ' "$@"
  printf '\nstdout_stderr=%s\n' "$log_file"
} > "$evidence_dir/$(basename "$log_file" .txt).metadata.txt"
exit "$run_code"
