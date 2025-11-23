"""
logger.py
---------
Central logging utility for unified application logging.
"""


import logging


def get_logger(name: str = "fundwise"):
    """
    Create and configure a logger.

    Args:
        name (str): logger name

    Returns:
        Logger: configured logger
    """

    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger
