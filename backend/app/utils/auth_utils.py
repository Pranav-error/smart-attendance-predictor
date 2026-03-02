"""
Authentication utility functions
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app import db
from app.models.user import User

def token_required(f):
    """Decorator to protect routes that require authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            # identity is stored as str — cast back to int for DB lookup
            current_user = db.session.get(User, int(current_user_id))

            if not current_user:
                return jsonify({'error': 'User not found'}), 404

            return f(current_user, *args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Invalid or expired token', 'message': str(e)}), 401

    return decorated
