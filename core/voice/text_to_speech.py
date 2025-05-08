# Text to Speech module

import os
import tempfile
from typing import Dict, List, Optional, Any
from gtts import gTTS

class TextToSpeech:
    """Class for text to speech conversion"""
    
    @staticmethod
    def convert(text: str, output_path: str, language: str = 'en', 
               slow: bool = False, voice_type: str = 'standard') -> str:
        """Convert text to speech
        
        Args:
            text: Text to convert to speech
            output_path: Path where output audio file will be saved
            language: Language code (e.g., 'en', 'es', 'fr')
            slow: Whether to speak slowly
            voice_type: Type of voice to use (currently only 'standard' supported with gTTS)
            
        Returns:
            Path to output audio file
        """
        # Using gTTS for simple implementation
        # In a production environment, consider more advanced TTS solutions
        tts = gTTS(text=text, lang=language, slow=slow)
        tts.save(output_path)
        return output_path
    
    @staticmethod
    def available_languages() -> Dict[str, str]:
        """Get available language codes and names
        
        Returns:
            Dictionary of language codes and names
        """
        # This is a subset of languages supported by gTTS
        return {
            'af': 'Afrikaans',
            'ar': 'Arabic',
            'bg': 'Bulgarian',
            'bn': 'Bengali',
            'bs': 'Bosnian',
            'ca': 'Catalan',
            'cs': 'Czech',
            'da': 'Danish',
            'de': 'German',
            'el': 'Greek',
            'en': 'English',
            'es': 'Spanish',
            'et': 'Estonian',
            'fi': 'Finnish',
            'fr': 'French',
            'gu': 'Gujarati',
            'hi': 'Hindi',
            'hr': 'Croatian',
            'hu': 'Hungarian',
            'id': 'Indonesian',
            'is': 'Icelandic',
            'it': 'Italian',
            'ja': 'Japanese',
            'kn': 'Kannada',
            'ko': 'Korean',
            'lt': 'Lithuanian',
            'lv': 'Latvian',
            'ml': 'Malayalam',
            'mr': 'Marathi',
            'nb': 'Norwegian',
            'nl': 'Dutch',
            'pl': 'Polish',
            'pt': 'Portuguese',
            'ro': 'Romanian',
            'ru': 'Russian',
            'sk': 'Slovak',
            'sl': 'Slovenian',
            'sr': 'Serbian',
            'sv': 'Swedish',
            'ta': 'Tamil',
            'te': 'Telugu',
            'th': 'Thai',
            'tr': 'Turkish',
            'uk': 'Ukrainian',
            'vi': 'Vietnamese',
            'zh-CN': 'Chinese (Simplified)',
            'zh-TW': 'Chinese (Traditional)'
        }
