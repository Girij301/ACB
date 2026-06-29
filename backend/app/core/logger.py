import logging
import sys

from app.core.config import settings


def setup_logger():
    logger = logging.getLogger("ACB_AI")

    # Avoid duplicate logs
    if logger.handlers:
        return logger

    logger.setLevel(settings.LOG_LEVEL)

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


logger = setup_logger()
