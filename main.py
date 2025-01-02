import requests
import re
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def download_bitview_video(url, save_path):
    try:
        # Extract the video ID from the provided URL
        video_id_match = re.search(r'v=([\w\d]+)', url)
        if not video_id_match:
            messagebox.showerror("Error", "Invalid URL. Could not find video ID.")
            return

        video_id = video_id_match.group(1)
        video_url = f"https://www.bitview.net/m/video.php?v={video_id}"

        print(f"Fetching video from: {video_url}")

        # Send a GET request to the video URL
        response = requests.get(video_url, stream=True)

        if response.status_code == 200:
            # Determine the filename for the video
            file_name = os.path.join(save_path, f"{video_id}.mp4")

            # Save the video locally
            with open(file_name, "wb") as video_file:
                for chunk in response.iter_content(chunk_size=1024):
                    video_file.write(chunk)

            messagebox.showinfo("Success", f"Video downloaded successfully: {file_name}")
        else:
            messagebox.showerror("Error", f"Failed to fetch video. HTTP status code: {response.status_code}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def start_download():
    url = url_entry.get()
    if not url.strip():
        messagebox.showwarning("Warning", "Please enter a video URL.")
        return

    save_path = filedialog.askdirectory(title="Select Directory to Save Video")
    if not save_path:
        messagebox.showwarning("Warning", "Please select a folder to save the video.")
        return

    download_bitview_video(url, save_path)

# Create the UI
root = tk.Tk()
root.title("BitView Video Downloader")
root.resizable(False, False)  # Make the window non-resizable

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

url_label = tk.Label(frame, text="Enter BitView Video URL:")
url_label.grid(row=0, column=0, pady=5, sticky="w")

url_entry = tk.Entry(frame, width=40)
url_entry.grid(row=1, column=0, pady=5, padx=5)

download_button = tk.Button(frame, text="Download Video", command=start_download)
download_button.grid(row=2, column=0, pady=10)

root.mainloop()
