from pydantic import BaseModel

class Score(BaseModel):
    user_id: str
    score: float
