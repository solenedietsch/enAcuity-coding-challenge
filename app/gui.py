import os

import cv2
import PySimpleGUI as sg
from PySimpleGUI import Menu

from app.components.custom_slider import CustomSlider
from app.components.image_filter import ImageFilter, FILTER_LIST
from app.components.video_player import VideoPlayer
from data.images.output import button_play, button_pause, button_next, button_previous

VIDEO_FILENAME = os.path.join(os.getcwd(), "data/video01_cropped.mp4")


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
        self.frame = None
        self.ret = None
        self.is_filter_applied = False
        self.filtered_image : ImageFilter = ImageFilter(self.frame)

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
        self.ret, self.frame = self.video_player.video_file.read()
        self.update_image(self.ret, self.frame)

        self.timeout = 1000 // self.video_player.fps

    def create_window(self):
        sg.theme('Black')
        button_color = sg.theme_background_color()

        time_elapsed_text = sg.Text('', key='-TIME_ELAPSED-')
        time_remaining_text = sg.Text('', key='-TIME_REMAINING-')
        self.video_slider = CustomSlider('-SLIDER-', time_elapsed_text, time_remaining_text)

        layout = [
            [Menu([['File', ['Import', 'Exit']], ['Filter', ['!Gray', 'Object Detection']]],  k='-CUST MENUBAR-')],
            [sg.Image(key='-IMAGE-', size=(854, 480))],
            [time_elapsed_text, self.video_slider, time_remaining_text],
            [sg.Button(image_data=button_previous, key='-PREVIOUS-', border_width=0, button_color=button_color),
             sg.Button(image_data=button_play, key='-PLAY-', border_width=0, button_color=button_color),
             sg.Button(image_data=button_pause, key='-PAUSE-', border_width=0, button_color=button_color, disabled=True),
             sg.Button(image_data=button_next, key='-NEXT-', border_width=0, button_color=button_color)],
            [sg.Button('Apply filter_type - Press (F)', key='-FILTER-')]
        ]

        self.window = sg.Window("EnAcuity Player", layout, element_justification='c',
                                 return_keyboard_events=True, finalize=True)


    def update_image(self, ret=False, frame=None):
        if ret:
            if self.is_filter_applied:
                self.frame = self.filtered_image.update_filtered_image(frame)
            imgbytes = cv2.imencode('.ppm', self.frame)[1].tobytes()
            self.image_element.update(data=imgbytes)


    def launch_app(self):
        # Main loop
        while True:
            event, values = self.window.read(timeout=self.timeout)

            if event in (sg.WIN_CLOSED, 'Exit'):
                break

            elif event == 'Import':
                file = sg.popup_get_file('Choose your file', keep_on_top=True)
                self.update_filename(filename=file)

            elif event == '-PLAY-':
                self.video_player.play_video()
                self.window['-PLAY-'].update(disabled=True)
                self.window['-PAUSE-'].update(disabled=False)

            elif event == '-PAUSE-':
                self.video_player.pause_video()
                self.window['-PAUSE-'].update(disabled=True)
                self.window['-PLAY-'].update(disabled=False)

            elif event == ' ':
                if self.video_player.is_playing:
                    self.video_player.pause_video()
                    self.window['-PAUSE-'].update(disabled=True)
                    self.window['-PLAY-'].update(disabled=False)
                else:
                    self.video_player.play_video()
                    self.window['-PLAY-'].update(disabled=True)
                    self.window['-PAUSE-'].update(disabled=False)

            elif event == '-NEXT-':
                self.ret, self.frame = self.video_player.next_frame()
                self.update_image(self.ret, self.frame)
                # Update the time elapsed and remaining in the GUI
                self.video_slider.update_slider_time_labels(self.current_frame_id)


            elif event == '-PREVIOUS-':
                self.ret, self.frame = self.video_player.previous_frame()
                self.update_image(self.ret, self.frame)
                # Update the time elapsed and remaining in the GUI
                self.video_slider.update_slider_time_labels(self.current_frame_id)

            elif event == '-SLIDER-':
                # Get the frame id from the slider
                self.current_frame_id = int(values['-SLIDER-'])
                # Update the time elapsed and remaining in the GUI
                self.video_slider.update_slider_time_labels(self.current_frame_id)
                # Update the image shown
                self.ret, self.frame = self.video_player.set_current_frame_from_id(self.current_frame_id)
                self.update_image(self.ret, self.frame)

            elif event.lower() == 'f' or  event == '-FILTER-':
                self.is_filter_applied = not self.is_filter_applied
                self.ret, self.frame = self.video_player.set_current_frame_from_id(self.current_frame_id-1)
                self.update_image(self.ret, self.frame)

            elif event in ['Gray', 'Object Detection']:
                current_filter = event.lower().replace(' ', '_')

                menu_definition = [['File', ['Import', 'Exit']],
                                   ['Filter', ['Gray', 'Object Detection']]]

                if event == 'Gray':
                    menu_definition[1][1][0] = '!Gray'
                    menu_definition[1][1][1] = 'Object Detection'
                elif event == 'Object Detection':
                    menu_definition[1][1][0] = 'Gray'
                    menu_definition[1][1][1] = '!Object Detection'


                self.window['-CUST MENUBAR-'].update(menu_definition=menu_definition)
                self.filtered_image.set_filter_type(current_filter)
                self.ret, self.frame = self.video_player.set_current_frame_from_id(self.current_frame_id - 1)
                self.update_image(self.ret, self.frame)

            if self.video_player and self.video_player.is_playing:
                # Keep playing the video if the video player is playing
                self.ret, self.frame = self.video_player.keep_playing()
                # Update the image shown
                self.update_image(self.ret, self.frame)
                # Update the time elapsed and remaining in the GUI
                self.current_frame_id = self.video_player.get_current_frame_id()
                self.video_slider.update_slider_time_labels(self.current_frame_id)

        self.window.close()

if __name__ == "__main__":
    VIDEO_FILENAME = os.path.join(os.getcwd(), "../data/video01_cropped.mp4")
    app = VideoPlayerApp()
    app.launch_app()

