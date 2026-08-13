# ENH-E7 Controlled Runbook

Use this directory for Human-controlled step prompts/results when executing or auditing the workflow manually.

Canonical order:

1. Architecture Review / approvals.
2. G01 freeze + preflight.
3. G01 Pxx execution.
4. G01 Candidate Assembly.
5. G01 Independent Verification / 999.
6. Current State promotion after PASS.
7. repeat for G02.

No runbook step may bypass Agent Execution Readiness.
