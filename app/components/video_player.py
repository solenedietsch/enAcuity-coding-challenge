import cv2

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
        self.num_frames = self.video_file.get(cv2.CAP_PROP_FRAME_COUNT)
        self.fps = self.video_file.get(cv2.CAP_PROP_FPS)
        self.height = int(self.video_file.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.duration = self.num_frames / self.fps if self.fps > 0 else 0

        self.ret = False
        self.frame = None

        self.current_frame_id = 0
        self.current_frame = self.set_current_frame()
        self.is_playing = False

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

    def set_current_frame(self):
        self.current_frame = self.video_file.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame_id)
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