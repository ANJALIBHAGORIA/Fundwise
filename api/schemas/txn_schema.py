"""
txn_schema.py
--------------
Transaction input + anomaly score schema
"""

from pydantic import BaseModel

class TxnRequest(BaseModel):
    txn_id: str
    user_id: str
    amount: float
    channel: str
    timestamp: str

class TxnAnomalyResponse(BaseModel):
    anomaly_score: float
    flagged: bool
