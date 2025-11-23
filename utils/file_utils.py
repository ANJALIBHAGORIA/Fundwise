"""
file_utils.py
--------------
Utility functions for reading/writing files safely.
"""


import json
from typing import Any


def read_json(path: str) -> Any:
    """
    Load JSON file from disk.

    Args:
        path (str): file path

    Returns:
        Any: JSON data
    """
    with open(path, "r") as f:
        return json.load(f)


def write_json(path: str, data: Any):
    """
    Write JSON data to a file.

    Args:
        path (str): output file path
        data (Any): JSON-serializable data
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
