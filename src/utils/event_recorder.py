import time
from collections import deque
import cv2
import os

class EventRecorder:
    #CLASE EXTRA QUE SIRVA PARA GESTIONAR EVENTOS DE LOS VIDEOS Y GRABE CONSTANTEMENTE
    #La idea es que esta clase tenga una grabacion constante (buffer) y que cada vez que entre input recuerde ese estado y capture esa aprte del video

    def __init__(self, pre_buffer_seconds=2, fps=30, folder="clips"):
        self.fps = fps
        self.pre_buffer_seconds = pre_buffer_seconds #Ajustamos cuantos segundos va a tener el buffer
        self.frame_buffer = deque(maxlen=int(pre_buffer_seconds * fps)) #Una cola que siempre mantiene una cantidad contante de frames 
        #Por ejemplo Siempre tenga 60 frames, si se pasa a 61 saca el 1er frame y asi..
        self.state = None  
        self.state_events = []  # Lista de tuplas: (start_time, end_time, estado)
        self.folder = folder
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
        print(f"Grabando estado {boton} desde {self.state_start_time:.2f}")

    def end_state(self):
        if self.state is None:
            return
        end_time = time.time()
        self.state_events.append((self.state_start_time, end_time, self.state))
        print(f"Estado {self.state} terminado a {end_time:.2f}")
        self.generate_clip(self.state_start_time, end_time, self.state)
        self.state = None


    def generate_clip(self, t_start, t_end, estado):
        # Se recorta del buffer y guardamos clip

        #Filtramos solo los framres que estan entre t_star y t_end  y de ahi solo tomamos los frames en si
        # de [(1.5, frame1), (1.6, frame2), (1.7, frame3), (1.8, frame4), (1.9, frame5)] pasamos a 
        # [frame2, frame3, frame4]
        frames_to_save = [f for t, f in self.frame_buffer if t_start <= t <= t_end]
        if not frames_to_save:
            return
        height, width = frames_to_save[0].shape[:2]
        filename = f"{estado}_{int(t_start)}_{int(t_end)}.mp4"
        path = os.path.join(self.folder, filename)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(path, fourcc, self.fps, (width, height))
        for f in frames_to_save:
            out.write(f)
        out.release()
        print(f"Clip guardado: {filename}")
