import cv2
import time
import os
import threading

class Camera:

    def __init__(self):
        #Index donde esta ubcada la camara por defecto
        self.camera_index = 0 #Ojo si tenes 2 camaras conectadas (A futuro veo si añadimos via bluetooth)
        self.cap = None
        self.frames = []
        self.is_recording = False
        self.recording_start_time = 0


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
    
    def get_recording_progress(self):
        if self.is_recording:
            return time.time() - self.recording_start_time
        return 0
    
    def start_recording(self, duration, folder_path, filename_prefix):
        if self.is_recording:
            print("Ya se está grabando.")
            return

        self.is_recording = True
        self.recording_start_time = time.time()
        self.frames = []
        print(f"Grabando durante {duration} segundos...")

        def record_loop():
            end_time = time.time() + duration
            
            while self.is_recording and time.time() < end_time:
                ret, frame = self.cap.read()
                if ret:
                    self.frames.append(frame)
                else:
                    break
            
            self.is_recording = False
            actual_duration = time.time() - self.recording_start_time
            real_fps = len(self.frames) / actual_duration
            print(f"Grabación finalizada. Duración real: {actual_duration:.2f}s, Frames: {real_fps}")
            self.save_recording(self.frames, folder_path, filename_prefix, real_fps)

        threading.Thread(target=record_loop, daemon=True).start()
    
    def save_recording(self, frames, folder_path, filename_prefix, fps):
        if not frames:
            return False
        
        existing_videos = [f for f in os.listdir(folder_path) if f.startswith(filename_prefix) and f.endswith('.mp4')]
        next_number = len(existing_videos) + 1
        filename = f"{filename_prefix}_{next_number}.mp4"

        video_path = os.path.join(folder_path, f"{filename}")

        height, width = frames[0].shape[:2]

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        video_writer = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

        for frame in frames:
            video_writer.write(frame)
        
        video_writer.release()
        print(f"Video guardado como {filename} en {folder_path} ({len(frames)} frames)")
        return True