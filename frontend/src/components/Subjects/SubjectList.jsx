import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { subjectsAPI } from '../../services/api';

const SubjectList = () => {
    const [subjects, setSubjects] = useState([]);
    const [newSubject, setNewSubject] = useState({ subject_name: '', minimum_required_percentage: 75 });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        fetchSubjects();
    }, []);

    const fetchSubjects = async () => {
        try {
            const response = await subjectsAPI.getAll();
            setSubjects(response.data.subjects);
            setLoading(false);
        } catch (err) {
            setError('Failed to load subjects');
            setLoading(false);
        }
    };

    const handleAddSubject = async (e) => {
        e.preventDefault();
        try {
            await subjectsAPI.create(newSubject);
            setNewSubject({ subject_name: '', minimum_required_percentage: 75 });
            fetchSubjects();
        } catch (err) {
            setError('Failed to add subject');
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm('Are you sure you want to delete this subject?')) {
            try {
                await subjectsAPI.delete(id);
                fetchSubjects();
            } catch (err) {
                setError('Failed to delete subject');
            }
        }
    };

    if (loading) return <div className="loading">Loading subjects...</div>;

    return (
        <div className="subject-management">
            <header className="page-header">
                <h1>📚 Manage Subjects</h1>
                <button onClick={() => navigate('/dashboard')} className="btn-secondary">
                    Back to Dashboard
                </button>
            </header>

            {error && <div className="error-message">{error}</div>}

            <div className="add-subject-form">
                <h2>Add New Subject</h2>
                <form onSubmit={handleAddSubject}>
                    <div className="form-row">
                        <input
                            type="text"
                            placeholder="Subject Name"
                            value={newSubject.subject_name}
                            onChange={(e) => setNewSubject({ ...newSubject, subject_name: e.target.value })}
                            required
                        />
                        <input
                            type="number"
                            placeholder="Min Required %"
                            value={newSubject.minimum_required_percentage}
                            onChange={(e) => setNewSubject({ ...newSubject, minimum_required_percentage: parseInt(e.target.value) })}
                            min="0"
                            max="100"
                            required
                        />
                        <button type="submit" className="btn-primary">Add Subject</button>
                    </div>
                </form>
            </div>

            <div className="subjects-list">
                <h2>Your Subjects ({subjects.length})</h2>
                {subjects.length > 0 ? (
                    <table className="subjects-table">
                        <thead>
                            <tr>
                                <th>Subject Name</th>
                                <th>Min Required %</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {subjects.map((subject) => (
                                <tr key={subject.id}>
                                    <td>{subject.subject_name}</td>
                                    <td>{subject.minimum_required_percentage}%</td>
                                    <td className="action-buttons">
                                        <button 
                                            onClick={() => navigate(`/attendance/${subject.id}`)}
                                            className="btn-small btn-primary"
                                        >
                                            Attendance
                                        </button>
                                        <button 
                                            onClick={() => navigate(`/analytics/${subject.id}`)}
                                            className="btn-small btn-secondary"
                                        >
                                            Analytics
                                        </button>
                                        <button 
                                            onClick={() => handleDelete(subject.id)}
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
                    <p className="empty-message">No subjects added yet. Add your first subject above!</p>
                )}
            </div>
        </div>
    );
};

export default SubjectList;
