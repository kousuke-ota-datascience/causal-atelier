# G6 Trial 004 — Migration round trip

- Status: PASS
- Dedicated PostgreSQL database upgraded to `20260807_product_0006`, seeded data was preserved across downgrade to `20260807_product_0005` and re-upgrade to head, and `tests/product/test_postgres_contract.py` passed (`4 passed in 1.72s`).
- Dedicated database was removed after verification.
