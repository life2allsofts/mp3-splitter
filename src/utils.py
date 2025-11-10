import os
from pydub import AudioSegment

def validate_file_path(file_path):
    """Validate if the file exists and is an MP3 file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    if not file_path.lower().endswith('.mp3'):
        raise ValueError("File must be an MP3 file")
    return True

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