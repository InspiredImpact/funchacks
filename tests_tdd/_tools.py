__all__ = ["testlogger", "has_args"]

import logging
from typing import Any, Generator

import pytest


@pytest.fixture()
def testlogger() -> Generator[logging.Logger, Any, None]:
    logger = logging.getLogger()
    logger.info("Running function object test...")
    yield logger
    logger.info("Testing complete.")


def has_args(obj: Any, /, *args: str) -> bool:
    return all((hasattr(obj, _) for _ in args))
