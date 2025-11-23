"""
auth.py
-------
JWT authentication + RBAC utilities
"""

from datetime import datetime, timedelta
from jose import jwt

class AuthService:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def create_token(self, user_id: str):
        payload = {"sub": user_id, "exp": datetime.utcnow() + timedelta(hours=12)}
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def verify_token(self, token: str):
        return jwt.decode(token, self.secret_key, algorithms=["HS256"])
