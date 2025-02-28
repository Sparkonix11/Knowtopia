from flask import Blueprint, request, jsonify
from models import db, Review
from flask_login import login_required, current_user

review_api_bp = Blueprint('review_api', __name__)

@review_api_bp.route('/materials/<int:material_id>/review', methods=['POST'])
@login_required
def create_review(material_id):
    try:
        data = request.form
        required_fields = ['rating', 'comment']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        existing_review = Review.query.filter_by(user_id=current_user.id, material_id=material_id).first()
        if existing_review:
            return jsonify({'error': 'Review already exists'}), 400
        
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

        return jsonify({'message': 'Review created', 'review': review_data}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create review: {str(e)}'}), 500