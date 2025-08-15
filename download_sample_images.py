#!/usr/bin/env python3
"""
Script to help prepare sample images for Magadheera app
Since I can't directly download the images you showed, this script will help you prepare them.
"""

import os
from PIL import Image, ImageDraw
import requests

def create_image_templates():
    """Create templates showing what kind of images we need"""
    
    print("🎭 Creating image templates...")
    
    # Create character template
    char_img = Image.new('RGBA', (300, 400), (0, 0, 0, 0))
    draw = ImageDraw.Draw(char_img)
    
    # Draw template for character face
    draw.rectangle([50, 50, 250, 350], outline='red', width=3)
    draw.text((60, 60), "CHARACTER FACE", fill='red')
    draw.text((60, 80), "300x400 pixels", fill='red')
    draw.text((60, 100), "PNG with transparency", fill='red')
    draw.text((60, 120), "Face should be centered", fill='red')
    draw.text((60, 140), "Clear facial features", fill='red')
    
    # Draw face outline
    draw.ellipse([100, 150, 200, 280], outline='blue', width=2)
    draw.text((110, 290), "Face area", fill='blue')
    
    char_img.save('character_template.png')
    print("📄 Created character_template.png")
    
    # Create lover template
    lover_img = Image.new('RGBA', (200, 300), (0, 0, 0, 0))
    draw = ImageDraw.Draw(lover_img)
    
    draw.rectangle([20, 20, 180, 280], outline='purple', width=3)
    draw.text((30, 30), "LOVER FACE", fill='purple')
    draw.text((30, 50), "200x300 pixels", fill='purple')
    draw.text((30, 70), "PNG format", fill='purple')
    draw.text((30, 90), "Smaller size", fill='purple')
    
    # Draw face outline
    draw.ellipse([60, 120, 140, 220], outline='pink', width=2)
    draw.text((70, 230), "Face area", fill='pink')
    
    lover_img.save('lover_template.png')
    print("📄 Created lover_template.png")

def prepare_instructions():
    """Create instructions for preparing the images"""
    
    instructions = """
# 🎭 How to Prepare Your Magadheera Images

## Images You Showed Me:
1. **Princess in traditional costume** - Perfect for lovers/ folder
2. **Modern actress** - Good for lovers/ folder  
3. **Warrior with armor** - Perfect for characters/ folder

## Steps to Prepare:

### For Character Images (Warriors):
1. **Save the warrior image** as PNG format
2. **Resize to 300x400 pixels** (or similar ratio)
3. **Remove background** (make transparent) if possible
4. **Name it:** `Warrior_Magadheera.png`
5. **Place in:** `backend/characters/` folder

### For Lover Images (Princesses):
1. **Save the princess images** as PNG format
2. **Resize to 200x300 pixels** (or similar ratio)
3. **Remove background** if possible
4. **Name them:** `Princess_1.png`, `Princess_2.png`
5. **Place in:** `backend/lovers/` folder

## Tools to Help:

### Online Background Removers:
- remove.bg
- photopea.com (free Photoshop alternative)
- canva.com

### Steps in Photopea (Free):
1. Open photopea.com
2. Upload your image
3. Use "Magic Wand" or "Background Eraser"
4. Delete background
5. Export as PNG

### Quick Method:
Even without removing backgrounds, the images will work!
Just resize them and save as PNG.

## File Structure Needed:
```
backend/
├── characters/
│   ├── Warrior_Magadheera.png
│   ├── Warrior_2.png (if you have more)
│   └── ...
└── lovers/
    ├── Princess_1.png
    ├── Princess_2.png
    └── ...
```

## Testing:
After adding images, run:
```bash
python debug_face_detection.py
```

This will test face detection and overlay with your new images!
"""
    
    with open('IMAGE_PREPARATION_GUIDE.md', 'w') as f:
        f.write(instructions)
    
    print("📖 Created IMAGE_PREPARATION_GUIDE.md")

def main():
    print("🏰 Magadheera Image Preparation Helper")
    print("=" * 50)
    
    create_image_templates()
    prepare_instructions()
    
    print("\n✅ Templates and instructions created!")
    print("\n📋 Next steps:")
    print("1. Save your images from the chat")
    print("2. Follow the guide in IMAGE_PREPARATION_GUIDE.md")
    print("3. Replace images in characters/ and lovers/ folders")
    print("4. Run: python debug_face_detection.py")
    print("\n🎯 The warrior image will replace faces")
    print("🎯 The princess images will appear as past lovers")

if __name__ == "__main__":
    main()
