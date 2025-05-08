#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AverisAPI Demo Client

This script demonstrates how to use the AverisAPI for video and voice processing.
It includes examples for various effects and translations.

Usage:
    python demo_client.py --api-key YOUR_API_KEY --endpoint http://localhost:8080
"""

import os
import argparse
import requests
import time
import json
from pathlib import Path

# Create samples directory if it doesn't exist
SAMPLES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'samples')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'temp', 'output')
os.makedirs(SAMPLES_DIR, exist_ok=True)
os.makedirs(os.path.join(SAMPLES_DIR, 'video'), exist_ok=True)
os.makedirs(os.path.join(SAMPLES_DIR, 'audio'), exist_ok=True)
os.makedirs(os.path.join(SAMPLES_DIR, 'images'), exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

class AverisAPIClient:
    """Client for interacting with AverisAPI"""
    
    def __init__(self, api_key, endpoint='http://localhost:8080'):
        self.api_key = api_key
        self.endpoint = endpoint.rstrip('/')
        self.headers = {
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        }
    
    def health_check(self):
        """Check if the API is running"""
        url = f"{self.endpoint}/health"
        response = requests.get(url)
        return response.json()
    
    def upload_file(self, file_path):
        """Upload a file to the API"""
        url = f"{self.endpoint}/upload"
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f)}
            response = requests.post(url, files=files, headers={'X-API-Key': self.api_key})
        return response.json()
    
    def apply_video_effect(self, video_path, output_path, effect_type, intensity=0.7):
        """Apply a basic effect to a video"""
        url = f"{self.endpoint}/video/apply_effect"
        data = {
            'input_path': video_path,
            'output_path': output_path,
            'effect_type': effect_type,
            'intensity': intensity
        }
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def apply_dream_effect(self, video_path, output_path, strength=0.5):
        """Apply dream effect to a video"""
        url = f"{self.endpoint}/video/dream_effect"
        data = {
            'video_path': video_path,
            'output_path': output_path,
            'strength': strength
        }
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def apply_vhs_effect(self, video_path, output_path, intensity=0.7):
        """Apply VHS effect to a video"""
        url = f"{self.endpoint}/video/vhs_effect"
        data = {
            'video_path': video_path,
            'output_path': output_path,
            'intensity': intensity
        }
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def create_ken_burns(self, image_path, output_path, duration=10, direction='in'):
        """Apply Ken Burns effect to an image"""
        url = f"{self.endpoint}/video/ken_burns"
        data = {
            'image_path': image_path,
            'output_path': output_path,
            'duration': duration,
            'zoom_start': 1.0,
            'zoom_end': 1.5,
            'direction': direction
        }
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def text_to_speech(self, text, output_path, language='en'):
        """Convert text to speech"""
        url = f"{self.endpoint}/voice/text_to_speech"
        data = {
            'text': text,
            'output_path': output_path,
            'language': language
        }
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def translate_audio(self, audio_path, output_path, source_lang='auto', target_lang='en'):
        """Translate audio from one language to another"""
        url = f"{self.endpoint}/voice/translate"
        data = {
            'input_path': audio_path,
            'output_path': output_path,
            'source_lang': source_lang,
            'target_lang': target_lang
        }
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def transcribe_audio(self, audio_path, language='auto'):
        """Transcribe audio to text"""
        url = f"{self.endpoint}/voice/transcribe"
        data = {
            'input_path': audio_path,
            'language': language
        }
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def get_languages(self):
        """Get available languages for voice processing"""
        url = f"{self.endpoint}/voice/languages"
        response = requests.get(url)
        return response.json()

def prepare_sample_video():
    """Prepare a sample video for testing (using FFmpeg)"""
    video_path = os.path.join(SAMPLES_DIR, 'video', 'sample.mp4')
    
    # Skip if the file already exists
    if os.path.exists(video_path):
        print(f"Sample video already exists at {video_path}")
        return video_path
    
    print("Generating sample video...")
    try:
        import subprocess
        # Generate a test pattern video
        command = [
            "ffmpeg", "-f", "lavfi", "-i", "testsrc=duration=5:size=640x480:rate=30",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", 
            video_path, "-y"
        ]
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Sample video created at {video_path}")
    except Exception as e:
        print(f"Could not generate sample video: {str(e)}")
        print("Please download a sample video and place it at:", video_path)
    
    return video_path

def prepare_sample_image():
    """Prepare a sample image for testing (using FFmpeg)"""
    image_path = os.path.join(SAMPLES_DIR, 'images', 'sample.jpg')
    
    # Skip if the file already exists
    if os.path.exists(image_path):
        print(f"Sample image already exists at {image_path}")
        return image_path
    
    print("Generating sample image...")
    try:
        import subprocess
        # Generate a test pattern image
        command = [
            "ffmpeg", "-f", "lavfi", "-i", "testsrc=size=640x480:rate=1",
            "-frames:v", "1", 
            image_path, "-y"
        ]
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Sample image created at {image_path}")
    except Exception as e:
        print(f"Could not generate sample image: {str(e)}")
        print("Please download a sample image and place it at:", image_path)
    
    return image_path

def run_demo(api_key, endpoint):
    """Run a demonstration of AverisAPI capabilities"""
    client = AverisAPIClient(api_key, endpoint)
    
    # Check if the API is running
    print("Checking API status...")
    try:
        health = client.health_check()
        print(f"API is running: {json.dumps(health, indent=2)}")
    except Exception as e:
        print(f"Error connecting to API: {str(e)}")
        print(f"Make sure the API is running at {endpoint}")
        return
    
    # Prepare sample files
    video_path = prepare_sample_video()
    image_path = prepare_sample_image()
    
    if not os.path.exists(video_path) or not os.path.exists(image_path):
        print("Cannot continue without sample files")
        return
    
    # Demo: Video Effects
    print("\n=== Video Effect Demo ===")
    output_path = os.path.join(OUTPUT_DIR, 'video_sepia.mp4')
    print("Applying sepia effect to video...")
    result = client.apply_video_effect(video_path, output_path, 'sepia')
    print(f"Result: {json.dumps(result, indent=2)}")
    
    # Demo: Dream Effect
    print("\n=== Dream Effect Demo ===")
    output_path = os.path.join(OUTPUT_DIR, 'video_dream.mp4')
    print("Applying dream effect to video...")
    result = client.apply_dream_effect(video_path, output_path)
    print(f"Result: {json.dumps(result, indent=2)}")
    
    # Demo: VHS Effect
    print("\n=== VHS Effect Demo ===")
    output_path = os.path.join(OUTPUT_DIR, 'video_vhs.mp4')
    print("Applying VHS effect to video...")
    result = client.apply_vhs_effect(video_path, output_path)
    print(f"Result: {json.dumps(result, indent=2)}")
    
    # Demo: Ken Burns Effect
    print("\n=== Ken Burns Effect Demo ===")
    output_path = os.path.join(OUTPUT_DIR, 'ken_burns.mp4')
    print("Creating Ken Burns effect from image...")
    result = client.create_ken_burns(image_path, output_path)
    print(f"Result: {json.dumps(result, indent=2)}")
    
    # Demo: Text to Speech
    print("\n=== Text to Speech Demo ===")
    output_path = os.path.join(OUTPUT_DIR, 'tts_output.mp3')
    print("Converting text to speech...")
    result = client.text_to_speech(
        "Hello! This is a demonstration of the Text to Speech capability in AverisAPI.", 
        output_path
    )
    print(f"Result: {json.dumps(result, indent=2)}")
    
    # Demo: Languages
    print("\n=== Available Languages ===")
    print("Getting available languages...")
    languages = client.get_languages()
    print(f"Languages: {json.dumps(languages, indent=2)}")
    
    print("\n=== Demo Complete ===")
    print(f"Output files are available in: {OUTPUT_DIR}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AverisAPI Demo Client')
    parser.add_argument('--api-key', default='dev_key_not_secure', 
                        help='API key for authentication')
    parser.add_argument('--endpoint', default='http://localhost:8080',
                        help='API endpoint URL')
    
    args = parser.parse_args()
    run_demo(args.api_key, args.endpoint)
