from datetime import datetime
import time
from collections import deque
import cv2
import os


class EventRecorder:
    # CLASE EXTRA QUE SIRVA PARA GESTIONAR EVENTOS DE LOS VIDEOS Y GRABE CONSTANTEMENTE
    # La idea es que esta clase tenga una grabacion constante (buffer) y que cada vez que entre input recuerde ese estado y capture esa aprte del video
    
    def __init__(self, pre_buffer_seconds=3, fps=30, camera_type="local"):
        self.fps = fps
        self.pre_buffer_seconds = pre_buffer_seconds  # Ajustamos cuantos segundos va a tener el buffer
        self.frame_buffer = deque(maxlen=int(pre_buffer_seconds * fps))  # Una cola que siempre mantiene una cantidad contante de frames
        # Por ejemplo Siempre tenga 30 frames, si se pasa a 61 saca el 1er frame y asi..
        self.state = None
        self.state_events = []  # Lista de tuplas: (start_time, end_time, estado)
        self.camera_type = camera_type

        self.clip_counters = {}
        self.folder = os.path.join("clips", camera_type)
        os.makedirs(self.folder, exist_ok=True)

    def add_frame(self, frame):
        t = time.time()
        self.frame_buffer.append((t, frame))

    def start_state(self, boton):
        if self.state == boton:
            return
        
        self.end_state()
        self.state = boton
        self.state_start_time = time.time()
        time_converted= datetime.fromtimestamp(self.state_start_time).strftime('%H:%M:%S')
        print(f"Grabando estado {boton} desde {time_converted}")

    def end_state(self):
        if self.state is None:
            return
        
        end_time = time.time()
        self.state_events.append((self.state_start_time, end_time, self.state))
        time_converted= datetime.fromtimestamp(end_time).strftime('%H:%M:%S')
        print(f"Estado {self.state} terminado a {time_converted}")
        actual_start_time = max(self.state_start_time - 0.5, 0)  # 0.5 segundos antes
        actual_duration = end_time - actual_start_time

        current_state = self.state
        self.state = None
        
        self.generate_clip(actual_duration, current_state)

    def generate_clip(self, duration, state):
        # Se recorta del buffer y guardamos clip
        # Filtramos solo los framres que estan entre t_star y t_end y de ahi solo tomamos los frames en si
        # de [(1.5, frame1), (1.6, frame2), (1.7, frame3), (1.8, frame4), (1.9, frame5)] pasamos a
        # [frame2, frame3, frame4]

        button_folder = os.path.join(self.folder, state.split("_")[0])
        os.makedirs(button_folder, exist_ok=True)

        num_frames = int(duration * self.fps)
        all_frames_with_timestamps = list(self.frame_buffer)
        
        # Tomamos los últimos num_frames frames del buffer
        frames_to_save = [frame for t, frame in all_frames_with_timestamps[-num_frames:]]
        
        if not frames_to_save:
            return
        
        if state not in self.clip_counters:
            existing_videos = [f for f in os.listdir(button_folder) if f.startswith(f"stick_{state}_") and f.endswith('.mp4')]
            max_number = 0
            for filename in existing_videos:
                try:
                    number_part = filename.replace(f"stick_{state}_", "").replace(".mp4", "")
                    number = int(number_part)
                    if number > max_number:
                        max_number = number
                except ValueError:
                    continue
            
            #inicializamos el contador con el máximo número encontrado + 1
            self.clip_counters[state] = max_number + 1
        else:
            #si ya existe, simplemente incrementamos
            self.clip_counters[state] += 1
        
        next_number = self.clip_counters[state]

        height, width = frames_to_save[0].shape[:2]
        filename = f"stick_{state}_{next_number}.mp4"
        path = os.path.join(self.folder, filename)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(path, fourcc, self.fps, (width, height))
        
        for f in frames_to_save:
            out.write(f)
        
        out.release()
        print(f"Clip guardado: {filename}")
