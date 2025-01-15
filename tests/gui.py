import os


import PySimpleGUI as sg
from PySimpleGUI import Menu
from gradio.themes.builder_app import current_theme
from torchgen.api.types import layoutT

VIDEO_FILENAME = os.path.join(os.getcwd(), "data/video01_cropped.mp4")


def create_window():
    current_theme = sg.theme('Topanga')
    current_theme = sg.theme_use_custom_titlebar()

    menu = Menu([['File', ['Import', 'Exit']], ['Filter', ['!Gray', 'Object Detection']]], k='-CUST MENUBAR-')
    menu.DisabledButtonColor = 'black'

    layout = [[menu]]

    window = sg.Window("EnAcuity Player", layout, element_justification='c', return_keyboard_events=True, finalize=True)

    return window

if __name__ == '__main__':
    window = create_window()
    # Main loop
    while True:
        event, values = window.read(timeout=10)

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

