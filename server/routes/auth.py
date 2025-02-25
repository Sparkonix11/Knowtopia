from flask import Blueprint, request, jsonify, session
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_api_bp = Blueprint('auth_api', __name__)

@auth_api_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.form
        required_fields = ['email', 'password', 'fname', 'lname', 'password_confirm']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if data['password'] != data['password_confirm']:
            return jsonify({'error': 'Passwords do not match'}), 400
        
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'User already exists'}), 400
        
        is_instructor_value = data.get('is_instructor', 'false').lower() == 'true'

        
        new_user = User(
            email=data['email'],
            password=generate_password_hash(data['password'], method='pbkdf2:sha256'),
            fname=data['fname'],
            lname=data['lname'],
            is_instructor=is_instructor_value,
            phone=data.get('phone', None)
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user, remember=True)

        user_data = {
            'id': new_user.id,
            'email': new_user.email,
            'fname': new_user.fname,
            'lname': new_user.lname,
            'is_instructor': new_user.is_instructor,
            'image': new_user.image
        }

        return jsonify({'message': 'User created', 'user': user_data}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create user: {str(e)}'}), 500

@auth_api_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.form
        required_fields = ['email', 'password']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'error': 'Invalid credentials'}), 400
        
        login_user(user, remember=True)

        user_data = {
            'id': user.id,
            'email': user.email,
            'fname': user.fname,
            'lname': user.lname,
            'is_instructor': user.is_instructor,
            'image': user.image
        }

        return jsonify({'message': 'User logged in', 'user': user_data}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to log in: {str(e)}'}), 500
    
@auth_api_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    try:
        logout_user()
        return jsonify({'message': 'User logged out'}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to log out: {str(e)}'}), 500