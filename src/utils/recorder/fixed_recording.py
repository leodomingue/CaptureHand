import os
from .recording_strategy import RecordingStrategy

class FixedRecording(RecordingStrategy):
    def __init__(self, camera, action_section, duration=6):
        self.camera = camera
        self.action_section = action_section
        self.duration = duration

    def start(self, gesture_name: str):
        folder = os.path.join("gesture_data", gesture_name)
        print(f"Grabando '{gesture_name}' durante {self.duration}s")
        self.action_section.start_action_sequence()
        self.camera.start_recording(self.duration, folder, gesture_name)

    def stop(self):
        pass