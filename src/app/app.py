import pygame
import sys
import time
import os
import cv2
from datetime import datetime
from src.camera.camera import Camera

class GestureRecorderApp:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tomador de Datos de Gestos de La Mano")
        
        self.camera = Camera()
        self.camera.initialize_camera()
        

        self.colors = {
            "background": (30, 30, 30),
            "button_ready": (0, 150, 0),
            "text_countdown": (255, 165, 0),
            "signal_recording": (255, 0, 0),
            "text": (255, 255, 255)
        }
        
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        self.button_rect = pygame.Rect(300, 450, 200, 60)
        

        self.data_folder = "gesture_data"
        os.makedirs(self.data_folder, exist_ok=True)


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
        return True
                
    def draw(self):
        #DEBEMOS SIEMPRE POR CADA TICK RELLENAR EL FONDO DE NEGRO PARA "LIMPIAR LA IAMGEN"
        #Pensa que por cada tick se "suponerpone" la imagen anterior para generar sensacion de movimiento en la app
        self.screen.fill(self.colors["background"])

        if self.camera:
            frame = self.camera.get_preview_frame()
            if frame is not None:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #Cambiamos a RGB

                #Pygame espera ancho y alto
                frame_surface = pygame.surfarray.make_surface(frame_rgb.swapaxes(0, 1)) #Cambiamos de lugar ancho y alto de la camra
                
                # Creamos superficie donde colocar la imagen
                frame_surface = pygame.transform.scale(frame_surface, (640, 480))
                self.screen.blit(frame_surface, (80, 100)) #Y la pegamos



    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            running = self.handle_events()

            self.draw()

            pygame.display.flip()

            clock.tick(30) 
        
        pygame.quit()
        sys.exit()