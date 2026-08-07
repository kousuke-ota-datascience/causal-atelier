# G6 Trial 005 — Migration round trip

- Status: PASS
- Clean dedicated PostgreSQL database upgraded through `20260807_product_0006`; `test_postgres_contract.py` passed (`4 passed`).
- A seeded project survived downgrade to `20260807_product_0005` and re-upgrade; the generated OWNER membership and project row were preserved at head.
- Dedicated database was removed after verification.
