from __future__ import annotations

from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING
from logging import FileHandler, Formatter, Logger, getLogger
from pathlib import Path
from typing import Any


_LOG_LEVELS = {
    "DEBUG": DEBUG,
    "INFO": INFO,
    "WARNING": WARNING,
    "ERROR": ERROR,
    "CRITICAL": CRITICAL,
}


class CustomLogger(): 
    def __init__(self, 
                 logger_name, 
                 file_handler_path, 
                 logger_level="INFO", 
                 fmt_str="%(asctime)s, %(levelname)s, %(filename)s, %(name)s, %(funcName)s, %(lineno)s, %(message)s"): 

        log_level = _LOG_LEVELS.get(str(logger_level).upper(), ERROR)
        log_path = Path(file_handler_path).resolve()
        log_path.parent.mkdir(parents=True, exist_ok=True)

        self._logger = getLogger(logger_name)
        self._logger.setLevel(log_level)
        self._logger.propagate = False

        if not self._has_file_handler(log_path):
            handler = FileHandler(log_path, encoding="utf-8")
            handler.setLevel(log_level)
            handler.setFormatter(Formatter(fmt_str))
            self._logger.addHandler(handler)

    def get_logger(self) -> Logger:
        return self._logger

    def __getattr__(self, name: str) -> Any:
        return getattr(self._logger, name)

    def _has_file_handler(self, log_path: Path) -> bool:
        return any(
            isinstance(handler, FileHandler)
            and Path(handler.baseFilename).resolve() == log_path
            for handler in self._logger.handlers
        )
