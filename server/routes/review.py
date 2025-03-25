from flask import request, jsonify
from flask_restful import Resource
from models import db, Review, Material, Week, Course, User
from flask_login import login_required, current_user
from sqlalchemy import and_

class ReviewResource(Resource):
    @login_required
    def post(self, material_id):
        try:
            data = request.form
            required_fields = ['rating', 'comment']
            if not all(field in data for field in required_fields):
                return {'error': 'Missing required fields'}, 400
            
            existing_review = Review.query.filter_by(user_id=current_user.id, material_id=material_id).first()
            if existing_review:
                return {'error': 'Review already exists'}, 400
            
            material = Material.query.filter_by(id=material_id).first()
            if not material:
                return {'error': 'Material not found'}, 404
            
            if int(data['rating']) < 1 or int(data['rating']) > 5:
                return {'error': 'Rating must be between 1 and 5'}, 400
            
            new_review = Review(
                rating=data['rating'],
                comment=data['comment'],
                user_id=current_user.id,
                material_id=material_id
            )

            db.session.add(new_review)
            db.session.commit()

            review_data = {
                'id': new_review.id,
                'rating': new_review.rating,
                'comment': new_review.comment,
                'user_id': new_review.user_id,
                'material_id': new_review.material_id
            }

            return {'message': 'Review created', 'review': review_data}, 201
        
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to create review: {str(e)}'}, 500

class ReviewDeleteResource(Resource):
    @login_required
    def delete(self, review_id):
        try:
            review = Review.query.filter_by(id=review_id, user_id=current_user.id).first()
            
            if not review:
                return {'error': 'Review not found or unauthorized'}, 404
            
            db.session.delete(review)
            db.session.commit()
            
            return {'message': 'Review deleted successfully'}, 200
        
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to delete review: {str(e)}'}, 500

class InstructorReviewsResource(Resource):
    @login_required
    def get(self):
        try:
            if not current_user.is_instructor:
                return {'error': 'Access denied. Only instructors can access this endpoint'}, 403
            
            # Find all courses created by the current instructor
            instructor_courses = Course.query.filter_by(creator_user_id=current_user.id).all()
            
            if not instructor_courses:
                return {'message': 'No courses found for this instructor', 'reviews': []}, 200
            
            course_ids = [course.id for course in instructor_courses]
            
            # Find all weeks in these courses
            weeks = Week.query.filter(Week.course_id.in_(course_ids)).all()
            
            if not weeks:
                return {'message': 'No weeks found in instructor courses', 'reviews': []}, 200
            
            week_ids = [week.id for week in weeks]
            
            # Find all materials in these weeks
            materials = Material.query.filter(Material.week_id.in_(week_ids)).all()
            
            if not materials:
                return {'message': 'No materials found in instructor courses', 'reviews': []}, 200
            
            material_ids = [material.id for material in materials]
            
            # Find all reviews for these materials
            reviews = Review.query.filter(Review.material_id.in_(material_ids)).all()
            
            if not reviews:
                return {'message': 'No reviews found for instructor materials', 'reviews': []}, 200
            
            # Get user information for each review
            review_data = []
            for review in reviews:
                user = User.query.get(review.user_id)
                material = Material.query.get(review.material_id)
                week = Week.query.get(material.week_id)
                course = Course.query.get(week.course_id)
                
                review_info = {
                    'id': review.id,
                    'rating': review.rating,
                    'comment': review.comment,
                    'user_id': review.user_id,
                    'username': f"{user.fname} {user.lname}" if user else "Unknown User",
                    'user_image': user.image,
                    'material_id': review.material_id,
                    'material_name': material.name if material else "Unknown Material",
                    'course_id': course.id if course else None,
                    'course_name': course.name if course else "Unknown Course"
                }
                review_data.append(review_info)
            
            return {'reviews': review_data}, 200
        
        except Exception as e:
            return {'error': f'Failed to retrieve instructor reviews: {str(e)}'}, 500

