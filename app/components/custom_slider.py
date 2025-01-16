from PySimpleGUI import Slider, Text
from datetime import timedelta

from app.components.video_player import VideoPlayer


class CustomSlider(Slider):
    def __init__(self, slider_key: str, time_elapsed: Text = '', time_remaining: Text = ''):
        super().__init__(range=(1, 100), orientation='h', size=(75, 10), key=slider_key,
                         disable_number_display=False, enable_events=True)

        self.nb_frames: int = 0
        self.fps: float = 0.0
        self.elapsed_time: Text = time_elapsed
        self.remaining_time: Text = time_remaining

    def update_metadata_from_video_player(self, video_player: VideoPlayer):
        """
        Update the metadata of the slider using the metadata from the video player.
            This method retrieves the number of frames and the frames-per-second (FPS)
        from the given VideoPlayer instance and updates the slider's metadata accordingly.

        Parameters:
            video_player (VideoPlayer):
                An instance of the VideoPlayer class containing metadata such as
                the total number of frames (`num_frames`) and frames-per-second (`fps`).

        Returns:
            None
        """

        self.set_nb_frames(video_player.num_frames)
        self.set_fps(video_player.fps)

    def set_nb_frames(self, nb_frames: int) -> None:
        """
        Set the number of frames in the video
        :param nb_frames: The number of frames in the video
        :return:
        """
        self.nb_frames = nb_frames
        # Update the slider range, the range is from 0 to the number of frames - 1
        self.update(range=(1, self.nb_frames))

    def set_fps(self, fps: float) -> None:
        self.fps = fps

    def get_video_duration_from_id(self, frame_id: int) -> str:
        # Check if the FPS and the frame id are valid
        if self.fps <= 0 or frame_id < 0:
            return "00:00:00"

        # Calculate total seconds according to the current frame id and the FPS
        total_seconds = frame_id/self.fps

        # Convert seconds to timedelta object
        time_passed = timedelta(seconds=total_seconds)

        # Format as HH:MM:SS
        hours, remainder = divmod(time_passed.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def get_video_duration(self) -> str:
        return self.get_video_duration_from_id(self.nb_frames)

    def get_remaining_time(self, frame_id: int) -> str:
        if frame_id < 0 or frame_id > self.nb_frames:
            return "00:00:00"

        remaining_frames = self.nb_frames - frame_id
        return self.get_video_duration_from_id(remaining_frames)

    def get_elapsed_time(self, frame_id: int) -> str:
        if frame_id > self.nb_frames:
            return self.get_video_duration()

        return self.get_video_duration_from_id(frame_id)

    def update_remaining_time_text(self, frame_id: int) -> None:
        remaining_time = self.get_remaining_time(frame_id)
        self.remaining_time.update(remaining_time)

    def update_elapsed_time_text(self, frame_id: int) -> None:
        elapsed_time = self.get_elapsed_time(frame_id)
        self.elapsed_time.update(elapsed_time)

    def update_slider_time_labels(self, frame_id: int) -> None:
        self.update_remaining_time_text(frame_id)
        self.update_elapsed_time_text(frame_id)

