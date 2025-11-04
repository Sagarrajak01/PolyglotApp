@echo off
echo Building Windows EXE...
pyinstaller --noconsole --onefile --name "PolyglotApp" main.py
pause