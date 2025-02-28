from flask import Blueprint, request, jsonify
from models import db, Material, Week
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads/materials"
ALLOWED_EXTENSIONS = {"pdf", "mp4", "jpg", "png", "txt"}

material_api_bp = Blueprint('material_api', __name__)

@material_api_bp.route('/weeks/<int:week_id>/create_material', methods=['POST'])
@login_required
def create_material(week_id):
    try:
        if not current_user.is_instructor:
            return jsonify({'error': 'User is not an instructor'}), 403
        week = Week.query.filter_by(id=week_id).first()
        if not week:
            return jsonify({'error": "Invalid week_id'}), 404
        
        data = request.form
        required_fields = ['name', 'duration']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        existing_material = Material.query.filter_by(name=data['name'], week_id=week_id).first()
        if existing_material:
            return jsonify({'error': 'Material already exists'}), 400
        
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        # Validate file extension
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit(".", 1)[-1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            return jsonify({"error": "File type not allowed"}), 400

        # Save file to upload folder
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        
        new_material = Material(
            name=data['name'],
            duration=data['duration'],
            week_id=week_id,
            filename=filename

        )

        db.session.add(new_material)
        db.session.commit()

        material_data = {
            'id': new_material.id,
            'name': new_material.name,
            'duration': new_material.duration,
        }

        return jsonify({'message': 'Material created', 'material': material_data}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create material: {str(e)}'}), 500
    
@material_api_bp.route('/delete_material/<int:material_id>', methods=['DELETE'])
@login_required
def delete_material(material_id):
    try:
        material = Material.query.get(material_id)
        if not material:
            return jsonify({'error': 'Material not found'}), 404
        
        week = Week.query.get(material.week_id)
        if not week:
            return jsonify({'error': 'Week not found'}), 404
        
        if not current_user.is_instructor:
            return jsonify({'error': 'User is not an instructor'}), 403
        
        if not week.course.creator_user_id == current_user.id:
            return jsonify({'error': 'User is not the creator of the course'}), 403
        
        db.session.delete(material)
        db.session.commit()
        
        return jsonify({'message': 'Material deleted'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete material: {str(e)}'}), 500