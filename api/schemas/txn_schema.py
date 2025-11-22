from pydantic import BaseModel

class Transaction(BaseModel):
    txn_id: str
    user_id: str
    amount: float
