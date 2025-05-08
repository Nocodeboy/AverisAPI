#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pytest
import tempfile
import subprocess
from unittest.mock import patch, MagicMock

# Import the modules to test
from core.video.effects import VideoEffects
from core.video.effects_advanced import AdvancedVideoEffects

class TestVideoEffects:
    """Test cases for basic video effects"""
    
    @classmethod
    def setup_class(cls):
        """Set up test fixtures, if any"""
        # Create a small test video file
        cls.test_video = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
        cls.output_path = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
        
        # Generate a test video file using FFmpeg
        try:
            subprocess.run([
                "ffmpeg", "-f", "lavfi", "-i", "testsrc=duration=3:size=640x480:rate=30",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", cls.test_video, "-y"
            ], check=True, capture_output=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            # If FFmpeg is not available, mark all tests to be skipped
            pytest.skip("FFmpeg not available for generating test video")
    
    @classmethod
    def teardown_class(cls):
        """Tear down test fixtures, if any"""
        # Remove test files
        for file_path in [cls.test_video, cls.output_path]:
            if os.path.exists(file_path):
                try:
                    os.unlink(file_path)
                except OSError:
                    pass
    
    @pytest.mark.parametrize("filter_type", ["grayscale", "sepia", "vintage", "vibrant"])
    def test_apply_color_filter(self, filter_type):
        """Test applying color filters to video"""
        # Skip actual execution if FFmpeg might not be available
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock()
            
            result = VideoEffects.apply_color_filter(
                self.test_video, 
                self.output_path, 
                filter_type,
                intensity=0.7
            )
            
            # Check that subprocess.run was called
            mock_run.assert_called_once()
            
            # Check that FFmpeg command contains the filter
            args = mock_run.call_args[0][0]
            assert "-vf" in args
            filter_idx = args.index("-vf") + 1
            assert filter_type.lower() in args[filter_idx].lower() or "colorchannelmixer" in args[filter_idx].lower()
            
            # Check output path
            assert result == self.output_path
    
    def test_add_transition(self):
        """Test adding transition between videos"""
        # Skip actual execution if FFmpeg might not be available
        with patch("subprocess.run") as mock_run:
            # Mock for the duration probe
            duration_mock = MagicMock()
            duration_mock.stdout = "5.0\n"
            mock_run.side_effect = [duration_mock, MagicMock()]
            
            result = VideoEffects.add_transition(
                self.test_video,
                self.test_video,
                self.output_path,
                "fade",
                duration=1.0
            )
            
            # Check that subprocess.run was called twice (duration probe + transition)
            assert mock_run.call_count == 2
            
            # Check that FFmpeg command contains transition filter
            args = mock_run.call_args_list[1][0][0]
            assert "-filter_complex" in args
            filter_idx = args.index("-filter_complex") + 1
            assert "xfade" in args[filter_idx].lower()
            
            # Check output path
            assert result == self.output_path
    
    def test_enhance_video(self):
        """Test enhancing video quality"""
        # Skip actual execution if FFmpeg might not be available
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock()
            
            result = VideoEffects.enhance_video(
                self.test_video,
                self.output_path,
                denoise=True,
                sharpen=True,
                brightness=0.1,
                contrast=0.2
            )
            
            # Check that subprocess.run was called
            mock_run.assert_called_once()
            
            # Check that FFmpeg command contains filters
            args = mock_run.call_args[0][0]
            assert "-vf" in args
            filter_idx = args.index("-vf") + 1
            
            # Check for expected filters
            filter_str = args[filter_idx].lower()
            assert any(filter_name in filter_str for filter_name in ["nlmeans", "hqdn3d"])  # Denoising
            assert "unsharp" in filter_str  # Sharpening
            assert "eq" in filter_str  # Brightness/contrast
            
            # Check output path
            assert result == self.output_path

class TestAdvancedVideoEffects:
    """Test cases for advanced video effects"""
    
    @classmethod
    def setup_class(cls):
        """Set up test fixtures, if any"""
        # Create a small test video file
        cls.test_video = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
        cls.test_image = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False).name
        cls.output_path = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
        
        # Generate a test video file using FFmpeg
        try:
            # Generate test video
            subprocess.run([
                "ffmpeg", "-f", "lavfi", "-i", "testsrc=duration=3:size=640x480:rate=30",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", cls.test_video, "-y"
            ], check=True, capture_output=True)
            
            # Generate test image
            subprocess.run([
                "ffmpeg", "-f", "lavfi", "-i", "testsrc=size=640x480:rate=1",
                "-frames:v", "1", cls.test_image, "-y"
            ], check=True, capture_output=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            # If FFmpeg is not available, mark all tests to be skipped
            pytest.skip("FFmpeg not available for generating test media")
    
    @classmethod
    def teardown_class(cls):
        """Tear down test fixtures, if any"""
        # Remove test files
        for file_path in [cls.test_video, cls.test_image, cls.output_path]:
            if os.path.exists(file_path):
                try:
                    os.unlink(file_path)
                except OSError:
                    pass
    
    def test_apply_overlay(self):
        """Test adding overlay to video"""
        # Skip actual execution if FFmpeg might not be available
        with patch("subprocess.run") as mock_run:
            # Mock for the probe command
            probe_mock = MagicMock()
            probe_mock.stdout = "640,480\n"
            mock_run.side_effect = [probe_mock, MagicMock()]
            
            result = AdvancedVideoEffects.apply_overlay(
                self.test_video,
                self.test_image,
                self.output_path,
                position="top-right",
                opacity=0.7
            )
            
            # Check that FFmpeg commands were called
            assert mock_run.call_count == 2
            
            # Check that FFmpeg command contains overlay filter
            args = mock_run.call_args_list[1][0][0]
            assert "-filter_complex" in args
            filter_idx = args.index("-filter_complex") + 1
            assert "overlay" in args[filter_idx].lower()
            
            # Check output path
            assert result == self.output_path
    
    def test_dream_effect(self):
        """Test applying dream effect to video"""
        # Skip actual execution if FFmpeg might not be available
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock()
            
            result = AdvancedVideoEffects.dream_effect(
                self.test_video,
                self.output_path,
                strength=0.5
            )
            
            # Check that subprocess.run was called
            mock_run.assert_called_once()
            
            # Check that FFmpeg command contains dream effect filters
            args = mock_run.call_args[0][0]
            assert "-filter_complex" in args
            filter_idx = args.index("-filter_complex") + 1
            
            # Check for expected components of dream effect
            filter_str = args[filter_idx].lower()
            assert "gblur" in filter_str  # Blur component
            assert "blend" in filter_str  # Blend component
            
            # Check output path
            assert result == self.output_path
    
    def test_vhs_effect(self):
        """Test applying VHS effect to video"""
        # Skip actual execution if FFmpeg might not be available
        with patch("subprocess.run") as mock_run:
            # Mock for commands
            probe_mock = MagicMock()
            probe_mock.stdout = "640,480,3.0\n"
            mock_run.side_effect = [probe_mock, MagicMock(), MagicMock()]
            
            result = AdvancedVideoEffects.vhs_effect(
                self.test_video,
                self.output_path,
                intensity=0.7
            )
            
            # Check that FFmpeg commands were called
            assert mock_run.call_count == 3
            
            # Check that final FFmpeg command contains VHS filters
            args = mock_run.call_args_list[2][0][0]
            assert "-filter_complex" in args
            filter_idx = args.index("-filter_complex") + 1
            
            # Check for expected components of VHS effect
            filter_str = args[filter_idx].lower()
            assert "noise" in filter_str or "colorbalance" in filter_str
            
            # Check output path
            assert result == self.output_path
    
    def test_apply_Ken_Burns(self):
        """Test applying Ken Burns effect to image"""
        # Skip actual execution if FFmpeg might not be available
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock()
            
            result = AdvancedVideoEffects.apply_Ken_Burns(
                self.test_image,
                self.output_path,
                duration=5,
                zoom_start=1.0,
                zoom_end=1.5,
                direction="in"
            )
            
            # Check that subprocess.run was called
            mock_run.assert_called_once()
            
            # Check that FFmpeg command contains zoompan filter
            args = mock_run.call_args[0][0]
            assert "-vf" in args
            filter_idx = args.index("-vf") + 1
            
            # Check for expected components of Ken Burns effect
            filter_str = args[filter_idx].lower()
            assert "zoompan" in filter_str
            
            # Check output path
            assert result == self.output_path
