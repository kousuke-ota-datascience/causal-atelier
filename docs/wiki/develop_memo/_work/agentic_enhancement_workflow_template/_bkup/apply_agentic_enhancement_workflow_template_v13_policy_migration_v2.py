#!/usr/bin/env python3
"""Migrate the current Agentic Enhancement Workflow Template to the v0.05 policy safely (policy migration v2).

This is NOT a mirror replacement and NOT a blind ZIP overlay.

Policy:
  - current-only semantic artifacts: PRESERVE
  - explicitly obsolete artifacts: DELETE_OBSOLETE
  - nested README.md: MIGRATE_README to deterministic README_<PATH_ID>.md
  - reconstruction-only bundle artifacts: SKIP_BUNDLE
  - actual repository semantic bodies (root docs / prompts): preserve body and MERGE managed policy blocks
  - safe v0.05 control-plane files: CREATE / OVERWRITE

The migration is first executed on a temporary staging copy. Dry-run prints the
resulting diff without touching the checkout. --apply creates a full backup,
replaces the target with the validated staged tree, verifies exact equality,
and rolls back on failure.

No git add/commit/push is performed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from typing import Iterable
import zipfile

EXPECTED_BRANCH = "feature/ariadne_mvp_e7"
EXPECTED_BUNDLE_SHA256 = "d121f0660c633cbdbde3dbc6aa2f727988a407f722458dbe68ed33a76dd4cdef"
TARGET_REL = Path("docs/wiki/develop_memo/_work/agentic_enhancement_workflow_template")
BUNDLE_ROOT_NAME = "agentic_enhancement_workflow_template"

TEXT_EXTENSIONS = {
    ".md", ".py", ".json", ".yaml", ".yml", ".toml", ".txt",
    ".sh", ".bash", ".zsh", ".ini", ".cfg",
}
SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__", "_bkup"}

# Explicitly obsolete by the accepted workflow design. Deletion is intentional,
# not inferred from absence in v0.05.
EXPLICIT_OBSOLETE_PATHS = {
    Path("TEMPLATE_Current_State_Control_Sheet.md"),
}

# v0.05 is a reconstructed policy bundle. These files are reconstruction aids or
# instance-shaped reconstruction artifacts and must not be introduced into the
# actual production template tree.
SKIP_BUNDLE_PATHS = {
    Path("RECONSTRUCTION_MANIFEST.json"),
    Path("RECONSTRUCTION_NOTES.md"),
    Path("40_operator_workflows/architecture_review/02_target_architecture_decision_record.md"),
}

# These v0.05 files are safe control-plane replacements. Everything else is
# either merged semantically below or preserved from the actual repository.
SAFE_V005_COPY = {
    Path("README_Appendix_HowToUse.md"),
    Path("README_NAMING_CONVENTION.md"),
    Path("40_operator_workflows/preflight/AGENT_EXECUTION_READINESS.md"),
    Path("40_operator_workflows/tools/instantiate_agent_entry_prompts.py"),
    Path("40_operator_workflows/tools/readme_naming.py"),
    Path("40_operator_workflows/tools/test_workflow_metadata.py"),
    Path("40_operator_workflows/tools/validate_agent_execution_readiness.py"),
    Path("40_operator_workflows/tools/workflow_metadata.py"),
}

# Actual semantic-body authority: these are never blindly replaced by the
# reconstructed v0.05 copies. Managed blocks are merged where appropriate.
PRESERVE_SEMANTIC_PATHS = {
    Path("00_enhance_background/04_design_revision.md"),
    Path("00_enhance_background/05_requirements_design_consistency_and_traceability_review.md"),
    Path("40_operator_workflows/architecture_review/01_architecture_discovery_prompt.md"),
}

PROMPT_DIR = Path("40_operator_workflows/agent_entry_prompts")
PROMPT_RUNTIME = {
    "10_normal_execution_01_single_execution_coding_agent_prompt.md": ["GATE_ID", "TRIAL_NO"],
    "10_normal_execution_02_work_package_coding_agent_prompt.md": ["GATE_ID", "PACKAGE_ID", "TRIAL_NO"],
    "20_candidate_assembly_01_work_package_candidate_assembly_agent_prompt.md": ["GATE_ID", "TRIAL_NO"],
    "30_independent_verification_01_test_agent_prompt.md": ["GATE_ID", "TRIAL_NO"],
    "40_fail_remediation_01_fail_rework_coding_agent_prompt.md": ["GATE_ID", "REMEDIATION_PACKAGE_ID", "TRIAL_NO"],
    "50_orchestration_01_gate_orchestrator_prompt.md": ["GATE_ID", "TRIAL_NO"],
}
FIXED_VARS = [
    "PROJECT_NAME", "ENHANCE_ID", "ENHANCE_SHORT_ID", "BRANCH_NAME",
    "REMOTE_NAME", "WORK_ROOT", "WORK_DIR_NAME",
]

BEGIN_EXEC = "<!-- BEGIN MANAGED: WORKFLOW_EXECUTION_CONTROL -->"
END_EXEC = "<!-- END MANAGED: WORKFLOW_EXECUTION_CONTROL -->"
BEGIN_HOWTO = "<!-- BEGIN MANAGED: OPERATOR_QUICK_HOWTOUSE -->"
END_HOWTO = "<!-- END MANAGED: OPERATOR_QUICK_HOWTOUSE -->"
BEGIN_README_NAMING = "<!-- BEGIN MANAGED: README_NAMING_CONVENTION -->"
END_README_NAMING = "<!-- END MANAGED: README_NAMING_CONVENTION -->"
BEGIN_PROMPT_DOC = "<!-- BEGIN MANAGED: AGENT_ENTRY_PROMPT_CONTROL -->"
END_PROMPT_DOC = "<!-- END MANAGED: AGENT_ENTRY_PROMPT_CONTROL -->"
BEGIN_IDENTITY = "<!-- BEGIN MANAGED: EXECUTION_IDENTITY_CONTROL -->"
END_IDENTITY = "<!-- END MANAGED: EXECUTION_IDENTITY_CONTROL -->"
BEGIN_V004 = "<!-- BEGIN MANAGED: V004_CONTRACT_SIMPLIFICATION -->"
END_V004 = "<!-- END MANAGED: V004_CONTRACT_SIMPLIFICATION -->"
BEGIN_PACKAGE_REPORT = "<!-- BEGIN MANAGED: PACKAGE_REPORT_CANONICAL_STATE -->"
END_PACKAGE_REPORT = "<!-- END MANAGED: PACKAGE_REPORT_CANONICAL_STATE -->"
BEGIN_DERIVED_STATE = "<!-- BEGIN MANAGED: DERIVED_STATE_AUTHORITY -->"
END_DERIVED_STATE = "<!-- END MANAGED: DERIVED_STATE_AUTHORITY -->"
BEGIN_STRUCTURE = "<!-- BEGIN MANAGED: V005_CONTROL_PLANE_STRUCTURE -->"
END_STRUCTURE = "<!-- END MANAGED: V005_CONTROL_PLANE_STRUCTURE -->"
BEGIN_LOCAL_AUTHORITY = "<!-- BEGIN MANAGED: V005_LOCAL_AUTHORITY -->"
END_LOCAL_AUTHORITY = "<!-- END MANAGED: V005_LOCAL_AUTHORITY -->"

STALE_STATE_PATTERNS = [
    "TEMPLATE_Current_State_Control_Sheet.md",
    "Current_State_Control_Sheet.md",
    "Current State Control Sheet",
    "Current State promotion",
]

LOCAL_README_AUTHORITY = {
    Path("00_enhance_background/README_00.md"): """## v0.05 runtime boundary

`00_enhance_background/` はPlanning / Requirements / Design / provenanceのauthoring・audit layerである。Normal runtime preflightのauthorityにはしない。

Gate 06が `FROZEN` になった後、Coding Agentへ仕様補完目的でこのdirectoryを探索させない。必要なimplementation semanticsはGate 06 / assigned Pxxへself-containedに固定する。""",
    Path("10_enhance_instruction/README_10.md"): """## v0.05 runtime authority

Gate local READMEはHuman navigation / canonical artifact index専用であり、execution eligibilityを変更しない。

Normal-path routing authority:

```text
Gate dependency declaration = Gate 06 `Depends on`
Execution mode              = Gate 06 `Execution mode`
Required package set        = Gate 06 `Required packages`
Verification authority      = Gate 07
Package dependency          = each assigned Pxx `Depends on`
```

P00は存在してもoptional authoring / audit artifactであり、preflight / Candidate Assembly / Orchestratorのruntime authorityにはしない。""",
    Path("20_implementation_reports/README_20.md"): """## v0.05 evidence authority

```text
Package completion evidence = canonical package execution status report (`State: PACKAGE_COMPLETE`)
Candidate identity          = Implementation Completion Report
Checkpoint report           = optional implementation evidence
Implementation detail       = optional audit ledger
```

Package report / candidate evidenceをGate PASS authorityとして扱わない。""",
    Path("30_test_report/README_30.md"): """## v0.05 Gate decision authority

Gateのfinal authorityはcanonical `999_gate_decision` である。

Phase Fはcurrent Gateのcanonical 999だけを読み、PASS / FAIL / BLOCKEDをroutingする。Phase FはNext Gate readinessを判定せず、新しいstate / transition / promotion artifactを書かない。""",
    Path("40_operator_workflows/architecture_review/README_40_architecture_review.md"): """## v0.05 runtime boundary

Architecture ReviewはGate 06 freeze前に必要なsource confirmation / design decisionを行うconditional authoring workflowである。

Normal runtime preflightはArchitecture Review artifactをread dependencyにしない。Gate 06が `FROZEN` であることをruntime contractとして扱う。""",
}


def run(cmd: list[str], cwd: Path) -> tuple[int, str, str]:
    p = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def is_skipped(rel: Path) -> bool:
    return any(part in SKIP_DIRS for part in rel.parts)


def text_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if is_skipped(rel) or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        yield path


def snapshot_tree(root: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not root.exists():
        return out
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if is_skipped(rel):
            continue
        out[rel.as_posix()] = sha256_file(path)
    return out


def safe_extract_bundle(bundle: Path, destination: Path) -> Path:
    with zipfile.ZipFile(bundle) as zf:
        roots = set()
        for info in zf.infolist():
            name = Path(info.filename)
            if name.is_absolute() or ".." in name.parts:
                raise RuntimeError(f"unsafe ZIP member: {info.filename}")
            if info.filename and not info.filename.startswith("__MACOSX/"):
                roots.add(info.filename.split("/", 1)[0])
        if roots != {BUNDLE_ROOT_NAME}:
            raise RuntimeError(f"unexpected ZIP roots: {sorted(roots)}")
        zf.extractall(destination)
    root = destination / BUNDLE_ROOT_NAME
    if not root.is_dir():
        raise RuntimeError(f"bundle root missing: {BUNDLE_ROOT_NAME}/")
    return root


def validate_bundle(bundle: Path, skip_sha: bool) -> None:
    if not bundle.is_file():
        raise RuntimeError(f"bundle not found: {bundle}")
    actual = sha256_file(bundle)
    if not skip_sha and actual != EXPECTED_BUNDLE_SHA256:
        raise RuntimeError(
            "v0.05 bundle SHA-256 mismatch; refusing unknown bundle. "
            f"expected={EXPECTED_BUNDLE_SHA256} actual={actual}"
        )


def git_preflight(repo: Path, target: Path, allow_other_branch: bool, allow_dirty: bool) -> str:
    if not (repo / ".git").exists():
        raise RuntimeError(f"repo root does not contain .git: {repo}")
    rc, branch, err = run(["git", "branch", "--show-current"], repo)
    if rc != 0:
        raise RuntimeError(f"git branch check failed: {err}")
    if branch != EXPECTED_BRANCH and not allow_other_branch:
        raise RuntimeError(f"branch mismatch: expected={EXPECTED_BRANCH} actual={branch}")
    if not allow_dirty:
        rc, status, err = run(["git", "status", "--porcelain", "--", str(target.relative_to(repo))], repo)
        if rc != 0:
            raise RuntimeError(f"git status failed: {err}")
        if status:
            raise RuntimeError(
                "template tree has uncommitted changes; refusing migration. "
                "Commit/stash them or use --allow-dirty after review.\n" + status
            )
    return branch


def validate_manifest_integrity(target: Path, skip: bool) -> None:
    manifest = target / "MANIFEST.json"
    if not manifest.is_file() or skip:
        return
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(f"current MANIFEST.json parse failed: {exc}") from exc
    failures: list[str] = []
    for item in data.get("files", []):
        rel = item.get("path")
        expected = item.get("sha256")
        if not isinstance(rel, str) or not isinstance(expected, str):
            failures.append(f"invalid manifest entry: {item!r}")
            continue
        path = target / rel
        if not path.is_file():
            failures.append(f"missing: {rel}")
        elif sha256_file(path) != expected:
            failures.append(f"hash mismatch: {rel}")
    if failures:
        raise RuntimeError("current MANIFEST integrity failed:\n  - " + "\n  - ".join(failures[:30]))


def tokenize_component(component: str) -> str:
    m = re.match(r"^(\d{2})_(.+)$", component)
    if m:
        return m.group(1)
    token = re.sub(r"[^A-Za-z0-9.-]+", "_", component).strip("_")
    if not token:
        raise RuntimeError(f"directory component has no usable README token: {component!r}")
    return token


def readme_filename_for_directory(root: Path, directory: Path) -> str:
    rel = directory.resolve().relative_to(root.resolve())
    if rel == Path("."):
        return "README.md"
    return "README_" + "_".join(tokenize_component(p) for p in rel.parts) + ".md"


def build_readme_migration_map(root: Path) -> dict[Path, Path]:
    mapping: dict[Path, Path] = {}
    claimed: dict[Path, Path] = {}
    for old in sorted(root.rglob("README.md")):
        if old.parent == root:
            continue
        rel = old.relative_to(root)
        if is_skipped(rel):
            continue
        new = old.parent / readme_filename_for_directory(root, old.parent)
        if new in claimed and claimed[new] != old:
            raise RuntimeError(f"README naming collision: {claimed[new]} and {old} -> {new}")
        if new.exists() and new.read_bytes() != old.read_bytes():
            raise RuntimeError(
                "README migration collision with different content; refusing to guess authority: "
                f"{old.relative_to(root)} -> {new.relative_to(root)}"
            )
        claimed[new] = old
        mapping[old] = new
    return mapping


def migrate_nested_readmes(mapping: dict[Path, Path]) -> None:
    for old, new in sorted(mapping.items(), key=lambda kv: len(kv[0].parts), reverse=True):
        if new.exists():
            old.unlink()
        else:
            old.rename(new)


def replace_markdown_link_targets(text: str, file_path: Path, mapping: dict[Path, Path]) -> str:
    pattern = re.compile(r"(?P<prefix>!?\[[^\]]*\]\()(?P<target><[^>]+>|[^)\s]+)(?P<suffix>(?:\s+['\"][^'\"]*['\"])?\))")
    resolved_map = {old.resolve(): new.resolve() for old, new in mapping.items()}

    def repl(match: re.Match[str]) -> str:
        raw = match.group("target")
        wrapped = raw.startswith("<") and raw.endswith(">")
        target = raw[1:-1] if wrapped else raw
        if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target) or target.startswith("#"):
            return match.group(0)
        path_part, sep, fragment = target.partition("#")
        candidate = (file_path.parent / path_part).resolve()
        new_abs = resolved_map.get(candidate)
        if new_abs is None:
            return match.group(0)
        rel = os.path.relpath(new_abs, file_path.parent).replace(os.sep, "/")
        if path_part.startswith("./") and not rel.startswith("."):
            rel = "./" + rel
        new_target = rel + (("#" + fragment) if sep else "")
        if wrapped:
            new_target = f"<{new_target}>"
        return match.group("prefix") + new_target + match.group("suffix")

    return pattern.sub(repl, text)


def rewrite_readme_references(root: Path, mapping: dict[Path, Path]) -> None:
    if not mapping:
        return
    for path in text_files(root):
        old_text = path.read_text(encoding="utf-8")
        new_text = old_text
        if path.suffix.lower() == ".md":
            new_text = replace_markdown_link_targets(new_text, path, mapping)
        for old, new in sorted(mapping.items(), key=lambda kv: len(kv[0].as_posix()), reverse=True):
            old_root = old.relative_to(root).as_posix()
            new_root = new.relative_to(root).as_posix()
            new_text = new_text.replace(old_root, new_root)
            old_from_file = os.path.relpath(old, path.parent).replace(os.sep, "/")
            new_from_file = os.path.relpath(new, path.parent).replace(os.sep, "/")
            if old_from_file != "README.md":
                new_text = new_text.replace(old_from_file, new_from_file)
            elif path.parent.resolve() == old.parent.resolve():
                for a, b in {
                    "`README.md`": f"`{new.name}`",
                    "(README.md)": f"({new.name})",
                    "(./README.md)": f"(./{new.name})",
                    "'README.md'": f"'{new.name}'",
                    '"README.md"': f'"{new.name}"',
                }.items():
                    new_text = new_text.replace(a, b)
        if new_text != old_text:
            path.write_text(new_text, encoding="utf-8")


def managed_body(text: str, begin: str, end: str) -> str:
    m = re.search(re.escape(begin) + r"\n(.*?)\n" + re.escape(end), text, flags=re.S)
    if not m:
        raise RuntimeError(f"managed block missing from v0.05 source: {begin}")
    return m.group(1).rstrip()


def upsert_managed(text: str, begin: str, end: str, body: str) -> str:
    block = f"{begin}\n{body.rstrip()}\n{end}"
    pattern = re.compile(re.escape(begin) + r".*?" + re.escape(end), flags=re.S)
    if pattern.search(text):
        return pattern.sub(block, text)
    return text.rstrip() + "\n\n" + block + "\n"


def copy_if_changed(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    data = src.read_bytes()
    if not dst.exists() or dst.read_bytes() != data:
        dst.write_bytes(data)
        try:
            os.chmod(dst, src.stat().st_mode & 0o777)
        except OSError:
            pass


def identity_block(runtime: list[str]) -> str:
    fixed_lines = "\n".join(f"{key}={{{{{key}}}}}" for key in FIXED_VARS)
    runtime_lines = "\n".join(f"{key}={{{{{key}}}}}" for key in runtime)
    return f"""## Execution identity control

This template-side prompt is an authoring source and MUST NOT be executed directly. Before execution it MUST be instantiated under `{{{{WORK_ROOT}}}}/40_operator_workflows/agent_entry_prompts/`.

Enhancement-fixed values:

```text
{fixed_lines}
```

Runtime values for this execution:

```text
{runtime_lines}
```

If any Enhancement-fixed value remains unresolved in the Enhancement-side prompt, stop with `BLOCKED_ENHANCEMENT_IDENTITY_UNRESOLVED`. If any required Runtime value is missing or ambiguous, stop with `BLOCKED_EXECUTION_UNRESOLVABLE`."""


def merge_root_and_operator_docs(v005: Path, root: Path) -> None:
    root_readme = root / "README.md"
    if not root_readme.is_file():
        raise RuntimeError("root README.md missing from current template")
    src_root = (v005 / "README.md").read_text(encoding="utf-8")
    text = root_readme.read_text(encoding="utf-8")
    for begin, end in [
        (BEGIN_EXEC, END_EXEC),
        (BEGIN_HOWTO, END_HOWTO),
        (BEGIN_README_NAMING, END_README_NAMING),
    ]:
        text = upsert_managed(text, begin, end, managed_body(src_root, begin, end))
    root_readme.write_text(text, encoding="utf-8")

    operator_dir = root / "40_operator_workflows"
    operator_readme = operator_dir / readme_filename_for_directory(root, operator_dir)
    if operator_readme.is_file():
        src = (v005 / "40_operator_workflows/README_40.md").read_text(encoding="utf-8")
        text = operator_readme.read_text(encoding="utf-8")
        for begin, end in [
            (BEGIN_EXEC, END_EXEC),
            (BEGIN_HOWTO, END_HOWTO),
            (BEGIN_README_NAMING, END_README_NAMING),
        ]:
            text = upsert_managed(text, begin, end, managed_body(src, begin, end))
        operator_readme.write_text(text, encoding="utf-8")
    else:
        copy_if_changed(v005 / "40_operator_workflows/README_40.md", operator_readme)

    prompt_dir = root / PROMPT_DIR
    prompt_readme = prompt_dir / readme_filename_for_directory(root, prompt_dir)
    src_prompt_readme = (v005 / PROMPT_DIR / "README_40_agent_entry_prompts.md").read_text(encoding="utf-8")
    if prompt_readme.is_file():
        text = prompt_readme.read_text(encoding="utf-8")
        text = upsert_managed(text, BEGIN_PROMPT_DOC, END_PROMPT_DOC, managed_body(src_prompt_readme, BEGIN_PROMPT_DOC, END_PROMPT_DOC))
        prompt_readme.write_text(text, encoding="utf-8")
    else:
        copy_if_changed(v005 / PROMPT_DIR / "README_40_agent_entry_prompts.md", prompt_readme)

    vars_path = prompt_dir / "00_variable_conventions.md"
    src_vars = (v005 / PROMPT_DIR / "00_variable_conventions.md").read_text(encoding="utf-8")
    if vars_path.is_file():
        text = vars_path.read_text(encoding="utf-8")
        text = upsert_managed(text, BEGIN_PROMPT_DOC, END_PROMPT_DOC, managed_body(src_vars, BEGIN_PROMPT_DOC, END_PROMPT_DOC))
        vars_path.write_text(text, encoding="utf-8")
    else:
        copy_if_changed(v005 / PROMPT_DIR / "00_variable_conventions.md", vars_path)


def merge_local_readme_authority(v005: Path, root: Path) -> None:
    for rel, body in LOCAL_README_AUTHORITY.items():
        dst = root / rel
        if dst.is_file():
            text = dst.read_text(encoding="utf-8")
            dst.write_text(upsert_managed(text, BEGIN_LOCAL_AUTHORITY, END_LOCAL_AUTHORITY, body), encoding="utf-8")
        else:
            src = v005 / rel
            if src.is_file():
                copy_if_changed(src, dst)
                text = dst.read_text(encoding="utf-8")
                dst.write_text(upsert_managed(text, BEGIN_LOCAL_AUTHORITY, END_LOCAL_AUTHORITY, body), encoding="utf-8")


def merge_structure_doc(root: Path) -> None:
    path = root / "TEMPLATE_STRUCTURE.md"
    if not path.is_file():
        return
    body = """## v0.05 control-plane authority

Actual repository semantic body is retained. The following rules supersede conflicting older runtime-routing prose in this document.

```text
Gate dependency declaration = Gate 06 `Depends on`
Gate dependency evidence    = upstream canonical 999_gate_decision
Execution mode              = Gate 06 `Execution mode`
Required package set        = Gate 06 `Required packages`
Package dependency          = assigned Pxx `Depends on` + canonical package report
Gate readiness              = Gate 06 + Gate 07 + 06-declared prerequisite evidence + blocking preflightなし
Candidate identity          = Implementation Completion Report
Final Gate authority        = canonical 999_gate_decision
Gate local README           = Human index only
P00                         = optional authoring/audit only
```

Phase F reads only the current Gate canonical 999 and writes no state/promotion artifact. Mutable Current State Control Sheet is not part of the template."""
    text = path.read_text(encoding="utf-8")
    path.write_text(upsert_managed(text, BEGIN_STRUCTURE, END_STRUCTURE, body), encoding="utf-8")


def merge_prompts(v005: Path, root: Path) -> None:
    prompt_dir = root / PROMPT_DIR
    for name, runtime in PROMPT_RUNTIME.items():
        dst = prompt_dir / name
        if not dst.is_file():
            src = v005 / PROMPT_DIR / name
            if not src.is_file():
                raise RuntimeError(f"required prompt missing in current and bundle: {name}")
            copy_if_changed(src, dst)
            continue

        old = dst.read_text(encoding="utf-8")
        src_path = v005 / PROMPT_DIR / name
        src_text = src_path.read_text(encoding="utf-8") if src_path.is_file() else ""

        if BEGIN_IDENTITY in src_text and END_IDENTITY in src_text:
            id_body = managed_body(src_text, BEGIN_IDENTITY, END_IDENTITY)
        else:
            id_body = identity_block(runtime)
        new = upsert_managed(old, BEGIN_IDENTITY, END_IDENTITY, id_body)

        if BEGIN_V004 in src_text and END_V004 in src_text:
            new = upsert_managed(new, BEGIN_V004, END_V004, managed_body(src_text, BEGIN_V004, END_V004))

        if name == "10_normal_execution_02_work_package_coding_agent_prompt.md":
            package_body = """### Canonical package completion metadata

`PACKAGE_READY` is the Coding Agent terminal outcome label. Canonical dependency/candidate semantics use the package report fields instead of the literal outcome label.

```text
Gate: {{GATE_ID}}
Package: {{PACKAGE_ID}}
Trial: {{TRIAL_NO}}
State: PACKAGE_COMPLETE
```

Markdown decoration is non-semantic. The dependency resolver / Candidate Assembly / preflight MUST use these semantic fields and MUST NOT use `PACKAGE_READY` as a workflow cursor."""
            new = upsert_managed(new, BEGIN_PACKAGE_REPORT, END_PACKAGE_REPORT, package_body)

        dst.write_text(new, encoding="utf-8")


def apply_safe_bundle_files(v005: Path, root: Path) -> None:
    for rel in sorted(SAFE_V005_COPY):
        src = v005 / rel
        if not src.is_file():
            raise RuntimeError(f"required v0.05 source missing: {rel}")
        copy_if_changed(src, root / rel)


def _replace_section(text: str, heading_pattern: str, next_heading_pattern: str, replacement: str) -> str:
    pattern = re.compile(
        rf"(?ms)^##\s+{heading_pattern}\s*$.*?(?=^##\s+{next_heading_pattern}\s*$)"
    )
    if not pattern.search(text):
        return text
    return pattern.sub(replacement.rstrip() + "\n\n", text, count=1)


def remove_mutable_state_artifacts(root: Path) -> None:
    """Remove obsolete mutable-state runtime semantics without rewriting history.

    Historical schema records under 90_change_history are evidence of what older
    schema versions actually required and MUST remain semantically unchanged.
    Current normative templates are migrated with targeted edits first, then a
    conservative residual terminology normalization outside change history.
    """

    # 1) Targeted semantic rewrites for current normative artifacts.
    amendment = root / "00_enhance_background/80_contract_amendment_log.md"
    if amendment.is_file():
        text = amendment.read_text(encoding="utf-8")
        text = text.replace(
            "- Current State Control Sheet impact: {{IMPACT_OR_NONE}}",
            "- Canonical evidence / downstream dependency impact: {{IMPACT_OR_NONE}}",
        )
        amendment.write_text(text, encoding="utf-8")

    detail = root / "20_implementation_reports/TEMPLATE_implementation_report_detail.md"
    if detail.is_file():
        text = detail.read_text(encoding="utf-8")
        text = text.replace(
            "- verified stateはCurrent State Control Sheetで管理する。",
            "- verified stateはこのledgerで管理しない。Gate stateはcanonical 999 Gate Decision、candidate identityはImplementation Completion Report、package stateはcanonical package execution status reportから導出する。",
        )
        detail.write_text(text, encoding="utf-8")

    decision = root / "30_test_report/TEMPLATE_gate_decision_report.md"
    if decision.is_file():
        text = decision.read_text(encoding="utf-8")
        replacement = """## 9. Canonical Gate state consequence after PASS

Complete only when Status=PASS.

- Gate state authority: this canonical 999 Gate Decision
- Mutable state / promotion artifact update: NONE
- Downstream Gate dependency evidence: this Gate Decision
- Phase F write-set: NONE
"""
        text = _replace_section(
            text,
            r"9\.\s+Current State Control Sheet promotion",
            r"10\.\s+Failure remediation input",
            replacement,
        )
        decision.write_text(text, encoding="utf-8")

    # 2) Current normative prose normalization.  Never mutate 90_change_history:
    # it is append-only historical evidence, not current runtime authority.
    replacements = [
        (
            "TEMPLATE_Current_State_Control_Sheet.md / generated Current State Control Sheet\n  = Verified current state control plane\n  = final PASS済みevidenceのみから構成する、現在の正へのindex\n\n",
            "Canonical evidence-derived state\n  = mutable state sheetを持たない\n  = package state / Gate state / candidate stateはcanonical evidenceから導出する\n\n",
        ),
        (
            "### Step 3 — Current State Control Sheetを初期化する\n\n`TEMPLATE_Current_State_Control_Sheet.md`をコピーし、開始時点で既にverifiedな状態だけを記載する。\n\n未検証の実装予定やpackage進捗をverified current stateへ書かない。",
            "### Step 3 — canonical evidence authorityを確認する\n\nmutable state sheetは作成しない。Package dependencyはpackage execution report、Gate dependencyはcanonical 999 Gate Decision、Gate readinessはGate 06 + Gate 07 + 06-declared prerequisite evidence + blocking preflight、candidate readinessはImplementation Completion Reportから導出する。",
        ),
        ("Current State Control Sheetへverified stateをpromotion", "canonical 999 Gate DecisionをGate state authorityとして確定"),
        ("Current State Control Sheetの初期verified baselineを作る", "canonical evidence authorityとdependencyを確認する"),
        (" / Current State Control Sheet", ""),
        ("、Current State Control Sheet", ""),
        ("Current State Control Sheet、", "canonical evidence、"),
        ("Current State Control Sheet", "canonical evidence-derived state model"),
        ("TEMPLATE_Current_State_Control_Sheet.md", "canonical evidence sources"),
        ("Current_State_Control_Sheet.md", "canonical evidence sources"),
        ("Control Sheetを更新する", "canonical evidenceからstateを再導出する"),
        ("Current State promotion", "canonical evidence derivation"),
        ("PASS-only verified-state promotion", "PASS-derived canonical state"),
        ("verified current state promotion", "canonical evidence-derived state transition"),
        ("verified-state promotion", "verified-state derivation"),
    ]

    for path in text_files(root):
        if path.name == "MANIFEST.json":
            continue
        rel = path.relative_to(root)
        if rel.parts and rel.parts[0] == "90_change_history":
            continue
        old = path.read_text(encoding="utf-8")
        new_text = old
        for a, b in replacements:
            new_text = new_text.replace(a, b)
        if new_text != old:
            path.write_text(new_text, encoding="utf-8")

    # 3) Explicitly obsolete artifact deletion.
    for rel in EXPLICIT_OBSOLETE_PATHS:
        path = root / rel
        if path.exists():
            path.unlink()

    root_readme = root / "README.md"
    body = """## Derived state and terminal routing authority

Mutable state sheetは作成しない。State / readiness / dependencyはcanonical evidenceとfrozen contractから直接導出する。

```text
Pxx dependency
  -> canonical package execution status report (`State: PACKAGE_COMPLETE`)

Gate dependency
  -> Gate 06 `Depends on` + upstream canonical 999_gate_decision

Gate readiness
  -> Gate 06 + Gate 07 + 06-declared prerequisite evidence + blocking preflightなし

Candidate identity
  -> Implementation Completion Report

Final Gate authority
  -> canonical 999_gate_decision
```

Gate local READMEはHuman index専用、P00はoptional authoring/audit専用とする。Phase Fはcurrent Gateのcanonical 999だけを読み、Next Gate readinessはNext Gate Phase Aで判定する。Phase Fは新しいstate / transition / promotion artifactを書かない。"""
    text = root_readme.read_text(encoding="utf-8")
    root_readme.write_text(upsert_managed(text, BEGIN_DERIVED_STATE, END_DERIVED_STATE, body), encoding="utf-8")



def regenerate_manifest(root: Path) -> None:
    manifest_path = root / "MANIFEST.json"
    if not manifest_path.exists():
        return
    try:
        old = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        old = {}

    files = []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p == manifest_path:
            continue
        rel = p.relative_to(root)
        if is_skipped(rel):
            continue
        data = p.read_bytes()
        files.append({
            "path": rel.as_posix(),
            "sha256": sha256_bytes(data),
            "bytes": len(data),
            "lines": data.count(b"\n") + (0 if not data or data.endswith(b"\n") else 1),
        })

    manifest = {
        "schema_version": old.get("schema_version", 2),
        "manifest_policy": old.get(
            "manifest_policy",
            "MANIFEST.json is excluded from its own hash set to avoid self-reference. Regenerate after all template changes are final.",
        ),
        "file_count": len(files),
        "files": files,
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_manifest(root: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = root / "MANIFEST.json"
    if not manifest_path.exists():
        return errors
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"MANIFEST parse failed: {exc}"]
    entries = data.get("files", [])
    if data.get("file_count") != len(entries):
        errors.append("MANIFEST file_count mismatch")
    seen = set()
    for item in entries:
        rel = item.get("path")
        if not isinstance(rel, str) or not rel or rel in seen:
            errors.append(f"MANIFEST invalid/duplicate path: {rel!r}")
            continue
        seen.add(rel)
        p = root / rel
        if not p.is_file():
            errors.append(f"MANIFEST path missing: {rel}")
            continue
        blob = p.read_bytes()
        if sha256_bytes(blob) != item.get("sha256"):
            errors.append(f"MANIFEST sha mismatch: {rel}")
        if len(blob) != item.get("bytes"):
            errors.append(f"MANIFEST bytes mismatch: {rel}")
    return errors


def validate_staging(root: Path, before: dict[str, str], readme_map: dict[Path, Path]) -> list[str]:
    errors: list[str] = []

    for rel in EXPLICIT_OBSOLETE_PATHS:
        if (root / rel).exists():
            errors.append(f"obsolete artifact remains: {rel}")

    for rel in SKIP_BUNDLE_PATHS:
        # If an identically named actual file already existed before migration, it
        # is preserved. Otherwise reconstruction-only bundle material must not be created.
        if rel.as_posix() not in before and (root / rel).exists():
            errors.append(f"reconstruction-only bundle artifact was created: {rel}")

    for stale in sorted(root.rglob("README.md")):
        if stale.parent != root:
            errors.append(f"nested unqualified README remains: {stale.relative_to(root)}")

    for path in text_files(root):
        if path.name == "MANIFEST.json":
            continue
        rel = path.relative_to(root)
        # 90_change_history is historical evidence. Older-schema references to the
        # retired Current State Control Sheet are expected and must not be treated
        # as current-runtime stale references.
        if rel.parts and rel.parts[0] == "90_change_history":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for token in STALE_STATE_PATTERNS:
            if token in text:
                errors.append(f"stale mutable-state reference {token!r}: {rel}")

    # Historical schema bodies are append-only evidence and must remain byte-identical.
    for rel_str, before_hash in before.items():
        rel = Path(rel_str)
        if len(rel.parts) >= 2 and rel.parts[0] == "90_change_history" and rel.name.startswith("schema_") and rel.suffix == ".md":
            p = root / rel
            if not p.is_file():
                errors.append(f"history preservation regression: deleted {rel}")
            elif sha256_file(p) != before_hash:
                errors.append(f"history preservation regression: modified {rel}")

    # User-highlighted current-only semantic artifact must remain byte-identical if present.
    example = "00_enhance_background/01_enhancement_concept_and_requirement_revision_plan.md"
    if example in before:
        p = root / example
        if not p.is_file():
            errors.append(f"preservation regression: deleted {example}")
        elif sha256_file(p) != before[example]:
            errors.append(f"preservation regression: modified {example}")

    decision = root / "30_test_report/TEMPLATE_gate_decision_report.md"
    if decision.is_file():
        dt = decision.read_text(encoding="utf-8")
        if "## 9. Canonical Gate state consequence after PASS" not in dt:
            errors.append("Gate Decision template missing canonical PASS consequence section")
        if "Mutable state / promotion artifact update: NONE" not in dt:
            errors.append("Gate Decision template still implies mutable state promotion")
        if "Sections to update:" in dt:
            errors.append("Gate Decision template retains obsolete state-update field")

    errors.extend(validate_manifest(root))

    tools = [
        root / "40_operator_workflows/tools/workflow_metadata.py",
        root / "40_operator_workflows/tools/test_workflow_metadata.py",
        root / "40_operator_workflows/tools/validate_agent_execution_readiness.py",
        root / "40_operator_workflows/tools/readme_naming.py",
        root / "40_operator_workflows/tools/instantiate_agent_entry_prompts.py",
    ]
    missing = [str(p.relative_to(root)) for p in tools if not p.is_file()]
    if missing:
        errors.append("required tooling missing: " + ", ".join(missing))
    else:
        rc, out, err = run([sys.executable, "-m", "py_compile", *[str(p) for p in tools]], root)
        if rc != 0:
            errors.append(f"Python compile failed: {out or err}")
        test = root / "40_operator_workflows/tools/test_workflow_metadata.py"
        rc, out, err = run([sys.executable, str(test)], root)
        if rc != 0:
            errors.append(f"metadata self-test failed: {out or err}")

    return errors


def apply_migration_pipeline(v005: Path, root: Path) -> dict[Path, Path]:
    readme_map = build_readme_migration_map(root)
    migrate_nested_readmes(readme_map)
    rewrite_readme_references(root, readme_map)

    apply_safe_bundle_files(v005, root)
    merge_root_and_operator_docs(v005, root)
    merge_local_readme_authority(v005, root)
    merge_structure_doc(root)
    merge_prompts(v005, root)
    remove_mutable_state_artifacts(root)

    # Reconstruction-only bundle files are never copied. Actual files with the
    # same path, if they pre-existed, remain untouched by this policy.
    regenerate_manifest(root)
    return readme_map


def classify_plan(
    before: dict[str, str],
    after: dict[str, str],
    bundle_paths: set[str],
    readme_map: dict[Path, Path],
    root_before: Path,
) -> list[tuple[str, str]]:
    actions: list[tuple[str, str]] = []
    old_readmes = {old.relative_to(root_before).as_posix(): new.relative_to(root_before).as_posix() for old, new in readme_map.items()}
    new_readmes = set(old_readmes.values())

    for old, new in sorted(old_readmes.items()):
        actions.append(("MIGRATE_README", f"{old} -> {new}"))

    for rel in sorted(set(before) | set(after)):
        if rel in old_readmes or rel in new_readmes:
            continue
        if rel in before and rel not in after:
            action = "DELETE_OBSOLETE" if Path(rel) in EXPLICIT_OBSOLETE_PATHS else "DELETE_UNEXPECTED"
            actions.append((action, rel))
        elif rel not in before and rel in after:
            actions.append(("CREATE", rel))
        elif before.get(rel) != after.get(rel):
            actions.append(("MODIFY_MANAGED", rel))

    for rel in sorted(bundle_paths):
        if Path(rel) in SKIP_BUNDLE_PATHS:
            actions.append(("SKIP_BUNDLE", rel))

    # Explicitly surface representative current-only preservation.
    for rel, digest in sorted(before.items()):
        if rel not in bundle_paths and rel not in old_readmes and rel in after and after[rel] == digest:
            actions.append(("PRESERVE_CURRENT_ONLY", rel))
    return actions


def print_plan(actions: list[tuple[str, str]]) -> None:
    counts: dict[str, int] = {}
    for action, _ in actions:
        counts[action] = counts.get(action, 0) + 1
    order = [
        "DELETE_OBSOLETE", "MIGRATE_README", "MODIFY_MANAGED", "CREATE",
        "SKIP_BUNDLE", "PRESERVE_CURRENT_ONLY", "DELETE_UNEXPECTED",
    ]
    print("V0.05 POLICY MIGRATION PLAN")
    for name in order:
        print(f"  {name:23s}: {counts.get(name, 0)}")
    print()
    for action, rel in actions:
        if action == "PRESERVE_CURRENT_ONLY" and counts.get(action, 0) > 20:
            continue
        print(f"[{action}] {rel}")
    if counts.get("PRESERVE_CURRENT_ONLY", 0) > 20:
        print(f"[PRESERVE_CURRENT_ONLY] ... {counts['PRESERVE_CURRENT_ONLY']} files total (suppressed detailed list)")


def backup_target(target: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = target.parent / f"{target.name}_pre_v005_policy_migration_backup_{ts}"
    if backup.exists():
        raise RuntimeError(f"backup already exists: {backup}")
    shutil.copytree(target, backup, copy_function=shutil.copy2)
    return backup


def restore_backup(target: Path, backup: Path) -> None:
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(backup, target, copy_function=shutil.copy2)


def trees_equal(a: Path, b: Path) -> tuple[bool, str]:
    sa = snapshot_tree(a)
    sb = snapshot_tree(b)
    if set(sa) != set(sb):
        only_a = sorted(set(sa) - set(sb))[:10]
        only_b = sorted(set(sb) - set(sa))[:10]
        return False, f"file-set mismatch only_target={only_a} only_staging={only_b}"
    for rel in sorted(sa):
        if sa[rel] != sb[rel]:
            return False, f"hash mismatch: {rel}"
    return True, "exact file-set/hash match"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--apply", action="store_true", help="Apply validated staged migration. Default is dry-run.")
    ap.add_argument("--allow-other-branch", action="store_true")
    ap.add_argument("--allow-dirty", action="store_true")
    ap.add_argument("--skip-bundle-sha-check", action="store_true")
    ap.add_argument("--skip-manifest-integrity", action="store_true")
    args = ap.parse_args()

    repo = Path(args.repo_root).resolve()
    bundle = Path(args.bundle).resolve()
    target = repo / TARGET_REL

    try:
        validate_bundle(bundle, args.skip_bundle_sha_check)
        branch = git_preflight(repo, target, args.allow_other_branch, args.allow_dirty)
        if not target.is_dir():
            raise RuntimeError(f"target template directory missing: {target}")
        validate_manifest_integrity(target, args.skip_manifest_integrity)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    before = snapshot_tree(target)

    with tempfile.TemporaryDirectory(prefix="v005_policy_migration_") as td:
        temp = Path(td)
        bundle_root = safe_extract_bundle(bundle, temp / "bundle")
        bundle_paths = {
            p.relative_to(bundle_root).as_posix()
            for p in bundle_root.rglob("*") if p.is_file()
        }
        staging = temp / "staging" / target.name
        shutil.copytree(target, staging, copy_function=shutil.copy2)

        try:
            readme_map_stage = apply_migration_pipeline(bundle_root, staging)
            after = snapshot_tree(staging)
            # Convert staging paths to target-root-shaped paths for readable migration mapping.
            logical_map = {
                target / old.relative_to(staging): target / new.relative_to(staging)
                for old, new in readme_map_stage.items()
            }
            errors = validate_staging(staging, before, readme_map_stage)
            actions = classify_plan(before, after, bundle_paths, logical_map, target)
            unexpected_deletes = [rel for action, rel in actions if action == "DELETE_UNEXPECTED"]
            if unexpected_deletes:
                errors.append("unexpected deletion(s): " + ", ".join(unexpected_deletes))
        except Exception as exc:
            print(f"ERROR: staging migration failed: {exc}", file=sys.stderr)
            return 2

        print(f"Repository : {repo}")
        print(f"Branch     : {branch}")
        print(f"Target     : {target}")
        print(f"Bundle     : {bundle}")
        print(f"Bundle SHA : {sha256_file(bundle)}")
        print(f"Mode       : {'APPLY' if args.apply else 'DRY-RUN'}")
        print()
        print_plan(actions)

        example = "00_enhance_background/01_enhancement_concept_and_requirement_revision_plan.md"
        if example in before:
            status = "PASS" if example in after and before[example] == after[example] else "FAIL"
            print(f"\nExample preservation: {status} {example}")

        if errors:
            print("\nVALIDATION: FAIL", file=sys.stderr)
            for err in errors:
                print(f"  - {err}", file=sys.stderr)
            print("No repository files were modified.", file=sys.stderr)
            return 2

        print("\nSTAGING VALIDATION: PASS")
        if not args.apply:
            print("DRY_RUN: PASS")
            print("No repository files were modified.")
            return 0

        backup: Path | None = None
        try:
            backup = backup_target(target)
            shutil.rmtree(target)
            shutil.copytree(staging, target, copy_function=shutil.copy2)

            ok, evidence = trees_equal(target, staging)
            if not ok:
                raise RuntimeError(f"post-apply exact-tree validation failed: {evidence}")

            post_errors = validate_staging(target, before, readme_map_stage)
            if post_errors:
                raise RuntimeError("post-apply validation failed:\n  - " + "\n  - ".join(post_errors))

            rc, out, err = run(["git", "diff", "--check", "--", str(TARGET_REL)], repo)
            if rc != 0:
                # Markdown hard line-break spaces may legitimately trigger this. Keep diagnostic,
                # but do not silently rewrite source content.
                print(f"WARN: git diff --check diagnostics:\n{out or err}", file=sys.stderr)
        except Exception as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            if backup is not None:
                print("Rolling back from backup...", file=sys.stderr)
                restore_backup(target, backup)
                print("Rollback complete.", file=sys.stderr)
            return 2

        print(f"\nBackup: {backup}")
        print("APPLY: PASS")
        print("Post-validation: PASS")
        print("No commit or push was performed.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
