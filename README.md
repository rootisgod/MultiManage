# MultiManage
GUI to manage multipass

## CONDA

Use correct environment.

```bash
conda config --add channels conda-forge
conda config --set channel_priority strict
conda install -c conda-forge pysimplegui pyinstaller
```

## Documentation

Using this an example: https://realpython.com/pysimplegui-python/

Some Basic Examples: https://www.pysimplegui.org/en/latest/cookbook/

Full Program Examples: https://github.com/PySimpleGUI/PySimpleGUI/tree/master/DemoPrograms

Reference: https://www.pysimplegui.org/en/stable/

# System Setup Guide

## Windows 2022

Install chocolatey

## Python

### Program Dependencies

Install chocolatey

```powershell
choco install python3 -y
python.exe -m pip install --upgrade pip
pip install pipenv
pip install pysimplegui pyinstaller
```

### Pyinstaller

```powershell
pip install pyinstaller
```

# Build

Run this and then zip the contents

```powershell
pyinstaller multimanage.py
.\dist\main\main.exe
```

## Linux

### Python 

```bash
apt install python3 python3-pip python3-tk
pip install pipenv
pip install pysimplegui pyinstaller
python3 -m PyInstaller multimanage.py
```

### Multipass
```bash
sudo mv /etc/apt/preferences.d/nosnap.pref ~/Documents/nosnap.backup
sudo apt update
sudo apt install snapd
sudo snap install multipass
```

## Project Setup

Just for my reference. How to setup a virtual env and test a build of the installer on windows.

Download and unzip repo

### Linux Mint

```bash
sudo apt install python3.10-venv python3-tk -y
python3 -m venv ./venv-multimanage/
sudo chmod +x ./venv-multimanage/bin/activate
. ./venv-multimanage/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
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
pyinstaller -F -w -n multimanage multimanage.py
```

