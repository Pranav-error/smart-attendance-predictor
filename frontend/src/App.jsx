import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Auth/Login';
import Signup from './components/Auth/Signup';
import Dashboard from './components/Dashboard/Dashboard';
import SubjectList from './components/Subjects/SubjectList';
import MarkAttendance from './components/Attendance/MarkAttendance';
import Analytics from './components/Analytics/AttendanceChart';
import './styles/App.css';

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        const token = localStorage.getItem('token');
        setIsAuthenticated(!!token);
    }, []);

    const ProtectedRoute = ({ children }) => {
        return isAuthenticated ? children : <Navigate to="/login" />;
    };

    return (
        <Router>
            <div className="app">
                <Routes>
                    <Route path="/login" element={
                        isAuthenticated ? <Navigate to="/dashboard" /> : <Login setIsAuthenticated={setIsAuthenticated} />
                    } />
                    <Route path="/signup" element={
                        isAuthenticated ? <Navigate to="/dashboard" /> : <Signup setIsAuthenticated={setIsAuthenticated} />
                    } />
                    <Route path="/dashboard" element={
                        <ProtectedRoute><Dashboard setIsAuthenticated={setIsAuthenticated} /></ProtectedRoute>
                    } />
                    <Route path="/subjects" element={
                        <ProtectedRoute><SubjectList /></ProtectedRoute>
                    } />
                    <Route path="/attendance/:subjectId" element={
                        <ProtectedRoute><MarkAttendance /></ProtectedRoute>
                    } />
                    <Route path="/analytics/:subjectId" element={
                        <ProtectedRoute><Analytics /></ProtectedRoute>
                    } />
                    <Route path="/" element={<Navigate to="/dashboard" />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
