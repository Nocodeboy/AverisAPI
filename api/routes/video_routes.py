# Video processing routes

from flask import Blueprint, request, jsonify
from core.video.effects import VideoEffects
from api.validators.video_validators import validate_effect_request, validate_transition_request, validate_enhance_request

video_bp = Blueprint('video', __name__, url_prefix='/video')

@video_bp.route('/apply_effect', methods=['POST'])
def apply_effect():
    """Apply visual effect to video
    
    Request body:
        input_path: Path to input video file
        output_path: Path where output video will be saved
        effect_type: Type of effect to apply (grayscale, sepia, vintage, etc.)
        intensity: Intensity of the effect (0.0 to 1.0)
    """
    data = request.json
    validation = validate_effect_request(data)
    
    if validation.get('error'):
        return jsonify(validation), 400
    
    try:
        output_path = VideoEffects.apply_color_filter(
            data['input_path'],
            data['output_path'],
            data['effect_type'],
            data.get('intensity', 1.0)
        )
        
        return jsonify({
            "status": "success",
            "output_path": output_path
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@video_bp.route('/add_transition', methods=['POST'])
def add_transition():
    """Add transition between two videos
    
    Request body:
        input1: Path to first video
        input2: Path to second video
        output_path: Path where output video will be saved
        transition_type: Type of transition (fade, wipe, zoom, etc.)
        duration: Duration of transition in seconds
    """
    data = request.json
    validation = validate_transition_request(data)
    
    if validation.get('error'):
        return jsonify(validation), 400
    
    try:
        output_path = VideoEffects.add_transition(
            data['input1'],
            data['input2'],
            data['output_path'],
            data['transition_type'],
            data.get('duration', 1.0)
        )
        
        return jsonify({
            "status": "success",
            "output_path": output_path
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@video_bp.route('/enhance', methods=['POST'])
def enhance_video():
    """Enhance video quality
    
    Request body:
        input_path: Path to input video file
        output_path: Path where output video will be saved
        denoise: Apply denoising filter (boolean)
        sharpen: Apply sharpening filter (boolean)
        brightness: Brightness adjustment (-1.0 to 1.0)
        contrast: Contrast adjustment (-1.0 to 1.0)
    """
    data = request.json
    validation = validate_enhance_request(data)
    
    if validation.get('error'):
        return jsonify(validation), 400
    
    try:
        output_path = VideoEffects.enhance_video(
            data['input_path'],
            data['output_path'],
            data.get('denoise', False),
            data.get('sharpen', False),
            data.get('brightness', 0.0),
            data.get('contrast', 0.0)
        )
        
        return jsonify({
            "status": "success",
            "output_path": output_path
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
