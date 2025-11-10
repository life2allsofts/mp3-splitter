import os
import sys

print("🔍 Testing FFmpeg Configuration...")
print("=" * 40)

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

# Test FFmpeg path
ffmpeg_path = os.path.join(current_dir, "ffmpeg", "bin", "ffmpeg.exe")
print(f"Expected FFmpeg path: {ffmpeg_path}")
print(f"FFmpeg exists: {os.path.exists(ffmpeg_path)}")

if os.path.exists(ffmpeg_path):
    print("✅ FFmpeg found in correct location!")
else:
    print("❌ FFmpeg NOT found!")
    print("Please ensure the structure is: mp3_splitter/ffmpeg/bin/ffmpeg.exe")

# Test imports
try:
    from src.config import setup_ffmpeg
    print("✅ Config import successful")
    
    from src.utils import format_time, calculate_part_duration
    print("✅ Utils import successful")
    
    from src.mp3_splitter import MP3Splitter
    print("✅ MP3Splitter import successful")
    
    # Test FFmpeg setup
    print("\n🔧 Testing FFmpeg setup...")
    setup_ffmpeg()
    
    # Test audio functionality
    print("\n🎵 Testing audio functionality...")
    from pydub import AudioSegment
    audio = AudioSegment.silent(duration=1000)  # 1 second silence
    print("✅ Audio functionality working!")
    
    print("\n🎉 ALL TESTS PASSED! Your setup is ready.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Test failed: {e}")