import os
import sys
import subprocess

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

from src.config import setup_ffmpeg

def test_direct_ffmpeg():
    """Test FFmpeg directly with your file"""
    
    # Your file path
    input_file = r"D:\ISAAC\QUANTIC\Wisdom Word GH\Songs\new26-10-25\New26-10-25\alphabets-journey (1).mp3"
    
    print("🎵 Testing Direct FFmpeg Access")
    print("=" * 50)
    
    # Setup FFmpeg
    setup_ffmpeg()
    
    # Test 1: Check file info with FFprobe
    print("1. Testing FFprobe...")
    try:
        cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', input_file]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ FFprobe can read the file!")
        else:
            print(f"❌ FFprobe failed: {result.stderr}")
    except Exception as e:
        print(f"❌ FFprobe error: {e}")
    
    # Test 2: Test conversion with FFmpeg
    print("\n2. Testing FFmpeg conversion...")
    try:
        output_file = "test_output.wav"
        cmd = ['ffmpeg', '-i', input_file, '-t', '5', output_file]  # Convert first 5 seconds
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ FFmpeg can process the file!")
            # Clean up
            if os.path.exists(output_file):
                os.remove(output_file)
        else:
            print(f"❌ FFmpeg failed: {result.stderr}")
    except Exception as e:
        print(f"❌ FFmpeg error: {e}")

if __name__ == "__main__":
    test_direct_ffmpeg()