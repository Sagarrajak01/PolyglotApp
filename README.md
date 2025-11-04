Polyglot File - cross-platform desktop app to create and search polyglot files

Install
pip install -r requirements.txt

Run GUI
python -m src.gui

Build Windows .exe (Windows machine)
pip install pyinstaller
pyinstaller --noconsole --onefile --name PolyglotFile src/gui.py

Build Linux binary (Linux machine)
pip install pyinstaller
pyinstaller --onefile --name PolyglotFile src/gui.py