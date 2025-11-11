#!/usr/bin/env python3
"""
Enhanced Media Processor - Video to Audio Converter + MP3 Splitter
"""

import os
import sys

# Auto-configure paths
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    from src.mp3_splitter import MediaProcessor
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def main():
    print("🎵 Enhanced Media Processor")
    print("===========================")
    print("Supports: MP4, AVI, MOV, WMV + MP3, WAV, FLAC")
    print("")
    
    try:
        # Get input file path
        input_file = input("Enter the path to your media file: ").strip()
        input_file = input_file.strip('"')
        
        # Validate file exists
        if not os.path.exists(input_file):
            print("❌ Error: File not found!")
            return
        
        # Create processor instance
        print("\n🚀 Initializing Media Processor...")
        processor = MediaProcessor(input_file)
        info = processor.get_media_info()
        
        # Display file information
        print(f"\n📊 Media Information:")
        print(f"   Name: {info['file_name']}")
        print(f"   Type: {'Video' if info['is_video'] else 'Audio'}")
        print(f"   Size: {info['file_size_mb']} MB")
        print(f"   Duration: {info['formatted_duration']}")
        
        # Get number of parts
        try:
            num_parts = int(input("\nEnter the number of parts to split into: "))
            if num_parts <= 0:
                print("❌ Error: Number of parts must be greater than 0!")
                return
        except ValueError:
            print("❌ Error: Please enter a valid number!")
            return
        
        # Confirm processing
        action = "convert and split" if info['is_video'] else "split"
        confirm = input(f"\nProceed with {action}? (y/n): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("Operation cancelled.")
            return
        
        # Process the media file
        print(f"\nStarting {action} process...")
        converted_path, output_files = processor.split_media(num_parts)
        
        # Display results
        print(f"\n🎉 Successfully created {len(output_files)} parts!")
        if info['is_video']:
            print(f"🎥 Converted: {os.path.basename(converted_path)}")
        print(f"📁 Output folder: {os.path.dirname(output_files[0])}")
        
        # Cleanup temporary files
        processor.cleanup()
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()