import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from PIL import Image, ImageTk
from pathlib import Path
from .utils import save_image_and_text, search_index, is_pair
import os

BG_COLOR = "#e6f0ff"
HEADER_COLOR = "#1c4e80"
BTN_COLOR = "#2979ff"
BTN_TEXT_COLOR = "#ffffff"
ENTRY_BG = "#ffffff"
THUMB_SIZE = (240, 240)


def choose_file(entry: tk.Entry):
    path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png *.jpg *.jpeg;*.bmp;*.gif")]
    )
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)


def create_action(img_entry, txt_widget):
    img = img_entry.get()
    text = txt_widget.get("1.0", "end").strip()
    if not img:
        messagebox.showerror("Error", "Select an image first.")
        return

    filename = simpledialog.askstring("Save As", "Enter filename (without extension):")
    if not filename:
        return

    out_dir = filedialog.askdirectory(initialdir=os.path.expanduser("~"))
    if not out_dir:
        return

    try:
        image_path, text_path = save_image_and_text(img, text, out_dir, filename)
        messagebox.showinfo("Saved", f"File saved as:\n{filename}.jpg\nin:\n{out_dir}")
        img_entry.delete(0, tk.END)
        txt_widget.delete("1.0", tk.END)
    except Exception as e:
        messagebox.showerror("Error", str(e))


def show_image_on_label(image_path: str, label: tk.Label, maxsize=THUMB_SIZE):
    try:
        img = Image.open(image_path)
        img.thumbnail(maxsize)
        tkimg = ImageTk.PhotoImage(img)
        label.config(image=tkimg)
        label.image = tkimg
    except Exception:
        label.config(image=None)
        label.image = None


def check_polyglot_action(parent: tk.Tk):
    path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
    if not path:
        return
    valid, pair = is_pair(path)
    if not valid:
        messagebox.showerror("Not a polyglot", "Matching .jpg or .jpg.txt not found.")
        return
    img_file = (
        path if Path(path).suffix.lower() in (".jpg", ".jpeg", ".png") else str(pair)
    )
    txt_file = path if Path(path).suffix.lower() == ".txt" else str(pair)
    win = tk.Toplevel(parent)
    win.title("Polyglot Viewer")
    win.configure(bg=BG_COLOR)
    frame = tk.Frame(win, padx=8, pady=8, bg=BG_COLOR)
    frame.pack(fill=tk.BOTH, expand=True)
    img_label = tk.Label(frame, bg=BG_COLOR)
    img_label.pack(side=tk.LEFT, padx=10)
    show_image_on_label(img_file, img_label)
    txt_widget = tk.Text(frame, wrap=tk.WORD, width=60, height=20, bg=ENTRY_BG)
    txt_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
    try:
        with open(txt_file, "r", encoding="utf-8") as f:
            txt_widget.insert("1.0", f.read())
    except Exception:
        txt_widget.insert("1.0", "(Error reading text)")
    txt_widget.config(state=tk.DISABLED)


def search_and_view(parent: tk.Tk):
    q = simpledialog.askstring(
        "Search Polyglot Files", "Enter keyword or ID:", parent=parent
    )
    if not q:
        return
    results = search_index(q)
    if not results:
        messagebox.showinfo("No results", "No polyglot files matched your query.")
        return
    win = tk.Toplevel(parent)
    win.title(f"Search results for '{q}'")
    win.configure(bg=BG_COLOR)
    win.geometry("950x550")
    frame = tk.Frame(win, bg=BG_COLOR)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    left_frame = tk.Frame(frame, bg=BG_COLOR)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=8)
    right_frame = tk.Frame(frame, bg=BG_COLOR)
    right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=8)
    listbox = tk.Listbox(left_frame, width=40, height=25, font=("Segoe UI", 11))
    scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=listbox.yview)
    listbox.config(yscrollcommand=scrollbar.set)
    listbox.pack(side=tk.LEFT, fill=tk.Y)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    for r in results:
        display = f"{r.get('id')} - {Path(r.get('image')).name}"
        listbox.insert(tk.END, display)
    img_label = tk.Label(right_frame, bg=BG_COLOR)
    img_label.pack(pady=5)
    txt_widget = tk.Text(right_frame, wrap=tk.WORD, width=70, height=22, bg=ENTRY_BG)
    txt_widget.pack(fill=tk.BOTH, expand=True)

    def on_select(event=None):
        sel = listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        rec = results[idx]
        img_file = rec.get("image")
        txt_file = rec.get("text")
        if img_file:
            show_image_on_label(img_file, img_label)
        txt_widget.config(state=tk.NORMAL)
        txt_widget.delete("1.0", tk.END)
        try:
            with open(txt_file, "r", encoding="utf-8") as f:
                txt_widget.insert("1.0", f.read())
        except Exception:
            txt_widget.insert("1.0", "(Error reading text)")
        txt_widget.config(state=tk.DISABLED)

    listbox.bind("<<ListboxSelect>>", on_select)
    listbox.selection_set(0)
    on_select()


def build_gui():
    root = tk.Tk()
    root.title("By 205124083 & 205124011")
    root.geometry("1000x550")
    root.configure(bg=BG_COLOR)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "TButton",
        font=("Segoe UI", 11, "bold"),
        padding=8,
        relief="flat",
        background=BTN_COLOR,
        foreground=BTN_TEXT_COLOR,
        borderwidth=0,
        focuscolor=BG_COLOR,
    )
    style.map(
        "TButton",
        background=[("active", "#2A4C84")],
        foreground=[("active", "#FFFFFF")],
    )

    style.configure(
        "TButton",
        font=("Segoe UI", 11),
        padding=6,
        background=BTN_COLOR,
        foreground=BTN_TEXT_COLOR,
    )
    style.map("TButton", background=[("active", "#155b9c")])
    header = tk.Label(
        root,
        text="Polyglot App",
        bg=HEADER_COLOR,
        fg="white",
        font=("Segoe UI", 16, "bold"),
        pady=10,
    )
    header.pack(fill=tk.X)
    container = tk.Frame(root, bg=BG_COLOR, padx=10, pady=10)
    container.pack(fill=tk.BOTH, expand=True)
    left = tk.Frame(container, bg=BG_COLOR, relief=tk.RIDGE, borderwidth=2)
    left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=8)
    tk.Label(
        left, text="Create Polyglot File ", font=("Segoe UI", 14, "bold"), bg=BG_COLOR
    ).pack(anchor="w")
    tk.Label(left, text="Image:", bg=BG_COLOR).pack(anchor="w", pady=(6, 0))
    img_entry = tk.Entry(left, width=70, bg=ENTRY_BG)
    img_entry.pack(anchor="w")
    ttk.Button(left, text="Browse...", command=lambda: choose_file(img_entry)).pack(
        anchor="w", pady=6
    )
    tk.Label(left, text="Text:", bg=BG_COLOR).pack(anchor="w")
    txt_widget = tk.Text(left, width=70, height=10, bg=ENTRY_BG)
    txt_widget.pack(anchor="w", pady=4)
    ttk.Button(
        left,
        text="Save Polyglot File",
        command=lambda: create_action(img_entry, txt_widget),
    ).pack(anchor="w", pady=10)
    right = tk.Frame(container, bg=BG_COLOR, relief=tk.RIDGE, borderwidth=2)
    right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=8)
    tk.Label(right, text="More", font=("Segoe UI", 14, "bold"), bg=BG_COLOR).pack(
        anchor="w", pady=(0, 10)
    )
    ttk.Button(
        right,
        text="Check Existing Polyglot File",
        command=lambda: check_polyglot_action(root),
    ).pack(fill=tk.X, pady=6)
    ttk.Button(
        right, text="Search Polyglot Files", command=lambda: search_and_view(root)
    ).pack(fill=tk.X, pady=6)
    ttk.Button(right, text="Exit", command=root.destroy).pack(fill=tk.X, pady=6)
    root.mainloop()
