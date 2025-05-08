# Advanced video processing routes

import os
import logging
from flask import Blueprint, request, jsonify
from core.video.effects_advanced import AdvancedVideoEffects
from api.middleware import authenticate

logger = logging.getLogger(__name__)

video_advanced_bp = Blueprint('video_advanced', __name__, url_prefix='/video')

@video_advanced_bp.route('/apply_overlay', methods=['POST'])
@authenticate
def apply_overlay():
    """Apply overlay to video (e.g., logo, watermark)
    
    Request body:
        video_path: Path to input video file
        overlay_path: Path to overlay image
        output_path: Path where output video will be saved
        position: Position of overlay (top-left, top-right, bottom-left, bottom-right, center)
        opacity: Opacity of overlay (0.0 to 1.0)
    """
    data = request.json
    
    # Validate required fields
    required_fields = ['video_path', 'overlay_path', 'output_path']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Validate file existence
    if not os.path.isfile(data['video_path']):
        return jsonify({"error": "Video file not found"}), 404
        
    if not os.path.isfile(data['overlay_path']):
        return jsonify({"error": "Overlay image not found"}), 404
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(data['output_path']), exist_ok=True)
        
        # Apply overlay effect
        result = AdvancedVideoEffects.apply_overlay(
            data['video_path'],
            data['overlay_path'],
            data['output_path'],
            position=data.get('position', 'top-right'),
            opacity=data.get('opacity', 0.7)
        )
        
        return jsonify({
            "status": "success",
            "output_path": result
        })
    except Exception as e:
        logger.error(f"Error applying overlay: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@video_advanced_bp.route('/timelapse', methods=['POST'])
@authenticate
def apply_timelapse():
    """Convert video to timelapse
    
    Request body:
        video_path: Path to input video file
        output_path: Path where output video will be saved
        speed_factor: How much to speed up the video (e.g., 10.0 = 10x speed)
    """
    data = request.json
    
    # Validate required fields
    required_fields = ['video_path', 'output_path']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Validate file existence
    if not os.path.isfile(data['video_path']):
        return jsonify({"error": "Video file not found"}), 404
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(data['output_path']), exist_ok=True)
        
        # Apply timelapse effect
        result = AdvancedVideoEffects.apply_timelapse(
            data['video_path'],
            data['output_path'],
            speed_factor=data.get('speed_factor', 10.0)
        )
        
        return jsonify({
            "status": "success",
            "output_path": result
        })
    except Exception as e:
        logger.error(f"Error creating timelapse: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@video_advanced_bp.route('/cinematic_bars', methods=['POST'])
@authenticate
def apply_cinematic_bars():
    """Add cinematic letterbox/bars effect to video
    
    Request body:
        video_path: Path to input video file
        output_path: Path where output video will be saved
        ratio: Aspect ratio (2.35:1, 2.39:1, 1.85:1, etc.)
    """
    data = request.json
    
    # Validate required fields
    required_fields = ['video_path', 'output_path']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Validate file existence
    if not os.path.isfile(data['video_path']):
        return jsonify({"error": "Video file not found"}), 404
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(data['output_path']), exist_ok=True)
        
        # Apply cinematic bars effect
        result = AdvancedVideoEffects.cinematic_bars(
            data['video_path'],
            data['output_path'],
            ratio=data.get('ratio', "2.35:1")
        )
        
        return jsonify({
            "status": "success",
            "output_path": result
        })
    except Exception as e:
        logger.error(f"Error applying cinematic bars: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@video_advanced_bp.route('/dream_effect', methods=['POST'])
@authenticate
def apply_dream_effect():
    """Apply dreamy/hazy effect to video
    
    Request body:
        video_path: Path to input video file
        output_path: Path where output video will be saved
        strength: Strength of effect (0.0 to 1.0)
    """
    data = request.json
    
    # Validate required fields
    required_fields = ['video_path', 'output_path']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Validate file existence
    if not os.path.isfile(data['video_path']):
        return jsonify({"error": "Video file not found"}), 404
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(data['output_path']), exist_ok=True)
        
        # Apply dream effect
        result = AdvancedVideoEffects.dream_effect(
            data['video_path'],
            data['output_path'],
            strength=data.get('strength', 0.5)
        )
        
        return jsonify({
            "status": "success",
            "output_path": result
        })
    except Exception as e:
        logger.error(f"Error applying dream effect: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@video_advanced_bp.route('/rgb_split', methods=['POST'])
@authenticate
def apply_rgb_split():
    """Apply RGB split/glitch effect
    
    Request body:
        video_path: Path to input video file
        output_path: Path where output video will be saved
        offset: Pixel offset for color channels
    """
    data = request.json
    
    # Validate required fields
    required_fields = ['video_path', 'output_path']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Validate file existence
    if not os.path.isfile(data['video_path']):
        return jsonify({"error": "Video file not found"}), 404
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(data['output_path']), exist_ok=True)
        
        # Apply RGB split effect
        result = AdvancedVideoEffects.rgb_split(
            data['video_path'],
            data['output_path'],
            offset=data.get('offset', 5)
        )
        
        return jsonify({
            "status": "success",
            "output_path": result
        })
    except Exception as e:
        logger.error(f"Error applying RGB split effect: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@video_advanced_bp.route('/vhs_effect', methods=['POST'])
@authenticate
def apply_vhs_effect():
    """Apply VHS/retro tape effect to video
    
    Request body:
        video_path: Path to input video file
        output_path: Path where output video will be saved
        intensity: Strength of effect (0.0 to 1.0)
    """
    data = request.json
    
    # Validate required fields
    required_fields = ['video_path', 'output_path']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Validate file existence
    if not os.path.isfile(data['video_path']):
        return jsonify({"error": "Video file not found"}), 404
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(data['output_path']), exist_ok=True)
        
        # Apply VHS effect
        result = AdvancedVideoEffects.vhs_effect(
            data['video_path'],
            data['output_path'],
            intensity=data.get('intensity', 0.7)
        )
        
        return jsonify({
            "status": "success",
            "output_path": result
        })
    except Exception as e:
        logger.error(f"Error applying VHS effect: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@video_advanced_bp.route('/ken_burns', methods=['POST'])
@authenticate
def apply_ken_burns():
    """Apply Ken Burns effect to an image (pan and zoom)
    
    Request body:
        image_path: Path to input image
        output_path: Path where output video will be saved
        duration: Duration of output video in seconds
        zoom_start: Initial zoom level
        zoom_end: Final zoom level
        direction: Direction of movement ("in", "out", "left", "right", "top", "bottom")
    """
    data = request.json
    
    # Validate required fields
    required_fields = ['image_path', 'output_path']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Validate file existence
    if not os.path.isfile(data['image_path']):
        return jsonify({"error": "Image file not found"}), 404
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(data['output_path']), exist_ok=True)
        
        # Apply Ken Burns effect
        result = AdvancedVideoEffects.apply_Ken_Burns(
            data['image_path'],
            data['output_path'],
            duration=data.get('duration', 10),
            zoom_start=data.get('zoom_start', 1.0),
            zoom_end=data.get('zoom_end', 1.5),
            direction=data.get('direction', 'in')
        )
        
        return jsonify({
            "status": "success",
            "output_path": result
        })
    except Exception as e:
        logger.error(f"Error applying Ken Burns effect: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
