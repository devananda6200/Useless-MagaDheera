#!/usr/bin/env python3
"""
Comprehensive Image Manager for Magadheera App
Allows easy addition and management of custom character images
"""

import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import json

class MagadheeraImageManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Magadheera Image Manager")
        self.root.geometry("800x600")
        
        # Directories
        self.characters_dir = "characters"
        self.lovers_dir = "lovers"
        
        # Ensure directories exist
        os.makedirs(self.characters_dir, exist_ok=True)
        os.makedirs(self.lovers_dir, exist_ok=True)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main title
        title_label = tk.Label(self.root, text="🏰 Magadheera Image Manager", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Characters tab
        char_frame = ttk.Frame(notebook)
        notebook.add(char_frame, text="🏰 Warriors/Characters")
        self.setup_characters_tab(char_frame)
        
        # Lovers tab
        lovers_frame = ttk.Frame(notebook)
        notebook.add(lovers_frame, text="👸 Princesses/Lovers")
        self.setup_lovers_tab(lovers_frame)
        
        # Instructions tab
        instructions_frame = ttk.Frame(notebook)
        notebook.add(instructions_frame, text="📖 Instructions")
        self.setup_instructions_tab(instructions_frame)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to add your custom images!")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def setup_characters_tab(self, parent):
        """Setup the characters management tab"""
        # Instructions
        inst_label = tk.Label(parent, text="Add warrior/character images for face replacement", 
                             font=("Arial", 12))
        inst_label.pack(pady=5)
        
        # Buttons frame
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="➕ Add Character Images", 
                 command=self.add_character_images, bg="#4CAF50", fg="white",
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🗑️ Clear All Characters", 
                 command=self.clear_characters, bg="#f44336", fg="white",
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🔄 Refresh List", 
                 command=self.refresh_character_list, bg="#2196F3", fg="white",
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Current images list
        list_frame = tk.Frame(parent)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(list_frame, text="Current Character Images:", 
                font=("Arial", 11, "bold")).pack(anchor="w")
        
        # Listbox with scrollbar
        listbox_frame = tk.Frame(list_frame)
        listbox_frame.pack(fill="both", expand=True)
        
        self.char_listbox = tk.Listbox(listbox_frame, height=10)
        char_scrollbar = tk.Scrollbar(listbox_frame, orient="vertical")
        self.char_listbox.config(yscrollcommand=char_scrollbar.set)
        char_scrollbar.config(command=self.char_listbox.yview)
        
        self.char_listbox.pack(side="left", fill="both", expand=True)
        char_scrollbar.pack(side="right", fill="y")
        
        # Delete selected button
        tk.Button(list_frame, text="🗑️ Delete Selected", 
                 command=self.delete_selected_character, bg="#ff9800", fg="white").pack(pady=5)
        
        self.refresh_character_list()
        
    def setup_lovers_tab(self, parent):
        """Setup the lovers management tab"""
        # Instructions
        inst_label = tk.Label(parent, text="Add princess/lover images that appear floating in the result", 
                             font=("Arial", 12))
        inst_label.pack(pady=5)
        
        # Buttons frame
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="➕ Add Lover Images", 
                 command=self.add_lover_images, bg="#E91E63", fg="white",
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🗑️ Clear All Lovers", 
                 command=self.clear_lovers, bg="#f44336", fg="white",
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🔄 Refresh List", 
                 command=self.refresh_lover_list, bg="#2196F3", fg="white",
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Current images list
        list_frame = tk.Frame(parent)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(list_frame, text="Current Lover Images:", 
                font=("Arial", 11, "bold")).pack(anchor="w")
        
        # Listbox with scrollbar
        listbox_frame = tk.Frame(list_frame)
        listbox_frame.pack(fill="both", expand=True)
        
        self.lover_listbox = tk.Listbox(listbox_frame, height=10)
        lover_scrollbar = tk.Scrollbar(listbox_frame, orient="vertical")
        self.lover_listbox.config(yscrollcommand=lover_scrollbar.set)
        lover_scrollbar.config(command=self.lover_listbox.yview)
        
        self.lover_listbox.pack(side="left", fill="both", expand=True)
        lover_scrollbar.pack(side="right", fill="y")
        
        # Delete selected button
        tk.Button(list_frame, text="🗑️ Delete Selected", 
                 command=self.delete_selected_lover, bg="#ff9800", fg="white").pack(pady=5)
        
        self.refresh_lover_list()
        
    def setup_instructions_tab(self, parent):
        """Setup the instructions tab"""
        # Create scrollable text widget
        text_frame = tk.Frame(parent)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Arial", 10))
        scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        instructions = """
🏰 MAGADHEERA IMAGE MANAGER INSTRUCTIONS

OVERVIEW:
This tool helps you add custom character images to your Magadheera Past Life Reveal app.

TYPES OF IMAGES:

1. 🏰 WARRIORS/CHARACTERS:
   - These images replace the user's face in the final result
   - Should contain warrior faces, character portraits, or any face you want to overlay
   - Best results with clear, front-facing portraits
   - Recommended size: 300x400 pixels (will be auto-resized)

2. 👸 PRINCESSES/LOVERS:
   - These appear as floating images in the corner of the result
   - Should contain princess, lover, or companion character images
   - Appear smaller in the final result
   - Recommended size: 200x300 pixels (will be auto-resized)

HOW TO USE:

1. ADDING IMAGES:
   - Click "Add Character Images" or "Add Lover Images"
   - Select multiple image files (PNG, JPG, JPEG supported)
   - Images will be automatically processed and resized
   - Transparent backgrounds (PNG) work best but not required

2. MANAGING IMAGES:
   - View current images in the lists
   - Delete individual images by selecting and clicking "Delete Selected"
   - Clear all images with "Clear All" buttons
   - Refresh lists to see updates

3. SUPPORTED FORMATS:
   - PNG (recommended - supports transparency)
   - JPG/JPEG (will work but no transparency)
   - Images are automatically converted to PNG format

4. TIPS FOR BEST RESULTS:
   - Use high-quality, clear images
   - Front-facing portraits work best for characters
   - Remove backgrounds if possible (use online tools like remove.bg)
   - Ensure faces are clearly visible and well-lit

AFTER ADDING IMAGES:

1. Close this manager
2. Restart your backend server: python app.py
3. Test the app at: http://localhost:3000
4. Your custom images will now be used for face replacement!

TROUBLESHOOTING:

- If images don't appear: Check that backend server is restarted
- If face replacement doesn't work well: Try images with clearer faces
- If app crashes: Check that image files are not corrupted
- For best results: Use PNG images with transparent backgrounds

EXAMPLE WORKFLOW:

1. Save warrior/character images from internet or your collection
2. Use this manager to add them to the "Characters" section
3. Add princess/lover images to the "Lovers" section
4. Restart backend server
5. Test the app - your face will be replaced with random characters!

The app will randomly select from your custom images each time someone uses it.
"""
        
        text_widget.insert("1.0", instructions)
        text_widget.config(state=tk.DISABLED)  # Make read-only
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def add_character_images(self):
        """Add character images"""
        files = filedialog.askopenfilenames(
            title="Select Character Images",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("All files", "*.*")
            ]
        )
        
        if files:
            success_count = 0
            for file_path in files:
                if self.process_and_save_image(file_path, self.characters_dir, (300, 400)):
                    success_count += 1
            
            self.status_var.set(f"Added {success_count}/{len(files)} character images successfully!")
            self.refresh_character_list()
            
            if success_count > 0:
                messagebox.showinfo("Success", 
                    f"Added {success_count} character images!\n\n"
                    "Remember to restart your backend server to use the new images.")
        
    def add_lover_images(self):
        """Add lover images"""
        files = filedialog.askopenfilenames(
            title="Select Lover/Princess Images",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("All files", "*.*")
            ]
        )
        
        if files:
            success_count = 0
            for file_path in files:
                if self.process_and_save_image(file_path, self.lovers_dir, (200, 300)):
                    success_count += 1
            
            self.status_var.set(f"Added {success_count}/{len(files)} lover images successfully!")
            self.refresh_lover_list()
            
            if success_count > 0:
                messagebox.showinfo("Success", 
                    f"Added {success_count} lover images!\n\n"
                    "Remember to restart your backend server to use the new images.")
    
    def process_and_save_image(self, input_path, output_dir, target_size):
        """Process and save an image"""
        try:
            # Generate output filename
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(output_dir, f"{base_name}.png")
            
            # Handle duplicate names
            counter = 1
            while os.path.exists(output_path):
                output_path = os.path.join(output_dir, f"{base_name}_{counter}.png")
                counter += 1
            
            # Process image
            with Image.open(input_path) as img:
                # Convert to RGBA for transparency support
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
                
                # Save as PNG
                new_img.save(output_path, 'PNG')
                return True
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process {os.path.basename(input_path)}:\n{str(e)}")
            return False
    
    def refresh_character_list(self):
        """Refresh the character images list"""
        self.char_listbox.delete(0, tk.END)
        if os.path.exists(self.characters_dir):
            files = [f for f in os.listdir(self.characters_dir) if f.lower().endswith('.png')]
            for file in sorted(files):
                # Get image info
                try:
                    img_path = os.path.join(self.characters_dir, file)
                    with Image.open(img_path) as img:
                        info = f"{file} ({img.size[0]}x{img.size[1]})"
                        self.char_listbox.insert(tk.END, info)
                except:
                    self.char_listbox.insert(tk.END, f"{file} (error)")
    
    def refresh_lover_list(self):
        """Refresh the lover images list"""
        self.lover_listbox.delete(0, tk.END)
        if os.path.exists(self.lovers_dir):
            files = [f for f in os.listdir(self.lovers_dir) if f.lower().endswith('.png')]
            for file in sorted(files):
                # Get image info
                try:
                    img_path = os.path.join(self.lovers_dir, file)
                    with Image.open(img_path) as img:
                        info = f"{file} ({img.size[0]}x{img.size[1]})"
                        self.lover_listbox.insert(tk.END, info)
                except:
                    self.lover_listbox.insert(tk.END, f"{file} (error)")
    
    def delete_selected_character(self):
        """Delete selected character image"""
        selection = self.char_listbox.curselection()
        if selection:
            item_text = self.char_listbox.get(selection[0])
            filename = item_text.split(' (')[0]  # Extract filename
            
            if messagebox.askyesno("Confirm Delete", f"Delete {filename}?"):
                try:
                    os.remove(os.path.join(self.characters_dir, filename))
                    self.refresh_character_list()
                    self.status_var.set(f"Deleted {filename}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete {filename}:\n{str(e)}")
    
    def delete_selected_lover(self):
        """Delete selected lover image"""
        selection = self.lover_listbox.curselection()
        if selection:
            item_text = self.lover_listbox.get(selection[0])
            filename = item_text.split(' (')[0]  # Extract filename
            
            if messagebox.askyesno("Confirm Delete", f"Delete {filename}?"):
                try:
                    os.remove(os.path.join(self.lovers_dir, filename))
                    self.refresh_lover_list()
                    self.status_var.set(f"Deleted {filename}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete {filename}:\n{str(e)}")
    
    def clear_characters(self):
        """Clear all character images"""
        if messagebox.askyesno("Confirm Clear", "Delete ALL character images?"):
            try:
                for file in os.listdir(self.characters_dir):
                    if file.lower().endswith('.png'):
                        os.remove(os.path.join(self.characters_dir, file))
                self.refresh_character_list()
                self.status_var.set("All character images cleared")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear images:\n{str(e)}")
    
    def clear_lovers(self):
        """Clear all lover images"""
        if messagebox.askyesno("Confirm Clear", "Delete ALL lover images?"):
            try:
                for file in os.listdir(self.lovers_dir):
                    if file.lower().endswith('.png'):
                        os.remove(os.path.join(self.lovers_dir, file))
                self.refresh_lover_list()
                self.status_var.set("All lover images cleared")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear images:\n{str(e)}")
    
    def run(self):
        """Run the image manager"""
        self.root.mainloop()

def main():
    """Main function"""
    try:
        app = MagadheeraImageManager()
        app.run()
    except Exception as e:
        print(f"Error starting Image Manager: {e}")
        print("Make sure you have tkinter installed: pip install tk")

if __name__ == "__main__":
    main()
