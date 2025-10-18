from pydantic import BaseModel
from datetime import datetime

class ReminderCreate(BaseModel):
    student_id: str
    message: str
    due_date: datetime
