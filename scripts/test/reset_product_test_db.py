from __future__ import annotations

import os
from urllib.parse import urlsplit, urlunsplit

import psycopg
from psycopg import sql


def main() -> None:
    target = os.environ["ARIADNE_PRODUCT_TEST_DATABASE_URL"]
    parsed = urlsplit(target.replace("postgresql+psycopg://", "postgresql://", 1))
    database = parsed.path.lstrip("/")
    if not database or database == "postgres":
        raise RuntimeError("refusing to reset a missing or maintenance database")
    maintenance = urlunsplit((parsed.scheme, parsed.netloc, "/postgres", "", ""))
    with psycopg.connect(maintenance, autocommit=True) as connection:
        connection.execute(
            "SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
            "WHERE datname = %s AND pid <> pg_backend_pid()",
            (database,),
        )
        connection.execute(sql.SQL("DROP DATABASE IF EXISTS {} WITH (FORCE)").format(sql.Identifier(database)))
        connection.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database)))
    print(f"test_database_reset=ok database={database}", flush=True)


if __name__ == "__main__":
    main()
