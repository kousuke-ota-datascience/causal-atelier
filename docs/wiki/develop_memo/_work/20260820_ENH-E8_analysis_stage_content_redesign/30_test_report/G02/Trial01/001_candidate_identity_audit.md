# G02 Trial01 — Candidate Identity Audit

- Gate: `G02`
- Trial: `01`
- Test Item ID: `001`
- Fixed Trial Candidate SHA: `a2399662f4f81ceadf36ae2aa71850d49786cae4`
- Result: `PASS`

## Acceptance Criteria

Entry identity audit required by frozen `07_Ariadne_ENH-E8_G02_test_instruction.md`. This is a precondition for all `G02-AC01`–`G02-AC23` verification.

## Method / command

```bash
git show -s --format='%H%n%P%n%s' a2399662f4f81ceadf36ae2aa71850d49786cae4
git worktree add --detach /tmp/ariadne-e8-g02-trial01-a239966 \
  a2399662f4f81ceadf36ae2aa71850d49786cae4
git -C /tmp/ariadne-e8-g02-trial01-a239966 rev-parse HEAD
git -C /tmp/ariadne-e8-g02-trial01-a239966 status --porcelain=v1
```

## Evidence

- G02 Trial01 Implementation Completion Report records `Fixed Trial Candidate SHA: a2399662f4f81ceadf36ae2aa71850d49786cae4`.
- The supplied SHA resolves to commit `a2399662f4f81ceadf36ae2aa71850d49786cae4` (`feat: redesign analysis stage content surfaces`).
- The primary worktree is at later documentation-attestation commit `768ef828…`; the Completion Report explicitly states that the attestation is not part of the fixed implementation candidate.
- An isolated detached worktree was created at `/tmp/ariadne-e8-g02-trial01-a239966`; its `HEAD` equals the report-recorded SHA. Candidate source and test commands below were executed only from that worktree.
- The pre-existing dirty file in the primary worktree is a G01 Completion Record and is not part of the detached candidate worktree.

## 判定理由

The Report now fixes an immutable candidate SHA, and the independently created detached worktree resolves exactly to it. The verification target is therefore established. A later documentation-only attestation commit does not alter the fixed candidate or make it mutable.
