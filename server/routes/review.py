from flask import request, jsonify
from flask_restful import Resource
from models import db, Review, Material
from flask_login import login_required, current_user

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

