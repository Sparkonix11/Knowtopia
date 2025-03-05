from .auth import auth_api_bp
from .course import course_api_bp
from .assignment import assignment_api_bp
from .question import question_api_bp
from .review import review_api_bp
from .material import material_api_bp
from .week import week_api_bp
from .ai import ai_api_bp

def init_routes(app):
    app.register_blueprint(auth_api_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(course_api_bp, url_prefix='/api/v1/course')
    app.register_blueprint(assignment_api_bp, url_prefix='/api/v1/assignment')
    app.register_blueprint(question_api_bp, url_prefix='/api/v1/question')
    app.register_blueprint(review_api_bp, url_prefix='/api/v1/review')
    app.register_blueprint(material_api_bp, url_prefix='/api/v1/material')
    app.register_blueprint(week_api_bp, url_prefix='/api/v1/week')
    app.register_blueprint(ai_api_bp, url_prefix='/api/v1/ai')