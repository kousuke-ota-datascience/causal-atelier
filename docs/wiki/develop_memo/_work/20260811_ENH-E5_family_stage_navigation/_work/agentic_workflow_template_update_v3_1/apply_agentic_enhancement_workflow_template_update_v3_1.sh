#!/usr/bin/env bash
set -euo pipefail
REPO="/loc0/bigbrother/repositories/causal-atelier"
DRY=0
while [[ $# -gt 0 ]]; do case "$1" in --repo) REPO="$2"; shift 2;; --dry-run) DRY=1; shift;; *) echo "unknown arg: $1" >&2; exit 2;; esac; done
SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAYLOAD="$SELF_DIR/payload/agentic_enhancement_workflow_template"
TARGET="$REPO/docs/wiki/develop_memo/_work/agentic_enhancement_workflow_template"
validate_payload(){
  local policy="$PAYLOAD/40_operator_workflows/BROWSER_E2E_GATE_POLICY.md"
  local wp="$PAYLOAD/40_operator_workflows/agent_entry_prompts/10_normal_execution_02_work_package_coding_agent_prompt.md"
  local testp="$PAYLOAD/40_operator_workflows/agent_entry_prompts/30_independent_verification_01_test_agent_prompt.md"
  local gate07="$PAYLOAD/10_enhance_instruction/{{GATE_ID}}/07_{{PROJECT_NAME}}_{{ENHANCE_ID}}_{{GATE_ID}}_test_instruction.md"
  [[ -f "$policy" ]] || { echo "payload missing Browser E2E policy" >&2; exit 1; }
  grep -q '^## 12\. Final status' "$wp" || { echo "Work Package Final status missing" >&2; exit 1; }
  grep -q '^## 13\. Final status' "$testp" || { echo "Test Agent Final status missing" >&2; exit 1; }
  grep -q 'PRODUCT_INTEGRATION_DEFECT' "$policy" || { echo "Browser E2E failure taxonomy missing" >&2; exit 1; }
  grep -q 'canonical Browser E2E suite' "$gate07" || { echo "07 Browser E2E planning rule missing" >&2; exit 1; }
  grep -q 'BROWSER_E2E_GATE_POLICY.md' "$PAYLOAD/TEMPLATE_STRUCTURE.md" || { echo "TEMPLATE_STRUCTURE Browser policy entry missing" >&2; exit 1; }
  if grep -R -nE 'ENH-E5|G04|Trial02|20260811_ENH-E5|family_stage_navigation|analysis_mode' "$PAYLOAD" >/tmp/agentic_workflow_v3_1_specific_refs.$$; then
    echo 'project-specific value found in payload:' >&2
    cat /tmp/agentic_workflow_v3_1_specific_refs.$$ >&2
    rm -f /tmp/agentic_workflow_v3_1_specific_refs.$$
    exit 1
  fi
  rm -f /tmp/agentic_workflow_v3_1_specific_refs.$$ || true
}
validate_payload
run(){ if [[ $DRY -eq 1 ]]; then printf '[dry-run]'; printf ' %q' "$@"; echo; else "$@"; fi; }
[[ -d "$REPO/.git" ]] || { echo "not a git repo: $REPO" >&2; exit 1; }
[[ -d "$TARGET" ]] || { echo "target missing: $TARGET" >&2; exit 1; }
[[ -z "$(git -C "$REPO" status --porcelain)" ]] || { echo "working tree is not clean" >&2; exit 1; }
AP="$TARGET/40_operator_workflows/agent_entry_prompts"
rename_if_needed(){ local old="$1" new="$2"; if [[ -e "$AP/$old" && ! -e "$AP/$new" ]]; then run git -C "$REPO" mv "${AP#$REPO/}/$old" "${AP#$REPO/}/$new"; fi; }
rename_if_needed VARIABLE_CONVENTIONS.md 00_variable_conventions.md
rename_if_needed coding_agent_prompt.md 10_normal_execution_01_single_execution_coding_agent_prompt.md
rename_if_needed work_package_coding_agent_prompt.md 10_normal_execution_02_work_package_coding_agent_prompt.md
rename_if_needed work_package_candidate_assembly_agent_prompt.md 20_candidate_assembly_01_work_package_candidate_assembly_agent_prompt.md
rename_if_needed test_agent_prompt.md 30_independent_verification_01_test_agent_prompt.md
rename_if_needed fail_rework_coding_agent_prompt.md 40_fail_remediation_01_fail_rework_coding_agent_prompt.md
# Copy all payload files; existing baseline text was preserved and minimally modified.
while IFS= read -r -d '' src; do rel="${src#$PAYLOAD/}"; dst="$TARGET/$rel"; run mkdir -p "$(dirname "$dst")"; run cp "$src" "$dst"; done < <(find "$PAYLOAD" -type f -print0)
# Remove legacy duplicates if both old/new exist after previous partial work.
for old in VARIABLE_CONVENTIONS.md coding_agent_prompt.md work_package_coding_agent_prompt.md work_package_candidate_assembly_agent_prompt.md test_agent_prompt.md fail_rework_coding_agent_prompt.md; do [[ ! -e "$AP/$old" ]] || run rm "$AP/$old"; done
# dry-runでは未変更targetを監査せず、payload自体のinvariantを検査して終了する。
if [[ $DRY -eq 1 ]]; then
  echo '--- payload invariant audit ---'
  grep -R -nE '80_contract_amendment_log|BLOCKED_CANDIDATE_IDENTITY|BLOCKED_REMEDIATION_NOT_APPLIED|Final status|Final Status|READY_FOR_TEST|BROWSER_E2E_GATE_POLICY|PRODUCT_INTEGRATION_DEFECT|TEST_ORCHESTRATION_DEFECT|canonical Browser E2E suite' \
    "$PAYLOAD/00_enhance_background" "$PAYLOAD/10_enhance_instruction" "$PAYLOAD/20_implementation_reports" "$PAYLOAD/30_test_report" "$PAYLOAD/40_operator_workflows" | head -160 || true
  echo '--- current branch / status (unchanged) ---'
  git -C "$REPO" branch --show-current
  git -C "$REPO" status --short
  echo 'DRY_RUN_COMPLETE: no files changed.'
  exit 0
fi

# MANIFESTは全変更確定後、適用先template全体から再生成する。
"$SELF_DIR/regenerate_agentic_workflow_manifest.py" "$TARGET"

# Audit legacy refs and key invariants.
echo '--- legacy filename references (review; expected only in history/migration notes if any) ---'
git -C "$REPO" grep -nE '(^|/)(VARIABLE_CONVENTIONS|coding_agent_prompt|work_package_coding_agent_prompt|work_package_candidate_assembly_agent_prompt|test_agent_prompt|fail_rework_coding_agent_prompt)\.md' -- "${TARGET#$REPO/}" || true
echo '--- key invariant grep ---'
grep -R -nE '80_contract_amendment_log|BLOCKED_CANDIDATE_IDENTITY|BLOCKED_REMEDIATION_NOT_APPLIED|Final status|Final Status|READY_FOR_TEST|BROWSER_E2E_GATE_POLICY|PRODUCT_INTEGRATION_DEFECT|TEST_ORCHESTRATION_DEFECT|canonical Browser E2E suite' "$TARGET/00_enhance_background" "$TARGET/10_enhance_instruction" "$TARGET/20_implementation_reports" "$TARGET/30_test_report" "$TARGET/40_operator_workflows" | head -160 || true
echo '--- diff check ---'
git -C "$REPO" diff --check
echo '--- status ---'
git -C "$REPO" status --short
echo '--- diff summary ---'
git -C "$REPO" diff --stat --find-renames
