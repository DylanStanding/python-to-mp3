import os
import subprocess
from tkinter import Tk, Button, Label, filedialog

# Check and install dependencies if needed
try:
    import pydub
    from pydub import AudioSegment
    import moviepy
    from moviepy.video.io.VideoFileClip import VideoFileClip
except ImportError:
    print("Installing required dependencies...")
    subprocess.run(["pip", "install", "pydub", "moviepy"])

    # Check again after installing dependencies
    try:
        import pydub
        from pydub import AudioSegment
        import moviepy
        from moviepy.video.io.VideoFileClip import VideoFileClip
    except ImportError:
        raise ImportError("Unable to install required dependencies. Please install them manually.")

class FileConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MesaTech™")

        # Set the window size and position it in the center of the screen
        window_width = 250
        window_height = 100
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Set background color to black
        self.root.configure(bg="black")

        self.file_path_label = Label(root, text="Selected File: ", fg="white", bg="black")
        self.file_path_label.pack()

        # Set button colors to grey
        button_color = "#808080"  # Hex color for grey
        self.select_file_button = Button(root, text="Select File", command=self.select_file, bg=button_color, fg="white")
        self.select_file_button.pack()

        self.convert_button = Button(root, text="Convert to MP3", command=self.convert_to_mp3, bg=button_color, fg="white")
        self.convert_button.pack()

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio/Video Files", "*.mp3;*.mp4;*.wav;*.ogg")])
        if file_path:
            self.file_path_label.config(text=f"Selected File: {file_path}")
            self.input_file_path = file_path

    def convert_to_mp3(self):
        if hasattr(self, 'input_file_path'):
            if self.input_file_path.lower().endswith('.mp4'):
                video_clip = VideoFileClip(self.input_file_path)
                audio_clip = video_clip.audio

                # Ask user for the save location
                output_file_path = filedialog.asksaveasfilename(defaultextension=".mp3",
                                                                  filetypes=[("MP3 files", "*.mp3")])

                # Check if the user selected a location
                if output_file_path:
                    audio_clip.write_audiofile(output_file_path)
                    audio_clip.close()
                    video_clip.close()
                    self.file_path_label.config(text=f"Conversion complete. Output file: {output_file_path}")
                else:
                    self.file_path_label.config(text="Conversion canceled.")
            else:
                input_file = AudioSegment.from_file(self.input_file_path)

                # Ask user for the save location
                output_file_path = filedialog.asksaveasfilename(defaultextension=".mp3",
                                                                  filetypes=[("MP3 files", "*.mp3")])

                # Check if the user selected a location
                if output_file_path:
                    input_file.export(output_file_path, format="mp3")
                    self.file_path_label.config(text=f"Conversion complete. Output file: {output_file_path}")
                else:
                    self.file_path_label.config(text="Conversion canceled.")
        else:
            self.file_path_label.config(text="Please select a file first.")

if __name__ == "__main__":
    root = Tk()
    app = FileConverterApp(root)
    root.mainloop()
