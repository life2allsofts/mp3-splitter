#!/usr/bin/env python3
"""
MP3 File Splitter - Simple Command Line Version
"""

import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.mp3_splitter import MP3Splitter

def main():
    if len(sys.argv) != 3:
        print("Usage: python simple_splitter.py <input_file> <num_parts>")
        print("Example: python simple_splitter.py song.mp3 5")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        num_parts = int(sys.argv[2])
    except ValueError:
        print("Error: Number of parts must be a valid integer")
        sys.exit(1)
    
    try:
        print("🚀 Starting MP3 splitter...")
        splitter = MP3Splitter(input_file)
        info = splitter.get_audio_info()
        print(f"Splitting: {info['file_name']} ({info['formatted_duration']})")
        
        output_files = splitter.split_mp3(num_parts)
        print(f"✅ Successfully created {len(output_files)} parts in '{os.path.dirname(output_files[0])}'")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()