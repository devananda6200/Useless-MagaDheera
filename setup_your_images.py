#!/usr/bin/env python3
"""
Complete Image Setup Wizard for Magadheera
Guides users through replacing placeholder images with their custom images
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def print_banner():
    """Print the setup banner"""
    print("""
🏰 ═══════════════════════════════════════════════════════════════ 🏰
    
    ⚔️  MAGADHEERA IMAGE SETUP WIZARD  ⚔️
    
    Replace placeholder images with your custom characters!
    
🏰 ═══════════════════════════════════════════════════════════════ 🏰
""")

def check_current_images():
    """Check current image status"""
    print("🔍 Checking current images...")
    
    chars_dir = Path("characters")
    lovers_dir = Path("lovers")
    
    char_files = list(chars_dir.glob("*.png")) if chars_dir.exists() else []
    lover_files = list(lovers_dir.glob("*.png")) if lovers_dir.exists() else []
    
    print(f"📁 Characters folder: {len(char_files)} images")
    for file in char_files:
        print(f"   - {file.name}")
    
    print(f"💕 Lovers folder: {len(lover_files)} images")
    for file in lover_files:
        print(f"   - {file.name}")
    
    return len(char_files), len(lover_files)

def show_setup_options():
    """Show available setup options"""
    print("\n🎯 CHOOSE YOUR SETUP METHOD:")
    print("=" * 50)
    print("1. 🖱️  GUI Image Manager (Easy drag & drop)")
    print("2. 🚀 Smart Image Converter (Auto face detection)")
    print("3. 📁 Quick File Browser (Simple file selection)")
    print("4. 🔄 Quick Drag & Drop Tool")
    print("5. 📋 Manual Instructions")
    print("6. 🌐 Test Current Setup")
    print("7. 🗑️  Clear All Images")
    print("8. ❌ Exit")
    print("=" * 50)

def launch_gui_manager():
    """Launch the GUI image manager"""
    print("🚀 Starting GUI Image Manager...")
    try:
        subprocess.Popen([sys.executable, "image_manager.py"])
        print("✅ GUI Image Manager launched!")
        print("📝 Use the GUI to add your warrior and princess images")
        return True
    except Exception as e:
        print(f"❌ Failed to launch GUI: {e}")
        return False

def launch_smart_converter():
    """Launch the smart image converter"""
    print("🧠 Starting Smart Image Converter...")
    try:
        subprocess.Popen([sys.executable, "smart_image_converter.py"])
        print("✅ Smart Converter launched!")
        print("📝 This tool will auto-detect faces and optimize your images")
        return True
    except Exception as e:
        print(f"❌ Failed to launch converter: {e}")
        return False

def launch_quick_replacer():
    """Launch the quick drag & drop replacer"""
    print("⚡ Starting Quick Drag & Drop Tool...")
    try:
        subprocess.Popen([sys.executable, "quick_replace_images.py"])
        print("✅ Quick Replacer launched!")
        print("📝 Drag and drop your images into the tool")
        return True
    except Exception as e:
        print(f"❌ Failed to launch replacer: {e}")
        return False

def simple_file_browser():
    """Simple file browser method"""
    print("📁 Simple File Browser Method")
    print("=" * 30)
    
    try:
        subprocess.run([sys.executable, "add_custom_images.py"])
        return True
    except Exception as e:
        print(f"❌ Failed to run file browser: {e}")
        return False

def show_manual_instructions():
    """Show manual setup instructions"""
    print("\n📋 MANUAL SETUP INSTRUCTIONS")
    print("=" * 40)
    print("""
🏰 WARRIOR/CHARACTER IMAGES (for face replacement):
   1. Save your warrior images (PNG, JPG, JPEG)
   2. Copy them to: backend/characters/
   3. Recommended size: 300x400 pixels
   4. These will replace faces in the app

👸 PRINCESS/LOVER IMAGES (floating companions):
   1. Save your princess images (PNG, JPG, JPEG)  
   2. Copy them to: backend/lovers/
   3. Recommended size: 200x300 pixels
   4. These appear as floating images

📐 OPTIMAL IMAGE SPECS:
   - Format: PNG (supports transparency)
   - Warriors: Clear face portraits, front-facing
   - Princesses: Full body or portrait shots
   - High quality, good lighting

🔄 AFTER ADDING IMAGES:
   1. Restart the backend server: python app.py
   2. Test the app: http://localhost:3000
   3. Your custom images will now be used!

📁 FOLDER STRUCTURE:
   backend/
   ├── characters/     (warrior images here)
   ├── lovers/         (princess images here)
   └── app.py
""")

def test_current_setup():
    """Test the current image setup"""
    print("🧪 Testing current setup...")
    
    char_count, lover_count = check_current_images()
    
    if char_count == 0:
        print("⚠️ No character images found!")
        print("   Add warrior images for face replacement")
    else:
        print(f"✅ {char_count} character images ready")
    
    if lover_count == 0:
        print("⚠️ No lover images found!")
        print("   Add princess images for floating companions")
    else:
        print(f"✅ {lover_count} lover images ready")
    
    if char_count > 0 or lover_count > 0:
        print("\n🌐 Opening Magadheera app to test...")
        try:
            webbrowser.open('http://localhost:3000')
            print("✅ App opened in browser")
        except:
            print("⚠️ Could not open browser automatically")
            print("   Manually open: http://localhost:3000")
    else:
        print("\n❌ No images to test. Please add some images first.")

def clear_all_images():
    """Clear all custom images"""
    print("🗑️ Clearing all custom images...")
    
    if input("Are you sure? This will delete all custom images (y/N): ").lower() != 'y':
        print("❌ Operation cancelled")
        return
    
    try:
        # Clear directories
        for directory in ["characters", "lovers"]:
            if os.path.exists(directory):
                for file in os.listdir(directory):
                    if file.endswith('.png'):
                        os.remove(os.path.join(directory, file))
                        print(f"   Deleted {file}")
        
        # Recreate placeholders
        subprocess.run([sys.executable, "create_placeholders.py"], check=True)
        print("✅ All images cleared and placeholders restored")
        
    except Exception as e:
        print(f"❌ Failed to clear images: {e}")

def main():
    """Main setup wizard"""
    print_banner()
    
    while True:
        print()
        check_current_images()
        show_setup_options()
        
        try:
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == '1':
                launch_gui_manager()
            elif choice == '2':
                launch_smart_converter()
            elif choice == '3':
                simple_file_browser()
            elif choice == '4':
                launch_quick_replacer()
            elif choice == '5':
                show_manual_instructions()
            elif choice == '6':
                test_current_setup()
            elif choice == '7':
                clear_all_images()
            elif choice == '8':
                print("\n👋 Goodbye! Your Magadheera adventure awaits!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-8.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Setup wizard interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🎯 NEXT STEPS:")
    print("1. Make sure backend is running: python app.py")
    print("2. Open the app: http://localhost:3000")
    print("3. Test face replacement with your custom images!")
    print("\n🏰 Enjoy your Magadheera transformation! ⚔️")

if __name__ == "__main__":
    main()
