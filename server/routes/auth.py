from flask import request
from flask_restful import Resource
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

def get_user_data(user):
    return {
        'id': user.id,
        'email': user.email,
        'fname': user.fname,
        'lname': user.lname,
        'is_instructor': user.is_instructor,
        'image': user.image,
        'dob': user.dob.isoformat() if user.dob else None,
        'phone': user.phone,
        'gender': user.gender,
        'about': user.about
    }


class SignupResource(Resource):
    def post(self):
        try:
            data = request.form
            required_fields = ['email', 'password', 'fname', 'lname', 'password_confirm']
            if not all(field in data for field in required_fields):
                return {'error': 'Missing required fields'}, 400

            if data['password'] != data['password_confirm']:
                return {'error': 'Passwords do not match'}, 400

            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user:
                return {'error': 'User already exists'}, 400

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
            
            return {
                'message': 'User created successfully',
                'user': get_user_data(new_user)
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to create user: {str(e)}'}, 500


class LoginResource(Resource):
    def post(self):
        try:
            data = request.form
            
            if not data.get('email') or not data.get('password'):
                return {'error': 'Email and password are required'}, 400
                
            user = User.query.filter_by(email=data['email']).first()
            
            if not user or not check_password_hash(user.password, data['password']):
                return {'error': 'Invalid credentials'}, 401
                
            login_user(user, remember=True)
            
            return {
                'message': 'Login successful',
                'user': get_user_data(user)
            }, 200
            
        except Exception as e:
            return {'error': f'Login failed: {str(e)}'}, 500


class LogoutResource(Resource):
    @login_required
    def post(self):
        try:
            logout_user()
            return {'message': 'Logout successful'}, 200
        except Exception as e:
            return {'error': f'Logout failed: {str(e)}'}, 500