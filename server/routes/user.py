from flask import request
from flask_restful import Resource
from flask_login import login_required, current_user
from models import db, User
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

PFP_FOLDER = "uploads/pfp"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
SECRET_KEY = "mysecretkey"

def get_user_data(user):
    return {
        'id': user.id,
        'email': user.email,
        'fname': user.fname,
        'lname': user.lname,
        'is_instructor': user.is_instructor,
        'image': user.image,
        'dob': user.dob.strftime("%d-%m-%Y") if user.dob else None,
        'phone': user.phone,
        'gender': user.gender,
        'about': user.about
    }

class UserProfileResource(Resource):
    @login_required
    def get(self):
        try:
            return {
                'user': get_user_data(current_user)
            }, 200
        except Exception as e:
            return {'error': f'Failed to get user profile: {str(e)}'}, 500
            
    @login_required
    def put(self):
        try:
            data = request.form
            user = User.query.get(current_user.id)
            
            user.fname = data.get('fname', user.fname)
            user.lname = data.get('lname', user.lname)
            user.phone = data.get('phone', user.phone)

            if(data.get('dob')):
                try:
                    user.dob = datetime.strptime(data.get('dob'), "%d-%m-%Y").date()
                except ValueError:
                    return {'error': 'Invalid date format. Please use DD-MM-YYYY.'}, 400
            if(data.get('gender')):
                user.gender = data.get('gender', user.gender)
            if(data.get('about')):
                user.about = data.get('about', user.about)

            if(data.get('new_password')):
                current_password = data.get('current_password')
                if not current_password:
                    return {'error': 'Current password is required'}, 400
                if not check_password_hash(user.password, current_password):
                    return {'error': 'Current password is incorrect'}, 400
                user.password = generate_password_hash(data['new_password'], method='pbkdf2:sha256')
                
                
            if 'image' in request.files:
                image_file = request.files['image']
                if image_file.filename:
                    filename = secure_filename(image_file.filename)
                    file_ext = filename.rsplit(".", 1)[-1].lower()
                    if file_ext not in ALLOWED_EXTENSIONS:
                        return {'error': 'File type not allowed'}, 400
                    
                    if not os.path.exists(PFP_FOLDER):
                        os.makedirs(PFP_FOLDER)
                    
                    image_filename = secure_filename(f"{user.id}.{file_ext}")
                    image_path = os.path.join(PFP_FOLDER, image_filename)
                    image_file.save(image_path)
                    user.image = f"/{PFP_FOLDER}/{image_filename}"

            
            db.session.commit()
            
            return {
                'message': 'Profile updated successfully',
                'user': get_user_data(user)
            }, 200
            
        except Exception as e:
            db.session.rollback()
            print(e)
            return {'error': f'Failed to update profile: {str(e)}'}, 500

class UserStudentListResource(Resource):
    @login_required
    def get(self):
        try:
            if not current_user.is_instructor:
                return {'error': 'Access denied. Only instructors can view students'}, 403
            
            students = User.query.filter_by(is_instructor=False).all()
            students_data = [get_user_data(student) for student in students]
            
            return {
                'students': students_data
            }, 200
        except Exception as e:
            return {'error': f'Failed to get students: {str(e)}'}, 500

class DeleteUserResource(Resource):
    def delete(self, user_id):
        try:
            data = request.form
            provided_secret_key = data.get("secret_key")
            
            if provided_secret_key != SECRET_KEY:
                return {'error': 'Unauthorized request'}, 403
            
            user = User.query.get(user_id)
            if not user:
                return {'error': 'User not found'}, 404
            
            # Delete profile image if exists
            # if user.image:
            #     image_path = user.image.lstrip("/")
            #     if os.path.exists(image_path):
            #         os.remove(image_path)
            
            db.session.delete(user)
            db.session.commit()
            
            return {'message': 'User deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to delete user: {str(e)}'}, 500
