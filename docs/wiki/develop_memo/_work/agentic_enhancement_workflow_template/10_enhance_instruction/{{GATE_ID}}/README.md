# {{GATE_ID}} Gate-local Contract Package

このdirectoryは1 Gateのcontract / execution decompositionを保存する。

## Required

- `06_*` Gate Coding Contract
- `07_*` Gate Verification Contract

## Conditional

- `06_{{GATE_ID}}_P00_work_package_plan.md` — Work Package Mode
- `06_{{GATE_ID}}_P01_*` ... `P99_*` — planned Work Packages
- `08_*_Remediation_Instruction.md` — formal FAIL後
- `08_{{GATE_ID}}_R01_*` ... `R99_*` — remediation Work Packages
- `09_*_{{AMENDMENT_ID}}_*` — Gate contract defect時

Gateはacceptance contractであり、packageはexecution unitである。package数に応じてGateを分割してはならない。
