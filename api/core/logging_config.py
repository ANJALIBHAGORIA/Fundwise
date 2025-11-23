"""
logging_config.py
-----------------
Structured JSON logging
"""

import logging
import json

def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter('%(message)s')
    )

    logger.addHandler(handler)
    return logger
