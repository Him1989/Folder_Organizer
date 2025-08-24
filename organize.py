import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# ====== 檔案類型分類 ======
file_types = {
    "圖片": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "文件": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
    "影片": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
    "音樂": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "壓縮檔": [".zip", ".rar", ".7z", ".tar", ".gz"],
}

def organize_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isdir(file_path):
            continue

        file_ext = os.path.splitext(filename)[1].lower()
        moved = False
        for category, extensions in file_types.items():
            if file_ext in extensions:
                move_file(file_path, os.path.join(folder_path, category))
                moved = True
                break

        if not moved:
            move_file(file_path, os.path.join(folder_path, "其他"))

def move_file(src_path, dest_folder):
    os.makedirs(dest_folder, exist_ok=True)
    dest_path = os.path.join(dest_folder, os.path.basename(src_path))

    base, ext = os.path.splitext(dest_path)
    counter = 1
    while os.path.exists(dest_path):
        dest_path = f"{base} ({counter}){ext}"
        counter += 1

    shutil.move(src_path, dest_path)

def choose_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_var.set(folder_path)

def start_organizing():
    folder_path = folder_var.get()
    if not folder_path:
        messagebox.showwarning("警告", "請先選擇資料夾！")
        return
    if not os.path.isdir(folder_path):
        messagebox.showerror("錯誤", "資料夾不存在！")
        return

    organize_folder(folder_path)
    messagebox.showinfo("完成", f"已整理: {folder_path}")

# ====== GUI 介面 ======
root = tk.Tk()
root.title("📂 自動整理資料夾")
root.geometry("500x200")

folder_var = tk.StringVar()

tk.Label(root, text="選擇要整理的資料夾:", font=("Microsoft JhengHei", 12)).pack(pady=10)

frame = tk.Frame(root)
frame.pack()

entry = tk.Entry(frame, textvariable=folder_var, width=40, font=("Microsoft JhengHei", 10))
entry.pack(side=tk.LEFT, padx=5)

browse_btn = tk.Button(frame, text="瀏覽", command=choose_folder, font=("Microsoft JhengHei", 10))
browse_btn.pack(side=tk.LEFT)

start_btn = tk.Button(root, text="開始整理", command=start_organizing, font=("Microsoft JhengHei", 12), bg="green", fg="white")
start_btn.pack(pady=20)

root.mainloop()
