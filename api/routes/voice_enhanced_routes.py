# Enhanced voice processing routes

import os
import logging
from flask import Blueprint, request, jsonify, send_file
from core.voice.translator_enhanced import EnhancedVoiceTranslator
from core.voice.text_to_speech import TextToSpeech
from api.middleware import authenticate

logger = logging.getLogger(__name__)

voice_enhanced_bp = Blueprint('voice_enhanced', __name__, url_prefix='/voice')

# Initialize translator on first use
_translator = None
def get_translator():
    global _translator
    if _translator is None:
        _translator = EnhancedVoiceTranslator()
    return _translator

@voice_enhanced_bp.route('/text_to_speech', methods=['POST'])
@authenticate
def text_to_speech():
    """Convert text to speech with enhanced features
    
    Request body:
        text: Text to convert to speech
        output_path: Path where output audio file will be saved
        language: Language code (e.g., 'en', 'es', 'fr')
        slow: Whether to speak slowly (boolean)
        voice_type: Type of voice to use
    """
    data = request.json
    
    # Validate required fields
    required_fields = ['text', 'output_path']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Validate text length
    if len(data['text']) > 10000:
        return jsonify({"error": "Text too long (max 10000 characters)"}), 400
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(data['output_path']), exist_ok=True)
        
        # Use enhanced TTS if available
        translator = get_translator()
        result = translator._text_to_speech(
            data['text'],
            data['output_path'],
            language=data.get('language', 'en')
        )
        
        return jsonify({
            "status": "success",
            "output_path": result
        })
    except Exception as e:
        logger.error(f"Error in text-to-speech: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@voice_enhanced_bp.route('/translate', methods=['POST'])
@authenticate
def translate_audio():
    """Translate audio from one language to another with enhanced quality
    
    Request body:
        input_path: Path to input audio file
        output_path: Path where translated audio will be saved
        source_lang: Language code of source audio (or 'auto' for auto-detection)
        target_lang: Language code for target translation
        preserve_voice: Try to preserve original voice characteristics (experimental)
    """
    data = request.json
    
    # Validate required fields
    required_fields = ['input_path', 'output_path']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Validate file existence
    if not os.path.isfile(data['input_path']):
        return jsonify({"error": "Audio file not found"}), 404
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(data['output_path']), exist_ok=True)
        
        # Use the enhanced translator
        translator = get_translator()
        result = translator.translate_audio(
            data['input_path'],
            data['output_path'],
            source_lang=data.get('source_lang', 'auto'),
            target_lang=data.get('target_lang', 'en'),
            preserve_voice=data.get('preserve_voice', False)
        )
        
        if 'error' in result:
            return jsonify({
                "status": "error",
                "message": result['error']
            }), 500
        
        return jsonify({
            "status": "success",
            "original_text": result.get('original_text', ''),
            "translated_text": result.get('translated_text', ''),
            "source_language": result.get('source_language', 'unknown'),
            "target_language": result.get('target_language', 'unknown'),
            "output_path": result.get('output_path', '')
        })
    except Exception as e:
        logger.error(f"Error translating audio: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@voice_enhanced_bp.route('/batch_translate', methods=['POST'])
@authenticate
def batch_translate_audio():
    """Batch process multiple audio files with translation
    
    Request body:
        input_files: List of paths to input audio files
        output_dir: Directory where output files will be saved
        source_lang: Language code of source audio (or 'auto' for auto-detection)
        target_lang: Language code for target translation
    """
    data = request.json
    
    # Validate required fields
    required_fields = ['input_files', 'output_dir']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Validate input files
    if not isinstance(data['input_files'], list) or len(data['input_files']) == 0:
        return jsonify({"error": "input_files must be a non-empty list"}), 400
    
    # Check all input files exist
    for input_file in data['input_files']:
        if not os.path.isfile(input_file):
            return jsonify({"error": f"File not found: {input_file}"}), 404
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(data['output_dir'], exist_ok=True)
        
        # Use the enhanced translator for batch processing
        translator = get_translator()
        results = translator.translate_audio_file_batch(
            data['input_files'],
            data['output_dir'],
            source_lang=data.get('source_lang', 'auto'),
            target_lang=data.get('target_lang', 'en')
        )
        
        # Filter out any results with errors
        errors = [r for r in results if 'error' in r]
        if errors:
            # If some files failed, return partial success
            return jsonify({
                "status": "partial_success",
                "success_count": len(results) - len(errors),
                "error_count": len(errors),
                "results": results
            }), 207
        
        return jsonify({
            "status": "success",
            "count": len(results),
            "results": results
        })
    except Exception as e:
        logger.error(f"Error in batch translation: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@voice_enhanced_bp.route('/transcribe', methods=['POST'])
@authenticate
def transcribe_audio():
    """Transcribe audio to text with improved quality
    
    Request body:
        input_path: Path to input audio file
        language: Language code (or 'auto' for auto-detection)
    """
    data = request.json
    
    # Validate required fields
    if 'input_path' not in data:
        return jsonify({"error": "Missing required field: input_path"}), 400
    
    # Validate file existence
    if not os.path.isfile(data['input_path']):
        return jsonify({"error": "Audio file not found"}), 404
    
    try:
        # Use the enhanced translator for transcription
        translator = get_translator()
        
        # Prepare audio for better results
        temp_audio = translator._prepare_audio(data['input_path'])
        
        # Detect language if set to auto
        language = data.get('language', 'auto')
        if language == 'auto':
            detected_lang = translator._detect_language(temp_audio)
            language = detected_lang
        
        # Transcribe audio
        transcription = translator._transcribe_audio(temp_audio, language)
        
        # Clean up temp file
        if os.path.exists(temp_audio) and temp_audio != data['input_path']:
            os.unlink(temp_audio)
        
        if not transcription:
            return jsonify({
                "status": "error",
                "message": "Could not transcribe audio. Please check the audio quality."
            }), 500
        
        return jsonify({
            "status": "success",
            "text": transcription,
            "language": language
        })
    except Exception as e:
        logger.error(f"Error transcribing audio: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@voice_enhanced_bp.route('/languages', methods=['GET'])
def get_languages():
    """Get available languages for voice processing"""
    try:
        # Use the enhanced translator for language info
        translator = get_translator()
        languages = translator.available_languages()
        
        return jsonify({
            "status": "success",
            "languages": languages
        })
    except Exception as e:
        logger.error(f"Error getting languages: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@voice_enhanced_bp.route('/stream/<path:filename>', methods=['GET'])
def stream_audio(filename):
    """Stream audio file for immediate playback"""
    try:
        # Ensure path is within allowed directories
        if not filename.startswith(('temp/output/', 'temp/uploads/')):
            return jsonify({"error": "Access denied"}), 403
        
        # Check if file exists
        if not os.path.isfile(filename):
            return jsonify({"error": "File not found"}), 404
        
        # Stream file
        return send_file(filename, mimetype='audio/mpeg')
    except Exception as e:
        logger.error(f"Error streaming audio: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
