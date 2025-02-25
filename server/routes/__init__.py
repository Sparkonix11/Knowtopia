from .auth import auth_api_bp

def init_routes(app):
    app.register_blueprint(auth_api_bp, url_prefix='/api/v1/auth')