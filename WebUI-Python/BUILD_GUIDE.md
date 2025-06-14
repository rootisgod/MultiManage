# MultiManage Executable Build Guide

This guide explains how to build an executable version of MultiManage using PyInstaller.

## Prerequisites

- Python 3.9 or later
- Pip package manager
- Git (to clone the repository)

## Building the Executable

### On macOS/Linux

1. Open a terminal and navigate to the WebUI-Python directory:
   ```bash
   cd /path/to/MultiManage/WebUI-Python
   ```

2. Run the build script:
   ```bash
   ./build.sh
   ```

3. The executable will be created in the `dist/MultiManage` directory, and a macOS app bundle will be created in `dist/MultiManage.app`.

### On Windows

1. Open a command prompt and navigate to the WebUI-Python directory:
   ```cmd
   cd \path\to\MultiManage\WebUI-Python
   ```

2. Run the build script:
   ```cmd
   build.bat
   ```

3. The executable will be created in the `dist\MultiManage` directory.

## Running the Application

### On macOS/Linux

You can run the application in several ways:

1. Double-click the macOS app bundle:
   - Open Finder and navigate to `dist/MultiManage.app`
   - Double-click the app to run it

2. Run the executable directly:
   ```bash
   cd dist/MultiManage
   ./MultiManage
   ```

### On Windows

1. Double-click the executable:
   - Open File Explorer and navigate to `dist\MultiManage`
   - Double-click `MultiManage.exe` to run it

## What's Included

The executable package includes:

- Flask web interface
- FastAPI backend
- All required dependencies

## Troubleshooting

If you encounter any issues:

1. Make sure you have the correct Python version installed (3.9+)
2. Check that all dependencies are installed (`pip install -r requirements-build.txt`)
3. If the application fails to start, try running it from the command line to see error messages
4. On macOS, you might need to allow the app in System Preferences > Security & Privacy if it's blocked

## Creating an Installer (Optional)

### On Windows

You can use tools like Inno Setup to create a Windows installer:

1. Install Inno Setup from https://jrsoftware.org/isinfo.php
2. Create a new script using the Inno Setup Script Wizard
3. Add the contents of the `dist\MultiManage` directory to the installer
4. Configure the installer to create shortcuts and set up file associations as needed

### On macOS

You can create a DMG file for easy distribution:

1. Create a new folder called `MultiManage`
2. Copy the `MultiManage.app` into this folder
3. Create a symbolic link to the Applications folder:
   ```bash
   ln -s /Applications Applications
   ```
4. Open Disk Utility and create a new image from the folder
5. Distribute the resulting DMG file
