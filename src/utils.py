from pathlib import Path
from PIL import Image
import json
import os

APP_DIR = Path.home().joinpath("polyglot_files")
INDEX_FILE = APP_DIR.joinpath("index.json")

def ensure_storage():
    APP_DIR.mkdir(parents=True, exist_ok=True)
    if not INDEX_FILE.exists():
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

def save_image_and_text(image_path, text, out_dir=None):
    ensure_storage()
    p = Path(image_path)
    out = Path(out_dir) if out_dir else APP_DIR
    out.mkdir(parents=True, exist_ok=True)
    img = Image.open(p)
    base = p.stem
    target_image = out.joinpath(f"{base}.jpg")
    if img.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "RGBA":
            bg.paste(img, mask=img.split()[3])
        else:
            bg.paste(img)
        bg.save(target_image, format="JPEG", quality=95)
    else:
        img.convert("RGB").save(target_image, format="JPEG", quality=95)
    text_file = out.joinpath(f"{base}.jpg.txt")
    with open(text_file, "w", encoding="utf-8") as f:
        f.write(text)
    record = {
        "id": base,
        "image": str(target_image),
        "text": str(text_file)
    }
    add_index(record)
    return str(target_image), str(text_file)

def add_index(record):
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    existing = [r for r in data if r.get("id") == record.get("id")]
    if existing:
        data = [r for r in data if r.get("id") != record.get("id")]
    data.append(record)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def search_index(query):
    ensure_storage()
    results = []
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    q = query.lower().strip()
    for r in data:
        try:
            with open(r.get("text"), "r", encoding="utf-8") as tf:
                content = tf.read().lower()
        except Exception:
            content = ""
        if q in content or q in r.get("id", "").lower():
            results.append(r)
    return results