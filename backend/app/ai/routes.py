from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
from ..auth.utils import get_current_parent
from ..db import get_db
from .services import GeminiService

router = APIRouter()

class DocPayload(BaseModel):
    text: str

@router.post("/summarize")
async def summarize(
    current = Depends(get_current_parent),
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    if not text and not file:
        raise HTTPException(status_code=400, detail="Either text or file must be provided")
    
    try:
        service = GeminiService()
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    if file:
        # Handle file upload
        summary = await service.summarize_file(file)
    else:
        # Handle text input
        summary = await service.summarize_document(text)
    
    return {"summary": summary}

@router.get("/advice")
async def advice(current = Depends(get_current_parent)):
    db = get_db()
    student = await db.students.find_one({"parent_id": current["_id"]})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    breakdown = student.get("fee_breakdown", {})
    history = []
    async for p in db.payments.find({"parent_id": current["_id"], "student_id": str(student["_id"]) }).sort("created_at", -1):
        history.append({"amount": float(p.get("amount", 0)), "category": p.get("category"), "status": p.get("status"), "created_at": p.get("created_at").isoformat() if hasattr(p.get("created_at"), 'isoformat') else str(p.get("created_at"))})
    try:
        service = GeminiService()
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    text = await service.financial_advice(student.get("name", "Student"), breakdown, history)
    return {"advice": text}
