"""
Subject management routes
"""
from flask import Blueprint, request, jsonify
from app import db
from app.models.subject import Subject
from app.utils.auth_utils import token_required

subjects_bp = Blueprint('subjects', __name__)

@subjects_bp.route('', methods=['POST'])
@token_required
def create_subject(current_user):
    """Create a new subject"""
    try:
        data = request.get_json()
        
        if not data or 'subject_name' not in data:
            return jsonify({'error': 'Subject name is required'}), 400
        
        subject_name = data['subject_name'].strip()
        min_percentage = data.get('minimum_required_percentage', 75)
        
        # Validate minimum percentage
        if not (0 <= min_percentage <= 100):
            return jsonify({'error': 'Minimum percentage must be between 0 and 100'}), 400
        
        # Create subject
        subject = Subject(
            user_id=current_user.id,
            subject_name=subject_name,
            minimum_required_percentage=min_percentage
        )
        
        db.session.add(subject)
        db.session.commit()
        
        return jsonify({
            'message': 'Subject created successfully',
            'subject': subject.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create subject', 'message': str(e)}), 500

@subjects_bp.route('', methods=['GET'])
@token_required
def get_subjects(current_user):
    """Get all subjects for current user"""
    try:
        subjects = Subject.query.filter_by(user_id=current_user.id).all()
        
        return jsonify({
            'subjects': [subject.to_dict() for subject in subjects]
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to fetch subjects', 'message': str(e)}), 500

@subjects_bp.route('/<int:subject_id>', methods=['GET'])
@token_required
def get_subject(current_user, subject_id):
    """Get specific subject"""
    try:
        subject = Subject.query.filter_by(id=subject_id, user_id=current_user.id).first()
        
        if not subject:
            return jsonify({'error': 'Subject not found'}), 404
        
        return jsonify({'subject': subject.to_dict()}), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to fetch subject', 'message': str(e)}), 500

@subjects_bp.route('/<int:subject_id>', methods=['PUT'])
@token_required
def update_subject(current_user, subject_id):
    """Update subject"""
    try:
        subject = Subject.query.filter_by(id=subject_id, user_id=current_user.id).first()
        
        if not subject:
            return jsonify({'error': 'Subject not found'}), 404
        
        data = request.get_json()
        
        if 'subject_name' in data:
            subject.subject_name = data['subject_name'].strip()
        
        if 'minimum_required_percentage' in data:
            min_percentage = data['minimum_required_percentage']
            if not (0 <= min_percentage <= 100):
                return jsonify({'error': 'Minimum percentage must be between 0 and 100'}), 400
            subject.minimum_required_percentage = min_percentage
        
        db.session.commit()
        
        return jsonify({
            'message': 'Subject updated successfully',
            'subject': subject.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update subject', 'message': str(e)}), 500

@subjects_bp.route('/<int:subject_id>', methods=['DELETE'])
@token_required
def delete_subject(current_user, subject_id):
    """Delete subject"""
    try:
        subject = Subject.query.filter_by(id=subject_id, user_id=current_user.id).first()
        
        if not subject:
            return jsonify({'error': 'Subject not found'}), 404
        
        db.session.delete(subject)
        db.session.commit()
        
        return jsonify({'message': 'Subject deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete subject', 'message': str(e)}), 500
