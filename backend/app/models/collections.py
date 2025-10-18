from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# Pydantic schemas
class ParentBase(BaseModel):
    email: EmailStr
    full_name: str
    role: Literal["parent"] = "parent"

class ParentCreate(ParentBase):
    password: str

class ParentOut(ParentBase):
    id: str = Field(alias="_id")

class Student(BaseModel):
    parent_id: str
    name: str
    class_id: str
    fee_breakdown: dict  # {tuition, hostel, transport, scholarships}

class Payment(BaseModel):
    parent_id: str
    student_id: str
    amount: float
    category: str  # tuition/hostel/transport/etc
    status: Literal["success", "failed", "pending"] = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    receipt_id: Optional[str] = None

class Reminder(BaseModel):
    parent_id: str
    student_id: str
    message: str
    due_date: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Helpers to coerce ObjectId <-> str when needed will be in route layers.
