"""
user_schema.py
----------------
User & KYC request/response models
"""

from pydantic import BaseModel
from typing import List

class UserKYCRequest(BaseModel):
    user_id: str
    document_type: str
    document_image_b64: str

class UserKYCResponse(BaseModel):
    status: str
    reasons: List[str]
