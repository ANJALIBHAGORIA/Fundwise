"""
validators.py
--------------
Utility validation functions for PAN, Aadhaar, Email and generic patterns.
"""

import re


# --- Pre-compiled regex patterns for performance ---
PAN_REGEX = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]$")
AADHAAR_REGEX = re.compile(r"^[2-9][0-9]{11}$")  # Aadhaar cannot start with 0 or 1
EMAIL_REGEX = re.compile(
    r"^(?=.{6,254}$)([a-zA-Z0-9_.+-]+)@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)$"
)


def is_valid_pan(pan: str) -> bool:
    """
    Validate Indian PAN.
    Format Example: ABCDE1234F

    Rules:
    - 5 letters + 4 digits + 1 letter
    - Case-insensitive but normalized to uppercase
    """
    if not pan:
        return False

    pan = pan.strip().upper()
    return bool(PAN_REGEX.match(pan))


def is_valid_aadhaar(aadhaar: str) -> bool:
    """
    Validate Indian Aadhaar number.

    Rules:
    - Exactly 12 digits
    - Cannot start with 0 or 1
    """
    if not aadhaar:
        return False

    aadhaar = aadhaar.strip()
    return bool(AADHAAR_REGEX.match(aadhaar))


def is_valid_email(email: str) -> bool:
    """
    Validate email address.

    Enforces:
    - 6 to 254 characters (RFC constraint)
    - Valid username + domain + TLD
    """
    if not email:
        return False

    email = email.strip()
    return bool(EMAIL_REGEX.match(email))


def matches_pattern(value: str, pattern: str) -> bool:
    """
    Generic pattern matcher for custom validations.
    """
    if not value:
        return False
    return bool(re.match(pattern, value))
