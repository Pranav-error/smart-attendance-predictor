# 🚀 Setup Guide

Complete step-by-step instructions to set up and run the Smart Attendance & Shortage Predictor application.

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn
- Git (optional)

## Backend Setup

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Create Virtual Environment
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
The `.env` file is already configured with default values. For production, update:
```bash
# Edit backend/.env
SECRET_KEY=your-production-secret-key
JWT_SECRET_KEY=your-production-jwt-key
```

### 5. Run the Backend Server
```bash
python run.py
```

The backend API will start on `http://localhost:5000`

### 6. Verify Backend is Running
Open browser and visit: `http://localhost:5000/api/health`

You should see:
```json
{
  "status": "healthy",
  "message": "Smart Attendance API is running"
}
```

## Frontend Setup

### 1. Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Configure Environment Variables
The `.env` file is already set. For production:
```bash
# Edit frontend/.env
REACT_APP_API_URL=https://your-api-domain.com/api
```

### 4. Start Development Server
```bash
npm start
# or
yarn start
```

The frontend will open automatically at `http://localhost:3000`

## First Time Usage

### 1. Create an Account
- Click "Sign up" on the login page
- Enter your name, email, and password (minimum 6 characters)
- Click "Sign Up"

### 2. Add Subjects
- After login, click "Manage Subjects"
- Enter subject name and minimum required percentage (default: 75%)
- Click "Add Subject"

### 3. Mark Attendance
- From dashboard, click "Mark Attendance" on any subject card
- Select date and status (Present/Absent)
- Click "Mark Attendance"

### 4. View Analytics
- Click "View Analytics" on any subject card
- See predictions, risk analysis, and recommendations

## Production Deployment

### Backend Deployment (Example: Heroku)

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set JWT_SECRET_KEY=your-jwt-key

# Deploy
git push heroku main
```

### Frontend Deployment (Example: Vercel)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel --prod
```

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError`
- **Solution**: Make sure virtual environment is activated and dependencies are installed

**Problem**: Database errors
- **Solution**: Delete `attendance.db` file and restart the server

**Problem**: Port 5000 already in use
- **Solution**: Kill the process or change port in `.env`: `PORT=5001`

### Frontend Issues

**Problem**: `npm install` fails
- **Solution**: Clear npm cache: `npm cache clean --force`

**Problem**: API connection errors
- **Solution**: Verify backend is running and `.env` has correct API_URL

**Problem**: CORS errors
- **Solution**: Check CORS_ORIGINS in backend `.env` includes frontend URL

## Database Management

### Reset Database
```bash
cd backend
rm attendance.db
python run.py  # Will recreate tables
```

### Backup Database
```bash
cd backend
cp attendance.db attendance_backup_$(date +%Y%m%d).db
```

## Testing

### Test Backend APIs
```bash
# Test signup
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"password123"}'

# Test login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

### Run Frontend Tests
```bash
cd frontend
npm test
```

## Performance Tips

1. **Database Indexing**: Already configured on frequently queried fields
2. **API Caching**: Consider implementing Redis for production
3. **Frontend Optimization**: Run `npm run build` for production-optimized bundle
4. **Lazy Loading**: Consider code-splitting for large applications

## Security Best Practices

1. Change default SECRET_KEY and JWT_SECRET_KEY
2. Use HTTPS in production
3. Implement rate limiting for APIs
4. Regular security updates: `pip list --outdated` and `npm outdated`
5. Never commit `.env` files to version control

## Support

For issues or questions:
1. Check this guide first
2. Review error messages carefully
3. Check browser console (F12) for frontend errors
4. Check terminal for backend errors

Happy tracking! 🎓
