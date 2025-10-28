
import time

from abc import ABC, abstractmethod

class Camera(ABC):

    def __init__(self):
        #Index donde esta ubcada la camara por defecto
        self.camera_index = 0 
        self.cap = None
        self.frames = []
        self.is_recording = False
        self.recording_start_time = 0
        self.real_fps = 20.0 
        self.fps_calculated = False



    @abstractmethod
    def initialize_camera(self):
        pass

    
    def get_preview_frame(self):
        if self.cap and self.cap.isOpened():
            valid_lecture, frame = self.cap.read() #Devuelve un bool que indica la lectura y fotograma
            if valid_lecture:
                return frame
        return None
    
    def get_recording_progress(self):
        if self.is_recording:
            return time.time() - self.recording_start_time
        return 0
    
