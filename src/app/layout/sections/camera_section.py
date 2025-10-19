import pygame
import cv2

class CameraSection:
    def __init__(self, screen, camera):
        self.screen = screen
        self.camera = camera


    def draw_camera(self,position):
            if self.camera:
                frame = self.camera.get_preview_frame()
                if frame is not None:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #Cambiamos a RGB

                    #Pygame espera ancho y alto
                    frame_surface = pygame.surfarray.make_surface(frame_rgb.swapaxes(0, 1)) #Cambiamos de lugar ancho y alto de la camra
                    
                    # Creamos superficie donde colocar la imagen
                    frame_surface = pygame.transform.scale(frame_surface, (self.screen.get_width()//2, 400))
                    self.screen.blit(frame_surface, position) #Y la pegamos