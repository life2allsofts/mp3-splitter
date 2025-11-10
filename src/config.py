"""
FFmpeg configuration for MP3 Splitter - Auto-Configuring Version
"""

import os
import sys
import glob
from pydub import AudioSegment

# Cache for found paths to avoid repeated searches
_FFMPEG_CACHE = {
    'ffmpeg': None,
    'ffprobe': None,
    'project_root': None
}

def find_ffmpeg_automatically():
    """
    Automatically find FFmpeg in common locations without manual configuration.
    Search order:
    1. Project's ffmpeg/bin folder
    2. System PATH
    3. Common installation directories
    """
    # Get project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    _FFMPEG_CACHE['project_root'] = project_root
    
    # Priority 1: Project's ffmpeg folder (various possible structures)
    project_paths = [
        os.path.join(project_root, "ffmpeg", "bin", "ffmpeg.exe"),
        os.path.join(project_root, "ffmpeg", "ffmpeg.exe"),
        os.path.join(project_root, "ffmpeg-win64", "bin", "ffmpeg.exe"),
        os.path.join(project_root, "ffmpeg", "bin", "ffmpeg"),  # Linux/Mac
        os.path.join(project_root, "ffmpeg", "ffmpeg"),         # Linux/Mac
    ]
    
    for ffmpeg_path in project_paths:
        if os.path.exists(ffmpeg_path):
            _FFMPEG_CACHE['ffmpeg'] = ffmpeg_path
            # Find corresponding ffprobe
            ffprobe_path = ffmpeg_path.replace("ffmpeg", "ffprobe")
            if os.path.exists(ffprobe_path):
                _FFMPEG_CACHE['ffprobe'] = ffprobe_path
            return True
    
    # Priority 2: System PATH
    try:
        import shutil
        system_ffmpeg = shutil.which("ffmpeg")
        if system_ffmpeg:
            _FFMPEG_CACHE['ffmpeg'] = system_ffmpeg
            system_ffprobe = shutil.which("ffprobe") or shutil.which("ffmpeg")  # ffmpeg often includes ffprobe
            _FFMPEG_CACHE['ffprobe'] = system_ffprobe
            return True
    except:
        pass
    
    return False

def setup_ffmpeg():
    """
    Auto-configure FFmpeg paths. This function is self-healing and will
    automatically find FFmpeg in various locations without manual updates.
    """
    # If already configured, return cached values
    if _FFMPEG_CACHE['ffmpeg'] and os.path.exists(_FFMPEG_CACHE['ffmpeg']):
        return True
    
    print("🔄 Auto-configuring FFmpeg...")
    
    if find_ffmpeg_automatically():
        ffmpeg_path = _FFMPEG_CACHE['ffmpeg']
        ffprobe_path = _FFMPEG_CACHE['ffprobe']
        
        # Configure pydub
        AudioSegment.converter = ffmpeg_path
        AudioSegment.ffprobe = ffprobe_path or ffmpeg_path.replace("ffmpeg", "ffprobe")

        if ffprobe_path and os.path.exists(ffprobe_path):
            AudioSegment.ffprobe = ffprobe_path
            print(f"✅ FFprobe auto-configured: {os.path.basename(ffprobe_path)}")
        
        print(f"✅ FFmpeg auto-configured: {os.path.basename(ffmpeg_path)}")
        print(f"📁 Location: {os.path.dirname(ffmpeg_path)}")
        return True
    else:
        print("❌ Could not auto-configure FFmpeg")
        print("💡 Please ensure FFmpeg is either:")
        print("   1. In project/ffmpeg/bin/ folder")
        print("   2. In system PATH")
        print("   3. In a standard installation location")
        return False

def get_ffmpeg_path():
    """Get the full path to ffmpeg executable."""
    if _FFMPEG_CACHE['ffmpeg'] and os.path.exists(_FFMPEG_CACHE['ffmpeg']):
        return _FFMPEG_CACHE['ffmpeg']
    return None

def get_ffprobe_path():
    """Get the full path to ffprobe executable."""
    if _FFMPEG_CACHE['ffprobe'] and os.path.exists(_FFMPEG_CACHE['ffprobe']):
        return _FFMPEG_CACHE['ffprobe']
    return None

def get_ffmpeg_info():
    """Get information about the configured FFmpeg."""
    return {
        'ffmpeg_path': _FFMPEG_CACHE['ffmpeg'],
        'ffprobe_path': _FFMPEG_CACHE['ffprobe'],
        'project_root': _FFMPEG_CACHE['project_root'],
        'is_configured': _FFMPEG_CACHE['ffmpeg'] is not None and os.path.exists(_FFMPEG_CACHE['ffmpeg'])
    }

# Auto-configure on import
if setup_ffmpeg():
    print("🚀 FFmpeg auto-configuration completed successfully!")
else:
    print("⚠️  FFmpeg auto-configuration failed - manual setup may be required")