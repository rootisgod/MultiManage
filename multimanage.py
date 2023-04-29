######################################################################
# Import Required Libraries
######################################################################
import PySimpleGUI as sg
import json
import csv
import subprocess
import os
import sys
import platform
import yaml
import textwrap

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

def UpdateInstanceTableValues():
    global instancesHeadersForTable
    global instancesDataForTable
    results = sg.execute_get_results(sg.execute_command_subprocess(r'multipass', 'list', '--format', 'csv', pipe_output=True, wait=True, stdin=subprocess.PIPE))
    if results[0]:
        joinedData = results[0].splitlines()
        csvData = csv.reader(joinedData)
        instancesHeadersForTable = next(csvData)
        instancesDataForTable = list(csvData)  # read everything else into a list of rows

def UpdateInstanceTableValuesAndTable(key):
    global instanceTableNumRows
    UpdateInstanceTableValues()
    window[key].update(values=instancesDataForTable, num_rows=instanceTableNumRows)
    # Fancy. Returns either rows count when less than 5, but settles on 5 once rows are over 5
    # tblInstances.update(values=instancesDataForTable, num_rows=min(len(instancesDataForTable), 5) )

def UpdatetxtStatusBoxAndRefreshWindow(key, value, window):
    window[key].update(value)
    window.refresh()

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
        sg.popup('Error. I will improve the deedback later... It is probably your cloudinit file that is invalid though.')
    return (retval, output)                         # also return the output just for fun

def loadYAMLCloudInitFile(filePathAndName='./cloud-init/quick.yaml'):
    # https://stackoverflow.com/questions/67065794/how-to-open-a-file-upon-button-click-pysimplegui
    cloud_init_yaml = ''
    with open(filePathAndName, 'r') as file:
        cloud_init_yaml = yaml.safe_load(file)
    with open(filePathAndName, "rt", encoding='utf-8') as file:
        cloud_init_yaml= file.read()
    return cloud_init_yaml


# This function does the actual "running" of the command in a popup window
def runCommandInPopupWindow(cmd, timeout=None):
    popup_layout = [[sg.Output(size=(60,4), key='-OUT-')]]
    popup_window = sg.Window('Console', popup_layout, finalize=True)
    print('==================================================')
    print(f'    COMMAND: "{cmd}"')
    print('==================================================')
    popup_window.Refresh() if window else None        # yes, a 1-line if, so shoot me
    # f'GUI SIZE: {GUISize}'
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
        sg.popup('Error. I will improve the deedback later... It is probably your cloudinit file that is invalid though.')
    popup_window.close()
    # return (retval, output)                         # also return the output just for fun

# Had to create this to be able to resize the GUI. I'm not sure if this is the best way to do it, but it works.
# https://github.com/PySimpleGUI/PySimpleGUI/issues/4976
def new_window():
    global GUISize
    global instanceTableNumRows
    labeltextwidth = 12

    ### Manage Instances ###
    txtInstanceType = sg.Text('Instance Type?', size=labeltextwidth)
    cboInstanceTypes = sg.Combo(instanceTypes, readonly=True, enable_events=True, expand_x=True, key='-INSTANCETYPE-')
    txtInstanceName = sg.Text('Instance Name', size=labeltextwidth)
    inpInstanceName = sg.Input(key='-INSTANCENAME-', expand_x=True)
    txtCPUCores = sg.Text('CPU Cores', size=labeltextwidth)
    sliCPUCores = sg.Slider((1, 8), 2, 1, disable_number_display=True, tick_interval=1, orientation="h", key="-OUTPUT-CPU-", expand_x=True)
    txtRAM = sg.Text('RAM (MB)', size=labeltextwidth)
    sliRAM = sg.Slider((0, 8192), 1024, 256, tick_interval=2048, orientation="h", key="-OUTPUT-RAM-", expand_x=True)
    txtDiskGB = sg.Text('Disk (GB)', size=labeltextwidth)
    sliDiskGB = sg.Slider((0, 128), 8, 4, tick_interval=16, orientation="h", key="-OUTPUT-DISK-", expand_x=True)
    cbUseCloudInit = sg.CBox(textwrap.fill('Run Cloud Init File?', labeltextwidth), default=False, enable_events=True, key='-USECLOUDINIT-')
    txtCloudInitFile = sg.Text(textwrap.fill('Load File?', labeltextwidth), size=labeltextwidth, key='-CLOUDINITFILEPATH-')
    inpCloudInitFile = sg.Input(expand_x=True, key='-CLOUDINITINPUT-')
    btnLoadCloudInitFile = sg.Button('Browse', key='-LOADCLOUDINITFILE-', expand_x=True)
    mulCloudInitYAML = sg.Multiline(default_text='package_update: true\npackage_upgrade: true', size=(50,8),  expand_x=True, key='-CLOUDINITYAML-')
    btnCreateInstance = sg.Button('⚡ Create Instance', key="-CREATEINSTANCE-", expand_x=True)
    txtInstances = sg.Text('Instances')
    tblInstances = sg.Table(values=instancesDataForTable, enable_events=True, key='-INSTANCEINFO-', headings=instancesHeadersForTable, max_col_width=25, auto_size_columns=True, justification='right', num_rows=instanceTableNumRows, expand_x=True, select_mode=sg.TABLE_SELECT_MODE_BROWSE)
    btnStartInstance  = sg.Button('⏵ Start Instance',   disabled=True, key='-STARTBUTTON-', expand_x=True)
    btnStopInstance   = sg.Button('⏹ Stop Instance',   disabled=True, key='-STOPBUTTON-', expand_x=True)
    btnDeleteInstance = sg.Button('⨉ Delete Instance', disabled=True, key='-DELETEBUTTON-', expand_x=True)
    btnShellIntoInstance = sg.Button('$ Shell Into Instance', disabled=True, key='-SHELLINTOINSTANCEBUTTON-', expand_x=True)
    btnRefreshTable = sg.Button('↻ Refresh Table', disabled=False, key='-REFRESHTABLEBUTTON-', expand_x=True)
    stsInstanceInfo = sg.InputText('', readonly=True, expand_x=True, disabled_readonly_background_color ='black', key='-STATUS-')
    cbConsole = sg.CBox('Console?', default=True, enable_events=True, key='-SHOWCONSOLE-')
    txtGuiSize = sg.Text(f'GUI SIZE: {GUISize}')
    btnDecreaseGUISize = sg.Button('-', disabled=False, size=2, key='-DECREASEGUISIZE-')
    btnIncreaseGUISize = sg.Button('+', disabled=False, size=2, key='-INCREASEGUISIZE-')
    outBox = sg.Output(size=(20,5), expand_x=True, visible=False, key='-OUTBOX-')
    # btnExit = sg.Exit()

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
            [txtInstances],
            [tblInstances],
            [[btnStartInstance, btnStopInstance, btnDeleteInstance, btnShellIntoInstance],
            [btnRefreshTable]],
        ],
        ### STATUS ###
        [
            [sg.HorizontalSeparator()],
            [stsInstanceInfo, cbConsole, txtGuiSize, btnDecreaseGUISize, btnIncreaseGUISize],
            [outBox]
        ],
    ]

    window = sg.Window('MultiManage', layout)
    return window

######################################################################
# Pre Launch Check and Data Initialization
######################################################################
if not IsMultipassRunning():
    import PySimpleGUI as psgmultipassnotfound
    psgmultipassnotfound.popup("Multipass not found or is not running.\nPlease ensure the command\n\n  multipass version\n\nworks from the command line first.")
    quit()

results = sg.execute_get_results(sg.execute_command_subprocess(r'multipass', 'find', '--format', 'json', pipe_output=True, wait=True, stdin=subprocess.PIPE))
if results[0]:
    jsonData = json.loads(results[0])
    instanceTypes = list(jsonData['images'].keys())

results = sg.execute_get_results(sg.execute_command_subprocess(r'multipass', 'list', '--format', 'json', pipe_output=True, wait=True, stdin=subprocess.PIPE))
if results[0]:
    jsonData = json.loads(results[0])
    instanceNames = [i['name'] for i in jsonData['list']]
    print(str(len(instanceNames)) + " instances: " + ", ".join(instanceNames))

# Data Initialization
# Vars we want to keep in a kind of 'cache'
selectedInstanceName = ''
instanceTableNumRows = 6
local_cloud_init_yaml_filename = 'cloud-init.yaml'
# Load Multipass Info
UpdateInstanceTableValues()

######################################################################
# Look and Feel
######################################################################
GUISize = 10
sg.set_options(font=f'Default {GUISize}')
sg.theme('DarkGrey13')    # Keep things interesting for your users
window = new_window()

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
        commandline = (f'multipass launch {itype} -vvv -c {icpus} -m {iram} -d {idisk}')
        if values["-USECLOUDINIT-"] == True:
            f = open(f"{local_cloud_init_yaml_filename}", "w")
            f.write(values["-CLOUDINITYAML-"])
            f.close()
            commandline = commandline + f' --cloud-init ./{local_cloud_init_yaml_filename}'
        if iname != '':
            commandline = commandline + f' -n {iname}'
            UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"CREATING - '{iname}', OS:{itype}, {icpus}CPU, {str(int(values['-OUTPUT-RAM-']))}MB, {str(int(values['-OUTPUT-DISK-']))}GB", window)
            runCommand(cmd=(commandline), window=window)
            UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"CREATED INSTANCE '{iname}'", window)
        else:
            UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"CREATING RANDOM NAMED INSTANCE - OS:{itype}, {icpus}CPU, {str(int(values['-OUTPUT-RAM-']))}MB, {str(int(values['-OUTPUT-DISK-']))}GB", window)
            runCommand(cmd=(commandline), window=window)
            UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"CREATED INSTANCE", window)
        UpdateInstanceTableValuesAndTable('-INSTANCEINFO-')
    if event == '-INSTANCEINFO-':
        selection = values[event]
        if selection:
            # Not sure why i have to select the list inside the list... im a noob so probably me
            data_selected = [instancesDataForTable[row] for row in values[event]][0]
            selectedInstanceName = data_selected[0]
            # Start Button
            if ('Running' in data_selected):
                window['-STARTBUTTON-'].update(disabled=True)
                window['-STOPBUTTON-'].update(disabled=False)
                window['-DELETEBUTTON-'].update(disabled=True)
                window['-SHELLINTOINSTANCEBUTTON-'].update(disabled=False)
            # Stop Button
            if ('Stopped' in data_selected):
                window['-STARTBUTTON-'].update(disabled=False)
                window['-STOPBUTTON-'].update(disabled=True)
                window['-DELETEBUTTON-'].update(disabled=False)
                window['-SHELLINTOINSTANCEBUTTON-'].update(disabled=True)
    if event == '-LOADCLOUDINITFILE-':
        chosen_file = (sg.popup_get_file('Which CloudInit File?', multiple_files=False, no_window=True, keep_on_top=True, file_types=((('YAML Files', '*.yml, *.yaml'),))))
        if chosen_file != '':
            window['-CLOUDINITINPUT-'].update(chosen_file)
            window['-CLOUDINITYAML-'].update(loadYAMLCloudInitFile(filePathAndName=chosen_file))
            window['-USECLOUDINIT-'].update(True)
    if event == '-STARTBUTTON-':
        UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"STARTING INSTANCE: {selectedInstanceName}", window)
        commandline = (f'multipass start {selectedInstanceName} -vvv')
        runCommand(cmd=(commandline), window=window)
        # runCommandInPopupWindow(cmd=commandline)
        UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"STARTED INSTANCE: {selectedInstanceName}", window)
        UpdateInstanceTableValuesAndTable('-INSTANCEINFO-')
    if event == '-STOPBUTTON-':
        UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"STOPPING INSTANCE: {selectedInstanceName}", window)
        commandline = (f'multipass stop {selectedInstanceName} -vvv')
        runCommand(cmd=(commandline), window=window)
        # runCommandInPopupWindow(cmd=commandline)
        UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"STOPPED INSTANCE: {selectedInstanceName}", window)
        UpdateInstanceTableValuesAndTable('-INSTANCEINFO-')
    if event == '-DELETEBUTTON-':
        UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"DELETING INSTANCE: {selectedInstanceName}", window)
        sg.execute_get_results(sg.execute_command_subprocess(r'multipass', 'delete', selectedInstanceName, pipe_output=True, wait=True, stdin=subprocess.PIPE))
        sg.execute_get_results(sg.execute_command_subprocess(r'multipass', 'purge', pipe_output=True, wait=True, stdin=subprocess.PIPE))
        UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"DELETED INSTANCE: {selectedInstanceName}", window)
        UpdateInstanceTableValuesAndTable('-INSTANCEINFO-')
    if event == '-REFRESHTABLEBUTTON-':
        UpdateInstanceTableValuesAndTable('-INSTANCEINFO-')
    if event == '-SHELLINTOINSTANCEBUTTON-':
        UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"SHELLING INTO INSTANCE: {selectedInstanceName}", window)
        if platform.system() in ("Windows"):
            os.system(f"start cmd /c multipass shell {selectedInstanceName}")
        elif platform.system() in ("Linux"):
            # Need to see if we need a KDE style alternative, works for now
            os.system(f"gnome-terminal -e 'bash -c \"multipass shell {selectedInstanceName} \"'")
        elif platform.system() in ("Darwin"):
            os.system(f'echo "/usr/local/bin/multipass shell {selectedInstanceName}" > shell.sh ; chmod +x shell.sh ; open -a Terminal shell.sh ; sleep 2; rm shell.sh')
        else:
            sg.popup("Sorry, not supported on this OS: " + platform.system() + "\n\nOnly supported on\n- Windows\n- Linux\n- Mac")
        UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"SHELLED INTO INSTANCE: {selectedInstanceName}", window)
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
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

######################################################################
# Close
######################################################################
window.close()