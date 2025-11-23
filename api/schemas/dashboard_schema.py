"""
dashboard_schema.py
-------------------
Dashboard aggregated output
"""

from pydantic import BaseModel

class DashboardResponse(BaseModel):
    group_id: str
    transparency_score: float
