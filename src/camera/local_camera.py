from .camera import Camera
import cv2
import time
import os
import threading

class LocalCamera(Camera):
   #Camra mediante usb o webcam integrada

    def __init__(self):
        super().__init__()
        self.index = 0

    def initialize_camera(self):
        self.cap = cv2.VideoCapture(self.index)
        if not self.cap.isOpened():
            raise Exception(f"No se pudo abrir la cámara local")
        print(f"Cámara local inicializada")
        self.get_preview_frame()
        return True
    

    def start_recording(self, duration, folder_path, filename_prefix):
        if self.is_recording:
            print("Ya se está grabando.")
            return

        self.is_recording = True
        self.recording_start_time = time.time()
        print(f"Grabando durante {duration} segundos con FPS: {self.real_fps:.2f}...")

        def record_loop():

            # Preparamos la ruta con el archivo a guardar
            existing_videos = [f for f in os.listdir(folder_path) 
                            if f.startswith(filename_prefix) and f.endswith('.mp4')]
            next_number = len(existing_videos) + 1
            filename = f"{filename_prefix}_{next_number}.mp4"
            video_path = os.path.join(folder_path, filename)

            #vemos las dimensiones y vemos si se graba correctamente
            ret, first_frame = self.cap.read()
            if not ret:
                self.is_recording = False
                return

            height, width = first_frame.shape[:2]

            #El programa para grabar
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter(video_path, fourcc, self.real_fps, (width, height))

            #Calculamos la cantidad de frames a grabar según los FPS reales y la duración
            total_frames_to_record = int(round(duration * self.real_fps))
            frame_count = 0

            while self.is_recording and frame_count < total_frames_to_record:
                ret, frame = self.cap.read()
                if ret:
                    video_writer.write(frame)
                    frame_count += 1
                else:
                    break

            #Liberamos los recursos
            video_writer.release()
            self.is_recording = False

            print(f"Grabación finalizada: {filename}")

        #Lo hacemos en otro hilo
        threading.Thread(target=record_loop, daemon=True).start()

