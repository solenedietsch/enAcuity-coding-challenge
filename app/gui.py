import cv2
import PySimpleGUI as sg

from app.components.video_player import VideoPlayer
from data.images.output import button_play, button_pause, button_next, button_previous
from app.components.video_loader import VideoLoader

def create_window():
    sg.theme('Black')
    button_color = sg.theme_background_color()

    layout = [
        [sg.Text('Select a video to play:', size=(17, 1)), sg.InputText(key='-FILE-', enable_events=True), sg.FileBrowse(target='-FILE-')],
        [sg.Image(key='-IMAGE-', size=(854, 480))],
        [sg.Button(image_data=button_previous, key= '-PREVIOUS-', border_width=0, button_color=button_color) ,
            sg.Button(image_data=button_play, key='-PLAY-', border_width=0, button_color=button_color),
            sg.Button(image_data=button_pause, key='-PAUSE-', border_width=0, button_color=button_color),
            sg.Button(image_data=button_next, key='-NEXT-', border_width=0, button_color=button_color)],
    ]
    window = sg.Window("EnAcuity Player", layout, element_justification='c')

    return window


class VideoPlayerApp:
    def __init__(self):
        self.window = create_window()
        self.video_loader = None
        self.video_player = None
        self.timeout = 0

        self.image_element = self.window['-IMAGE-']
        self.ret = False
        self.frame = None
    def launch_app(self):
        # Main loop
        while True:
            event, values = self.window.read(timeout=self.timeout)

            if event == sg.WIN_CLOSED:
                break

            elif event == '-FILE-':
                filename = values['-FILE-']
                self.video_loader = VideoLoader(filename)
                self.timeout = 1000 // self.video_loader.fps
                self.video_player = VideoPlayer(self.video_loader)

            elif event == '-PLAY-':
                self.video_player.play_video()

            elif event == '-PAUSE-':
                self.video_player.pause_video()

            elif event == '-NEXT-':
                self.video_player.next_frame()

            elif event == '-PREVIOUS-':
                self.video_player.previous_frame()



        self.window.close()

if __name__ == "__main__":
    app = VideoPlayerApp()
    app.launch_app()

