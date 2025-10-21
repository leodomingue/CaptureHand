import pygame
import cv2

class CameraSection:
    def __init__(self, screen, camera, width, height, margin_x, margin_y):
        self.screen = screen
        self.camera = camera
        self.width = width
        self.height = height
        self.margin_x = margin_x
        self.margin_y = margin_y


    def draw_camera(self,position):
        if self.camera:
            frame = self.camera.get_preview_frame()
            if frame is not None:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #Cambiamos a RGB

                #Pygame espera ancho y alto
                frame_surface = pygame.surfarray.make_surface(frame_rgb.swapaxes(0, 1)) #Cambiamos de lugar ancho y alto de la camra
                
                # Creamos superficie donde colocar la imagen
                frame_surface = pygame.transform.scale(frame_surface, (self.width, self.height))
                final_position = (position[0] + self.margin_x, position[1] + self.margin_y)
                self.screen.blit(frame_surface, final_position) #Y la pegamos

                camera_rect = pygame.Rect(final_position[0], final_position[1], self.width, self.height)
        return camera_rect
        