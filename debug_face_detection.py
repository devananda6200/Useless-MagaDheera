#!/usr/bin/env python3
"""
Debug script to test face detection and image overlay
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw
import os
import math

# Initialize OpenCV face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def debug_face_detection(image_path):
    """Debug face detection on a test image"""
    print(f"🔍 Testing face detection on: {image_path}")
    
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print("❌ Could not load image")
        return None
    
    print(f"📐 Image dimensions: {image.shape}")
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    print(f"👤 Detected {len(faces)} faces")
    
    if len(faces) == 0:
        print("❌ No faces detected!")
        return None
    
    # Get the largest face
    face = max(faces, key=lambda x: x[2] * x[3])
    x, y, w, h = face
    print(f"📍 Face location: x={x}, y={y}, width={w}, height={h}")
    
    # Draw face rectangle for debugging
    debug_image = image.copy()
    cv2.rectangle(debug_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Detect eyes within the face
    face_roi_gray = gray[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(face_roi_gray)
    print(f"👁️ Detected {len(eyes)} eyes")
    
    if len(eyes) >= 2:
        # Sort eyes by x coordinate
        eyes = sorted(eyes, key=lambda e: e[0])
        left_eye_local = eyes[0]
        right_eye_local = eyes[-1]
        
        # Convert to global coordinates
        left_eye = (x + left_eye_local[0] + left_eye_local[2]//2, 
                   y + left_eye_local[1] + left_eye_local[3]//2)
        right_eye = (x + right_eye_local[0] + right_eye_local[2]//2, 
                    y + right_eye_local[1] + right_eye_local[3]//2)
        
        print(f"👁️ Left eye: {left_eye}")
        print(f"👁️ Right eye: {right_eye}")
        
        # Draw eyes
        cv2.circle(debug_image, left_eye, 5, (255, 0, 0), -1)
        cv2.circle(debug_image, right_eye, 5, (255, 0, 0), -1)
    else:
        print("⚠️ Using estimated eye positions")
        left_eye = (x + w//4, y + h//3)
        right_eye = (x + 3*w//4, y + h//3)
        
        # Draw estimated eyes
        cv2.circle(debug_image, left_eye, 5, (0, 0, 255), -1)
        cv2.circle(debug_image, right_eye, 5, (0, 0, 255), -1)
    
    # Save debug image
    debug_path = "debug_face_detection.jpg"
    cv2.imwrite(debug_path, debug_image)
    print(f"💾 Debug image saved as: {debug_path}")
    
    return {
        'face_rect': (x, y, w, h),
        'left_eye': left_eye,
        'right_eye': right_eye,
        'nose_tip': (x + w//2, y + h//2),
        'chin': (x + w//2, y + h - h//8)
    }

def test_character_overlay(base_image_path, character_path, face_landmarks):
    """Test character overlay"""
    print(f"\n🎭 Testing character overlay...")
    print(f"📸 Base image: {base_image_path}")
    print(f"🏰 Character: {character_path}")
    
    if not os.path.exists(character_path):
        print(f"❌ Character image not found: {character_path}")
        return
    
    # Load images
    base_image = cv2.imread(base_image_path)
    character_img = Image.open(character_path).convert("RGBA")
    base_pil = Image.fromarray(cv2.cvtColor(base_image, cv2.COLOR_BGR2RGB))
    
    print(f"🎭 Character image size: {character_img.size}")
    print(f"🎭 Character mode: {character_img.mode}")
    
    # Get face information
    left_eye = face_landmarks['left_eye']
    right_eye = face_landmarks['right_eye']
    face_rect = face_landmarks['face_rect']
    
    # Calculate dimensions
    eye_distance = math.sqrt((right_eye[0] - left_eye[0])**2 + (right_eye[1] - left_eye[1])**2)
    face_width = face_rect[2]
    
    print(f"📏 Eye distance: {eye_distance:.1f}")
    print(f"📏 Face width: {face_width}")
    
    # Calculate rotation angle
    angle = math.atan2(right_eye[1] - left_eye[1], right_eye[0] - left_eye[0])
    angle_degrees = math.degrees(angle)
    print(f"🔄 Rotation angle: {angle_degrees:.1f} degrees")
    
    # Scale character image
    scale_factor = face_width / character_img.width * 1.2
    new_width = int(character_img.width * scale_factor)
    new_height = int(character_img.height * scale_factor)
    
    print(f"📐 Scale factor: {scale_factor:.2f}")
    print(f"📐 New character size: {new_width}x{new_height}")
    
    # Resize and rotate
    character_resized = character_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    character_rotated = character_resized.rotate(-angle_degrees, expand=True)
    
    # Calculate position
    face_center_x = (left_eye[0] + right_eye[0]) // 2
    face_center_y = (left_eye[1] + right_eye[1]) // 2 - int(eye_distance * 0.1)
    
    paste_x = face_center_x - character_rotated.width // 2
    paste_y = face_center_y - character_rotated.height // 2
    
    print(f"📍 Paste position: ({paste_x}, {paste_y})")
    
    # Create result
    result = base_pil.copy()
    
    # Paste character with transparency
    if character_rotated.mode == 'RGBA':
        result.paste(character_rotated, (paste_x, paste_y), character_rotated)
        print("✅ Applied character with transparency")
    else:
        result.paste(character_rotated, (paste_x, paste_y))
        print("⚠️ Applied character without transparency")
    
    # Save result
    result_path = "debug_character_overlay.jpg"
    result_cv = cv2.cvtColor(np.array(result), cv2.COLOR_RGB2BGR)
    cv2.imwrite(result_path, result_cv)
    print(f"💾 Result saved as: {result_path}")

def main():
    print("🧪 Magadheera Face Detection Debug Tool")
    print("=" * 50)
    
    # Test with a sample image (you can change this path)
    test_image_path = input("Enter path to test image (or press Enter for webcam capture): ").strip()
    
    if not test_image_path:
        print("📷 Capturing from webcam...")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Could not open webcam")
            return
        
        print("📸 Press SPACE to capture, ESC to exit")
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            cv2.imshow('Webcam - Press SPACE to capture', frame)
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord(' '):  # Space to capture
                test_image_path = "webcam_capture.jpg"
                cv2.imwrite(test_image_path, frame)
                print(f"📸 Captured image saved as: {test_image_path}")
                break
            elif key == 27:  # ESC to exit
                cap.release()
                cv2.destroyAllWindows()
                return
        
        cap.release()
        cv2.destroyAllWindows()
    
    if not os.path.exists(test_image_path):
        print(f"❌ Image not found: {test_image_path}")
        return
    
    # Test face detection
    face_landmarks = debug_face_detection(test_image_path)
    
    if face_landmarks is None:
        print("❌ Cannot proceed without face detection")
        return
    
    # Test character overlay
    character_files = [f for f in os.listdir("characters") if f.lower().endswith('.png')]
    if character_files:
        character_path = os.path.join("characters", character_files[0])
        test_character_overlay(test_image_path, character_path, face_landmarks)
    else:
        print("❌ No character images found in characters/ folder")
    
    print("\n🎉 Debug complete! Check the generated debug images.")

if __name__ == "__main__":
    main()
