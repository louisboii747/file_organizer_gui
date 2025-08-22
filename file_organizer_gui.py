import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv"],
    "Music": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    # Add more categories/extensions as you like
}

class FileOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📁 File Organizer")
        self.root.geometry("450x250")
        self.root.resizable(False, False)

        self.selected_folder = tk.StringVar()

        self.setup_widgets()

    def setup_widgets(self):
        padding = {"padx": 10, "pady": 10}

        ttk.Label(self.root, text="Select a folder to organize:", font=("Arial", 12)).pack(**padding)

        folder_frame = ttk.Frame(self.root)
        folder_frame.pack(fill=tk.X, **padding)

        folder_entry = ttk.Entry(folder_frame, textvariable=self.selected_folder, width=40)
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        browse_button = ttk.Button(folder_frame, text="Browse", command=self.browse_folder)
        browse_button.pack(side=tk.LEFT, padx=5)

        organize_button = ttk.Button(self.root, text="Organize Files", command=self.organize_files)
        organize_button.pack(pady=15)

        self.status_label = ttk.Label(self.root, text="", foreground="green")
        self.status_label.pack()

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_folder.set(folder)
            self.status_label.config(text="")

    def organize_files(self):
        folder = self.selected_folder.get()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid folder.")
            return

        moved_files_count = 0

        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)

            if os.path.isfile(filepath):
                moved = False
                ext = os.path.splitext(filename)[1].lower()

                for category, extensions in FILE_TYPES.items():
                    if ext in extensions:
                        dest_dir = os.path.join(folder, category)
                        os.makedirs(dest_dir, exist_ok=True)
                        try:
                            shutil.move(filepath, os.path.join(dest_dir, filename))
                            moved = True
                            moved_files_count += 1
                        except Exception as e:
                            messagebox.showerror("Error", f"Failed to move {filename}: {e}")
                        break

                # Files with unknown extensions are left untouched

        self.status_label.config(text=f"Organizing complete! Moved {moved_files_count} files.")
        messagebox.showinfo("Done", f"Organizing complete! Moved {moved_files_count} files.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerGUI(root)
    root.mainloop()
