#!/usr/bin/env python3
"""
MP3 File Splitter - Working Version
"""

import os
import sys

# Add src to path - FIXED PATH
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    from src.mp3_splitter import MP3Splitter
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure the src folder exists with mp3_splitter.py and utils.py")
    sys.exit(1)

def validate_mp3_file(file_path):
    """Enhanced file validation."""
    file_path = file_path.strip().strip('"')
    
    if not os.path.exists(file_path):
        return False, "File does not exist"
    
    if not file_path.lower().endswith('.mp3'):
        return False, "File is not an MP3 file"
    
    try:
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            return False, "File is empty"
        if file_size < 1024:  # Less than 1KB
            return False, "File is too small to be a valid MP3"
    except OSError:
        return False, "Cannot access file"
    
    return True, "Valid MP3 file"

def main():
    print("🎵 MP3 File Splitter")
    print("====================")
    
    try:
        # Get input file path
        input_file = input("Enter the path to your MP3 file: ").strip()
        
        # Enhanced file validation
        is_valid, message = validate_mp3_file(input_file)
        if not is_valid:
            print(f"❌ Error: {message}")
            print("Please check the file path and try again.")
            return
        
        print(f"✅ File validation: {message}")
        
        # Get number of parts
        try:
            num_parts = int(input("Enter the number of parts to split into: "))
            if num_parts <= 0:
                print("❌ Error: Number of parts must be greater than 0!")
                return
            if num_parts > 50:
                print("⚠️  Warning: Large number of parts may take time")
        except ValueError:
            print("❌ Error: Please enter a valid number!")
            return
        
        # Create splitter instance
        print("\n🚀 Initializing MP3 Splitter...")
        splitter = MP3Splitter(input_file)
        info = splitter.get_audio_info()
        
        print(f"\n📊 File Information:")
        print(f"   Name: {info['file_name']}")
        print(f"   Size: {info['file_size_mb']} MB")
        print(f"   Duration: {info['formatted_duration']} ({info['duration_minutes']:.2f} minutes)")
        print(f"   Parts: {num_parts}")
        print(f"   Each part: ~{info['duration_seconds']/num_parts:.2f} seconds")
        
        # Confirm splitting
        confirm = input("\nProceed with splitting? (y/n): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("Operation cancelled.")
            return
        
        # Split the file
        print(f"\nStarting split process...")
        output_files = splitter.split_mp3(num_parts)
        
        print(f"\n🎉 Successfully created {len(output_files)} parts!")
        print(f"📁 Output folder: {os.path.dirname(output_files[0])}")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Operation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()