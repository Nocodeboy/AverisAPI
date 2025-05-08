# Advanced video effects module

import os
import subprocess
import tempfile
import cv2
import numpy as np
from typing import Dict, List, Optional, Tuple, Any

class AdvancedVideoEffects:
    """Class for applying advanced effects to video files"""
    
    @staticmethod
    def apply_overlay(video_path: str, overlay_path: str, output_path: str, 
                     position: str = 'top-right', opacity: float = 0.7) -> str:
        """Apply overlay to video (e.g., logo, watermark)
        
        Args:
            video_path: Path to input video file
            overlay_path: Path to overlay image
            output_path: Path where output video will be saved
            position: Position of overlay (top-left, top-right, bottom-left, bottom-right, center)
            opacity: Opacity of overlay (0.0 to 1.0)
            
        Returns:
            Path to output video file
        """
        # Get video dimensions
        probe_cmd = [
            "ffprobe", "-v", "error", "-select_streams", "v:0", 
            "-show_entries", "stream=width,height", "-of", "csv=p=0", video_path
        ]
        result = subprocess.run(probe_cmd, stdout=subprocess.PIPE, text=True, check=True)
        width, height = map(int, result.stdout.strip().split(','))
        
        # Calculate position
        position_map = {
            'top-left': "10:10",
            'top-right': f"{width-overlay_width-10}:10",
            'bottom-left': f"10:{height-overlay_height-10}",
            'bottom-right': f"{width-overlay_width-10}:{height-overlay_height-10}",
            'center': f"{width//2-overlay_width//2}:{height//2-overlay_height//2}"
        }
        
        # Default to top-right if position not in map
        pos_coords = position_map.get(position, position_map['top-right'])
        
        command = [
            "ffmpeg", "-i", video_path, "-i", overlay_path,
            "-filter_complex", f"[1:v]format=rgba,colorchannelmixer=aa={opacity}[overlay];"
                              f"[0:v][overlay]overlay={pos_coords}",
            "-c:a", "copy",
            output_path, "-y"
        ]
        
        subprocess.run(command, check=True)
        return output_path
    
    @staticmethod
    def apply_timelapse(video_path: str, output_path: str, speed_factor: float = 10.0) -> str:
        """Convert video to timelapse
        
        Args:
            video_path: Path to input video file
            output_path: Path where output video will be saved
            speed_factor: How much to speed up the video (e.g., 10.0 = 10x speed)
            
        Returns:
            Path to output video file
        """
        # Use select filter to pick 1 out of N frames
        # For a 30fps video, speed_factor=10 means selecting 1 out of 10 frames = 3fps
        # Then we use setpts to maintain original timing
        command = [
            "ffmpeg", "-i", video_path,
            "-filter:v", f"select='not(mod(n,{int(speed_factor)}))',setpts=N/(FRAME_RATE*TB)",
            "-c:a", "copy",
            output_path, "-y"
        ]
        
        subprocess.run(command, check=True)
        return output_path
    
    @staticmethod
    def cinematic_bars(video_path: str, output_path: str, ratio: str = "2.35:1") -> str:
        """Add cinematic letterbox/bars effect to video
        
        Args:
            video_path: Path to input video file
            output_path: Path where output video will be saved
            ratio: Aspect ratio (2.35:1, 2.39:1, 1.85:1, etc.)
            
        Returns:
            Path to output video file
        """
        ratios = {
            "2.35:1": 2.35,
            "2.39:1": 2.39,
            "1.85:1": 1.85,
            "16:9": 16/9,
            "4:3": 4/3
        }
        
        target_ratio = ratios.get(ratio, 2.35)
        
        # Get video dimensions
        probe_cmd = [
            "ffprobe", "-v", "error", "-select_streams", "v:0", 
            "-show_entries", "stream=width,height", "-of", "csv=p=0", video_path
        ]
        result = subprocess.run(probe_cmd, stdout=subprocess.PIPE, text=True, check=True)
        width, height = map(int, result.stdout.strip().split(','))
        
        current_ratio = width / height
        
        if current_ratio < target_ratio:
            # Need to add bars to top/bottom (letterbox)
            new_height = int(width / target_ratio)
            padding = (height - new_height) // 2
            filter_complex = f"pad=width={width}:height={height}:x=0:y={padding}:color=black"
        else:
            # Need to add bars to left/right (pillarbox)
            new_width = int(height * target_ratio)
            padding = (width - new_width) // 2
            filter_complex = f"pad=width={width}:height={height}:x={padding}:y=0:color=black"
        
        command = [
            "ffmpeg", "-i", video_path,
            "-vf", filter_complex,
            "-c:a", "copy",
            output_path, "-y"
        ]
        
        subprocess.run(command, check=True)
        return output_path
    
    @staticmethod
    def dream_effect(video_path: str, output_path: str, strength: float = 0.5) -> str:
        """Apply dreamy/hazy effect to video
        
        Args:
            video_path: Path to input video file
            output_path: Path where output video will be saved
            strength: Strength of effect (0.0 to 1.0)
            
        Returns:
            Path to output video file
        """
        # Create a subtle glow effect with blur and overlay
        blur_amount = int(20 * strength)
        glow_opacity = 0.3 * strength
        
        # Adjust colors to be more dreamlike
        saturation = 1.1 + (0.4 * strength)
        brightness = 0.05 * strength
        
        filter_complex = (
            f"split=2[original][blurred];"
            f"[blurred]gblur=sigma={blur_amount},eq=brightness={brightness}:saturation={saturation}[glowed];"
            f"[original][glowed]blend=all_mode=overlay:all_opacity={glow_opacity}"
        )
        
        command = [
            "ffmpeg", "-i", video_path,
            "-filter_complex", filter_complex,
            "-c:a", "copy",
            output_path, "-y"
        ]
        
        subprocess.run(command, check=True)
        return output_path
    
    @staticmethod
    def rgb_split(video_path: str, output_path: str, offset: int = 5) -> str:
        """Apply RGB split/glitch effect
        
        Args:
            video_path: Path to input video file
            output_path: Path where output video will be saved
            offset: Pixel offset for color channels
            
        Returns:
            Path to output video file
        """
        # Use RGB split effect - separate R, G, B channels and offset them
        filter_complex = (
            f"split=3[r][g][b];"
            f"[r]lutrgb=r=1:g=0:b=0,geq=r='r(X,Y)':g='0':b='0',crop=iw:ih:0:0[r1];"
            f"[g]lutrgb=r=0:g=1:b=0,geq=r='0':g='g(X,Y)':b='0',crop=iw:ih:{offset}:0[g1];"
            f"[b]lutrgb=r=0:g=0:b=1,geq=r='0':g='0':b='b(X,Y)',crop=iw:ih:{offset*2}:0[b1];"
            f"[r1][g1]blend=all_mode=addition[rg];"
            f"[rg][b1]blend=all_mode=addition[rgb]"
        )
        
        command = [
            "ffmpeg", "-i", video_path,
            "-filter_complex", filter_complex,
            "-map", "[rgb]", "-map", "0:a?",
            "-c:a", "copy",
            output_path, "-y"
        ]
        
        subprocess.run(command, check=True)
        return output_path
    
    @staticmethod
    def vhs_effect(video_path: str, output_path: str, intensity: float = 0.7) -> str:
        """Apply VHS/retro tape effect to video
        
        Args:
            video_path: Path to input video file
            output_path: Path where output video will be saved
            intensity: Strength of effect (0.0 to 1.0)
            
        Returns:
            Path to output video file
        """
        # Create temp files for processing
        temp_noise = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
        
        try:
            # We need to create a noise pattern first
            # Get video dimensions and duration
            probe_cmd = [
                "ffprobe", "-v", "error", "-select_streams", "v:0", 
                "-show_entries", "stream=width,height,duration", "-of", "csv=p=0", video_path
            ]
            result = subprocess.run(probe_cmd, stdout=subprocess.PIPE, text=True, check=True)
            width, height, duration = result.stdout.strip().split(',')
            width, height = int(width), int(height)
            
            # Generate noise video
            noise_cmd = [
                "ffmpeg", "-f", "lavfi", "-i", 
                f"color=c=black:s={width}x{height}:d={duration},"
                f"noise=alls={10*intensity}:allf=t",
                "-c:v", "libx264", "-preset", "ultrafast",
                temp_noise, "-y"
            ]
            subprocess.run(noise_cmd, check=True)
            
            # Now combine with original video to create VHS effect
            filter_complex = (
                # Reduce quality and add artifacts
                f"[0:v]noise=alls=0:allf=t,"
                f"eq=brightness=0.05:saturation={0.8 - 0.3*intensity}:contrast=0.8,"
                f"unsharp=3:3:0.3:3:3:0,"
                # Add slight color shift
                f"colorbalance=rs=0.05:gs=0:bs=-0.05[main];"
                # Overlay noise with low opacity
                f"[1:v]format=rgba,colorchannelmixer=aa={0.03 + 0.05*intensity}[noise];"
                f"[main][noise]overlay=shortest=1[out]"
            )
            
            # Audio effects for VHS sound
            audio_filter = f"highpass=200,lowpass=3000,volume=0.9,aecho=0.8:0.1:50:0.5"
            
            command = [
                "ffmpeg", "-i", video_path, "-i", temp_noise,
                "-filter_complex", filter_complex,
                "-map", "[out]", "-map", "0:a?",
                "-af", audio_filter,
                output_path, "-y"
            ]
            
            subprocess.run(command, check=True)
            return output_path
            
        finally:
            # Clean up temp files
            if os.path.exists(temp_noise):
                os.unlink(temp_noise)
    
    @staticmethod
    def apply_Ken_Burns(image_path: str, output_path: str, duration: int = 10, 
                       zoom_start: float = 1.0, zoom_end: float = 1.5, 
                       direction: str = "in") -> str:
        """Apply Ken Burns effect to an image (pan and zoom)
        
        Args:
            image_path: Path to input image
            output_path: Path where output video will be saved
            duration: Duration of output video in seconds
            zoom_start: Initial zoom level
            zoom_end: Final zoom level
            direction: Direction of movement ("in", "out", "left", "right", "top", "bottom")
            
        Returns:
            Path to output video file
        """
        # Map directions to zoompan parameters
        directions = {
            "in": f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':z='zoom'",
            "out": f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':z='zoom'",
            "left": f"x='iw/2-(iw/zoom/2)+{duration}*5':y='ih/2-(ih/zoom/2)':z='zoom'",
            "right": f"x='iw/2-(iw/zoom/2)-{duration}*5':y='ih/2-(ih/zoom/2)':z='zoom'",
            "top": f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)+{duration}*5':z='zoom'",
            "bottom": f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)-{duration}*5':z='zoom'"
        }
        
        # Get zoom formula based on direction
        if direction == "out":
            zoom_formula = f"{zoom_end}-({zoom_end-{zoom_start}})*t/{duration}"
        else:
            zoom_formula = f"{zoom_start}+({zoom_end-{zoom_start}})*t/{duration}"
        
        position_formula = directions.get(direction, directions["in"])
        
        command = [
            "ffmpeg", "-loop", "1", "-i", image_path,
            "-vf", f"scale=1920:1080:force_original_aspect_ratio=decrease,"
                    f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2,"
                    f"zoompan={position_formula}:d={fps*duration}:fps={fps}",
            "-t", str(duration),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            output_path, "-y"
        ]
        
        # Set fps for smooth motion
        fps = 30
        
        subprocess.run(command, check=True)
        return output_path
