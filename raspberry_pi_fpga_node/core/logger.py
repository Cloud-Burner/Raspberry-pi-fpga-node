"""This module provides logging functionality"""

import sys

from loguru import logger


def setup_logger(log_level: str = "DEBUG") -> None:
    logger.remove()
    logger.add(sys.stdout, level=log_level, enqueue=True, backtrace=True, diagnose=True)
    logger.add(
        "logs/debug.log",
        level="DEBUG",
        rotation="1 MB",
        retention="7 days",
        enqueue=True,
    )

    class InterceptHandler:
        def write(self, message: str) -> None:
            if message.strip():
                logger.info(message.strip())

        def flush(self) -> None:
            pass

    sys.stdout = InterceptHandler()
    sys.stderr = InterceptHandler()
