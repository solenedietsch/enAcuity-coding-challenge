import cv2

from app.components.video_loader import VideoLoader


class VideoPlayer:
    def __init__(self, video_loader: VideoLoader):

        self.video_loader = video_loader
        self.current_frame_id = 0
        self.current_frame = self.set_current_frame()
        self.is_playing = False

    def read_frame(self, frame_id):
        self.video_loader.video_file.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ret, frame = self.video_loader.video_file.read()
        if not ret:
            raise ValueError("Error reading frame")
        return frame

    def set_current_frame(self):
        self.current_frame = self.video_loader.video_file.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame_id)
        return self.current_frame

    def next_frame(self):
        self.current_frame_id += 1
        self.current_frame = self.set_current_frame()
        return self.current_frame

    def previous_frame(self):
        self.current_frame_id -= 1
        self.current_frame = self.set_current_frame()
        return self.current_frame

    def play_video(self):
        self.is_playing = True

    def pause_video(self):
        self.is_playing = False