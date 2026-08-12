# ENH-E5 AMEND-001 Trace Repair Package

## Purpose

Repair the traceability defect in AMEND-001 after the application commit:

`6e9c59515abb8c5c5981f96df5ad87782a7cdfc7`

The audited classification is:

- 35 instruction Markdown files changed by AMEND-001
- 2 normative semantic changes
- 33 metadata-only changes

The initial Ledger addendum incorrectly recorded metadata-only instruction changes as `(none)`.

## Changes made by this repair

- Adds a local `AMEND-001` metadata-only trace to all 33 metadata-only instruction documents.
- Verifies, but does not rewrite, the existing semantic traces in G01/P02 and G01/07.
- Appends `AMEND-001 Traceability Correction — TRACE-FIX-001` to `80_contract_amendment_log.md`.
- Retains the old erroneous `(none)` line as historical evidence and explicitly supersedes it.
- Does not modify the Trial01 blocker evidence.
- Uses the actual AMEND-001 commit changed-file set, not historical status-field regex inference.

## Dry run

```bash
python3 /path/to/apply_enh_e5_amend001_trace_fix.py --repo-root .
```

Expected on the current repository state:

- 33 instruction files changed
- 1 Ledger file changed
- total: **34 files**

## Apply

```bash
python3 /path/to/apply_enh_e5_amend001_trace_fix.py   --repo-root .   --apply
```

The script requires the ENH-E5 target tree to be clean by default.

## Rerun

After committing the first application, running the script again should report:

```text
files changed by this run: 0
```

## Suggested commit message

```text
AMEND-001 TRACE-FIX-001: repair instruction amendment traceability
```
