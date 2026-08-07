"""Worker runner – poll loop that claims and processes executions."""

from __future__ import annotations

import logging
import os
import signal
import socket
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from ariadne.adapters.local_artifact_store import LocalArtifactStore
from ariadne.interfaces.worker.execution_processor import ExecutionProcessor
from ariadne.product.application.exploratory_service import ExploratoryWorkspaceService
from ariadne.scientific.core_adapter import ScientificCoreAdapter

logger = logging.getLogger(__name__)

_stop = False


def _handle_signal(signum: int, frame: Any) -> None:
    global _stop
    logger.info("Signal %d received, stopping worker...", signum)
    _stop = True


def run_worker(
    database_url: str,
    artifact_root: Path,
    poll_seconds: float = 2.0,
) -> None:
    """Main worker loop: poll for QUEUED executions and process them."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from ariadne.product.persistence.unit_of_work import SqlUnitOfWork

    engine = create_engine(database_url)
    session_factory = sessionmaker(bind=engine)

    @contextmanager
    def uow_context():  # type: ignore[no-untyped-def]
        session = session_factory()
        try:
            yield SqlUnitOfWork(session)
        finally:
            session.close()

    artifact_store = LocalArtifactStore(artifact_root)
    scientific_core = ScientificCoreAdapter()

    processor = ExecutionProcessor(
        uow_factory=uow_context,
        scientific_core=scientific_core,
        artifact_store=artifact_store,
    )
    exploratory_processor = ExploratoryWorkspaceService(session_factory, artifact_store)

    signal.signal(signal.SIGTERM, _handle_signal)
    signal.signal(signal.SIGINT, _handle_signal)

    logger.info("Worker started. Polling every %.1fs", poll_seconds)
    global _stop
    _stop = False
    worker_token = str(uuid.uuid4())
    worker_id = f"{socket.gethostname()}:{os.getpid()}"

    while not _stop:
        try:
            with uow_context() as uow:
                execution = uow.executions.claim_next(worker_token)
                uow.commit()

            if execution is not None:
                logger.info("Claimed execution %s (%s)", execution.execution_id, execution.operation.value)
                processor.process(execution)
            else:
                exploratory_execution_id = exploratory_processor.claim_next(
                    worker_token, worker_id=worker_id,
                )
                if exploratory_execution_id is not None:
                    logger.info("Claimed exploratory execution %s", exploratory_execution_id)
                    exploratory_processor.process_execution(
                        exploratory_execution_id, worker_token=worker_token,
                    )
                else:
                    time.sleep(poll_seconds)
        except Exception as exc:
            logger.exception("Worker loop error: %s", exc)
            time.sleep(poll_seconds)

    logger.info("Worker stopped.")


def main() -> None:
    import logging as _logging
    _logging.basicConfig(level=_logging.INFO)

    database_url = os.getenv("ARIADNE_PRODUCT_DATABASE_URL")
    if not database_url:
        raise RuntimeError("ARIADNE_PRODUCT_DATABASE_URL is required")
    artifact_root = Path(os.getenv("ARIADNE_ARTIFACT_ROOT", ".ariadne/objects"))
    poll_seconds = float(os.getenv("ARIADNE_WORKER_POLL_SECONDS", "2"))

    run_worker(database_url, artifact_root, poll_seconds)


if __name__ == "__main__":
    main()
