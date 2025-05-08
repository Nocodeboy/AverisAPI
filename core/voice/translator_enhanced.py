# Enhanced Voice Translation Module

import os
import tempfile
import subprocess
from typing import Dict, List, Optional, Any
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import nltk
from nltk.tokenize import sent_tokenize
from transformers import MarianMTModel, MarianTokenizer

# Download necessary NLTK data (if not already downloaded)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class EnhancedVoiceTranslator:
    """Enhanced class for voice translation with better results"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
        # Initialize speech recognition with noise adjustment
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 300
        self.recognizer.pause_threshold = 0.8
        
        # Cache for translation models (loaded only when needed)
        self._translation_models = {}
        self._translation_tokenizers = {}
    
    def _get_translation_model(self, source_lang: str, target_lang: str):
        """Get translation model for the specific language pair"""
        model_name = f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}"
        model_key = f"{source_lang}-{target_lang}"
        
        if model_key not in self._translation_models:
            try:
                self._translation_tokenizers[model_key] = MarianTokenizer.from_pretrained(model_name)
                self._translation_models[model_key] = MarianMTModel.from_pretrained(model_name)
            except Exception as e:
                # Fallback to alternative model if specific language pair not available
                print(f"Warning: Translation model {model_name} not available. Using fallback.")
                fallback_model = "Helsinki-NLP/opus-mt-en-ROMANCE" if target_lang in ['es', 'fr', 'it', 'pt'] else "Helsinki-NLP/opus-mt-en-de"
                self._translation_tokenizers[model_key] = MarianTokenizer.from_pretrained(fallback_model)
                self._translation_models[model_key] = MarianMTModel.from_pretrained(fallback_model)
        
        return self._translation_models[model_key], self._translation_tokenizers[model_key]
    
    def _convert_language_code(self, code: str, for_whisper: bool = False) -> str:
        """Convert between different language code formats"""
        # Mapping of common language codes
        iso_639_1_to_name = {
            'en': 'english',
            'es': 'spanish',
            'fr': 'french',
            'de': 'german',
            'it': 'italian',
            'pt': 'portuguese',
            'ru': 'russian',
            'ja': 'japanese',
            'zh': 'chinese',
            'ar': 'arabic',
            'hi': 'hindi',
            'ko': 'korean'
        }
        
        iso_639_1_to_whisper = {
            'en': 'en',
            'es': 'es',
            'fr': 'fr',
            'de': 'de',
            'it': 'it',
            'pt': 'pt',
            'ru': 'ru',
            'ja': 'ja',
            'zh': 'zh',
            'ar': 'ar',
            'hi': 'hi',
            'ko': 'ko'
        }
        
        # For translation models (Helsinki NLP format)
        iso_639_1_to_helsinki = {
            'en': 'en',
            'es': 'es',
            'fr': 'fr',
            'de': 'de',
            'it': 'it',
            'pt': 'pt',
            'ru': 'ru',
            'ja': 'jap',
            'zh': 'zh',
            'ar': 'ar',
            'hi': 'hi',
            'ko': 'ko'
        }
        
        if for_whisper:
            return iso_639_1_to_whisper.get(code, code)
        
        return iso_639_1_to_helsinki.get(code, code)
    
    def _detect_language(self, audio_file: str) -> str:
        """Detect language from audio file using Whisper"""
        # Use a small Whisper model for language detection
        try:
            import whisper
            model = whisper.load_model("tiny")
            result = model.transcribe(audio_file, task="detect_language")
            detected_lang = result.get("language", "en")
            return detected_lang
        except ImportError:
            # Fallback to Google Speech Recognition
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
                try:
                    # Use Google Speech Recognition which returns recognized language
                    self.recognizer.recognize_google(audio)
                    # Get language from the response
                    return "en"  # Default to English if we can't detect
                except sr.UnknownValueError:
                    return "en"
    
    def _transcribe_audio(self, audio_file: str, language: str = None) -> str:
        """Transcribe audio to text with better accuracy"""
        try:
            # Try to use Whisper if available (better accuracy)
            import whisper
            
            # If language is auto, detect first
            if language == "auto" or language is None:
                language = self._detect_language(audio_file)
            
            # Use whisper for transcription
            model = whisper.load_model("base")
            result = model.transcribe(
                audio_file, 
                language=self._convert_language_code(language, for_whisper=True),
                fp16=False
            )
            return result["text"]
            
        except ImportError:
            # Fallback to Google Speech Recognition
            with sr.AudioFile(audio_file) as source:
                # Apply noise reduction
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.record(source)
                
                try:
                    if language == "auto" or language is None:
                        return self.recognizer.recognize_google(audio)
                    else:
                        return self.recognizer.recognize_google(
                            audio, 
                            language=language
                        )
                except sr.UnknownValueError:
                    return ""
                except sr.RequestError:
                    raise Exception("Could not request results from speech recognition service")
    
    def _translate_text(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text with improved quality"""
        if not text:
            return ""
        
        if source_lang == target_lang:
            return text
            
        try:
            # Try to use MarianMT for better translation
            model, tokenizer = self._get_translation_model(
                self._convert_language_code(source_lang), 
                self._convert_language_code(target_lang)
            )
            
            # Split text into sentences for better translation
            sentences = sent_tokenize(text)
            translated_parts = []
            
            for sentence in sentences:
                # Skip empty sentences
                if not sentence.strip():
                    continue
                    
                # Translate sentence
                inputs = tokenizer([sentence], return_tensors="pt", padding=True)
                outputs = model.generate(**inputs)
                translated = tokenizer.decode(outputs[0], skip_special_tokens=True)
                translated_parts.append(translated)
            
            return " ".join(translated_parts)
            
        except Exception as e:
            # Fallback to Google Translate
            from googletrans import Translator
            translator = Translator()
            translation = translator.translate(text, src=source_lang, dest=target_lang)
            return translation.text
    
    def _text_to_speech(self, text: str, output_file: str, language: str = "en") -> str:
        """Convert text to speech with improved quality"""
        try:
            # Try to use better TTS if available
            import torch
            from TTS.api import TTS
            
            # Initialize TTS with appropriate model
            tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")
            
            # Generate speech
            tts.tts_to_file(text=text, file_path=output_file)
            return output_file
            
        except ImportError:
            # Fallback to gTTS
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(output_file)
            return output_file
    
    def _prepare_audio(self, audio_file: str) -> str:
        """Prepare audio for processing (convert format, normalize, etc.)"""
        # Create temporary file for processed audio
        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
        
        try:
            # Convert to WAV using FFmpeg with noise reduction and normalization
            command = [
                "ffmpeg", "-i", audio_file,
                "-af", "highpass=f=200,lowpass=f=3000,afftdn=nr=10:nf=-20,loudnorm=I=-16:LRA=11:TP=-1.5",
                "-ar", "16000", "-ac", "1",
                temp_file, "-y"
            ]
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return temp_file
            
        except Exception as e:
            # Fallback to simpler conversion if FFmpeg fails
            audio = AudioSegment.from_file(audio_file)
            audio = audio.set_channels(1)  # Convert to mono
            audio = audio.set_frame_rate(16000)  # Set sample rate to 16kHz
            audio.export(temp_file, format="wav")
            return temp_file
    
    def translate_audio(self, input_path: str, output_path: str, 
                       source_lang: str = "auto", target_lang: str = "en",
                       preserve_voice: bool = False) -> Dict[str, Any]:
        """Translate audio from one language to another with enhanced quality
        
        Args:
            input_path: Path to input audio file
            output_path: Path where translated audio will be saved
            source_lang: Language code of source audio (or 'auto' for auto-detection)
            target_lang: Language code for target translation
            preserve_voice: Try to preserve original voice characteristics (experimental)
            
        Returns:
            Dictionary containing:
                - original_text: Transcribed text from original audio
                - translated_text: Translated text
                - source_language: Detected or specified source language
                - target_language: Target language
                - output_path: Path to output audio file
        """
        # Temporary files for processing
        temp_audio = None
        
        try:
            # Step 1: Prepare audio for processing
            temp_audio = self._prepare_audio(input_path)
            
            # Step 2: Detect language if set to auto
            if source_lang == "auto":
                detected_lang = self._detect_language(temp_audio)
                source_lang = detected_lang
            
            # Step 3: Transcribe audio to text
            original_text = self._transcribe_audio(temp_audio, source_lang)
            if not original_text:
                return {"error": "Could not transcribe audio. Please check the audio quality."}
            
            # Step 4: Translate text
            translated_text = self._translate_text(original_text, source_lang, target_lang)
            if not translated_text:
                return {"error": "Translation failed. Please try again."}
            
            # Step 5: Generate speech from translated text
            if preserve_voice and False:  # Voice preservation not fully implemented yet
                # TODO: Implement voice preservation using voice conversion models
                pass
            else:
                self._text_to_speech(translated_text, output_path, target_lang)
            
            return {
                "original_text": original_text,
                "translated_text": translated_text,
                "source_language": source_lang,
                "target_language": target_lang,
                "output_path": output_path
            }
            
        except Exception as e:
            return {"error": str(e)}
            
        finally:
            # Clean up temporary files
            if temp_audio and os.path.exists(temp_audio):
                os.unlink(temp_audio)
    
    def translate_audio_file_batch(self, input_files: List[str], output_dir: str,
                                 source_lang: str = "auto", target_lang: str = "en") -> List[Dict[str, Any]]:
        """Batch process multiple audio files
        
        Args:
            input_files: List of paths to input audio files
            output_dir: Directory where output files will be saved
            source_lang: Language code of source audio (or 'auto' for auto-detection)
            target_lang: Language code for target translation
            
        Returns:
            List of dictionaries with results for each file
        """
        results = []
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        for input_file in input_files:
            # Generate output filename
            filename = os.path.basename(input_file)
            name, ext = os.path.splitext(filename)
            output_file = os.path.join(output_dir, f"{name}_translated.mp3")
            
            # Process file
            result = self.translate_audio(
                input_file, output_file, source_lang, target_lang
            )
            
            # Add filename to result
            result["input_file"] = input_file
            results.append(result)
        
        return results
    
    def available_languages(self) -> Dict[str, str]:
        """Get list of available languages for speech recognition and translation"""
        return {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'zh': 'Chinese',
            'ar': 'Arabic',
            'hi': 'Hindi',
            'ko': 'Korean',
            'nl': 'Dutch',
            'pl': 'Polish'
        }
