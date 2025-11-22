import logging
def get_logger(name=__name__):
    logger = logging.getLogger(name)
    if not logger.handlers:
        ch = logging.StreamHandler()
        logger.addHandler(ch)
    return logger
