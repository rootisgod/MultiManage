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

ipconfig()

os.system("start /wait cmd /c multipass shell test")

quit()

# GUI Items
txtResult = sg.Text('--------------')
btnGo   = sg.Button('Go', key='-GO-')
btnExit = sg.Exit()

# GUI Layout
layout = [[txtResult],[btnGo ],[btnExit]]
window = sg.Window('Test', layout)

# GUI
while True:
    event, values = window.read()

    # Test multithreaded thingy. Disable buttons while things happen, but try display the bash outputss
    if event == '-GO-':
        print('PINGING')
        results = sg.execute_get_results(sg.execute_command_subprocess(r'ping', '127.0.0.1', '-t', '3', pipe_output=True, wait=True, stdin=subprocess.PIPE))
        txtResult.update(results[0].splitlines())
        print(results)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

window.close()

