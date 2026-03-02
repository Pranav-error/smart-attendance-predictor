import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { subjectsAPI, attendanceAPI } from '../../services/api';
import { getTodayDate } from '../../utils/helpers';

const MarkAttendance = () => {
    const { subjectId } = useParams();
    const navigate = useNavigate();
    const [subject, setSubject] = useState(null);
    const [attendance, setAttendance] = useState([]);
    const [date, setDate] = useState(getTodayDate());
    const [status, setStatus] = useState('Present');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchData();
    }, [subjectId]);

    const fetchData = async () => {
        try {
            const [subjectRes, attendanceRes] = await Promise.all([
                subjectsAPI.getById(subjectId),
                attendanceAPI.getBySubject(subjectId)
            ]);
            setSubject(subjectRes.data.subject);
            setAttendance(attendanceRes.data.attendance);
            setLoading(false);
        } catch (err) {
            setError('Failed to load data');
            setLoading(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await attendanceAPI.mark({
                subject_id: parseInt(subjectId),
                date,
                status
            });
            fetchData();
            setDate(getTodayDate());
            setStatus('Present');
        } catch (err) {
            setError('Failed to mark attendance');
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm('Delete this attendance record?')) {
            try {
                await attendanceAPI.delete(id);
                fetchData();
            } catch (err) {
                setError('Failed to delete record');
            }
        }
    };

    if (loading) return <div className="loading">Loading...</div>;
    if (!subject) return <div className="error-message">Subject not found</div>;

    return (
        <div className="attendance-page">
            <header className="page-header">
                <h1>📝 Mark Attendance - {subject.subject_name}</h1>
                <button onClick={() => navigate('/dashboard')} className="btn-secondary">
                    Back to Dashboard
                </button>
            </header>

            {error && <div className="error-message">{error}</div>}

            <div className="mark-attendance-form">
                <h2>Mark Today's Attendance</h2>
                <form onSubmit={handleSubmit}>
                    <div className="form-row">
                        <div className="form-group">
                            <label>Date</label>
                            <input
                                type="date"
                                value={date}
                                onChange={(e) => setDate(e.target.value)}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Status</label>
                            <select value={status} onChange={(e) => setStatus(e.target.value)}>
                                <option value="Present">Present</option>
                                <option value="Absent">Absent</option>
                            </select>
                        </div>
                        <button type="submit" className="btn-primary">
                            Mark Attendance
                        </button>
                    </div>
                </form>
            </div>

            <div className="attendance-history">
                <h2>Attendance History ({attendance.length} records)</h2>
                {attendance.length > 0 ? (
                    <table className="attendance-table">
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {attendance.map((record) => (
                                <tr key={record.id}>
                                    <td>{new Date(record.date).toLocaleDateString()}</td>
                                    <td>
                                        <span className={`status-badge ${record.status.toLowerCase()}`}>
                                            {record.status === 'Present' ? '✓' : '✗'} {record.status}
                                        </span>
                                    </td>
                                    <td>
                                        <button 
                                            onClick={() => handleDelete(record.id)}
                                            className="btn-small btn-danger"
                                        >
                                            Delete
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ) : (
                    <p className="empty-message">No attendance records yet</p>
                )}
            </div>
        </div>
    );
};

export default MarkAttendance;
