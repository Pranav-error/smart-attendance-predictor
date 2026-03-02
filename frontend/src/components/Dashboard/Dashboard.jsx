import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { analyticsAPI, subjectsAPI } from '../../services/api';
import AttendanceCard from './AttendanceCard';
import RiskIndicator from './RiskIndicator';
import '../../styles/App.css';

const Dashboard = ({ setIsAuthenticated }) => {
    const [dashboardData, setDashboardData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        fetchDashboard();
    }, []);

    const fetchDashboard = async () => {
        try {
            const response = await analyticsAPI.getDashboard();
            setDashboardData(response.data);
            setLoading(false);
        } catch (err) {
            setError('Failed to load dashboard');
            setLoading(false);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        setIsAuthenticated(false);
        navigate('/login');
    };

    if (loading) return <div className="loading">Loading dashboard...</div>;
    if (error) return <div className="error-message">{error}</div>;

    const { overall_stats, subjects } = dashboardData || {};

    return (
        <div className="dashboard">
            <header className="dashboard-header">
                <h1>📊 Attendance Dashboard</h1>
                <div className="header-actions">
                    <button onClick={() => navigate('/subjects')} className="btn-secondary">
                        Manage Subjects
                    </button>
                    <button onClick={handleLogout} className="btn-logout">
                        Logout
                    </button>
                </div>
            </header>

            <div className="overall-stats">
                <div className="stat-card">
                    <h3>Total Subjects</h3>
                    <p className="stat-value">{overall_stats?.total_subjects || 0}</p>
                </div>
                <div className="stat-card safe">
                    <h3>🟢 Safe</h3>
                    <p className="stat-value">{overall_stats?.safe_subjects || 0}</p>
                </div>
                <div className="stat-card warning">
                    <h3>🟡 Warning</h3>
                    <p className="stat-value">{overall_stats?.warning_subjects || 0}</p>
                </div>
                <div className="stat-card danger">
                    <h3>🔴 Danger</h3>
                    <p className="stat-value">{overall_stats?.danger_subjects || 0}</p>
                </div>
                <div className="stat-card">
                    <h3>Average Attendance</h3>
                    <p className="stat-value">{overall_stats?.average_attendance || 0}%</p>
                </div>
            </div>

            {subjects && subjects.length > 0 ? (
                <div className="subjects-grid">
                    {subjects.map((item) => (
                        <AttendanceCard 
                            key={item.subject.id} 
                            subject={item.subject}
                            stats={item.stats}
                            riskZone={item.risk_zone}
                            onRefresh={fetchDashboard}
                        />
                    ))}
                </div>
            ) : (
                <div className="empty-state">
                    <h2>No subjects yet!</h2>
                    <p>Add your first subject to start tracking attendance</p>
                    <button onClick={() => navigate('/subjects')} className="btn-primary">
                        Add Subject
                    </button>
                </div>
            )}
        </div>
    );
};

export default Dashboard;
