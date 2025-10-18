from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from ..auth.utils import get_current_parent
from ..db import get_db
from .schemas import ReminderCreate

router = APIRouter()

@router.post("/")
async def create_reminder(payload: ReminderCreate, current = Depends(get_current_parent)):
    db = get_db()
    student = await db.students.find_one({"_id": ObjectId(payload.student_id), "parent_id": current["_id"]})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found or not yours")
    doc = {
        "parent_id": current["_id"],
        "student_id": payload.student_id,
        "message": payload.message,
        "due_date": payload.due_date,
    }
    res = await db.reminders.insert_one(doc)
    doc["_id"] = str(res.inserted_id)
    return {"reminder": doc}

@router.get("/")
async def list_reminders(current = Depends(get_current_parent)):
    db = get_db()
    items = []
    async for r in db.reminders.find({"parent_id": current["_id"]}).sort("due_date", 1):
        r["_id"] = str(r["_id"])
        items.append(r)
    return {"reminders": items}
