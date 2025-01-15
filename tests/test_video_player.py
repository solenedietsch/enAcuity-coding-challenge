import pytest
import PySimpleGUI as sg

from app.components.video_player import VideoPlayer

@pytest.fixture
def video_player():
    video_player = VideoPlayer("../data/video01_cropped.mp4")
    yield video_player

def test_video_player_initialisation(video_player):
    assert video_player.filename == "../data/video01_cropped.mp4"
    assert video_player.current_frame_id == 1

def test_get_nb_frames(video_player):
    assert 2375 == video_player.get_nb_frames()

def test_set_current_frame_from_frame_id(video_player):
    frame_id = 0
    video_player.set_current_frame_from_frame_id(frame_id)
    assert frame_id == video_player.get_current_frame_id()
