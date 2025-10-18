from ..db import get_db, connect_to_mongo, close_mongo_connection
from ..auth.utils import hash_password
from datetime import datetime, timedelta

async def reset_and_update_fee_breakdowns():
    """Reset fee breakdowns to original amounts and then apply payment reductions."""
    db = get_db()

    # Original fee structures
    original_fees = {
        "john.doe@example.com": {"tuition": 55000, "hostel": 35000, "transport": 12000, "library": 3000, "activities": 5000, "scholarships": 10000},
        "sarah.smith@example.com": {"tuition": 60000, "hostel": 0, "transport": 15000, "library": 3000, "activities": 4000, "scholarships": 8000},
        "michael.brown@example.com": {"tuition": 50000, "hostel": 32000, "transport": 10000, "library": 3000, "activities": 6000, "scholarships": 12000},
        "emily.wilson@example.com": {"tuition": 58000, "hostel": 0, "transport": 14000, "library": 3000, "activities": 5000, "scholarships": 7000},
        "david.garcia@example.com": {"tuition": 52000, "hostel": 30000, "transport": 11000, "library": 3000, "activities": 4500, "scholarships": 9000},
    }

    # Get parents and students
    parents_data = await db.parents.find({}).to_list(length=100)
    students_data = await db.students.find({}).to_list(length=100)

    # Reset to original amounts
    for parent in parents_data:
        if parent["email"] in original_fees:
            student = await db.students.find_one({"parent_id": str(parent["_id"])})
            if student:
                await db.students.update_one(
                    {"_id": student["_id"]}, 
                    {"$set": {"fee_breakdown": original_fees[parent["email"]]}}
                )

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

    # Parents (password for all: password123)
    parents = [
        {"email": "john.doe@example.com", "full_name": "John Doe", "password_hash": hash_password("password123"), "role": "parent", "phone": "+91-9876543210"},
        {"email": "sarah.smith@example.com", "full_name": "Sarah Smith", "password_hash": hash_password("password123"), "role": "parent", "phone": "+91-9876543211"},
        {"email": "michael.brown@example.com", "full_name": "Michael Brown", "password_hash": hash_password("password123"), "role": "parent", "phone": "+91-9876543212"},
        {"email": "emily.wilson@example.com", "full_name": "Emily Wilson", "password_hash": hash_password("password123"), "role": "parent", "phone": "+91-9876543213"},
        {"email": "david.garcia@example.com", "full_name": "David Garcia", "password_hash": hash_password("password123"), "role": "parent", "phone": "+91-9876543214"},
    ]

    existing = {p["email"] for p in await db.parents.find({}, {"email": 1}).to_list(length=100)}
    for p in parents:
        if p["email"] not in existing:
            await db.parents.insert_one(p)

    # Fetch inserted parents
    p1 = await db.parents.find_one({"email": "john.doe@example.com"})
    p2 = await db.parents.find_one({"email": "sarah.smith@example.com"})
    p3 = await db.parents.find_one({"email": "michael.brown@example.com"})
    p4 = await db.parents.find_one({"email": "emily.wilson@example.com"})
    p5 = await db.parents.find_one({"email": "david.garcia@example.com"})

    # Students with original fee structures
    students = [
        {
            "parent_id": str(p1["_id"]),
            "name": "Alex Doe",
            "class_id": "9-A",
            "roll_number": "9A001",
            "fee_breakdown": {"tuition": 55000, "hostel": 35000, "transport": 12000, "library": 3000, "activities": 5000, "scholarships": 10000},
        },
        {
            "parent_id": str(p2["_id"]),
            "name": "Emma Smith",
            "class_id": "11-B",
            "roll_number": "11B015",
            "fee_breakdown": {"tuition": 60000, "hostel": 0, "transport": 15000, "library": 3000, "activities": 4000, "scholarships": 8000},
        },
        {
            "parent_id": str(p3["_id"]),
            "name": "Olivia Brown",
            "class_id": "7-C",
            "roll_number": "7C022",
            "fee_breakdown": {"tuition": 50000, "hostel": 32000, "transport": 10000, "library": 3000, "activities": 6000, "scholarships": 12000},
        },
        {
            "parent_id": str(p4["_id"]),
            "name": "Liam Wilson",
            "class_id": "10-A",
            "roll_number": "10A008",
            "fee_breakdown": {"tuition": 58000, "hostel": 0, "transport": 14000, "library": 3000, "activities": 5000, "scholarships": 7000},
        },
        {
            "parent_id": str(p5["_id"]),
            "name": "Sophia Garcia",
            "class_id": "8-B",
            "roll_number": "8B012",
            "fee_breakdown": {"tuition": 52000, "hostel": 30000, "transport": 11000, "library": 3000, "activities": 4500, "scholarships": 9000},
        },
    ]

    for s in students:
        exists = await db.students.find_one({"parent_id": s["parent_id"], "name": s["name"]})
        if not exists:
            await db.students.insert_one(s)

    # Update fee breakdowns based on existing payments
    await reset_and_update_fee_breakdowns()

    # Payments (various statuses: success, pending, failed)
    st1 = await db.students.find_one({"parent_id": str(p1["_id"])})
    st2 = await db.students.find_one({"parent_id": str(p2["_id"])})
    st3 = await db.students.find_one({"parent_id": str(p3["_id"])})
    st4 = await db.students.find_one({"parent_id": str(p4["_id"])})
    st5 = await db.students.find_one({"parent_id": str(p5["_id"])})

    payments = [
        # Parent 1 (John Doe) - Alex Doe
        {"parent_id": str(p1["_id"]), "student_id": str(st1["_id"]), "amount": 25000, "category": "tuition", "status": "success", "created_at": datetime.utcnow() - timedelta(days=60), "receipt_id": "RCPT-2024-001", "payment_method": "UPI"},
        {"parent_id": str(p1["_id"]), "student_id": str(st1["_id"]), "amount": 15000, "category": "hostel", "status": "success", "created_at": datetime.utcnow() - timedelta(days=45), "receipt_id": "RCPT-2024-002", "payment_method": "Credit Card"},
        {"parent_id": str(p1["_id"]), "student_id": str(st1["_id"]), "amount": 12000, "category": "transport", "status": "success", "created_at": datetime.utcnow() - timedelta(days=30), "receipt_id": "RCPT-2024-003", "payment_method": "Net Banking"},
        {"parent_id": str(p1["_id"]), "student_id": str(st1["_id"]), "amount": 5000, "category": "activities", "status": "pending", "created_at": datetime.utcnow() - timedelta(days=2)},
        
        # Parent 2 (Sarah Smith) - Emma Smith
        {"parent_id": str(p2["_id"]), "student_id": str(st2["_id"]), "amount": 30000, "category": "tuition", "status": "success", "created_at": datetime.utcnow() - timedelta(days=50), "receipt_id": "RCPT-2024-004", "payment_method": "UPI"},
        {"parent_id": str(p2["_id"]), "student_id": str(st2["_id"]), "amount": 15000, "category": "transport", "status": "success", "created_at": datetime.utcnow() - timedelta(days=35), "receipt_id": "RCPT-2024-005", "payment_method": "Debit Card"},
        {"parent_id": str(p2["_id"]), "student_id": str(st2["_id"]), "amount": 3000, "category": "library", "status": "failed", "created_at": datetime.utcnow() - timedelta(days=10), "failure_reason": "Insufficient funds"},
        
        # Parent 3 (Michael Brown) - Olivia Brown
        {"parent_id": str(p3["_id"]), "student_id": str(st3["_id"]), "amount": 20000, "category": "tuition", "status": "success", "created_at": datetime.utcnow() - timedelta(days=55), "receipt_id": "RCPT-2024-006", "payment_method": "UPI"},
        {"parent_id": str(p3["_id"]), "student_id": str(st3["_id"]), "amount": 32000, "category": "hostel", "status": "success", "created_at": datetime.utcnow() - timedelta(days=40), "receipt_id": "RCPT-2024-007", "payment_method": "Net Banking"},
        {"parent_id": str(p3["_id"]), "student_id": str(st3["_id"]), "amount": 10000, "category": "transport", "status": "success", "created_at": datetime.utcnow() - timedelta(days=25), "receipt_id": "RCPT-2024-008", "payment_method": "Credit Card"},
        
        # Parent 4 (Emily Wilson) - Liam Wilson
        {"parent_id": str(p4["_id"]), "student_id": str(st4["_id"]), "amount": 28000, "category": "tuition", "status": "success", "created_at": datetime.utcnow() - timedelta(days=48), "receipt_id": "RCPT-2024-009", "payment_method": "UPI"},
        {"parent_id": str(p4["_id"]), "student_id": str(st4["_id"]), "amount": 14000, "category": "transport", "status": "pending", "created_at": datetime.utcnow() - timedelta(days=5)},
        {"parent_id": str(p4["_id"]), "student_id": str(st4["_id"]), "amount": 3000, "category": "library", "status": "success", "created_at": datetime.utcnow() - timedelta(days=20), "receipt_id": "RCPT-2024-010", "payment_method": "Debit Card"},
        
        # Parent 5 (David Garcia) - Sophia Garcia
        {"parent_id": str(p5["_id"]), "student_id": str(st5["_id"]), "amount": 26000, "category": "tuition", "status": "success", "created_at": datetime.utcnow() - timedelta(days=52), "receipt_id": "RCPT-2024-011", "payment_method": "Net Banking"},
        {"parent_id": str(p5["_id"]), "student_id": str(st5["_id"]), "amount": 15000, "category": "hostel", "status": "success", "created_at": datetime.utcnow() - timedelta(days=38), "receipt_id": "RCPT-2024-012", "payment_method": "UPI"},
        {"parent_id": str(p5["_id"]), "student_id": str(st5["_id"]), "amount": 11000, "category": "transport", "status": "failed", "created_at": datetime.utcnow() - timedelta(days=8), "failure_reason": "Payment gateway timeout"},
    ]

    for pay in payments:
        dup = await db.payments.find_one({"parent_id": pay["parent_id"], "student_id": pay["student_id"], "amount": pay["amount"], "category": pay["category"]})
        if not dup:
            await db.payments.insert_one(pay)

    # Reminders
    reminders = [
        {"parent_id": str(p1["_id"]), "student_id": str(st1["_id"]), "message": "Remaining tuition fee of ₹30,000 is due by end of month.", "due_date": datetime.utcnow() + timedelta(days=15), "priority": "high", "category": "tuition"},
        {"parent_id": str(p1["_id"]), "student_id": str(st1["_id"]), "message": "Hostel fee payment of ₹20,000 pending.", "due_date": datetime.utcnow() + timedelta(days=20), "priority": "medium", "category": "hostel"},
        {"parent_id": str(p2["_id"]), "student_id": str(st2["_id"]), "message": "Tuition fee balance of ₹30,000 due soon.", "due_date": datetime.utcnow() + timedelta(days=10), "priority": "high", "category": "tuition"},
        {"parent_id": str(p2["_id"]), "student_id": str(st2["_id"]), "message": "Library fee payment failed. Please retry.", "due_date": datetime.utcnow() + timedelta(days=5), "priority": "medium", "category": "library"},
        {"parent_id": str(p3["_id"]), "student_id": str(st3["_id"]), "message": "Activities fee of ₹6,000 is pending.", "due_date": datetime.utcnow() + timedelta(days=25), "priority": "low", "category": "activities"},
        {"parent_id": str(p4["_id"]), "student_id": str(st4["_id"]), "message": "Remaining tuition fee of ₹30,000 due by month end.", "due_date": datetime.utcnow() + timedelta(days=12), "priority": "high", "category": "tuition"},
        {"parent_id": str(p4["_id"]), "student_id": str(st4["_id"]), "message": "Transport fee payment is pending approval.", "due_date": datetime.utcnow() + timedelta(days=8), "priority": "medium", "category": "transport"},
        {"parent_id": str(p5["_id"]), "student_id": str(st5["_id"]), "message": "Tuition fee balance of ₹26,000 due in 2 weeks.", "due_date": datetime.utcnow() + timedelta(days=14), "priority": "high", "category": "tuition"},
        {"parent_id": str(p5["_id"]), "student_id": str(st5["_id"]), "message": "Transport fee payment failed. Please retry payment.", "due_date": datetime.utcnow() + timedelta(days=3), "priority": "high", "category": "transport"},
    ]

    for r in reminders:
        dup = await db.reminders.find_one({"parent_id": r["parent_id"], "student_id": r["student_id"], "message": r["message"]})
        if not dup:
            await db.reminders.insert_one(r)

    print("✅ Successfully seeded database with:")
    print(f"   - {len(parents)} parents")
    print(f"   - {len(students)} students")
    print(f"   - {len(payments)} payments")
    print(f"   - {len(reminders)} reminders")
    print("\n📧 Login credentials (all passwords: password123):")
    for p in parents:
        print(f"   - {p['email']}")
    await close_mongo_connection()
