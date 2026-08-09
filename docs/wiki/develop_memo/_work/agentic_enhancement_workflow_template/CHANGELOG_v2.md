# v2 Change Log

## Major schema changes from complete/v1

1. Added `TEMPLATE_Current_State_Control_Sheet.md` as the verified-state control plane.
2. Changed `10_enhance_instruction` from enhancement-global 06/07 to Gate-local 06/07.
3. Added Trial-local `08_*_Remediation_Instruction.md` and explicit `09_*_Gate_Contract_Amendment.md` for the exceptional case where the contract itself is defective.
4. Added passed-Gate immutability and mandatory regression semantics.
5. Added first-class Transition Debt lifecycle and traceability.
6. Changed Test Agent independence from a document-deny model to explicit authority/precedence.
7. Changed `20_implementation_reports` to Gate-local; implementation detail is no longer the enhancement-wide verified-state ledger.
8. Changed `30_test_report` to Gate-local and added protected-contract / Transition Debt fields.
9. Renamed `40_operator_prompts` to `40_operator_workflows`.
10. Added conditional architecture-review workflow.
11. Added prerequisite/preflight workflow separate from product acceptance.
12. Added human-controlled sequential runbook pattern for destructive or high-risk operations.
13. Canonicalized Gate ID to `GNN` and added Enhancement / Transition Debt identifiers.
14. Added PASS-only promotion into verified current state.

## Non-goals

- v2 does not prescribe project-specific architecture.
- v2 does not require architecture review for every small enhancement.
- v2 does not make the Current State Control Sheet a new requirements source of truth; it is an index/control plane over approved contracts and verified evidence.
