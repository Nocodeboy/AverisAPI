# AverisAPI - Main application entry point

import os
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from api.routes import register_routes
from api.middleware import authenticate, setup_middleware
import tempfile

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask application
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Create temp directory if it doesn't exist
os.makedirs("temp/uploads", exist_ok=True)
os.makedirs("temp/output", exist_ok=True)

# Basic routes
@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        "status": "ok",
        "name": "AverisAPI",
        "version": os.environ.get('API_VERSION', '0.1.0')
    })

@app.route('/info', methods=['GET'])
def api_info():
    """Provides information about the API capabilities"""
    return jsonify({
        "name": "AverisAPI",
        "version": os.environ.get('API_VERSION', '0.1.0'),
        "description": "Advanced API for multimedia processing, video effects, and voice translation",
        "documentation": "/docs",
        "endpoints": {
            "video": {
                "prefix": "/video",
                "description": "Video processing capabilities",
                "operations": [
                    "apply_effect", "add_transition", "enhance", 
                    "apply_overlay", "timelapse", "cinematic_bars",
                    "dream_effect", "rgb_split", "vhs_effect", "ken_burns"
                ]
            },
            "voice": {
                "prefix": "/voice",
                "description": "Voice processing capabilities",
                "operations": [
                    "text_to_speech", "translate", "transcribe", "languages"
                ]
            },
            "storage": {
                "prefix": "/storage",
                "description": "Storage operations",
                "operations": [
                    "upload", "download", "list", "delete"
                ]
            }
        }
    })

@app.route('/docs', methods=['GET'])
def docs():
    """API documentation"""
    # In a production environment, this would serve Swagger/OpenAPI documentation
    return jsonify({
        "message": "API documentation is available in the /docs directory of the project",
        "github": "https://github.com/Nocodeboy/AverisAPI"
    })

@app.route('/upload', methods=['POST'])
@authenticate
def upload_file():
    """Upload a file for processing"""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
        
    if file:
        # Generate a unique filename
        filename = os.path.join("temp/uploads", f"{next(tempfile._get_candidate_names())}_{file.filename}")
        file.save(filename)
        
        return jsonify({
            "message": "File uploaded successfully",
            "file_path": filename
        })

def initialize_app():
    """Initialize application components"""
    logger.info("Initializing AverisAPI...")
    
    # Setup middleware
    setup_middleware(app)
    
    # Register all routes
    register_routes(app)
    
    # Check for API key
    api_key = os.environ.get('API_KEY')
    if not api_key:
        logger.warning("API_KEY not set. Using default value for development.")
        os.environ['API_KEY'] = 'dev_key_not_secure'
    
    logger.info("AverisAPI initialization complete")
    return app

if __name__ == '__main__':
    app = initialize_app()
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting AverisAPI on port {port}, debug mode: {debug}")
    app.run(host='0.0.0.0', port=port, debug=debug)
