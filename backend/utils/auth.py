# utils/auth.py
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.user import User

def jwt_required_custom(fn):
    """Custom JWT required decorator"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Invalid or expired token'}), 401
    return wrapper

def get_current_user():
    """Get current user from JWT token"""
    try:
        user_id = get_jwt_identity()
        return User.query.get(user_id)
    except:
        return None