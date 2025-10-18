# 🌱 Database Seeding Guide

This guide explains how to seed your Finance AI database with sample data for testing and development.

## 📋 Prerequisites

1. **MongoDB** must be running (local or Atlas)
2. **Environment variables** must be configured in `.env` file
3. **Virtual environment** must be activated

## 🚀 Quick Start

### Option 1: Seed with Existing Data (Recommended)
This will add sample data without deleting existing records:

```bash
python seed_database.py
```

### Option 2: Reset and Seed (⚠️ Destructive)
This will **DELETE ALL** existing data and seed fresh data:

```bash
python seed_database.py --reset
```

## 📊 Sample Data Overview

The seeding script creates the following data:

### 👥 Parents (5 accounts)
All passwords: `password123`

| Email | Full Name | Phone | Students |
|-------|-----------|-------|----------|
| john.doe@example.com | John Doe | +91-9876543210 | Alex Doe (9-A) |
| sarah.smith@example.com | Sarah Smith | +91-9876543211 | Emma Smith (11-B) |
| michael.brown@example.com | Michael Brown | +91-9876543212 | Olivia Brown (7-C) |
| emily.wilson@example.com | Emily Wilson | +91-9876543213 | Liam Wilson (10-A) |
| david.garcia@example.com | David Garcia | +91-9876543214 | Sophia Garcia (8-B) |

### 🎓 Students (5 students)

Each student has a detailed fee breakdown:

| Student | Class | Roll No | Total Fees | Categories |
|---------|-------|---------|------------|------------|
| Alex Doe | 9-A | 9A001 | ₹110,000 | Tuition, Hostel, Transport, Library, Activities, Scholarships |
| Emma Smith | 11-B | 11B015 | ₹94,000 | Tuition, Transport, Library, Activities, Scholarships |
| Olivia Brown | 7-C | 7C022 | ₹113,000 | Tuition, Hostel, Transport, Library, Activities, Scholarships |
| Liam Wilson | 10-A | 10A008 | ₹87,000 | Tuition, Transport, Library, Activities, Scholarships |
| Sophia Garcia | 8-B | 8B012 | ₹109,500 | Tuition, Hostel, Transport, Library, Activities, Scholarships |

### 💳 Payments (16 transactions)

Payment statuses include:
- ✅ **Success** (11 payments) - With receipt IDs
- ⏳ **Pending** (2 payments) - Awaiting confirmation
- ❌ **Failed** (3 payments) - With failure reasons

Payment methods:
- UPI
- Credit Card
- Debit Card
- Net Banking

### 🔔 Reminders (9 reminders)

Reminders with different priorities:
- 🔴 **High Priority** (5 reminders) - Urgent fee payments
- 🟡 **Medium Priority** (3 reminders) - Moderate urgency
- 🟢 **Low Priority** (1 reminder) - Can be paid later

## 📁 Fee Categories

Each student has fees broken down into:

1. **Tuition** - Academic fees (₹50,000 - ₹60,000)
2. **Hostel** - Accommodation fees (₹0 - ₹35,000)
3. **Transport** - Bus/transportation fees (₹10,000 - ₹15,000)
4. **Library** - Library access fees (₹3,000)
5. **Activities** - Extra-curricular activities (₹4,000 - ₹6,000)
6. **Scholarships** - Scholarship deductions (₹7,000 - ₹12,000)

## 🔄 How Fee Calculation Works

The seeding script:

1. **Sets original fee amounts** for each student
2. **Creates payment records** with various statuses
3. **Automatically deducts successful payments** from fee breakdown
4. **Maintains accurate outstanding balances**

Example:
- Original Tuition: ₹55,000
- Successful Payment: ₹25,000
- **Outstanding Balance: ₹30,000**

## 🧪 Testing Scenarios

The sample data supports testing:

### ✅ Successful Payment Flow
- Login as `john.doe@example.com`
- View completed payments with receipt IDs
- Check updated fee balances

### ⏳ Pending Payment Flow
- Login as `emily.wilson@example.com`
- View pending transport fee payment
- Test payment confirmation

### ❌ Failed Payment Flow
- Login as `sarah.smith@example.com`
- View failed library fee payment
- Test payment retry functionality

### 🔔 Reminder System
- All accounts have multiple reminders
- Different priority levels
- Various due dates

## 🛠️ Customizing Seed Data

To modify the seed data, edit:
```
backend/app/seed/seed_data.py
```

Key sections to customize:
- `parents` list (line 59-65)
- `students` list (line 80-116)
- `payments` list (line 133-159)
- `reminders` list (line 167-177)

## 🔍 Verifying Seeded Data

After seeding, you can verify the data:

### Using MongoDB Compass
1. Connect to your MongoDB instance
2. Select `finance_db` database
3. Browse collections: `parents`, `students`, `payments`, `reminders`

### Using MongoDB Shell
```bash
mongosh
use finance_db
db.parents.countDocuments()
db.students.countDocuments()
db.payments.countDocuments()
db.reminders.countDocuments()
```

### Using the API
1. Start the backend: `python run.py`
2. Login with any parent account
3. Check dashboard endpoint: `GET /dashboard`

## ⚠️ Important Notes

1. **Idempotent Seeding**: Running the script multiple times won't create duplicates
2. **Password Security**: All test accounts use `password123` - change in production!
3. **Reset Option**: Use `--reset` flag carefully - it deletes ALL data
4. **Fee Consistency**: The script ensures fee balances are accurate after payments

## 🐛 Troubleshooting

### Error: "Mongo client not initialized"
- Ensure MongoDB is running
- Check `.env` file has correct `MONGODB_URI`

### Error: "Field required [type=missing]"
- Add required environment variables to `.env`:
  ```
  MONGODB_URI=mongodb://localhost:27017
  JWT_SECRET=your-secret-key-here
  ```

### Error: "Connection refused"
- Start MongoDB service
- Verify connection string in `.env`

### Duplicate Key Error
- The script checks for duplicates
- If error persists, use `--reset` flag

## 📞 Support

For issues or questions:
1. Check MongoDB connection
2. Verify environment variables
3. Review error logs
4. Check database permissions

---

**Happy Testing! 🚀**
