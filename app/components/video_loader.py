import cv2

SUPPORTED_FORMATS = ['.mp4', '.avi', '.mov', '.mkv']

def is_video(filename:str):
    ext = filename[filename.rfind('.'):]
    if ext in SUPPORTED_FORMATS:
        return filename
    else:
        raise ValueError(f"Invalid video file format. Supported formats are: {', '.join(SUPPORTED_FORMATS)}")

class VideoLoader:
    def __init__(self, filename):
        print(f"Loading video file: {filename}")

        self.filename = is_video(filename)
        self.video_file = cv2.VideoCapture(self.filename)
        self.num_frames = self.video_file.get(cv2.CAP_PROP_FRAME_COUNT)
        self.fps = self.video_file.get(cv2.CAP_PROP_FPS)
        self.height = int(self.video_file.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.duration = self.num_frames / self.fps if self.fps > 0 else 0

    def __del__(self):
        self.video_file.release()
        cv2.destroyAllWindows()
