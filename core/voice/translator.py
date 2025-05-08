# Voice translation module

import os
import tempfile
from typing import Dict, List, Optional, Any
import speech_recognition as sr
from googletrans import Translator
from .text_to_speech import TextToSpeech

class VoiceTranslator:
    """Class for voice translation"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.translator = Translator()
        self.tts = TextToSpeech()
    
    def translate_audio(self, input_path: str, output_path: str, 
                       source_lang: str = 'auto', target_lang: str = 'en') -> Dict[str, Any]:
        """Translate audio from one language to another
        
        Args:
            input_path: Path to input audio file
            output_path: Path where translated audio will be saved
            source_lang: Language code of source audio (or 'auto' for auto-detection)
            target_lang: Language code for target translation
            
        Returns:
            Dictionary containing:
                - original_text: Transcribed text from original audio
                - translated_text: Translated text
                - output_path: Path to output audio file
        """
        # Step 1: Transcribe audio to text
        with sr.AudioFile(input_path) as source:
            audio_data = self.recognizer.record(source)
            
            try:
                if source_lang == 'auto':
                    original_text = self.recognizer.recognize_google(audio_data)
                    # Detect language from text
                    detected = self.translator.detect(original_text)
                    source_lang = detected.lang
                else:
                    original_text = self.recognizer.recognize_google(audio_data, language=source_lang)
            except sr.UnknownValueError:
                return {"error": "Speech recognition could not understand audio"}
            except sr.RequestError:
                return {"error": "Could not request results from speech recognition service"}
        
        # Step 2: Translate text
        translation = self.translator.translate(original_text, src=source_lang, dest=target_lang)
        translated_text = translation.text
        
        # Step 3: Convert translated text to speech
        self.tts.convert(translated_text, output_path, language=target_lang)
        
        return {
            "original_text": original_text,
            "translated_text": translated_text,
            "source_language": source_lang,
            "target_language": target_lang,
            "output_path": output_path
        }
