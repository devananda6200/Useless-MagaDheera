#!/usr/bin/env python3
"""
Quick Image Replacement Tool
Simple drag-and-drop interface to replace placeholder images
"""

import os
import shutil
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD

class QuickImageReplacer:
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.title("🏰 Quick Image Replacer - Magadheera")
        self.root.geometry("800x600")
        self.root.configure(bg="#2C3E50")
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = tk.Label(self.root, text="🏰 Quick Image Replacer", 
                              font=("Arial", 20, "bold"), fg="#F39C12", bg="#2C3E50")
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(self.root, text="Drag & Drop your Magadheera images here", 
                                 font=("Arial", 14), fg="#ECF0F1", bg="#2C3E50")
        subtitle_label.pack(pady=10)
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#2C3E50")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Characters drop zone
        self.setup_drop_zone(main_frame, "🏰 WARRIORS/CHARACTERS", "characters", "#E74C3C")
        
        # Lovers drop zone  
        self.setup_drop_zone(main_frame, "👸 PRINCESSES/LOVERS", "lovers", "#9B59B6")
        
        # Control buttons
        button_frame = tk.Frame(self.root, bg="#2C3E50")
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="📁 Browse Files", command=self.browse_files,
                 bg="#3498DB", fg="white", font=("Arial", 12, "bold"), 
                 padx=20, pady=10).pack(side="left", padx=10)
        
        tk.Button(button_frame, text="🗑️ Clear All", command=self.clear_all,
                 bg="#E67E22", fg="white", font=("Arial", 12, "bold"), 
                 padx=20, pady=10).pack(side="left", padx=10)
        
        tk.Button(button_frame, text="✅ Test App", command=self.test_app,
                 bg="#27AE60", fg="white", font=("Arial", 12, "bold"), 
                 padx=20, pady=10).pack(side="left", padx=10)
        
        # Status
        self.status_var = tk.StringVar(value="Ready - Drag images or click Browse Files")
        status_label = tk.Label(self.root, textvariable=self.status_var, 
                               font=("Arial", 11), fg="#BDC3C7", bg="#2C3E50")
        status_label.pack(pady=10)
        
    def setup_drop_zone(self, parent, title, folder_type, color):
        """Setup a drag and drop zone"""
        # Container frame
        container = tk.Frame(parent, bg="#2C3E50")
        container.pack(side="left", fill="both", expand=True, padx=10)
        
        # Title
        title_label = tk.Label(container, text=title, font=("Arial", 16, "bold"), 
                              fg=color, bg="#2C3E50")
        title_label.pack(pady=10)
        
        # Drop zone
        drop_frame = tk.Frame(container, bg="#34495E", relief="raised", bd=2)
        drop_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Drop zone label
        drop_label = tk.Label(drop_frame, 
                             text=f"Drop {title.split()[1]} images here\n\nSupported: PNG, JPG, JPEG\nOptimal size: {'300x400' if folder_type == 'characters' else '200x300'}", 
                             font=("Arial", 12), fg="#ECF0F1", bg="#34495E",
                             justify="center")
        drop_label.pack(expand=True)
        
        # Enable drag and drop
        drop_frame.drop_target_register(DND_FILES)
        drop_frame.dnd_bind('<<Drop>>', lambda e: self.handle_drop(e, folder_type))
        
        # Current images list
        list_frame = tk.Frame(container, bg="#2C3E50")
        list_frame.pack(fill="x", pady=10)
        
        tk.Label(list_frame, text="Current Images:", font=("Arial", 11, "bold"), 
                fg="#ECF0F1", bg="#2C3E50").pack(anchor="w")
        
        listbox = tk.Listbox(list_frame, height=8, bg="#34495E", fg="#ECF0F1", 
                            selectbackground=color)
        listbox.pack(fill="x", pady=5)
        
        # Store references
        if folder_type == "characters":
            self.char_listbox = listbox
        else:
            self.lover_listbox = listbox
            
        # Update list
        self.update_image_list(folder_type)
        
    def handle_drop(self, event, folder_type):
        """Handle dropped files"""
        files = self.root.tk.splitlist(event.data)
        
        processed = 0
        for file_path in files:
            if self.is_image_file(file_path):
                if self.process_image(file_path, folder_type):
                    processed += 1
        
        if processed > 0:
            self.status_var.set(f"✅ Added {processed} images to {folder_type}")
            self.update_image_list(folder_type)
        else:
            self.status_var.set("❌ No valid images were processed")
            
    def is_image_file(self, file_path):
        """Check if file is a valid image"""
        valid_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
        return os.path.splitext(file_path.lower())[1] in valid_extensions
        
    def process_image(self, file_path, folder_type):
        """Process and save an image"""
        try:
            # Determine target directory and size
            if folder_type == "characters":
                target_dir = "characters"
                target_size = (300, 400)
            else:
                target_dir = "lovers"
                target_size = (200, 300)
                
            os.makedirs(target_dir, exist_ok=True)
            
            # Generate output filename
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            output_name = f"{base_name}.png"
            output_path = os.path.join(target_dir, output_name)
            
            # Handle duplicates
            counter = 1
            while os.path.exists(output_path):
                output_name = f"{base_name}_{counter}.png"
                output_path = os.path.join(target_dir, output_name)
                counter += 1
            
            # Process image
            with Image.open(file_path) as img:
                # Convert to RGBA
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                # Resize maintaining aspect ratio
                img.thumbnail(target_size, Image.Resampling.LANCZOS)
                
                # Create new image with target size and transparent background
                new_img = Image.new('RGBA', target_size, (0, 0, 0, 0))
                
                # Center the resized image
                x = (target_size[0] - img.width) // 2
                y = (target_size[1] - img.height) // 2
                new_img.paste(img, (x, y), img)
                
                # Save
                new_img.save(output_path, 'PNG')
                
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process {os.path.basename(file_path)}:\n{str(e)}")
            return False
            
    def update_image_list(self, folder_type):
        """Update the image list display"""
        if folder_type == "characters":
            listbox = self.char_listbox
            directory = "characters"
        else:
            listbox = self.lover_listbox
            directory = "lovers"
            
        listbox.delete(0, tk.END)
        
        if os.path.exists(directory):
            files = [f for f in os.listdir(directory) if f.lower().endswith('.png')]
            for file in sorted(files):
                listbox.insert(tk.END, file)
                
    def browse_files(self):
        """Browse for files to add"""
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
        )
        
        if not files:
            return
            
        # Ask user what type of images these are
        choice = messagebox.askyesnocancel(
            "Image Type", 
            "Are these WARRIOR/CHARACTER images?\n\n"
            "Yes = Warriors (for face replacement)\n"
            "No = Princesses/Lovers (floating images)\n"
            "Cancel = Cancel operation"
        )
        
        if choice is None:  # Cancel
            return
            
        folder_type = "characters" if choice else "lovers"
        
        processed = 0
        for file_path in files:
            if self.process_image(file_path, folder_type):
                processed += 1
                
        if processed > 0:
            self.status_var.set(f"✅ Added {processed} images to {folder_type}")
            self.update_image_list("characters")
            self.update_image_list("lovers")
        else:
            self.status_var.set("❌ No images were processed")
            
    def clear_all(self):
        """Clear all images"""
        if messagebox.askyesno("Confirm", "Delete ALL custom images and restore placeholders?"):
            try:
                # Clear directories
                for directory in ["characters", "lovers"]:
                    if os.path.exists(directory):
                        for file in os.listdir(directory):
                            if file.endswith('.png'):
                                os.remove(os.path.join(directory, file))
                
                # Recreate placeholders
                import subprocess
                subprocess.run(["python", "create_placeholders.py"], check=True)
                
                # Update lists
                self.update_image_list("characters")
                self.update_image_list("lovers")
                
                self.status_var.set("✅ All images cleared and placeholders restored")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear images: {str(e)}")
                
    def test_app(self):
        """Test the app with current images"""
        try:
            import webbrowser
            webbrowser.open('http://localhost:3000')
            self.status_var.set("🌐 Opened Magadheera app in browser")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open browser: {str(e)}")
            
    def run(self):
        """Run the replacer"""
        self.root.mainloop()

def main():
    """Main function"""
    try:
        replacer = QuickImageReplacer()
        replacer.run()
    except ImportError:
        print("❌ tkinterdnd2 not installed. Installing...")
        import subprocess
        subprocess.run(["pip", "install", "tkinterdnd2"])
        print("✅ Please run the script again")
    except Exception as e:
        print(f"Error: {e}")
        print("Falling back to basic image manager...")
        import subprocess
        subprocess.run(["python", "image_manager.py"])

if __name__ == "__main__":
    main()
