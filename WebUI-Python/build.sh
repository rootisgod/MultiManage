#!/bin/bash

# Exit on error
set -e

echo "===== Building MultiManage Executable ====="

# Create a virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements-build.txt

# Run PyInstaller
echo "Running PyInstaller..."
pyinstaller --clean multimanage.spec

# Deactivate virtual environment
deactivate

echo "===== Build Complete ====="
echo "The executable is located in the dist/MultiManage directory"
echo "On macOS, you can also find the app bundle at dist/MultiManage.app"
