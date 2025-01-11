import PySimpleGUI as sg
from data.images.output import button_play, button_pause, button_next, button_previous

def create_window():
    layout = [
        [sg.Button(image_data=button_previous, key= '-PREVIOUS-', border_width=0) ,
            sg.Button(image_data=button_play, key='-PLAY-', border_width=0),
            sg.Button(image_data=button_pause, key='-PAUSE-', border_width=0),
            sg.Button(image_data=button_next, key='-NEXT-', border_width=0)],
    ]
    window = sg.Window("EnAcuity Player", layout)

    return window

def launch_app():
    window = create_window()

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

    window.close()

if __name__ == "__main__":
    launch_app()

