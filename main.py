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
# Look and Feel
######################################################################
sg.set_options(font='Default 12')
sg.theme('DarkGrey13')    # Keep things interesting for your users

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

def UpdateInstanceTableValuesAndTable():
    UpdateInstanceTableValues()
    tblInstances.update(values=instancesDataForTable, num_rows=5)
    # Fancy. Returns either rows count when less than 5, but settles on 5 once rows are over 5
    # tblInstances.update(values=instancesDataForTable, num_rows=min(len(instancesDataForTable), 5) )


######################################################################
# Pre Launch Check
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

UpdateInstanceTableValues()
######################################################################
# Layout
######################################################################
# GUI OBJECTS

# Create Instances
txtInstanceType = sg.Text('Instance Type?')
cboInstanceTypes = sg.Combo(instanceTypes, size=43, readonly=True, enable_events=True, key='-INSTANCETYPE-')
txtInstanceName = sg.Text('Instance Name')
inpInstanceName = sg.Input(key='-INSTANCENAME-')
txtCPUCores = sg.Text('CPU Cores')
sliCPUCores = sg.Slider((1, 8), 2, 1, tick_interval=1, orientation="h", size=(40, 15), key="-OUTPUT-CPU-",)
txtRAM = sg.Text('RAM (MB)')
sliRAM = sg.Slider((0, 8192), 512, 256, tick_interval=2048, orientation="h", size=(40, 15), key="-OUTPUT-RAM-")
txtDiskGB = sg.Text('Disk Size (GB)')
sliDiskGB = sg.Slider((0, 128), 4, 4, tick_interval=16, orientation="h", size=(40, 15), key="-OUTPUT-DISK-")
btnCreateInstance = sg.Button('Create Instance', size=43, key="-CREATEINSTANCE-", disabled=True)

# Manage Instances
txtInstances = sg.Text('Instances')
tblInstances = sg.Table(values=instancesDataForTable, enable_events=True, key='-INSTANCEINFO-',
        headings=instancesHeadersForTable,
        max_col_width=25,
        auto_size_columns=True,
        justification='right',
        num_rows=5,
        select_mode=sg.TABLE_SELECT_MODE_BROWSE)
btnStartInstance  = sg.Button('Start Instance',  disabled=True, key='-STARTBUTTON-')
btnStopInstance   = sg.Button('Stop Instance',   disabled=True, key='-STOPBUTTON-')
btnDeleteInstance = sg.Button('Delete Instance', disabled=True, key='-DELETEBUTTON-')
btnShellIntoInstance = sg.Button('Shell Into Instance', disabled=True, key='-SHELLINTOINSTANCEBUTTON-')
stsInstanceInfo = sg.StatusBar('Status: ')
btnExit = sg.Exit()

# GUI Layout
layout = [ \
    ### Create Instances ###
    [
        [txtInstanceType],
        [cboInstanceTypes],
        [txtInstanceName],
        [inpInstanceName],
        [txtCPUCores],
        [sliCPUCores],
        [txtRAM],
        [sliRAM],
        [txtDiskGB],
        [sliDiskGB],
        [btnCreateInstance],
    ],
    ### Manage Instances ###
    [
        [sg.HorizontalSeparator()],
        [txtInstances],
        [tblInstances],
        [btnStartInstance, btnStopInstance, btnDeleteInstance, btnShellIntoInstance],
        [stsInstanceInfo],
    ],
    ### QUIT ###
    [
        [sg.HorizontalSeparator()],
        [btnExit],
    ],
]

######################################################################
# Window Creation
######################################################################
window = sg.Window('MultiManage', layout)

######################################################################
# Event Loop
######################################################################
while True:
    # Always Required
    event, values = window.read()
    # Useful for debugging
    # print(event, values)

    # The real events
    if event == '-INSTANCETYPE-':
        btnCreateInstance.update(disabled=False)
    if event == '-CREATEINSTANCE-':
        if values['-INSTANCETYPE-']:    # if something is highlighted in the list
            itype = values['-INSTANCETYPE-']
            iname = values['-INSTANCENAME-']
            icpus = str(int(values['-OUTPUT-CPU-']))
            iram  = str(int(values['-OUTPUT-RAM-'])*1024*1024)
            idisk = str(int((values['-OUTPUT-DISK-'])*1024*1024*1024))
            results = sg.execute_get_results(sg.execute_command_subprocess(r'multipass', 'launch', itype, '-n', iname,'-c', icpus, '-m', iram, '-d', idisk, pipe_output=True, wait=True, stdin=subprocess.PIPE))
            print(results)
            print('==================================')
            print(f"INSTANCETYPE: {itype}, CPUS:{icpus}, MEMORY:{iram}, DISK:{idisk}")
            print('==================================')
            UpdateInstanceTableValuesAndTable()
    if event == '-INSTANCEINFO-':
        selection = values[event]
        if selection:
            # Not sure why i have to select the list inside the list... im a noob so probably me
            data_selected = [instancesDataForTable[row] for row in values[event]][0]
            selectedInstanceName = data_selected[0]
            # Start Button
            if ('Running' in data_selected):
                btnStartInstance.update(disabled=True)
                btnStopInstance.update(disabled=False)
                btnDeleteInstance.update(disabled=True)
                btnShellIntoInstance.update(disabled=False)
            # Stop Button
            if ('Stopped' in data_selected):
                btnStartInstance.update(disabled=False)
                btnStopInstance.update(disabled=True)
                btnDeleteInstance.update(disabled=False)
                btnShellIntoInstance.update(disabled=True)
        # TODO: Else disable buttons

    if event == '-STARTBUTTON-':
        sg.execute_get_results(sg.execute_command_subprocess(r'multipass', 'start', selectedInstanceName, pipe_output=True, wait=True, stdin=subprocess.PIPE))
        UpdateInstanceTableValuesAndTable()
    if event == '-STOPBUTTON-':
        sg.execute_get_results(sg.execute_command_subprocess(r'multipass', 'stop', selectedInstanceName, pipe_output=True, wait=True, stdin=subprocess.PIPE))
        UpdateInstanceTableValuesAndTable()
    if event == '-DELETEBUTTON-':
        sg.execute_get_results(sg.execute_command_subprocess(r'multipass', 'delete', selectedInstanceName, pipe_output=True, wait=True, stdin=subprocess.PIPE))
        sg.execute_get_results(sg.execute_command_subprocess(r'multipass', 'purge', pipe_output=True, wait=True, stdin=subprocess.PIPE))
        UpdateInstanceTableValuesAndTable()
    if event == '-SHELLINTOINSTANCEBUTTON-':
        if platform.system() in ("Windows"): # if on a windows machine
            os.system(f"start cmd /c multipass shell {selectedInstanceName}")
        elif platform.system() in ("Linux"): # if on a linux machine
            # Need to see if we need a KDE style alternative, works for now
            os.system(f"gnome-terminal -e 'bash -c \"multipass shell {selectedInstanceName} \"'")
        elif platform.system() in ("Darwin"): # if on a mac machine
            os.system(f'echo "/usr/local/bin/multipass shell {selectedInstanceName}" > shell.sh ; chmod +x shell.sh ; open -a Terminal shell.sh ; sleep 2; rm shell.sh')
        else:
            sg.popup("Sorry, not supported on this OS: " + platform.system() + "\n\nOnly supported on\n- Windows\n- Linux\n- Mac")
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

######################################################################
# Close
######################################################################
window.close()