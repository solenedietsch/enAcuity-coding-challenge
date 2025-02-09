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

        self.ret = False
        self.frame = None

        self.current_frame_id = self.get_current_frame_id()
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

    def set_current_frame_id(self, frame_id: float):
        self.current_frame_id = self.video_file.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        return self.current_frame_id

    def set_current_frame_from_frame_id(self, frame_id: float):
        # As the frame is updated using self.video_file.read() that increments the current frame id
        # Set it to the previous one to match the right frame id
        self.set_current_frame_id(frame_id - 1)
        self.ret, self.frame = self.video_file.read()

        return self.ret, self.frame

    def get_current_frame_id(self):
        self.current_frame_id = self.video_file.get(cv2.CAP_PROP_POS_FRAMES)
        return self.current_frame_id

    def set_previous_frame(self):
        # Get the current frame id when clicking on the previous button
        current_frame_id = self.get_current_frame_id()

        # The index must 2, as the frame id is set to -2, but displayed -1 with read.
        previous_frame_id = current_frame_id - 2

        # Set the current frame to the previous frame
        self.current_frame_id = previous_frame_id
        self.video_file.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame_id)

    def play_video(self):
        self.is_playing = True

    def pause_video(self):
        self.is_playing = False

    def __del__(self):
        self.video_file.release()
        cv2.destroyAllWindows()