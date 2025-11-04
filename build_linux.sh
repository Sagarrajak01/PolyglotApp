#!/bin/bash
echo "Building Polyglot Linux executable..."

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

cd src
pyinstaller --noconsole --onefile --name "PolyglotApp" gui.py
cd ..

echo "Build complete."
echo "Executable path: src/dist/PolyglotApp"
