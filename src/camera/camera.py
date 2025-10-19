import cv2
import time
import os
import threading

class Camera:

    def __init__(self):
        #Index donde esta ubcada la camara por defecto
        self.camera_index = 0 #Ojo si tenes 2 camaras conectadas (A futuro veo si añadimos via bluetooth)
        self.cap = None
        self.is_savinf = False
        self.frames = []
        self.is_recording = False

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
    
    def start_recording(self, duration, folder_path, filename_prefix):
        if self.is_recording:
            print("Ya se está grabando.")
            return

        self.is_recording = True
        self.frames = []
        print(f"Grabando durante {duration} segundos...")

        def record_loop():
            target_frames = int(duration * 30)
            frames_captured = 0
            while self.is_recording and frames_captured < target_frames:
                ret, frame = self.cap.read()
                if ret:
                    self.frames.append(frame)
                    frames_captured += 1
                else:
                    break
            self.is_recording = False
            print("Grabación finalizada.")
            self.save_recording(self.frames, folder_path, filename_prefix)

        #Grabacion en 2do plano
        threading.Thread(target=record_loop, daemon=True).start()



        return self.frames
    
    def save_recording(self, frames, folder_path, filename_prefix):
        if not frames:
            return False
        
        existing_videos = [f for f in os.listdir(folder_path) if f.startswith(filename_prefix) and f.endswith('.mp4')]
        next_number = len(existing_videos) + 1
        filename = f"{filename_prefix}_{next_number}.mp4"

        video_path = os.path.join(folder_path, f"{filename}")

        height, width = frames[0].shape[:2]

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        fps = 30  
        out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

        for frame in frames:
            out.write(frame)
        
        out.release()
        print(f"Video guardado como {filename} en {folder_path} ({len(frames)} frames)")
        return True