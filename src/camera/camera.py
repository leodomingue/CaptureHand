import cv2
import time
import os

class Camera:

    def __init__(self):
        #Index donde esta ubcada la camara por defecto
        self.camera_index = 0 #Ojo si tenes 2 camaras conectadas (A futuro veo si añadimos via bluetooth)
        self.cap = None
        self.is_savinf = False
        self.frames = []

    def initialize_camera(self):
        self.cap = cv2.VideoCapture(self.camera_index) #Establece una conexion cone la camara 
        if not self.cap.isOpened():
            raise Exception("No se pudo abrir la cámara")
        return True
    
    def get_preview_frame(self):
        if self.cap and self.cap.isOpened():
            valid_lecture, frame = self.cap.read() #Devuelve un bool que indica la lectura y fotograma
            if valid_lecture:
                return frame
        return None