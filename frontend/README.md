# Finance AI Assistant - Frontend

Modern React frontend built with Vite, plain JavaScript, and Tailwind CSS.

## Features

- **Authentication**: JWT-based login/signup
- **Dashboard**: Fee breakdown, payment history, upcoming dues
- **Payments**: Dummy payment initiation and receipt viewing
- **AI Assistant**: Document summarization and financial advice (powered by Gemini)
- **Reminders**: Create and manage payment reminders

## Quick Start

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

Frontend will be available at http://localhost:3000

## Build for Production

```bash
npm run build
npm run preview
```

## Tech Stack

- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS
- **Routing**: React Router v6
- **Icons**: Lucide React
- **API**: Fetch API with proxy to backend

## Project Structure

```
src/
├── components/       # Reusable components (Layout, ProtectedRoute)
├── context/          # React Context (AuthContext)
├── pages/            # Page components (Dashboard, Payments, etc.)
├── utils/            # Utilities (API client)
├── App.jsx           # Main app with routing
├── main.jsx          # Entry point
└── index.css         # Global styles with Tailwind
```

## API Proxy

The Vite dev server proxies `/api/*` requests to `http://127.0.0.1:8000` (backend).

## Demo Credentials

- Email: `parent1@example.com`
- Password: `password123`

## Notes

- All API calls use JWT tokens stored in localStorage
- Protected routes redirect to login if not authenticated
- Responsive design works on mobile, tablet, and desktop
