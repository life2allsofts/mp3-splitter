#!/usr/bin/env python3
"""
MP4 to MP3 Converter + Splitter - Simple GUI
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from src.mp3_splitter import MediaProcessor

class MediaProcessorGUI:
    def __init__(self):
        # Setup the main window
        self.root = tk.Tk()
        self.root.title("🎵 Media Processor Pro")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Initialize variables
        self.input_file = None
        self.processing = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = ttk.Label(
            self.main_frame, 
            text="🎵 MEDIA PROCESSOR PRO", 
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = ttk.Label(
            self.main_frame,
            text="Convert MP4 to MP3 + Split Audio Files",
            font=("Arial", 11)
        )
        subtitle_label.pack(pady=(0, 20))
        
        # File selection section
        file_frame = ttk.LabelFrame(self.main_frame, text="File Selection", padding="10")
        file_frame.pack(fill="x", pady=(0, 15))
        
        # File path display and browse button
        file_selection_frame = ttk.Frame(file_frame)
        file_selection_frame.pack(fill="x")
        
        self.file_path_label = ttk.Label(
            file_selection_frame, 
            text="No file selected",
            wraplength=400
        )
        self.file_path_label.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ttk.Button(
            file_selection_frame,
            text="Browse",
            command=self.browse_file
        ).pack(side="right")
        
        # File info display
        self.file_info_label = ttk.Label(
            file_frame,
            text="Supported: MP4, AVI, MOV, WMV, MKV, MP3, WAV, FLAC",
            font=("Arial", 9)
        )
        self.file_info_label.pack(anchor="w", pady=(5, 0))
        
        # Processing options
        options_frame = ttk.LabelFrame(self.main_frame, text="Processing Options", padding="10")
        options_frame.pack(fill="x", pady=(0, 15))
        
        # Number of parts
        parts_frame = ttk.Frame(options_frame)
        parts_frame.pack(fill="x", pady=5)
        
        ttk.Label(parts_frame, text="Number of Parts:").pack(side="left")
        self.parts_var = tk.StringVar(value="5")
        self.parts_entry = ttk.Entry(
            parts_frame, 
            width=10, 
            textvariable=self.parts_var
        )
        self.parts_entry.pack(side="left", padx=(10, 0))
        
        # Quality selection
        quality_frame = ttk.Frame(options_frame)
        quality_frame.pack(fill="x", pady=5)
        
        ttk.Label(quality_frame, text="Audio Quality:").pack(side="left")
        self.quality_var = tk.StringVar(value="320k")
        quality_options = ttk.Combobox(
            quality_frame,
            values=["128k", "192k", "320k"],
            textvariable=self.quality_var,
            state="readonly",
            width=10
        )
        quality_options.pack(side="left", padx=(10, 0))
        
        # Progress section
        progress_frame = ttk.LabelFrame(self.main_frame, text="Progress", padding="10")
        progress_frame.pack(fill="x", pady=(0, 15))
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.pack(fill="x", pady=5)
        self.progress_bar['value'] = 0
        
        self.status_label = ttk.Label(
            progress_frame,
            text="Ready to process...",
            font=("Arial", 9)
        )
        self.status_label.pack(anchor="w", pady=(5, 0))
        
        # Action buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill="x", pady=(0, 10))
        
        self.process_button = ttk.Button(
            button_frame,
            text="🔄 PROCESS MEDIA",
            command=self.process_media,
            style="Accent.TButton"
        )
        self.process_button.pack(fill="x", pady=5)
        
        # Output info
        self.output_label = ttk.Label(
            self.main_frame,
            text="",
            font=("Arial", 10),
            foreground="green"
        )
        self.output_label.pack(pady=(10, 0))
        
    def browse_file(self):
        """Open file browser to select media file"""
        file_types = [
            ("Media Files", "*.mp4 *.avi *.mov *.wmv *.mkv *.mp3 *.wav *.flac *.m4a *.aac"),
            ("Video Files", "*.mp4 *.avi *.mov *.wmv *.mkv"),
            ("Audio Files", "*.mp3 *.wav *.flac *.m4a *.aac"),
            ("All Files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(filetypes=file_types)
        if filename:
            self.input_file = filename
            self.file_path_label.configure(text=os.path.basename(filename))
            self.update_file_info(filename)
            
    def update_file_info(self, file_path):
        """Update file information display"""
        try:
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                file_ext = os.path.splitext(file_path)[1].lower()
                
                file_type = "Video" if file_ext in ['.mp4', '.avi', '.mov', '.wmv', '.mkv'] else "Audio"
                info_text = f"{file_type} file • {file_size:.2f} MB • {file_ext.upper()}"
                self.file_info_label.configure(text=info_text)
        except Exception as e:
            self.file_info_label.configure(text="Could not read file info")
            
    def process_media(self):
        """Process the media file in a separate thread"""
        if self.processing:
            return
            
        if not self.input_file:
            messagebox.showerror("Error", "Please select a media file first!")
            return
            
        try:
            num_parts = int(self.parts_var.get())
            if num_parts <= 0:
                messagebox.showerror("Error", "Number of parts must be greater than 0!")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for parts!")
            return
            
        # Disable button and start processing
        self.processing = True
        self.process_button.configure(state="disabled", text="PROCESSING...")
        self.progress_bar['value'] = 0
        self.status_label.configure(text="Initializing...")
        self.output_label.configure(text="")
        
        # Start processing in separate thread
        thread = threading.Thread(target=self._process_media_thread, args=(num_parts,))
        thread.daemon = True
        thread.start()
        
    def _process_media_thread(self, num_parts):
        """Process media in background thread"""
        try:
            # Initialize processor
            self.update_status("Loading media file...", 10)
            processor = MediaProcessor(self.input_file)
            
            # Get file info
            info = processor.get_media_info()
            is_video = info['is_video']
            
            # Update status based on file type
            if is_video:
                self.update_status("Converting video to MP3...", 30)
            else:
                self.update_status("Preparing audio for splitting...", 30)
                
            # Process the media
            self.update_status("Splitting into parts...", 60)
            converted_path, output_files = processor.split_media(
                num_parts, 
                bitrate=self.quality_var.get()
            )
            
            # Complete
            self.update_status("Process completed successfully!", 100)
            
            # Show success message
            action = "converted and split" if is_video else "split"
            output_text = f"✅ Successfully {action} into {len(output_files)} parts!"
            self.root.after(0, lambda: self.output_label.configure(text=output_text))
            
            # Cleanup
            processor.cleanup()
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.root.after(0, lambda: self.show_error(error_msg))
            
        finally:
            # Re-enable button
            self.root.after(0, self.processing_complete)
            
    def update_status(self, message, progress):
        """Update status from background thread"""
        self.root.after(0, lambda: self.status_label.configure(text=message))
        self.root.after(0, lambda: self.progress_bar.configure(value=progress))
        
    def show_error(self, message):
        """Show error message"""
        messagebox.showerror("Processing Error", message)
        self.output_label.configure(text="❌ Processing failed!")
        
    def processing_complete(self):
        """Re-enable UI after processing"""
        self.processing = False
        self.process_button.configure(state="normal", text="🔄 PROCESS MEDIA")
        
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = MediaProcessorGUI()
    app.run()