from __future__ import annotations

import os
import threading
import uuid
from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from ariadne.product.persistence.repositories import SqlExecutionRepository


@pytest.fixture
def postgres_engine():  # type: ignore[no-untyped-def]
    url = os.getenv("ARIADNE_PRODUCT_TEST_DATABASE_URL")
    if not url:
        pytest.skip("ARIADNE_PRODUCT_TEST_DATABASE_URL is not configured")
    engine = create_engine(url, pool_pre_ping=True)
    yield engine
    engine.dispose()


def _seed_queued_execution(engine):  # type: ignore[no-untyped-def]
    ids = {name: str(uuid.uuid4()) for name in ("project", "artifact", "dataset", "execution")}
    now = datetime.now(timezone.utc)
    with engine.begin() as connection:
        connection.execute(
            text("INSERT INTO product_project "
                 "(project_id,name,status,created_at,updated_at) "
                 "VALUES (:project,'claim-contract','ACTIVE',:now,:now)"),
            {**ids, "now": now},
        )
        connection.execute(
            text("INSERT INTO product_artifact "
                 "(artifact_id,project_id,artifact_type,object_key,content_hash,media_type,size_bytes,metadata_json,created_at) "
                 "VALUES (:artifact,:project,'DATASET_FILE',:object_key,'hash','text/csv',1,'{}',:now)"),
            {**ids, "object_key": f"postgres-contract/{ids['artifact']}", "now": now},
        )
        connection.execute(
            text("INSERT INTO product_dataset_version "
                 "(dataset_version_id,project_id,source_artifact_id,dataset_key,name,version_label,content_hash,"
                 "schema_json,profile_summary_json,row_count,column_count,created_at) "
                 "VALUES (:dataset,:project,:artifact,'claim','claim','v1','hash','{}','{}',1,1,:now)"),
            {**ids, "now": now},
        )
        connection.execute(
            text("INSERT INTO product_execution "
                 "(execution_id,project_id,dataset_version_id,batch_key,operation,analysis_spec_json,"
                 "algorithm_or_estimator,parameter_json,code_version,runtime_version_json,snapshot_hash,"
                 "status,retry_count,requested_by,requested_at) "
                 "VALUES (:execution,:project,:dataset,:execution,'DISCOVERY','{}','pc','{}','test','{}','hash',"
                 "'QUEUED',0,'postgres-contract',:now)"),
            {**ids, "now": now},
        )
    return ids


def _delete_seed(engine, ids):  # type: ignore[no-untyped-def]
    with engine.begin() as connection:
        connection.execute(text("DELETE FROM product_execution WHERE execution_id=:execution"), ids)
        connection.execute(text("DELETE FROM product_dataset_version WHERE dataset_version_id=:dataset"), ids)
        connection.execute(text("DELETE FROM product_artifact WHERE artifact_id=:artifact"), ids)
        connection.execute(text("DELETE FROM product_project WHERE project_id=:project"), ids)


@pytest.mark.postgres
def test_product_migration_contains_only_product_schema(postgres_engine):  # type: ignore[no-untyped-def]
    tables = set(inspect(postgres_engine).get_table_names())
    assert {
        "alembic_version_product",
        "product_idempotency",
        "product_project",
        "product_dataset_version",
        "product_execution",
        "product_result",
        "product_artifact",
        "product_graph_version",
        "product_annotation",
    } <= tables
    assert not any(name.startswith(("execution_stage", "pipeline_", "outbox")) for name in tables)


@pytest.mark.postgres
def test_product_constraints_and_transaction_rollback(postgres_engine):  # type: ignore[no-untyped-def]
    project_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    connection = postgres_engine.connect()
    transaction = connection.begin()
    connection.execute(
        text("INSERT INTO product_project (project_id,name,status,created_at,updated_at) "
             "VALUES (:id,'rollback','ACTIVE',:now,:now)"),
        {"id": project_id, "now": now},
    )
    transaction.rollback()
    connection.close()
    with postgres_engine.connect() as check:
        assert check.scalar(
            text("SELECT count(*) FROM product_project WHERE project_id=:id"), {"id": project_id}
        ) == 0

    with pytest.raises(IntegrityError):
        with postgres_engine.begin() as invalid:
            invalid.execute(
                text("INSERT INTO product_project (project_id,name,status,created_at,updated_at) "
                     "VALUES (:id,'invalid','UNKNOWN',:now,:now)"),
                {"id": str(uuid.uuid4()), "now": now},
            )

    with pytest.raises(IntegrityError):
        with postgres_engine.begin() as invalid_fk:
            invalid_fk.execute(
                text("INSERT INTO product_artifact "
                     "(artifact_id,project_id,artifact_type,object_key,content_hash,media_type,size_bytes,metadata_json,created_at) "
                     "VALUES (:artifact,:missing,'LOG',:object_key,'hash','text/plain',1,'{}',:now)"),
                {"artifact": str(uuid.uuid4()), "missing": str(uuid.uuid4()),
                 "object_key": f"missing/{uuid.uuid4()}", "now": now},
            )

    ids = _seed_queued_execution(postgres_engine)
    try:
        with postgres_engine.connect() as connection:
            object_key = connection.scalar(
                text("SELECT object_key FROM product_artifact WHERE artifact_id=:artifact"), ids
            )
        with pytest.raises(IntegrityError):
            with postgres_engine.begin() as duplicate:
                duplicate.execute(
                    text("INSERT INTO product_artifact "
                         "(artifact_id,project_id,artifact_type,object_key,content_hash,media_type,size_bytes,metadata_json,created_at) "
                         "VALUES (:new_artifact,:project,'LOG',:object_key,'hash','text/plain',1,'{}',:now)"),
                    {**ids, "new_artifact": str(uuid.uuid4()), "object_key": object_key, "now": now},
                )
    finally:
        _delete_seed(postgres_engine, ids)


@pytest.mark.postgres
def test_claim_next_is_atomic_across_concurrent_workers(postgres_engine):  # type: ignore[no-untyped-def]
    ids = _seed_queued_execution(postgres_engine)
    factory = sessionmaker(bind=postgres_engine, expire_on_commit=False)
    barrier = threading.Barrier(2)
    claimed: list[str | None] = []
    failures: list[BaseException] = []

    def claim(worker_token: str) -> None:
        try:
            barrier.wait(timeout=5)
            with factory() as session:
                execution = SqlExecutionRepository(session).claim_next(worker_token)
                session.commit()
                claimed.append(execution.execution_id if execution else None)
        except BaseException as exc:  # pragma: no cover - surfaced by assertion below
            failures.append(exc)

    try:
        workers = [threading.Thread(target=claim, args=(str(uuid.uuid4()),)) for _ in range(2)]
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join(timeout=10)
        assert not failures
        assert claimed.count(ids["execution"]) == 1
        assert claimed.count(None) == 1
        with postgres_engine.connect() as connection:
            assert connection.scalar(
                text("SELECT status FROM product_execution WHERE execution_id=:execution"), ids
            ) == "RUNNING"
    finally:
        _delete_seed(postgres_engine, ids)
