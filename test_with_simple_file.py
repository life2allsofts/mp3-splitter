import os
from pydub import AudioSegment
from pydub.generators import Sine

def create_test_mp3():
    """Create a simple test MP3 file in the current directory"""
    output_path = "test_audio.mp3"
    
    # Generate a 10-second sine wave
    print("Creating test audio file...")
    sine_wave = Sine(440).to_audio_segment(duration=10000)  # 440 Hz for 10 seconds
    
    # Export as MP3
    sine_wave.export(output_path, format="mp3", bitrate="192k")
    print(f"✅ Created test file: {output_path}")
    return output_path

def test_with_simple_file():
    """Test with a simple generated MP3 file"""
    from src.config import setup_ffmpeg
    
    print("Testing with simple generated MP3...")
    setup_ffmpeg()
    
    # Create test file
    test_file = create_test_mp3()
    
    try:
        # Try to load it
        audio = AudioSegment.from_mp3(test_file)
        print(f"✅ Successfully loaded test file! Duration: {len(audio)}ms")
        
        # Try splitting
        parts = 3
        part_duration = len(audio) // parts
        
        for i in range(parts):
            start = i * part_duration
            end = (i + 1) * part_duration if i < parts - 1 else len(audio)
            part = audio[start:end]
            part.export(f"test_part_{i+1}.mp3", format="mp3")
            print(f"✅ Created part {i+1}")
            
        print("🎉 All tests passed! The issue is with your specific file path.")
        
    except Exception as e:
        print(f"❌ Failed with test file: {e}")
    finally:
        # Clean up
        for file in [test_file, "test_part_1.mp3", "test_part_2.mp3", "test_part_3.mp3"]:
            if os.path.exists(file):
                os.remove(file)

if __name__ == "__main__":
    test_with_simple_file()