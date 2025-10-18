# 📋 Seed Data Quick Reference

## 🔐 Login Credentials

**Password for all accounts:** `password123`

### Parent Accounts

| # | Email | Name | Student | Class | Key Features |
|---|-------|------|---------|-------|--------------|
| 1 | john.doe@example.com | John Doe | Alex Doe | 9-A | Has hostel, 3 successful payments, 1 pending |
| 2 | sarah.smith@example.com | Sarah Smith | Emma Smith | 11-B | No hostel, 2 successful, 1 failed payment |
| 3 | michael.brown@example.com | Michael Brown | Olivia Brown | 7-C | Has hostel, all 3 payments successful |
| 4 | emily.wilson@example.com | Emily Wilson | Liam Wilson | 10-A | No hostel, 2 successful, 1 pending |
| 5 | david.garcia@example.com | David Garcia | Sophia Garcia | 8-B | Has hostel, 2 successful, 1 failed |

---

## 💰 Fee Breakdown by Student

### Alex Doe (9-A) - John Doe's Child
```
Original Fees:
├─ Tuition:      ₹55,000
├─ Hostel:       ₹35,000
├─ Transport:    ₹12,000
├─ Library:      ₹3,000
├─ Activities:   ₹5,000
└─ Scholarships: -₹10,000
   TOTAL:        ₹100,000

Payments Made:
├─ Tuition:      ₹25,000 ✅ (RCPT-2024-001)
├─ Hostel:       ₹15,000 ✅ (RCPT-2024-002)
├─ Transport:    ₹12,000 ✅ (RCPT-2024-003)
└─ Activities:   ₹5,000  ⏳ (Pending)

Outstanding:
├─ Tuition:      ₹30,000
├─ Hostel:       ₹20,000
└─ Activities:   ₹5,000 (if pending fails)
```

### Emma Smith (11-B) - Sarah Smith's Child
```
Original Fees:
├─ Tuition:      ₹60,000
├─ Transport:    ₹15,000
├─ Library:      ₹3,000
├─ Activities:   ₹4,000
└─ Scholarships: -₹8,000
   TOTAL:        ₹74,000

Payments Made:
├─ Tuition:      ₹30,000 ✅ (RCPT-2024-004)
├─ Transport:    ₹15,000 ✅ (RCPT-2024-005)
└─ Library:      ₹3,000  ❌ (Failed - Insufficient funds)

Outstanding:
├─ Tuition:      ₹30,000
├─ Library:      ₹3,000
└─ Activities:   ₹4,000
```

### Olivia Brown (7-C) - Michael Brown's Child
```
Original Fees:
├─ Tuition:      ₹50,000
├─ Hostel:       ₹32,000
├─ Transport:    ₹10,000
├─ Library:      ₹3,000
├─ Activities:   ₹6,000
└─ Scholarships: -₹12,000
   TOTAL:        ₹89,000

Payments Made:
├─ Tuition:      ₹20,000 ✅ (RCPT-2024-006)
├─ Hostel:       ₹32,000 ✅ (RCPT-2024-007)
└─ Transport:    ₹10,000 ✅ (RCPT-2024-008)

Outstanding:
├─ Tuition:      ₹30,000
├─ Library:      ₹3,000
└─ Activities:   ₹6,000
```

### Liam Wilson (10-A) - Emily Wilson's Child
```
Original Fees:
├─ Tuition:      ₹58,000
├─ Transport:    ₹14,000
├─ Library:      ₹3,000
├─ Activities:   ₹5,000
└─ Scholarships: -₹7,000
   TOTAL:        ₹73,000

Payments Made:
├─ Tuition:      ₹28,000 ✅ (RCPT-2024-009)
├─ Transport:    ₹14,000 ⏳ (Pending)
└─ Library:      ₹3,000  ✅ (RCPT-2024-010)

Outstanding:
├─ Tuition:      ₹30,000
├─ Transport:    ₹14,000 (if pending fails)
└─ Activities:   ₹5,000
```

### Sophia Garcia (8-B) - David Garcia's Child
```
Original Fees:
├─ Tuition:      ₹52,000
├─ Hostel:       ₹30,000
├─ Transport:    ₹11,000
├─ Library:      ₹3,000
├─ Activities:   ₹4,500
└─ Scholarships: -₹9,000
   TOTAL:        ₹91,500

Payments Made:
├─ Tuition:      ₹26,000 ✅ (RCPT-2024-011)
├─ Hostel:       ₹15,000 ✅ (RCPT-2024-012)
└─ Transport:    ₹11,000 ❌ (Failed - Gateway timeout)

Outstanding:
├─ Tuition:      ₹26,000
├─ Hostel:       ₹15,000
├─ Transport:    ₹11,000
├─ Library:      ₹3,000
└─ Activities:   ₹4,500
```

---

## 📊 Payment Statistics

### By Status
- ✅ **Successful:** 11 payments (₹2,53,000)
- ⏳ **Pending:** 2 payments (₹19,000)
- ❌ **Failed:** 3 payments (₹19,000)

### By Category
- **Tuition:** 5 payments (₹1,29,000)
- **Hostel:** 3 payments (₹62,000)
- **Transport:** 5 payments (₹52,000)
- **Library:** 2 payments (₹6,000)
- **Activities:** 1 payment (₹5,000)

### By Payment Method
- **UPI:** 6 payments
- **Net Banking:** 4 payments
- **Credit Card:** 2 payments
- **Debit Card:** 2 payments

---

## 🔔 Active Reminders

### High Priority (🔴)
1. **John Doe** - Tuition ₹30,000 due in 15 days
2. **Sarah Smith** - Tuition ₹30,000 due in 10 days
3. **Emily Wilson** - Tuition ₹30,000 due in 12 days
4. **David Garcia** - Tuition ₹26,000 due in 14 days
5. **David Garcia** - Transport payment failed, retry in 3 days

### Medium Priority (🟡)
1. **John Doe** - Hostel ₹20,000 due in 20 days
2. **Sarah Smith** - Library payment failed, retry in 5 days
3. **Emily Wilson** - Transport pending approval (8 days)

### Low Priority (🟢)
1. **Michael Brown** - Activities ₹6,000 due in 25 days

---

## 🧪 Test Scenarios

### Scenario 1: View Successful Payments
```
Login: john.doe@example.com
Expected: 3 successful payments with receipt IDs
Total Paid: ₹52,000
```

### Scenario 2: Handle Failed Payment
```
Login: sarah.smith@example.com
Expected: 1 failed library payment
Reason: Insufficient funds
Action: Retry payment
```

### Scenario 3: Track Pending Payment
```
Login: emily.wilson@example.com
Expected: 1 pending transport payment
Amount: ₹14,000
Action: Check status/confirm
```

### Scenario 4: Multiple Reminders
```
Login: david.garcia@example.com
Expected: 2 high-priority reminders
- Tuition balance
- Failed transport payment
```

### Scenario 5: Complete Payment History
```
Login: michael.brown@example.com
Expected: All 3 payments successful
No pending/failed payments
```

---

## 🎯 Quick Commands

### Seed Database
```bash
python seed_database.py
```

### Reset and Seed
```bash
python seed_database.py --reset
```

### Check Data in MongoDB
```bash
mongosh
use finance_db
db.parents.find().pretty()
db.students.find().pretty()
db.payments.find().pretty()
db.reminders.find().pretty()
```

### Start Backend
```bash
python run.py
```

---

## 📱 API Testing

### Login
```bash
POST http://localhost:8000/auth/login
{
  "email": "john.doe@example.com",
  "password": "password123"
}
```

### Get Dashboard
```bash
GET http://localhost:8000/dashboard
Headers: Authorization: Bearer <token>
```

### Get Payments
```bash
GET http://localhost:8000/payments
Headers: Authorization: Bearer <token>
```

### Get Reminders
```bash
GET http://localhost:8000/reminders
Headers: Authorization: Bearer <token>
```

---

**Last Updated:** 2024
**Version:** 1.0
