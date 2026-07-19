"""Worker command line entrypoint."""

from __future__ import annotations

import argparse
import signal
import time

from causal_atelier.infrastructure.persistence import Database
from causal_atelier.infrastructure.settings import WebSettings

from .executor import Worker


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the causal-atelier execution worker"
    )
    parser.add_argument(
        "--once", action="store_true", help="Process at most one outbox item"
    )
    parser.add_argument("--worker-id", default=None)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    settings = WebSettings.from_env()
    settings.ensure_directories()
    database = Database(settings.database_url)
    if settings.auto_create_schema:
        database.create_schema()
    worker = Worker(database, settings, worker_id=args.worker_id)
    if args.once:
        worker.run_once()
        return
    running = True

    def stop(*_: object) -> None:
        nonlocal running
        running = False

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    while running:
        if not worker.run_once():
            time.sleep(settings.worker_poll_seconds)


if __name__ == "__main__":
    main()


__all__ = ["main"]
