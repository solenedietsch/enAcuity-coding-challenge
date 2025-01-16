import os

import cv2
from datetime import datetime
import PySimpleGUI as sg
from PySimpleGUI import Menu

from app.components.custom_slider import CustomSlider
from app.components.image_filter import ImageFilter
from app.components.video_player import VideoPlayer
from images.output import button_next, button_previous, play_button, pause_button

VIDEO_FILENAME = os.path.join(os.getcwd(), "data/video01_cropped.mp4")


class VideoPlayerApp:
    def __init__(self):
        self.window: sg.Window|None = None
        self.video_slider: CustomSlider|None = None

        # Build the window from layout
        self.create_window()

        self.timeout: int = 0

        self.video_player = None
        self.image_element: sg.Image = self.window['-IMAGE-']
        self.current_frame_id: int = 0
        self.frame = None
        self.ret: bool = False
        self.is_filter_applied: bool = False
        self.filtered_image : ImageFilter = ImageFilter(self.frame)

        # Load a default video file
        self.filename: str = VIDEO_FILENAME
        self.update_filename(filename=self.filename)

    def update_filename(self, filename: str=''):
        """
        Update the filename and the video player using the new video file.
        :param filename: the new video filepath.
        :return:
        """
        # Update the filename
        self.filename = filename

        # Set video player with the new video file
        self.video_player = VideoPlayer(self.filename)

        # Set the slider range
        self.video_slider.update_metadata_from_video_player(self.video_player)

        # Read the first frame
        self.update_image_element()

        # Update the slider accordingly
        self.update_slider_from_current_id()

        # Set the GUI timeout
        self.timeout = 1000 // self.video_player.fps

    def create_window(self):
        # Set the theme
        sg.theme('Black2')
        button_color = sg.theme_background_color()

        # Create the custom slider
        time_elapsed_text = sg.Text('', key='-TIME_ELAPSED-')
        time_remaining_text = sg.Text('', key='-TIME_REMAINING-')
        self.video_slider = CustomSlider('-SLIDER-', time_elapsed_text, time_remaining_text)

        # Build the layout
        layout = [
            [Menu([['File', ['Import', 'Save', 'Exit']],
                   ['Filter', ['!Gray', 'Object Detection', 'Detect edges']]],  k='-CUST MENUBAR-',
                  disabled_text_color='red')],
            [sg.Image(key='-IMAGE-', size=(854, 480))],
            [time_elapsed_text, self.video_slider, time_remaining_text],
            [sg.Button(image_data=button_previous, key='-PREVIOUS-', border_width=0, button_color=button_color),
             sg.Button(image_data=play_button, key='-PLAY_PAUSE-', border_width=0, button_color=button_color),
             sg.Button(image_data=button_next, key='-NEXT-', border_width=0, button_color=button_color)],
            [sg.Button('Apply filter_type - Press (F)', key='-FILTER-')]
        ]

        # Finally, generate the window
        self.window = sg.Window("EnAcuity Player", layout, element_justification='c',
                                 return_keyboard_events=True, finalize=True)


    def update_image_element(self, ret=None, frame=None):
        """
        Update the image element with the current frame.

        If no frame is provided, the current frame is read from the video player.
        In case, the filter is applied; the filtered image is displayed instead.
        :param ret: boolean indicating if the frame was read successfully.
        :param frame: the frame to be displayed.
        :return:
        """
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

    def update_slider_from_current_id(self):
        """
        Update the slider value from the current frame id.

        Also update the time labels in the GUI.
        :return:
        """
        self.current_frame_id = self.video_player.get_current_frame_id()

        # Update the slider value
        self.video_slider.update(self.current_frame_id)
        self.video_slider.update_slider_time_labels(self.current_frame_id)

    def update_current_filter(self, event: str):
        """
        Update the current filter applied to the image.

        Also update the layout, to disable the selected filter.

        :param event: the menu event that triggered the filter change.
        :return:
        """
        current_filter = event.lower().replace(' ', '_')

        menu_definition = [['File', ['Import', 'Exit']],
                           ['Filter', ['Gray', 'Object Detection', 'Detect edges']]]

        # Highlight the selected filter
        filters = ['Gray', 'Object Detection', 'Detect edges']
        menu_definition[1][1] = [f'!{filter}' if filter == event else filter for filter in filters]

        self.window['-CUST MENUBAR-'].update(menu_definition=menu_definition)
        self.filtered_image.set_filter_type(current_filter)
        self.ret, self.frame = self.video_player.set_current_frame_from_frame_id(self.current_frame_id)
        self.update_image_element(self.ret, self.frame)

    def save_current_frame(self):
        # Make sure the output folder exist or creates its is not created
        os.makedirs('output', exist_ok=True)
        datatime_f = datetime.now().strftime('%Y_%m_%d-%H_%M_%S_%f')
        cv2.imwrite(f'output/frame_{current_frame_id}-{datatime_f}.png', self.frame)

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
                # Set the next image
                self.update_image_element()
                # Update the slider value
                self.update_slider_from_current_id()

            elif event == '-PREVIOUS-':
                # Set the current frame id to the previous frame
                self.video_player.set_previous_frame()
                # Update the image accordingly
                self.update_image_element()
                # Update the gui component such as the slider
                self.update_slider_from_current_id()

            elif event == '-SLIDER-':
                # Setting the slider id to -1 as the next frame is shown
                current_frame_id = int(values['-SLIDER-'])
                # And update the displayed frame
                self.video_player.set_current_frame_id(current_frame_id)
                # Get the new frame and update the window image element
                self.update_image_element()
                # Update the slider accordingly
                self.update_slider_from_current_id()

            elif event.lower() == 'f' or  event == '-FILTER-':
                self.is_filter_applied = not self.is_filter_applied
                self.ret, self.frame = self.video_player.set_current_frame_from_frame_id(self.current_frame_id)
                self.update_image_element(self.ret, self.frame)

            elif event.lower() == 's' or  event == 'Save':
                self.save_current_frame()

            elif event in ['Gray', 'Object Detection', 'Detect edges']:
                self.update_current_filter(event)

            elif self.video_player and self.video_player.is_playing:
                # Update the image shown
                self.update_image_element()

                # Update the time elapsed and remaining in the GUI
                self.update_slider_from_current_id()

        self.window.close()

if __name__ == "__main__":
    VIDEO_FILENAME = os.path.join(os.getcwd(), "../data/video01_cropped.mp4")
    app = VideoPlayerApp()
    app.launch_app()

