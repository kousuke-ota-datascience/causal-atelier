# G01 Trial03 Remediation Package

## Purpose

Create the formal Trial03 `08 Trial Remediation Contract` after the G01 Trial02 formal FAIL.

No existing `06`, `P02`, or `07` contract is modified.

## Output path

```text
docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/
10_enhance_instruction/G01/
08_ENH-E5_G01_03_Remediation_Instruction.md
```

## Dry run

```bash
python3 /path/to/apply_g01_trial03_remediation_contract.py --repo-root .
```

## Apply

```bash
python3 /path/to/apply_g01_trial03_remediation_contract.py --repo-root . --apply
```

## After commit/push

Invoke the FAIL Rework Coding Agent for:

```text
GATE_ID=G01
TRIAL_NO=03
```

Use the new `08_ENH-E5_G01_03_Remediation_Instruction.md` as the normative remediation contract.

After rework succeeds:

1. assemble a new Trial03 Fixed Trial Candidate;
2. generate the canonical Trial03 Implementation Completion Report;
3. run the independent Test Agent for G01 / Trial03.
