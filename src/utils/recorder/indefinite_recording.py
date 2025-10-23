from src.utils.event_recorder import EventRecorder
from .recording_strategy import RecordingStrategy
import os

class IndefiniteRecording(RecordingStrategy):
    def __init__(self, camera):
        self.camera = camera
        self.recorder = EventRecorder(pre_buffer_seconds=2, fps=int(self.camera.real_fps))
        self.is_recording = False
        self.current_gesture = None

    def start(self, gesture_name):
        if self.is_recording:
            self.stop()
        print(f"Grabación indefinida iniciada para '{gesture_name}'")
        self.current_gesture = gesture_name
        self.is_recording = True

    def stop(self):
        if not self.is_recording:
            return
        print(f"Grabación terminada para '{self.current_gesture}'")
        folder = os.path.join("clips", self.current_gesture)
        self.is_recording = False
        self.current_gesture = None
    