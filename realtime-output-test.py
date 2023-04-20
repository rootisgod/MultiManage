# https://stackoverflow.com/questions/64680384/pysimplegui-displaying-console-output-in-gui

import subprocess
import sys
import PySimpleGUI as sg

def main():
    layout = [  [sg.Text('Enter a command to execute (e.g. dir or ls)')],
                [sg.Input(key='_IN_')],             # input field where you'll type command
                [sg.InputText('', expand_x=True, key='-STATUS-')],
                [sg.Button('Run'), sg.Button('Exit')] ]     # a couple of buttons

    window = sg.Window('Realtime Shell Command Output', layout)
    while True:             # Event Loop
        event, values = window.Read()
        if event in (None, 'Exit'):         # checks if user wants to
            exit
            break

        if event == 'Run':                  # the two lines of code needed to get button and run command
            runCommand(cmd='dir', window=window)
    window.Close()

# This function does the actual "running" of the command.  Also watches for any output. If found output is printed
def runCommand(cmd, timeout=None, window=None):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        output += line
        window['-STATUS-'].update(line)
        window.Refresh() if window else None        # yes, a 1-line if, so shoot me
    retval = p.wait(timeout)
    return (retval, output)                         # also return the output just for fun

if __name__ == '__main__':
    main()