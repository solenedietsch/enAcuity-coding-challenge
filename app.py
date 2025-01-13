import gradio as gr
from app.gui import VideoPlayerApp

if __name__ == "__main__":
    app = VideoPlayerApp()
    app.launch_app()
