from pydantic import BaseModel

class Alert(BaseModel):
    user_id: str
    message: str
