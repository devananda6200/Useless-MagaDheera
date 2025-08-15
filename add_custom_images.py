#!/usr/bin/env python3
"""
Tool to help add your custom Magadheera images to the project
"""

import os
import shutil
from PIL import Image
import requests
from io import BytesIO

def clear_existing_images():
    """Remove existing placeholder images"""
    print("🧹 Clearing existing placeholder images...")
    
    # Clear characters folder
    chars_dir = "characters"
    if os.path.exists(chars_dir):
        for file in os.listdir(chars_dir):
            if file.endswith('.png'):
                file_path = os.path.join(chars_dir, file)
                os.remove(file_path)
                print(f"  Removed: {file}")
    
    # Clear lovers folder
    lovers_dir = "lovers"
    if os.path.exists(lovers_dir):
        for file in os.listdir(lovers_dir):
            if file.endswith('.png'):
                file_path = os.path.join(lovers_dir, file)
                os.remove(file_path)
                print(f"  Removed: {file}")

def process_image(input_path, output_path, target_size, image_type):
    """Process and resize image for the app"""
    try:
        print(f"📸 Processing {image_type}: {input_path}")
        
        # Open and convert image
        with Image.open(input_path) as img:
            print(f"  Original size: {img.size}")
            print(f"  Original mode: {img.mode}")
            
            # Convert to RGBA for transparency support
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Calculate new size maintaining aspect ratio
            img.thumbnail(target_size, Image.Resampling.LANCZOS)
            
            # Create new image with target size and transparent background
            new_img = Image.new('RGBA', target_size, (0, 0, 0, 0))
            
            # Center the resized image
            x = (target_size[0] - img.width) // 2
            y = (target_size[1] - img.height) // 2
            new_img.paste(img, (x, y), img)
            
            # Save the processed image
            new_img.save(output_path, 'PNG')
            print(f"  ✅ Saved: {output_path} ({new_img.size})")
            return True
            
    except Exception as e:
        print(f"  ❌ Error processing {input_path}: {e}")
        return False

def add_images_interactively():
    """Interactive process to add images"""
    print("\n🎭 ADDING YOUR MAGADHEERA IMAGES")
    print("=" * 40)

    print("\nYou can add:")
    print("1. 🏰 WARRIOR/CHARACTER IMAGES - for face replacement")
    print("2. 👸 PRINCESS/LOVER IMAGES - for floating companions")
    print("\nTip: You can drag and drop files into this terminal!")

    # Get warrior images (allow multiple)
    print("\n🏰 ADDING WARRIOR/CHARACTER IMAGES:")
    print("Enter paths one by one (press Enter with empty line to finish)")

    warrior_count = 0
    while True:
        warrior_path = input(f"Warrior image {warrior_count + 1} (or Enter to finish): ").strip().strip('"')

        if not warrior_path:
            break

        if os.path.exists(warrior_path):
            # Generate unique filename
            base_name = os.path.splitext(os.path.basename(warrior_path))[0]
            output_name = f"characters/{base_name}_warrior.png"

            # Handle duplicates
            counter = 1
            while os.path.exists(output_name):
                output_name = f"characters/{base_name}_warrior_{counter}.png"
                counter += 1

            success = process_image(
                warrior_path,
                output_name,
                (300, 400),
                f"Warrior Character {warrior_count + 1}"
            )
            if success:
                warrior_count += 1
                print(f"✅ Warrior character {warrior_count} added successfully!")
            else:
                print("❌ Failed to add warrior character")
        else:
            print(f"❌ File not found: {warrior_path}")

    # Get princess images (allow multiple)
    print("\n👸 ADDING PRINCESS/LOVER IMAGES:")
    print("Enter paths one by one (press Enter with empty line to finish)")

    princess_count = 0
    while True:
        princess_path = input(f"Princess image {princess_count + 1} (or Enter to finish): ").strip().strip('"')

        if not princess_path:
            break

        if os.path.exists(princess_path):
            # Generate unique filename
            base_name = os.path.splitext(os.path.basename(princess_path))[0]
            output_name = f"lovers/{base_name}_princess.png"

            # Handle duplicates
            counter = 1
            while os.path.exists(output_name):
                output_name = f"lovers/{base_name}_princess_{counter}.png"
                counter += 1

            success = process_image(
                princess_path,
                output_name,
                (200, 300),
                f"Princess {princess_count + 1}"
            )
            if success:
                princess_count += 1
                print(f"✅ Princess {princess_count} added successfully!")
            else:
                print("❌ Failed to add princess")
        else:
            print(f"❌ File not found: {princess_path}")

    print(f"\n🎉 SUMMARY:")
    print(f"✅ Added {warrior_count} warrior/character images")
    print(f"✅ Added {princess_count} princess/lover images")

def add_images_from_folder():
    """Add images from a specific folder"""
    print("\n📁 ADDING IMAGES FROM FOLDER")
    print("=" * 30)
    
    folder_path = input("Enter folder path containing your images: ").strip().strip('"')
    
    if not os.path.exists(folder_path):
        print(f"❌ Folder not found: {folder_path}")
        return
    
    # List all image files
    image_files = []
    for file in os.listdir(folder_path):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_files.append(file)
    
    if not image_files:
        print("❌ No image files found in folder")
        return
    
    print(f"\n📸 Found {len(image_files)} image files:")
    for i, file in enumerate(image_files, 1):
        print(f"  {i}. {file}")
    
    # Select warrior image
    print("\n🏰 Select warrior image:")
    try:
        warrior_choice = int(input("Enter number for warrior image: ")) - 1
        if 0 <= warrior_choice < len(image_files):
            warrior_file = image_files[warrior_choice]
            warrior_path = os.path.join(folder_path, warrior_file)
            
            success = process_image(
                warrior_path, 
                "characters/Magadheera_Warrior.png", 
                (300, 400), 
                "Warrior Character"
            )
            if success:
                print("✅ Warrior character added!")
        else:
            print("❌ Invalid selection")
    except ValueError:
        print("❌ Invalid input")
    
    # Select princess images
    print("\n👸 Select princess images (enter numbers separated by commas):")
    try:
        princess_input = input("Enter numbers for princess images: ").strip()
        if princess_input:
            princess_choices = [int(x.strip()) - 1 for x in princess_input.split(',')]
            
            for i, choice in enumerate(princess_choices, 1):
                if 0 <= choice < len(image_files):
                    princess_file = image_files[choice]
                    princess_path = os.path.join(folder_path, princess_file)
                    
                    success = process_image(
                        princess_path, 
                        f"lovers/Magadheera_Princess_{i}.png", 
                        (200, 300), 
                        f"Princess {i}"
                    )
                    if success:
                        print(f"✅ Princess {i} added!")
                else:
                    print(f"❌ Invalid selection: {choice + 1}")
    except ValueError:
        print("❌ Invalid input format")

def check_final_setup():
    """Check the final image setup"""
    print("\n🔍 CHECKING FINAL SETUP")
    print("=" * 25)
    
    # Check characters
    chars_dir = "characters"
    char_files = [f for f in os.listdir(chars_dir) if f.endswith('.png')] if os.path.exists(chars_dir) else []
    print(f"🏰 Character images: {len(char_files)}")
    for file in char_files:
        print(f"  ✅ {file}")
    
    # Check lovers
    lovers_dir = "lovers"
    lover_files = [f for f in os.listdir(lovers_dir) if f.endswith('.png')] if os.path.exists(lovers_dir) else []
    print(f"👸 Princess/Lover images: {len(lover_files)}")
    for file in lover_files:
        print(f"  ✅ {file}")
    
    if len(char_files) > 0 and len(lover_files) > 0:
        print("\n🎉 SUCCESS! Your custom images are ready!")
        print("🌐 Test the app at: http://localhost:3000")
        return True
    else:
        print("\n⚠️ WARNING: Missing images")
        if len(char_files) == 0:
            print("❌ No warrior/character images found")
        if len(lover_files) == 0:
            print("❌ No princess/lover images found")
        return False

def main():
    print("🏰 MAGADHEERA CUSTOM IMAGE SETUP")
    print("=" * 40)
    
    print("\nThis tool will help you add your custom Magadheera images:")
    print("🏰 Warrior characters (for face replacement)")
    print("👸 Princess/lover characters (floating images)")
    
    print("\nChoose how to add images:")
    print("1. Add images one by one (recommended)")
    print("2. Add images from a folder")
    print("3. Check current setup")
    print("4. Clear all images and start fresh")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == '1':
        clear_existing_images()
        add_images_interactively()
        check_final_setup()
    elif choice == '2':
        clear_existing_images()
        add_images_from_folder()
        check_final_setup()
    elif choice == '3':
        check_final_setup()
    elif choice == '4':
        clear_existing_images()
        print("✅ All images cleared. Run this script again to add new ones.")
    else:
        print("❌ Invalid choice")
        return
    
    print("\n📋 NEXT STEPS:")
    print("1. Make sure backend is running: python app.py")
    print("2. Make sure frontend is running: python -m http.server 3000")
    print("3. Open http://localhost:3000 in your browser")
    print("4. Test the face replacement with your custom images!")

if __name__ == "__main__":
    main()
