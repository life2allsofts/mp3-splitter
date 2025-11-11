"""
Enhanced utility functions for video and audio processing
"""

import os
from pydub import AudioSegment

def validate_file_path(file_path):
    """Validate if the file exists and is a supported media format."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Supported formats
    supported_extensions = [
        # Video formats
        '.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv', '.webm',
        # Audio formats  
        '.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg'
    ]
    
    file_ext = os.path.splitext(file_path)[1].lower()
    if file_ext not in supported_extensions:
        raise ValueError(f"Unsupported file format: {file_ext}. Supported formats: {', '.join(supported_extensions)}")
    
    return True

def is_video_file(file_path):
    """Check if file is a supported video format."""
    video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv', '.webm']
    file_ext = os.path.splitext(file_path)[1].lower()
    return file_ext in video_extensions

def is_audio_file(file_path):
    """Check if file is a supported audio format."""
    audio_extensions = ['.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg']
    file_ext = os.path.splitext(file_path)[1].lower()
    return file_ext in audio_extensions

def convert_video_to_mp3(input_file, output_file=None, bitrate='320k'):
    """
    Convert video file to MP3 audio file.
    
    Args:
        input_file (str): Path to input video file
        output_file (str): Path for output MP3 file (optional)
        bitrate (str): Audio quality (128k, 192k, 320k)
    
    Returns:
        str: Path to the created MP3 file
    """
    if output_file is None:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}_converted.mp3"
    
    print(f"🎥 Converting video to audio: {os.path.basename(input_file)}")
    print(f"   Input: {input_file}")
    print(f"   Output: {output_file}")
    print(f"   Quality: {bitrate}")
    
    try:
        # Load video and extract audio
        video = AudioSegment.from_file(input_file)
        
        # Export as MP3 with specified quality
        video.export(output_file, format="mp3", bitrate=bitrate)
        
        print(f"✅ Conversion successful: {os.path.basename(output_file)}")
        return output_file
        
    except Exception as e:
        raise RuntimeError(f"Video conversion failed: {str(e)}")

def calculate_part_duration(audio_duration, num_parts):
    """Calculate duration for each part in milliseconds."""
    if num_parts <= 0:
        raise ValueError("Number of parts must be greater than 0")
    return audio_duration / num_parts

def create_output_directory(input_file):
    """Create output directory based on input filename."""
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = f"{base_name}_parts"
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def format_time(milliseconds):
    """Format milliseconds to MM:SS format."""
    seconds = milliseconds / 1000
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def get_file_size(file_path):
    """Get file size in MB."""
    if os.path.exists(file_path):
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)  # Convert to MB
    return 0

def get_media_duration(file_path):
    """Get duration of video or audio file in milliseconds."""
    try:
        media = AudioSegment.from_file(file_path)
        return len(media)
    except Exception as e:
        raise RuntimeError(f"Cannot get duration of {file_path}: {str(e)}")

def get_file_info(file_path):
    """Get comprehensive information about media file."""
    file_ext = os.path.splitext(file_path)[1].lower()
    file_size = get_file_size(file_path)
    
    info = {
        'file_path': file_path,
        'file_name': os.path.basename(file_path),
        'file_extension': file_ext,
        'file_size_mb': round(file_size, 2),
        'is_video': is_video_file(file_path),
        'is_audio': is_audio_file(file_path),
    }
    
    # Get duration if possible
    try:
        duration_ms = get_media_duration(file_path)
        duration_seconds = duration_ms / 1000
        info.update({
            'duration_ms': duration_ms,
            'duration_seconds': round(duration_seconds, 2),
            'duration_minutes': round(duration_seconds / 60, 2),
            'formatted_duration': format_time(duration_ms)
        })
    except:
        info['duration_ms'] = 0
        info['formatted_duration'] = 'Unknown'
    
    return info