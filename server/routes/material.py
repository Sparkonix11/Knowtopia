from flask import request
from flask_restful import Resource, reqparse
from models import db, Material, Week
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads/materials"
ALLOWED_EXTENSIONS = {"pdf", "mp4", "jpg", "png", "txt"}

class MaterialResource(Resource):
    @login_required
    def post(self, week_id):
        try:
            if not current_user.is_instructor:
                return {'error': 'User is not an instructor'}, 403
            
            week = Week.query.get(week_id)
            if not week:
                return {'error': 'Invalid week_id'}, 404
            
            parser = reqparse.RequestParser()
            parser.add_argument('name', required=True, help='Name is required')
            parser.add_argument('duration', required=True, help='Duration is required')
            args = parser.parse_args()
            
            if Material.query.filter_by(name=args['name'], week_id=week_id).first():
                return {'error': 'Material already exists'}, 400
            
            if 'file' not in request.files:
                return {'error': 'No file uploaded'}, 400
            
            file = request.files['file']
            if file.filename == "":
                return {'error': 'No selected file'}, 400
            
            filename = secure_filename(file.filename)
            file_ext = filename.rsplit(".", 1)[-1].lower()
            if file_ext not in ALLOWED_EXTENSIONS:
                return {'error': 'File type not allowed'}, 400
            
            new_material = Material(
                name=args['name'],
                duration=args['duration'],
                week_id=week_id,
                filename=filename
            )
            
            db.session.add(new_material)
            db.session.flush()
            
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            
            material_filename = secure_filename(f"{new_material.id}.{file_ext}")
            new_material_path = os.path.join(UPLOAD_FOLDER, material_filename)
            file.save(new_material_path)
            new_material.file_path = f"/uploads/materials/{material_filename}"
            
            db.session.commit()
            
            return {'message': 'Material created', 'material': {
                'id': new_material.id,
                'name': new_material.name,
                'duration': new_material.duration,
            }}, 201
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to create material: {str(e)}'}, 500
    
class MaterialDeleteResource(Resource):
    @login_required
    def delete(self, material_id):
        try:
            material = Material.query.get(material_id)
            if not material:
                return {'error': 'Material not found'}, 404
            
            week = Week.query.get(material.week_id)
            if not week:
                return {'error': 'Week not found'}, 404
            
            if not current_user.is_instructor:
                return {'error': 'User is not an instructor'}, 403
            
            if week.user_id != current_user.id:
                return {'error': 'User is not the creator of the course'}, 403
            
            db.session.delete(material)
            db.session.commit()
            
            return {'message': 'Material deleted'}, 200
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to delete material: {str(e)}'}, 500
