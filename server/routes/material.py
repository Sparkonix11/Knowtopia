from flask import request
from flask_restful import Resource
from models import db, Material, Week
from flask_login import login_required, current_user
import os
import torch
import whisper
from fpdf import FPDF
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads/materials"
TRANSCRIPT_FOLDER = "uploads/transcripts"
ALLOWED_EXTENSIONS = {"pdf", "mp4", "jpg", "png", "txt"}

class MaterialCreateResource(Resource):
    @login_required
    def post(self, week_id):
        try:
            if not current_user.is_instructor:
                return {'error': 'User is not an instructor'}, 403
            
            week = Week.query.get(week_id)
            if not week:
                return {'error': 'Invalid week_id'}, 404
            
            data = request.form
            
            if Material.query.filter_by(name=data['name'], week_id=week_id).first():
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
                name=data['name'],
                duration=data['duration'],
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
            new_material.filename = material_filename
            
            transcript_file_path = None

            # If the uploaded file is a video, generate transcript
            if file_ext == "mp4":
                if not os.path.exists(TRANSCRIPT_FOLDER):
                    os.makedirs(TRANSCRIPT_FOLDER)

                transcript_text = self.generate_transcript(new_material_path)
                if transcript_text:
                    transcript_filename = f"{new_material.id}.pdf"
                    transcript_file_path = os.path.join(TRANSCRIPT_FOLDER, transcript_filename)
                    self.save_transcript_as_pdf(transcript_text, transcript_file_path)
                    new_material.transcript_path = f"/uploads/transcripts/{transcript_filename}"

            db.session.commit()

            return {
                'message': 'Material created',
                'material': {
                    'id': new_material.id,
                    'name': new_material.name,
                    'duration': new_material.duration,
                    'transcript_path': new_material.transcript_path if transcript_file_path else None
                }
            }, 201
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to create material: {str(e)}'}, 500

    def generate_transcript(self, video_path):
        try:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            model = whisper.load_model("base", device=device)  # Load Whisper model on GPU if available
            result = model.transcribe(video_path)
            return result["text"]
        except Exception as e:
            print(f"Error in transcription: {str(e)}")
            return None

    def save_transcript_as_pdf(self, text, pdf_path):
        try:
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, text)
            pdf.output(pdf_path)
        except Exception as e:
            print(f"Error saving transcript PDF: {str(e)}")

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
