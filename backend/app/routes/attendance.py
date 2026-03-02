"""
Attendance management routes
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models.subject import Subject
from app.models.attendance import Attendance
from app.utils.auth_utils import token_required
from app.utils.validators import validate_date

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('', methods=['POST'])
@token_required
def mark_attendance(current_user):
    """Mark attendance for a subject"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or not all(k in data for k in ['subject_id', 'date', 'status']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        subject_id = data['subject_id']
        date_str = data['date']
        status = data['status']
        
        # Validate subject ownership
        subject = Subject.query.filter_by(id=subject_id, user_id=current_user.id).first()
        if not subject:
            return jsonify({'error': 'Subject not found'}), 404
        
        # Validate date
        if not validate_date(date_str):
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Validate status
        if status not in ['Present', 'Absent']:
            return jsonify({'error': 'Status must be "Present" or "Absent"'}), 400
        
        # Check if attendance already exists for this date
        existing = Attendance.query.filter_by(subject_id=subject_id, date=date_obj).first()
        
        if existing:
            # Update existing attendance
            existing.status = status
            message = 'Attendance updated successfully'
        else:
            # Create new attendance
            attendance = Attendance(
                subject_id=subject_id,
                date=date_obj,
                status=status
            )
            db.session.add(attendance)
            message = 'Attendance marked successfully'
        
        db.session.commit()
        
        return jsonify({
            'message': message,
            'attendance': existing.to_dict() if existing else attendance.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to mark attendance', 'message': str(e)}), 500

@attendance_bp.route('/<int:subject_id>', methods=['GET'])
@token_required
def get_attendance(current_user, subject_id):
    """Get all attendance records for a subject"""
    try:
        # Validate subject ownership
        subject = Subject.query.filter_by(id=subject_id, user_id=current_user.id).first()
        if not subject:
            return jsonify({'error': 'Subject not found'}), 404
        
        # Get attendance records
        records = Attendance.query.filter_by(subject_id=subject_id).order_by(Attendance.date.desc()).all()
        
        return jsonify({
            'subject': subject.to_dict(),
            'attendance': [record.to_dict() for record in records]
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to fetch attendance', 'message': str(e)}), 500

@attendance_bp.route('/record/<int:attendance_id>', methods=['DELETE'])
@token_required
def delete_attendance(current_user, attendance_id):
    """Delete an attendance record"""
    try:
        attendance = Attendance.query.get(attendance_id)
        
        if not attendance:
            return jsonify({'error': 'Attendance record not found'}), 404
        
        # Verify ownership through subject
        subject = Subject.query.filter_by(id=attendance.subject_id, user_id=current_user.id).first()
        if not subject:
            return jsonify({'error': 'Unauthorized'}), 403
        
        db.session.delete(attendance)
        db.session.commit()
        
        return jsonify({'message': 'Attendance record deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete attendance', 'message': str(e)}), 500

@attendance_bp.route('/bulk', methods=['POST'])
@token_required
def mark_bulk_attendance(current_user):
    """Mark attendance for multiple dates"""
    try:
        data = request.get_json()
        
        if not data or 'records' not in data:
            return jsonify({'error': 'Records array is required'}), 400
        
        created = []
        errors = []
        
        for record in data['records']:
            try:
                subject_id = record['subject_id']
                date_str = record['date']
                status = record['status']
                
                # Validate subject ownership
                subject = Subject.query.filter_by(id=subject_id, user_id=current_user.id).first()
                if not subject:
                    errors.append({'record': record, 'error': 'Subject not found'})
                    continue
                
                # Validate and parse date
                if not validate_date(date_str):
                    errors.append({'record': record, 'error': 'Invalid date format'})
                    continue
                
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                
                # Check if exists
                existing = Attendance.query.filter_by(subject_id=subject_id, date=date_obj).first()
                
                if existing:
                    existing.status = status
                else:
                    attendance = Attendance(
                        subject_id=subject_id,
                        date=date_obj,
                        status=status
                    )
                    db.session.add(attendance)
                
                created.append(record)
            
            except Exception as e:
                errors.append({'record': record, 'error': str(e)})
        
        db.session.commit()
        
        return jsonify({
            'message': f'Processed {len(created)} records',
            'created': len(created),
            'errors': errors
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Bulk operation failed', 'message': str(e)}), 500
