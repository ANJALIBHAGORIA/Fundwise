"""
security.py
-----------
Security helpers: hashing, token generation, signatures.
"""


import hashlib
import hmac
import base64


def sha256_hash(text: str) -> str:
    """Return SHA256 hash for a given string."""
    return hashlib.sha256(text.encode()).hexdigest()


def sign_message(secret: str, message: str) -> str:
    """Return HMAC signature."""
    signature = hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).digest()

    return base64.b64encode(signature).decode()
