from __future__ import annotations

from logging import FileHandler
from pathlib import Path
from uuid import uuid4

from causal_atelier.infrastructure.logging import CustomLogger


def test_custom_logger_writes_formatted_log(tmp_path: Path) -> None:
    log_path = tmp_path / "logs/app.log"
    logger_name = f"test_custom_logger.{uuid4()}"

    logger = CustomLogger(
        logger_name,
        log_path,
        logger_level="INFO",
        fmt_str="%(levelname)s:%(message)s",
    )
    logger.info("hello")

    for handler in logger.get_logger().handlers:
        handler.flush()

    assert log_path.read_text(encoding="utf-8") == "INFO:hello\n"


def test_custom_logger_does_not_duplicate_same_file_handler(tmp_path: Path) -> None:
    log_path = tmp_path / "app.log"
    logger_name = f"test_custom_logger.{uuid4()}"

    first = CustomLogger(logger_name, log_path)
    second = CustomLogger(logger_name, log_path)

    matching_handlers = [
        handler
        for handler in second.get_logger().handlers
        if isinstance(handler, FileHandler)
        and Path(handler.baseFilename).resolve() == log_path.resolve()
    ]

    assert first.get_logger() is second.get_logger()
    assert len(matching_handlers) == 1
