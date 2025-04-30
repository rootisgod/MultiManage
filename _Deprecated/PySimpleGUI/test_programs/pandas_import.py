import PySimpleGUI as sg
import pandas as pd
import subprocess
import io

results = sg.execute_get_results(sg.execute_command_subprocess(r'multipass', 'info', '--all', '--format', 'csv', pipe_output=True, wait=True, stdin=subprocess.PIPE))
if results[0]:
    columnsToRead = ["Name", "State", "Ipv4", "Release", "CPU(s)", "Memory total"]
    df = pd.read_csv(io.StringIO(results[0]), usecols = columnsToRead)
    data = df.values.tolist()
    header_list = df.iloc[0].tolist()
    print(columnsToRead)
    print(data)