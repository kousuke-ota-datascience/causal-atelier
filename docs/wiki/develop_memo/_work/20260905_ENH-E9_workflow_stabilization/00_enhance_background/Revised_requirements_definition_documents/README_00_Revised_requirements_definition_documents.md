# Revised Requirements Definition Documents — ENH-E9

This directory is the only ENH-E9 location for revised canonical-document snapshots/proposals. Source canonical files under `docs/wiki/requirement_definition/**` remain reference-only.

## E9 revision decision

- `10_requirements_definition.md`: no new FR/NFR/AR text required. FR-048 implementation truth is treated as partially conformant at E9 baseline; see parent `03_requirements_revision.md`.
- `21_logical_data_design.md`: existing snapshot retained; G04 structured diagnostics delta is specified by parent `04_design_revision.md` and G04 06/07 until a full revised snapshot is needed.
- `22_product_basic_design.md`: existing Stage responsibility remains sufficient; no semantic delta required.
- `23_api_interface_design.md`: no route grammar change. Structured `DIAGNOSTICS_RESULT` payload extension is governed by G04 contract.
- `30_detailed_design.md`: existing snapshot retained; E9-specific diagnostics implementation delta is governed by parent `04_design_revision.md` and G04 06/07.

The copied files in this directory are the E9 reference snapshots captured at workflow initialization. Do not edit the source canonical directory from ENH-E9.
