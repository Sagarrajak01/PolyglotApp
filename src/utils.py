from pathlib import Path
from PIL import Image
import json
import tempfile
import shutil
import subprocess
import platform
import os
from .config import APP_DIR, INDEX_FILE, logger


def open_in_viewers(image_path: str, text_path: str):
    try:
        system = platform.system()
        if system == "Windows":
            os.startfile(image_path)
            os.startfile(text_path)
        elif system == "Darwin":
            subprocess.Popen(["open", image_path])
            subprocess.Popen(["open", text_path])
        else:
            subprocess.Popen(["xdg-open", image_path])
            subprocess.Popen(["xdg-open", text_path])
    except Exception as e:
        logger.warning("Unable to auto-open viewers: %s", e)


def open_polyglot_pair(path: str):
    p = Path(path)
    valid, pair = is_pair(p)
    if not valid or not pair:
        raise FileNotFoundError(f"Matching pair not found for {path}")
    if p.suffix.lower() == ".txt" or p.name.endswith(".jpg.txt"):
        img = str(pair)
        txt = str(p)
    else:
        img = str(p)
        txt = str(pair)
    open_in_viewers(img, txt)


def ensure_storage():
    APP_DIR.mkdir(parents=True, exist_ok=True)
    if not INDEX_FILE.exists():
        with INDEX_FILE.open("w", encoding="utf-8") as f:
            json.dump([], f)
        logger.info("Created new index file at %s", INDEX_FILE)


def _atomic_write(path: Path, data: str, encoding="utf-8"):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name, dir=str(path.parent))
    try:
        with open(fd, "w", encoding=encoding) as f:
            f.write(data)
        shutil.move(tmp, str(path))
    except Exception:
        Path(tmp).unlink(missing_ok=True)
        raise


def save_image_and_text(image_path: str, text: str, out_dir: str | None = None, custom_name: str | None = None):
    """Save image and text pair with optional custom filename."""
    ensure_storage()
    p = Path(image_path)
    if not p.exists():
        raise FileNotFoundError(f"Source image not found: {p}")

    out = Path(out_dir) if out_dir else APP_DIR
    out.mkdir(parents=True, exist_ok=True)

    # Use custom name if given
    base = custom_name if custom_name else p.stem
    target_image = out.joinpath(f"{base}.jpg")
    text_file = out.joinpath(f"{base}.jpg.txt")

    img = Image.open(p)
    if img.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        if "A" in img.getbands():
            bg.paste(img, mask=img.split()[-1])
        else:
            bg.paste(img)
        bg.save(target_image, format="JPEG", quality=95)
    else:
        img.convert("RGB").save(target_image, format="JPEG", quality=95)

    _atomic_write(text_file, text or "")
    record = {"id": base, "image": str(target_image), "text": str(text_file)}
    add_index(record)
    logger.info("Saved polyglot pair: %s", base)
    return str(target_image), str(text_file)


def add_index(record: dict):
    ensure_storage()
    try:
        with INDEX_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = []
    data = [r for r in data if r.get("id") != record.get("id")]
    data.append(record)
    _atomic_write(INDEX_FILE, json.dumps(data, ensure_ascii=False, indent=2))
    logger.debug("Index updated with id=%s", record.get("id"))


def search_index(query: str):
    ensure_storage()
    q = (query or "").lower().strip()
    if not q:
        return []
    results = []
    try:
        with INDEX_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return results
    for r in data:
        try:
            text_path = Path(r.get("text", ""))
            content = (
                text_path.read_text(encoding="utf-8").lower()
                if text_path.exists()
                else ""
            )
        except Exception:
            content = ""
        if q in r.get("id", "").lower() or q in content:
            results.append(r)
    return results


def is_pair(path: str) -> tuple[bool, Path | None]:
    p = Path(path)
    name = p.name
    if name.endswith(".jpg.txt"):
        img = p.with_name(name.replace(".jpg.txt", ".jpg"))
        if not img.exists():
            img = p.with_name(name.replace(".jpg.txt", ".jpeg"))
        return img.exists(), img if img.exists() else None
    elif p.suffix.lower() in (".jpg", ".jpeg", ".png"):
        txt = p.with_name(p.stem + ".jpg.txt")
        return txt.exists(), txt
    else:
        return False, None


def delete_polyglot_pair(path: str):
    p = Path(path)
    valid, pair = is_pair(p)
    deleted = []
    if valid and pair:
        for f in (p, pair):
            if f.exists():
                f.unlink(missing_ok=True)
                deleted.append(f.name)
        logger.info("Deleted polyglot pair: %s", deleted)
        _remove_from_index(p.stem)
    return deleted


def _remove_from_index(file_id: str):
    ensure_storage()
    try:
        with INDEX_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = []
    new_data = [r for r in data if r.get("id") != file_id]
    _atomic_write(INDEX_FILE, json.dumps(new_data, ensure_ascii=False, indent=2))
    logger.debug("Removed id=%s from index", file_id)


def list_all_polyglots():
    ensure_storage()
    try:
        with INDEX_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = []
    valid = []
    for r in data:
        img = Path(r.get("image", ""))
        txt = Path(r.get("text", ""))
        if img.exists() and txt.exists():
            valid.append(r)
    return valid


def rebuild_index():
    ensure_storage()
    all_files = list(APP_DIR.glob("*.jpg"))
    data = []
    for img in all_files:
        txt = img.with_name(img.stem + ".jpg.txt")
        if txt.exists():
            data.append({"id": img.stem, "image": str(img), "text": str(txt)})
    _atomic_write(INDEX_FILE, json.dumps(data, ensure_ascii=False, indent=2))
    logger.info("Rebuilt index with %d entries", len(data))
    return data