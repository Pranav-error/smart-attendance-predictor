# 🎓 Smart Attendance & Shortage Predictor

A full-stack web application that intelligently tracks student attendance and predicts shortage risks before exams.

## 📋 Project Overview

This system is designed to help students manage their attendance proactively by:
- Real-time attendance tracking
- Intelligent shortage risk detection
- Predictive analytics for future attendance
- Visual dashboards with actionable insights

## 🚀 Tech Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT tokens with bcrypt password hashing
- **API Style**: RESTful JSON APIs

### Frontend
- **Framework**: React 18
- **State Management**: React Hooks (useState, useEffect)
- **Charts**: Chart.js with react-chartjs-2
- **Styling**: Modern CSS with responsive design
- **HTTP Client**: Axios

## 🏗️ System Architecture

```
┌─────────────────┐
│   React Client  │
│   (Frontend)    │
└────────┬────────┘
         │ REST APIs
         ▼
┌─────────────────┐
│  Flask Backend  │
│  - Auth Routes  │
│  - API Routes   │
│  - Services     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  SQLite DB      │
│  - Users        │
│  - Subjects     │
│  - Attendance   │
└─────────────────┘
```

## 📊 Core Features

### ✅ Attendance Management
- Add, edit, and delete subjects
- Mark daily attendance (Present/Absent)
- View subject-wise attendance records

### ✅ Real-Time Calculations
- **Total Classes**: Count of all classes
- **Classes Attended**: Count of present days
- **Attendance %**: (Attended / Total) × 100
- **Classes to Skip Safely**: Maximum absences before hitting threshold
- **Classes Needed to Recover**: Required attendance to reach safe zone

### ✅ Shortage Risk Detection
- **SAFE** (🟢): ≥ 85% - You're doing great!
- **WARNING** (🟡): 75-84% - Be careful!
- **DANGER** (🔴): < 75% - Immediate action needed!

### ✅ Prediction Logic
Smart algorithms that predict:
- Future attendance percentage based on current trend
- Minimum classes needed to reach safe zone
- Maximum classes that can be missed safely
- Risk messages with actionable advice

### ✅ Visual Dashboard
- Attendance bar charts per subject
- Trend graphs over time
- Risk indicator cards
- Overall attendance summary

## 🗄️ Database Schema

### Users Table
```sql
id              INTEGER PRIMARY KEY
name            VARCHAR(100)
email           VARCHAR(120) UNIQUE
password_hash   VARCHAR(255)
created_at      TIMESTAMP
```

### Subjects Table
```sql
id                          INTEGER PRIMARY KEY
user_id                     INTEGER (FK → Users)
subject_name                VARCHAR(100)
minimum_required_percentage INTEGER DEFAULT 75
created_at                  TIMESTAMP
```

### Attendance Table
```sql
id          INTEGER PRIMARY KEY
subject_id  INTEGER (FK → Subjects)
date        DATE
status      VARCHAR(10) ('Present'/'Absent')
created_at  TIMESTAMP
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info

### Subjects
- `POST /api/subjects` - Add new subject
- `GET /api/subjects` - Get all subjects for user
- `PUT /api/subjects/<id>` - Update subject
- `DELETE /api/subjects/<id>` - Delete subject

### Attendance
- `POST /api/attendance` - Mark attendance
- `GET /api/attendance/<subject_id>` - Get attendance records
- `DELETE /api/attendance/<id>` - Delete attendance record

### Analytics
- `GET /api/analytics/<subject_id>` - Get detailed analytics
- `GET /api/analytics/dashboard` - Get dashboard summary

## 📐 Prediction Formulas

### Current Attendance Percentage
```
percentage = (classes_attended / total_classes) × 100
```

### Classes Can Miss Safely
```
max_absences = floor((total_classes × min_percentage/100 - classes_attended) / (1 - min_percentage/100))
```

### Classes Needed to Recover
```
needed = ceil((min_percentage/100 × (total_classes + x) - classes_attended) / 1)
where x is classes needed
```

### Future Percentage Prediction
```
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
