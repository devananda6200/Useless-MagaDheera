from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import cv2
import numpy as np
from PIL import Image, ImageDraw
import random
import os
import io
import base64
from typing import Optional
import math

app = FastAPI(
    title="Magadheera Past Life Reveal API",
    description="Transform faces into epic Magadheera warriors",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Add error handling middleware
@app.middleware("http")
async def error_handling_middleware(request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        print(f"Unhandled error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": "Internal server error", "detail": str(e)}

# Initialize OpenCV face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def get_random_character():
    """Get a random character image from the characters folder"""
    characters_dir = "characters"
    if not os.path.exists(characters_dir):
        return None
    
    character_files = [f for f in os.listdir(characters_dir) if f.lower().endswith('.png')]
    if not character_files:
        return None
    
    random_character = random.choice(character_files)
    return os.path.join(characters_dir, random_character)

def get_random_lover():
    """Get a random lover image from the lovers folder"""
    lovers_dir = "lovers"
    if not os.path.exists(lovers_dir):
        return None
    
    lover_files = [f for f in os.listdir(lovers_dir) if f.lower().endswith('.png')]
    if not lover_files:
        return None
    
    random_lover = random.choice(lover_files)
    return os.path.join(lovers_dir, random_lover)

def calculate_angle(point1, point2):
    """Calculate angle between two points"""
    return math.atan2(point2[1] - point1[1], point2[0] - point1[0])

def get_face_landmarks(image):
    """Extract face landmarks using OpenCV"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces with more sensitive parameters
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.05,      # More sensitive scaling
        minNeighbors=3,        # Fewer neighbors required
        minSize=(30, 30),      # Smaller minimum face size
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # If no faces found, try with even more sensitive parameters
    if len(faces) == 0:
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.03,
            minNeighbors=2,
            minSize=(20, 20),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

    if len(faces) == 0:
        return None

    # Get the largest face
    face = max(faces, key=lambda x: x[2] * x[3])
    x, y, w, h = face

    # Extract face region for eye detection
    face_roi_gray = gray[y:y+h, x:x+w]
    face_roi_color = image[y:y+h, x:x+w]

    # Detect eyes within the face with multiple attempts
    eyes = eye_cascade.detectMultiScale(
        face_roi_gray,
        scaleFactor=1.05,
        minNeighbors=3,
        minSize=(10, 10)
    )

    # If no eyes found, try more sensitive detection
    if len(eyes) == 0:
        eyes = eye_cascade.detectMultiScale(
            face_roi_gray,
            scaleFactor=1.03,
            minNeighbors=2,
            minSize=(5, 5)
        )

    if len(eyes) < 2:
        # If we can't detect both eyes, estimate positions based on face proportions
        left_eye = (x + int(w * 0.3), y + int(h * 0.35))
        right_eye = (x + int(w * 0.7), y + int(h * 0.35))
    else:
        # Sort eyes by x coordinate (left to right)
        eyes = sorted(eyes, key=lambda e: e[0])
        left_eye_local = eyes[0]
        right_eye_local = eyes[-1]

        # Convert to global coordinates and get center points
        left_eye = (x + left_eye_local[0] + left_eye_local[2]//2,
                   y + left_eye_local[1] + left_eye_local[3]//2)
        right_eye = (x + right_eye_local[0] + right_eye_local[2]//2,
                    y + right_eye_local[1] + right_eye_local[3]//2)

    # Create simplified landmark structure
    face_landmarks = {
        'face_rect': (x, y, w, h),
        'left_eye': left_eye,
        'right_eye': right_eye,
        'nose_tip': (x + w//2, y + h//2),
        'chin': (x + w//2, y + h - h//8)
    }

    return face_landmarks

def align_and_overlay_face(base_image, character_path, face_landmarks):
    """Align and overlay character face on detected face"""
    if not os.path.exists(character_path):
        return base_image

    # Load character image with transparency
    character_img = Image.open(character_path).convert("RGBA")
    base_pil = Image.fromarray(cv2.cvtColor(base_image, cv2.COLOR_BGR2RGB))

    # Get face information from landmarks
    left_eye = face_landmarks['left_eye']
    right_eye = face_landmarks['right_eye']
    nose_tip = face_landmarks['nose_tip']
    chin = face_landmarks['chin']
    face_rect = face_landmarks['face_rect']

    # Calculate face dimensions and angle
    eye_distance = math.sqrt((right_eye[0] - left_eye[0])**2 + (right_eye[1] - left_eye[1])**2)
    face_width = face_rect[2]
    face_height = face_rect[3]

    # Calculate rotation angle
    angle = calculate_angle(left_eye, right_eye)
    angle_degrees = math.degrees(angle)

    # Improved scaling logic for better face replacement
    # Scale based on face height for better proportions
    scale_factor = max(face_width / character_img.width, face_height / character_img.height) * 1.3
    new_width = int(character_img.width * scale_factor)
    new_height = int(character_img.height * scale_factor)

    # Ensure minimum size for visibility
    min_size = 150
    if new_width < min_size:
        scale_factor = min_size / character_img.width
        new_width = min_size
        new_height = int(character_img.height * scale_factor)

    # Resize character image with high quality
    character_resized = character_img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Rotate character image to match face angle
    character_rotated = character_resized.rotate(-angle_degrees, expand=True)

    # Improved positioning - center on the entire face area
    face_center_x = face_rect[0] + face_rect[2] // 2
    face_center_y = face_rect[1] + face_rect[3] // 2

    # Adjust position slightly upward for better alignment
    paste_x = face_center_x - character_rotated.width // 2
    paste_y = face_center_y - character_rotated.height // 2 - int(face_height * 0.1)

    # Ensure paste position is within image bounds
    paste_x = max(0, min(paste_x, base_pil.width - character_rotated.width))
    paste_y = max(0, min(paste_y, base_pil.height - character_rotated.height))

    # Create a copy of base image for compositing
    result = base_pil.copy()

    # Apply character face with improved blending
    if character_rotated.mode == 'RGBA':
        # Create a mask for better blending
        mask = character_rotated.split()[-1]  # Alpha channel
        result.paste(character_rotated, (paste_x, paste_y), mask)
    else:
        # Convert to RGBA and create a simple mask
        character_rgba = character_rotated.convert('RGBA')
        result.paste(character_rgba, (paste_x, paste_y))

    return cv2.cvtColor(np.array(result), cv2.COLOR_RGB2BGR)

def add_lover_image(image, lover_path):
    """Add lover image as a floating element"""
    if not os.path.exists(lover_path):
        return image

    lover_img = Image.open(lover_path).convert("RGBA")
    base_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Improved scaling for lover image
    # Scale based on image size for better proportions
    base_width, base_height = base_pil.size
    lover_scale = min(base_width / lover_img.width * 0.25, base_height / lover_img.height * 0.35)

    lover_width = int(lover_img.width * lover_scale)
    lover_height = int(lover_img.height * lover_scale)

    # Ensure minimum and maximum sizes
    min_size, max_size = 100, 300
    if lover_width < min_size:
        scale_factor = min_size / lover_width
        lover_width = min_size
        lover_height = int(lover_height * scale_factor)
    elif lover_width > max_size:
        scale_factor = max_size / lover_width
        lover_width = max_size
        lover_height = int(lover_height * scale_factor)

    lover_resized = lover_img.resize((lover_width, lover_height), Image.Resampling.LANCZOS)

    # Better positioning - top right with elegant placement
    margin_x = 30
    margin_y = 30
    paste_x = base_pil.width - lover_width - margin_x
    paste_y = margin_y

    # Ensure position is within bounds
    paste_x = max(0, min(paste_x, base_pil.width - lover_width))
    paste_y = max(0, min(paste_y, base_pil.height - lover_height))

    # Apply lover image with transparency
    if lover_resized.mode == 'RGBA':
        mask = lover_resized.split()[-1]  # Alpha channel
        base_pil.paste(lover_resized, (paste_x, paste_y), mask)
    else:
        lover_rgba = lover_resized.convert('RGBA')
        base_pil.paste(lover_rgba, (paste_x, paste_y))

    return cv2.cvtColor(np.array(base_pil), cv2.COLOR_RGB2BGR)

@app.post("/process-image")
async def process_image(file: UploadFile = File(...)):
    """Process uploaded image and return Magadheera transformation"""
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")

        # Check file size (max 10MB)
        contents = await file.read()
        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large (max 10MB)")

        if len(contents) == 0:
            raise HTTPException(status_code=400, detail="Empty file")

        # Decode image
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image format. Please use JPG, PNG, or other common formats.")

        # Check image dimensions
        h, w = image.shape[:2]
        if w < 50 or h < 50:
            raise HTTPException(status_code=400, detail="Image too small (minimum 50x50 pixels)")

        if w > 4000 or h > 4000:
            raise HTTPException(status_code=400, detail="Image too large (maximum 4000x4000 pixels)")

        print(f"Processing image: {w}x{h} pixels")

        # Detect face landmarks
        face_landmarks = get_face_landmarks(image)
        using_fallback = False

        if face_landmarks is None:
            # Fallback: create estimated face landmarks based on image center
            center_x, center_y = w // 2, h // 2
            face_size = min(w, h) // 4

            face_landmarks = {
                'face_rect': (center_x - face_size, center_y - face_size, face_size * 2, face_size * 2),
                'left_eye': (center_x - face_size//2, center_y - face_size//3),
                'right_eye': (center_x + face_size//2, center_y - face_size//3),
                'nose_tip': (center_x, center_y),
                'chin': (center_x, center_y + face_size//2)
            }
            using_fallback = True
            print("Using fallback face landmarks (no face detected)")
        else:
            print("Face detected successfully")

        # Get random character and lover
        character_path = get_random_character()
        lover_path = get_random_lover()

        if character_path is None:
            raise HTTPException(status_code=500, detail="No character images available. Please add character images to the backend.")

        print(f"Using character: {character_path}")
        if lover_path:
            print(f"Using lover: {lover_path}")

        # Apply character face overlay
        result_image = align_and_overlay_face(image, character_path, face_landmarks)

        # Add lover image if available
        if lover_path:
            result_image = add_lover_image(result_image, lover_path)

        # Convert result to bytes with high quality
        encode_params = [
            cv2.IMWRITE_JPEG_QUALITY, 95,
            cv2.IMWRITE_JPEG_OPTIMIZE, 1
        ]
        success, buffer = cv2.imencode('.jpg', result_image, encode_params)

        if not success:
            raise HTTPException(status_code=500, detail="Failed to encode result image")

        print(f"Processing complete. Result size: {len(buffer)} bytes")

        return StreamingResponse(
            io.BytesIO(buffer.tobytes()),
            media_type="image/jpeg",
            headers={
                "Content-Disposition": "inline; filename=magadheera_result.jpg",
                "X-Face-Detection": "fallback" if using_fallback else "detected"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Magadheera Past Life Reveal API is running!"}

@app.get("/health")
async def health_check():
    characters_count = len([f for f in os.listdir("characters") if f.lower().endswith('.png')]) if os.path.exists("characters") else 0
    lovers_count = len([f for f in os.listdir("lovers") if f.lower().endswith('.png')]) if os.path.exists("lovers") else 0
    
    return {
        "status": "healthy",
        "characters_available": characters_count,
        "lovers_available": lovers_count
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
