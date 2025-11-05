from pathlib import Path
import logging

APP_DIR = Path.home().joinpath("polyglot_files")
INDEX_FILE = APP_DIR.joinpath("index.json")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("polyglot")
