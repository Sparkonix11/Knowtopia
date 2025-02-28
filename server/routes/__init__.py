from .auth import auth_api_bp
from .course import course_api_bp

def init_routes(app):
    app.register_blueprint(auth_api_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(course_api_bp, url_prefix='/api/v1/course')
    # app.register_blueprint(assignment_api_bp, url_prefix='/api/v1/assignment')
    # app.register_blueprint(question_api_bp, url_prefix='/api/v1/question')
    # app.register_blueprint(review_api_bp, url_prefix='/api/v1/review')