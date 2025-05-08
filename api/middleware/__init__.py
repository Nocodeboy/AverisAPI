# Middleware initialization

from flask import Flask, request, jsonify, g
import time
import os
from functools import wraps

def authenticate(f):
    """Authentication middleware"""
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        expected_api_key = os.environ.get('API_KEY')
        
        if not api_key or api_key != expected_api_key:
            return jsonify({"error": "Unauthorized"}), 401
        
        return f(*args, **kwargs)
    return decorated

def request_logger(app):
    """Log request information"""
    @app.before_request
    def before_request():
        g.start_time = time.time()
    
    @app.after_request
    def after_request(response):
        diff = time.time() - g.start_time
        app.logger.info(
            f"Request: {request.method} {request.path} {response.status_code} - {diff:.4f}s"
        )
        return response

def setup_middleware(app: Flask):
    """Setup all middleware"""
    request_logger(app)
    
    # Add more middleware as needed
    
    return app
