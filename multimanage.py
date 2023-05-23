######################################################################
# Import Required Libraries
######################################################################
import PySimpleGUI as sg
import pandas as pd
import numpy as np
import pyperclip
import yaml
import webbrowser
# Needed for linux machines
import tkinter as tk
# Builtin packages
import json
import subprocess
import os
import sys
import platform
import textwrap
import io
import random
import pathlib

######################################################################
# Global Vars
######################################################################
randomwords = ["time", "year", "people", "way", "day", "man", "thing", "woman", "life", "child", "world", "school", "state", "family", "student", "group", "country", "problem", "hand", "part", "place", "case", "week", "company", "system", "program", "question", "work", "government", "number", "night", "point", "home", "water", "room", "mother", "area", "money", "story", "fact", "month", "lot", "right", "study", "book", "eye", "job", "word", "business", "issue", "side", "kind", "head", "house", "service", "friend", "father", "power", "hour", "game", "line", "end", "member", "law", "car", "city", "community", "name", "president", "team", "minute", "idea", "kid", "body", "information", "back", "parent", "face", "others", "level", "office", "door", "health", "person", "art", "war", "history", "party", "result", "change", "morning", "reason", "research", "girl", "guy", "moment", "air", "teacher", "force", "education"]
selectedInstanceName = ''
columnsToRead = ["Name", "State", "Ipv4", "Release", "Memory total", "Memory usage", "CPU(s)", "Load", "Disk usage", "Disk total"]
instanceTableNumRows = 6
local_cloud_init_yaml_filename = 'cloud-init.yaml'
local_mac_shell_script_name = '_mac_launch_script.sh'
cloud_init_examples_url = 'https://cloudinit.readthedocs.io/en/latest/reference/examples.html'


def runCommandInTerminalWindow(cmd):
    if platform.system() in ("Windows"):
        retval = os.system(cmd)
    if platform.system() in ("Darwin"):
        retval = os.system(f'clear; echo "/usr/local/bin/{cmd}; kill -9 $$" > {local_mac_shell_script_name} ; chmod +x {local_mac_shell_script_name} ; open --wait-apps -a Terminal {local_mac_shell_script_name}; sleep 0.5; rm {local_mac_shell_script_name}; kill -9 $$')
    if platform.system() in ("Linux"):
        terminal_command = get_linux_terminal()
        # Gnome terminal needs a wait command added
        if terminal_command == 'gnome-terminal': 
            terminal_command = f"{terminal_command} --wait"
        retval = os.system(f"{terminal_command} -e '{get_linux_shell()} -c \"{cmd}\"'")
    return retval


def GetScreenHeight():
    root = tk.Tk()
    root.withdraw()
    SCREEN_HEIGHT = root.winfo_screenheight()
    return SCREEN_HEIGHT


######################################################################
# Global Functions and Data
######################################################################
def IsMultipassRunning():
    global instancesHeadersForTable
    global instancesDataForTable
    results = sg.execute_get_results(sg.execute_command_subprocess(r'multipass', pipe_output=True, wait=True, stdin=subprocess.PIPE))
    if 'Available commands' in results[0]:
        print('MULTIPASS FOUND')
        return True
    else:
        print('MULTIPASS NOT FOUND')
        return False


def get_random_word():
    return random.choice(randomwords)


def UpdateInstanceTableValues():
    # https://www.digitalocean.com/community/tutorials/update-rows-and-columns-python-pandas
    global columnsToRead
    global instancesHeadersForTable
    global instancesDataForTable
    results = sg.execute_get_results(sg.execute_command_subprocess(r'multipass', 'info', '--all', '--format', 'csv', pipe_output=True, wait=True, stdin=subprocess.PIPE))
    if results[0]:
        df = pd.read_csv(io.StringIO(results[0]), usecols = columnsToRead)
        # Massive the data a bit to remove NaNs
        df['Memory total'] = df['Memory total'].replace(np.nan, 0)
        df['Memory usage'] = df['Memory usage'].replace(np.nan, 0)
        df['Disk total'] = df['Disk total'].replace(np.nan, 0)
        df['Disk usage'] = df['Disk usage'].replace(np.nan, 0)
        df['CPU(s)'] = df['CPU(s)'].replace(np.nan, 0)
        df['Load'] = df['Load'].replace(np.nan, 0)
        # Replace any others that we aren't calculating
        df.fillna('', inplace=True)
        # Make the numbers more human readable
        df['Memory total'] = df['Memory total'].map(lambda x: f'{int((x/1024/1024))} MB')
        df['Memory usage'] = df['Memory usage'].map(lambda x: f'{int((x/1024/1024))} MB')
        df['Disk total'] = df['Disk total'].map(lambda x: f'{(x/1024/1024/1024):.2f} GB')
        df['Disk usage'] = df['Disk usage'].map(lambda x: f'{(x/1024/1024/1024):.2f} GB')
        df['CPU(s)'] = df['CPU(s)'].map(lambda x: int(x))
        df['Load'] = df['Load'].map(lambda x: x)
        data = df.values.tolist()
        instancesHeadersForTable = list(df.columns.values)
        instancesDataForTable    = list(data)


def UpdateInstanceTableValuesAndTable(key):
    global instanceTableNumRows
    UpdateInstanceTableValues()
    window[key].update(values=instancesDataForTable, num_rows=instanceTableNumRows)
    # Fancy. Returns either rows count when less than 5, but settles on 5 once rows are over 5
    # tblInstances.update(values=instancesDataForTable, num_rows=min(len(instancesDataForTable), 5) )


def UpdatetxtStatusBoxAndRefreshWindow(key, value, window):
    window[key].update(value)
    window.refresh()


def running_instance_selected():
    window['-STARTBUTTON-'].update(disabled=True)
    window['-RESTARTBUTTON-'].update(disabled=False)
    window['-STOPBUTTON-'].update(disabled=False)
    window['-DELETEBUTTON-'].update(disabled=True)
    window['-SHELLINTOINSTANCEBUTTON-'].update(disabled=False)


def stopped_instance_selected():
    window['-STARTBUTTON-'].update(disabled=False)
    window['-RESTARTBUTTON-'].update(disabled=True)
    window['-STOPBUTTON-'].update(disabled=True)
    window['-DELETEBUTTON-'].update(disabled=False)
    window['-SHELLINTOINSTANCEBUTTON-'].update(disabled=True)


# This is a bit of a crutch. After a start/stop/restart/delete instance the table loses the row item selected
# If we keep the selection we update the button status of it and remove this (but its more complicated to do)
def no_instance_selected():
    window['-STARTBUTTON-'].update(disabled=True)
    window['-RESTARTBUTTON-'].update(disabled=True)
    window['-STOPBUTTON-'].update(disabled=True)
    window['-DELETEBUTTON-'].update(disabled=True)
    window['-SHELLINTOINSTANCEBUTTON-'].update(disabled=True)


def runCommand(cmd, timeout=None, window=None):
    if values["-SHOWCONSOLE-"]:
        runCommandInPopupWindow(cmd=cmd)
    elif not values["-SHOWCONSOLE-"]:
        runCommandSilently(cmd=cmd, window=window)


# This function does the actual "running" of the command.  Also watches for any output. If found output is printed
def runCommandSilently(cmd, timeout=None, window=None):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        line = line.strip()
        if line != '':
            output += line
            window['-OUTBOX-'].update(line)
            window.Refresh() if window else None        # yes, a 1-line if, so shoot me
    retval = p.wait(timeout)
    if retval != 0:
        sg.popup('Error. I will improve the feedback later... It is probably your cloudinit file, or lack of RAM/DISK for chosen image that is invalid though.', keep_on_top=True)
    return (retval, output)                         # also return the output just for fun


# This function does the actual "running" of the command in a popup window
def runCommandInPopupWindow(cmd, timeout=None):
    popup_layout = [[sg.Output(size=(60,4), key='-OUT-')]]
    popup_window = sg.Window('Running Actions. Please wait...', popup_layout, finalize=True, disable_close=True, keep_on_top=True)

    print(f'\n      COMMAND: "{cmd}"')
    popup_window.Refresh() if window else None        # yes, a 1-line if, so shoot me
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        line = line.strip()
        output += line
        print(line)
        popup_window['-OUT-'].update(line)
        popup_window.Refresh() if window else None        # yes, a 1-line if, so shoot me
    retval = p.wait(timeout)
    if retval != 0:
        sg.popup('Error. I will improve the feedback later... It is probably your cloudinit file, or lack of RAM/DISK for chosen image that is invalid though.', keep_on_top=True)
    popup_window.close()
    # return (retval, output)                         # also return the output just for fun


def loadYAMLCloudInitFile(filePathAndName):
    # https://stackoverflow.com/questions/67065794/how-to-open-a-file-upon-button-click-pysimplegui
    cloud_init_yaml = ''
    with open(filePathAndName, 'r') as file:
        cloud_init_yaml = yaml.safe_load(file)
    with open(filePathAndName, "rt", encoding='utf-8') as file:
        cloud_init_yaml = file.read()
    return cloud_init_yaml


# Had to create this to be able to resize the GUI. I'm not sure if this is the best way to do it, but it works.
# https://github.com/PySimpleGUI/PySimpleGUI/issues/4976
def new_window():
    global GUISize
    global instanceTableNumRows
    labeltextwidth = 12

    ### Manage Instances ###
    txtInstanceType = sg.Text('Instance Type?', size=labeltextwidth, tooltip='Which image to use')
    cboInstanceTypes = sg.Combo(instanceTypes, readonly=True, enable_events=True, expand_x=True, key='-INSTANCETYPE-')
    txtInstanceName = sg.Text('Instance Name', size=labeltextwidth, tooltip='Leave blank for a random name')
    inpInstanceName = sg.Input(key='-INSTANCENAME-', expand_x=True)
    txtCPUCores = sg.Text('CPU Cores', size=labeltextwidth)
    sliCPUCores = sg.Slider((1, 8), 2, 1, disable_number_display=True, tick_interval=1, orientation="h", key="-OUTPUT-CPU-", expand_x=True)
    txtRAM = sg.Text('RAM (MB)', size=labeltextwidth)
    sliRAM = sg.Slider((0, 16384), 1024, 256, tick_interval=2048, orientation="h", key="-OUTPUT-RAM-", expand_x=True)
    txtDiskGB = sg.Text('Disk (GB)', size=labeltextwidth)
    sliDiskGB = sg.Slider((0, 256), 8, 4, tick_interval=16, orientation="h", key="-OUTPUT-DISK-", expand_x=True)
    cbUseCloudInit = sg.CBox(textwrap.fill('Run Cloud Init File?', labeltextwidth), default=True, enable_events=True, key='-USECLOUDINIT-')
    txtCloudInitFile = sg.Text(textwrap.fill('Import\nFile?', labeltextwidth),font=(None, GUISize, "underline"), tooltip=f'Click for Cloud Init Reference Guide: {cloud_init_examples_url}', size=labeltextwidth, key='-CLOUDINITFILEPATH-', enable_events=True)
    inpCloudInitFile = sg.Input(expand_x=True, key='-CLOUDINITINPUT-')
    btnLoadCloudInitFile = sg.Button('Browse', key='-LOADCLOUDINITFILE-', expand_x=True)
    mulCloudInitYAML = sg.Multiline(default_text='package_update: true\npackage_upgrade: true', size=(50,8),  expand_x=True, key='-CLOUDINITYAML-')
    btnCreateInstance = sg.Button('⚡ Create Instance', key="-CREATEINSTANCE-", expand_x=True, tooltip='Create the instance described above (launches in new console window)')
    ### Table ###
    txtInstances = sg.Text('Instances', justification='center', expand_x=True)
    tblInstances = sg.Table(values=instancesDataForTable, enable_events=True, key='-INSTANCEINFO-', headings=instancesHeadersForTable, max_col_width=25, auto_size_columns=True, justification='right', num_rows=instanceTableNumRows, expand_x=True, select_mode=sg.TABLE_SELECT_MODE_BROWSE, enable_click_events=True)  # https://github.com/PySimpleGUI/PySimpleGUI/issues/5198
    btnStartInstance  = sg.Button('⏵ Start Instance',  disabled=True, key='-STARTBUTTON-',  expand_x=True)
    btnRestartInstance  = sg.Button('↻ Restart Instance',  disabled=True, key='-RESTARTBUTTON-',  expand_x=True)
    btnStopInstance   = sg.Button('⏹ Stop Instance',   disabled=True, key='-STOPBUTTON-',   expand_x=True)
    btnDeleteInstance = sg.Button('⨉ Delete Instance', disabled=True, key='-DELETEBUTTON-', expand_x=True)
    btnShellIntoInstance = sg.Button('$ Shell Into Instance', disabled=True, key='-SHELLINTOINSTANCEBUTTON-', expand_x=True)
    btnRefreshTable = sg.Button('↻ Refresh Table', disabled=False, key='-REFRESHTABLEBUTTON-', expand_x=True)
    ### STATUS ###
    stsInstanceInfo = sg.InputText('', readonly=True, expand_x=True, disabled_readonly_background_color ='black', key='-STATUS-')
    cbConsole = sg.CBox('Console?', default=True, enable_events=True, key='-SHOWCONSOLE-', visible=False)
    txtGuiSize = sg.Text(f'GUI SIZE: {GUISize}')
    btnDecreaseGUISize = sg.Button('-', disabled=False, size=2, key='-DECREASEGUISIZE-')
    btnIncreaseGUISize = sg.Button('+', disabled=False, size=2, key='-INCREASEGUISIZE-')
    outBox = sg.Output(size=(20,4), expand_x=True, visible=False, key='-OUTBOX-')

    # LAYOUT
    layout = [
        ### Create Instances ###
        [
            [
                [txtInstanceType, cboInstanceTypes],
                [txtInstanceName, inpInstanceName],
                [txtCPUCores, sliCPUCores],
                [txtRAM, sliRAM],
                [txtDiskGB, sliDiskGB],
                [txtCloudInitFile, inpCloudInitFile, btnLoadCloudInitFile],
                [cbUseCloudInit, mulCloudInitYAML],
                [btnCreateInstance],
            ],
            [sg.HorizontalSeparator()],
        ],
        ### Manage Instances ###
        [
            # [txtInstances],
            [tblInstances],
            [[btnStartInstance, btnRestartInstance, btnStopInstance, btnDeleteInstance, btnShellIntoInstance,btnRefreshTable],],
        ],
        ### STATUS ###
        [
            [sg.HorizontalSeparator()],
            [stsInstanceInfo, cbConsole, txtGuiSize, btnDecreaseGUISize, btnIncreaseGUISize],
            [outBox]
        ],
    ]

    # window = sg.Window("MultiManage", icon=icon_base64_png)
    window = sg.Window("MultiManage", icon=icon_base64_png, finalize=True).Layout(layout)
    return window


######################################################################
# Pre Launch Check and Data Initialization
######################################################################
if not IsMultipassRunning():
    import PySimpleGUI as psgmultipassnotfound
    psgmultipassnotfound.popup("Multipass not found or is not running.\nPlease ensure the command\n\n  multipass version\n\nworks from the command line first.")
    sys.exit()

results = sg.execute_get_results(sg.execute_command_subprocess(r'multipass', 'find', '--format', 'json', pipe_output=True, wait=True, stdin=subprocess.PIPE))
if results[0]:
    jsonData = json.loads(results[0])
    instanceTypes = list(jsonData['images'].keys())

results = sg.execute_get_results(sg.execute_command_subprocess(r'multipass', 'list', '--format', 'json', pipe_output=True, wait=True, stdin=subprocess.PIPE))
if results[0]:
    jsonData = json.loads(results[0])
    instanceNames = [i['name'] for i in jsonData['list']]
    print(str(len(instanceNames)) + " instances: " + ", ".join(instanceNames))

# To save the local cloud init file we generate on a run
working_folder = pathlib.Path().resolve()
######################################################################
# Look and Feel
######################################################################
# Get Values for the Instance Table
UpdateInstanceTableValues()
# ICON for Program
icon_base64 = 'iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAYAAABccqhmAAAFwWlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4KPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNS41LjAiPgogPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIgogICAgeG1sbnM6cGhvdG9zaG9wPSJodHRwOi8vbnMuYWRvYmUuY29tL3Bob3Rvc2hvcC8xLjAvIgogICAgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIgogICAgeG1sbnM6ZXhpZj0iaHR0cDovL25zLmFkb2JlLmNvbS9leGlmLzEuMC8iCiAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyIKICAgIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIgogICAgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIKICAgeG1wOkNyZWF0ZURhdGU9IjIwMjMtMDUtMTRUMjI6MDM6MDErMDEwMCIKICAgeG1wOk1vZGlmeURhdGU9IjIwMjMtMDUtMTRUMjI6MzU6MDgrMDE6MDAiCiAgIHhtcDpNZXRhZGF0YURhdGU9IjIwMjMtMDUtMTRUMjI6MzU6MDgrMDE6MDAiCiAgIHBob3Rvc2hvcDpEYXRlQ3JlYXRlZD0iMjAyMy0wNS0xNFQyMjowMzowMSswMTAwIgogICBwaG90b3Nob3A6Q29sb3JNb2RlPSIzIgogICBwaG90b3Nob3A6SUNDUHJvZmlsZT0ic1JHQiBJRUM2MTk2Ni0yLjEi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'
icon_base64_png = 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAypSURBVHhe5dtXiC3FFgbgOsecc84ZxQTmgGJWVEQwP6hHVFDUB0UMjwoqCD6oTwpGVMwZc84JI+asmHPO555v3V379vR09e49e871Xvyh2T1dXVUrr1VVPVOmz0D6G/Dbb7+ln3/+Oe7nmmuuNPvss8f9fxszXQBPPPFEuvPOO9PTTz+dnnrqqfTxxx/3Wpqx1FJLpY022ihtuOGGaccdd0ybbLJJr2XmYKYI4KqrrkoXXnhhuv3229Oss86a5p9//tDwbLPNlmaZZZY0ZcqU3ptjgZQ///wz/f7772Eh3333Xfrjjz/SzjvvnKZNm5b22Wef3puTh0kVwNFHH53OPffcMOkFF1wwzTHHHL2W0fDrr7+mb775JlzmqKOOSuecc06vZXRMigBo56KLLkqLLrpomnfeeXtPZw5++OGH9MUXX6SDDz44rGxUTO39Tgi0zZxvvfXWtNJKK8105sEc5jKnudEwCiZsASuuuGL69NNP05JLLtl78vfgk08+SUsssUR69913e0+Gw9AWIJqTvGD1dzMPaEALmtA2LIYSwBlnnBEpigmK7m1gWL/88kv6/vvv008//RREDgNZ4Mcff4y+MkEb0IImtKFxGHR2gcMPPzydf/75MdGgLgjG/HbbbRcaEr3VAx988EGkxDYYW8Tfcsst0worrBAp8fnnn0+vvfZaWmihhXpvNYMVvPPOO+mwww5L5513Xu9pOzoJAPMi7nLLLTeQ+b/++ity/XHHHdfP4wiTFh977LGoDUpCMDatn3TSSdFP+tN3vvnmS2+88Ua69NJL08ILL9x7uxneJ2iZqYsQBrrA6aefHprvwjzQ3hFHHJG+/PLLYIBAmL/Utdlmm0XwLLkDgR1yyCFh9q7c9+uvv04rr7xyVIVcow1oRCua0T4IrQJQup588smdzB4Qm+MD4mkjwz3hEAL3qMP4Cqjll1++bzUZ7uX/TTfdNAQzCMZCB9rx0IZWAWy88cadmQfvMddS0NI+zzzzNFqAtgUWWCB8vgm5L8F2gffRjoc2FAXAVJdddtkYqCumTp2aPvroozT33HP3noyFdrWDNUEdtPzZZ58VV4X6fv755419S0A7HvBSQqMAVFcIHZTq6kAkfxW19UVA9WIdd911V5pzzjl7Pf4DAhA877333hBCva/AeccddxSFWwI68FKqGBsFYFEz0SKHiRJEJhrBLoQ8+uij4f9V/66DC+ir5BUT9CWYt99+O7311ltxPyzwgqcmjBOA9LHYYov1/hoOfJvJrbXWWsE8qd92223puuuuC+3L7ZjCYB2eEdwOO+wQ71522WVhLVdffXUIQxZYZZVVihlkEPCEtzrGCcCqbqKLmq+++iodcMABoWWmLKe/+eab6fXXX08vvPBCRHLt3KQOGWK//faLyvGVV16JgubVV1+NGv/BBx+MlKrdHBMBnvBWxxgBHHPMMbGkbdLQIMjPm2++efgvE7/nnnv6ps8arr/++vh7mWWWGadJ93K3qE3711xzTRROAh7C77777rAO+wvS6KBaoAl4wlvdFcYIwEbDRLVP27vuumv4KAaqZSuBIF4Qo8l99913jCbd77///mE5mDVGNU4Qhl0mz3fbbbeYayLAWz0Y9gXA1/jnMKC5vFuzxx57RM0vVb388svjMojI/8ADD4QmMLf11luHS7hoNVsOAdTpMBa3MLY5zPXtt99GwOxaF2QYG68Z/bXALrvsEumr6zYWprPZYoJmaOiss87qB7Q6CIwZHnjggUH8zTffHM9333336HvllVdGHVEXHuTK8thjj41xrr322nApmQEtpfVFHRS23nrrRXCGvgAM3lYwVMFkDz300FitMUd9+aXNiYsvvjgtvvjivTfH48MPP4zFDiaz1hGFjFNOOSVK4RKsJwRC7+SCScwQYK+44oqBC6UMgbXH9r9dwFK1SepNUIvvtddewSRBIJ7v0tAaa6wRKbBUChPSTjvtFER7Xz8m7Z427f6WAhytS4XrrLNO3OvnUj0KqqyoyzoB8IpnCAHIt11MiNRMvsEGG8TktFe9rOa23377IiFcZZttton2el/Ptt1223inCSyN8Ph+va82cYTgs2bbgFc8QwjAiimbVBsMrqAoaYkmmWHTgkZfgVCMaSLSM23eaWo3prnN0YTc3tS3Drzm7bMQwJNPPtlpkUHaipiSsLQrZJrcSRuTZ0ElaPOOd+swJutoagM0ZesYBLyOcQHBSxQeBIMzM9tTJqxK2z3Teuihh8KfmyAFPfPMM+O07N4zbaVU7Pnjjz8eubze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'
# GUI Size. Mac needs a slightly bigger size than windows/linux due to retina screen
screen_height = GetScreenHeight()
if platform.system() in ("Darwin"):
    GUISize = 14
elif platform.system() in ("Windows"):
    if screen_height < 960:
        GUISize = 10
    elif screen_height >= 960 and screen_height < 1024:
        GUISize = 12
    elif screen_height >= 1024 and screen_height <= 1200:
        GUISize = 14
    elif screen_height > 1200:
        GUISize = 16
elif platform.system() in ("Linux"):
    if screen_height < 960:
        GUISize = 8
    elif screen_height >= 960 and screen_height < 1024:
        GUISize = 10
    elif screen_height >= 1024 and screen_height <= 1200:
        GUISize = 12
    elif screen_height > 1200:
        GUISize = 14
else:
    GUISize = 10

# Setup and Create Window
sg.set_options(font=f'Default {GUISize}')
sg.theme('DarkGrey13')
window = new_window()

def get_linux_terminal():
    global user_terminal
    user_terminal = 'gnome-terminal'
    # Naively try and see if the BASH command returns characters with the terminal path
    if len(subprocess.check_output(f'whereis gnome-terminal', shell=True)) > 20:
        user_terminal = 'gnome-terminal'
    elif len(subprocess.check_output(f'whereis konsole', shell=True)) > 20:
        user_terminal = 'konsole'
    elif len(subprocess.check_output(f'whereis xfce4-terminal', shell=True)) > 20:
        user_terminal = 'xfce4-terminal'
    else:
        user_terminal = 'gnome-terminal'
    return user_terminal

def get_linux_shell():
    global user_shell
    user_shell = os.getenv('SHELL')
    if user_shell is None:
        user_shell = '/bin/bash'
    return user_shell


######################################################################
# Event Loop
######################################################################
while True:
    event, values = window.read()
    print(event, values)  # Useful for debugging

    # MAIN GUI CODE
    if event == '-CREATEINSTANCE-':
        itype = values['-INSTANCETYPE-']
        if itype == '':
            itype = '22.04'
        iname = (values['-INSTANCENAME-']).strip()
        icpus = str(int(values['-OUTPUT-CPU-']))
        iram  = str(int(values['-OUTPUT-RAM-'])*1024*1024)
        idisk = str(int((values['-OUTPUT-DISK-'])*1024*1024*1024))
        if iname == '':
            iname = get_random_word() + "-" + get_random_word()
        commandline = (f'multipass launch {itype} -v -n {iname} -c {icpus} -m {iram} -d {idisk}')
        if values["-USECLOUDINIT-"] == True:
            f = open(f"{local_cloud_init_yaml_filename}", "w")
            f.write(values["-CLOUDINITYAML-"])
            f.close()
            commandline = commandline + f' --cloud-init {working_folder}/{local_cloud_init_yaml_filename}'
        UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"CREATING - '{iname}', OS:{itype}, {icpus}CPU, {str(int(values['-OUTPUT-RAM-']))}MB, {str(int(values['-OUTPUT-DISK-']))}GB", window)
        # For now, just push the windows command to a terminal window. Need to do the other OSs too
        if platform.system() in ("Windows"):
            retval = runCommandInTerminalWindow(commandline)
        elif platform.system() in ("Darwin"):
            retval = runCommandInTerminalWindow(commandline)
        elif platform.system() in ("Linux"):
            try:
                retval = runCommandInTerminalWindow(commandline)
            except:
                UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', 'COULD NOT FIND YOUR LINUX TERMINAL SOMEHOW', window)
        else:
            UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', 'COULD NOT FIND YOUR OS SOMEHOW - TRYING LAST RESORT', window)
            runCommand(cmd=(commandline), window=window)
        UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"CREATED INSTANCE '{iname}'", window)
        UpdateInstanceTableValuesAndTable('-INSTANCEINFO-')
    if event == '-INSTANCEINFO-':
        selection = values[event]
        if selection:
            # Not sure why i have to select the list inside the list... im a noob so probably me
            data_selected = [instancesDataForTable[row] for row in values[event]][0]
            selectedInstanceName = data_selected[0]
            # Start Button
            if ('Running' in data_selected):
                running_instance_selected()
            # Stop Button
            elif ('Stopped' in data_selected):
                stopped_instance_selected()
    # https://github.com/PySimpleGUI/PySimpleGUI/issues/5198
    if isinstance(event, tuple) and event[:2] == ('-INSTANCEINFO-', '+CLICKED+'):
        row, col = position = event[2]
        if None not in position and row >= 0:
            copiedValue = instancesDataForTable[row][col]
            try:
                pyperclip.copy(copiedValue)
                UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"COPIED TO CLIPBOARD: {copiedValue}", window)
            except:
                if platform.system() in ("Linux"):
                    UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"CANNOT COPY '{copiedValue}' TO CLIPBOARD. INSTALL XSEL TO FIX", window)
                else:
                    UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"CANNOT COPY '{copiedValue}' TO CLIPBOARD. UNKNOWN REASON", window)
    if event == '-LOADCLOUDINITFILE-':
        chosen_file = (sg.popup_get_file('Which CloudInit File?', multiple_files=False, no_window=True, keep_on_top=True, file_types=((('YAML Files', '*.yml, *.yaml'),))))
        if chosen_file != '':
            window['-CLOUDINITINPUT-'].update(chosen_file)
            window['-CLOUDINITYAML-'].update(loadYAMLCloudInitFile(filePathAndName=chosen_file))
            window['-USECLOUDINIT-'].update(True)
    if event == '-STARTBUTTON-':
        UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"STARTING INSTANCE: {selectedInstanceName}", window)
        commandline = (f'multipass start {selectedInstanceName} -v')
        runCommand(cmd=(commandline), window=window)
        UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"STARTED INSTANCE: {selectedInstanceName}", window)
        no_instance_selected()
        UpdateInstanceTableValuesAndTable('-INSTANCEINFO-')
    if event == '-RESTARTBUTTON-':
        UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"RESTARTING INSTANCE: {selectedInstanceName}", window)
        commandline = (f'multipass restart {selectedInstanceName} -v')
        runCommand(cmd=(commandline), window=window)
        UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"RESTARTED INSTANCE: {selectedInstanceName}", window)
        no_instance_selected()
        UpdateInstanceTableValuesAndTable('-INSTANCEINFO-')
    if event == '-STOPBUTTON-':
        UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"STOPPING INSTANCE: {selectedInstanceName}", window)
        commandline = (f'multipass stop {selectedInstanceName} -v')
        runCommand(cmd=(commandline), window=window)
        UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"STOPPED INSTANCE: {selectedInstanceName}", window)
        no_instance_selected()
        UpdateInstanceTableValuesAndTable('-INSTANCEINFO-')
    if event == '-DELETEBUTTON-':
        UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"DELETING INSTANCE: {selectedInstanceName} and PURGING ALL", window)
        commandline = (f'multipass delete {selectedInstanceName} -v')
        runCommand(cmd=(commandline), window=window)
        purgeAll = sg.popup_yes_no('Purge All Deleted Instances?', f'Deleted instances are recoverable if not purged.\nTo recover a deleted instance use the multipass CLI command below\n \n  multipass recover {selectedInstanceName}\n\n')
        if purgeAll == 'Yes':
            commandline = (f'multipass purge -v')
            runCommand(cmd=(commandline), window=window)
        UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"DELETED INSTANCE: {selectedInstanceName} and PURGED ALL", window)
        no_instance_selected()
        UpdateInstanceTableValuesAndTable('-INSTANCEINFO-')
    if event == '-REFRESHTABLEBUTTON-':
        no_instance_selected()
        UpdateInstanceTableValuesAndTable('-INSTANCEINFO-')
    if event == '-SHELLINTOINSTANCEBUTTON-':
        UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"SHELLING INTO INSTANCE: {selectedInstanceName}", window)
        if platform.system() in ("Windows"):
            os.system(f"start cmd /c multipass shell {selectedInstanceName}")
        elif platform.system() in ("Linux"):
            # Gnome and KDE. Not sure if we need others
            try:
                user_terminal = get_linux_terminal()
                user_shell = get_linux_shell()
                try:
                    os.system(f"{user_terminal} -e '{user_shell} -c \"multipass shell {selectedInstanceName}\"'")
                except:
                    UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', 'COULD NOT FIND YOUR TERMINAL SOMEHOW', window)
            except:
                UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', 'COULD NOT FIND YOUR SHELL SOMEHOW. SET THE $SHELL VAR', window)
                break
        elif platform.system() in ("Darwin"):
            os.system(f'echo "/usr/local/bin/multipass shell {selectedInstanceName}" > {local_mac_shell_script_name} ; chmod +x {local_mac_shell_script_name} ; open -a Terminal {local_mac_shell_script_name} ; sleep 2; rm {local_mac_shell_script_name}')
        else:
            sg.popup("Sorry, not supported on this OS: " + platform.system() + "\n\nOnly supported on\n- Windows\n- Linux\n- Mac")
        UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"SHELLED INTO INSTANCE: {selectedInstanceName}", window)
        no_instance_selected()
        UpdateInstanceTableValuesAndTable('-INSTANCEINFO-')
    if event == '-DECREASEGUISIZE-':
        GUISize -= 2
        sg.set_options(font=f'Default {GUISize}')
        window.close()
        window = new_window()
    if event == '-INCREASEGUISIZE-':
        GUISize += 2
        sg.set_options(font=f'Default {GUISize}')
        window.close()
        window = new_window()
    if event == "-CLOUDINITFILEPATH-":
        webbrowser.open(cloud_init_examples_url, new=0, autoraise=True)
    if event == sg.WIN_CLOSED or event == 'Exit':
        # Tidy up any files we created
        if platform.system() in ("Darwin"):
            os.remove(f'{working_folder}/{local_mac_shell_script_name}')
        if os.path.exists(local_cloud_init_yaml_filename):
            os.remove(f'{working_folder}/{local_cloud_init_yaml_filename}')
        break

######################################################################
# Close
######################################################################
window.close()
