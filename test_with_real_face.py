#!/usr/bin/env python3
"""
Test face detection with webcam or better test images
"""

import cv2
import numpy as np
import requests
import os

def capture_from_webcam():
    """Capture a real photo from webcam for testing"""
    print("📷 Opening webcam for face detection test...")
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Could not open webcam")
        return None
    
    print("📸 Position your face in the camera and press SPACE to capture")
    print("Press ESC to cancel")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to read from webcam")
            break
        
        # Show preview
        cv2.imshow('Webcam Test - Press SPACE to capture, ESC to cancel', frame)
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' '):  # Space to capture
            test_image_path = "webcam_test_capture.jpg"
            cv2.imwrite(test_image_path, frame)
            print(f"📸 Captured test image: {test_image_path}")
            cap.release()
            cv2.destroyAllWindows()
            return test_image_path
        elif key == 27:  # ESC to cancel
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return None

def test_face_detection_on_image(image_path):
    """Test face detection on a specific image"""
    print(f"🔍 Testing face detection on: {image_path}")
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return False
    
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print("❌ Could not load image")
        return False
    
    print(f"📐 Image size: {image.shape}")
    
    # Test face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Try multiple detection parameters
    detection_params = [
        {'scaleFactor': 1.05, 'minNeighbors': 3, 'minSize': (30, 30)},
        {'scaleFactor': 1.03, 'minNeighbors': 2, 'minSize': (20, 20)},
        {'scaleFactor': 1.1, 'minNeighbors': 5, 'minSize': (50, 50)},
        {'scaleFactor': 1.2, 'minNeighbors': 3, 'minSize': (40, 40)},
    ]
    
    for i, params in enumerate(detection_params):
        faces = face_cascade.detectMultiScale(gray, **params)
        print(f"🔍 Attempt {i+1}: Detected {len(faces)} faces with params {params}")
        
        if len(faces) > 0:
            # Draw rectangles around faces
            result_image = image.copy()
            for (x, y, w, h) in faces:
                cv2.rectangle(result_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(result_image, f'Face {len(faces)}', (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Save result
            result_path = f"face_detection_result_{i+1}.jpg"
            cv2.imwrite(result_path, result_image)
            print(f"✅ Face detection successful! Result saved: {result_path}")
            return True
    
    print("❌ No faces detected with any parameters")
    return False

def test_api_with_image(image_path):
    """Test the API with a real image"""
    print(f"🌐 Testing API with image: {image_path}")
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return False
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
            response = requests.post('http://localhost:8000/process-image', files=files, timeout=30)
        
        if response.status_code == 200:
            result_path = "api_test_result.jpg"
            with open(result_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ API test successful! Result saved: {result_path}")
            return True
        else:
            print(f"❌ API test failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"  Error: {error_data.get('detail', 'Unknown error')}")
            except:
                print(f"  Raw response: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ API test error: {e}")
        return False

def main():
    print("🧪 REAL FACE DETECTION TEST")
    print("=" * 40)
    
    print("\nChoose test method:")
    print("1. Capture from webcam")
    print("2. Use existing image file")
    print("3. Skip to API test with fallback")
    
    choice = input("Enter choice (1-3): ").strip()
    
    test_image_path = None
    
    if choice == '1':
        test_image_path = capture_from_webcam()
    elif choice == '2':
        test_image_path = input("Enter path to image file: ").strip()
    elif choice == '3':
        print("Skipping to API test...")
    else:
        print("Invalid choice")
        return
    
    if test_image_path:
        print(f"\n🔍 Testing face detection...")
        face_detected = test_face_detection_on_image(test_image_path)
        
        print(f"\n🌐 Testing API...")
        api_success = test_api_with_image(test_image_path)
        
        if face_detected and api_success:
            print("\n🎉 ALL TESTS PASSED!")
            print("✅ Face detection working")
            print("✅ API processing working")
            print("🌐 Your app should work at: http://localhost:3000")
        elif api_success:
            print("\n⚠️ PARTIAL SUCCESS!")
            print("⚠️ Face detection might be weak, but API fallback is working")
            print("🌐 Your app should still work at: http://localhost:3000")
        else:
            print("\n❌ TESTS FAILED!")
            print("❌ Check backend logs for errors")
    else:
        print("No test image available")
    
    print("\n📋 Next steps:")
    print("1. If tests passed: Open http://localhost:3000")
    print("2. If tests failed: Check backend is running with 'python app.py'")
    print("3. Try with different lighting or face angles")

if __name__ == "__main__":
    main()
