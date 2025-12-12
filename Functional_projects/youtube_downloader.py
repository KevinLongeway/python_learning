from pytube import YouTube
import tkinter as tk
from tkinter import filedialog, messagebox


def download_video(url, save_path):
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(
            progressive=True, file_extension='mp4').order_by('resolution').desc()
        highest_quality_stream = streams.get_highest_resolution()
        highest_quality_stream.download(output_path=save_path)
        # Alternatively, to download a specific resolution, uncomment the following line:
        # specific_stream = streams.filter(res="720p").first()
        print(f"Video downloaded successfully to {save_path}")
    except Exception as e:
        print(e)


def open_file_dialog():
    folder = filedialog.askdirectory()
    if folder:
        print(f"Selected folder: {folder}")
    return folder


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    video_url = input("Enter the YouTube video URL: ")
    save_directory = open_file_dialog()

    if save_directory:
        print("Downloading video...")
        download_video(video_url, save_directory)
        messagebox.showinfo("Success", "Video downloaded successfully!")
    else:
        messagebox.showwarning(
            "Cancelled", "No folder selected. Download cancelled.")
