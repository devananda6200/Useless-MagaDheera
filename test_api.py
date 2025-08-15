#!/usr/bin/env python3
"""
Test script for the Magadheera Past Life Reveal API
"""

import requests
import cv2
import numpy as np
from PIL import Image, ImageDraw
import io
import os

def create_test_face_image():
    """Create a simple test image with a face-like shape"""
    # Create a 640x480 image
    img = Image.new('RGB', (640, 480), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple face
    # Face outline (circle)
    face_center = (320, 240)
    face_radius = 100
    draw.ellipse([face_center[0] - face_radius, face_center[1] - face_radius,
                  face_center[0] + face_radius, face_center[1] + face_radius], 
                 fill='peachpuff', outline='black', width=2)
    
    # Eyes
    left_eye = (290, 210)
    right_eye = (350, 210)
    eye_radius = 10
    draw.ellipse([left_eye[0] - eye_radius, left_eye[1] - eye_radius,
                  left_eye[0] + eye_radius, left_eye[1] + eye_radius], 
                 fill='black')
    draw.ellipse([right_eye[0] - eye_radius, right_eye[1] - eye_radius,
                  right_eye[0] + eye_radius, right_eye[1] + eye_radius], 
                 fill='black')
    
    # Nose
    draw.ellipse([315, 235, 325, 250], fill='pink')
    
    # Mouth
    draw.arc([300, 260, 340, 280], 0, 180, fill='red', width=3)
    
    return img

def test_api_health():
    """Test the health endpoint"""
    try:
        response = requests.get('http://localhost:8000/health')
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed:")
            print(f"   Status: {data['status']}")
            print(f"   Characters available: {data['characters_available']}")
            print(f"   Lovers available: {data['lovers_available']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_image_processing():
    """Test the image processing endpoint"""
    try:
        # Create test image
        test_img = create_test_face_image()
        
        # Convert to bytes
        img_buffer = io.BytesIO()
        test_img.save(img_buffer, format='JPEG')
        img_buffer.seek(0)
        
        # Send to API
        files = {'file': ('test.jpg', img_buffer, 'image/jpeg')}
        response = requests.post('http://localhost:8000/process-image', files=files)
        
        if response.status_code == 200:
            print("✅ Image processing successful!")
            
            # Save result image
            with open('test_result.jpg', 'wb') as f:
                f.write(response.content)
            print("   Result saved as 'test_result.jpg'")
            return True
        else:
            print(f"❌ Image processing failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('detail', 'Unknown error')}")
            except:
                print(f"   Raw response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Image processing error: {e}")
        return False

def main():
    print("🧪 Testing Magadheera Past Life Reveal API")
    print("=" * 50)
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    health_ok = test_api_health()
    
    if not health_ok:
        print("❌ Cannot proceed with image testing - health check failed")
        return
    
    # Test image processing
    print("\n2. Testing image processing...")
    processing_ok = test_image_processing()
    
    print("\n" + "=" * 50)
    if health_ok and processing_ok:
        print("🎉 All tests passed! The API is working correctly.")
        print("💡 You can now use the frontend at http://localhost:3000")
    else:
        print("⚠️  Some tests failed. Check the backend logs for details.")

if __name__ == "__main__":
    main()
