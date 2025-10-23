import random
import time


class IndefiniteRecording:
    def __init__(self, camera):
        self.camera = camera
        self.recorder = None
        self.is_recording = False
        self.current_gesture = None
        self.clip_start_time = None
        self.clip_duration = 0

    def start(self, gesture_name):
        print(f"Iniciando grabación para estado: {gesture_name}")
        self.current_gesture = gesture_name
        self.is_recording = False 
        self.clip_start_time = None

    def stop(self):
        if self.is_recording and self.recorder:
            print(f"Terminando clip para: {self.current_gesture}")
            self.recorder.end_state()
            self.is_recording = False
        elif self.recorder:
            print(f"Deteniendo estrategia (sin clip activo)")

    def update(self):
        #EN CADA FRAME SE LLAMA A ESTA FUNCION
        if self.current_gesture is None or self.recorder is None:
            return
        
        now = time.time()
        
        #sI NO HAY CLIP, EMPEZAMOS UNO
        if not self.is_recording:
            self.clip_start_time = now
            self.clip_duration = random.uniform(2, 3)
            print(f" Iniciando nuevo clip de {self.clip_duration:.2f}s para: '{self.current_gesture}'")
            self.recorder.start_state(self.current_gesture)
            self.is_recording = True
        
        # Si se paso el clip, termianmos
        elif now - self.clip_start_time >= self.clip_duration:
            print(f"Clip completado después de {self.clip_duration:.2f}s para: '{self.current_gesture}'")
            self.recorder.end_state()
            self.is_recording = False 