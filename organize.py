import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# ====== File type categories ======
file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
    "Music": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
}

def organize_folder(folder_path):
    """Organize files in the given folder by their extensions."""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Skip directories
        if os.path.isdir(file_path):
            continue

        # Get file extension
        file_ext = os.path.splitext(filename)[1].lower()
        moved = False

        # Check which category the file belongs to
        for category, extensions in file_types.items():
            if file_ext in extensions:
                move_file(file_path, os.path.join(folder_path, category))
                moved = True
                break

        # If no category matches, move to "Others"
        if not moved:
            move_file(file_path, os.path.join(folder_path, "Others"))

def move_file(src_path, dest_folder):
    """Move file to the destination folder, rename if file already exists."""
    os.makedirs(dest_folder, exist_ok=True)
    dest_path = os.path.join(dest_folder, os.path.basename(src_path))

    base, ext = os.path.splitext(dest_path)
    counter = 1
    while os.path.exists(dest_path):
        dest_path = f"{base} ({counter}){ext}"
        counter += 1

    shutil.move(src_path, dest_path)

def choose_folder():
    """Open a dialog to select the target folder."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_var.set(folder_path)

def start_organizing():
    """Start organizing the selected folder."""
    folder_path = folder_var.get()
    if not folder_path:
        messagebox.showwarning("Warning", "Please select a folder first!")
        return
    if not os.path.isdir(folder_path):
        messagebox.showerror("Error", "The selected folder does not exist!")
        return

    organize_folder(folder_path)
    messagebox.showinfo("Done", f"Organized: {folder_path}")

# ====== GUI Interface ======
root = tk.Tk()
root.title("📂 Automatic Folder Organizer")
root.geometry("500x200")

folder_var = tk.StringVar()

tk.Label(root, text="Select the folder to organize:", font=("Arial", 12)).pack(pady=10)

frame = tk.Frame(root)
frame.pack()

entry = tk.Entry(frame, textvariable=folder_var, width=40, font=("Arial", 10))
entry.pack(side=tk.LEFT, padx=5)

browse_btn = tk.Button(frame, text="Browse", command=choose_folder, font=("Arial", 10))
browse_btn.pack(side=tk.LEFT)

start_btn = tk.Button(root, text="Start Organizing", command=start_organizing, font=("Arial", 12), bg="green", fg="white")
start_btn.pack(pady=20)

root.mainloop()
