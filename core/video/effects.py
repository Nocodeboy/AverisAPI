# Video effects module

import os
import subprocess
import cv2
import numpy as np
from typing import Dict, List, Optional, Tuple, Any

class VideoEffects:
    """Class for applying various effects to video files"""
    
    @staticmethod
    def apply_color_filter(input_path: str, output_path: str, filter_type: str, intensity: float = 1.0) -> str:
        """Apply color filter to video
        
        Args:
            input_path: Path to input video file
            output_path: Path where output video will be saved
            filter_type: Type of filter (grayscale, sepia, vintage, etc.)
            intensity: Intensity of the effect (0.0 to 1.0)
            
        Returns:
            Path to output video file
        """
        # Example implementation using FFmpeg
        filters = {
            "grayscale": f"colorchannelmixer=.3:.59:.11:0:.3:.59:.11:0:.3:.59:.11:0:0:0:0:1",
            "sepia": f"colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131:0:0:0:0:1",
            "vintage": f"curves=vintage,vignette=PI/4",
            "vibrant": f"eq=saturation={1.0 + intensity}:contrast=1.1"
        }
        
        filter_command = filters.get(filter_type, filters["grayscale"])
        
        command = [
            "ffmpeg", "-i", input_path,
            "-vf", filter_command,
            "-c:a", "copy",
            output_path, "-y"
        ]
        
        subprocess.run(command, check=True)
        return output_path
    
    @staticmethod
    def add_transition(input1: str, input2: str, output_path: str, transition_type: str, duration: float = 1.0) -> str:
        """Add transition between two videos
        
        Args:
            input1: Path to first video
            input2: Path to second video
            output_path: Path where output video will be saved
            transition_type: Type of transition (fade, wipe, zoom, etc.)
            duration: Duration of transition in seconds
            
        Returns:
            Path to output video file
        """
        transitions = {
            "fade": f"xfade=fade:duration={duration}",
            "wipe_left": f"xfade=wipeleft:duration={duration}",
            "wipe_right": f"xfade=wiperight:duration={duration}",
            "wipe_up": f"xfade=wipeup:duration={duration}",
            "wipe_down": f"xfade=wipedown:duration={duration}",
            "slide_left": f"xfade=slideleft:duration={duration}",
            "slide_right": f"xfade=slideright:duration={duration}",
            "zoom_in": f"xfade=zoomin:duration={duration}",
            "zoom_out": f"xfade=fadeoutfadein:duration={duration}",
        }
        
        transition_command = transitions.get(transition_type, transitions["fade"])
        
        # Get the duration of the first video to calculate transition point
        duration_cmd = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", input1
        ]
        result = subprocess.run(duration_cmd, stdout=subprocess.PIPE, text=True, check=True)
        first_duration = float(result.stdout.strip())
        offset = max(0, first_duration - duration)
        
        command = [
            "ffmpeg", "-i", input1, "-i", input2,
            "-filter_complex", f"[0:v][1:v]{transition_command}:offset={offset}",
            "-c:a", "aac",
            output_path, "-y"
        ]
        
        subprocess.run(command, check=True)
        return output_path
    
    @staticmethod
    def enhance_video(input_path: str, output_path: str, 
                    denoise: bool = False, sharpen: bool = False, 
                    brightness: float = 0.0, contrast: float = 0.0) -> str:
        """Enhance video quality
        
        Args:
            input_path: Path to input video file
            output_path: Path where output video will be saved
            denoise: Apply denoising filter
            sharpen: Apply sharpening filter
            brightness: Brightness adjustment (-1.0 to 1.0)
            contrast: Contrast adjustment (-1.0 to 1.0)
            
        Returns:
            Path to output video file
        """
        filters = []
        
        if denoise:
            filters.append("nlmeans=10:7:5:3:7")
            
        if sharpen:
            filters.append("unsharp=5:5:1.0:5:5:0.0")
            
        if brightness != 0.0 or contrast != 0.0:
            # Convert to eq2 parameters (gamma, contrast, brightness)
            eq_filter = f"eq=gamma=1.0:contrast={1.0 + contrast}:brightness={brightness}"
            filters.append(eq_filter)
        
        if not filters:
            # If no filters, just copy the video
            command = [
                "ffmpeg", "-i", input_path,
                "-c:v", "copy", "-c:a", "copy",
                output_path, "-y"
            ]
        else:
            filter_string = ",".join(filters)
            command = [
                "ffmpeg", "-i", input_path,
                "-vf", filter_string,
                "-c:a", "copy",
                output_path, "-y"
            ]
        
        subprocess.run(command, check=True)
        return output_path
