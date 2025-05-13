import inspect
import logging
import re
import sys
from typing import Any

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="log_")

    level: str = "INFO"
    serialize: bool = False

    obfuscates: str = "password"


settings = LogSettings()


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        try:
            level: str | int = logger.level(record.levelname).name
        except ValueError:  # pragma: no cover
            level = record.levelno  # pragma: no cover

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame:
            filename = frame.f_code.co_filename
            is_logging = filename == logging.__file__
            is_frozen = "importlib" in filename and "_bootstrap" in filename
            if depth > 0 and not (is_logging or is_frozen):
                break
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def obfuscate_message(message: str) -> str:
    regex = "|".join([f"(?<={x}=)\\S+" for x in settings.obfuscates.split(",")])
    return re.sub(regex, "'xxx'", message)


def formatter(record: dict[str, Any]) -> str:
    record["message"] = obfuscate_message(record["message"])
    if record["extra"]:
        return (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> <level>{level}</level>:"
            + "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            + "<level>{extra} - {message}</level>\n{exception}"
        )
    return (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> <level>{level}</level>:"
        + "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        + "<level>{message}</level>\n{exception}"
    )


def endpoint_filter(record: dict[str, Any]) -> bool:
    forbidden = [
        "/health",
        "/healthz",
        "/readiness",
        "/metrics",
        "/api/doc",
        "/openapi.json",
    ]
    for field in forbidden:
        if field in record["message"] and not record["exception"]:
            return False
    return True


def log_setup(backtrace: bool = False, diagnose: bool = False) -> None:
    """
    Intercept uvicorn logger by loguru
    """
    # intercept everything at the root logger
    level = logging.getLevelName(settings.level)
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(level)
    # remove every other logger's handlers
    # and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():  # pylint: disable=no-member
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True
    logger.configure(
        handlers=[
            {  # type: ignore
                "sink": sys.stderr,
                "filter": endpoint_filter,
                "format": formatter,
                "serialize": settings.serialize,
                "level": level,
                "backtrace": backtrace,
                "diagnose": diagnose,
            }
        ]
    )
