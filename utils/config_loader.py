"""
config_loader.py
-----------------
Loads configuration from .env, ini, or environment variables.
"""


import os
import configparser
from utils.common_exceptions import ConfigError


def load_ini(path: str) -> dict:
    """
    Load an INI configuration file.

    Args:
        path (str): path to .ini file

    Returns:
        dict: parsed config

    Raises:
        ConfigError: if file not found or invalid
    """

    if not os.path.exists(path):
        raise ConfigError(f"Config file not found: {path}")

    parser = configparser.ConfigParser()
    parser.read(path)

    return {section: dict(parser.items(section)) for section in parser.sections()}
