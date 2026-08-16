# Workflow Schema v2 — ENH-E7 instance

Key semantics used by this revised instance:

- Gate / Trial / Work Package are distinct.
- 06 and 07 are separate semantic/verification authorities.
- P00/Pxx implement WORK_PACKAGE mode.
- Work Package = bounded implementation + focused verification + lightweight handoff evidence.
- package execution evidence != Fixed Trial Candidate != Gate PASS.
- package eligibility is derived from real dependencies, not `READY_TO_EXECUTE` literals.
- package SHA is traceability evidence, not an execution lock.
- Gate-level Candidate Assembly establishes the Fixed Trial Candidate.
- Current State promotion occurs after final PASS only.
- Browser E2E is a small critical-journey proof.
- Preflight distinguishes FAIL / WARN / INFO and avoids non-essential protocol hard-fails.
