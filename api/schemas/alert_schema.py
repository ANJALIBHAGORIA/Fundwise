"""
alert_schema.py
----------------
Models for alerting engine
"""

from pydantic import BaseModel
from typing import List

class AlertRequest(BaseModel):
    user_id: str
    event: str
    metadata: dict

class AlertResponse(BaseModel):
    status: str
    alerts: List[str]
