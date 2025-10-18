from pydantic import BaseModel
from typing import Optional, Literal

class PaymentInitRequest(BaseModel):
    student_id: str
    amount: float
    category: str
    simulate: Optional[Literal["success", "failed"]] = None
