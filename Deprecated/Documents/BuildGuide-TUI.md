# MultiManage
TUI to manage multipass

## Documentation

# System Setup Guide

## Multipass

### Linux Mint
```bash
sudo mv /etc/apt/preferences.d/nosnap.pref ~/Documents/nosnap.backup
sudo apt update
sudo apt install snapd
sudo snap install multipass
```

## Python Setup

Just for my reference. How to setup a virtual env and test a build of the installer on windows.

Download and unzip repo

### Ubuntu 22.04/Mac

```bash
sudo apt install python3 python3-pip python3-venv python3-tk -y
python3 -m venv ./venv/
sudo chmod +x ./venv/bin/activate
. ./venv/bin/activate
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
# To see textual working
python -m textual

python3 multimanage-tui.py
pip install pyinstaller
pyinstaller -F -w -n multimanage-tui multimanage-tui.py
```

### Windows

```powershell
python -m venv .\venv\
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller
pyinstaller -F -w -n multimanage-tui --onefile --windowed --icon=MultiManage-Logo.ico multimanage-tui.py
.'C:\Program Files (x86)\Inno Setup 6\ISCC.exe' /dMyAppVersion=1.00) multimanage.iss
```

