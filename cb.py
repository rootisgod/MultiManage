import PySimpleGUI as sg

sg.change_look_and_feel('Dark Blue 3')

layout = [  [sg.Column([[sg.Text('My Window')],
                        [sg.CBox('Checkbox', key='-CBOX-')]])],
            [sg.B('Visible'), sg.B('Invisible'), sg.Button('Exit')]  ]

window = sg.Window('Window Title', layout)

while True:             # Event Loop
    event, values = window.read()
    print(event, values)
    if event in (None, 'Exit'):
        break
    if event == 'Visible':
        window['-CBOX-'].Update(visible=True)
        window['-CBOX-'].unhide_row()
    if event == 'Invisible':
        window['-CBOX-'].Update(visible=False)
        window['-CBOX-'].hide_row()
window.close()