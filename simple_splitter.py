#!/usr/bin/env python3
"""
Enhanced Media Processor - Command Line Version
"""

import os
import sys

# Auto-configure paths
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

from src.mp3_splitter import MediaProcessor

def main():
    if len(sys.argv) != 3:
        print("Enhanced Media Processor - Command Line Interface")
        print("Supports: MP4, AVI, MOV, WMV + MP3, WAV, FLAC")
        print("Usage: python simple_splitter.py <media_file> <num_parts>")
        print("Example: python simple_splitter.py 'video.mp4' 5")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        num_parts = int(sys.argv[2])
        if num_parts <= 0:
            print("Error: Number of parts must be greater than 0")
            sys.exit(1)
    except ValueError:
        print("Error: Number of parts must be a valid integer")
        sys.exit(1)
    
    try:
        print("🚀 Starting Enhanced Media Processor...")
        processor = MediaProcessor(input_file)
        info = processor.get_media_info()
        
        print(f"Processing: {info['file_name']}")
        print(f"Type: {'Video' if info['is_video'] else 'Audio'}")
        print(f"Duration: {info['formatted_duration']}")
        
        converted_path, output_files = processor.split_media(num_parts)
        
        action = "converted and split" if info['is_video'] else "split"
        print(f"✅ Successfully {action} into {len(output_files)} parts")
        print(f"📁 Location: {os.path.dirname(output_files[0])}")
        
        processor.cleanup()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()