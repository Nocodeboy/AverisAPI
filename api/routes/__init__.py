# Routes initialization

import logging
from flask import Flask
from .video_routes import video_bp
from .video_advanced_routes import video_advanced_bp
from .voice_routes import voice_bp
from .voice_enhanced_routes import voice_enhanced_bp

logger = logging.getLogger(__name__)

def register_routes(app: Flask):
    """Register all blueprint routes"""
    logger.info("Registering API routes...")
    
    # Basic video processing routes
    app.register_blueprint(video_bp)
    logger.info("Registered basic video routes under /video")
    
    # Advanced video processing routes
    app.register_blueprint(video_advanced_bp)
    logger.info("Registered advanced video routes under /video")
    
    # Basic voice processing routes
    app.register_blueprint(voice_bp)
    logger.info("Registered basic voice routes under /voice")
    
    # Enhanced voice processing routes
    app.register_blueprint(voice_enhanced_bp)
    logger.info("Registered enhanced voice routes under /voice")
    
    # Additional route registration can be added here
    
    logger.info("Route registration complete")
    return app
