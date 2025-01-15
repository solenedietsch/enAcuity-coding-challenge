import cv2
from pymediainfo import MediaInfo

SUPPORTED_FORMATS = ['.mp4', '.avi', '.mov', '.mkv']

def is_video(filename:str):
    if filename.endswith(tuple(SUPPORTED_FORMATS)):
        return filename
    else:
        raise ValueError(f"Invalid video file format. Supported formats are: {', '.join(SUPPORTED_FORMATS)}")

class VideoPlayer:
    def __init__(self, filename: str):
        print(f"Loading video file: {filename}")
        self.filename = is_video(filename)

        self.video_file = cv2.VideoCapture(self.filename)

        # Get the metadata of the video file
        self.num_frames = self.get_nb_frames()
        self.fps = self.video_file.get(cv2.CAP_PROP_FPS)
        self.height = int(self.video_file.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.duration = self.num_frames / self.fps if self.fps > 0 else 0

        self.ret = False
        self.frame = None

        self.current_frame_id = 0
        self.current_frame = self.set_current_frame_id(self.current_frame_id)
        self.is_playing = False

    def get_nb_frames(self):
        """
        Get the number of frames in the video file using the MediaInfo library as it is more reliable than OpenCV
        """
        num_frames = 0
        media_info = MediaInfo.parse(self.filename)
        for track in media_info.tracks:
            if track.track_type == "Video":
                num_frames = int(track.frame_count)

        return num_frames

    def read_frame(self, frame_id):
        self.video_file.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        self.ret, self.frame = self.video_file.read()
        if not self.ret:
            raise ValueError("Error reading frame")
        return self.frame

    def keep_playing(self):
        if self.is_playing:
            self.ret, self.frame = self.video_file.read()

        return self.ret, self.frame

    def set_current_frame_id(self, frame_id: int):
        self.current_frame = self.video_file.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        return self.current_frame

    def set_current_frame_from_id(self, frame_id: int):
        self.set_current_frame_id(frame_id)
        self.ret, self.frame = self.video_file.read()
        return self.ret, self.frame

    def get_current_frame_id(self):
        self.current_frame = self.video_file.get(cv2.CAP_PROP_POS_FRAMES)
        return self.current_frame

    def next_frame(self):
        self.current_frame_id = self.video_file.get(cv2.CAP_PROP_POS_FRAMES)

        if self.current_frame_id < self.num_frames:
            self.ret, self.frame = self.video_file.read()

        return self.ret, self.frame

    def previous_frame(self):
        self.current_frame_id = self.video_file.get(cv2.CAP_PROP_POS_FRAMES)

        if self.current_frame_id > 0:
            self.current_frame_id -= 2
            self.video_file.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame_id)
            self.ret, self.frame = self.video_file.read()

        return self.ret, self.frame

    def play_video(self):
        self.is_playing = True

    def pause_video(self):
        self.is_playing = False

    def __del__(self):
        self.video_file.release()
        cv2.destroyAllWindows()