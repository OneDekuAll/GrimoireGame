# routes/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from utils.database import db
from models.user import User
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.json
        
        # Validate required fields
        if not data.get('username'):
            return jsonify({'error': 'Username is required'}), 400
        if not data.get('email'):
            return jsonify({'error': 'Email is required'}), 400
        if not data.get('password'):
            return jsonify({'error': 'Password is required'}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already taken'}), 400
        
        # Create new user
        new_user = User(
            username=data['username'],
            email=data['email']
        )
        new_user.set_password(data['password'])
        
        db.session.add(new_user)
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(
            identity=new_user.id,
            expires_delta=timedelta(days=1)
        )
        
        return jsonify({
            'message': 'User registered successfully',
            'token': access_token,
            'user': new_user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Registration error: {str(e)}")  # Debug logging
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user with username or email"""
    try:
        data = request.json
        
        # Get login identifier (can be username or email)
        identifier = data.get('email') or data.get('username') or data.get('identifier')
        password = data.get('password')
        
        # Validate required fields
        if not identifier:
            return jsonify({'error': 'Username or email is required'}), 400
        if not password:
            return jsonify({'error': 'Password is required'}), 400
        
        # Try to find user by email first, then by username
        user = User.query.filter_by(email=identifier).first()
        if not user:
            user = User.query.filter_by(username=identifier).first()
        
        if not user:
            return jsonify({'error': 'Invalid username/email or password'}), 401
        
        # Check password
        if not user.check_password(password):
            return jsonify({'error': 'Invalid username/email or password'}), 401
        
        # Create access token
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(days=1)
        )
        
        return jsonify({
            'message': 'Login successful',
            'token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        print(f"Login error: {str(e)}")  # Debug logging
        import traceback
        traceback.print_exc()  # Print full stack trace
        return jsonify({'error': f'Login failed: {str(e)}'}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        print(f"Profile error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/update-profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.json
        
        # Update username if provided
        if 'username' in data and data['username']:
            # Check if username is already taken by another user
            existing = User.query.filter_by(username=data['username']).first()
            if existing and existing.id != user_id:
                return jsonify({'error': 'Username already taken'}), 400
            user.username = data['username']
        
        # Update email if provided
        if 'email' in data and data['email']:
            # Check if email is already taken by another user
            existing = User.query.filter_by(email=data['email']).first()
            if existing and existing.id != user_id:
                return jsonify({'error': 'Email already registered'}), 400
            user.email = data['email']
        
        # Update password if provided
        if 'password' in data and data['password']:
            user.set_password(data['password'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Update profile error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/preferences', methods=['PATCH'])
@jwt_required()
def update_preferences():
    """Update user preferences"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.json
        
        # Update preferences
        if 'preferences' in data:
            user.preferences = data['preferences']
        else:
            # Update individual preference fields
            if not user.preferences:
                user.preferences = {}
            
            for key, value in data.items():
                user.preferences[key] = value
        
        db.session.commit()
        
        return jsonify({
            'message': 'Preferences updated successfully',
            'preferences': user.preferences
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Update preferences error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/verify', methods=['GET'])
@jwt_required()
def verify_token():
    """Verify if token is valid"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'valid': True,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)}), 401