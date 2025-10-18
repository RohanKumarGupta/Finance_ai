# Financial Transparency & Payment Management AI Assistant

A full-stack web application for parents to manage student finances with AI-powered insights.

## 🚀 Features

### Backend (FastAPI)
- **JWT Authentication**: Secure parent login with role-based authorization
- **MongoDB Integration**: Motor async driver with MongoDB Compass support
- **AI-Powered**: LangChain + Gemini for document parsing and financial advice
- **Payment System**: Dummy transaction simulation with receipt generation
- **Dashboard APIs**: Fee breakdown, payment history, upcoming dues
- **Reminders**: Create and manage payment reminders

### Frontend (React + Vite)
- **Modern UI**: Tailwind CSS with responsive design
- **Authentication**: JWT-based login/signup with protected routes
- **Dashboard**: Visual fee breakdown, payment history, upcoming dues
- **Payments**: Initiate dummy payments and view receipts
- **AI Assistant**: Document summarization and personalized financial advice
- **Reminders**: Create and track payment reminders

## 📋 Prerequisites

- Python 3.10+
- Node.js 18+
- MongoDB (local or Atlas)
- Gemini API Key

## 🛠️ Setup Instructions

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
copy .env.example .env

# Edit .env and add your credentials:
# - MONGODB_URI (from MongoDB Compass)
# - GEMINI_API_KEY (from Google AI Studio)
# - JWT_SECRET (any random string)

# Seed dummy data
python run.py seed

# Start backend server
python run.py serve
```

Backend will run at: http://127.0.0.1:8000

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run at: http://localhost:3000

## 🔑 Demo Credentials

After seeding, use these credentials to login:

- **Email**: `parent1@example.com`
- **Password**: `password123`

OR

- **Email**: `parent2@example.com`
- **Password**: `password123`

## 📁 Project Structure

```
finance/
├── backend/
│   ├── app/
│   │   ├── auth/          # JWT authentication
│   │   ├── dashboard/     # Dashboard APIs
│   │   ├── payments/      # Payment simulation
│   │   ├── ai/            # LangChain + Gemini
│   │   ├── reminders/     # Reminder management
│   │   ├── models/        # Pydantic schemas
│   │   ├── seed/          # Seed data script
│   │   ├── config.py      # Settings
│   │   ├── db.py          # MongoDB connection
│   │   └── main.py        # FastAPI app
│   ├── requirements.txt
│   ├── run.py
│   └── .env.example
│
└── frontend/
    ├── src/
    │   ├── components/    # Reusable components
    │   ├── context/       # Auth context
    │   ├── pages/         # Page components
    │   ├── utils/         # API client
    │   ├── App.jsx
    │   └── main.jsx
    ├── package.json
    ├── vite.config.js
    └── tailwind.config.js
```

## 🔌 API Endpoints

### Authentication
- `POST /auth/signup` - Create parent account
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info

### Dashboard
- `GET /dashboard/fee-breakdown` - Get student fee details
- `GET /dashboard/payment-history` - Get payment history
- `GET /dashboard/upcoming-dues` - Calculate upcoming dues

### Payments
- `POST /payments/initiate` - Initiate dummy payment
- `GET /payments/receipt/{payment_id}` - Get payment receipt

### AI Assistant
- `POST /ai/summarize` - Summarize financial document
- `GET /ai/advice` - Get personalized financial advice

### Reminders
- `POST /reminders/` - Create payment reminder
- `GET /reminders/` - List all reminders

## 🎨 Frontend Pages

- **Login/Signup**: Authentication pages
- **Dashboard**: Overview with fee breakdown, payment history, upcoming dues
- **Payments**: Initiate payments and view receipts
- **AI Assistant**: Document summarizer and financial advice
- **Reminders**: Create and manage payment reminders

## 🗄️ MongoDB Collections

### parents
```json
{
  "_id": "ObjectId",
  "email": "string",
  "full_name": "string",
  "password_hash": "string",
  "role": "parent"
}
```

### students
```json
{
  "_id": "ObjectId",
  "parent_id": "string",
  "name": "string",
  "class_id": "string",
  "fee_breakdown": {
    "tuition": "number",
    "hostel": "number",
    "transport": "number",
    "scholarships": "number"
  }
}
```

### payments
```json
{
  "_id": "ObjectId",
  "parent_id": "string",
  "student_id": "string",
  "amount": "number",
  "category": "string",
  "status": "success|failed|pending",
  "created_at": "datetime",
  "receipt_id": "string|null"
}
```

### reminders
```json
{
  "_id": "ObjectId",
  "parent_id": "string",
  "student_id": "string",
  "message": "string",
  "due_date": "datetime",
  "created_at": "datetime"
}
```

## 🤖 AI Features

### Document Summarizer
- Paste any financial document (invoice, receipt, etc.)
- AI extracts key information: fees, due dates, scholarships
- Powered by Gemini via LangChain

### Financial Advice
- Analyzes student's fee breakdown and payment history
- Provides personalized planning recommendations
- Suggests optimization opportunities

## 🔒 Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- Role-based authorization (parent role only)
- Protected API routes
- CORS enabled for frontend

## 💳 Payment System

The payment system is **fully simulated** for demo purposes:
- No real payment gateway integration
- Transactions are stored in MongoDB only
- Can simulate success/failure for testing
- Generates dummy receipt IDs

## 🚀 Production Deployment

### Render Deployment (Recommended)

This project is configured for easy deployment on [Render](https://render.com).

#### 1. Deploy Backend to Render

1. **Connect your GitHub repository** to Render
2. **Create a new Web Service**:
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. **Add Environment Variables** in Render dashboard:
   ```env
   MONGODB_URI=<your-mongodb-atlas-connection-string>
   DATABASE_NAME=finance_db
   JWT_SECRET=<generate-a-secure-random-string>
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   GEMINI_API_KEY=<your-gemini-api-key>
   ```
4. **Deploy** - Render will automatically build and deploy your backend

#### 2. Deploy Frontend to Render

1. **Create another Web Service** for the frontend:
   - **Runtime**: `Node.js`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm start`
2. **Add Environment Variables**:
   ```env
   REACT_APP_API_URL=https://your-backend-service-name.onrender.com
   ```
3. **Deploy** - Render will build and serve your React app

#### 3. Alternative: Deploy with render.yaml

If you prefer using Render's blueprint system:

1. **Create a `render.yaml` file** (already included in this repo)
2. **Push to GitHub** and connect to Render
3. **Deploy** - Render will use the blueprint configuration

#### 4. Database Setup

For production, use **MongoDB Atlas**:

1. Create a MongoDB Atlas cluster
2. Get your connection string from Atlas dashboard
3. Add it as `MONGODB_URI` environment variable in Render

#### 5. Domain Configuration

1. **Add Custom Domain** in Render dashboard (optional)
2. **Configure SSL** - Render provides free SSL certificates

### Manual Deployment

#### Backend
1. Set environment variables in production
2. Use a production WSGI server (e.g., Gunicorn)
3. Enable HTTPS
4. Restrict CORS origins
5. Use strong JWT secret

#### Frontend
1. Build for production: `npm run build`
2. Deploy `dist/` folder to static hosting (Vercel, Netlify, etc.)
3. Update API proxy configuration for production backend URL

## 📝 Environment Variables

### Backend (.env)
```env
MONGODB_URI=mongodb+srv://user:pass@cluster/db
DATABASE_NAME=finance_db
JWT_SECRET=your-super-secret-key-change-this
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
GEMINI_API_KEY=your-gemini-api-key
```

### Frontend (.env - for production deployment)
```env
VITE_API_URL=https://your-backend-service.onrender.com
```

## 🧪 Testing the Application

1. **Login**: Use demo credentials
2. **View Dashboard**: See fee breakdown and payment history
3. **Make Payment**: Initiate a dummy payment (try both success/failure)
4. **View Receipt**: Check receipt for successful payments
5. **AI Summarizer**: Paste a sample invoice and get summary
6. **AI Advice**: Get personalized financial planning advice
7. **Create Reminder**: Add a payment reminder with due date

## 🛠️ Tech Stack

### Backend
- FastAPI 0.115.0
- Motor (MongoDB async driver)
- Pydantic for validation
- python-jose for JWT
- passlib for password hashing
- LangChain + langchain-google-genai
- Google Generative AI (Gemini)

### Frontend
- React 18
- Vite 5
- React Router v6
- Tailwind CSS 3
- Lucide React (icons)

## 📞 Support

For issues or questions:
1. Check the README files in `backend/` and `frontend/` directories
2. Verify environment variables are set correctly
3. Ensure MongoDB is accessible
4. Confirm Gemini API key is valid

## 📄 License

This is a demo project for educational purposes.

---

**Built with ❤️ using FastAPI, React, MongoDB, and Gemini AI**
