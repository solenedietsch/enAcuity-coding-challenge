import os

import cv2
import PySimpleGUI as sg

from app.components.custom_slider import CustomSlider
from app.components.video_player import VideoPlayer
from data.images.output import button_play, button_pause, button_next, button_previous

VIDEO_FILENAME = os.path.join(os.getcwd(), "../data/video01_cropped.mp4")


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
    window = sg.Window("EnAcuity Player", layout, element_justification='c', finalize=True)

    return window


class VideoPlayerApp:
    def __init__(self):
        self.window = create_window()
        self.video_slider = None

        self.video_player = None
        self.video_player = None
        self.timeout = 0
        self.image_element = self.window['-IMAGE-']

        self.current_frame_id = 0

        # Add a default video file
        self.filename = VIDEO_FILENAME
        self.update_filename(filename=self.filename)



    def update_filename(self, filename='', values=None):
        if filename:
            self.filename = filename
            print(f"Selected video file: {self.filename}")
        elif values:
            self.filename = values['-FILE-']
            print(f"Selected video file: {self.filename}")

        self.video_player = VideoPlayer(self.filename)

        # Set the slider range
        self.video_slider.nb_frames = self.video_player.num_frames
        self.video_slider.fps = self.video_player.fps

        # And its metrics accordingly
        self.video_slider.update(range=(0, self.video_player.num_frames))
        self.video_slider.update_slider_time_labels(self.current_frame_id)

        # Read the first frame
        self.current_frame_id = 0
        ret, frame = self.video_player.video_file.read()
        self.update_image(ret, frame)

        self.timeout = 1000 // self.video_player.fps

    def create_window(self):
    def update_image(self, ret=False, frame=None):
        if ret:
            imgbytes = cv2.imencode('.ppm', frame)[1].tobytes()
            self.image_element.update(data=imgbytes)


    def launch_app(self):
        # Main loop
        while True:
            event, values = self.window.read(timeout=self.timeout)

            if event == sg.WIN_CLOSED:
                break

            elif event == '-FILE-':
                self.update_filename(values=values)

            elif event == '-PLAY-':
                self.video_player.play_video()

            elif event == '-PAUSE-':
                self.video_player.pause_video()

            elif event == '-NEXT-':
                ret, frame = self.video_player.next_frame()
                self.update_image(ret, frame)

            elif event == '-PREVIOUS-':
                ret, frame = self.video_player.previous_frame()
                self.update_image(ret, frame)

            if self.video_player:
                ret, frame = self.video_player.keep_playing()
                self.update_image(ret, frame)


            if self.video_player:
                # Keep playing the video if the video player is playing
                ret, frame = self.video_player.keep_playing()
                # Update the image shown
                self.update_image(ret, frame)

        self.window.close()

if __name__ == "__main__":
    app = VideoPlayerApp()
    app.launch_app()

