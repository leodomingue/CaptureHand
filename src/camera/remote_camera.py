from .camera import Camera
import cv2

class RemoteCamera(Camera):
   
    def __init__(self, url):
        super().__init__()
        self.url = url

    def initialize_camera(self):
        self.cap = cv2.VideoCapture(self.url)
        if not self.cap.isOpened():
            raise Exception(f"No se pudo abrir la cámara remota ({self.url})")
        print(f"Cámara remota inicializada: {self.url}")
        self.get_preview_frame()
        return True