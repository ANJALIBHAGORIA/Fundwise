"""
anomaly_router.py
-----------------
Provides anomaly scoring for transactions and behavioral signals.
"""

from fastapi import APIRouter
from schemas.txn_schema import TxnRequest, TxnAnomalyResponse

router = APIRouter(prefix="/anomaly", tags=["Anomaly Detection"])

@router.post("/score")
async def score_anomaly(payload: TxnRequest) -> TxnAnomalyResponse:
    return TxnAnomalyResponse(anomaly_score=0.12, flagged=False)
