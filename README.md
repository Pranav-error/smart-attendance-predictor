# 🎓 Smart Attendance & Shortage Predictor

A full-stack web application that helps students track attendance, detect shortage risks in real time, and predict future attendance outcomes before exams.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1.0-black?logo=flask)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [API Reference](#-api-reference)
- [Prediction Logic](#-prediction-logic)
- [Screenshots](#-screenshots)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 Auth | JWT-based signup/login with bcrypt password hashing |
| 📚 Subjects | Full CRUD — add, edit, delete subjects with custom thresholds |
| ✅ Attendance | Mark Present/Absent per subject per day |
| 📊 Analytics | Per-subject stats with shortage alerts and scenario predictions |
| 🔴 Risk Zones | SAFE / WARNING / DANGER zones with actionable advice |
| 📈 Charts | Bar charts showing attendance trend per subject |
| 🔮 Prediction | Worst-case, best-case, and maintain-rate scenario projections |

---

## 🚀 Tech Stack

### Backend
- **Framework**: Flask 3.1.0 — Application Factory pattern, 4 Blueprints
- **ORM**: SQLAlchemy 2.0.47 (Python 3.13-compatible)
- **Database**: SQLite (auto-created on first run)
- **Auth**: Flask-JWT-Extended 4.7.1 + bcrypt 4.2.1
- **API Style**: RESTful JSON

### Frontend
- **Framework**: React 18
- **Routing**: react-router-dom v6 with protected routes
- **Charts**: Chart.js + react-chartjs-2
- **HTTP Client**: Axios with JWT interceptor
- **State**: React Hooks (useState, useEffect)

---

## 🏗️ Architecture

```
┌──────────────────────────────────┐
│       React Frontend (:3000)     │
│  Login · Dashboard · Analytics   │
└────────────────┬─────────────────┘
                 │  Axios + JWT Bearer
                 ▼
┌──────────────────────────────────┐
│       Flask Backend (:5001)      │
│  auth_bp · subjects_bp           │
│  attendance_bp · analytics_bp    │
│  Services: Calculator · Risk ·   │
│           ShortagePredictor      │
└────────────────┬─────────────────┘
                 │  SQLAlchemy ORM
                 ▼
┌──────────────────────────────────┐
│   SQLite — attendance.db         │
│   users · subjects · attendance  │
└──────────────────────────────────┘
```

---

## �️ Project Structure

```
attendance/
├── backend/
│   ├── run.py                    # Entry point
│   ├── requirements.txt
│   ├── .env                      # PORT, SECRET_KEY, DB_URL
│   └── app/
│       ├── __init__.py           # App factory (create_app)
│       ├── config.py             # Dev / Prod / Test configs
│       ├── models/
│       │   ├── user.py
│       │   ├── subject.py
│       │   └── attendance.py
│       ├── routes/
│       │   ├── auth.py           # /api/auth/*
│       │   ├── subjects.py       # /api/subjects/*
│       │   ├── attendance.py     # /api/attendance/*
│       │   └── analytics.py      # /api/analytics/*
│       ├── services/
│       │   ├── attendance_calculator.py
│       │   ├── risk_analyzer.py
│       │   └── shortage_predictor.py
│       └── utils/
│           ├── auth_utils.py     # token_required decorator
│           └── validators.py
└── frontend/
    └── src/
        ├── App.jsx               # Router + ProtectedRoute
        ├── services/api.js       # Axios instance + interceptor
        └── components/
            ├── Auth/             # Login, Signup
            ├── Dashboard/        # Dashboard, AttendanceCard, RiskIndicator
            ├── Subjects/         # SubjectList
            ├── Attendance/       # MarkAttendance
            └── Analytics/        # AttendanceChart
```

---

## 🛠️ Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm 9+

### 1 — Clone the repo

```bash
git clone https://github.com/Pranav-error/smart-attendance-predictor.git
cd smart-attendance-predictor
```

### 2 — Backend setup

```bash
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << 'EOF'
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-change-in-production
DATABASE_URL=sqlite:///attendance.db
CORS_ORIGINS=http://localhost:3000
PORT=5001
EOF

# Start the server
python run.py
# → Running on http://localhost:5001
```

### 3 — Frontend setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
echo "REACT_APP_API_URL=http://localhost:5001/api" > .env

# Start the app
npm start
# → Running on http://localhost:3000
```

> **macOS note:** Port 5000 is occupied by AirPlay Receiver — use **5001** for Flask.

---

## 🔌 API Reference

All protected routes require `Authorization: Bearer <token>`.

### Auth — `/api/auth`

| Method | Endpoint | Body | Description |
|--------|----------|------|-------------|
| POST | `/signup` | `{name, email, password}` | Register a new user |
| POST | `/login` | `{email, password}` | Login, returns JWT |
| GET | `/me` | — | Get current user info |

### Subjects — `/api/subjects`

| Method | Endpoint | Body | Description |
|--------|----------|------|-------------|
| GET | `/` | — | List all subjects |
| POST | `/` | `{subject_name, minimum_required_percentage}` | Create subject |
| PUT | `/<id>` | `{subject_name, minimum_required_percentage}` | Update subject |
| DELETE | `/<id>` | — | Delete subject |

### Attendance — `/api/attendance`

| Method | Endpoint | Body | Description |
|--------|----------|------|-------------|
| POST | `/` | `{subject_id, date, status}` | Mark attendance |
| GET | `/<subject_id>` | — | Get all records for subject |
| DELETE | `/<id>` | — | Delete a record |

### Analytics — `/api/analytics`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/<subject_id>` | Full stats, risk analysis, and predictions |
| GET | `/dashboard` | Aggregated summary across all subjects |

**Sample analytics response:**
```json
{
  "stats": {
    "total_classes": 12,
    "classes_attended": 9,
    "percentage": 75.0,
    "can_skip_safely": 0,
    "classes_needed_to_recover": 0
  },
  "risk_analysis": {
    "risk_zone": { "zone": "WARNING", "emoji": "🟡" }
  },
  "predictions": {
    "worst_case":  { "miss_5": 60.0, "miss_10": 52.94 },
    "best_case":   { "attend_5": 82.35, "attend_10": 86.96 },
    "maintain":    { "after_5": 75.0, "after_10": 75.0 }
  }
}
```

---

## 📐 Prediction Logic

### Attendance Percentage
```
percentage = (classes_attended / total_classes) × 100
```

### Safe Skips (how many classes you can miss)
```
can_skip = floor( (attended − min% × total) / min% )
```
where `min%` is the threshold (default 0.75).

### Classes Needed to Recover
Iterates `x` from 1 upward until:
```
(attended + x) / (total + x) ≥ min_percentage / 100
```

### Scenario Projections

| Scenario | Logic |
|---|---|
| **Worst case** | Miss next 5/10/15 — all absent |
| **Best case** | Attend next 5/10/15 — all present |
| **Maintain rate** | Continue at current attendance rate |

---

## 🔴 Risk Zones

| Zone | Threshold | Emoji | Message |
|------|-----------|-------|---------|
| SAFE | ≥ 85% | 🟢 | You're doing great! |
| WARNING | 75 – 84% | 🟡 | Be careful — attend regularly |
| DANGER | < 75% | 🔴 | Immediate action required |

---

## 🗄️ Database Schema

```sql
-- Users
CREATE TABLE users (
    id            INTEGER PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    email         VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Subjects
CREATE TABLE subjects (
    id                          INTEGER PRIMARY KEY,
    user_id                     INTEGER NOT NULL REFERENCES users(id),
    subject_name                VARCHAR(100) NOT NULL,
    minimum_required_percentage INTEGER DEFAULT 75,
    created_at                  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Attendance
CREATE TABLE attendance (
    id         INTEGER PRIMARY KEY,
    subject_id INTEGER NOT NULL REFERENCES subjects(id),
    date       DATE NOT NULL,
    status     VARCHAR(10) NOT NULL CHECK(status IN ('Present','Absent')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🧪 Demo Credentials

A demo account is seeded automatically on first run:

```
Email:    demo@student.com
Password: demo1234
```

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push and open a PR: `git push origin feature/your-feature`

---

## 📄 License

MIT © [Pranav-error](https://github.com/Pranav-error)
If trend continues:
future_percentage = classes_attended / (total_classes + predicted_future_classes)
```

## 🎨 Resume-Ready Project Description

**Smart Attendance & Shortage Predictor** | Full-Stack Web Application
- Developed a production-grade attendance management system with predictive analytics using **React, Flask, and SQLite**
- Implemented **JWT-based authentication** with bcrypt password hashing for secure user management
- Built intelligent **shortage risk detection algorithm** that categorizes attendance into Safe/Warning/Danger zones
- Created **predictive analytics engine** that forecasts future attendance and calculates recovery strategies
- Designed **RESTful APIs** following industry best practices with proper error handling and validation
- Developed **responsive React dashboard** with real-time charts using Chart.js for data visualization
- Architected clean **3-tier architecture** with separation of concerns (Models, Services, Routes)
- Implemented advanced SQL queries with **SQLAlchemy ORM** including relationships and indexing

## 📝 Setup Instructions

See [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md) for detailed installation steps.

## 🎯 Interview Preparation

See [docs/INTERVIEW_QA.md](docs/INTERVIEW_QA.md) for common questions and answers about this project.

## 📄 License

MIT License - Feel free to use this project for learning and portfolio purposes.
