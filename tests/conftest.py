from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(PROJECT_ROOT / "src"))


@pytest.fixture
def project_root() -> Path:
    """Return the repository root used by path-resolution tests."""

    return PROJECT_ROOT


def pytest_sessionfinish(session: object, exitstatus: int) -> None:
    """Keep repository-level smoke checks independent from generated caches."""

    for pycache in PROJECT_ROOT.rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)
