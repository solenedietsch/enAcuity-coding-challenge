import os

import cv2
from datetime import datetime
import PySimpleGUI as sg
from PySimpleGUI import Menu

from app.components.custom_slider import CustomSlider
from app.components.image_filter import ImageFilter, FILTER_LIST
from app.components.video_player import VideoPlayer
from data.images.output import button_next, button_previous, play_button, pause_button

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

    def update_filename(self, filename=''):
        # Update the filename
        self.filename = filename

        # Set video player with the new video file
        self.video_player = VideoPlayer(self.filename)

        # Set the slider range
        # And its metrics accordingly
        self.video_slider.update(range=(0, self.video_player.num_frames))
        self.video_slider.update_slider_time_labels(self.current_frame_id)
        self.video_slider.update_metadata_from_video_player(self.video_player)

        # Read the first frame
        self.current_frame_id = 0
        self.update_image_element()

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
             sg.Button(image_data=play_button, key='-PLAY_PAUSE-', border_width=0, button_color=button_color),
             sg.Button(image_data=button_next, key='-NEXT-', border_width=0, button_color=button_color)],
            [sg.Button('Apply filter_type - Press (F)', key='-FILTER-')]
        ]

        self.window = sg.Window("EnAcuity Player", layout, element_justification='c',
                                 return_keyboard_events=True, finalize=True)


    def update_image_element(self, ret=None, frame=None):
        if ret is None and frame is None:
            # Keep playing the video if the video player is playing
            self.ret, self.frame = self.video_player.video_file.read()

        # Check if the frame was valid
        if self.ret:
            # Apply the selected filter if necessary
            if self.is_filter_applied:
                self.frame = self.filtered_image.update_filtered_image(self.frame)

            # Encode the image
            imgbytes = cv2.imencode('.ppm', self.frame)[1].tobytes()
            # And update the window image element
            self.image_element.update(data=imgbytes)

    def save_current_frame(self):
        # Make sure the output folder exist or creates its is not created
        os.makedirs('../output', exist_ok=True)
        datatime_f = datetime.now().strftime('%Y_%m_%d-%H_%M_%S_%f')
        cv2.imwrite(f'../output/frame-{datatime_f}.png', self.frame)

    def launch_app(self):
        # Main loop
        while True:
            event, values = self.window.read(timeout=self.timeout)

            if event in (sg.WIN_CLOSED, 'Exit'):
                break

            elif event == 'Import':
                file = sg.popup_get_file('Choose your file', keep_on_top=True)
                self.update_filename(filename=file)

            elif event in ['-PLAY_PAUSE-', ' ']:
                self.video_player.is_playing = not self.video_player.is_playing
                button_image = pause_button if self.video_player.is_playing else play_button
                self.window['-PLAY_PAUSE-'].update(image_data=button_image)

            elif event == '-NEXT-':
                # Update the time elapsed and remaining in the GUI
                self.video_slider.update_slider_time_labels(self.current_frame_id)

                # Set the next image
                self.update_image_element()

            elif event == '-PREVIOUS-':
                # Update the time elapsed and remaining in the GUI
                self.video_slider.update_slider_time_labels(self.current_frame_id)
                # Update the image accordingly
                self.update_image_element()

            elif event == '-SLIDER-':
                # Get the frame id from the slider
                self.current_frame_id = int(values['-SLIDER-'])
                # Update the time elapsed and remaining in the GUI
                self.video_slider.update_slider_time_labels(self.current_frame_id)
                # Update the image shown
                # Get the new frame and update the window image element
                self.update_image_element()

            elif event.lower() == 'f' or  event == '-FILTER-':
                self.is_filter_applied = not self.is_filter_applied
                self.ret, self.frame = self.video_player.set_current_frame_from_frame_id(self.current_frame_id)
                self.update_image_element(self.ret, self.frame)

            elif event.lower() == 's' or  event == 'Save':
                self.save_current_frame()

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
                self.ret, self.frame = self.video_player.set_current_frame_from_frame_id(self.current_frame_id)
                self.update_image_element(self.ret, self.frame)

            elif self.video_player and self.video_player.is_playing:
                # Update the image shown
                self.update_image_element()

                # Update the time elapsed and remaining in the GUI
                self.current_frame_id = self.video_player.get_current_frame_id()
                self.video_slider.update_slider_time_labels(self.current_frame_id)

        self.window.close()

if __name__ == "__main__":
    VIDEO_FILENAME = os.path.join(os.getcwd(), "../data/video01_cropped.mp4")
    app = VideoPlayerApp()
    app.launch_app()

