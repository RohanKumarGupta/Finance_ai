import random
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from ..auth.utils import get_current_parent
from ..db import get_db
from .schemas import PaymentInitRequest

router = APIRouter()

@router.post("/initiate")
async def initiate_payment(payload: PaymentInitRequest, current = Depends(get_current_parent)):
    db = get_db()
    student = await db.students.find_one({"_id": ObjectId(payload.student_id), "parent_id": current["_id"]})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found or not yours")

    status_choice = payload.simulate or random.choice(["success", "failed"])  # simulate gateway result

    doc = {
        "parent_id": current["_id"],
        "student_id": payload.student_id,
        "amount": float(payload.amount),
        "category": payload.category,
        "status": status_choice,
        "created_at": datetime.utcnow(),
        "receipt_id": str(uuid.uuid4()) if status_choice == "success" else None,
    }
    res = await db.payments.insert_one(doc)
    doc["_id"] = str(res.inserted_id)
    doc["created_at"] = doc["created_at"].isoformat()

    # If payment is successful, update the student's fee breakdown
    if status_choice == "success":
        await update_student_fee_breakdown(db, payload.student_id, payload.category, float(payload.amount))

    return {"payment": doc}

async def update_student_fee_breakdown(db, student_id: str, category: str, payment_amount: float):
    """Update student's fee breakdown by reducing the outstanding amount for the paid category."""
    student = await db.students.find_one({"_id": ObjectId(student_id)})
    if not student or "fee_breakdown" not in student:
        return

    current_fee_breakdown = student["fee_breakdown"]

    # Check if the category exists in fee breakdown
    if category not in current_fee_breakdown:
        return

    # Reduce the outstanding amount for this category
    current_outstanding = float(current_fee_breakdown[category])
    new_outstanding = max(0.0, current_outstanding - payment_amount)

    # Update the fee breakdown
    updated_fee_breakdown = current_fee_breakdown.copy()
    updated_fee_breakdown[category] = new_outstanding

    # Update the student record
    await db.students.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": {"fee_breakdown": updated_fee_breakdown}}
    )

import random
import uuid
import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from ..auth.utils import get_current_parent
from ..db import get_db
from ..ai.services import GeminiService
from .schemas import PaymentInitRequest

router = APIRouter()

@router.post("/initiate")
async def initiate_payment(payload: PaymentInitRequest, current = Depends(get_current_parent)):
    db = get_db()
    student = await db.students.find_one({"_id": ObjectId(payload.student_id), "parent_id": current["_id"]})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found or not yours")

    status_choice = payload.simulate or random.choice(["success", "failed"])  # simulate gateway result

    doc = {
        "parent_id": current["_id"],
        "student_id": payload.student_id,
        "amount": float(payload.amount),
        "category": payload.category,
        "status": status_choice,
        "created_at": datetime.utcnow(),
        "receipt_id": str(uuid.uuid4()) if status_choice == "success" else None,
    }
    res = await db.payments.insert_one(doc)
    doc["_id"] = str(res.inserted_id)
    doc["created_at"] = doc["created_at"].isoformat()

    # If payment is successful, update the student's fee breakdown
    if status_choice == "success":
        await update_student_fee_breakdown(db, payload.student_id, payload.category, float(payload.amount))

    return {"payment": doc}

async def update_student_fee_breakdown(db, student_id: str, category: str, payment_amount: float):
    """Update student's fee breakdown by reducing the outstanding amount for the paid category."""
    student = await db.students.find_one({"_id": ObjectId(student_id)})
    if not student or "fee_breakdown" not in student:
        return

    current_fee_breakdown = student["fee_breakdown"]

    # Check if the category exists in fee breakdown
    if category not in current_fee_breakdown:
        return

    # Reduce the outstanding amount for this category
    current_outstanding = float(current_fee_breakdown[category])
    new_outstanding = max(0.0, current_outstanding - payment_amount)

    # Update the fee breakdown
    updated_fee_breakdown = current_fee_breakdown.copy()
    updated_fee_breakdown[category] = new_outstanding

    # Update the student record
    await db.students.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": {"fee_breakdown": updated_fee_breakdown}}
    )

@router.get("/receipt/{payment_id}")
async def get_receipt(payment_id: str, current = Depends(get_current_parent)):
    db = get_db()
    p = await db.payments.find_one({"_id": ObjectId(payment_id), "parent_id": current["_id"]})
    if not p or p.get("status") != "success":
        raise HTTPException(status_code=404, detail="Receipt not available")
    # Dummy receipt content
    receipt = {
        "receipt_id": p.get("receipt_id"),
        "payment_id": str(p["_id"]),
        "parent_id": p["parent_id"],
        "student_id": p["student_id"],
        "amount": float(p["amount"]),
        "category": p["category"],
        "paid_at": p["created_at"].isoformat() if hasattr(p["created_at"], 'isoformat') else str(p["created_at"]),
    }
    return {"receipt": receipt}

@router.get("/all-receipts")
async def get_all_receipts(current = Depends(get_current_parent)):
    """Get all successful payment receipts for the current parent"""
    db = get_db()

    # Get all successful payments for this parent
    payments = []
    async for payment in db.payments.find(
        {"parent_id": current["_id"], "status": "success"}
    ).sort("created_at", -1):
        # Get student info for each payment
        student = await db.students.find_one({"_id": ObjectId(payment["student_id"])})

        receipt = {
            "receipt_id": payment.get("receipt_id"),
            "payment_id": str(payment["_id"]),
            "student_name": student["name"] if student else "Unknown Student",
            "student_class": student["class_id"] if student else "Unknown",
            "amount": float(payment["amount"]),
            "category": payment["category"],
            "paid_at": payment["created_at"].isoformat() if hasattr(payment["created_at"], 'isoformat') else str(payment["created_at"]),
        }
        payments.append(receipt)

    return {"receipts": payments, "total_count": len(payments)}

@router.post("/summarize-receipts")
async def summarize_receipts(request: dict, current = Depends(get_current_parent)):
    """Generate AI-powered summaries of receipts based on user prompt"""
    prompt = request.get("prompt", "")
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")

    db = get_db()

    # Get all receipts for this parent
    receipts_data = []
    async for payment in db.payments.find(
        {"parent_id": current["_id"], "status": "success"}
    ).sort("created_at", -1):
        # Get student info
        student = await db.students.find_one({"_id": ObjectId(payment["student_id"])})

        receipt_data = {
            "receipt_id": payment.get("receipt_id"),
            "payment_id": str(payment["_id"]),
            "student_name": student["name"] if student else "Unknown Student",
            "student_class": student["class_id"] if student else "Unknown",
            "amount": float(payment["amount"]),
            "category": payment["category"],
            "paid_at": payment["created_at"].isoformat() if hasattr(payment["created_at"], 'isoformat') else str(payment["created_at"]),
        }
        receipts_data.append(receipt_data)

    if not receipts_data:
        return {"summary": "No payment receipts found to summarize."}

    # Prepare data for AI analysis
    receipts_text = json.dumps(receipts_data, indent=2, default=str)

    # Use AI service to generate summary based on prompt
    try:
        ai_service = GeminiService()
        summary = await ai_service.generate_receipt_summary(receipts_text, prompt)
    except RuntimeError:
        summary = "Receipt summarization requires AI service configuration."

    return {"summary": summary, "receipts_count": len(receipts_data)}
