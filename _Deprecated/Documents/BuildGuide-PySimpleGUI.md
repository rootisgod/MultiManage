# MultiManage
GUI to manage multipass

## Documentation

Using this an example: https://realpython.com/pysimplegui-python/

Some Basic Examples: https://www.pysimplegui.org/en/latest/cookbook/

Full Program Examples: https://github.com/PySimpleGUI/PySimpleGUI/tree/master/DemoPrograms

Reference: https://www.pysimplegui.org/en/stable/

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

### Ubuntu 22.04

```bash
sudo apt install python3 python3-pip python3-venv python3-tk -y
python3 -m venv ./venv-multimanage/
sudo chmod +x ./venv-multimanage/bin/activate
. ./venv-multimanage/bin/activate
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
python3 multimanage.py
pip install pyinstaller
pyinstaller -F -w -n multimanage multimanage.py
```

### Mac

# https://www.pythonguis.com/installation/install-tkinter-mac/

```bash
pip install python3-tk -y
python3 -m venv ./venv/
sudo chmod +x ./venv/bin/activate
. ./venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade pip setuptools wheel
pip3 install setuptools wheek --only-binary :all:
pip3 install -r requirements-binary.txt  --only-binary :all:
pip3 install -r requirements-build.txt
python3 -m pip install --force-reinstall --extra-index-url https://PySimpleGUI.net/install PySimpleGUI
python --version
brew install python-tk@3.11
python3 multimanage.py
pip install pyinstaller
pyinstaller -F -w -n multimanage multimanage.py
```

### Windows

```powershell
python -m venv .\venv-multimanage\
.\venv-multimanage\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller
pyinstaller -F -w -n multimanage --onefile --windowed --icon=MultiManage-Logo.ico multimanage.py
.'C:\Program Files (x86)\Inno Setup 6\ISCC.exe' /dMyAppVersion=1.00) multimanage.iss
```

