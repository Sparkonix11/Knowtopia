from flask import request
from flask_restful import Resource
from flask_login import login_required, current_user
from models import db, MaterialDoubt, Material, Week, Course
from sqlalchemy import func, desc

class MaterialDoubtCreateResource(Resource):
    @login_required
    def post(self, material_id):
        try:
            # Check if material exists
            material = Material.query.get(material_id)
            if not material:
                return {'error': 'Material not found'}, 404
            
            # Get data from request
            data = request.get_json()
            if not data or 'doubt_text' not in data:
                return {'error': 'Doubt text is required'}, 400
            
            # Create new doubt
            new_doubt = MaterialDoubt(
                material_id=material_id,
                student_id=current_user.id,
                doubt_text=data['doubt_text']
            )
            
            db.session.add(new_doubt)
            db.session.commit()
            
            return {'message': 'Doubt created successfully', 'doubt_id': new_doubt.id}, 201
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to create doubt: {str(e)}'}, 500

class MaterialDoubtsResource(Resource):
    @login_required
    def get(self, material_id):
        try:
            # Check if material exists
            material = Material.query.get(material_id)
            if not material:
                return {'error': 'Material not found'}, 404
            
            # Get all doubts for this material
            doubts = MaterialDoubt.query.filter_by(material_id=material_id).all()
            
            # Format doubts data
            doubts_data = [{
                'id': doubt.id,
                'student_id': doubt.student_id,
                'student_name': doubt.student.name if hasattr(doubt.student, 'name') else 'Unknown',
                'doubt_text': doubt.doubt_text,
                'created_at': doubt.created_at.isoformat()
            } for doubt in doubts]
            
            return {'material_id': material_id, 'doubts': doubts_data}, 200
        except Exception as e:
            return {'error': f'Failed to retrieve doubts: {str(e)}'}, 500

class AllMaterialDoubtsResource(Resource):
    @login_required
    def get(self):
        try:
            # Check if user is an instructor
            if not current_user.is_instructor:
                return {'error': 'Access denied. Only instructors can view all doubts'}, 403
            
            # Get all materials with their doubts count
            # Join with Material, Week, and Course to get course and week information
            materials_with_doubts = db.session.query(
                Material.id,
                Material.name,
                Week.id.label('week_id'),
                Week.name.label('week_name'),
                Course.id.label('course_id'),
                Course.name.label('course_name'),
                func.count(MaterialDoubt.id).label('doubts_count')
            ).join(
                MaterialDoubt, MaterialDoubt.material_id == Material.id, isouter=True
            ).join(
                Week, Week.id == Material.week_id
            ).join(
                Course, Course.id == Week.course_id
            ).filter(
                Course.creator_user_id == current_user.id
            ).group_by(
                Material.id
            ).having(
                func.count(MaterialDoubt.id) > 0
            ).order_by(
                desc('doubts_count')
            ).all()
            
            # Format materials data
            materials_data = [{
                'id': material.id,
                'name': material.name,
                'week_id': material.week_id,
                'week_name': material.week_name,
                'course_id': material.course_id,
                'course_name': material.course_name,
                'doubts_count': material.doubts_count
            } for material in materials_with_doubts]
            
            return {'materials': materials_data}, 200
        except Exception as e:
            return {'error': f'Failed to retrieve material doubts: {str(e)}'}, 500

class StudentDoubtsResource(Resource):
    @login_required
    def get(self):
        try:
            # Get all doubts for the current student grouped by day
            # for the last 10 days
            from datetime import datetime, timedelta
            
            # Calculate date 10 days ago
            ten_days_ago = datetime.now() - timedelta(days=10)
            
            # Query doubts count by day
            doubts_by_day = db.session.query(
                func.date(MaterialDoubt.created_at).label('date'),
                func.count(MaterialDoubt.id).label('count')
            ).filter(
                MaterialDoubt.student_id == current_user.id,
                MaterialDoubt.created_at >= ten_days_ago
            ).group_by(
                func.date(MaterialDoubt.created_at)
            ).all()
            
            # Create a dictionary with all days in the last 10 days
            doubts_data = {}
            for i in range(10):
                date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
                doubts_data[date] = 0
            
            # Fill in the actual counts
            for doubt in doubts_by_day:
                # Handle the date properly - it could be a string or a date object
                if hasattr(doubt.date, 'strftime'):
                    date_str = doubt.date.strftime('%Y-%m-%d')
                else:
                    # If it's already a string, use it directly
                    date_str = str(doubt.date)
                if date_str in doubts_data:
                    doubts_data[date_str] = doubt.count
            
            # Convert to list format for the frontend
            result = [{
                'date': date,
                'count': count
            } for date, count in doubts_data.items()]
            
            # Sort by date
            result.sort(key=lambda x: x['date'])
            
            return {'doubts_by_day': result}, 200
        except Exception as e:
            return {'error': f'Failed to retrieve student doubts: {str(e)}'}, 500