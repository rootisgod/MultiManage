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
pyinstaller main.py
.\dist\main\main.exe
```

## Linux

### Python 

```bash
apt install python3 python3-pip python3-tk
pip install pipenv
pip install pysimplegui pyinstaller
python3 -m PyInstaller main.py
```

### Multipass
```bash
sudo mv /etc/apt/preferences.d/nosnap.pref ~/Documents/nosnap.backup
sudo apt update
sudo apt install snapd
sudo snap install multipass
```