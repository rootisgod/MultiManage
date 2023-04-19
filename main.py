######################################################################
# Import Required Libraries
######################################################################
import PySimpleGUI as sg
import json
import csv
import subprocess
import os
import platform

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
    UpdateInstanceTableValues()
    window[key].update(values=instancesDataForTable, num_rows=5)
    # Fancy. Returns either rows count when less than 5, but settles on 5 once rows are over 5
    # tblInstances.update(values=instancesDataForTable, num_rows=min(len(instancesDataForTable), 5) )

def UpdatetxtStatusBoxAndRefreshWindow(key, value, window):
    window[key].update(value)
    window.refresh()

# Had to create this to be able to resize the GUI. I'm not sure if this is the best way to do it, but it works.
# https://github.com/PySimpleGUI/PySimpleGUI/issues/4976
def new_window():
    global GUISize
    labeltextwidth = 12

    ### Manage Instances ###
    txtInstanceType = sg.Text('Instance Type?', size=labeltextwidth)
    cboInstanceTypes = sg.Combo(instanceTypes, readonly=True, enable_events=True, expand_x=True, key='-INSTANCETYPE-')
    txtInstanceName = sg.Text('Instance Name', size=labeltextwidth)
    inpInstanceName = sg.Input(key='-INSTANCENAME-', expand_x=True)
    txtCPUCores = sg.Text('CPU Cores', size=labeltextwidth)
    sliCPUCores = sg.Slider((1, 8), 2, 1, disable_number_display=True, tick_interval=1, orientation="h", key="-OUTPUT-CPU-", expand_x=True)
    txtRAM = sg.Text('RAM (MB)', size=labeltextwidth)
    sliRAM = sg.Slider((0, 8192), 512, 256, tick_interval=2048, orientation="h", key="-OUTPUT-RAM-", expand_x=True)
    txtDiskGB = sg.Text('Disk (GB)', size=labeltextwidth)
    sliDiskGB = sg.Slider((0, 128), 4, 4, tick_interval=16, orientation="h", key="-OUTPUT-DISK-", expand_x=True)
    btnCreateInstance = sg.Button('Create Instance', key="-CREATEINSTANCE-", disabled=True, expand_x=True)
    txtInstances = sg.Text('Instances')
    tblInstances = sg.Table(values=instancesDataForTable, enable_events=True, key='-INSTANCEINFO-', headings=instancesHeadersForTable, max_col_width=25, auto_size_columns=True, justification='right', num_rows=5, expand_x=True, select_mode=sg.TABLE_SELECT_MODE_BROWSE)
    btnStartInstance  = sg.Button('Start Instance',   disabled=True, key='-STARTBUTTON-', expand_x=True)
    btnStopInstance   = sg.Button('Stop Instance',   disabled=True, key='-STOPBUTTON-', expand_x=True)
    btnDeleteInstance = sg.Button('Delete Instance', disabled=True, key='-DELETEBUTTON-', expand_x=True)
    btnShellIntoInstance = sg.Button('Shell Into Instance', disabled=True, key='-SHELLINTOINSTANCEBUTTON-', expand_x=True)
    stsInstanceInfo = sg.InputText('', readonly=True, expand_x=True, disabled_readonly_background_color ='black', key='-STATUS-')
    txtGuiSize = sg.Text(f'GUI SIZE: {GUISize}')
    btnDecreaseGUISize = sg.Button('-', disabled=False, size=2, key='-DECREASEGUISIZE-')
    btnIncreaseGUISize = sg.Button('+', disabled=False, size=2, key='-INCREASEGUISIZE-')
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
                [btnCreateInstance],
            ],
            [sg.HorizontalSeparator()],
        ],
        ### Manage Instances ###
        [
            [txtInstances],
            [tblInstances],
            [btnStartInstance, btnStopInstance, btnDeleteInstance, btnShellIntoInstance],
        ],
        ### STATUS ###
        [
            [sg.HorizontalSeparator()],
            [stsInstanceInfo, txtGuiSize, btnDecreaseGUISize, btnIncreaseGUISize]
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

# Do Any Data Initialization
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
# Vars we want to keep in a kind of 'cache'
selectedInstanceName = ''

while True:
    event, values = window.read()
    # print(event, values)  # Useful for debugging

    # MAIN GUI CODE
    if event == '-INSTANCETYPE-':
        window['-CREATEINSTANCE-'].update(disabled=False)
    if event == '-CREATEINSTANCE-':
        if values['-INSTANCETYPE-']:    # if something is highlighted in the list
            itype = values['-INSTANCETYPE-']
            iname = values['-INSTANCENAME-']
            icpus = str(int(values['-OUTPUT-CPU-']))
            iram  = str(int(values['-OUTPUT-RAM-'])*1024*1024)
            idisk = str(int((values['-OUTPUT-DISK-'])*1024*1024*1024))
            UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"CREATING - '{iname}', OS:{itype}, {icpus}CPU, {str(int(values['-OUTPUT-RAM-']))}MB, {str(int(values['-OUTPUT-DISK-']))}GB", window)
            results = sg.execute_get_results(sg.execute_command_subprocess(r'multipass', 'launch', itype, '-n', iname,'-c', icpus, '-m', iram, '-d', idisk, pipe_output=True, wait=True, stdin=subprocess.PIPE))
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

    # Annoyingly, the txtStatus box doesn't update before it runs the action. No idea why...
    if event == '-STARTBUTTON-':
        UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"STARTING INSTANCE: {selectedInstanceName}", window)
        sg.execute_get_results(sg.execute_command_subprocess(r'multipass', 'start', selectedInstanceName, pipe_output=True, wait=True, stdin=subprocess.PIPE))
        UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"STARTED INSTANCE: {selectedInstanceName}", window)
    if event == '-STOPBUTTON-':
        UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"STOPPING INSTANCE: {selectedInstanceName}", window)
        window.refresh()
        sg.execute_get_results(sg.execute_command_subprocess(r'multipass', 'stop', selectedInstanceName, pipe_output=True, wait=True, stdin=subprocess.PIPE))
        UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"STOPPED INSTANCE: {selectedInstanceName}", window)
        UpdateInstanceTableValuesAndTable('-INSTANCEINFO-')
    if event == '-DELETEBUTTON-':
        UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"DELETING INSTANCE: {selectedInstanceName}", window)
        sg.execute_get_results(sg.execute_command_subprocess(r'multipass', 'delete', selectedInstanceName, pipe_output=True, wait=True, stdin=subprocess.PIPE))
        sg.execute_get_results(sg.execute_command_subprocess(r'multipass', 'purge', pipe_output=True, wait=True, stdin=subprocess.PIPE))
        UpdatetxtStatusBoxAndRefreshWindow('-STATUS-', f"DELETED INSTANCE: {selectedInstanceName}", window)
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