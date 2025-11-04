import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from pathlib import Path
from src.utils import save_image_and_text
import os

def choose_file(entry):
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)

def create_action(img_entry, txt_widget):
    img = img_entry.get()
    text = txt_widget.get("1.0", tk.END).strip()
    if not img:
        messagebox.showerror("Error", "Select an image first.")
        return
    out = filedialog.askdirectory(initialdir=os.path.expanduser("~"))
    if not out:
        return
    try:
        image_path, text_path = save_image_and_text(img, text, out)
        messagebox.showinfo("Saved", f"Created:\n{image_path}\n{text_path}")
        img_entry.delete(0, tk.END)
        txt_widget.delete("1.0", tk.END)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_image_on_label(image_path, label, maxsize=(200, 200)):
    try:
        img = Image.open(image_path)
        img.thumbnail(maxsize)
        tkimg = ImageTk.PhotoImage(img)
        label.config(image=tkimg)
        label.image = tkimg
    except Exception:
        label.config(image=None)
        label.image = None

def is_valid_polyglot(path):
    p = Path(path)
    stem = p.stem.replace(".jpg", "")
    if p.suffix.lower() in [".jpg", ".jpeg"]:
        txt = p.with_name(f"{stem}.jpg.txt")
        return txt.exists(), txt
    elif p.suffix.lower() == ".txt":
        img = p.with_name(f"{stem}.jpg")
        return img.exists(), img
    else:
        return False, None

def check_polyglot_action():
    path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
    if not path:
        return
    valid, pair = is_valid_polyglot(path)
    if valid:
        win = tk.Toplevel()
        win.title("Polyglot File Viewer")
        frame = tk.Frame(win)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        img_label = tk.Label(frame)
        img_label.pack(side=tk.LEFT, padx=10)
        txt_widget = tk.Text(frame, width=60, height=20)
        txt_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        img_file = path if path.lower().endswith((".jpg", ".jpeg")) else str(pair)
        txt_file = path if path.lower().endswith(".txt") else str(pair)
        show_image_on_label(img_file, img_label)
        try:
            with open(txt_file, "r", encoding="utf-8") as f:
                txt_widget.insert("1.0", f.read())
        except Exception:
            txt_widget.insert("1.0", "(Error reading text)")
        txt_widget.config(state=tk.DISABLED)
    else:
        messagebox.showerror("Not a Polyglot", "Matching .jpg or .jpg.txt not found.")

def build_gui():
    root = tk.Tk()
    root.title("Polyglot File")
    nb = tk.Frame(root)
    nb.pack(fill=tk.BOTH, expand=True)

    left = tk.Frame(nb)
    left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=8)
    tk.Label(left, text="Create Polyglot File").pack(anchor="w")
    tk.Label(left, text="Image:").pack(anchor="w")
    img_entry = tk.Entry(left, width=60)
    img_entry.pack(anchor="w")
    tk.Button(left, text="Browse", command=lambda: choose_file(img_entry)).pack(anchor="w")
    tk.Label(left, text="Text:").pack(anchor="w")
    txt_widget = tk.Text(left, width=60, height=8)
    txt_widget.pack(anchor="w")
    tk.Button(left, text="Save", command=lambda: create_action(img_entry, txt_widget)).pack(anchor="w", pady=6)

    right = tk.Frame(nb)
    right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=8)
    tk.Label(right, text="Check Polyglot File").pack(anchor="w")
    tk.Button(right, text="Browse & Check", command=check_polyglot_action).pack(anchor="w", pady=8)

    root.mainloop()

if __name__ == "__main__":
    build_gui()