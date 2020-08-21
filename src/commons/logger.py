"""Logging bootstrapping"""

import logging

from elasticlogger import Logger
from src.config import CONFIG


LOGGER = Logger(CONFIG["app_name"], level=logging.DEBUG,)


def init_logger():
    """
    Bootstrap logger configuration options
    """

    logging.getLogger("urllib3").setLevel(logging.WARNING)
    LOGGER.logger.propagate = False
