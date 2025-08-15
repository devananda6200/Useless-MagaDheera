#!/usr/bin/env python3
"""
Simple launcher for the Magadheera Image Manager
"""

import sys
import os

def main():
    print("🏰 MAGADHEERA IMAGE MANAGER LAUNCHER")
    print("=" * 40)
    
    try:
        # Try to import tkinter
        import tkinter as tk
        print("✅ GUI support detected")
        
        # Launch the image manager
        print("🚀 Starting Image Manager...")
        from image_manager import MagadheeraImageManager
        
        app = MagadheeraImageManager()
        app.run()
        
    except ImportError:
        print("❌ GUI not available (tkinter not installed)")
        print("🔄 Falling back to command line tool...")
        
        # Fall back to command line tool
        import subprocess
        subprocess.run([sys.executable, "add_custom_images.py"])
        
    except Exception as e:
        print(f"❌ Error starting Image Manager: {e}")
        print("🔄 Trying command line tool...")
        
        try:
            import subprocess
            subprocess.run([sys.executable, "add_custom_images.py"])
        except Exception as e2:
            print(f"❌ Command line tool also failed: {e2}")
            print("\n📋 Manual instructions:")
            print("1. Copy your warrior images to: characters/ folder")
            print("2. Copy your princess images to: lovers/ folder")
            print("3. Restart backend: python app.py")

if __name__ == "__main__":
    main()
