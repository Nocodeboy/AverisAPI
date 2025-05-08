# Routes initialization

from flask import Flask
from .video_routes import video_bp
from .voice_routes import voice_bp

def register_routes(app: Flask):
    """Register all blueprint routes"""
    app.register_blueprint(video_bp)
    app.register_blueprint(voice_bp)
    
    # Register other blueprints as needed
    
    return app
