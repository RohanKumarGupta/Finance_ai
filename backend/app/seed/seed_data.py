from ..db import get_db, connect_to_mongo, close_mongo_connection
from ..auth.utils import hash_password
from datetime import datetime, timedelta

async def reset_and_update_fee_breakdowns():
    """Reset fee breakdowns to original amounts and then apply payment reductions."""
    db = get_db()

    # Original fee structures
    original_fees = {
        "parent1@example.com": {"tuition": 50000, "hostel": 30000, "transport": 10000, "scholarships": 8000},
        "parent2@example.com": {"tuition": 60000, "hostel": 0, "transport": 12000, "scholarships": 5000},
    }

    # Get parents and students
    p1 = await db.parents.find_one({"email": "parent1@example.com"})
    p2 = await db.parents.find_one({"email": "parent2@example.com"})
    st1 = await db.students.find_one({"parent_id": str(p1["_id"])})
    st2 = await db.students.find_one({"parent_id": str(p2["_id"])})

    # Reset to original amounts
    await db.students.update_one({"_id": st1["_id"]}, {"$set": {"fee_breakdown": original_fees["parent1@example.com"]}})
    await db.students.update_one({"_id": st2["_id"]}, {"$set": {"fee_breakdown": original_fees["parent2@example.com"]}})

    # Get all successful payments and apply reductions
    async for payment in db.payments.find({"status": "success"}):
        student_id = payment["student_id"]
        category = payment["category"]
        amount = float(payment["amount"])

        # Update the corresponding student's fee breakdown
        student = await db.students.find_one({"_id": student_id})
        if student and "fee_breakdown" in student:
            current_fee_breakdown = student["fee_breakdown"]
            if category in current_fee_breakdown:
                current_outstanding = float(current_fee_breakdown[category])
                new_outstanding = max(0.0, current_outstanding - amount)

                updated_fee_breakdown = current_fee_breakdown.copy()
                updated_fee_breakdown[category] = new_outstanding

                await db.students.update_one(
                    {"_id": student_id},
                    {"$set": {"fee_breakdown": updated_fee_breakdown}}
                )

async def run_seed():
    await connect_to_mongo()
    db = get_db()

    # Parents
    parents = [
        {"email": "parent1@example.com", "full_name": "Alex Martin", "password_hash": hash_password("password123"), "role": "parent"},
        {"email": "parent2@example.com", "full_name": "Sam Lee", "password_hash": hash_password("password123"), "role": "parent"},
    ]

    existing = {p["email"] for p in await db.parents.find({}, {"email": 1}).to_list(length=100)}
    for p in parents:
        if p["email"] not in existing:
            await db.parents.insert_one(p)

    # Fetch inserted parents
    p1 = await db.parents.find_one({"email": "parent1@example.com"})
    p2 = await db.parents.find_one({"email": "parent2@example.com"})

    # Students with original fee structures
    students = [
        {
            "parent_id": str(p1["_id"]),
            "name": "Jamie Martin",
            "class_id": "8-A",
            "fee_breakdown": {"tuition": 50000, "hostel": 30000, "transport": 10000, "scholarships": 8000},
        },
        {
            "parent_id": str(p2["_id"]),
            "name": "Chris Lee",
            "class_id": "10-B",
            "fee_breakdown": {"tuition": 60000, "hostel": 0, "transport": 12000, "scholarships": 5000},
        },
    ]

    for s in students:
        exists = await db.students.find_one({"parent_id": s["parent_id"], "name": s["name"]})
        if not exists:
            await db.students.insert_one(s)

    # Update fee breakdowns based on existing payments
    await reset_and_update_fee_breakdowns()

    # Payments (some success, some pending/failed)
    st1 = await db.students.find_one({"parent_id": str(p1["_id"])})
    st2 = await db.students.find_one({"parent_id": str(p2["_id"])})

    payments = [
        {"parent_id": str(p1["_id"]), "student_id": str(st1["_id"]), "amount": 20000, "category": "tuition", "status": "success", "created_at": datetime.utcnow() - timedelta(days=30), "receipt_id": "rcpt-1"},
        {"parent_id": str(p1["_id"]), "student_id": str(st1["_id"]), "amount": 10000, "category": "transport", "status": "failed", "created_at": datetime.utcnow() - timedelta(days=10)},
        {"parent_id": str(p2["_id"]), "student_id": str(st2["_id"]), "amount": 15000, "category": "tuition", "status": "success", "created_at": datetime.utcnow() - timedelta(days=5), "receipt_id": "rcpt-2"},
    ]

    for pay in payments:
        dup = await db.payments.find_one({"parent_id": pay["parent_id"], "student_id": pay["student_id"], "amount": pay["amount"], "category": pay["category"]})
        if not dup:
            await db.payments.insert_one(pay)

    # Reminders
    reminders = [
        {"parent_id": str(p1["_id"]), "student_id": str(st1["_id"]), "message": "Pay remaining tuition before due date.", "due_date": datetime.utcnow() + timedelta(days=15)},
        {"parent_id": str(p2["_id"]), "student_id": str(st2["_id"]), "message": "Transport fee due next week.", "due_date": datetime.utcnow() + timedelta(days=7)},
    ]

    for r in reminders:
        dup = await db.reminders.find_one({"parent_id": r["parent_id"], "student_id": r["student_id"], "message": r["message"]})
        if not dup:
            await db.reminders.insert_one(r)

    print("Seeded parents, students, payments, reminders.")
    await close_mongo_connection()
