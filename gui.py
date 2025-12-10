"""
GUI Application for PPTX Automation Tool
Provides a user-friendly interface for creating presentations
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkinter.font import Font
import os
import json
from pathlib import Path
from config import SpecBuilder, validate_spec
from main import build_presentation


class PresentationGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PPTX Automation Tool")
        self.root.geometry("900x800")
        self.root.resizable(True, True)
        
        # Variables
        self.language_var = tk.StringVar(value="es")
        self.slides_count_var = tk.IntVar(value=10)
        self.brand_name_var = tk.StringVar(value="")
        self.user_name_var = tk.StringVar(value="")
        self.footer_text_var = tk.StringVar(value="Confidential 2026")
        self.show_numbers_var = tk.BooleanVar(value=True)
        self.description_text = ""
        self.logo_path = ""
        self.image_paths = []
        self.audio_paths = []
        self.primary_color_var = tk.StringVar(value="#1F2D3D")
        self.accent_color_var = tk.StringVar(value="#2979FF")
        self.font_family_var = tk.StringVar(value="Inter")
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_font = Font(family="Segoe UI", size=18, weight="bold")
        title_label = ttk.Label(main_frame, text="🎨 Presentation Generator", font=title_font)
        title_label.grid(row=0, column=0, pady=(0, 20), sticky=tk.W)
        
        # Language Selection
        lang_frame = ttk.LabelFrame(main_frame, text="Language / Idioma", padding="10")
        lang_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        lang_frame.columnconfigure(1, weight=1)
        
        ttk.Radiobutton(lang_frame, text="🇪🇸 Español", variable=self.language_var, 
                       value="es", command=self.update_language_labels).grid(row=0, column=0, padx=10)
        ttk.Radiobutton(lang_frame, text="🇬🇧 English", variable=self.language_var, 
                       value="en", command=self.update_language_labels).grid(row=0, column=1, padx=10)
        
        # Basic Information
        info_frame = ttk.LabelFrame(main_frame, text="Basic Information", padding="10")
        info_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        info_frame.columnconfigure(1, weight=1)
        
        ttk.Label(info_frame, text="Brand/Company Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(info_frame, textvariable=self.brand_name_var, width=40).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        ttk.Label(info_frame, text="Your Name (optional):").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(info_frame, textvariable=self.user_name_var, width=40).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        ttk.Label(info_frame, text="Number of Slides:").grid(row=2, column=0, sticky=tk.W, pady=5)
        slides_spin = ttk.Spinbox(info_frame, from_=3, to=50, textvariable=self.slides_count_var, width=10)
        slides_spin.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Content Section
        content_frame = ttk.LabelFrame(main_frame, text="Content", padding="10")
        content_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        desc_label_frame = ttk.Frame(content_frame)
        desc_label_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(desc_label_frame, text="Description (paste text or load from file):").pack(side=tk.LEFT)
        ttk.Button(desc_label_frame, text="📁 Load from file", command=self.load_text_file).pack(side=tk.RIGHT)
        
        self.description_textbox = scrolledtext.ScrolledText(content_frame, height=8, wrap=tk.WORD)
        self.description_textbox.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Images Section
        images_frame = ttk.LabelFrame(main_frame, text="Images (optional)", padding="10")
        images_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        images_frame.columnconfigure(0, weight=1)
        
        btn_frame = ttk.Frame(images_frame)
        btn_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(btn_frame, text="➕ Add Images", command=self.add_images).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="🗑️ Clear Images", command=self.clear_images).pack(side=tk.LEFT)
        
        self.images_label = ttk.Label(images_frame, text="No images added", foreground="gray")
        self.images_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # Logo Section
        logo_frame = ttk.LabelFrame(main_frame, text="Logo (optional)", padding="10")
        logo_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        logo_frame.columnconfigure(0, weight=1)
        
        logo_btn_frame = ttk.Frame(logo_frame)
        logo_btn_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(logo_btn_frame, text="📁 Select Logo", command=self.select_logo).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(logo_btn_frame, text="✖ Clear Logo", command=self.clear_logo).pack(side=tk.LEFT)
        
        self.logo_label = ttk.Label(logo_frame, text="No logo selected", foreground="gray")
        self.logo_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # Theme Section
        theme_frame = ttk.LabelFrame(main_frame, text="Theme & Styling", padding="10")
        theme_frame.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        theme_frame.columnconfigure(1, weight=1)
        theme_frame.columnconfigure(3, weight=1)
        
        ttk.Label(theme_frame, text="Font:").grid(row=0, column=0, sticky=tk.W, pady=5)
        font_combo = ttk.Combobox(theme_frame, textvariable=self.font_family_var, 
                                  values=["Inter", "Arial", "Helvetica", "Roboto", "Calibri", "Times New Roman"],
                                  state="readonly", width=15)
        font_combo.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 20))
        
        ttk.Label(theme_frame, text="Primary Color:").grid(row=0, column=2, sticky=tk.W, pady=5)
        primary_color_frame = ttk.Frame(theme_frame)
        primary_color_frame.grid(row=0, column=3, sticky=tk.W, pady=5, padx=(10, 0))
        ttk.Entry(primary_color_frame, textvariable=self.primary_color_var, width=10).pack(side=tk.LEFT)
        ttk.Button(primary_color_frame, text="🎨", width=3, 
                  command=lambda: self.choose_color(self.primary_color_var)).pack(side=tk.LEFT, padx=(5, 0))
        
        ttk.Label(theme_frame, text="Accent Color:").grid(row=1, column=2, sticky=tk.W, pady=5)
        accent_color_frame = ttk.Frame(theme_frame)
        accent_color_frame.grid(row=1, column=3, sticky=tk.W, pady=5, padx=(10, 0))
        ttk.Entry(accent_color_frame, textvariable=self.accent_color_var, width=10).pack(side=tk.LEFT)
        ttk.Button(accent_color_frame, text="🎨", width=3, 
                  command=lambda: self.choose_color(self.accent_color_var)).pack(side=tk.LEFT, padx=(5, 0))
        
        # Footer Section
        footer_frame = ttk.LabelFrame(main_frame, text="Footer Settings", padding="10")
        footer_frame.grid(row=7, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        footer_frame.columnconfigure(1, weight=1)
        
        ttk.Label(footer_frame, text="Footer Text:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(footer_frame, textvariable=self.footer_text_var, width=40).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        ttk.Checkbutton(footer_frame, text="Show slide numbers", 
                       variable=self.show_numbers_var).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Generate Button
        generate_btn = ttk.Button(main_frame, text="🚀 Generate Presentation", 
                                 command=self.generate_presentation, style="Accent.TButton")
        generate_btn.grid(row=8, column=0, pady=(10, 0), sticky=(tk.W, tk.E))
        
        # Status bar
        self.status_label = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=9, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Style configuration
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Segoe UI", 11, "bold"))
        
    def update_language_labels(self):
        """Update UI labels based on selected language."""
        # This can be expanded to translate all UI elements
        pass
    
    def load_text_file(self):
        """Load text from a file into the description box."""
        file_path = filedialog.askopenfilename(
            title="Select Text File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.description_textbox.delete('1.0', tk.END)
                    self.description_textbox.insert('1.0', content)
            except Exception as e:
                messagebox.showerror("Error", f"Could not read file: {e}")
    
    def add_images(self):
        """Add images for the presentation."""
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*")]
        )
        if files:
            self.image_paths.extend(files)
            self.update_images_label()
    
    def clear_images(self):
        """Clear all selected images."""
        self.image_paths = []
        self.update_images_label()
    
    def update_images_label(self):
        """Update the images label."""
        if self.image_paths:
            count = len(self.image_paths)
            self.images_label.config(text=f"{count} image(s) added", foreground="green")
        else:
            self.images_label.config(text="No images added", foreground="gray")
    
    def select_logo(self):
        """Select a logo file."""
        file = filedialog.askopenfilename(
            title="Select Logo",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.svg"), ("All files", "*.*")]
        )
        if file:
            self.logo_path = file
            self.logo_label.config(text=Path(file).name, foreground="green")
    
    def clear_logo(self):
        """Clear the selected logo."""
        self.logo_path = ""
        self.logo_label.config(text="No logo selected", foreground="gray")
    
    def choose_color(self, color_var):
        """Open color picker dialog."""
        try:
            from tkinter import colorchooser
            color = colorchooser.askcolor(title="Choose Color", initialcolor=color_var.get())
            if color[1]:
                color_var.set(color[1])
        except Exception as e:
            messagebox.showwarning("Color Picker", "Color picker not available. Please enter hex color manually.")
    
    def generate_presentation(self):
        """Generate the presentation."""
        # Validate inputs
        if not self.brand_name_var.get().strip():
            messagebox.showerror("Error", "Please enter a brand/company name.")
            return
        
        description = self.description_textbox.get('1.0', tk.END).strip()
        if not description and not self.image_paths and not self.audio_paths:
            messagebox.showerror("Error", "Please provide a description, images, or audio files.")
            return
        
        try:
            self.status_label.config(text="Generating presentation...")
            self.root.update()
            
            # Build specification
            spec_builder = SpecBuilder(language=self.language_var.get())
            spec_builder.set_slides_count(self.slides_count_var.get())
            spec_builder.set_user(
                name=self.user_name_var.get() if self.user_name_var.get() else None,
                brand_name=self.brand_name_var.get(),
                logo_path=self.logo_path if self.logo_path else None
            )
            spec_builder.set_footer(self.footer_text_var.get(), self.show_numbers_var.get())
            spec_builder.set_theme(
                font_family=self.font_family_var.get(),
                primary_color=self.primary_color_var.get(),
                accent_color=self.accent_color_var.get()
            )
            spec_builder.set_description(description)
            
            # Add images
            for img_path in self.image_paths:
                spec_builder.add_image(img_path, Path(img_path).stem)
            
            # Set output directory
            output_dir = "output"
            spec_builder.set_output_dir(output_dir)
            
            spec = spec_builder.build()
            
            # Validate
            is_valid, errors = validate_spec(spec)
            if not is_valid:
                messagebox.showerror("Validation Error", "\n".join(errors))
                self.status_label.config(text="Validation failed")
                return
            
            # Generate
            result = build_presentation(spec, language=self.language_var.get())
            
            self.status_label.config(text="✅ Generation complete!")
            
            # Show success dialog with results
            msg = f"Presentation generated successfully!\n\n"
            msg += f"PPTX: {result['pptx']}\n"
            msg += f"HTML: {result['html']}\n\n"
            msg += "Would you like to open the output folder?"
            
            if messagebox.askyesno("Success", msg):
                os.startfile(output_dir)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate presentation:\n{str(e)}")
            self.status_label.config(text="❌ Generation failed")
            import traceback
            traceback.print_exc()


def main():
    """Main entry point for the GUI application."""
    root = tk.Tk()
    app = PresentationGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
