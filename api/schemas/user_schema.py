from pydantic import BaseModel

class User(BaseModel):
    user_id: str
    name: str
    kyc_id: str | None = None
