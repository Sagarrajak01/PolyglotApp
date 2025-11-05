# 🧩 Polyglot File Manager

A simple, cross-platform desktop application built with **Python** and **Tkinter** to create, view, and search **Polyglot files** — paired `.jpg` and `.txt` files that are linked together for image–text management.

---

## 📘 Features

* 🖼️ **Create Polyglot Files:** Combine an image with custom text and save both together.
* ✏️ **Custom Filename:** Choose your own filename before saving.
* 🔍 **Search Functionality:** Instantly find any saved polyglot by keyword or ID.
* 👁️ **View Mode:** Check existing polyglots side-by-side (image + text).
* 🗑️ **Clean Storage:** Automatically maintains a JSON index of all saved files.
* 💾 **Standalone Windows App:** Build into a single `.exe` for easy sharing — no Python required.

---

## 🧠 How It Works

Each **Polyglot File** is stored as:

```
filename.jpg
filename.jpg.txt
```

Both files share the same base name.
The application tracks them automatically inside an internal JSON index for quick lookup.

---

## 🏗️ Project Structure

```
Polyglot-v3/
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── gui.py
│   └── utils.py
│
├── main.py
├── README.md
└── requirements.txt
```

---

## ⚙️ Requirements

* **Python 3.10+**
* Dependencies (auto-installed from `requirements.txt`):

  ```bash
  pip install -r requirements.txt
  ```

  Currently includes:

  * `pillow` (for image handling)
  * `tkinter` (standard in Python)

---

## ▶️ Run Locally (Development Mode)

```bash
python main.py
```

---

## 💾 Build Windows Executable

To package as a portable `.exe`:

1. Install **PyInstaller**:

   ```bash
   pip install pyinstaller
   ```
2. Build:

   ```bash
   pyinstaller --noconsole --onefile --name PolyglotFile main.py
   ```
3. Find your app in:

   ```
   dist/PolyglotFile.exe
   ```

This `.exe` can run on any **Windows 64-bit** system — **no Python required**.

---

## 🧩 App Usage

### 1. Create a Polyglot File

* Click **Browse...** to choose an image.
* Type your custom text.
* Click **Save Polyglot File**.
* Enter your desired **filename** when prompted.
* Choose a folder — both `.jpg` and `.txt` files will be created there.

### 2. Check Existing File

* Click **Check Existing Polyglot File**.
* Select either the `.jpg` or `.txt` — the app displays both together.

### 3. Search Saved Files

* Click **Search Polyglot Files**.
* Enter a keyword or ID — results show image + text preview.

---

## 🗃️ Data Storage

* All saved polyglots are indexed in:

  ```
  %USERPROFILE%\polyglot_files\index.json
  ```
* The app automatically rebuilds or updates this index as needed.

---

## 🪜 Maintenance Commands

If the index ever gets corrupted or files are moved:

```python
from src.utils import rebuild_index
rebuild_index()
```

This will rebuild your index from the `polyglot_files` directory.

---

## ⚠️ Notes

* The `.exe` must remain in the same directory as your app data if you plan to use persistent indexing.
* Avoid renaming `.jpg` or `.txt` files manually; use the app to keep them synced.
---

## 🧪 License

This project is released under the **MIT License** — free for personal and educational use.
