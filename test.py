import subprocess
import sys
import PySimpleGUI as sg

def runCommand(cmd, timeout=None, window=None):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        output = line
        print(line)
        window.Refresh() if window else None        # yes, a 1-line if, so shoot me
    retval = p.wait(timeout)
    return (retval, output)                         # also return the output just for fun


layout = [
    [[sg.Input(key='_IN_')], [sg.Output(size=(60,1))], [sg.Button('Run')]]
]

window = sg.Window('Test', layout)

# GUI
while True:
    event, values = window.read()

    # Test multithreaded thingy. Disable buttons while things happen, but try display the bash outputss
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Run':
        print("RUNNING")
        # runCommand(cmd=values['multipass list'], window=window)
        # results = sg.execute_get_results(sg.execute_command_subprocess(r'multipass', 'launch', itype, '-c', icpus, '-m', iram, '-d', idisk, pipe_output=True, wait=True, stdin=subprocess.PIPE))

window.close()

