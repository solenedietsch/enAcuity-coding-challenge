import os

import cv2
import PySimpleGUI as sg

from app.components.custom_slider import CustomSlider
from app.components.video_player import VideoPlayer
from data.images.output import button_play, button_pause, button_next, button_previous

VIDEO_FILENAME = os.path.join(os.getcwd(), "../data/video01_cropped.mp4")

class VideoPlayerApp:
    def __init__(self):
        self.window= None
        self.video_slider = None

        # Build the window from layout
        self.create_window()

        self.timeout = 0

        self.video_player = None
        self.image_element = self.window['-IMAGE-']
        self.current_frame_id = 0

        # Add a default video file
        self.filename = VIDEO_FILENAME
        self.update_filename(filename=self.filename)

    def update_filename(self, filename='', values=None):
        if filename:
            self.filename = filename
        elif values:
            self.filename = values['-FILE-']

        # Set video player with the new video file
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
        sg.theme('Black')
        button_color = sg.theme_background_color()

        time_elapsed_text = sg.Text('', key='-TIME_ELAPSED-')
        time_remaining_text = sg.Text('', key='-TIME_REMAINING-')
        self.video_slider = CustomSlider('-SLIDER-', time_elapsed_text, time_remaining_text)

        layout = [
            [sg.Text('Select a video to play:', size=(17, 1)), sg.InputText(key='-FILE-', enable_events=True),
             sg.FileBrowse(target='-FILE-')],
            [sg.Image(key='-IMAGE-', size=(854, 480))],
            [time_elapsed_text, self.video_slider, time_remaining_text],
            [sg.Button(image_data=button_previous, key='-PREVIOUS-', border_width=0, button_color=button_color),
             sg.Button(image_data=button_play, key='-PLAY-', border_width=0, button_color=button_color),
             sg.Button(image_data=button_pause, key='-PAUSE-', border_width=0, button_color=button_color, disabled=True),
             sg.Button(image_data=button_next, key='-NEXT-', border_width=0, button_color=button_color)],
        ]

        self.window = sg.Window("EnAcuity Player", layout, element_justification='c', finalize=True)


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
                self.window['-PLAY-'].update(disabled=True)
                self.window['-PAUSE-'].update(disabled=False)

            elif event == '-PAUSE-':
                self.video_player.pause_video()
                self.window['-PAUSE-'].update(disabled=True)
                self.window['-PLAY-'].update(disabled=False)

            elif event == '-NEXT-':
                ret, frame = self.video_player.next_frame()
                self.update_image(ret, frame)

            elif event == '-PREVIOUS-':
                ret, frame = self.video_player.previous_frame()
                self.update_image(ret, frame)

            elif event == '-SLIDER-':
                # Get the frame id from the slider
                self.current_frame_id = int(values['-SLIDER-'])
                # Update the time elapsed and remaining in the GUI
                self.video_slider.update_slider_time_labels(self.current_frame_id)
                # Update the image shown
                ret, frame = self.video_player.set_current_frame_from_id(self.current_frame_id)
                self.update_image(ret, frame)


            if self.video_player:
                # Keep playing the video if the video player is playing
                ret, frame = self.video_player.keep_playing()
                # Update the image shown
                self.update_image(ret, frame)
                # Update the time elapsed and remaining in the GUI
                self.current_frame_id = self.video_player.get_current_frame_id()
                self.video_slider.update_slider_time_labels(self.current_frame_id)

        self.window.close()

if __name__ == "__main__":
    app = VideoPlayerApp()
    app.launch_app()

