"""
Enhanced MP3 Splitter with Video-to-Audio conversion support
"""

import os
from pydub import AudioSegment
from .utils import (
    validate_file_path, calculate_part_duration, create_output_directory, 
    format_time, get_file_size, is_video_file, convert_video_to_mp3, get_file_info
)
from .config import setup_ffmpeg

class MediaProcessor:
    """
    Enhanced processor that handles both video conversion and audio splitting
    """
    
    def __init__(self, input_file):
        # Setup FFmpeg first
        if not setup_ffmpeg():
            raise RuntimeError("FFmpeg configuration failed. Cannot proceed.")
        
        # Validate and clean the file path
        input_file = os.path.abspath(input_file.strip().strip('"'))
        validate_file_path(input_file)
        self.input_file = input_file
        self.is_video = is_video_file(input_file)
        self.converted_mp3_path = None
        
        print("📁 Analyzing media file...")
        self.file_info = get_file_info(input_file)
        
        print(f"📊 File Type: {'Video' if self.is_video else 'Audio'}")
        print(f"📏 File size: {self.file_info['file_size_mb']} MB")
        print(f"⏱️  Duration: {self.file_info['formatted_duration']}")
        
    def convert_to_mp3(self, output_path=None, bitrate='320k'):
        """
        Convert video file to MP3 if it's a video file.
        If it's already audio, returns the original path.
        
        Args:
            output_path (str): Custom output path for converted file
            bitrate (str): Audio quality setting
            
        Returns:
            str: Path to MP3 file ready for splitting
        """
        if not self.is_video:
            print("✅ File is already audio, no conversion needed")
            return self.input_file
        
        print("🎥 Video file detected, converting to MP3...")
        self.converted_mp3_path = convert_video_to_mp3(
            self.input_file, 
            output_path, 
            bitrate
        )
        return self.converted_mp3_path
    
    def load_audio_for_splitting(self, bitrate='320k'):
        """
        Prepare audio for splitting - converts video if necessary.
        
        Returns:
            AudioSegment: Loaded audio ready for splitting
        """
        # Convert to MP3 if it's a video
        mp3_path = self.convert_to_mp3(bitrate=bitrate)
        
        print("📁 Loading audio for splitting...")
        try:
            self.audio = AudioSegment.from_mp3(mp3_path)
            self.duration = len(self.audio)
            print("✅ Audio loaded successfully for splitting")
            return self.audio
        except Exception as e:
            raise RuntimeError(f"Failed to load audio for splitting: {str(e)}")
    
    def split_media(self, num_parts, output_dir=None, bitrate='320k'):
        """
        Main method: Convert video to MP3 (if needed) and split into parts.
        
        Args:
            num_parts (int): Number of parts to split into
            output_dir (str): Custom output directory
            bitrate (str): Audio quality for conversion
            
        Returns:
            tuple: (converted_mp3_path, list_of_split_files)
        """
        if num_parts <= 0:
            raise ValueError("Number of parts must be greater than 0")
        
        # Load audio (converts video if necessary)
        self.load_audio_for_splitting(bitrate)
        
        # Create output directory
        base_name = os.path.splitext(os.path.basename(self.input_file))[0]
        if output_dir is None:
            output_dir = f"{base_name}_parts"
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
            part_audio.export(output_path, format="mp3", bitrate=bitrate)
            output_files.append(output_path)
            
            print(f"✅ {output_filename} ({format_time(start_time)} - {format_time(end_time)})")
        
        return self.converted_mp3_path, output_files
    
    def get_media_info(self):
        """Get comprehensive information about the media file."""
        return self.file_info
    
    def cleanup(self):
        """Clean up any temporary converted files."""
        if self.converted_mp3_path and os.path.exists(self.converted_mp3_path):
            # Only delete if it was created during this session
            if self.converted_mp3_path != self.input_file:
                os.remove(self.converted_mp3_path)
                print(f"🧹 Cleaned up temporary file: {self.converted_mp3_path}")