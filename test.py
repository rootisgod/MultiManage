import PySimpleGUI as sg
import json
import csv
import os
import subprocess

def ipconfig():
    terminal = "ifconfig" # if on mac
    if os.name in ("nt"): # if on a windows machine
        terminal = "multipass list"
        return os.system(terminal)
    return os.system(terminal)

# GUI Items
lefta = sg.Text('LEFT A')
leftb = sg.Text('LEFT B')
righta= sg.Text('RIGHTA')
rightb = sg.Text('RIGHTB')
bottoma = sg.Text('BOTTOMA')
bottomb = sg.Text('BOTTOMB')
seperatorLeftRight = sg.VerticalSeparator()
seperatorBottom = sg.HorizontalSeparator()

btnGo   = sg.Button('Go', key='-GO-')
btnExit = sg.Exit()

# GUI Layout
# layout = [[txtResult],[btnGo ],[btnExit]]

layout = [
    [[lefta, righta], seperatorLeftRight, [bottoma]]
]

window = sg.Window('Test', layout)

# GUI
while True:
    event, values = window.read()

    # Test multithreaded thingy. Disable buttons while things happen, but try display the bash outputss
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

window.close()

