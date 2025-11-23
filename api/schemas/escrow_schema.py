"""
escrow_schema.py
----------------
Models for escrow evaluation
"""

from pydantic import BaseModel

class EscrowRequest(BaseModel):
    txn_id: str
    sender: str
    receiver: str
    amount: float

class EscrowResponse(BaseModel):
    status: str
    reason: str
