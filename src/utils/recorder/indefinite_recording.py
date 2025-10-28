import random
import time


class IndefiniteRecording:
    def __init__(self, cameras):
        self.recorders = cameras
        self.is_recording = False
        self.current_gesture = None
        self.clip_start_time = None
        self.max_total_duration = None

    def start(self, gesture_name):
        print(f"Iniciando grabación para estado: {gesture_name}")
        self.current_gesture = gesture_name
        self.is_recording = True 
        self.clip_start_time = time.time()
        self.max_total_duration = random.uniform(2, 3)
        for recorder in self.recorders:
            if recorder:
                recorder.start_state(self.current_gesture)

    def stop(self):
        if self.is_recording:
            for recorder in self.recorders:
                if recorder:
                    recorder.end_state()
                    print(f"Terminando clip para: {self.current_gesture}")

        self.is_recording = False
        self.current_gesture = None
        self.clip_start_time = None
        self.max_total_duration = None

    def update(self):
        if not self.is_recording or not self.recorders:
            return False
        
        elapsed = time.time() - self.clip_start_time
        if elapsed >= self.max_total_duration:
            print(f"Tiempo máximo alcanzado ({self.max_total_duration}s). Deteniendo grabación.")
            self.stop()
            return False
        
        #sI SIGUE GRABANDO 
        return True