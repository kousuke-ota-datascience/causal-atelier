# Schema v11 Change History

## Summary

Schema v11 standardizes canonical artifact paths so that filenames and directory names use ASCII technical English only.

## Changes

1. Removed Japanese text from all canonical filenames in the template tree.
2. Renamed Gate primary contracts to:
   - `06_{{PROJECT_NAME}}_{{ENHANCE_ID}}_{{GATE_ID}}_implementation_instruction.md`
   - `07_{{PROJECT_NAME}}_{{ENHANCE_ID}}_{{GATE_ID}}_test_instruction.md`
3. Renamed `00_enhance_background` planning / requirements / design artifact filenames to technical English.
4. Updated `TEMPLATE_STRUCTURE.md`, `MANIFEST.json`, README references, and parameterized operator prompts to the same naming schema.
5. Added a canonical filename policy: ASCII filenames/directories, technical English semantic suffixes, Japanese allowed only in document titles/body text.

## Compatibility

This is a naming/schema migration. Document semantics, Gate / Trial / Work Package responsibilities, self-containment rules, and 08 DELTA / CONSOLIDATED remediation policy are unchanged.
