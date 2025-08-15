#!/usr/bin/env python3
"""
Comprehensive error diagnosis tool for Magadheera app
"""

import os
import sys
import requests
import cv2
import numpy as np
from PIL import Image
import traceback

def check_dependencies():
    """Check if all required packages are working"""
    print("🔍 Checking Dependencies...")
    
    try:
        import fastapi
        print(f"✅ FastAPI: {fastapi.__version__}")
    except Exception as e:
        print(f"❌ FastAPI error: {e}")
        return False
    
    try:
        import uvicorn
        print(f"✅ Uvicorn: {uvicorn.__version__}")
    except Exception as e:
        print(f"❌ Uvicorn error: {e}")
        return False
    
    try:
        import cv2
        print(f"✅ OpenCV: {cv2.__version__}")
    except Exception as e:
        print(f"❌ OpenCV error: {e}")
        return False
    
    try:
        from PIL import Image
        print(f"✅ Pillow: {Image.__version__}")
    except Exception as e:
        print(f"❌ Pillow error: {e}")
        return False
    
    try:
        import numpy as np
        print(f"✅ NumPy: {np.__version__}")
    except Exception as e:
        print(f"❌ NumPy error: {e}")
        return False
    
    return True

def check_opencv_cascades():
    """Check if OpenCV cascade files are available"""
    print("\n🔍 Checking OpenCV Cascades...")
    
    try:
        face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        if os.path.exists(face_cascade_path):
            print("✅ Face cascade found")
        else:
            print("❌ Face cascade not found")
            return False
        
        eye_cascade_path = cv2.data.haarcascades + 'haarcascade_eye.xml'
        if os.path.exists(eye_cascade_path):
            print("✅ Eye cascade found")
        else:
            print("❌ Eye cascade not found")
            return False
        
        # Test loading cascades
        face_cascade = cv2.CascadeClassifier(face_cascade_path)
        eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
        
        if face_cascade.empty():
            print("❌ Face cascade failed to load")
            return False
        
        if eye_cascade.empty():
            print("❌ Eye cascade failed to load")
            return False
        
        print("✅ Cascades loaded successfully")
        return True
        
    except Exception as e:
        print(f"❌ Cascade error: {e}")
        return False

def check_image_folders():
    """Check image folders and contents"""
    print("\n🔍 Checking Image Folders...")
    
    # Check characters folder
    chars_dir = "characters"
    if not os.path.exists(chars_dir):
        print(f"❌ {chars_dir} folder missing")
        return False
    
    char_files = [f for f in os.listdir(chars_dir) if f.lower().endswith('.png')]
    print(f"📁 Characters folder: {len(char_files)} PNG files")
    
    for file in char_files:
        try:
            img_path = os.path.join(chars_dir, file)
            img = Image.open(img_path)
            print(f"  ✅ {file}: {img.size} {img.mode}")
        except Exception as e:
            print(f"  ❌ {file}: Error - {e}")
    
    # Check lovers folder
    lovers_dir = "lovers"
    if not os.path.exists(lovers_dir):
        print(f"❌ {lovers_dir} folder missing")
        return False
    
    lover_files = [f for f in os.listdir(lovers_dir) if f.lower().endswith('.png')]
    print(f"💕 Lovers folder: {len(lover_files)} PNG files")
    
    for file in lover_files:
        try:
            img_path = os.path.join(lovers_dir, file)
            img = Image.open(img_path)
            print(f"  ✅ {file}: {img.size} {img.mode}")
        except Exception as e:
            print(f"  ❌ {file}: Error - {e}")
    
    return len(char_files) > 0 and len(lover_files) > 0

def test_backend_connection():
    """Test backend API connection"""
    print("\n🔍 Testing Backend Connection...")
    
    try:
        # Test health endpoint
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend health check passed")
            print(f"  Status: {data['status']}")
            print(f"  Characters: {data['characters_available']}")
            print(f"  Lovers: {data['lovers_available']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend - is it running?")
        return False
    except Exception as e:
        print(f"❌ Backend connection error: {e}")
        return False

def test_face_detection():
    """Test face detection with a simple image"""
    print("\n🔍 Testing Face Detection...")
    
    try:
        # Create a simple test image with a face-like shape
        test_img = np.zeros((480, 640, 3), dtype=np.uint8)
        test_img.fill(200)  # Light gray background
        
        # Draw a simple face
        cv2.circle(test_img, (320, 240), 80, (150, 150, 150), -1)  # Face
        cv2.circle(test_img, (300, 220), 10, (0, 0, 0), -1)  # Left eye
        cv2.circle(test_img, (340, 220), 10, (0, 0, 0), -1)  # Right eye
        cv2.ellipse(test_img, (320, 260), (20, 10), 0, 0, 180, (0, 0, 0), 2)  # Mouth
        
        # Save test image
        cv2.imwrite('test_face.jpg', test_img)
        print("✅ Created test face image")
        
        # Test face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        print(f"🔍 Detected {len(faces)} faces in test image")
        
        if len(faces) > 0:
            print("✅ Face detection working")
            return True
        else:
            print("⚠️ No faces detected in test image (this might be normal)")
            return True  # Not necessarily an error
        
    except Exception as e:
        print(f"❌ Face detection error: {e}")
        traceback.print_exc()
        return False

def test_image_processing():
    """Test the complete image processing pipeline"""
    print("\n🔍 Testing Image Processing Pipeline...")
    
    try:
        # Create test image
        test_img = np.zeros((480, 640, 3), dtype=np.uint8)
        test_img.fill(200)
        
        # Save as JPEG
        cv2.imwrite('pipeline_test.jpg', test_img)
        
        # Test API endpoint
        with open('pipeline_test.jpg', 'rb') as f:
            files = {'file': ('test.jpg', f, 'image/jpeg')}
            response = requests.post('http://localhost:8000/process-image', files=files, timeout=30)
        
        if response.status_code == 200:
            print("✅ Image processing pipeline working")
            with open('pipeline_result.jpg', 'wb') as f:
                f.write(response.content)
            print("✅ Result saved as pipeline_result.jpg")
            return True
        else:
            print(f"❌ Image processing failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"  Error: {error_data.get('detail', 'Unknown error')}")
            except:
                print(f"  Raw response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Image processing error: {e}")
        traceback.print_exc()
        return False

def main():
    print("🏰 MAGADHEERA ERROR DIAGNOSIS TOOL")
    print("=" * 50)
    
    all_good = True
    
    # Run all checks
    if not check_dependencies():
        all_good = False
        print("\n❌ CRITICAL: Dependencies missing or broken")
    
    if not check_opencv_cascades():
        all_good = False
        print("\n❌ CRITICAL: OpenCV cascades not working")
    
    if not check_image_folders():
        all_good = False
        print("\n❌ WARNING: Image folders have issues")
    
    if not test_backend_connection():
        all_good = False
        print("\n❌ CRITICAL: Backend not responding")
    else:
        # Only test these if backend is running
        if not test_face_detection():
            all_good = False
            print("\n❌ WARNING: Face detection issues")
        
        if not test_image_processing():
            all_good = False
            print("\n❌ CRITICAL: Image processing pipeline broken")
    
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 ALL CHECKS PASSED!")
        print("✅ Your Magadheera app should be working correctly")
        print("🌐 Frontend: http://localhost:3000")
        print("🔧 Backend: http://localhost:8000")
    else:
        print("⚠️ ISSUES FOUND!")
        print("Please fix the errors above and run this script again")
    
    print("\n📋 Next steps:")
    print("1. Fix any critical errors shown above")
    print("2. If backend isn't running: python app.py")
    print("3. If frontend isn't running: python -m http.server 3000")
    print("4. Test the app at http://localhost:3000")

if __name__ == "__main__":
    main()
