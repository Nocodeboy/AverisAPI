# Voice processing routes

from flask import Blueprint, request, jsonify
from core.voice.text_to_speech import TextToSpeech
from core.voice.translator import VoiceTranslator
from api.validators.voice_validators import validate_tts_request, validate_translate_request

voice_bp = Blueprint('voice', __name__, url_prefix='/voice')

@voice_bp.route('/text_to_speech', methods=['POST'])
def text_to_speech():
    """Convert text to speech
    
    Request body:
        text: Text to convert to speech
        output_path: Path where output audio file will be saved
        language: Language code (e.g., 'en', 'es', 'fr')
        slow: Whether to speak slowly (boolean)
    """
    data = request.json
    validation = validate_tts_request(data)
    
    if validation.get('error'):
        return jsonify(validation), 400
    
    try:
        output_path = TextToSpeech.convert(
            data['text'],
            data['output_path'],
            data.get('language', 'en'),
            data.get('slow', False),
            data.get('voice_type', 'standard')
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

@voice_bp.route('/translate', methods=['POST'])
def translate_audio():
    """Translate audio from one language to another
    
    Request body:
        input_path: Path to input audio file
        output_path: Path where translated audio will be saved
        source_lang: Language code of source audio (or 'auto' for auto-detection)
        target_lang: Language code for target translation
    """
    data = request.json
    validation = validate_translate_request(data)
    
    if validation.get('error'):
        return jsonify(validation), 400
    
    try:
        translator = VoiceTranslator()
        result = translator.translate_audio(
            data['input_path'],
            data['output_path'],
            data.get('source_lang', 'auto'),
            data.get('target_lang', 'en')
        )
        
        if 'error' in result:
            return jsonify({
                "status": "error",
                "message": result['error']
            }), 500
        
        return jsonify({
            "status": "success",
            **result
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@voice_bp.route('/languages', methods=['GET'])
def get_languages():
    """Get available languages for text to speech"""
    try:
        languages = TextToSpeech.available_languages()
        return jsonify({
            "status": "success",
            "languages": languages
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
