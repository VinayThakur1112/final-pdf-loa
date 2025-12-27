import logging
import os
import sys

# Read GCP project ID (needed for trace correlation)
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")


def get_logger(name: str = None) -> logging.Logger:
    """
    Usage:
        logger = get_logger(__name__)
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger  # Avoid duplicate handlers

    formatter = logging.Formatter(
        fmt=(
            "[%(levelname)s] "
            f"[{GCP_PROJECT_ID}] "
            "[%(filename)s:%(lineno)d] "
            "[%(name)s] "
            "%(message)s"
        )
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False

    return logger