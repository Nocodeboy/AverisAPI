# Validators for video processing endpoints

from typing import Dict, Any
import os

def validate_effect_request(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate request data for apply_effect endpoint"""
    if not data.get('input_path'):
        return {"error": "input_path is required"}
    
    if not data.get('output_path'):
        return {"error": "output_path is required"}
    
    if not data.get('effect_type'):
        return {"error": "effect_type is required"}
    
    valid_effects = ["grayscale", "sepia", "vintage", "vibrant"]
    if data.get('effect_type') not in valid_effects:
        return {
            "error": f"Invalid effect_type. Must be one of: {', '.join(valid_effects)}"
        }
    
    if 'intensity' in data:
        intensity = data.get('intensity')
        if not isinstance(intensity, (int, float)) or intensity < 0 or intensity > 1:
            return {"error": "intensity must be a number between 0.0 and 1.0"}
    
    if not os.path.isfile(data.get('input_path')):
        return {"error": "input_path does not exist or is not a file"}
    
    return {}

def validate_transition_request(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate request data for add_transition endpoint"""
    if not data.get('input1'):
        return {"error": "input1 is required"}
    
    if not data.get('input2'):
        return {"error": "input2 is required"}
    
    if not data.get('output_path'):
        return {"error": "output_path is required"}
    
    if not data.get('transition_type'):
        return {"error": "transition_type is required"}
    
    valid_transitions = [
        "fade", "wipe_left", "wipe_right", "wipe_up", "wipe_down", 
        "slide_left", "slide_right", "zoom_in", "zoom_out"
    ]
    
    if data.get('transition_type') not in valid_transitions:
        return {
            "error": f"Invalid transition_type. Must be one of: {', '.join(valid_transitions)}"
        }
    
    if 'duration' in data:
        duration = data.get('duration')
        if not isinstance(duration, (int, float)) or duration <= 0:
            return {"error": "duration must be a positive number"}
    
    if not os.path.isfile(data.get('input1')):
        return {"error": "input1 does not exist or is not a file"}
    
    if not os.path.isfile(data.get('input2')):
        return {"error": "input2 does not exist or is not a file"}
    
    return {}

def validate_enhance_request(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate request data for enhance_video endpoint"""
    if not data.get('input_path'):
        return {"error": "input_path is required"}
    
    if not data.get('output_path'):
        return {"error": "output_path is required"}
    
    if 'denoise' in data and not isinstance(data.get('denoise'), bool):
        return {"error": "denoise must be a boolean"}
    
    if 'sharpen' in data and not isinstance(data.get('sharpen'), bool):
        return {"error": "sharpen must be a boolean"}
    
    if 'brightness' in data:
        brightness = data.get('brightness')
        if not isinstance(brightness, (int, float)) or brightness < -1 or brightness > 1:
            return {"error": "brightness must be a number between -1.0 and 1.0"}
    
    if 'contrast' in data:
        contrast = data.get('contrast')
        if not isinstance(contrast, (int, float)) or contrast < -1 or contrast > 1:
            return {"error": "contrast must be a number between -1.0 and 1.0"}
    
    if not os.path.isfile(data.get('input_path')):
        return {"error": "input_path does not exist or is not a file"}
    
    return {}
