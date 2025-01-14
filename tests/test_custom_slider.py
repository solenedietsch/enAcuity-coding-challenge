import pytest
import PySimpleGUI as sg
from app.components.custom_slider import CustomSlider  # Import your custom slider class


@pytest.fixture
def fake_window():
    """Fixture to create a fake window with a CustomSlider for testing."""
    time_elapsed_text = sg.Text('', key='-TIME_ELAPSED-')
    time_remaining_text = sg.Text('', key='-TIME_REMAINING-')
    video_slider = CustomSlider('-SLIDER-', time_elapsed_text, time_remaining_text)

    layout = [[time_elapsed_text, video_slider, time_remaining_text]]

    window = sg.Window("Fake Window for Testing", layout, finalize=True)
    yield window  # Provide the window object to the test
    window.close()  # Ensure window is closed after test

def test_custom_slider_initialization():
    """
    Test to ensure default values and attributes.
    """
    elapsed_time_label = sg.Text("Elapsed")
    remaining_time_label = sg.Text("Remaining")
    slider = CustomSlider("slider_key", time_elapsed=elapsed_time_label, time_remaining=remaining_time_label)

    assert slider.nb_frames == 0
    assert slider.fps == 0.0
    assert slider.elapsed_time == elapsed_time_label
    assert slider.remaining_time == remaining_time_label

    assert slider.Key == "slider_key"
    assert slider.Range == (0, 100)
    assert slider.Orientation == 'h'

def test_get_video_duration_from_id():
    """
    Test check time formatting from frame ID.
    """
    slider = CustomSlider("slider_key")
    slider.fps = 30.0  # 30 FPS

    assert slider.get_video_duration_from_id(0) == "00:00:00"  # At frame 0
    assert slider.get_video_duration_from_id(90) == "00:00:03"  # 90 frames = 3 seconds
    assert slider.get_video_duration_from_id(3600 * 30) == "01:00:00"  # 1 hour worth of frames

def test_get_video_duration():
    """
    Test the total video duration.
    """
    slider = CustomSlider("slider_key")
    slider.fps = 60.0  # 60 FPS
    slider.nb_frames = 3600 * 60  # 1 hour worth of frames at 60 FPS

    assert slider.get_video_duration() == "01:00:00"

def test_get_elapsed_time():
    """
    Ensure you get the correct remaining time based on the current frame ID.
    """
    elapsed_label = sg.Text("Elapsed")
    remaining_label = sg.Text("Remaining")
    slider = CustomSlider("slider_key", time_elapsed=elapsed_label, time_remaining=remaining_label)

    slider.fps = 60.0  # 60 frames per second
    slider.nb_frames = 60 * 10  # 10 seconds worth of frames (600 frames)

    # Test case 1: At the start (frame 0)
    elapsed_time = slider.get_elapsed_time(0)
    assert elapsed_time == "00:00:00", "Elapsed time should be 0 seconds at the start."

    # Test case 2: Halfway point (frame 300)
    elapsed_time = slider.get_elapsed_time(300)
    assert elapsed_time == "00:00:05", "Elapsed time should be 5 seconds at halfway point."

    # Test case 3: End of video (frame 600)
    elapsed_time = slider.get_elapsed_time(600)
    assert elapsed_time == "00:00:10", "Elapsed time should be 10 seconds at the end."

    # Edge case 1: Negative frame ID
    elapsed_time = slider.get_elapsed_time(-10)
    assert elapsed_time == "00:00:00", "Elapsed time should be 0 seconds when frame ID is negative."

    # Edge case 2: Frame ID beyond nb_frames (e.g., 1000)
    elapsed_time = slider.get_elapsed_time(1000)
    assert elapsed_time == "00:00:10", "Elapsed time should be 0 seconds if frame ID exceeds nb_frames."


def test_get_remaining_time():
    """
    Ensure you get the correct remaining time based on the current frame ID.
    """
    elapsed_label = sg.Text("Elapsed")
    remaining_label = sg.Text("Remaining")
    slider = CustomSlider("slider_key", time_elapsed=elapsed_label, time_remaining=remaining_label)

    slider.fps = 60.0  # 60 frames per second
    slider.nb_frames = 60 * 10  # 10 seconds worth of frames (600 frames)

    # Test case 1: At the start (frame 0)
    remaining_time = slider.get_remaining_time(0)
    assert remaining_time == "00:00:10", "Remaining time should be 10 seconds at the start."

    # Test case 2: Halfway point (frame 300)
    remaining_time = slider.get_remaining_time(300)
    assert remaining_time == "00:00:05", "Remaining time should be 5 seconds at halfway point."

    # Test case 3: End of video (frame 600)
    remaining_time = slider.get_remaining_time(600)
    assert remaining_time == "00:00:00", "Remaining time should be 0 seconds at the end."

    # Edge case 1: Negative frame ID
    remaining_time = slider.get_remaining_time(-10)
    assert remaining_time == "00:00:00", "Remaining time should be 0 seconds when frame ID is negative."

    # Edge case 2: Frame ID beyond nb_frames (e.g., 1000)
    remaining_time = slider.get_remaining_time(1000)
    assert remaining_time == "00:00:00", "Remaining time should be 0 seconds if frame ID exceeds nb_frames."

def test_get_video_duration_zero_fps():
    """
    Tests fps=0.0 and negative frame IDs.
    """
    slider = CustomSlider("slider_key")
    slider.fps = 0.0  # FPS is zero
    slider.nb_frames = 100  # Arbitrary number of frames
    assert slider.get_video_duration_from_id(100) == "00:00:00"  # Should gracefully handle without crashing

    slider.fps = -1.0  # FPS is zero
    assert slider.get_video_duration_from_id(100) == "00:00:00"  # Should gracefully handle without crashing

def test_negative_frame_id():
    slider = CustomSlider("slider_key")
    slider.fps = 30.0
    slider.nb_frames = -1  # Arbitrary number of frames
    assert slider.get_video_duration_from_id(-1) == "00:00:00"  # Negative frame ID should return zero
