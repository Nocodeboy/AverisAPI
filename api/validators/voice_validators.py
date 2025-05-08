# Validators for voice processing endpoints

from typing import Dict, Any
import os
from core.voice.text_to_speech import TextToSpeech

def validate_tts_request(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate request data for text_to_speech endpoint"""
    if not data.get('text'):
        return {"error": "text is required"}
    
    if not data.get('output_path'):
        return {"error": "output_path is required"}
    
    if 'language' in data:
        languages = TextToSpeech.available_languages()
        if data.get('language') not in languages:
            return {
                "error": f"Invalid language code. See /voice/languages for valid options."
            }
    
    if 'slow' in data and not isinstance(data.get('slow'), bool):
        return {"error": "slow must be a boolean"}
    
    return {}

def validate_translate_request(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate request data for translate_audio endpoint"""
    if not data.get('input_path'):
        return {"error": "input_path is required"}
    
    if not data.get('output_path'):
        return {"error": "output_path is required"}
    
    if 'source_lang' in data and data.get('source_lang') != 'auto':
        languages = TextToSpeech.available_languages()
        if data.get('source_lang') not in languages:
            return {
                "error": f"Invalid source language code. Use 'auto' or see /voice/languages for valid options."
            }
    
    if 'target_lang' in data:
        languages = TextToSpeech.available_languages()
        if data.get('target_lang') not in languages:
            return {
                "error": f"Invalid target language code. See /voice/languages for valid options."
            }
    
    if not os.path.isfile(data.get('input_path')):
        return {"error": "input_path does not exist or is not a file"}
    
    return {}
