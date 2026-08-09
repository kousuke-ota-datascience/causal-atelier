# E4-G07 Trial01 — 007 Architecture Exit Audit

## Result

`PASS`

| Question | Answer |
|---|---|
| Product runtime can reach retired legacy authority? | NO |
| Deployment invokes legacy API/CLI/worker? | NO |
| Shared science works without legacy orchestration? | YES |
| Product bootstrap can invoke root legacy migrations? | NO |
| Fresh Product DB is Product-only migration state? | YES |
| Low-level CLI owns persistent Product lifecycle? | NO |
| Existing auditable CLI bypasses canonical Execution? | NO / no such CLI identified |
| Legacy-named contracts classified by real consumption? | YES |
| G02–G06 old authority revived? | NO |
| Residual legacy surfaces explicitly non-authoritative? | YES |

## Residual classifications

- `src/ariadne/legacy/`: `RETIRED_UNREACHABLE` / physical source retained for later cleanup.
- Root `alembic.ini` and `migrations/`: `HISTORY_ONLY` for Product bootstrap.
- `ariadne.causal`, preprocessing, shared, and ScientificCoreAdapter: `RETAIN_SHARED_CAPABILITY`.
- Low-level analysis CLIs: `LOW_LEVEL_UTILITY`.
- Legacy-named consumed data contracts, where present: `COMPATIBILITY_DATA_CONTRACT`.

## Decision

Evidence supports:

```text
Product runtime legacy dependency = 0
Product bootstrap legacy migration dependency = 0
low-level CLI hidden persistent lifecycle = 0
shared scientific capability = preserved
TD-005 CLOSABLE
```

`TD-005` is closable at the architecture level; it is recorded as `CLOSED` only in the final gate decision per the instruction.

