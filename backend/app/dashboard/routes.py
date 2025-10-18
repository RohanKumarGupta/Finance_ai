from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from ..auth.utils import get_current_parent
from ..db import get_db

router = APIRouter()

@router.get("/fee-breakdown")
async def fee_breakdown(current = Depends(get_current_parent)):
    db = get_db()
    student = await db.students.find_one({"parent_id": current["_id"]})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"student_id": str(student["_id"]), "name": student["name"], "class_id": student["class_id"], "fee_breakdown": student.get("fee_breakdown", {})}

@router.get("/payment-history")
async def payment_history(current = Depends(get_current_parent)):
    db = get_db()
    cursor = db.payments.find({"parent_id": current["_id"]}).sort("created_at", -1)
    items = []
    async for p in cursor:
        p["_id"] = str(p["_id"])
        p["created_at"] = p["created_at"].isoformat()
        items.append(p)
    return {"payments": items}

@router.get("/upcoming-dues")
async def upcoming_dues(current = Depends(get_current_parent)):
    # For demo: dues are now calculated from the current fee_breakdown in student record
    # (which is already reduced by successful payments)
    db = get_db()
    student = await db.students.find_one({"parent_id": current["_id"]})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    breakdown = student.get("fee_breakdown", {})
    dues = {}

    for k, v in breakdown.items():
        if k == "scholarships":
            continue
        # Since fee_breakdown already reflects outstanding amounts after successful payments,
        # we can use it directly as dues
        due = max(0.0, float(v))
        dues[k] = due

    # Apply scholarships reduction if present
    scholarship = float(breakdown.get("scholarships", 0.0) or 0.0)
    total_due = max(0.0, sum(dues.values()) - scholarship)

    return {"dues_by_category": dues, "scholarships": scholarship, "total_due": total_due}
