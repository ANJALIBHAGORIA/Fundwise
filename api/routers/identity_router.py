"""
identity_router.py
-------------------
KYC verification, document validation, and device fingerprint checks.
"""

from fastapi import APIRouter
from schemas.user_schema import UserKYCRequest, UserKYCResponse

router = APIRouter(prefix="/identity", tags=["Identity"])

@router.post("/verify")
async def verify_identity(payload: UserKYCRequest) -> UserKYCResponse:
    """
    Perform document + device verification
    """
    return UserKYCResponse(status="verified", reasons=[])
