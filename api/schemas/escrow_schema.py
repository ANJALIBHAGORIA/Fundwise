from pydantic import BaseModel

class Escrow(BaseModel):
    escrow_id: str
    status: str
