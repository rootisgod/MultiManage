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

## Program Design
Options
 - Create New VM
   - Image (20.04, 22.04 etc)   (may need a refresh button to do a 'multipass find')
   - CPUs 1,2,3,4,5,6,7,8
   - Memory 256,512,1024,2048,4096,8192
   - Disk (GB)

# Linux Mint Setup

## Python 
```bash
apt install python3 python3-pip python3-tk
pip install pysimplegui 
```

## Multipass
```bash
sudo mv /etc/apt/preferences.d/nosnap.pref ~/Documents/nosnap.backup
sudo apt update
sudo apt install snapd
sudo snap install multipass
```