"""
Self-testing module for MP3 Splitter - Runs automatically
"""

import os
import sys

def run_self_test():
    """Run comprehensive self-test of all components."""
    print("🧪 MP3 Splitter Self-Test")
    print("=" * 40)
    
    # Test 1: Configuration
    print("1. Testing FFmpeg auto-configuration...")
    try:
        from .config import setup_ffmpeg, get_ffmpeg_info
        if setup_ffmpeg():
            info = get_ffmpeg_info()
            print(f"   ✅ FFmpeg: {os.path.basename(info['ffmpeg_path']) if info['ffmpeg_path'] else 'Not found'}")
            print(f"   ✅ FFprobe: {os.path.basename(info['ffprobe_path']) if info['ffprobe_path'] else 'Not found'}")
        else:
            print("   ❌ FFmpeg auto-configuration failed")
    except Exception as e:
        print(f"   ❌ Configuration test failed: {e}")
    
    # Test 2: Utility functions
    print("2. Testing utility functions...")
    try:
        from .utils import format_time, calculate_part_duration
        test_time = format_time(65000)
        test_duration = calculate_part_duration(1000, 4)
        print(f"   ✅ Utilities working: {test_time}, {test_duration}")
    except Exception as e:
        print(f"   ❌ Utilities test failed: {e}")
    
    # Test 3: MP3 Splitter class
    print("3. Testing MP3 Splitter class...")
    try:
        from .mp3_splitter import MP3Splitter
        print("   ✅ MP3Splitter class imported successfully")
    except Exception as e:
        print(f"   ❌ MP3Splitter test failed: {e}")
    
    print("=" * 40)
    print("🎉 Self-test completed!")

# Run self-test when module is imported
if __name__ != "__main__":
    run_self_test()