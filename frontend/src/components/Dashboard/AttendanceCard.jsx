import React from 'react';
import { useNavigate } from 'react-router-dom';
import RiskIndicator from './RiskIndicator';

const AttendanceCard = ({ subject, stats, riskZone, onRefresh }) => {
    const navigate = useNavigate();

    if (!stats) {
        return (
            <div className="attendance-card">
                <h3>{subject.subject_name}</h3>
                <p className="no-data">No attendance records yet</p>
                <button 
                    onClick={() => navigate(`/attendance/${subject.id}`)}
                    className="btn-secondary"
                >
                    Mark Attendance
                </button>
            </div>
        );
    }

    return (
        <div className="attendance-card">
            <div className="card-header">
                <h3>{subject.subject_name}</h3>
                {riskZone && <RiskIndicator riskZone={riskZone} />}
            </div>

            <div className="percentage-display">
                <div className="percentage-circle" style={{ borderColor: riskZone?.color }}>
                    <span className="percentage-value">{stats.percentage}%</span>
                </div>
            </div>

            <div className="stats-grid">
                <div className="stat-item">
                    <span className="stat-label">Total Classes</span>
                    <span className="stat-value">{stats.total_classes}</span>
                </div>
                <div className="stat-item">
                    <span className="stat-label">Attended</span>
                    <span className="stat-value">{stats.classes_attended}</span>
                </div>
                <div className="stat-item">
                    <span className="stat-label">Absent</span>
                    <span className="stat-value">{stats.classes_absent}</span>
                </div>
                <div className="stat-item">
                    <span className="stat-label">Can Skip</span>
                    <span className="stat-value">{stats.can_skip_safely}</span>
                </div>
            </div>

            {stats.classes_needed_to_recover > 0 && (
                <div className="recovery-alert">
                    ⚠️ Attend next {stats.classes_needed_to_recover} classes to recover
                </div>
            )}

            <div className="card-actions">
                <button 
                    onClick={() => navigate(`/attendance/${subject.id}`)}
                    className="btn-primary"
                >
                    Mark Attendance
                </button>
                <button 
                    onClick={() => navigate(`/analytics/${subject.id}`)}
                    className="btn-secondary"
                >
                    View Analytics
                </button>
            </div>
        </div>
    );
};

export default AttendanceCard;
