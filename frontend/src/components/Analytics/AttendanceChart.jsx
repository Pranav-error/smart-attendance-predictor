import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import { Bar, Doughnut } from 'react-chartjs-2';
import { analyticsAPI } from '../../services/api';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

const Analytics = () => {
    const { subjectId } = useParams();
    const navigate = useNavigate();
    const [analytics, setAnalytics] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchAnalytics();
    }, [subjectId]);

    const fetchAnalytics = async () => {
        try {
            const response = await analyticsAPI.getSubjectAnalytics(subjectId);
            setAnalytics(response.data);
            setLoading(false);
        } catch (err) {
            setError('Failed to load analytics');
            setLoading(false);
        }
    };

    if (loading) return <div className="loading">Loading analytics...</div>;
    if (error) return <div className="error-message">{error}</div>;
    if (!analytics) return <div className="error-message">No data available</div>;

    const { subject, stats, risk_analysis, predictions, alerts, trend } = analytics;

    // Chart data
    const attendanceChartData = {
        labels: ['Attended', 'Absent'],
        datasets: [{
            data: [stats.classes_attended, stats.classes_absent],
            backgroundColor: ['#4CAF50', '#F44336'],
        }]
    };

    const predictionChartData = {
        labels: ['After 5', 'After 10', 'After 15', 'After 20'],
        datasets: [{
            label: 'Predicted %',
            data: [
                predictions.maintain_trend.after_5,
                predictions.maintain_trend.after_10,
                predictions.maintain_trend.after_15,
                predictions.maintain_trend.after_20
            ],
            backgroundColor: '#2196F3',
        }]
    };

    return (
        <div className="analytics-page">
            <header className="page-header">
                <h1>📊 Analytics - {subject.subject_name}</h1>
                <button onClick={() => navigate('/dashboard')} className="btn-secondary">
                    Back to Dashboard
                </button>
            </header>

            {/* Risk Zone */}
            <div className="risk-section" style={{ borderColor: risk_analysis.risk_zone.color }}>
                <div className="risk-header">
                    <h2>{risk_analysis.risk_zone.emoji} {risk_analysis.risk_zone.zone}</h2>
                    <p>{risk_analysis.risk_zone.message}</p>
                </div>
            </div>

            {/* Current Stats */}
            <div className="stats-cards">
                <div className="stat-card-large">
                    <h3>Current Percentage</h3>
                    <div className="large-percentage" style={{ color: risk_analysis.risk_zone.color }}>
                        {stats.percentage}%
                    </div>
                </div>
                <div className="stat-card-large">
                    <h3>Total Classes</h3>
                    <p className="large-number">{stats.total_classes}</p>
                </div>
                <div className="stat-card-large">
                    <h3>Classes Attended</h3>
                    <p className="large-number">{stats.classes_attended}</p>
                </div>
                <div className="stat-card-large">
                    <h3>Can Skip Safely</h3>
                    <p className="large-number">{stats.can_skip_safely}</p>
                </div>
            </div>

            {/* Alerts */}
            {alerts && alerts.length > 0 && (
                <div className="alerts-section">
                    <h2>⚠️ Alerts</h2>
                    {alerts.map((alert, index) => (
                        <div key={index} className={`alert alert-${alert.level.toLowerCase()}`}>
                            <strong>{alert.level}:</strong> {alert.message}
                            <br />
                            <em>Action: {alert.action}</em>
                        </div>
                    ))}
                </div>
            )}

            {/* Recommendations */}
            <div className="recommendations-section">
                <h2>💡 Recommendations</h2>
                <ul className="recommendations-list">
                    {risk_analysis.recommendations.map((rec, index) => (
                        <li key={index}>{rec}</li>
                    ))}
                </ul>
            </div>

            {/* Charts */}
            <div className="charts-section">
                <div className="chart-container">
                    <h3>Attendance Distribution</h3>
                    <Doughnut data={attendanceChartData} />
                </div>
                <div className="chart-container">
                    <h3>Future Prediction (Maintain Trend)</h3>
                    <Bar data={predictionChartData} options={{
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 100
                            }
                        }
                    }} />
                </div>
            </div>

            {/* Scenarios */}
            <div className="scenarios-section">
                <div className="scenario-card">
                    <h3>😱 Worst Case Scenarios</h3>
                    <p>If you miss next 5 classes: {predictions.worst_case_scenarios.miss_5}%</p>
                    <p>If you miss next 10 classes: {predictions.worst_case_scenarios.miss_10}%</p>
                    <p>If you miss next 15 classes: {predictions.worst_case_scenarios.miss_15}%</p>
                </div>
                <div className="scenario-card">
                    <h3>🌟 Best Case Scenarios</h3>
                    <p>If you attend next 5 classes: {predictions.best_case_scenarios.attend_5}%</p>
                    <p>If you attend next 10 classes: {predictions.best_case_scenarios.attend_10}%</p>
                    <p>If you attend next 15 classes: {predictions.best_case_scenarios.attend_15}%</p>
                </div>
            </div>

            {/* Trend */}
            {trend && trend.trend !== 'insufficient_data' && (
                <div className="trend-section">
                    <h3>📈 Attendance Trend</h3>
                    <p><strong>Status:</strong> {trend.trend.toUpperCase()}</p>
                    <p><strong>Recent Rate:</strong> {trend.recent_rate}%</p>
                    <p><strong>Overall Rate:</strong> {trend.overall_rate}%</p>
                    <p>{trend.message}</p>
                </div>
            )}
        </div>
    );
};

export default Analytics;
