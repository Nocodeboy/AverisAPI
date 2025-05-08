# AverisAPI - Main application entry point

from flask import Flask, jsonify
from api.routes import register_routes
from api.middleware import setup_middleware
from core.video import init_video_processors
from core.audio import init_audio_processors
from core.voice import init_voice_processors
from core.storage import init_storage
import os

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        "status": "ok",
        "name": "AverisAPI",
        "version": "0.1.0"
    })

def initialize_app():
    """Initialize application components"""
    # Setup middleware
    setup_middleware(app)
    
    # Register all routes
    register_routes(app)
    
    # Initialize core components
    init_video_processors()
    init_audio_processors()
    init_voice_processors()
    init_storage()
    
    return app

if __name__ == '__main__':
    app = initialize_app()
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
