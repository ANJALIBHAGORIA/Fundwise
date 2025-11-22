from pydantic import BaseModel

class GroupOverview(BaseModel):
    group_id: str
    goal_amount: float
