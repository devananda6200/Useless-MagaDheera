#!/usr/bin/env python3
"""
Simple script to help replace placeholder images with your Magadheera images
"""

import os
import shutil
from PIL import Image

def clear_old_images():
    """Remove old placeholder images"""
    print("Clearing old placeholder images...")
    
    # Clear characters folder
    chars_dir = "characters"
    if os.path.exists(chars_dir):
        for file in os.listdir(chars_dir):
            if file.endswith('.png'):
                os.remove(os.path.join(chars_dir, file))
                print(f"Removed {file}")
    
    # Clear lovers folder  
    lovers_dir = "lovers"
    if os.path.exists(lovers_dir):
        for file in os.listdir(lovers_dir):
            if file.endswith('.png'):
                os.remove(os.path.join(lovers_dir, file))
                print(f"Removed {file}")

def resize_image(input_path, output_path, target_size):
    """Resize image to target size while maintaining aspect ratio"""
    try:
        with Image.open(input_path) as img:
            # Convert to RGBA for transparency support
            img = img.convert('RGBA')
            
            # Calculate new size maintaining aspect ratio
            img.thumbnail(target_size, Image.Resampling.LANCZOS)
            
            # Create new image with target size and transparent background
            new_img = Image.new('RGBA', target_size, (0, 0, 0, 0))
            
            # Center the resized image
            x = (target_size[0] - img.width) // 2
            y = (target_size[1] - img.height) // 2
            new_img.paste(img, (x, y), img if img.mode == 'RGBA' else None)
            
            # Save the result
            new_img.save(output_path, 'PNG')
            print(f"Resized and saved: {output_path}")
            return True
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False

def setup_new_images():
    """Help user set up new images"""
    print("\nSetting up new images...")
    print("Please place your images in this folder with these exact names:")
    print("- Warrior_Magadheera.png (the warrior with armor)")
    print("- Princess_1.png (first princess/lover)")
    print("- Princess_2.png (second princess/lover)")
    print("\nPress Enter when you've added the images...")
    input()
    
    # Check for warrior image
    warrior_path = "Warrior_Magadheera.png"
    if os.path.exists(warrior_path):
        print("Found warrior image!")
        resize_image(warrior_path, "characters/Warrior_Magadheera.png", (300, 400))
    else:
        print("WARNING: Warrior_Magadheera.png not found!")
    
    # Check for princess images
    for i in range(1, 3):
        princess_path = f"Princess_{i}.png"
        if os.path.exists(princess_path):
            print(f"Found princess {i} image!")
            resize_image(princess_path, f"lovers/Princess_{i}.png", (200, 300))
        else:
            print(f"WARNING: Princess_{i}.png not found!")

def check_setup():
    """Check if images are properly set up"""
    print("\nChecking image setup...")
    
    chars_count = len([f for f in os.listdir("characters") if f.endswith('.png')])
    lovers_count = len([f for f in os.listdir("lovers") if f.endswith('.png')])
    
    print(f"Character images: {chars_count}")
    print(f"Lover images: {lovers_count}")
    
    if chars_count > 0 and lovers_count > 0:
        print("SUCCESS: Images are ready!")
        print("You can now test the app:")
        print("1. python app.py (start backend)")
        print("2. Open http://localhost:3000 (frontend)")
        return True
    else:
        print("WARNING: Missing images. Please add them and run this script again.")
        return False

def main():
    print("MAGADHEERA IMAGE REPLACEMENT TOOL")
    print("=" * 40)
    
    print("\nThis tool will help you replace the placeholder images")
    print("with your actual Magadheera character images.")
    
    choice = input("\nDo you want to clear old images and set up new ones? (y/n): ").lower()
    
    if choice == 'y':
        clear_old_images()
        setup_new_images()
        check_setup()
    else:
        print("Checking current setup...")
        check_setup()
    
    print("\nDone! If you need help, check REPLACE_IMAGES_GUIDE.txt")

if __name__ == "__main__":
    main()
