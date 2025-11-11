#!/usr/bin/env python3
"""
MP4 to MP3 Converter + Splitter - Enhanced GUI with Optional Splitting
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
        self.root.geometry("700x600")  # Good default size
        self.root.minsize(650, 550)   # Set minimum size
        self.root.resizable(True, True)

        # Initialize variables
        self.input_file = None
        self.processing = False
        self.media_info = None

        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface"""
        # Main container with consistent padding
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill="both", expand=True)

        # Title
        title_label = tk.Label(
            self.main_frame,
            text="🎵 MEDIA PROCESSOR PRO",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 10))

        # Subtitle
        subtitle_label = tk.Label(
            self.main_frame,
            text="Convert Videos to MP3 • Optional Audio Splitting",
            font=("Arial", 11)
        )
        subtitle_label.pack(pady=(0, 20))

        # File selection section
        file_frame = ttk.LabelFrame(self.main_frame, text="File Selection", padding="10")
        file_frame.pack(fill="x", pady=(0, 15))

        # File path display and browse button
        file_selection_frame = ttk.Frame(file_frame)
        file_selection_frame.pack(fill="x")

        self.file_path_label = tk.Label(
            file_selection_frame,
            text="No file selected",
            wraplength=400,
            foreground="gray",
            font=("Arial", 9)
        )
        self.file_path_label.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ttk.Button(
            file_selection_frame,
            text="Browse",
            command=self.browse_file
        ).pack(side="right")

        # File info display
        self.file_info_label = tk.Label(
            file_frame,
            text="Supported: MP4, AVI, MOV, WMV, MKV, MP3, WAV, FLAC",
            font=("Arial", 9),
            foreground="blue"
        )
        self.file_info_label.pack(anchor="w", pady=(5, 0))

        # Media Info Section
        self.info_frame = ttk.LabelFrame(self.main_frame, text="Media Information", padding="10")
        self.info_frame.pack(fill="x", pady=(0, 15))

        self.media_info_label = tk.Label(
            self.info_frame,
            text="Select a file to see details",
            font=("Arial", 10),
            justify="left"
        )
        self.media_info_label.pack(anchor="w")

        # Processing options
        options_frame = ttk.LabelFrame(self.main_frame, text="Processing Options", padding="10")
        options_frame.pack(fill="x", pady=(0, 15))

        # Quality selection
        quality_frame = ttk.Frame(options_frame)
        quality_frame.pack(fill="x", pady=5)

        tk.Label(quality_frame, text="Audio Quality:", font=("Arial", 9)).pack(side="left")
        self.quality_var = tk.StringVar(value="320k")
        quality_options = ttk.Combobox(
            quality_frame,
            values=["128k", "192k", "320k"],
            textvariable=self.quality_var,
            state="readonly",
            width=10
        )
        quality_options.pack(side="left", padx=(10, 0))

        # Splitting options
        splitting_frame = ttk.Frame(options_frame)
        splitting_frame.pack(fill="x", pady=10)

        self.split_var = tk.BooleanVar(value=True)
        self.split_check = tk.Checkbutton(
            splitting_frame,
            text="Split audio into multiple parts",
            variable=self.split_var,
            command=self.toggle_splitting_options
        )
        self.split_check.pack(anchor="w")

        # Splitting details frame
        self.splitting_details_frame = ttk.Frame(options_frame)
        self.splitting_details_frame.pack(fill="x", pady=5)

        # Initialize splitting options
        self.initialize_splitting_options()

        # Progress section
        progress_frame = ttk.LabelFrame(self.main_frame, text="Progress", padding="10")
        progress_frame.pack(fill="x", pady=(0, 15))

        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.pack(fill="x", pady=5)
        self.progress_bar['value'] = 0

        self.status_label = tk.Label(
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
            command=self.process_media
        )
        self.process_button.pack(fill="x", pady=5)

        # Output info
        self.output_label = tk.Label(
            self.main_frame,
            text="",
            font=("Arial", 10),
            foreground="green"
        )
        self.output_label.pack(pady=(10, 0))

    def initialize_splitting_options(self):
        """Initialize the splitting options UI"""
        self.toggle_splitting_options()

    def toggle_splitting_options(self):
        """Show/hide splitting options"""
        # Clear the splitting details frame
        for widget in self.splitting_details_frame.winfo_children():
            widget.destroy()

        if self.split_var.get():
            # Show splitting options
            parts_frame = ttk.Frame(self.splitting_details_frame)
            parts_frame.pack(fill="x", pady=5)

            tk.Label(parts_frame, text="Number of Parts:").pack(side="left")
            self.parts_var = tk.StringVar(value="3")
            self.parts_entry = ttk.Entry(
                parts_frame,
                width=10,
                textvariable=self.parts_var
            )
            self.parts_entry.pack(side="left", padx=(10, 0))
            self.parts_entry.bind('<KeyRelease>', lambda e: self.update_duration_info())

            # Duration info
            self.duration_info_label = tk.Label(
                self.splitting_details_frame,
                text="Duration per part: --:--",
                font=("Arial", 9),
                foreground="green"
            )
            self.duration_info_label.pack(anchor="w", pady=(5, 0))
            
            # Update duration if we have media info
            if self.media_info:
                self.update_duration_info()
        else:
            # Show disabled state message
            disabled_label = tk.Label(
                self.splitting_details_frame,
                text="Single file output (no splitting)",
                font=("Arial", 9),
                foreground="gray"
            )
            disabled_label.pack(anchor="w", pady=5)

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
            display_name = os.path.basename(filename)
            if len(display_name) > 40:
                display_name = display_name[:37] + "..."
            self.file_path_label.configure(text=display_name, foreground="black")
            self.update_file_info(filename)

    def update_file_info(self, file_path):
        """Update file information display"""
        try:
            if os.path.exists(file_path):
                # Get basic file info
                file_size = os.path.getsize(file_path) / (1024 * 1024)
                file_ext = os.path.splitext(file_path)[1].lower()

                file_type = "Video" if file_ext in ['.mp4', '.avi', '.mov', '.wmv', '.mkv'] else "Audio"
                info_text = f"{file_type} file • {file_size:.2f} MB • {file_ext.upper()}"
                self.file_info_label.configure(text=info_text)

                # Get detailed media info
                self.load_media_info(file_path)
        except Exception:
            self.file_info_label.configure(text="Could not read file info")

    def load_media_info(self, file_path):
        """Load detailed media information"""
        try:
            processor = MediaProcessor(file_path)
            self.media_info = processor.get_media_info()

            info_text = f"Duration: {self.media_info['formatted_duration']} • Size: {self.media_info['file_size_mb']} MB"
            if self.media_info['is_video']:
                info_text += " • Type: Video"
            else:
                info_text += " • Type: Audio"

            self.media_info_label.configure(text=info_text)
            self.update_duration_info()
        except Exception:
            self.media_info_label.configure(text="Could not load media details")

    def update_duration_info(self):
        """Update duration per part information"""
        if self.media_info and self.media_info.get('duration_ms', 0) > 0 and self.split_var.get():
            try:
                num_parts = int(self.parts_var.get())
                if num_parts > 0:
                    duration_ms = self.media_info['duration_ms']
                    part_duration_ms = duration_ms / num_parts
                    total_seconds = part_duration_ms / 1000
                    minutes = int(total_seconds // 60)
                    seconds = int(total_seconds % 60)
                    duration_text = f"Duration per part: {minutes:02d}:{seconds:02d}"
                    self.duration_info_label.configure(text=duration_text)
            except Exception:
                self.duration_info_label.configure(text="Duration per part: --:--")

    def validate_inputs(self):
        """Validate user inputs"""
        if not self.input_file:
            messagebox.showerror("Error", "Please select a media file first!")
            return False

        if self.split_var.get():
            try:
                num_parts = int(self.parts_var.get())
                if num_parts <= 0:
                    messagebox.showerror("Error", "Number of parts must be greater than 0!")
                    return False
                    
                # Ask for confirmation with duration info
                if self.media_info and self.media_info.get('duration_ms', 0) > 0:
                    duration_ms = self.media_info['duration_ms']
                    part_duration_ms = duration_ms / num_parts
                    total_seconds = part_duration_ms / 1000
                    minutes = int(total_seconds // 60)
                    seconds = int(total_seconds % 60)
                    
                    confirm_msg = f"Split into {num_parts} parts?\nEach part will be {minutes:02d}:{seconds:02d} long."
                    if not messagebox.askyesno("Confirm Splitting", confirm_msg):
                        return False
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for parts!")
                return False
        return True

    def process_media(self):
        """Process media in background thread"""
        if self.processing:
            return

        if not self.validate_inputs():
            return

        self.processing = True
        self.process_button.configure(state="disabled", text="PROCESSING...")
        self.progress_bar['value'] = 0
        self.status_label.configure(text="Initializing...")
        self.output_label.configure(text="")

        split_media = self.split_var.get()
        num_parts = int(self.parts_var.get()) if split_media else 1

        thread = threading.Thread(target=self._process_media_thread, args=(num_parts, split_media))
        thread.daemon = True
        thread.start()

    def _process_media_thread(self, num_parts, split_media):
        """Processing logic"""
        try:
            self.update_status("Loading media file...", 10)
            processor = MediaProcessor(self.input_file)
            info = processor.get_media_info()
            is_video = info['is_video']

            if is_video:
                if split_media:
                    self.update_status("Converting video to MP3 and splitting...", 30)
                else:
                    self.update_status("Converting video to MP3...", 30)
            else:
                if split_media:
                    self.update_status("Splitting audio file...", 30)
                else:
                    self.update_status("Processing audio file...", 30)

            if split_media:
                self.update_status("Processing and splitting...", 60)
                converted_path, output_files = processor.split_media(num_parts, bitrate=self.quality_var.get())
            else:
                self.update_status("Converting media...", 60)
                converted_path = processor.convert_to_mp3(bitrate=self.quality_var.get())
                output_files = [converted_path]

            self.update_status("Process complete!", 100)
            
            # Success message
            if is_video:
                if split_media:
                    action_text = f"✅ Successfully converted and split into {len(output_files)} parts!"
                else:
                    action_text = "✅ Successfully converted to MP3!"
            else:
                if split_media:
                    action_text = f"✅ Successfully split into {len(output_files)} parts!"
                else:
                    action_text = "✅ Processing completed successfully!"
                    
            self.root.after(0, lambda: self.output_label.configure(text=action_text))

            # Don't cleanup to preserve converted files
            # processor.cleanup()

        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"Error: {str(e)}"))
        finally:
            self.root.after(0, self.processing_complete)

    def update_status(self, message, progress):
        self.root.after(0, lambda: self.status_label.configure(text=message))
        self.root.after(0, lambda: self.progress_bar.configure(value=progress))

    def show_error(self, message):
        messagebox.showerror("Processing Error", message)
        self.output_label.configure(text="❌ Processing failed!")

    def processing_complete(self):
        self.processing = False
        self.process_button.configure(state="normal", text="🔄 PROCESS MEDIA")

    def run(self):
        self.root.mainloop()


class MediaProcessorWithPreservation(MediaProcessor):
    """Extended MediaProcessor that preserves converted files"""
    
    def convert_to_mp3(self, output_file=None, bitrate='320k'):
        """
        Convert video file to MP3 if it's a video file.
        If it's already audio, returns the original path.
        
        Args:
            output_file (str): Custom output path for converted file
            bitrate (str): Audio quality setting
            
        Returns:
            str: Path to MP3 file ready for splitting
        """
        if not self.is_video:
            print("✅ File is already audio, no conversion needed")
            return self.input_file
        
        print("🎥 Video file detected, converting to MP3...")
        
        # If no output file specified, create one in the same directory as input
        if output_file is None:
            base_name = os.path.splitext(self.input_file)[0]
            output_file = f"{base_name}_converted.mp3"
        
        self.converted_mp3_path = self.convert_video_to_mp3(
            self.input_file, 
            output_file, 
            bitrate
        )
        return self.converted_mp3_path
    
    def convert_video_to_mp3(self, input_file, output_file, bitrate='320k'):
        """
        Convert video file to MP3 using FFmpeg
        
        Args:
            input_file (str): Path to input video file
            output_file (str): Path for output MP3 file
            bitrate (str): Audio bitrate
            
        Returns:
            str: Path to converted MP3 file
        """
        import subprocess
        
        try:
            cmd = [
                'ffmpeg',
                '-i', input_file,
                '-codec:a', 'libmp3lame',
                '-b:a', bitrate,
                '-vn',  # No video
                '-y',   # Overwrite output file
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"FFmpeg error: {result.stderr}")
            
            print(f"✅ Successfully converted to: {output_file}")
            return output_file
            
        except Exception as e:
            raise Exception(f"Conversion failed: {str(e)}")
    
    def cleanup(self):
        """
        Override cleanup to NOT delete converted files
        Only perform minimal cleanup if needed
        """
        print("🔄 Cleanup: Preserving all converted files")
        # You can add any non-destructive cleanup here
        # but don't delete the converted MP3 files


if __name__ == "__main__":
    # Replace the original MediaProcessor with our preservation version
    import src.mp3_splitter
    src.mp3_splitter.MediaProcessor = MediaProcessorWithPreservation
    
    app = MediaProcessorGUI()
    app.run()