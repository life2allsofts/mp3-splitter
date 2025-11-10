import os

def verify_file(file_path):
    """Verify that a specific file exists and is accessible."""
    file_path = file_path.strip().strip('"')
    
    print(f"🔍 Verifying file: {file_path}")
    print("=" * 50)
    
    # Check if file exists
    if not os.path.exists(file_path):
        print("❌ File does not exist")
        return False
    
    print("✅ File exists")
    
    # Check file size
    try:
        file_size = os.path.getsize(file_path)
        print(f"📏 File size: {file_size} bytes ({file_size / (1024*1024):.2f} MB)")
        
        if file_size == 0:
            print("❌ File is empty")
            return False
    except OSError as e:
        print(f"❌ Cannot access file: {e}")
        return False
    
    # Check file extension
    if not file_path.lower().endswith('.mp3'):
        print("⚠️  Warning: File does not have .mp3 extension")
    else:
        print("✅ File has .mp3 extension")
    
    # Check if readable
    try:
        with open(file_path, 'rb') as f:
            header = f.read(4)
            print(f"📄 File header: {header}")
    except Exception as e:
        print(f"❌ Cannot read file: {e}")
        return False
    
    print("✅ File is readable")
    return True

if __name__ == "__main__":
    # Test your specific file
    test_file = r"D:\ISAAC\QUANTIC\Wisdom Word GH\Songs\new26-10-25\New26-10-25\alphabets-journey (1).mp3"
    verify_file(test_file)