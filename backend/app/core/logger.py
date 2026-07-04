import logging
import sys

from app.core.config import settings


LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(module)s.%(funcName)s:%(lineno)d | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger() -> logging.Logger:
    """
    Configure the application's central logger.

    The logger is configured only once and reused across the
    entire application.
    """

    logger = logging.getLogger("ACB_AI")

    if logger.handlers:
        return logger

    logger.setLevel(settings.LOG_LEVEL.upper())
    logger.propagate = False

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    """
    Return the central application logger or one of its children.

    Example:
        logger = get_logger(__name__)
    """

    root_logger = setup_logger()

    if name:
        return root_logger.getChild(name)

    return root_logger


logger = setup_logger()