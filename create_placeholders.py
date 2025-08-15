from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image(width, height, color, text, filename):
    """Create a placeholder image with text"""
    # Create image with transparent background
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a colored circle/oval for face
    margin = 20
    draw.ellipse([margin, margin, width-margin, height-margin], fill=color)
    
    # Add text
    try:
        # Try to use a default font
        font = ImageFont.load_default()
    except:
        font = None
    
    # Calculate text position
    if font:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    else:
        text_width = len(text) * 6
        text_height = 11
    
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    
    draw.text((text_x, text_y), text, fill='white', font=font)
    
    # Save image
    img.save(filename, 'PNG')
    print(f"Created {filename}")

def main():
    # Create characters directory if it doesn't exist
    os.makedirs('characters', exist_ok=True)
    os.makedirs('lovers', exist_ok=True)
    
    # Create character placeholder images
    characters = [
        ('Warrior1', (139, 69, 19)),    # Brown
        ('Warrior2', (160, 82, 45)),    # Saddle brown
        ('Warrior3', (101, 67, 33)),    # Dark brown
        ('Prince', (205, 133, 63)),     # Peru
        ('Hero', (210, 180, 140)),      # Tan
    ]
    
    for name, color in characters:
        create_placeholder_image(200, 250, color, name, f'characters/{name}.png')
    
    # Create lover placeholder images
    lovers = [
        ('Princess1', (255, 182, 193)),  # Light pink
        ('Princess2', (255, 160, 122)),  # Light salmon
        ('Lover1', (255, 218, 185)),     # Peach puff
        ('Lover2', (255, 228, 196)),     # Bisque
        ('Beauty', (255, 240, 245)),     # Lavender blush
    ]
    
    for name, color in lovers:
        create_placeholder_image(150, 180, color, name, f'lovers/{name}.png')
    
    print("All placeholder images created successfully!")

if __name__ == "__main__":
    main()
