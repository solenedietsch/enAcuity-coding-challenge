from PySimpleGUI import Slider, Text, RELIEF_RAISED
from datetime import timedelta

class CustomSlider(Slider):
    def __init__(self, slider_key: str, time_elapsed: Text = '', time_remaining: Text = ''):
        super().__init__(range=(0, 100), orientation='h', size=(75, 10), key=slider_key,
                         disable_number_display =True, enable_events=True)
        self.nb_frames = 0
        self.fps = 0
        self.elapsed_time = time_elapsed
        self.remaining_time = time_remaining

    def get_nb_frames(self, nb_frames: int) -> None:
        self.nb_frames = nb_frames
        self.update(range=(0, nb_frames))

    def get_video_duration_from_id(self, frame_id: int) -> str:
        # Calculate total seconds
        total_seconds = frame_id/self.fps

        # Convert seconds to timedelta object
        time_passed = timedelta(seconds=total_seconds)

        # Format as HH:MM:SS
        hours, remainder = divmod(time_passed.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def get_video_duration(self) -> str:
        return self.get_video_duration_from_id(self.nb_frames)

    def update_remaining_time(self, frame_id: int) -> None:
        remaining_frames = self.nb_frames - frame_id
        self.remaining_time.update(self.get_video_duration_from_id(remaining_frames))

    def update_elapsed_time(self, frame_id: int) -> None:
        self.elapsed_time.update(self.get_video_duration_from_id(frame_id))

    def update_slider_time_labels(self, frame_id: int) -> None:
        """
        Updates the elapsed time and remaining time labels around the slider.

        This function synchronises the displayed time labels based on the current frame ID,
        updating the elapsed time (to the left of the slider) and remaining time (to the right).

        :param frame_id: int - The current frame ID indicating the position in the video.
        :return: :param
        """

        self.update_remaining_time(frame_id)
        self.update_elapsed_time(frame_id)

