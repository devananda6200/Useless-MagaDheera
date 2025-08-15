#!/usr/bin/env python3
"""
Smart Image Converter for Magadheera
Automatically processes and optimizes images for face replacement
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

class SmartImageConverter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏰 Magadheera Smart Image Converter")
        self.root.geometry("900x700")
        
        # Initialize face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main title
        title_label = tk.Label(self.root, text="🏰 Smart Image Converter", 
                              font=("Arial", 18, "bold"), fg="#8B4513")
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(self.root, text="Convert your images to perfect Magadheera characters", 
                                 font=("Arial", 12), fg="#666")
        subtitle_label.pack(pady=5)
        
        # Create main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left panel - Controls
        left_panel = tk.Frame(main_frame, width=300)
        left_panel.pack(side="left", fill="y", padx=(0, 20))
        left_panel.pack_propagate(False)
        
        # Right panel - Preview
        right_panel = tk.Frame(main_frame, bg="#f0f0f0")
        right_panel.pack(side="right", fill="both", expand=True)
        
        self.setup_controls(left_panel)
        self.setup_preview(right_panel)
        
    def setup_controls(self, parent):
        """Setup control panel"""
        # Image type selection
        type_frame = tk.LabelFrame(parent, text="Image Type", font=("Arial", 12, "bold"))
        type_frame.pack(fill="x", pady=10)
        
        self.image_type = tk.StringVar(value="character")
        tk.Radiobutton(type_frame, text="🏰 Warrior/Character (Face Replacement)", 
                      variable=self.image_type, value="character").pack(anchor="w", padx=10, pady=5)
        tk.Radiobutton(type_frame, text="👸 Princess/Lover (Floating Image)", 
                      variable=self.image_type, value="lover").pack(anchor="w", padx=10, pady=5)
        
        # File selection
        file_frame = tk.LabelFrame(parent, text="Select Images", font=("Arial", 12, "bold"))
        file_frame.pack(fill="x", pady=10)
        
        tk.Button(file_frame, text="📁 Select Images", command=self.select_images,
                 bg="#4CAF50", fg="white", font=("Arial", 11, "bold")).pack(pady=10)
        
        self.file_list = tk.Listbox(file_frame, height=6)
        self.file_list.pack(fill="x", padx=10, pady=5)
        
        # Processing options
        options_frame = tk.LabelFrame(parent, text="Processing Options", font=("Arial", 12, "bold"))
        options_frame.pack(fill="x", pady=10)
        
        self.auto_crop_face = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="🎯 Auto-crop to face (for characters)", 
                      variable=self.auto_crop_face).pack(anchor="w", padx=10, pady=2)
        
        self.enhance_quality = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="✨ Enhance image quality", 
                      variable=self.enhance_quality).pack(anchor="w", padx=10, pady=2)
        
        self.remove_background = tk.BooleanVar(value=False)
        tk.Checkbutton(options_frame, text="🎭 Try to remove background", 
                      variable=self.remove_background).pack(anchor="w", padx=10, pady=2)
        
        self.resize_optimal = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="📐 Resize to optimal dimensions", 
                      variable=self.resize_optimal).pack(anchor="w", padx=10, pady=2)
        
        # Process button
        tk.Button(parent, text="🚀 Process Images", command=self.process_images,
                 bg="#2196F3", fg="white", font=("Arial", 14, "bold")).pack(pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(parent, mode='determinate')
        self.progress.pack(fill="x", pady=10)
        
        # Status
        self.status_var = tk.StringVar(value="Ready to process images")
        status_label = tk.Label(parent, textvariable=self.status_var, 
                               font=("Arial", 10), fg="#666")
        status_label.pack(pady=5)
        
    def setup_preview(self, parent):
        """Setup preview panel"""
        preview_label = tk.Label(parent, text="Preview", font=("Arial", 14, "bold"))
        preview_label.pack(pady=10)
        
        # Canvas for image preview
        self.canvas = tk.Canvas(parent, bg="white", width=400, height=400)
        self.canvas.pack(pady=10)
        
        # Results text
        self.results_text = tk.Text(parent, height=10, width=50)
        self.results_text.pack(fill="both", expand=True, padx=10, pady=10)
        
    def select_images(self):
        """Select images to process"""
        files = filedialog.askopenfilenames(
            title="Select Images to Convert",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
        )
        
        self.file_list.delete(0, tk.END)
        for file in files:
            self.file_list.insert(tk.END, os.path.basename(file))
        
        self.selected_files = files
        self.status_var.set(f"Selected {len(files)} images")
        
    def process_images(self):
        """Process selected images"""
        if not hasattr(self, 'selected_files') or not self.selected_files:
            messagebox.showwarning("No Images", "Please select images first!")
            return
        
        # Run processing in separate thread
        threading.Thread(target=self._process_images_thread, daemon=True).start()
        
    def _process_images_thread(self):
        """Process images in background thread"""
        try:
            total_files = len(self.selected_files)
            self.progress['maximum'] = total_files
            
            results = []
            
            for i, file_path in enumerate(self.selected_files):
                self.status_var.set(f"Processing {os.path.basename(file_path)}...")
                self.progress['value'] = i
                self.root.update()
                
                try:
                    result = self.process_single_image(file_path)
                    results.append(result)
                except Exception as e:
                    results.append(f"❌ {os.path.basename(file_path)}: {str(e)}")
                
            self.progress['value'] = total_files
            self.status_var.set("Processing complete!")
            
            # Update results
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "\n".join(results))
            
            messagebox.showinfo("Complete", f"Processed {total_files} images!\nCheck the results panel for details.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Processing failed: {str(e)}")
            
    def process_single_image(self, file_path):
        """Process a single image"""
        # Load image
        image = cv2.imread(file_path)
        if image is None:
            raise Exception("Could not load image")
        
        original_image = image.copy()
        
        # Determine output directory and size
        if self.image_type.get() == "character":
            output_dir = "characters"
            target_size = (300, 400)
            os.makedirs(output_dir, exist_ok=True)
        else:
            output_dir = "lovers"
            target_size = (200, 300)
            os.makedirs(output_dir, exist_ok=True)
        
        # Auto-crop face for characters
        if self.auto_crop_face.get() and self.image_type.get() == "character":
            image = self.crop_to_face(image)
        
        # Enhance quality
        if self.enhance_quality.get():
            image = self.enhance_image_quality(image)
        
        # Remove background (simple method)
        if self.remove_background.get():
            image = self.simple_background_removal(image)
        
        # Convert to PIL for final processing
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        # Resize to optimal dimensions
        if self.resize_optimal.get():
            pil_image = self.resize_with_aspect_ratio(pil_image, target_size)
        
        # Convert to RGBA for transparency
        if pil_image.mode != 'RGBA':
            pil_image = pil_image.convert('RGBA')
        
        # Generate output filename
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_name = f"{base_name}_magadheera.png"
        output_path = os.path.join(output_dir, output_name)
        
        # Handle duplicates
        counter = 1
        while os.path.exists(output_path):
            output_name = f"{base_name}_magadheera_{counter}.png"
            output_path = os.path.join(output_dir, output_name)
            counter += 1
        
        # Save processed image
        pil_image.save(output_path, 'PNG')
        
        return f"✅ {os.path.basename(file_path)} → {output_name}"
        
    def crop_to_face(self, image):
        """Crop image to focus on face"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) > 0:
            # Get the largest face
            largest_face = max(faces, key=lambda f: f[2] * f[3])
            x, y, w, h = largest_face
            
            # Expand crop area around face
            margin = int(max(w, h) * 0.3)
            x1 = max(0, x - margin)
            y1 = max(0, y - margin)
            x2 = min(image.shape[1], x + w + margin)
            y2 = min(image.shape[0], y + h + margin)
            
            return image[y1:y2, x1:x2]
        
        return image
        
    def enhance_image_quality(self, image):
        """Enhance image quality"""
        # Convert to PIL for enhancement
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(pil_image)
        pil_image = enhancer.enhance(1.2)
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(pil_image)
        pil_image = enhancer.enhance(1.1)
        
        # Enhance color
        enhancer = ImageEnhance.Color(pil_image)
        pil_image = enhancer.enhance(1.1)
        
        # Convert back to OpenCV
        return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
    def simple_background_removal(self, image):
        """Simple background removal using edge detection"""
        # Create mask using GrabCut algorithm
        mask = np.zeros(image.shape[:2], np.uint8)
        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)
        
        # Define rectangle around the subject (center area)
        height, width = image.shape[:2]
        rect = (width//6, height//6, width*2//3, height*2//3)
        
        try:
            cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
            mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
            
            # Apply mask
            result = image * mask2[:, :, np.newaxis]
            return result
        except:
            # If GrabCut fails, return original
            return image
            
    def resize_with_aspect_ratio(self, pil_image, target_size):
        """Resize image maintaining aspect ratio"""
        # Calculate new size maintaining aspect ratio
        pil_image.thumbnail(target_size, Image.Resampling.LANCZOS)
        
        # Create new image with target size and transparent background
        new_img = Image.new('RGBA', target_size, (0, 0, 0, 0))
        
        # Center the resized image
        x = (target_size[0] - pil_image.width) // 2
        y = (target_size[1] - pil_image.height) // 2
        new_img.paste(pil_image, (x, y), pil_image if pil_image.mode == 'RGBA' else None)
        
        return new_img
        
    def run(self):
        """Run the converter"""
        self.root.mainloop()

def main():
    """Main function"""
    try:
        converter = SmartImageConverter()
        converter.run()
    except Exception as e:
        print(f"Error starting Smart Image Converter: {e}")
        print("Make sure you have all required packages installed")

if __name__ == "__main__":
    main()
