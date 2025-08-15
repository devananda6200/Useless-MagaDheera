#!/usr/bin/env python3
"""
Magadheera Past Life Reveal - Backend Startup Script
"""

import os
import sys
import subprocess
import uvicorn

def check_dependencies():
    """Check if all required packages are installed"""
    try:
        import fastapi
        import cv2
        import PIL
        import mediapipe
        import numpy
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def check_image_folders():
    """Check if image folders exist and have content"""
    characters_dir = "characters"
    lovers_dir = "lovers"
    
    if not os.path.exists(characters_dir):
        print(f"❌ {characters_dir} folder not found")
        return False
    
    if not os.path.exists(lovers_dir):
        print(f"❌ {lovers_dir} folder not found")
        return False
    
    character_files = [f for f in os.listdir(characters_dir) if f.lower().endswith('.png')]
    lover_files = [f for f in os.listdir(lovers_dir) if f.lower().endswith('.png')]
    
    print(f"📁 Found {len(character_files)} character images")
    print(f"💕 Found {len(lover_files)} lover images")
    
    if len(character_files) == 0:
        print("⚠️  No character images found. Run create_placeholders.py to create sample images.")
        return False
    
    return True

def main():
    print("🏰 Starting Magadheera Past Life Reveal Backend...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check image folders
    if not check_image_folders():
        print("\n🔧 Creating placeholder images...")
        try:
            subprocess.run([sys.executable, "create_placeholders.py"], check=True)
            print("✅ Placeholder images created successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to create placeholder images")
            sys.exit(1)
    
    print("\n🚀 Starting FastAPI server...")
    print("📡 API will be available at: http://localhost:8000")
    print("📖 API documentation: http://localhost:8000/docs")
    print("🏥 Health check: http://localhost:8000/health")
    print("\n⚠️  Make sure your frontend is configured to use http://localhost:8000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start the server
    try:
        uvicorn.run(
            "app:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
