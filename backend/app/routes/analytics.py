"""
Analytics and prediction routes
"""
from flask import Blueprint, request, jsonify
from app.models.subject import Subject
from app.models.attendance import Attendance
from app.utils.auth_utils import token_required
from app.services.attendance_calculator import AttendanceCalculator
from app.services.risk_analyzer import RiskAnalyzer
from app.services.shortage_predictor import ShortagePredictor

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/<int:subject_id>', methods=['GET'])
@token_required
def get_subject_analytics(current_user, subject_id):
    """Get comprehensive analytics for a subject"""
    try:
        # Validate subject ownership
        subject = Subject.query.filter_by(id=subject_id, user_id=current_user.id).first()
        if not subject:
            return jsonify({'error': 'Subject not found'}), 404
        
        # Get attendance records
        records = Attendance.query.filter_by(subject_id=subject_id).all()
        
        if not records:
            return jsonify({
                'subject': subject.to_dict(),
                'message': 'No attendance records found',
                'stats': {
                    'total_classes': 0,
                    'classes_attended': 0,
                    'classes_absent': 0,
                    'percentage': 0,
                    'can_skip_safely': 0,
                    'classes_needed_to_recover': 0,
                    'predicted_percentage_10_classes': 0,
                    'minimum_required': subject.minimum_required_percentage
                }
            }), 200
        
        # Calculate statistics
        stats = AttendanceCalculator.get_attendance_stats(
            records, 
            subject.minimum_required_percentage
        )
        
        # Analyze risk
        analysis = RiskAnalyzer.analyze(stats)
        
        # Predict scenarios
        worst_case = ShortagePredictor.predict_scenario(
            stats['total_classes'],
            stats['classes_attended'],
            'worst_case',
            subject.minimum_required_percentage
        )
        
        best_case = ShortagePredictor.predict_scenario(
            stats['total_classes'],
            stats['classes_attended'],
            'best_case',
            subject.minimum_required_percentage
        )
        
        maintain_trend = ShortagePredictor.predict_scenario(
            stats['total_classes'],
            stats['classes_attended'],
            'maintain',
            subject.minimum_required_percentage
        )
        
        # Get alerts
        alerts = ShortagePredictor.get_shortage_alert(stats)
        
        # Get trend analysis
        trend = ShortagePredictor.predict_trend(records)
        
        return jsonify({
            'subject': subject.to_dict(),
            'stats': stats,
            'risk_analysis': analysis,
            'predictions': {
                'worst_case_scenarios': worst_case,
                'best_case_scenarios': best_case,
                'maintain_trend': maintain_trend
            },
            'alerts': alerts,
            'trend': trend
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to fetch analytics', 'message': str(e)}), 500

@analytics_bp.route('/dashboard', methods=['GET'])
@token_required
def get_dashboard(current_user):
    """Get dashboard summary for all subjects"""
    try:
        subjects = Subject.query.filter_by(user_id=current_user.id).all()
        
        dashboard_data = {
            'overall_stats': {
                'total_subjects': len(subjects),
                'safe_subjects': 0,
                'warning_subjects': 0,
                'danger_subjects': 0,
                'average_attendance': 0
            },
            'subjects': []
        }
        
        total_percentage = 0
        subject_count = 0
        
        for subject in subjects:
            records = Attendance.query.filter_by(subject_id=subject.id).all()
            
            if records:
                stats = AttendanceCalculator.get_attendance_stats(
                    records,
                    subject.minimum_required_percentage
                )
                
                risk_zone = RiskAnalyzer.get_risk_zone(stats['percentage'])
                
                # Count risk zones
                if risk_zone['zone'] == 'SAFE':
                    dashboard_data['overall_stats']['safe_subjects'] += 1
                elif risk_zone['zone'] == 'WARNING':
                    dashboard_data['overall_stats']['warning_subjects'] += 1
                else:
                    dashboard_data['overall_stats']['danger_subjects'] += 1
                
                total_percentage += stats['percentage']
                subject_count += 1
                
                dashboard_data['subjects'].append({
                    'subject': subject.to_dict(),
                    'stats': stats,
                    'risk_zone': risk_zone
                })
            else:
                dashboard_data['subjects'].append({
                    'subject': subject.to_dict(),
                    'stats': None,
                    'risk_zone': None
                })
        
        # Calculate average attendance
        if subject_count > 0:
            dashboard_data['overall_stats']['average_attendance'] = round(
                total_percentage / subject_count, 2
            )
        
        return jsonify(dashboard_data), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to fetch dashboard', 'message': str(e)}), 500

@analytics_bp.route('/predict/<int:subject_id>', methods=['POST'])
@token_required
def predict_future(current_user, subject_id):
    """Predict future attendance based on custom scenarios"""
    try:
        # Validate subject ownership
        subject = Subject.query.filter_by(id=subject_id, user_id=current_user.id).first()
        if not subject:
            return jsonify({'error': 'Subject not found'}), 404
        
        records = Attendance.query.filter_by(subject_id=subject_id).all()
        
        if not records:
            return jsonify({'error': 'No attendance records to analyze'}), 400
        
        data = request.get_json()
        future_present = data.get('future_present', 0)
        future_absent = data.get('future_absent', 0)
        
        stats = AttendanceCalculator.get_attendance_stats(
            records,
            subject.minimum_required_percentage
        )
        
        # Calculate prediction
        new_total = stats['total_classes'] + future_present + future_absent
        new_attended = stats['classes_attended'] + future_present
        new_percentage = (new_attended / new_total * 100) if new_total > 0 else 0
        
        return jsonify({
            'current_percentage': stats['percentage'],
            'predicted_percentage': round(new_percentage, 2),
            'future_present': future_present,
            'future_absent': future_absent,
            'new_total_classes': new_total,
            'new_attended_classes': new_attended,
            'risk_zone': RiskAnalyzer.get_risk_zone(new_percentage)
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Prediction failed', 'message': str(e)}), 500
