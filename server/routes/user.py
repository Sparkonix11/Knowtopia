from flask import request
from flask_restful import Resource
from flask_login import login_required, current_user
from models import db, User

def get_user_data(user):
    return {
        'id': user.id,
        'email': user.email,
        'fname': user.fname,
        'lname': user.lname,
        'is_instructor': user.is_instructor,
        'image': user.image
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
            
            if 'fname' in data:
                user.fname = data['fname']
            if 'lname' in data:
                user.lname = data['lname']
            if 'phone' in data:
                user.phone = data['phone']
                
            # if 'image' in request.files:
            #     image_file = request.files['image']
            #     if image_file.filename:
            #         # Here you would add code to save the image
            #         # For example: user.image = save_image(image_file)
            #         user.image = image_file.filename  # Placeholder for actual image handling
            
            db.session.commit()
            
            return {
                'message': 'Profile updated successfully',
                'user': get_user_data(user)
            }, 200
            
        except Exception as e:
            db.session.rollback()
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