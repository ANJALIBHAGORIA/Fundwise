"""
helpers.py
-----------
General helper functions used across modules.
"""


from datetime import datetime, timezone
import uuid


def now_iso() -> str:
    """
    Returns current timestamp in ISO 8601 format.

    Returns:
        str: ISO timestamp
    """
    return datetime.now(timezone.utc).isoformat()


def generate_id(prefix: str = "") -> str:
    """
    Generate a unique ID with optional prefix.

    Example:
        generate_id("txn_") -> "txn_af93be823a..."

    """
    return f"{prefix}{uuid.uuid4().hex}"
