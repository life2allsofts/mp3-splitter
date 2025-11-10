"""
Main MP3 splitting logic - Self-Configuring Version
"""

import os
import subprocess
from pydub import AudioSegment
from .utils import validate_file_path, calculate_part_duration, create_output_directory, format_time, get_file_size
from .config import setup_ffmpeg, get_ffmpeg_path, get_ffprobe_path

class MP3Splitter:
    def __init__(self, input_file):
        # Auto-configure FFmpeg on initialization
        if not setup_ffmpeg():
            raise RuntimeError("FFmpeg auto-configuration failed. Please ensure FFmpeg is available.")
        
        # Validate and clean the file path
        input_file = os.path.abspath(input_file.strip().strip('"'))
        validate_file_path(input_file)
        self.input_file = input_file
        
        print("📁 Loading audio file...")
        try:
            # Test if file is accessible
            file_size = os.path.getsize(input_file)
            print(f"📏 File size: {file_size / (1024*1024):.2f} MB")
            
            # Try to load audio with auto-configured FFmpeg
            self.audio = AudioSegment.from_mp3(input_file)
            self.duration = len(self.audio)
            self.file_size = get_file_size(input_file)
            print("✅ Audio file loaded successfully")
            
        except Exception as e:
            raise RuntimeError(f"Failed to load audio file: {str(e)}")
    
    def split_mp3(self, num_parts, output_dir=None):
        """Split MP3 file into specified number of parts."""
        if num_parts <= 0:
            raise ValueError("Number of parts must be greater than 0")
        
        if num_parts > 100:
            raise ValueError("Number of parts cannot exceed 100 for performance reasons")
        
        if output_dir is None:
            output_dir = create_output_directory(self.input_file)
        else:
            os.makedirs(output_dir, exist_ok=True)
        
        part_duration = calculate_part_duration(self.duration, num_parts)
        output_files = []
        
        print(f"✂️  Splitting '{os.path.basename(self.input_file)}' into {num_parts} parts...")
        print(f"📁 Output directory: {output_dir}")
        print(f"⏱️  Duration per part: {format_time(part_duration)}")
        
        for i in range(num_parts):
            start_time = int(i * part_duration)
            end_time = int((i + 1) * part_duration)
            
            # For the last part, ensure we include the remaining audio
            if i == num_parts - 1:
                end_time = self.duration
            
            part_audio = self.audio[start_time:end_time]
            output_filename = f"part_{i+1:03d}.mp3"
            output_path = os.path.join(output_dir, output_filename)
            
            print(f"  Creating part {i+1}/{num_parts}...", end=" ")
            part_audio.export(output_path, format="mp3")
            output_files.append(output_path)
            
            print(f"✅ {output_filename} ({format_time(start_time)} - {format_time(end_time)})")
        
        return output_files
    
    def get_audio_info(self):
        """Get information about the audio file."""
        duration_seconds = self.duration / 1000
        return {
            'file_path': self.input_file,
            'file_name': os.path.basename(self.input_file),
            'file_size_mb': round(self.file_size, 2),
            'duration_ms': self.duration,
            'duration_seconds': round(duration_seconds, 2),
            'duration_minutes': round(duration_seconds / 60, 2),
            'formatted_duration': format_time(self.duration)
        }