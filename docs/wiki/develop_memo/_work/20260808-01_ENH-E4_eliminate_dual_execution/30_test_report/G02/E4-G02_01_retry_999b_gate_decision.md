# E4-G02 Trial 01 Verification Retry — Final Gate Decision

- Project: Ariadne / causal-atelier
- Gate / Trial: E4-G02 / 01 verification retry
- Implementation commit: `166e90cd1c2d0e523fb863795a88343403d8cc44`
- Decision: **BLOCKED**

## Decision basis

The implementation commit remained unchanged. Initial PASS evidence for AC-001, AC-003, AC-004, and the 41-test relevant regression remains valid and was not overwritten. The requested TCP preflight to `172.17.0.1:55432` succeeded, but PostgreSQL protocol connection failed immediately afterward.

| Required result | Status |
|---|---|
| Product migration verification | BLOCKED — Alembic `current` and `upgrade head` failed at DB connection |
| AC-002 cross-family claim/lifecycle | BLOCKED — PostgreSQL contract suite could not acquire a DB connection |
| AC-005 double claim / lease ownership / invalid transition | BLOCKED — PostgreSQL contract suite could not acquire a DB connection |
| AC-001 / AC-003 / AC-004 | PASS — unchanged-commit evidence retained |
| Relevant regression | PASS — initial `41 passed` evidence retained |

## Infrastructure evidence

- `ARIADNE_PRODUCT_DATABASE_URL`: SET
- `ARIADNE_PRODUCT_TEST_DATABASE_URL`: SET
- TCP `172.17.0.1:55432`: CONNECTED
- PostgreSQL protocol: `connection is bad`
- PostgreSQL contract tests: `4 failed` before DB assertions
- Alembic `current`: exit `1`, connection failure
- Alembic `upgrade head`: exit `1`, connection failure

No source, automated test, migration, dependency, or implementation report was modified. Initial BLOCKED evidence and prior retry evidence remain intact. No Coding Trial 02 was started, and G03 was not entered.
